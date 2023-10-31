from tkinter import *
import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

appWidth, appHeight = 800, 500

asset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Assets')

# Define Colors
text_primary = '#1E1E1E'
text_secondary = '#F5F5F5'
button_default = '#0E89CB'
button_hover = '#08527A'
widget_color = '#B5CBD7'

# Define Font Styles
font_heading = ('montserrat', 24, 'bold')
font_subheading = ('montserrat', 16, 'bold')
font_body_16 = ('montserrat', 16)
font_body_14 = ('montserrat', 14)


def button_hover_event(button):
    button.configure(text_color=button_hover, fg_color='transparent',
                     border_width=1, border_color=button_hover)


def button_default_event(button):
    button.configure(text_color=text_secondary, fg_color=button_default,
                     border_width=0)


def button_click_event(button):
    button.configure(text_color=text_secondary, fg_color=button_hover,
                     border_width=1)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create window
        x = (self.winfo_screenwidth() // 2) - (appWidth // 2)
        y = (self.winfo_screenheight() // 2) - (appHeight // 2)
        self.geometry(f'{appWidth}x{appHeight}+{x}+{y}')
        self.resizable(False, False)
        self.title('What to do?')

        self.bg_image = ctk.CTkImage(Image.open(os.path.join(asset_path, 'What to do.png')),
                                     size=(appWidth, appHeight))

        self.frame = ctk.CTkFrame(self, fg_color='#FFFFFF', corner_radius=0)
        self.frame.pack(fill='both', expand=True)

        # Configure frame grid layout
        self.frame.columnconfigure(0, weight=1, uniform='a')
        self.frame.columnconfigure(1, weight=1, uniform='a')

        self.bg_image_label = ctk.CTkLabel(self.frame, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, columnspan=2)

        self.title_label = ctk.CTkLabel(self.frame, text='What to do?', text_color=text_primary,
                                        font=font_heading)
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky='nw')

        self.get_started_frame = GetStarted(self.frame, fg_color='transparent', corner_radius=0,
                                            command=self.get_started_button_event, )
        self.get_started_frame.grid(row=0, column=1, sticky='nsew')

        self.register_frame = Register(self.frame, fg_color='transparent', corner_radius=0,
                                       command=None)

    def get_started_button_event(self):
        self.get_started_frame.grid_forget()
        self.register_frame.grid(row=0, column=1, sticky='nsew')


class GetStarted(ctk.CTkFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command

        # Configure frame grid layout
        self.columnconfigure(0, weight=1)

        self.subheading_label = ctk.CTkLabel(self, text='Get your tasks doe with What to do?',
                                             text_color=text_primary, font=font_subheading)
        self.subheading_label.grid(row=0, column=0, padx=10, pady=(150, 0), sticky='ew')

        self.body_label = ctk.CTkLabel(self, text='Tired of feeling overwhelmed by your to-do list?\nWrite it down!',
                                       text_color=text_primary, font=font_body_14)
        self.body_label.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.get_started_button = ctk.CTkButton(self, text='Get Started', text_color=text_secondary, height=35,
                                                font=font_subheading, corner_radius=18, fg_color=button_default,
                                                command=self.command)
        self.get_started_button.grid(row=2, column=0, padx=10, pady=10)

        self.get_started_button.bind('<Enter>', lambda event: button_hover_event(self.get_started_button))
        self.get_started_button.bind('<Leave>', lambda event: button_default_event(self.get_started_button))
        # self.get_started_button.bind('<Button-1>', lambda event: button_click_event(self.get_started_button))


class Register(ctk.CTkFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command

        # Configure frame grid layout
        self.columnconfigure(0, weight=1)

        # Load Image Icons
        self.show_icon = ctk.CTkImage(Image.open(os.path.join(asset_path, 'show-outline.png')),
                                      size=(20, 20))
        self.hide_icon = ctk.CTkImage(Image.open(os.path.join(asset_path, 'hide-outline.png')),
                                      size=(20, 20))

        self.subheading_label = ctk.CTkLabel(self, text='Welcome Back, User !!',
                                             text_color=text_primary, font=font_subheading)
        self.subheading_label.grid(row=0, column=0, padx=10, pady=(100, 0), sticky='ew')

        self.email_entry = self.create_entry_widget(self, text='Enter your Email')
        self.email_entry.grid(row=1, column=0, padx=20, pady=32, sticky='ew')

        self.password_entry = self.create_entry_widget(self, text='Enter your Password', show='•',
                                                       icon=self.show_icon)
        self.password_entry.grid(row=2, column=0, padx=20, sticky='ew')

    @staticmethod
    def create_entry_widget(master, text, icon=None, show=''):
        frame = ctk.CTkFrame(master, fg_color=widget_color, corner_radius=18)
        frame.columnconfigure(0, weight=1)

        icon_label = ctk.CTkLabel(frame, text='', image=icon)
        icon_label.grid(row=0, column=1, padx=(0, 10), sticky='e')

        entry = ctk.CTkEntry(frame, placeholder_text=text,
                             fg_color='transparent',
                             text_color=text_primary, font=font_body_16,
                             justify='center', border_width=0, corner_radius=0,
                             show=show)
        entry.grid(row=0, column=0, padx=(10, 0), pady=5, sticky='nsew')


        return frame


if __name__ == '__main__':
    app = App()
    app.mainloop()
