VIDEO_TITLE = '<a id="video-title" class="yt-simple-endpoint style-scope ytd-playlist-video-renderer"'
INDEX_CONTAINER = '<div id="index-container" class="playlist-drag-handle style-scope ytd-playlist-video-renderer">'
VIDEO_AUTHOR = '<a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="'
f_public = open("public_html.in", 'r', encoding='utf-8')
f_private = open("all_html.in", 'r', encoding='utf-8')
list_of_public_songs = []
list_of_all_songs = []

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
                channel_name = clean_line[end_link_index+2: end_link_index + clean_line[end_link_index:].find("</a>")]
                break
            line = next(lines, None)
            if line is None:
                break

        list_of_public_songs.append((video_title, video_link, channel_name, channel_link))

lines = iter(f_private)
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
                channel_name = clean_line[end_link_index+2: end_link_index + clean_line[end_link_index:].find("</a>")]
                break
            line = next(lines, None)
            if line is None:
                break

        list_of_all_songs.append((video_title, video_link, channel_name, channel_link))

total_missing = 0
song_index = 0
temp = []

# weird ?multiple copies of songs? glitch fix:
for song in list_of_all_songs:
    if song not in temp:
        temp.append(song)
list_of_all_songs = temp

for song in list_of_all_songs:
    song_index += 1
    if song not in list_of_public_songs:
        total_missing += 1
        print(f"{song_index}.\"{song[0]}\"\n{song[1]}\n{song[2]}\n{song[3]}\n")

print(f"missing videos: {total_missing}/{song_index}")
