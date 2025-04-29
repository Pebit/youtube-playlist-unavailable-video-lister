# YouTube Playlist - Unavailable Video Lister
A simple Python script to **find and list unavailable videos** in a YouTube playlist by comparing its HTML before and after unavailable videos are revealed.  
Want to skip the wall of text? Watch the video tutorial:  https://youtu.be/aC80fCiigCk?si=ftrKo5w2KRKkIVaa
MediaFire download: https://www.mediafire.com/file/5t66243lr5j0oql/youtube-playlist-unavailable-video-scraper.zip/file  
## 📜 What It Does
Given:
- The public HTML of a YouTube playlist (before unavailable videos are shown)
  
- The private HTML of the same playlist (after unavailable videos are shown)
  
This script:
  
- Sifts through both HTML files.
- Compares the available vs. all videos.
- Identifies missing/unavailable videos.
- Outputs for each missing video in the following format:
  -Position in the playlist
  -Title (if available)
  -Video link
  -Channel name (if available)
  -Channel link (if available)
  
Here's an example: the 4th video in the playlist is unavailable
![image](https://github.com/user-attachments/assets/afe59608-e319-4004-97b2-981b32f167b3)
the script will output the following:  
> 4."bad"  
> https://www.youtube.com/watch?v=B7RTFjbg_7k  
> wave to earth  
> https://www.youtube.com/channel/UCBJNpcJaUcVyw4LlqGRMpcQ  
  
  
  
At the end, it also summarizes how many videos were missing out of the total.  
example: "missing videos: 7/54"
## 🛠️ How To Use
1. Export the playlist's HTML before showing unavailable videos (on the playlist page: right-click → InspectElement → copy the entire _\<body\>_ → paste into _public_html.in_).
![image](https://github.com/user-attachments/assets/dd2d9136-7958-4c37-bd1f-0199c9e3f11a)
![image](https://github.com/user-attachments/assets/329ae823-6a75-4ac8-ba9a-c9264f9745a8)  
  
  
  
3. Toggle shown unavailable videos by hitting the three dots symbol next your playlist cover image and clicking  "Show unavailable videos"
![image](https://github.com/user-attachments/assets/3ec20d37-5023-442e-a5a2-151eafb260af)


   
4. Export the playlist's HTML after showing unavailable videos (same method → paste into all_html.in).
![image](https://github.com/user-attachments/assets/12d7d874-c335-4fb5-8a52-00a4db6fa3d3)
![image](https://github.com/user-attachments/assets/9b9cc1a3-2db5-49a4-a493-39b6a1738d5e)


  
5. Place both files (public_html.in, all_html.in) in the same directory as the script (if they are not already there for some reason).
![image](https://github.com/user-attachments/assets/7c7e97c1-6c89-4a46-8058-d3536f6bf84f)


  
6. Run the script: open a terminal in the same folder you have the script and type "python main.py"
![image](https://github.com/user-attachments/assets/fef06154-dcf5-42e1-a16a-7629bb0b91a2)
![image](https://github.com/user-attachments/assets/7549b6f0-104b-4a08-89f8-71e320fb2d34)


  
7. The script will print information about all unavailable videos directly in the console.


  
8. (optional) If it doesn't work you probably don't have python installed.  
  Here's the official page for python downloads where you can get the newest version:
  https://www.python.org/downloads/


  
9. There may be videos that appear like the following (or similar):  
> 37."[Deleted video]"  
> https://www.youtube.com/watch?v=8RSvUTG4Jfc  
  
  To recover these, paste the url given on the site [Wayback Machine](https://web.archive.org).  
  This site stores older versions of urls and most somewhat popular videos are stored here!  
  If the video isn't up, there's a high chance you'll at least find the title and possibly a thumbnail.  

## 📂 Files
- main.py — The main script.  
- public_html.in — HTML content of the playlist before showing unavailable videos.  
- all_html.in — HTML content of the playlist after showing unavailable videos.  

##⚡ Notes
- The script assumes **UTF-8 encoding** for input files.
- It handles a rare YouTube glitch that happens to me once where multiple identical entries for a song may appear.
- This is a **manual comparison tool**; it does not directly fetch playlist data from YouTube servers.




