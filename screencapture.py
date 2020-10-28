import tkinter as tk
import mss
import os
import string


class NoFilenameEntered(Exception):
    pass

def create_valid_filename(name):
    i = 1
    valid_filename = name
    while os.path.isfile(valid_filename + '.png'):
        valid_filename = f"{name}-{i}"
        i += 1
    return valid_filename


def screen_capture(monitor_number, filename):
    # screenshot and generate png file
    with mss.mss() as sct:
        mon = sct.monitors[monitor_number]
        sct_img = sct.grab(mon)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename + '.png')


class MainMenu(tk.Frame):
    def __init__(self, parent):
        # inherent from tk.Frame
        super().__init__(parent)

        # show the Frame.
        self.pack()
        self.parent = parent

        # continuous snapping is False by default
        self.continuous_snapping = False

        # create widgets in main menu
        self.instruction = tk.Label(self, text='Enter the filename: ')
        self.input_filename_box = tk.Entry(self, width=50)
        self.status_bar = tk.Label(self, bd=10)
        self.screenshot_button = tk.Button(self, text='Screen cap!',
                                           padx=50, pady=20, command=self.start_snapping)

        # tick box for user to choose screenshot mode
        self.screenshot_mode_check_variable = tk.BooleanVar()  # a variable to track continuous snapping
        self.screenshot_mode_check_button = tk.Checkbutton(self, text='Continuous snapping',
                                                           variable=self.screenshot_mode_check_variable,
                                                           command=self.show_continuous_snapping_widgets)

        # a list of monitors available
        self.monitor_number = tk.IntVar()
        self.monitor_radiobutton = tk.Radiobutton(self, text="All monitors",
                                                  variable=self.monitor_number,
                                                  value=0)

        # create widgets in continuous snapping menu - NOT DISPLAY UNTIL THE MODE IS TICKED
        self.interval = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL)
        self.interval.set(1)
        self.stop_button = tk.Button(self, text='Stop',
                                     padx=70, pady=20, command=self.stop_snapping)

    def show_main_widgets(self):
        # display main widgets
        self.instruction.pack()
        self.input_filename_box.pack()
        self.status_bar.pack()
        self.screenshot_button.pack()

        # display a list of available monitors
        self.monitor_radiobutton.pack()
        for i in range(1, len(mss.mss().monitors)):  # create radiobutton for other monitors
            self.monitor_radiobutton = tk.Radiobutton(self, text=f"Monitor {i}",
                                                      variable=self.monitor_number, value=i)
            self.monitor_radiobutton.pack()

        # display check_button for user to select screenshot mode
        self.screenshot_mode_check_button.pack()

    def show_continuous_snapping_widgets(self):
        # if the continuous snapping option is ticked, show its widgets
        if self.screenshot_mode_check_variable.get():
            self.continuous_snapping = True
            self.interval.pack()
            self.stop_button.pack()
        # when the option is unticked, remove its widgets and stop self.snapping
        else:
            self.stop_snapping()
            self.interval.pack_forget()
            self.stop_button.pack_forget()

    def screenshot(self):
        # get the target monitor to capture and create an appropriate filename
        monitor_number = self.monitor_number.get()
        filename = create_valid_filename(self.input_filename_box.get())

        # take screen shot
        screen_capture(monitor_number, filename)

        # display result accordingly
        self.status_bar['text'] = f"{filename}.png captured!"

        if self.continuous_snapping:
            self.after(1000 * self.interval.get(), self.screenshot)

    def raise_error_for_invalid_inputs(self):
        # check if the user has entered filename
        if not self.input_filename_box.get():
            raise NoFilenameEntered
        # check if there is any punctuation in the filename
        if any(char in set(string.punctuation) for char in self.input_filename_box.get()):
            raise TypeError

    def check_valid_inputs(self):
        # try checking for valid inputs
        try:
            self.raise_error_for_invalid_inputs()
        except NoFilenameEntered:  # Display ERROR when no filename is entered
            self.status_bar['text'] = 'Please enter something!'
        except TypeError:
            self.status_bar['text'] = 'Invalid filename!'
        except:
            self.status_bar['text'] = 'Something is wrong!'
        else:
            return True
        return False

    def start_snapping(self):
        # only activate snapping when all inputs are valid
        if self.check_valid_inputs():
            self.screenshot()

    def stop_snapping(self):
        if self.continuous_snapping:
            self.continuous_snapping = False
            self.status_bar['text'] = 'Finished!'


def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Screen Capture")
    app = MainMenu(root)
    app.show_main_widgets()

    root.mainloop()


if __name__ == '__main__':
    main()
