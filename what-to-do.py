from tkinter import *
import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

# Define Application Width and Height
appWidth, appHeight = 800, 500

# Define Assets Path
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


def create_button(master, text, command, width=140):
    button = ctk.CTkButton(master, text=text, text_color=text_secondary, height=35, width=width,
                           font=font_subheading, corner_radius=18, fg_color=button_default,
                           command=command)

    button.bind('<Enter>', lambda event: button_hover_event(button))
    button.bind('<Leave>', lambda event: button_default_event(button))

    return button


def button_default_event(button):
    button.configure(text_color=text_secondary, fg_color=button_default,
                     border_width=0)


def button_hover_event(button):
    button.configure(text_color=button_hover, fg_color='transparent',
                     border_width=1, border_color=button_hover)


def button_click_event(button):
    button.configure(text_color=text_secondary, fg_color=button_hover,
                     border_width=1)


def create_entry_widget(master, text, icon=None, show=''):
    frame = ctk.CTkFrame(master, fg_color=widget_color, corner_radius=18)
    frame.columnconfigure(0, weight=1)

    entry = ctk.CTkEntry(frame, placeholder_text=text,
                         fg_color='transparent',
                         text_color=text_primary, font=font_body_16,
                         justify='center', border_width=0, corner_radius=0,
                         show=show)
    entry.grid(row=0, column=0, columnspan=2, padx=10, pady=3, sticky='nsew')

    icon_label = ctk.CTkLabel(frame, text='', image=icon, cursor='hand2')
    icon_label.grid(row=0, column=0, padx=15, sticky='e')

    return frame


def password_toggle(widget, state, hide_icon, show_icon):
    if not state:
        widget.winfo_children()[0].configure(show='')
        widget.winfo_children()[1].configure(image=hide_icon)
        return True
    else:
        widget.winfo_children()[0].configure(show='•')
        widget.winfo_children()[1].configure(image=show_icon)
        return False


def have_account(master, label, text):
    frame = ctk.CTkFrame(master, fg_color='transparent', corner_radius=0)

    have_account_label = ctk.CTkLabel(frame, text=label, text_color=text_primary,
                                      font=font_body_16)
    have_account_label.grid(row=0, column=0, padx=(45, 5))

    text_label = ctk.CTkLabel(frame, text=text, text_color=button_hover,
                              font=font_subheading, cursor='hand2')
    text_label.grid(row=0, column=1, padx=(5, 20))

    return frame


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
                                     size=(appWidth, 450))

        self.frame = ctk.CTkFrame(self, fg_color='#FFFFFF', corner_radius=0)
        self.frame.pack(fill='both', expand=True)

        # Configure frame grid layout
        self.frame.columnconfigure(0, weight=1, uniform='a')
        self.frame.columnconfigure(1, weight=1, uniform='a')

        self.frame.rowconfigure(0, weight=1)

        self.bg_image_label = ctk.CTkLabel(self.frame, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, columnspan=2, sticky='sew')

        self.title_label = ctk.CTkLabel(self.frame, text='What to do?', text_color=text_primary,
                                        font=font_heading)
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky='nw')

        self.get_started_frame = GetStartedFrame(self.frame, fg_color='transparent', corner_radius=0,
                                                 command=self.get_started_button_event)
        self.get_started_frame.grid(row=0, column=1, sticky='nsew')

        self.signin_frame = SignInFrame(self.frame, fg_color='transparent', corner_radius=0,
                                        forgot_password_command=lambda event: self.forgot_password_label_event(),
                                        switch_to_register_frame=lambda event: self.register_label_event())

        self.change_password_frame = ChangePasswordFrame(self.frame, fg_color='transparent', corner_radius=0,
                                                         back_button_command=self.back_button_event)

        self.register_frame = RegisterFrame(self.frame, fg_color='transparent', corner_radius=0,)

    def get_started_button_event(self):
        self.get_started_frame.grid_forget()
        self.signin_frame.grid(row=0, column=1, sticky='nsew')

    def forgot_password_label_event(self):
        self.signin_frame.grid_forget()
        self.change_password_frame.grid(row=0, column=1, sticky='nsew')

    def back_button_event(self):
        self.change_password_frame.grid_forget()
        self.signin_frame.grid(row=0, column=1, sticky='nsew')

    def register_label_event(self):
        self.signin_frame.grid_forget()
        self.register_frame.grid(row=0, column=1, sticky='nsew')


class GetStartedFrame(ctk.CTkFrame):
    def __init__(self, master, command, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command

        # Configure frame grid layout
        self.columnconfigure(0, weight=1)

        self.subheading_label = ctk.CTkLabel(self, text='Get your tasks done with What to do?',
                                             text_color=text_primary, font=font_subheading)
        self.subheading_label.grid(row=0, column=0, padx=10, pady=(160, 0), sticky='ew')

        self.body_label = ctk.CTkLabel(self, text='Tired of feeling overwhelmed by your to-do list?\nWrite it down!',
                                       text_color=text_primary, font=font_body_14)
        self.body_label.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.get_started_button = create_button(self, text='Get Started', command=self.command)
        self.get_started_button.grid(row=2, column=0, padx=10, pady=10)


class SignInFrame(ctk.CTkFrame):
    def __init__(self, master, forgot_password_command, switch_to_register_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.forgot_pass_command = forgot_password_command
        self.switch_to_command = switch_to_register_frame
        self.show_password = False

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

        self.email_entry = create_entry_widget(self, text='Enter your Email')
        self.email_entry.grid(row=1, column=0, padx=20, pady=32, sticky='ew')

        self.password_entry = create_entry_widget(self, text='Enter your Password', show='•',
                                                  icon=self.show_icon)
        self.password_entry.grid(row=2, column=0, padx=20, sticky='ew')

        self.forgot_pass_label = ctk.CTkLabel(self, text='Forgot password?', text_color=button_hover,
                                              font=font_body_14, cursor='hand2')
        self.forgot_pass_label.grid(row=3, column=0, padx=20, pady=5, sticky='e')

        self.sign_in_button = create_button(self, text='Sign in', command=self.sign_in_button_event, width=100)
        self.sign_in_button.grid(row=4, column=0, padx=20, pady=10, )

        self.switch_to_register = have_account(self, label="Don't have an account?", text='Register')
        self.switch_to_register.grid(row=5, column=0, padx=20, pady=5, sticky='ew')

        # Event Binding
        self.password_entry.winfo_children()[1].bind('<Button-1>', lambda event: self.password_toggle())
        self.forgot_pass_label.bind('<Button-1>', self.forgot_pass_command)
        self.switch_to_register.winfo_children()[1].bind('<Button-1>', self.switch_to_command)

    def password_toggle(self):
        self.show_password = password_toggle(self.password_entry, self.show_password, self.hide_icon, self.show_icon)

    def get_entry_data(self):
        email = self.email_entry.winfo_children()[0].get()
        password = self.password_entry.winfo_children()[0].get()

        return email, password

    def sign_in_button_event(self):
        print(self.get_entry_data())


class ChangePasswordFrame(ctk.CTkFrame):
    def __init__(self, master, back_button_command, **kwargs):
        super().__init__(master, **kwargs)
        self.back_button_command = back_button_command
        self.old_show_password = False
        self.new_show_password = False

        # Configure frame grid layout
        self.columnconfigure(0, weight=1)

        # Load Image Icons
        self.show_icon = ctk.CTkImage(Image.open(os.path.join(asset_path, 'show-outline.png')),
                                      size=(20, 20))
        self.hide_icon = ctk.CTkImage(Image.open(os.path.join(asset_path, 'hide-outline.png')),
                                      size=(20, 20))

        self.subheading_label = ctk.CTkLabel(self, text='Oh no, you forgot your password?',
                                             text_color=text_primary, font=font_subheading)
        self.subheading_label.grid(row=0, column=0, padx=10, pady=(100, 0), sticky='ew')

        self.email_entry = create_entry_widget(self, text='Enter your Email')
        self.email_entry.grid(row=1, column=0, padx=20, pady=32, sticky='ew')

        self.old_password_entry = create_entry_widget(self, text='Enter Old Password', show='•',
                                                      icon=self.show_icon)
        self.old_password_entry.grid(row=2, column=0, padx=20, sticky='ew')

        self.new_password_entry = create_entry_widget(self, text='Enter New Password', show='•',
                                                      icon=self.show_icon)
        self.new_password_entry.grid(row=3, column=0, padx=20, pady=32, sticky='ew')

        self.back_button = create_button(self, text='Back', command=self.back_button_command, width=80)
        self.back_button.grid(row=4, column=0, padx=20, sticky='w')

        self.change_pass_button = create_button(self, text='Change Password', command=None)
        self.change_pass_button.grid(row=4, column=0, padx=20, sticky='e')

        # Event Binding
        self.old_password_entry.winfo_children()[1].bind('<Button-1>', lambda event: self.old_password_toggle())
        self.new_password_entry.winfo_children()[1].bind('<Button-1>', lambda event: self.new_password_toggle())

    def old_password_toggle(self):
        self.old_show_password = password_toggle(self.old_password_entry, self.old_show_password, self.hide_icon,
                                                 self.show_icon)

    def new_password_toggle(self):
        self.new_show_password = password_toggle(self.new_password_entry, self.new_show_password, self.hide_icon,
                                                 self.show_icon)


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure frame grid layout
        self.columnconfigure(0, weight=1)

        self.subheading_label = ctk.CTkLabel(self, text='Welcome onboard !!',
                                             text_color=text_primary, font=font_subheading)
        self.subheading_label.grid(row=0, column=0, padx=10, pady=(100, 0), sticky='ew')


if __name__ == '__main__':
    app = App()
    app.mainloop()
