import tkinter as tk
from tkinter import *
from tkinter import font as tkfont # python 3
from tkinter import ttk
from tkinter.ttk import *
from tkinter import Scrollbar
from PIL import ImageTk, Image
from main import *

class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.total_price = 0.0
        for F in (StartPage, InfoPage, BakerScrapePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if type(frame) == BakerScrapePage:
            frame.tkraise()
            time.sleep(1)
            frame.call_main()
        else:
            frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to WTF Rice", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        # scraping options
        info_label = tk.Button(self, text="what is WTF?", font="Helvetica 9 italic", command=lambda: controller.show_frame("InfoPage"))
        info_label.place(relx = 0.5, rely = 0.8, anchor = CENTER)


        baker = tk.Button(self, text="WTF Baker?", font = "Helvetica 13",
                           command=lambda: controller.show_frame("BakerScrapePage"))
        baker.place(relx = 0.4, rely = 0.15, anchor = NE)
        
        all = tk.Button(self, text="WTF Rice?",font = "Helvetica 13",
                           command=lambda: controller.show_frame("BakerScrapePage"))
        all.place(relx = 0.6, rely = 0.15, anchor = NW)

        self.controller.choose_cal = IntVar()
        c = Checkbutton(self, text = "Add WTF events to my calendar", variable =self.controller.choose_cal)
        c.pack()

        self.close_button = ttk.Button(self, text="Quit", command=parent.quit)
        # self.close_button.config(height = 20, width = 30)
        self.close_button.place(x=0, y=0,width=60,height=40)
        img = ImageTk.PhotoImage(Image.open('rice.jpg').resize((700, 500), Image.ANTIALIAS))
        # img = img.resize((500, 500), Image.ANTIALIAS)
        panel = tk.Label(self, image =img, text="wtf-rice")
        panel.image = img
        panel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
       

class BakerScrapePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Currently finding food . . .", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.event_count = tk.Label(self, text="", font=controller.title_font)
        self.event_count.pack(side="top", fill="x", pady=10)
        self.progress_label = tk.Label(self, text="Initializing . . .", font="Helvetica 13")
        self.progress_label.pack(side="top", fill="x", pady=30)


    def call_main(self):
        mf = MainFunctionality()
        self.progress_label['text'] = "Looking through Baker Facebook feed for food"
        events, count = mf.scrape_baker()
        self.event_count['text'] = str(count) + " new food events found "  + " out of " + str(len(events)) + " total events."
        if self.controller.choose_cal.get():
            self.progress_label['text'] = "Adding the events to your calendar (you will be prompted to login)"
            mf.cal_update(events)
        self.progress_label['text'] = "Done! Thanks for using WTF"



        
        

        


class InfoPage(tk.Frame):
    def __init__(self,parent,controller):
        about_str = """
        WTF (Where's the food) Rice is a program designed to help you, presumably
        a hungry, penny-pinching college student, mooch, freeload, leech, scavenge, and exploit
        the various events on campus that offer free food. Simply hit the WTF button specific to
        your location preference, and we'll try to find events on facebook that feed 
        broke, starving, college students like yourself. It'll even add them to your google calendar
        for your mooching pleasure.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to WTF Rice", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        about_info = tk.Label(self, text=about_str, font="Helvetica 9")
        about_info.pack(side="top", fill="x", pady=10)
        self.back = ttk.Button(self, text="Back", command=lambda:self.controller.show_frame("StartPage"))
        # self.close_button.config(height = 20, width = 30)
        self.back.place(x=0, y=0,width=60,height=40)


root = Controller()
root.geometry("1200x1200")
root.mainloop()