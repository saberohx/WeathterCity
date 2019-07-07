#! python 3
#WeatherCity.py - Load data of weather from OpenWeatherMap.org

import json, requests
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from random import randint

############ DESIGN ##############
##################################

##########Main Winndow##########
window=Tk()
window.title('WeatherCity')
window.geometry("400x300+50+50")
window.resizable(0,0)
window.iconbitmap("Images/icon.ico")
canvas=Canvas(window,width=400,height=300)
canvas.pack()
PIL_img=Image.open('Images/basic6.jpg').resize((450,400), Image.ANTIALIAS)
basic_img=ImageTk.PhotoImage(PIL_img)
Background=canvas.create_image(200,100,image=basic_img)

'''lab_img=Image.open('Images/yellow.jpg')#.resize((450,400), Image.ANTIALIAS)
label_img=ImageTk.PhotoImage(lab_img)
LabBackground=canvas.create_image(200,100,image=label_img)'''

# LIST OF IMAGES
def img(sit):
        global binary_img
        random_num=randint(1,6)
        #name_list=["sunny","rain","cloudy","clear"]
        changed_img = Image.open('Images/%s%s.jpg'%(sit,random_num)).resize((400,400),Image.ANTIALIAS)
        binary_img = ImageTk.PhotoImage(changed_img)

######### First Frame ###########
entry_frame=Frame(window,bg='#631B0C',bd=1,relief='ridge')
entry_frame.place(relx=0.08,rely=0.1,relwidth=0.85,relheight=0.15)

# ENTRY  ***************
city_var=StringVar()
ent=Entry(entry_frame,width=40,font=('Verdena',12),textvariable=city_var)
ent.place(relx=0.05,rely=0.1,relwidth=0.7,relheight=0.75)
ent.focus()

# Button ***************
but=Button(entry_frame,width=5,text='OK',bg='#ffffff',fg='#631B0C',relief='groove',font=('arial',10,'bold'),command=lambda :weather())
but.place(relx=0.8,rely=0.1,relheight=0.8)




def weather(event=None):
    try:

        #Get data from the web site
        url1 = 'https://api.apixu.com/v1/forecast.json?key=4cbd5a3e9f874a588c702312192505&q=%s' % (city_var.get())
        res1=requests.get(url1)

        res1.raise_for_status()

         #load json data to python's variable
        weatherData1=json.loads(res1.text)

       #First web site
        #print('Web site : https://api.apixu.com')
        global u,t,desc,v,c
        u=weatherData1['current']['last_updated']
        t=weatherData1['current']['temp_c']
        v=weatherData1['location']['name']
        desc=weatherData1['current']['condition']['text']
        c=weatherData1['location']['country']

        if c=="United States of America":
            c="USA"
        elif c=="United Kingdom":
            c="UK"

        # Conditions
        if "Sunny" in desc:
            img("sunny")
        elif "rain" in desc:
            img("rain")
        elif "cloudy" or "Overcast" in desc:
            img("cloudy")
        elif "Clear" in desc:
            img("clear")
        elif "Mist" in desc:
            img("mist")
        # Frame lower ************

        lower_frame = Frame(window)
        lower_frame.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.35)

        # Label ****************
        # flat, groove, raised, ridge, solid, or sunken
        lab = Label(lower_frame,bg="white",font=('Verdena', 11, 'bold'), bd=3, relief='ridge', wraplength=200)
        lab.place(relwidth=1, relheight=1)



        ### Getting Information in Labe ###
        lab.config(text=("%s,%s\n%s °C\n%s\n%s")%(v,c,t,desc,u))
        canvas.itemconfig(Background, image=binary_img)


    except Exception as exc:
        lower_frame = Frame(window)
        lower_frame.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.35)
        lab = Label(lower_frame,bg="red",fg='white',font=('Verdena', 11, 'bold'), bd=3, relief='ridge', wraplength=200)
        lab.place(relwidth=1, relheight=1)
        if 'Bad Request' in str(exc):
            lab.config(text="Entred City Not Found")
        elif 'connection' in str(exc):
            lab.config(text="Failed Connection")

window.mainloop()



