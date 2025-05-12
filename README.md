# YouTube Playlist - Unavailable Video Lister
A tool written in Python to **find and list unavailable videos** in a YouTube playlist by comparing its HTML before and after unavailable videos are revealed.  
Want to skip the wall of text? Watch the video tutorial:  (coming soon)  
MediaFire download: https://www.mediafire.com/file/n5z9hcrpl1sxfdq/youtube-playlist-unavailable-video-lister.zip/file
## What It Does
Given:
- The Playlist URL
- (optional) number of seconds extra wait time (for slower internet connections) 
  
This script:
  
- Sifts through both HTML files of the page (one with and one without the unavailable videos).
- Compares the available vs. all videos.
- Identifies missing/unavailable videos.
- Outputs for each missing video in the following format:  
  - Position in the playlist  
  - Title (if available)  
  - Video link  
  - Channel name (if available)  
  - Channel link (if available)  
  
Here's an example (the 4th video in the playlist is unavailable)
![image](https://github.com/user-attachments/assets/afe59608-e319-4004-97b2-981b32f167b3)
the script will output the following:  
```
4."bad"  
https://www.youtube.com/watch?v=B7RTFjbg_7k  
wave to earth  
https://www.youtube.com/channel/UCBJNpcJaUcVyw4LlqGRMpcQ  
```
  
  
At the end, it also summarizes how many videos were missing out of the total.  
example:
```
missing videos: 7/54  
```
## How To Use
### 1. Run the "youtube_unavailable_scraper.exe". These windows should appear on the screen:
<img src="https://github.com/user-attachments/assets/5a0818e7-a4a3-43ce-aff8-12e444a58e50" width="75%" />

  
  
### 2. Inside the field at the top paste your playlist url, and then press the button on the right side of the field:
<img src="https://github.com/user-attachments/assets/6a08d55b-c3f7-4e53-b064-afe4ba01e44c" width="75%" />




   
### 3. Don't click anything or scroll on the browser popup or the script might not work properly!  
Things you can still do to the browser window:
- resize the window
- move the window
- open other windows on top of the running program
- **unsure:** minimize the window (_might affect the program but all previous tests have given the correct output_)
<img src="https://github.com/user-attachments/assets/b15cd853-115d-4348-bb4b-66134684f9d0" width="75%" />



  
### 4. Profit
shortly after the browser is automatically closed by the program, a list of all unavailable videos will be printed on the "Unavailable Video Links" field that you can copy by pressing the button underneeth it
<img src="https://github.com/user-attachments/assets/e774719b-4ed0-4311-909b-5ad681bc1617" width="75%" />

  
### 5. paste the list wherever it's easier for you to read (ex: on a private discord chat)
<img src="https://github.com/user-attachments/assets/59d08140-89f0-40ec-af37-702ecde57030" width="75%" />

### 6. There may be videos that appear like the following (or similar):  
```
37."[Deleted video]"  
https://www.youtube.com/watch?v=8RSvUTG4Jfc  
```
  To recover these, paste the url given on the site [Wayback Machine](https://web.archive.org).  
  This site stores older versions of urls and most somewhat popular videos are stored here!  
  If the video isn't up, there's a high chance you'll at least find the title and possibly a thumbnail.  
  
## (optional) How to create the .exe  ( warning: kinda hard, eta: 15-20mins )
For the scheptics who don't trust the exe I already built, you can build your own exe file from the source code "youtube_unavailable_scraper.py" by following these steps :
### 1. Open PowerShell Terminal inside the folder containing the .py file
```Bash
pip install playwright
pip install pyinstaller
```
### 2. Now on the same Terminal you'll want to create the executable with pyinstaller. 

For that you'll need to add the data about the browser that playwright will use and the binaries for playwright. (playwright is the python library managing interactions between program and browser)

2.1 To find the binaries locate the python package "playwright" on your pc. 
Usually it's somewhere like:
```
C:\users\YOURUSERNAME\appdata\local\programs\python\python311\lib\site-packages\playwright
```
from there navigate to driver\package\bin, so your final path should look like:
```
C:\users\YOURUSERNAME\appdata\local\programs\python\python311\lib\site-packages\playwright\driver\package\bin
```
If you can't find it, literally ask ChatGPT how to find it

2.2 The browser is already in the directory with the .py file (if you cloned the github repo right)
You'll want to have a path like this for it ready:
```
"(...)\youtube-playlist-unavailable-video-lister\browsers\chromium-1169;browsers\chromium-1169"
```

2.3 Now that you have the two paths, replace them in this command:
```Bash
pyinstaller --onefile --add-data "(...)\youtube-playlist-unavailable-video-lister\browsers\chromium-1169;browsers\chromium-1169" --add-data "(...)\playwright\driver\package\bin;playwright\driver\package\bin" ".\youtube_unavailable_scraper.py"
```
for example, this is how it looks for me:
```Bash
pyinstaller --onefile --add-data "C:\CodingProjects\youtube-playlist-unavailable-video-lister\browsers\chromium-1169;browsers\chromium-1169" --add-data "C:\Users\Andrei\AppData\Local\Programs\Python\Python311\Lib\site-packages\playwright\driver\package\bin;playwright\driver\package\bin" ".\youtube_unavailable_scraper.py"
```

### 3. At the moment of posting (11th of May 2025) the tool uses the latest version of chromium that works with the playwright libraries... but a future version of playwright might not be compatible with the browser I have already saved under /browsers in the folder.
If I haven't updated the browser directory to work for the current version of playwright, install the most recent working chromium ver using:
```Bash
playwright install chromium
```
then locate the browser   
should be a folder in  
```
C:\Users\YOURUSER\AppData\Local\ms-playwright  
```
under the name _"chromium-XXXX"_.  

copy that folder and replace the folder in the ./browsers directory with that one
<img src="https://github.com/user-attachments/assets/88335ab7-da99-4663-a19c-5d572084b065" width="75%" />

now you're good to go and can try running the pyinstaller command again to make the .exe file:
```
pyinstaller --onefile --add-data "(...)\youtube-playlist-unavailable-video-lister\browsers\chromium-XXXX;browsers\chromium-XXXX" --add-data "(...)\playwright\driver\package\bin;playwright\driver\package\bin" ".\youtube_unavailable_scraper.py"
```
## Thanks for visiting my app and have fun restoring your playlists!
If any bugs are found feel free to message me 
Discord: "pebitandreiutz" (I will respond in like a day)
Emai: "andrei.vio.ionescu@gmail.com" (I will respond 1 month later)
