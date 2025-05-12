from tkinter import *
from tkinter import ttk
import threading
from playwright.sync_api import sync_playwright
import os
import sys
import re
import time

# Set the browsers path for Playwright
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    base_path = sys._MEIPASS
    browsers_dir = os.path.join(base_path, 'browsers')
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))
    browsers_dir = os.path.join(base_path, 'browsers')

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browsers_dir


def on_select(event):
    extraWaitTime.set(int(waitTimeCombo.get()))


def toggle_show_unavailable(page):
    # 1) find all the “More actions” buttons
    buttons = page.locator('button[aria-label="More actions"]')
    count = buttons.count()
    if count < 2:
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', "- Can't find the playlist 'More actions' button\n", "red_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")
        return

    # 2) pick the second one (index 1)
    more_btn = buttons.nth(1)

    # 3) ensure it’s in view & clickable
    more_btn.scroll_into_view_if_needed()
    more_btn.wait_for(state="visible", timeout=5_000)
    more_btn.click()
    logTextWidget.config(state="normal")
    logTextWidget.insert('end', "✔ Clicked playlist 'More actions' button\n", "green_text")
    logTextWidget.see(END)
    logTextWidget.config(state="disabled")
    # 4) click the “Show unavailable videos” item
    try:
        item = page.locator('yt-list-item-view-model >> text=Show unavailable videos')
        item.wait_for(state="visible", timeout=5_000)  # Increased timeout
        item.click()
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', "✔ Clicked 'Show unavailable videos'\n", "green_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")
    except:
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', "- Can’t find the 'Show unavailable videos' button\n", "red_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")
    # Give YouTube a sec to update the list
    page.wait_for_timeout(1_000)


def scroll_to_bottom(page):
    previous_count = 0
    logTextWidget.config(state="normal")
    logTextWidget.insert('end', f"waiting {1 + extraWaitTime.get()} "
                                f"{'seconds...' if 1 + extraWaitTime.get() != 1 else 'second... '}", "yellow_text")
    logTextWidget.see(END)
    logTextWidget.config(state="disabled")
    time.sleep(1 + extraWaitTime.get())
    current_count = page.locator('ytd-playlist-video-renderer').count()
    logTextWidget.config(state="normal")
    logTextWidget.insert('end', f"   [0] Loaded videos: {current_count}\n", "white_text")
    logTextWidget.see(END)
    logTextWidget.config(state="disabled")
    for i in range(18):  # max scroll attempts (if it scrolls more than 18 times => playlist has 1800+ videos)
        page.mouse.wheel(0, 20000)  # scrolls like a bajillion lines to reach the bottom
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', f"waiting {3 + extraWaitTime.get()} seconds...", "yellow_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")
        time.sleep(3 + extraWaitTime.get())

        current_count = page.locator('ytd-playlist-video-renderer').count()
        logTextWidget.config(state="normal")
        if current_count == previous_count:
            logTextWidget.insert('end', f"   [{i+1}] All videos loaded\n", "white_text")
            logTextWidget.see(END)
            break

        logTextWidget.insert('end', f"   [{i + 1}] Loaded videos: {current_count}\n", "white_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")

        previous_count = current_count


def accept_form(page):  # finds and clicks "Reject all" in the form asking to allow cookies
    for frame in page.frames:
        if "consent" in frame.url:
            try:
                button = frame.locator("button:has-text('Reject all')").first
                button.click(timeout=5000)
                logTextWidget.config(state="normal")
                logTextWidget.insert('end', "✔ Clicked \"Reject all\" to cookies popup\n", "green_text")
                logTextWidget.see(END)
                logTextWidget.config(state="disabled")
                return True
            except:
                pass
    return False

def writepagein(page, file):
    html = page.content()  # Copy and paste the page in public.html
    with open(file, "w", encoding="utf-8") as f:
        f.write(html)


def get_full_youtube_playlist_htmls(playlist_url):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)  # set to False to see in real time what the script does
            context = browser.new_context()
            page = context.new_page()
            page.goto(playlist_url)
        except:
            logTextWidget.config(state="normal")
            logTextWidget.insert('end', f"- Possible timeout-error while loading the page\n", "red_text")
            logTextWidget.insert('end', f"continuing anyway...\n\n", "yellow_text")
            logTextWidget.see(END)
            logTextWidget.config(state="disabled")
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', f"waiting {extraWaitTime.get() if extraWaitTime.get() > -1 else 0} "
                                    f"{'seconds' if extraWaitTime.get() != 1 else 'second '} for form to load...\n",
                             "yellow_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")

        time.sleep(extraWaitTime.get() if extraWaitTime.get() > -1 else 0)
        # Accept cookie banner if it appears
        if not accept_form(page):
            logTextWidget.config(state="normal")
            logTextWidget.insert('end', f"- Form not found\n",
                                 "red_text")
            logTextWidget.config(state="disabled")

        # Wait for page to load after accepting form
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', f"waiting {5 + extraWaitTime.get()} seconds for page to load...\n", "yellow_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")

        time.sleep(7 + extraWaitTime.get())

        # Load all videos in the playlist
        scroll_to_bottom(page)
        writepagein(page, "playlist_public.html")

        toggle_show_unavailable(page)
        scroll_to_bottom(page)
        writepagein(page, "playlist_all.html")

        browser.close()


def is_youtube_playlist_url(url):
    return bool(re.search(r"youtube\.com/playlist\?list=", url)) and (url.find("youtube") == 0 or url.find("https") == 0)


def script():
    runScriptButton.config(state="disabled")
    URL = URLField.get().strip()
    if not is_youtube_playlist_url(URL):
        runScriptButton.config(state="normal")
        URLValidationMessage.config(text="invalid URL", fg="#ff9393")
        return
    if URL.find("https://") == -1:
        URL = "https://" + URL
    URL = URL.replace("https://music.youtube.com", "https://www.youtube.com")
    scriptState.config(text=f"program running...", fg="#ffec93")
    URLValidationMessage.config(text=f"valid URL", fg="#c9ffcb")
    # Start the browser and copy the HTML files into playlist_all and playlist_public
    html_recovered = True
    try:
        get_full_youtube_playlist_htmls(URL)
    except:
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', "\n❌ Something went wrong with the browser popup\n", "red_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")
        scriptState.config(text=f"program stopped", fg=FG_LOG_ERROR)
        html_recovered = False
    if html_recovered:
        # Read from the html files create list of public and unavailable+public songs
        PLAYLIST_TITLE = '<title>'
        VIDEO_TITLE = '<a id="video-title" class="yt-simple-endpoint style-scope ytd-playlist-video-renderer"'
        INDEX_CONTAINER = '<div id="index-container" class="playlist-drag-handle style-scope ytd-playlist-video-renderer">'
        VIDEO_AUTHOR = '<a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="'
        f_public = open("playlist_public.html", 'r', encoding='utf-8')
        f_all = open("playlist_all.html", 'r', encoding='utf-8')
        list_of_public_songs = []
        list_of_all_songs = []
        # finds the playlist title
        lines = iter(f_public)
        playlist_title = None
        for line in lines:
            if PLAYLIST_TITLE in line:
                clean_line = line.strip()
                start_index = clean_line.find(PLAYLIST_TITLE) + len(PLAYLIST_TITLE)
                end_index = clean_line.find(" - YouTube", start_index)
                playlist_title = clean_line[start_index:end_index]
                if len(playlist_title) > 150:
                    playlist_title = None
                break
        # filters public songs from playlist_public.html (site code)
        f_public = open("playlist_public.html", 'r', encoding='utf-8')
        lines = iter(f_public)
        for line in lines:
            if VIDEO_TITLE in line:
                clean_line = line.strip()
                end_title_index = clean_line[94:].find('"')
                video_title = clean_line[94:(94 + end_title_index)]
                video_link = "https://www.youtube.com" + clean_line[94 + end_title_index + 8: 94 + end_title_index + 28]
                channel_name = ""
                channel_link = ""
                while INDEX_CONTAINER not in line:
                    if VIDEO_AUTHOR in line:
                        clean_line = line.strip()
                        link_index = clean_line.find('spellcheck="false"') + 25
                        end_link_index = link_index + clean_line[link_index:].find('"')
                        channel_link = ("https://www.youtube.com" +
                                        clean_line[link_index: end_link_index])
                        channel_name = clean_line[
                                       end_link_index + 2: end_link_index + clean_line[end_link_index:].find("</a>")]
                        break
                    line = next(lines, None)
                    if line is None:
                        break

                list_of_public_songs.append((video_title, video_link, channel_name, channel_link))
        f_public.close()

        # filters all songs from playlist_all.html (site code)
        lines = iter(f_all)
        for line in lines:
            if VIDEO_TITLE in line:
                clean_line = line.strip()
                end_title_index = clean_line[94:].find('"')
                video_title = clean_line[94:(94 + end_title_index)]
                video_link = "https://www.youtube.com" + clean_line[94 + end_title_index + 8: 94 + end_title_index + 28]
                channel_name = ""
                channel_link = ""
                while INDEX_CONTAINER not in line:
                    if VIDEO_AUTHOR in line:
                        clean_line = line.strip()
                        link_index = clean_line.find('spellcheck="false"') + 25
                        end_link_index = link_index + clean_line[link_index:].find('"')
                        channel_link = ("https://www.youtube.com" +
                                        clean_line[link_index: end_link_index])
                        channel_name = clean_line[
                                       end_link_index + 2: end_link_index + clean_line[end_link_index:].find("</a>")]
                        break
                    line = next(lines, None)
                    if line is None:
                        break
                list_of_all_songs.append((video_title, video_link, channel_name, channel_link))
        f_all.close()
        # comparing the two lists, finding and printing the unavailable videos
        total_missing = 0
        song_index = 0
        temp = []

        # weird ?multiple copies of songs? glitch that happened once <bruteforce fix> but ruins video count if
        # a video appears multiple times in the playlist

        # for song in list_of_all_songs:
        #     if song not in temp:
        #         temp.append(song)
        # list_of_all_songs = temp

        textWidget.config(state='normal')
        textWidget.insert('end', f"[PLAYLIST] ", "yellow_text")
        if playlist_title is not None:
            textWidget.insert('end', f"\"{playlist_title}\"\n\n", "white_text")
        else:
            textWidget.insert('end', "<error: couldn't fetch playlist title>\n\n", "orange_text")
        if list_of_all_songs != list_of_public_songs:
            textWidget.insert('end', "[UNAVAILABLE VIDEOS]\n\n", "yellow_text")

        for song in list_of_all_songs:
            song_index += 1
            if song not in list_of_public_songs:
                total_missing += 1
                textWidget.insert('end', f"{song_index}.\"{song[0]}\"\n", "white_text")
                textWidget.insert('end', f"{song[1]}\n", "blue_text")
                textWidget.insert('end', f"{song[2]}\n", "white_text")
                textWidget.insert('end', f"{song[3]}\n\n", "blue_text")
        textWidget.insert('end', f"missing videos: {total_missing}/{song_index}\n")
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', "✔ Program ended successfully\n", "green_text")
        logTextWidget.see(END)
        logTextWidget.config(state="disabled")
        textWidget.insert('end', "\n=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n\n", "white_text")
        scriptState.config(text=f"program finished!", fg="#93ffb2")
    else:
        logTextWidget.config(state="normal")
        logTextWidget.insert('end', "❌ Program crashed\n", "red_text")
        logTextWidget.config(state="disabled")

    logTextWidget.config(state="normal")
    logTextWidget.insert('end', "\n=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n\n", "white_text")
    logTextWidget.see(END)
    logTextWidget.config(state="disabled")
    runScriptButton.config(state="normal")
    textWidget.see(END)
    textWidget.config(state='disabled')


    # Delete the temporary HTML files
    try:
        os.remove("playlist_public.html")
        os.remove("playlist_all.html")
    except FileNotFoundError:
        pass # Ignore if already deleted or never created


def runScript():
    threading.Thread(target=script).start()


def copyOutput():
    textWidget.config(state='normal')
    text = textWidget.get("1.0", "end-1c")  # Get all text, excluding trailing newline
    textWidget.config(state='disabled')

    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


BG_WINDOW = "#2b2d30"
BG_WIDGET = "#1e1f22"
FG_TEXT = "#ffffff"
FG_TEXT_ERROR = "orange"
FG_TEXT_YELLOW_HIGHLIGHT = "#fff582"
FG_TEXT_GREEN_HIGHLIGHT = "#5caa72"
FG_LINK = '#93b7ff'
FG_LOG_THINKING = '#ffda58'
FG_LOG_SUCCESS = '#74ff7a'
FG_LOG_ERROR = '#ff4700'

# === ROOT WINDOW SETUP ===
root = Tk()
root.configure(bg=BG_WINDOW)
root.title("YouTube Unavailable Video Scraper")
try:
    root.iconbitmap('assets/icons/icon.ico')
except TclError:
    pass
root.geometry("900x500")
root.minsize(700, 400)
root.configure(padx=10, pady=10)

# Use modern ttk theme
style = ttk.Style(root)
style.theme_use('clam')  # Alternatives: 'clam', 'alt', 'default', 'vista' on Windows

# Style ttk widgets
style.configure("TFrame", background=BG_WINDOW)
style.configure("TLabel", background=BG_WIDGET, foreground=FG_TEXT)
style.configure("TButton", background=BG_WIDGET, foreground=FG_TEXT)
style.map("TButton", background=[("active", "#3a3b3f")])
style.configure("TEntry", fieldbackground=BG_WIDGET, foreground=FG_TEXT)
style.configure("TLabelframe", background=BG_WINDOW, foreground=FG_TEXT)
style.configure("TLabelframe.Label", background=BG_WINDOW, foreground=FG_TEXT)
style.configure("Vertical.TScrollbar", background=BG_WIDGET, troughcolor=BG_WINDOW)
style.configure("Horizontal.TScrollbar", background=BG_WIDGET, troughcolor=BG_WINDOW)

# === TOP INPUT FRAME ===
inputFrame = ttk.Frame(root)
inputFrame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
inputFrame.columnconfigure(0, weight=1)

URLField = ttk.Entry(inputFrame)
URLField.grid(row=0, column=0, sticky="ew", padx=(0, 10))

runScriptButton = ttk.Button(inputFrame, text="Find Unavailable Videos", command=runScript)
runScriptButton.grid(row=0, column=1)

# === VALIDATION & STATUS MESSAGES ===
statusFrame = ttk.Frame(root)
statusFrame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
statusFrame.columnconfigure((0, 1), weight=1)

URLValidationMessage = Label(statusFrame, fg="red", bg=BG_WINDOW, anchor="w")
URLValidationMessage.grid(row=0, column=0, sticky="w")

scriptState = Label(statusFrame, fg="#ffec93", bg=BG_WINDOW, anchor="e")
scriptState.grid(row=0, column=1, sticky="e")

# === OUTPUT AND LOG AREA ===
contentFrame = ttk.Frame(root)
contentFrame.grid(row=2, column=0, columnspan=2, sticky="nsew")
contentFrame.columnconfigure((0, 1), weight=1)
contentFrame.rowconfigure(0, weight=1)

# Output Frame
textFrame = ttk.LabelFrame(contentFrame, text="Unavailable Video Links")
textFrame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
textFrame.rowconfigure(0, weight=1)
textFrame.columnconfigure(0, weight=1)

textWidget = Text(textFrame, wrap='word', height=10,
                  bg=BG_WIDGET, fg=FG_TEXT, insertbackground=FG_TEXT,
                  highlightbackground=BG_WIDGET, highlightcolor=BG_WIDGET)
textWidget.grid(row=0, column=0, sticky='nsew')
textWidget.tag_configure("white_text", foreground=FG_TEXT)
textWidget.tag_configure("blue_text", foreground=FG_LINK)
textWidget.tag_configure("yellow_text", foreground=FG_TEXT_YELLOW_HIGHLIGHT)
textWidget.tag_configure("orange_text", foreground=FG_TEXT_ERROR)

scrollbar = ttk.Scrollbar(textFrame, orient='vertical', command=textWidget.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
textWidget.configure(yscrollcommand=scrollbar.set)
textWidget.config(state='disabled')

# Log Frame
logFrame = ttk.LabelFrame(contentFrame, text="Runtime Logs")
logFrame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
logFrame.rowconfigure(0, weight=1)
logFrame.columnconfigure(0, weight=1)

logTextWidget = Text(logFrame, wrap='word', height=10,
                     bg=BG_WIDGET, fg=FG_TEXT, insertbackground=FG_TEXT,
                     highlightbackground=BG_WIDGET, highlightcolor=BG_WIDGET)
logTextWidget.grid(row=0, column=0, sticky='nsew')
logTextWidget.tag_configure("white_text", foreground=FG_TEXT)
logTextWidget.tag_configure("yellow_text", foreground=FG_LOG_THINKING)
logTextWidget.tag_configure("green_text", foreground=FG_LOG_SUCCESS)
logTextWidget.tag_configure("red_text", foreground=FG_LOG_ERROR)

logScrollbar = ttk.Scrollbar(logFrame, orient='vertical', command=logTextWidget.yview)
logScrollbar.grid(row=0, column=1, sticky='ns')
logTextWidget.configure(yscrollcommand=logScrollbar.set)
logTextWidget.config(state='disabled')

# === COPY BUTTON ===
copyButton = ttk.Button(root, text="Copy Output", command=copyOutput)
copyButton.grid(row=3, column=0, sticky="w", pady=(10, 0))

# Allow window to resize nicely
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure((0, 1), weight=1)


# === EXTRA TIME DROPDOWN FIELD ===

wait_time_frame = Frame(root, bg=BG_WINDOW)
wait_time_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Label
WaitTimeLabel = Label(wait_time_frame, text="Videos not loading? Add extra wait time(seconds):", bg=BG_WINDOW, fg="white")
WaitTimeLabel.pack(side="left", padx=(0, 10))

numbers = list(str(x) for x in range(-1, 41))

# Combobox
waitTimeCombo = ttk.Combobox(wait_time_frame, values=numbers, style="Custom.TCombobox", state="readonly")
waitTimeCombo.set(0)

waitTimeCombo.pack(side="left")
extraWaitTime = IntVar()
extraWaitTime.set(int(waitTimeCombo.get()))

waitTimeCombo.bind("<<ComboboxSelected>>", on_select)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)


root.mainloop()