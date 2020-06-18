import csv
import base64
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen


window = tk.Tk()
window.title("Resim Seçme Programı")
window.geometry('600x60')

pathLabel = ttk.Label(
    window, text="Lütfen stok bilgisi dosyasının yolunu giriniz: ")
pathLabel.grid(column=0, row=0, padx=(10, 10), pady=(2, 2))

pathEntry = ttk.Entry(window, width=50)
pathEntry.grid(column=1, row=0, padx=(10, 10), pady=(2, 2))
pathEntry.focus()

imageLists = []


def clicked():
    pathEntryText = pathEntry.get()
    window.destroy()
    i = 0
    options = Options()
    options.headless = True
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get("https://www.google.com.tr/imghp?hl=tr&tab=wi&authuser=0&ogbl")
    with open(pathEntryText.replace('"', ''), encoding="utf8") as csv_file:

        resoruceFile = csv.reader(csv_file, delimiter=';')
        for row in resoruceFile:

            print(row[1])
            stockCode = row[0]
            productName = row[1]
            inputElement = browser.find_element_by_name("q")
            inputElement.send_keys(row[1])
            inputElement.submit()

            try:
                browser.find_element_by_xpath(
                    "//*[@id=\"islrg\"]/div[1]/div[1]/a[1]").click()
                img = browser.find_element_by_xpath(
                    "//*[@id=\"Sva75c\"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute("src")
                imageLists.append(img)

            except:
                pass

            newBrowser = webdriver.Chrome()
            newBrowser.implicitly_wait(10)
            src = newBrowser.get(imageLists[0])
            print(src)
            i += 1

            homeElement = browser.find_element_by_xpath(
                "//*[@id=\"sf\"]/div[1]/div[1]/c-wiz/div/a").click()
            browser.find_element_by_xpath(
                "//*[@id=\"gbw\"]/div/div/div[1]/div[2]/a").click()
            newBrowser.close()

    browser.close()

    imageWindow = tk.Tk()
    imageWindow.title("Resim Seçme Ekranı")
    imageWindow.geometry('1120x280')

    image_byt = urlopen(imageLists[0]).read()
    print(image_byt)
    image_b64 = base64.encodestring(image_byt)
    photo = tk.PhotoImage(data=image_b64)

    cv = tk.Canvas(bg='white')
    cv.pack(side='top', fill='both', expand='yes')
    cv.create_image(10, 10, image=photo, anchor='nw')
    cv.grid(column=0, row=1, padx=(10, 10), pady=(2, 2))

startButon = ttk.Button(window, text="XML Oluştur", command=clicked)
startButon.grid(column=1, row=2, padx=(10, 10), pady=(2, 2))

window.call('wm', 'attributes', '.', '-topmost', '1')
window.mainloop()
