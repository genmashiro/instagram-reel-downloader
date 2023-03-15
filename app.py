import instaloader
import threading
import tkinter as tk
from tkinter import messagebox

# Create an instance of Instaloader class
L = instaloader.Instaloader()

# Create GUI window
root = tk.Tk()
root.title("Instagram Reel Downloader")

# Define function to download reel
def download_reels():
    reel_urls = url_entry.get("1.0", "end-1c").split("\n")
    threads = []
    for url in reel_urls:
        t = threading.Thread(target=download_reel, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    messagebox.showinfo("Success", "All reels downloaded successfully.")

def download_reel(reel_url):
    try:
        post = instaloader.Post.from_shortcode(L.context, reel_url.split("/")[-2])
        L.download_post(post, target=post.owner_username)
    except Exception as e:
        print(f"Error downloading reel: {e}")

# Create GUI elements
url_label = tk.Label(root, text="Enter Instagram Reel URLs (one URL per line):")
url_entry = tk.Text(root, width=50, height=10)
download_button = tk.Button(root, text="Download Reels", command=download_reels)

# Add GUI elements to window
url_label.pack()
url_entry.pack()
download_button.pack()

root.mainloop()
