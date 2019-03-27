import tkinter, os, re
from tkinter.messagebox import * #Space above for the message
from tkinter.filedialog import * #Get the dialog box to open when required

class Notepad:
    __root = Tk()
    
    #Dimensions
    __thisWidth = 300
    __thisHeight = 300
    #Components
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisTextArea["bg"] = "lightgrey"
    #Menu Components
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    #Scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):
        #Set icon
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass
        #Set window size
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass
        #Set Window text
        self.__root.title("Untitled - Notepad")

        #Center the window
        screenWidth = self.__root.winfo_screenmmwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth /2) - (self.__thisWidth /2)
        top = (screenHeight /2) - (self.__thisHeight /2)
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self.__thisTextArea.grid(sticky = N + E + S + W) #Controls widget
        #File Menu
        self.__thisFileMenu.add_command(label = "New        Ctrl+N", command= lambda: self.__newFile('x'))
        self.__thisFileMenu.add_command(label = "Open       Ctrl+O", command= lambda: self.__openFile('x'))
        self.__thisFileMenu.add_command(label = "Save       Ctrl+S", command= lambda: self.__saveFile('x'))
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label = "Exit       Ctrl+W", command=lambda: self.__quitApplication('x'))
        self.__thisMenuBar.add_cascade(label = "File", menu=self.__thisFileMenu)
        #Edit Menu
        self.__thisEditMenu.add_command(label = "Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label = "Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label = "Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label = "Edit", menu=self.__thisEditMenu)
        #Help Menu
        self.__thisHelpMenu.add_command(label = "About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label= "Help", menu=self.__thisHelpMenu)

        self.__root.config(menu = self.__thisMenuBar, background="orange")
        #Scroll Bar
        self.__thisScrollBar.pack(side=RIGHT, fill = Y)
        #Adjust according to content
        self.__thisScrollBar.config(command = self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand = self.__thisScrollBar.set)

        #Keybindings
        self.__root.bind('<Control-w>', self.__quitApplication)
        self.__root.bind('<Control-n>', self.__newFile)
        self.__root.bind('<Control-s>', self.__saveFile)
        self.__root.bind('<Control-o>', self.__openFile)
        self.__root.bind('<Control-Shift-n>', self.__quitApplication)
        self.__root.bind('<Control-f>', self.__findTextArea)

    def __quitApplication(self, gbg):
        if self.__file != None:
            file = open(self.__file, 'r')
            read = file.read()
            file.close()
        else:
            read = self.__thisTextArea.get(1.0, END)
        if (self.__file == None and len(self.__thisTextArea.get(1.0, END)) != 1) or (self.__thisTextArea.get(1.0, END) != read):
            popup = Menu(self.__root)
            popup.add_command(label="Save", command= lambda: self.__saveFile('x'))
            popup.post(self.__root.winfo_rootx, self.__root.winfo_rooty)
            print('Can\'t close')
        else:
            self.__root.destroy()

    def __showAbout(self, gbg):
        showinfo("Notepad", "Mrinal Verma")

    def __openFile(self, gbg):
        self.__file = askopenfilename(defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])
        if self.__file == '':
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + "- Notepad")
            self.__thisTextArea.delete(1.0, END)
            file = open(self.__file, "r")
            self.__thisTextArea.insert(1.0, file.read())
            file.close()

    def __newFile(self, gbg):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self, gbg):
        if self.__file == None:
            self.__file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])
            if self.__file == '':
                self.__file = None
            else:
                file = open(self.__file, 'w')
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()
                self.__root.title(os.path.basename(self.__file))
        else:
            file = open(self.__file, 'w')
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()

    def __findTextArea(self, gbg):
        area = self.__thisTextArea.get(1.0, END)
        word = 'test'
        
        for match in re.finditer(word, area):
            print('Found at:' + str(match.start())+ str(match.end()))
            self.__thisTextArea.mark_set('start'+str(match.start()), float(match.start()))
            self.__thisTextArea.mark_set('end'+str(match.end()), float(match.end()))
            self.__thisTextArea.tag_add('tag'+str(match.start()), 'start'+str(match.start()), 'end'+str(match.end()))
            self.__thisTextArea.tag_configure('tag'+str(match.start()), foreground="#ff0000")
        print('Ran it')
    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

notepad = Notepad(width=600, height=400)
notepad.run()