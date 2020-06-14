
import tkinter as tk
from AngleMannager import AngleMannager
from PIL import ImageGrab,ImageTk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2) # windows 10


class MainRoot:
    def __init__(self):
       self.root = tk.Tk()
       self.angleMannager = AngleMannager()
       self.fullCanvas = tk.Canvas(self.root)
       self.number = 0
       self.horizontalLine = None
       self.angleLine = None

    def Draw(self,event):# r = 3
        if self.number > 1:
            if self.angleLine is not None:
                self.fullCanvas.delete(self.angleLine)
            if self.horizontalLine is not None:
                self.createAngleLine(event)

    def bindUnbind(self,bind):
        if bind:
            self.root.bind("<Button-1>", self.root.onClick)
            self.root.bind("<Button-3>", self.root.saveAngle)
            self.root.bind("<B1-Motion>", self.root.Draw)
        else:
            self.root.unbind("<Button-1>", self.root.onClick)
            self.root.unbind("<Button-3>", self.root.saveAngle)
            self.root.unbind("<B1-Motion>", self.root.Draw)

    def onClick(self, event):
        if self.number == 0:
            self.angleMannager.centerPoint = [event.x,event.y]
        elif self.number == 1:
            self.angleMannager.cornerPoint = [event.x, event.y]
            self.horizontalLine = self.fullCanvas.create_line(self.angleMannager.centerPoint[0],self.angleMannager.cornerPoint[1],self.angleMannager.cornerPoint[0],self.angleMannager.cornerPoint[1])
        elif self.number > 1:
            if self.angleLine is not None:
                self.fullCanvas.delete(self.angleLine)
            self.createAngleLine(event)

        self.number = self.number + 1

    def showTool(self): # the small tool window
        self.toolWin = ToolWin(self.root)
        self.toolWin.mainloop()

    def createAngleLine(self, event):
        self.angleLine = self.fullCanvas.create_line(self.angleMannager.cornerPoint[0], self.angleMannager.cornerPoint[1], event.x, event.y)
        self.angleMannager.finalPoint = [event.x, event.y]
        angleValue = self.angleMannager.calculateAngle()
        self.toolWin.angle.set(str(angleValue) + "º")
        self.toolWin.update_idletasks()

    def main(self):
        #root initiation
        self.root.state('iconic')
        self.root.overrideredirect(0)
        background = ImageTk.PhotoImage(
            ImageGrab.grab())  # show the background,make it "draw on the screen".
        self.fullCanvas.create_image(0, 0, anchor="nw", image=background)
        self.fullCanvas.pack(expand="YES",fill="both")
        self.root.after(100, self.showTool)
        self.root.mainloop()
class ToolWin(tk.Toplevel):
    global root
    def __init__(self):
        self.angle = tk.StringVar()
        tk.Toplevel.__init__(self)
        self._offsetx = 0
        self._offsety = 0
        self.wm_attributes('-topmost', 1)
        self.overrideredirect(1)
        self.geometry('200x200')
        self.penModeId = None
        self.bind('<ButtonPress-1>',self.clickTool)
        self.bind('<B1-Motion>',self.moveTool) # bind move event
        cancel = tk.Button(self, text="Quit", command=root.destroy)
        cancel.pack()
        new_angle = tk.Button(self, text="Tomar Medida", command=self.newAngle)
        new_angle.pack()
        angleLabel = tk.Label(self, textvariable=self.angle, font=('Times','30'), fg='black')
        angleLabel.pack()


    def moveTool(self):
        self.geometry("200x200+{}+{}".format(self.winfo_pointerx()-self._offsetx,self.winfo_pointery()-self._offsety))

    def clickTool(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def newAngle(self):
        # Global
        global fullCanvas
        global number
        global centerPoint
        global cornerPoint
        global angleLine
        global horizontalLine
        global toolWin
        global angle
        # endGlobal

        # reset variables
        centerPoint = None
        cornerPoint = None
        angleLine = None
        horizontalLine = None
        self.root.number = 0
        self.root.fullCanvas.destroy()
        toolWin.destroy()
        # en reset variables

        # Rebind Mouse
        root.bind("<Button-1>", root.onClick)
        root.bind("<Button-3>", root.saveAngle)
        # fullCanvas.create_text("asdfasd")
        root.bind("<B1-Motion>", root.Draw)
        # End Rebind Mouse

        background = ImageTk.PhotoImage(
            ImageGrab.grab())
        fullCanvas = tk.Canvas(root)
        root.state('zoomed')
        root.overrideredirect(1)

        fullCanvas.create_image(0, 0, anchor="nw", image=background)
        fullCanvas.pack(expand="YES", fill="both")

root = MainRoot()
mainRoot = MainRoot()
mainRoot.main()