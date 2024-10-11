import os, time
# import tkinter
# from tkinter import ttk
# from tkinter import filedialog
# from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pytube import YouTube 
from threading import Thread

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Dev Variables (Disable for build)
testPlaylist = "https://www.youtube.com/playlist?list=PLeKFAv7V8KjyhrQU7tmFLOTt6t53-qJdL"
testDestinasion = 'test'
testDriver = 'firefox'

test = True

def dlVideo(link: str, *args, **kwargs):
    print('Downloading video')
    if not test:
        videoLabel = kwargs.get(videoLabel)
        videoProg = kwargs.get(videoProg)
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

            if not test:
                videoProg['value'] = 100
                videoLabel['text'] = f'1/1 | 100%'
                window.update_idletasks()

    except:
        pass

def dlPlaylist(link: str, *args, **kwargs):

    if not os.path.isdir(destination):
        print('Invalid destination')
    
    print('Downloading playlist')
    if not test:

        listLabel = tkinter.Label(kwargs.get(labelListProg))
        listProg = ttk.Progressbar(kwargs.get(progressList))
        videoLabel = tkinter.Label(kwargs.get(labelVideoProg))
        videoProg = ttk.Progressbar(kwargs.get(progressVideo))

        global listProgress
        listProgress = 0
        listProg['value'] = listProgress
        listLabel['text'] = f'{listProgress}%'
        window.update_idletasks()

        if radioVar.get() == 1:
            driver = webdriver.Chrome()
        elif radioVar.get() == 2:
            driver = webdriver.Firefox()
    
    else: 
        driver = webdriver.Firefox()

    driver.get(link)

    driver.implicitly_wait(0.5)
    driver.maximize_window()
    try:
        driver.find_element(By.XPATH, '//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc Gu558e"]').click()
    except:
        print('Cookie accept btn not found')

    totalVideos = driver.find_elements(By.XPATH, '//span[@class="style-scope yt-formatted-string"]')
    goodVideos = totalVideos.__len__()
    # print(f'TotalVideos: {totalVideos}')
    # for v in totalVideos:
    #     try:
    #         goodVideos = int(v.text)
    #         break
    #     except:
    #         pass
    
    print(f"total vids: {goodVideos}")

    if not test: listLabel['text'] = f'0/{goodVideos} | {listProgress}%'

    link = []
    cachedVideos = []
    videoCount = 0

    while cachedVideos.__len__() < int(goodVideos):
        cachedVideos = driver.find_elements(By.XPATH, '//ytd-playlist-video-renderer[@class="style-scope ytd-playlist-video-list-renderer"]')
        elem = driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        if videoCount != cachedVideos.__len__(): videoCount = cachedVideos.__len__()
        else: goodVideos = cachedVideos.__len__()

        print(f'Cached videos: {cachedVideos.__len__()}')

        if not test:
            videoProg['value'] = (cachedVideos.__len__()/goodVideos)*100
            videoLabel['text'] = f'{cachedVideos.__len__()}/{goodVideos} | {round((cachedVideos.__len__()/goodVideos)*100, 2)}%'
            window.update_idletasks()

        time.sleep(2)

    links = driver.find_elements(By.XPATH, '//a[@class="yt-simple-endpoint style-scope ytd-playlist-video-renderer"]')
    for l in links:
        link.append(l.get_attribute('href').split('&')[0])

    # print(link)

    counter = 0
    agerestricted = []

    for l in link:

        print(f'{counter}/{goodVideos}: {l}')
        yt = YouTube(str(l))
        # check if mp3 file exists
        # print('Getting title')
        try:
            title = yt.title.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('\'', '').replace('.', '')
        except:
            title = f'Errored Title: {l}'
        if os.path.isfile(f'{destination}/{title}.mp3'):
            print(f'{destination}/{title}.mp3 exists')
            counter += 1
        else:
            try:
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=destination, filename=title)
                base, ext = os.path.splitext(out_file) 
                new_file = base + '.mp3'
                os.rename(out_file, new_file) 
                print(new_file)
                counter += 1
            except:
                print(f'Errored Title: {title}')
                counter += 1

        if not test:
            counter += 1
            listProg['value'] = (counter/goodVideos)*100
            listLabel['text'] = f'{counter}/{goodVideos} | {round((counter/goodVideos)*100, 2)}%'
            window.update_idletasks()
        

def ytDownloader(link: str):
    # check if argument is a link
    if not test:
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

        inputDest.configure(bg='lightgreen')
    else: 
        if not os.path.isdir(destination):
            print('Invalid destination')
    # Check if link is a playlist or a video
    linkType = link.split('.com/')[1].split('?')[0]
    
    if not test:
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

if test:

    destination = testDestinasion
    dlPlaylist(testPlaylist)
    

else:
    listProgress = 0
    videoProgress = 0
    destination = ''

    # GUI Colors

    bgColor = '#333'

    # GUI Elements

    window = tkinter.Tk()
    window.title('Youtube Playlist Downloader By: Kaszabi')
    window.geometry('1000x500')
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
