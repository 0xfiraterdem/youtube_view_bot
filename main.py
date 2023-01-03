import time
from tkinter import ttk
from tkinter import *

from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extension import proxies
from PIL import Image, ImageTk
import tkinter.messagebox as MessageBox

import pyautogui

height = pyautogui.size()[1]
width = pyautogui.size()[0]
window = Tk()
window.title("YouTube Bot")
window.config(bg='#363636')

username = 'username'
password = 'password'
endpoint = 'Proxy ip'
port = 'Port'
website1 = 'xxxxxxxx'

proxies_extension = proxies(username, password, endpoint, port)

def fetch(img):
    import requests as r
    res = r.get(f"https://img.youtube.com/vi/{img}/maxresdefault.jpg")
    print(res)
    with open("./images/image1.jpg", "wb") as f:
        f.write(res.content)


def filter():
    img = url_input.get().split("=")[1].split("&")[0]
    if img == "":
        return
    try:
        fetch(img)
        global img0
        img0 = Image.open("./images/image1.jpg")
        img0 = img0.resize((round(img0.size[0] * 0.7 * width / 2220), round(img0.size[1] * 0.7 * width / 2220)))
        img0 = ImageTk.PhotoImage(img0)
        thumbnail_frm.configure(image=img0)
    except:
        return

def start():
    dur = dur_entry.get()
    loop = loop_entry.get()
    if not dur.isdigit() or not loop.isdigit():
        MessageBox.showinfo("Uyarı", "Süre ve İzlenme sayısı sayı olamlıdır...")
        return
    if url_input.get() =='':
        MessageBox.showinfo("Uyarı", "Lütfen youtube video linkini giriniz...")
        return
    if loop == "" or dur == "":
        MessageBox.showinfo("Uyarı", "Süre ve İzlenme sayısı boş bırakılamaz...")
        return
    dur = int(dur)
    loop = int(loop)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(proxies_extension)

    chrome_options_proxy = webdriver.ChromeOptions()
    chrome_options_proxy.add_extension(proxies_extension)
    chrome_options_proxy.add_argument("--headless=chrome")
    chrome_options_proxy.add_experimental_option("excludeSwitches", ["enable-automation"])

    while loop:

        chrome_porxy = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options_proxy)
        chrome_porxy.get(website1)
        time.sleep(1)
        chrome_porxy.quit()

        chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        chrome.get(url_input.get())
        try:
            click_button_play = chrome.find_element(By.CSS_SELECTOR, "#movie_player > div.ytp-cued-thumbnail-overlay > button")
            click_button_play.click()
            click_button_mute = chrome.find_element(By.CSS_SELECTOR,"#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > span > button")
            click_button_mute.click()
        except:
            pass
        time.sleep(dur)
        chrome.quit()
        loop -= 1

# ---> IMAGES <--- #
img0 = Image.open("./images/image.png")
img0 = img0.resize((round(img0.size[0] * 0.7 * width / 1920), round(img0.size[1] * 0.7 * width / 1920)))
img0 = ImageTk.PhotoImage(img0)
img1 = Image.open("./images/youtubebot.png")
img1 = img1.resize((round(img1.size[0] * 0.5 * width / 1920), round(img1.size[1] * 0.5 * width / 1920)))
img1 = ImageTk.PhotoImage(img1)

# ---> TITLE OF THE GUI <--- #
title = Label(master=window, image=img1, font=("", 40), bg="#363636")
title.grid(row=0, column=0, sticky="W", pady=10, padx=40, columnspan=3)

# ---> DESCRIPTION <--- #
desc = Label(master=window, text="Herhangi bir YouTube videosunun görüntülenme sayısını artırın.", font=("", 12),
             bg="#363636", fg='white')
desc.grid(row=0, column=0, pady=45, columnspan=3)

# ---> URL INPUT <--- #
url_label = Label(master=window, text="Youtube Video Linki ", font=("", 15), bg="#363636", fg='white')
url_label.grid(row=2, column=0, padx=(15, 5), pady=(0, 5))
url_input = Entry(master=window, font=("", 15), width=50)
url_input.grid(row=2, column=1, sticky="ew", pady=(0, 5), padx=20)
# ---> SUBMIT BUTTON <--- #
style = ttk.Style()
style.configure("TButton", font=("", 15))
url_btn = ttk.Button(style='TButton', master=window, text="Kaydet", command=filter)
url_btn.grid(row=2, column=2, padx=(3, 15), pady=(0, 5))

# ---> YOUTUBE THUMBNAIL FRAME <--- #
thumbnail_frm = Label(master=window, image=img0, bg='#363636')
thumbnail_frm.grid(row=3, column=0, columnspan=3)

# ---> BOTTOM FRAME <--- #
dur_loop_frm = Frame(master=window, bg='#363636')
dur_loop_frm.grid(row=4, column=0, columnspan=3, sticky="nsew")

# ---> DURATION <--- #
dur_lbl = Label(master=dur_loop_frm, text="Süre (saniye) ", font=("", 15), bg='#363636', fg='white')
dur_lbl.grid(row=0, column=0, pady=10, padx=23)
dur_entry = ttk.Entry(master=dur_loop_frm, font=("", 15))
dur_entry.grid(row=0, column=1, padx=5)
# ---> LOOP <--- #
loop_lbl = Label(master=dur_loop_frm, text="İzlenme Sayısı ", font=("", 15), bg='#363636', fg='white')
loop_lbl.grid(row=0, column=3, pady=10, padx=(15, 3))
loop_entry = ttk.Entry(master=dur_loop_frm, font=("", 15))
loop_entry.grid(row=0, column=2, padx=5)
# ---> START BUTTON <--- #
dur_loop_btn = ttk.Button(style="TButton", master=dur_loop_frm, text="Başlat", command=start)
dur_loop_btn.grid(row=0, column=4)

window.mainloop()
