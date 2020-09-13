import tkinter as tk
import mss
import os
import string
import pygame

class NoFilenameEntered(Exception):
    pass


class MainMenu(tk.Frame):
    def __init__(self, parent):
        pygame.mixer.init()
        # inherent from tk.Frame
        super().__init__(parent)
        # show the Frame.
        self.pack()
        self.parent = parent
        '''The program continuously scans to see if user has pressed screenshot button
        When the screenshot button is press, self.snapping is changed to True
        Then the program will capture screen according to the screenshot mode (single or continuous)'''
        self.snapping = False  # snapping option is False by default
        self.after(1, self.scanning)

        # create widgets in main menu
        self.instruction = tk.Label(self, text='Enter the filename: ')
        self.input_filename_box = tk.Entry(self, width=50)
        self.status_bar = tk.Label(self, bd=10)
        self.screenshot_button = tk.Button(self, text='Screen cap!',
                                           padx=50, pady=20, command=self.start_snapping)
        self.screenshot_mode_check_variable = tk.IntVar()  # a variable to track if user has ticked continuous snapping
        self.screenshot_mode_check_button = tk.Checkbutton(self, text='Continuous snapping',
                                                           variable=self.screenshot_mode_check_variable,
                                                           command=self.show_continuous_snapping_widgets)
        # display main widgets
        self.instruction.pack()
        self.input_filename_box.pack()
        self.status_bar.pack()
        self.screenshot_button.pack()

        # display radiobutton for user to select target monitor
        self.monitor_number = tk.IntVar()

        self.monitor_radiobutton = tk.Radiobutton(self, text="All monitors",
                                                  variable=self.monitor_number,
                                                  value=0)  # create radiobutton for all monitors
        self.monitor_radiobutton.pack()  # display the radiobutton
        for i in range(1, len(mss.mss().monitors)):  # create radiobutton for other monitors
            self.monitor_radiobutton = tk.Radiobutton(self, text=f"Monitor {i}",
                                                      variable=self.monitor_number, value=i)
            self.monitor_radiobutton.pack()  # display the radiobutton

        # display check_button for user to select screenshot mode
        self.screenshot_mode_check_button.pack()

        # create widgets in continuous snapping menu - NOT DISPLAY UNTIL THE MODE IS TICKED
        self.interval = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL)
        self.interval.set(1)
        self.stop_button = tk.Button(self, text='Stop',
                                     padx=70, pady=20, command=self.stop_snapping)

        # create sound effects
        self.capture_sound = pygame.mixer.Sound('capturesound.wav')

    def scanning(self):
        ''' This scanning function run recursively to create an infinitive loop to
        continuously check if user has clicked screenshot button '''
        if self.snapping:
            self.screenshot()  # take a screenshot if self.snapping is True
            if self.screenshot_mode_check_variable.get():
                # if continuous mode is ticked, recursively call self.scanning with a delay of 1000ms * interval
                self.after(1000 * self.interval.get(), self.scanning)
            else:
                # if continuous mode is not ticked, turn off snapping and recursively call self.scanning
                self.snapping = False
                self.after(1, self.scanning)
        else:
            self.after(1, self.scanning)

    def show_continuous_snapping_widgets(self):
        # if the continuous snapping option is ticked, show its widgets
        if self.screenshot_mode_check_variable.get():
            self.interval.pack()
            self.stop_button.pack()
        # when the option is unticked remove its widgets, also stop self.snapping
        else:
            self.stop_snapping()
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

    def screenshot(self):
        # get the target monitor to capture and create an appropriate filename
        monitor_number = self.monitor_number.get()
        filename = self.create_appropriate_filename()
        
        self.play_sound()
        # screenshot and generate png file
        with mss.mss() as sct:
            mon = sct.monitors[monitor_number]
            sct_img = sct.grab(mon)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename + '.png')
        
        # display result accordingly
        self.status_bar['text'] = f"{filename}.png captured!"

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
            
            self.snapping = True

    def stop_snapping(self):
        self.snapping = False

    def play_sound(self):
        self.capture_sound.play()
        
def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Screen Capture")
    app = MainMenu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
