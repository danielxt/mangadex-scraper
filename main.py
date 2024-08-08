import subprocess
from PIL import Image
import os
import pathlib

class MangaOrder:
    def __init__(self, url, start, end):
        self.url = url
        self.start = start
        self.end = end

KINDLE_PATH = "D:\documents"
def main():

    # 0. kindle check
    toKindle = "1" == input("Enter 1 if want to direct to kindle: ")
    
    # 1. fetch orders from user
    url = ""
    orders = []
    while True:
        url = input("Enter mangadex url (enter 'done' to stop): ")
        if url == 'done':
            break
        start = input("Enter start chapter:")
        end = input("Enter end chapter:")
        orders.append(MangaOrder(url, start, end))


    # 2. run downloads
    for order in orders:
        subprocess.run(["py", "-3", "-m", "mangadex_downloader", order.url, "--start-chapter", order.start, "--end-chapter", order.end, "--no-group-name"])
    
    # 3. convert to pdf
    cwd = os.getcwd()
    for name in os.listdir(cwd):
        mangaFolderPath = pathlib.PurePath(cwd, name)
        if os.path.isdir(mangaFolderPath): # top level manga folder e.g: Jigokuraku
            chapterFolders = [pathlib.PurePath(mangaFolderPath, chapterFolder) for chapterFolder in os.listdir(mangaFolderPath) if os.path.isdir(pathlib.PurePath(mangaFolderPath, chapterFolder))]
            images = []
       
            for chapterFolder in chapterFolders:
                for panel in os.listdir(chapterFolder):
                    
                    images.append(Image.open(str(pathlib.PurePath(chapterFolder, panel))).convert('RGB'))
            savePath = f"{name}.pdf"
            if toKindle:
                kindlePath = str(pathlib.PurePath(KINDLE_PATH, savePath))
                images[0].save(kindlePath, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
            else:
                images[0].save(savePath, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
     
                
   

if __name__ == "__main__":
    main()