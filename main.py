import os, tkinter, time
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pytube import YouTube 
from threading import Thread

def dlVideo(link: str, videoLabel: tkinter.Label, videoProg: ttk.Progressbar):
    print('Downloading video')
    videoProg['value'] = 0
    videoLabel['text'] = f'0/1 | 0%'
    window.update_idletasks()
    try:
        yt = YouTube(link)
        # check if mp3 file exists
        title = yt.title.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('\'', '').replace('.', '')
        if os.path.isfile(f'{destination}\\{title}.mp3'):
            pass
        else:
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=destination, filename=title)
            base, ext = os.path.splitext(out_file) 
            new_file = base + '.mp3'
            os.rename(out_file, new_file) 

            videoProg['value'] = 100
            videoLabel['text'] = f'1/1 | 100%'
            window.update_idletasks()

    except:
        pass

def dlPlaylist(link: str, listLabel: tkinter.Label, listProg: ttk.Progressbar, videoLabel: tkinter.Label, videoProg: ttk.Progressbar):
    global listProgress
    print('Downloading playlist')
    listProgress = 0
    listProg['value'] = listProgress
    listLabel['text'] = f'{listProgress}%'
    window.update_idletasks()

    if radioVar.get() == 1:
        driver = webdriver.Chrome()
    elif radioVar.get() == 2:
        driver = webdriver.Firefox()

    driver.get(link)

    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.find_element(By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc iMLaPd"]').click()

    totalVideos = driver.find_element(By.XPATH, '//span[@class="style-scope yt-formatted-string"]').text
    try:
        errorVideos = driver.find_element(By.XPATH, '//yt-formatted-string[@class="style-scope ytd-alert-with-button-renderer"]').text.split(" ")[0]
    except:
        errorVideos = 0

    goodVideos = int(totalVideos) - int(errorVideos)

    listLabel['text'] = f'0/{goodVideos} | {listProgress}%'

    link = []
    cachedVideos = []

    while cachedVideos.__len__() < int(goodVideos):
        cachedVideos = driver.find_elements(By.XPATH, '//ytd-playlist-video-renderer[@class="style-scope ytd-playlist-video-list-renderer"]')
        elem = driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)

        videoProg['value'] = (cachedVideos.__len__()/goodVideos)*100
        videoLabel['text'] = f'{cachedVideos.__len__()}/{goodVideos} | {round((cachedVideos.__len__()/goodVideos)*100, 2)}%'
        window.update_idletasks()

        time.sleep(3)

    links = driver.find_elements(By.XPATH, '//a[@class="yt-simple-endpoint style-scope ytd-playlist-video-renderer"]')
    for l in links:
        link.append(l.get_attribute('href').split('&')[0])

    counter = 0
    agerestricted = []

    for l in link:
        try:
            yt = YouTube(str(l))
            # check if mp3 file exists
            title = yt.title.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('\'', '').replace('.', '')
            if os.path.isfile(f'{destination}\\{title}.mp3'):
                pass
            else:
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=destination, filename=title)
                base, ext = os.path.splitext(out_file) 
                new_file = base + '.mp3'
                os.rename(out_file, new_file) 

        except:
            agerestricted.append(l)

        counter += 1
        listProg['value'] = (counter/goodVideos)*100
        listLabel['text'] = f'{counter}/{goodVideos} | {round((counter/goodVideos)*100, 2)}%'
        window.update_idletasks()
        

def ytDownloader(link: str):
    # check if argument is a link
    if link == '':
        print('No link provided')
        # set input backgroung to red
        inputLink.configure(bg='red')
        return
    
    if 'youtube.com' not in link:
        print('Invalid link')
        # set input backgroung to red
        inputLink.configure(bg='red')
        return
    
    inputLink.configure(bg='lightgreen')
    
    # check if destination is valid is os
    if destination == '':
        print('No destination provided')
        # set input backgroung to red
        inputDest.configure(bg='red')
        return
    
    if not os.path.isdir(destination):
        print('Invalid destination')
        # set input backgroung to red
        inputDest.configure(bg='red')
        return
    
    # Check if link is a playlist or a video
    linkType = link.split('.com/')[1].split('?')[0]
    
    inputDest.configure(bg='lightgreen')


    global labelListProg, progressList, labelVideoProg, progressVideo
    if linkType == 'playlist':
        Thread(target=dlPlaylist, args=(link, labelListProg, progressList, labelVideoProg, progressVideo)).start()
    elif linkType == 'watch':
        Thread(target=dlVideo, args=(link, labelVideoProg, progressVideo)).start()

def selectDestination():
    global destination
    destination = filedialog.askdirectory() 
    inputDest.delete(0, END)
    inputDest.insert(0, destination)

listProgress = 0
videoProgress = 0
destination = ''

# GUI Colors

bgColor = '#333'

# GUI Elements

window = tkinter.Tk()
window.title('Youtube Playlist Downloader By: Kaszabi')
window.geometry('750x500')
window.configure(bg=bgColor)
# window.overrideredirect(True)
window.resizable(False, False)

tkinter.Label(window, text="Select file output:  ", bg=bgColor, fg='white').grid(column=0, row=0, sticky=W) 
inputDest = tkinter.Entry(window, width=50, bg='white', fg='black')
inputDest.grid(column=0, row=0)
btnDest = tkinter.Button(window, text="...", command=lambda: selectDestination(), width=2, height=2, bg=bgColor, fg='white')
btnDest.grid(column=0, row=0, sticky=E)

radioVar = IntVar()
tkinter.Label(window, text="V Select browser V", bg=bgColor, fg='white').grid(column=1, row=0, sticky=W) 
R1 = tkinter.Radiobutton(window, text="Chrome", bg=bgColor, fg='lime', variable=radioVar, value=1)
R1.grid( column=1, row=1, sticky=W )
# autoselect R1
radioVar.set(1)
R2 = tkinter.Radiobutton(window, text="Firefox", bg=bgColor, fg='lime', variable=radioVar, value=2)
R2.grid( column=1, row=1, sticky=E)

tkinter.Label(window, text="Paste your youtube video/playlist link here:  ", bg=bgColor, fg='white').grid(column=0, row=1)                                     
inputLink = tkinter.Entry(window, width=75, bg='white', fg='black')
inputLink.grid(column=0, row=2)

btnDl = tkinter.Button(window, text="Download", command=lambda: ytDownloader(inputLink.get()), width=20, height=2, bg=bgColor, fg='white')
btnDl.grid(column=1, row=2)

progStyle = ttk.Style()
progStyle.theme_use('clam')
progStyle.configure('green.Horizontal.TProgressbar', background='green')

progressList = ttk.Progressbar(window, orient='horizontal', length=500, mode='determinate', style='green.Horizontal.TProgressbar', maximum=100, value=0)
progressList.grid(column=0, row=3, padx=30, pady=30)
labelListProg = tkinter.Label(window, text=f'{listProgress}%', bg=bgColor, fg='white')
labelListProg.grid(column=1, row=3)

progressVideo = ttk.Progressbar(window, orient='horizontal', length=500, mode='determinate', style='green.Horizontal.TProgressbar', maximum=100, value=0)
progressVideo.grid(column=0, row=4, padx=30, pady=30)
labelVideoProg = tkinter.Label(window, text=f'{videoProgress}%', bg=bgColor, fg='white')
labelVideoProg.grid(column=1, row=4)

window.mainloop()
