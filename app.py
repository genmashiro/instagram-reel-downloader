import instaloader
import concurrent.futures
import PySimpleGUI as sg
from pathlib import Path

# Create an instance of Instaloader class
L = instaloader.Instaloader()

# Define function to download reel
def download_reel(reel_url):
    try:
        post = instaloader.Post.from_shortcode(L.context, reel_url.split("/")[-2])
        L.download_post(post, target=post.owner_username)
        return True
    except Exception as e:
        print(f"Error downloading reel: {e}")
        return False

def download_reels(values):
    reel_urls = values['-URLS-'].split('\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_reel, url) for url in reel_urls]
        results = [future.result() for future in futures]

    if all(results):
        sg.Popup('Success', 'All reels downloaded successfully.')
    else:
        sg.Popup('Error', 'One or more reels failed to download.')

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

# Close GUI window
window.close()