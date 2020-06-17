import csv
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

window = tk.Tk()
window.title("Katagori XML Olusturucu")
window.geometry('600x50')

pathLabel = ttk.Label(window, text="Lütfen stok bilgisi dosyasının yolunu giriniz: ")
pathLabel.grid(column=0, row=0, padx=(10, 10), pady=(2, 2))

pathEntry = ttk.Entry(window, width=50)
pathEntry.grid(column=1, row=0, padx=(10, 10), pady=(2, 2))
pathEntry.focus()

imageLists = []

def clicked():
    i=0
    options = Options()
    options.headless = True
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get("https://www.google.com.tr/imghp?hl=tr&tab=wi&authuser=0&ogbl")
    print(pathEntry.get())
    with open(pathEntry.get().replace('"',''),encoding="utf8") as csv_file:

        resoruceFile = csv.reader(csv_file, delimiter=';')
        for row in resoruceFile:
            
            print(row[1])
            stockCode = row[0]
            productName = row[1]
            inputElement = browser.find_element_by_name("q")
            inputElement.send_keys(row[1])
            inputElement.submit()

            try:
                browser.find_element_by_xpath("//*[@id=\"islrg\"]/div[1]/div[1]/a[1]").click()
                imageLists[i].append(browser.find_element_by_xpath("//*[@id=\"Sva75c\"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img"))
                
            except:
                pass
            
            print(imageLists)
            newBrowser = webdriver.Chrome()
            newBrowser.implicitly_wait(10)
            newBrowser.get(imageLists[i][1].get_attribute("src"))
            i+=1
            homeElement = browser.find_element_by_xpath("//*[@id=\"sf\"]/div[1]/div[1]/c-wiz/div/a").click()
            browser.find_element_by_xpath("//*[@id=\"gbw\"]/div/div/div[1]/div[2]/a").click()
            

    browser.close()



startButon = ttk.Button(window, text="XML Oluştur", command=clicked)
startButon.grid(column=1, row=2, padx=(10, 10), pady=(2, 2))

window.call('wm', 'attributes', '.', '-topmost', '1')
window.mainloop()
