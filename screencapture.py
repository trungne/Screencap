import mss
import os
import time
from tkinter import *


def main():
    root = Tk()
    root.title('Screen Capture')
    selection = Frame(root)

    def update(entry, status, curselection):
        # check if user has selected a monitor
        if not curselection:  # curseselection return (n,) with n = number of the selection
            status['text'] = 'Please select a monitor!'
            return

        # check if user has entered text in the input box
        if not entry.get():
            status['text'] = 'Please enter something!'
            return

        monitor = curselection[0]

        filename = entry.get()
        i = 1
        # check if filename already exists
        while os.path.isfile(filename + '.png'):
            filename = entry.get() + '-' + str(i)  # rename the file if it already exists
            i += 1
        screenshot(filename, monitor)  # screenshot!
        status['text'] = filename + '.png captured!'  # display result
        print(var1.get())
    # create widgets
    instruction = Label(root, text='Enter the filename: ')
    inputBox = Entry(root, width=50)
    screenshot_button = Button(selection, text='Screen cap!',
                               padx=50, pady=20,
                               command=lambda: update(inputBox, statusBar, listBox.curselection()))
    statusBar = Label(root, bd=10)
    var1 = IntVar()
    screenshot_mode = Checkbutton(selection, text='Continuous snapping', variable=var1)

    # create options for monitors
    listBox = Listbox(root)
    for i in range(len(mss.mss().monitors)):
        if i == 0:
            listBox.insert(END, 'All monitors')
        else:
            listBox.insert(END, 'Monitor ' + str(i))

    # show widgets
    instruction.grid(row=0, column=0)
    inputBox.grid(row=1, column=0)

    # selection frame
    selection.grid(row=2, column=0)
    screenshot_button.grid(row=0, column=0)
    screenshot_mode.grid(row=0, column=1)

    listBox.grid(row=3, column=0)
    statusBar.grid(row=4, column=0)

    # mainloop
    root.mainloop()


# Screenshot part of the screen of the second monitor
def screenshot(filename, monitor_number):
    with mss.mss() as sct:
        # Get information of the monitor
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }
        # output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename + '.png')
        print(filename)


if __name__ == '__main__':
    main()
