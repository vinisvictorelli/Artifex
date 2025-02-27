import os

def download_file(url, dest):
    os.system(f"yt-dlp -o {dest} -f mp4 {url}")


if __name__ == "__main__":
    download_file("https://www.youtube.com/watch?v=ZbZSe6N_BXs", "test.mp4")