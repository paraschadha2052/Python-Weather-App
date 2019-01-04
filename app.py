# -*- coding: utf-8 -*-

from Tkinter import *
import requests, json
from datetime import datetime, date, timedelta
import base64
import urllib
from weather_utils import * #python file made to retrieve data from openweathermaps
import re
import tkMessageBox
def go():
    city = entry.get()
    try:
        lo = 0
        hi = len(autocompleteList)-1
        while lo<=hi:
            mid = (lo+hi)/2
            if (autocompleteList[mid].lower())==city.lower():
                break
            elif (autocompleteList[mid].lower())<city.lower():
                lo = mid+1
            else:
                hi = mid-1
        if lo<=hi:
            dic = get(city) #create dictionary
        else:
            raise Exception("Invalid location")
    except requests.exceptions.ConnectionError:
        tkMessageBox.showwarning("Alert", "Computer not Connected to internet")
        raise
    except ValueError:
        print 'Entered'
        tkMessageBox.showwarning("Alert", "Server Error")
        raise
    except:
        print "invalid"
        tkMessageBox.showwarning("Alert", "Invalid City!!")
        raise
    print city
    main = Toplevel()#same as frame but a new window
    main.geometry('450x450+200+200')
    Title = city
    main.title(Title)
    main.geometry("{0}x{1}+0+0".format(main.winfo_screenwidth(), main.winfo_screenheight()))
    main.resizable(width=False, height=False)
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()
    print screen_width , screen_height

    
#using API
    tmp = dic['today']['temp']
    tmp_min = dic['today']['min']
    tmp_max = dic['today']['max']
    t = tmp
    tmp = str(tmp) + "°C"
    tmp_min = "Min : " + str(tmp_min) + "°C"
    tmp_max = "Max : " + str(tmp_max) + "°C"
    ids2 = {1:0,2:1,3:2,4:3,9:4,10:5,11:6,13:7,50:8}
    

#using CANVAS and dividing screen to 15 parts on width and height, hence 1/15 = 0.066667
    canvas = Canvas(main,width = 1920,height = 1080)
    canvas.create_image(0, 0, anchor=NW, image=back_img2)
    canvas.create_text(screen_width/2,screen_height*0.066667,text=city,fill="white",font="Comic 60 ")
#current weather icon
    canvas.create_image(screen_width/2, screen_height*0.066667*3.5,image=icons2[ids2[int(dic['today']['icon'][0:2])]])
    canvas.create_text(screen_width/2,screen_height*6*0.066667,text=tmp,fill="white",font="Sans 40 ")
    canvas.create_text(screen_width*0.066667*4,screen_height*5.5*0.066667,text=tmp_min,fill="white",font="Sans 30 ")
    canvas.create_text(screen_width*0.066667*11,screen_height*5.5*0.066667,text=tmp_max,fill="white",font="Sans 30 ")
#image of thermometer
    if t <= 2:
         canvas.create_image(screen_width/12, screen_height*2*0.066667*3.5,image=therm1)   
    elif t <= 15:
         canvas.create_image(screen_width/12, screen_height*2*0.066667*3.5,image=therm2)
    elif t <= 25:
         canvas.create_image(screen_width/12, screen_height*2*0.066667*3.5,image=therm3)
    elif t <= 35:
         canvas.create_image(screen_width/12, screen_height*2*0.066667*3.5,image=therm4)
    else :
         canvas.create_image(screen_width/12, screen_height*2*0.066667*3.5,image=therm5)

    canvas.create_text(screen_width/2,screen_height*7.2*0.066667,text=dic['today']['desc'],fill="white",font="Sans 40")
    canvas.create_line(screen_width/5, screen_height*8*0.066667,screen_width/1.2,screen_height*8*0.066667,fill="white",width=0.1)
    canvas.create_text(screen_width/3.8,screen_height*9*0.066667,text=dic[1]['day'],fill="white",font="Sans 20 bold")
    canvas.create_text(screen_width/2.3,screen_height*9*0.066667,text=dic[2]['day'],fill="white",font="Sans 20 bold")
    canvas.create_text(screen_width/1.65,screen_height*9*0.066667,text=dic[3]['day'],fill="white",font="Sans 20 bold")
    canvas.create_text(screen_width/1.3,screen_height*9*0.066667,text=dic[4]['day'],fill="white",font="Sans 20 bold")

#icons here
    canvas.create_image(screen_width/3.8,screen_height*10*0.066667,image=icons[ids2[int(dic[1]['icon'][0:2])]])
    canvas.create_image(screen_width/2.3,screen_height*10*0.066667,image=icons[ids2[int(dic[2]['icon'][0:2])]])
    canvas.create_image(screen_width/1.65,screen_height*10*0.066667,image=icons[ids2[int(dic[3]['icon'][0:2])]])
    canvas.create_image(screen_width/1.3,screen_height*10*0.066667,image=icons[ids2[int(dic[4]['icon'][0:2])]])

#min and max temp for future four days
    canvas.create_text(screen_width/3.8,screen_height*11*0.066667,text=dic[1]['min'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/2.3,screen_height*11*0.066667,text=dic[2]['min'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/1.65,screen_height*11*0.066667,text=dic[3]['min'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/1.3,screen_height*11*0.066667,text=dic[4]['min'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/3.8,screen_height*11.5*0.066667,text=dic[1]['max'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/2.3,screen_height*11.5*0.066667,text=dic[2]['max'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/1.65,screen_height*11.5*0.066667,text=dic[3]['max'],fill="white",font="Sans 17 bold")
    canvas.create_text(screen_width/1.3,screen_height*11.5*0.066667,text=dic[4]['max'],fill="white",font="Sans 17 bold")
    
    canvas.pack()
    return

def matches(fieldValue, acListEntry):
    pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
    return re.match(pattern, acListEntry)
    
class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        #self.width = 60
        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)
                
            self.matchesFunction = matches

        
        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList
        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        
        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                
                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END,w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False
        
    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
                
            if index != '0':                
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
                
            if index != END:                        
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index) 

    def comparison(self):
        lst = []
        lo = 0
        hi = len(self.autocompleteList)-1
        s = self.var.get().lower()
        while lo<=hi:
            mid = (lo+hi)/2
            if (self.autocompleteList[mid].lower()).startswith(s):
                break
            elif (self.autocompleteList[mid].lower())<s:
                lo = mid+1
            else:
                hi = mid-1
        if (self.autocompleteList[mid].lower()).startswith(s):
            lst.append(self.autocompleteList[mid])
            lo = mid-1
            while lo >=0 and self.autocompleteList[lo].lower().startswith(s):
                lst.append(self.autocompleteList[lo])
                lo -= 1
            hi = mid+1
            while hi<len(self.autocompleteList) and self.autocompleteList[hi].lower().startswith(s):
                lst.append(self.autocompleteList[hi])
                hi += 1
        return lst



if __name__ == '__main__':
    autocompleteList = list(set(cities()))
    autocompleteList.sort()
    
#create window   
    win = Tk()
    win.geometry("320x180+600+400")
    win.resizable(width=False, height=False)
    win.title('Weather Reporter')
#get some images
    back_img = PhotoImage(file="rsz_backk.png")
    back_img2 = PhotoImage(file="gradient_wallpaper_1.gif")
#background image
    back_label = Label(win,image=back_img)
    back_label.place(x=0, y=0, relwidth=1, relheight=1)
#create autocomplete entry
    entry = AutocompleteEntry(autocompleteList, win, listboxLength=6,width=32, matchesFunction=matches)
    entry.insert(END, 'Enter City Here ...')
    entry.place(relx=0.5,rely=0.5,anchor=CENTER)
#GO button
    button_img = PhotoImage(file="button1.gif")
    b = Button(text="",command=go,width=50,height=50,font=("Comic sans ms",10,"bold"),image=button_img,compound=RIGHT,bg="light blue",relief=RIDGE).place(relx=0.5,rely=0.7,anchor=CENTER)
#thermometer icons
    therm1 = PhotoImage(file="PNG/simple_weather_icon_51.png")
    therm2 = PhotoImage(file="PNG/simple_weather_icon_52.png")
    therm3 = PhotoImage(file="PNG/simple_weather_icon_53.png")
    therm4 = PhotoImage(file="PNG/simple_weather_icon_54.png")
    therm5 = PhotoImage(file="PNG/simple_weather_icon_55.png")
#small weather icons
    i1 = PhotoImage(file="icons/01d.png")
    i2 = PhotoImage(file="icons/02d.png")
    i3 = PhotoImage(file="icons/03d.png")
    i4 = PhotoImage(file="icons/04d.png")
    i5 = PhotoImage(file="icons/09d.png")
    i6 = PhotoImage(file="icons/10d.png")
    i7 = PhotoImage(file="icons/11d.png")
    i8 = PhotoImage(file="icons/13d.png")
    i9 = PhotoImage(file="icons/50d.png")
    icons = [i1,i2,i3,i4,i5,i6,i7,i8,i9]
#big weather icons
    ii1 = PhotoImage(file="big_icons/01d.png")
    ii2 = PhotoImage(file="big_icons/02d.png")
    ii3 = PhotoImage(file="big_icons/03d.png")
    ii4 = PhotoImage(file="big_icons/04d.png")
    ii5 = PhotoImage(file="big_icons/09d.png")
    ii6 = PhotoImage(file="big_icons/10d.png")
    ii7 = PhotoImage(file="big_icons/11d.png")
    ii8 = PhotoImage(file="big_icons/13d.png")
    ii9 = PhotoImage(file="big_icons/50d.png")
    icons2 = [ii1,ii2,ii3,ii4,ii5,ii6,ii7,ii8,ii9]
    
    win.mainloop()
