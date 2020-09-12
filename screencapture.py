import tkinter as tk
import mss
import os
import string


class NoMonitorSelected(Exception):
    pass


class NoFilenameEntered(Exception):
    pass


class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.parent = parent
        self.snapping = False
        self.after(1, self.scanning)
        # widgets in main menu
        self.instruction = tk.Label(self, text='Enter the filename: ')
        self.input_filename_box = tk.Entry(self, width=50)
        self.status_bar = tk.Label(self, bd=10)
        self.screenshot_button = tk.Button(self, text='Screen cap!',
                                           padx=50, pady=20, command=self.screenshot)
        self.button_check = tk.IntVar()  # a variable to track if user has ticked continuous snapping
        self.screenshot_mode = tk.Checkbutton(self, text='Continuous snapping', variable=self.button_check,
                                              command=self.show_continuous_snapping_widgets)
        self.list_of_monitors = tk.Listbox(self, selectmode=tk.SINGLE)
        self.list_of_monitors.insert(tk.END, "All monitors")
        for i in range(1, len(mss.mss().monitors)):
            self.list_of_monitors.insert(tk.END, f"Monitor {i}")

        # display main widgets
        self.instruction.pack()
        self.input_filename_box.pack()
        self.status_bar.pack()
        self.screenshot_button.pack()
        self.list_of_monitors.pack()
        self.screenshot_mode.pack()

        # widgets in continuous snapping menu - NOT DISPLAY UNTIL THE MODE IS TICKED
        self.interval = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL)
        self.interval.set(1)
        self.stop_button = tk.Button(self, text='Stop',
                                     padx=70, pady=20, command=self.stop_continuous_snapping)

    def scanning(self):
        if self.snapping:
            self.single_screenshot()
            if self.button_check.get():
                self.after(1000 * self.interval.get(), self.scanning)
            else:
                self.snapping = False
        self.after(1, self.scanning)

    def show_continuous_snapping_widgets(self):
        if self.button_check.get():
            self.interval.pack()
            self.stop_button.pack()
        else:
            self.interval.pack_forget()
            self.stop_button.pack_forget()

    def create_appropriate_filename(self):
        filename = self.input_filename_box.get()
        i = 1
        # in case filename has already been taken, add "-{i}" at the end
        while os.path.isfile(filename + '.png'):
            filename = f"{self.input_filename_box.get()}-{i}"
            i += 1
        return filename

    def single_screenshot(self):
        # get the target monitor to screencap and the filename
        monitor_number = self.list_of_monitors.curselection()[0]
        filename = self.create_appropriate_filename()

        # screenshot and generate png file
        with mss.mss() as sct:
            mon = sct.monitors[monitor_number]
            sct_img = sct.grab(mon)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename + '.png')

        # display result accordingly
        self.status_bar['text'] = f"{filename}.png captured!"

    def screenshot(self):
        # try checking for valid inputs
        try:
            self.check_valid_inputs()
        except NoMonitorSelected:  # Display ERROR when no monitor is selected
            self.status_bar['text'] = 'Please select a monitor!'
        except NoFilenameEntered:  # Display ERROR when no filename is entered
            self.status_bar['text'] = 'Please enter something!'
        except TypeError:
            self.status_bar['text'] = 'Invalid filename!'
        # if successful, take screenshot
        else:
            self.snapping = True

    def check_valid_inputs(self):
        if not self.list_of_monitors.curselection():
            raise NoMonitorSelected
        if not self.input_filename_box.get():
            raise NoFilenameEntered
        if any(char in set(string.punctuation) for char in self.input_filename_box.get()):
            raise TypeError

    def stop_continuous_snapping(self):
        self.snapping = False


def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
