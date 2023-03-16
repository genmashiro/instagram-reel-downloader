import instaloader
import threading
import PySimpleGUI as sg
from pathlib import Path

# Create an instance of Instaloader class
L = instaloader.Instaloader()

# Define function to download reel
def download_reels(values):
    reel_urls = values['-URLS-'].split('\n')
    for url in reel_urls:
        t = threading.Thread(target=download_reel, args=(url,))
        t.start()

def download_reel(reel_url):
    try:
        post = instaloader.Post.from_shortcode(L.context, reel_url.split("/")[-2])
        L.download_post(post, target=post.owner_username)
    except Exception as e:
        print(f"Error downloading reel: {e}")

# Define GUI layout
layout = [[sg.Text('Enter Instagram Reel URLs (one URL per line):')],
          [sg.Multiline(size=(50, 10), key='-URLS-')],
          [sg.Button('Download Reels'), sg.Button('Exit')]]

# Create GUI window
window = sg.Window('Instagram Reel Downloader', layout)

# Event loop to process "Download Reels" and "Exit" buttons
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Download Reels':
        download_reels(values)
        sg.Popup('Success', 'All reels downloaded successfully.')

# Close GUI window
window.close()