"""Please read the License Agreement before modifying any code!"""

from webbrowser import open as open_file
import customtkinter as ctk
from tkinter import messagebox
from serial.tools.list_ports import comports
import serial
from threading import Thread
from queue import Queue
from datetime import datetime

from tools.ctk_listbox import CTkListbox
from tools.theme import Theme, Icons
import tools.clock as clk
try: import tools.xsi_custom_test as ct
except: pass
from tools.__init__ import __file_dir__, __path_separator__, __version__, __system__, __help_path__

class Base(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"1100x600+{int(self.winfo_screenwidth()/2 - 500)}+{int(self.winfo_screenheight()/2.2 - 300)}")
        self.title("XBee Sniffer Interface")

        self.root = ctk.CTkFrame(self, corner_radius=0, fg_color=Theme.bg_color)
        self.root.pack(expand=True, fill="both")

class NavigationFrame:
    def __init__(self, master):
        self.master = master

    def create_frame(self):
        self.outer_frame = ctk.CTkFrame(self.master, fg_color=Theme.accent, corner_radius=0)
        self.inner_frame = ctk.CTkFrame(self.outer_frame, fg_color=Theme.fg_color, corner_radius=0, width=170)
        self.start_test_button = ctk.CTkButton(self.inner_frame, anchor="w", image=Icons.start_image, text="Start Test", width=150, height=50, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover)
        self.test_button = ctk.CTkButton(self.inner_frame, anchor="w", image=Icons.test_image, text="Test Settings", width=150, height=50, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover)
        self.device_button = ctk.CTkButton(self.inner_frame, anchor="w", image=Icons.device_image, text="Devices", width=150, height=50, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover)
        self.preferences_button = ctk.CTkButton(self.inner_frame, anchor="w", image=Icons.settings_image, text="Preferences", width=150, height=50, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover)
        self.info_button = ctk.CTkButton(self.inner_frame, anchor="w", image=Icons.info_image, text="App Info", width=150, height=50, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover)
        self.help_button = ctk.CTkButton(self.inner_frame, anchor="w", image=Icons.help_image, text="Help", width=150, height=50, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover, command=lambda: open_file(__help_path__))

    def place_frame(self):
        self.outer_frame.pack(side="left", fill="y")
        self.inner_frame.pack(side="left", fill="y", expand=True, padx=(0,3))
        self.start_test_button.place(x=10, y=20)
        self.test_button.place(x=10, y=80)
        self.device_button.place(x=10, y=140)
        self.preferences_button.place(x=10, y=200)
        self.info_button.place(x=10, y=260)
        self.help_button.place(x=10, y=320)

    def resize_frame(self, root_size:int):
        if (root_size <= 1000): 
            self.inner_frame.configure(width=75)
            Icons.start_image.configure(size=(30,30))
            Icons.test_image.configure(size=(30,30))
            Icons.device_image.configure(size=(30,30))
            Icons.stop_image.configure(size=(30,30))
            Icons.settings_image.configure(size=(30,30))
            Icons.info_image.configure(size=(30,30))
            Icons.help_image.configure(size=(30,30))
            Icons.disabled_test_image.configure(size=(30,30))
            Icons.disabled_device_image.configure(size=(30,30))
            self.start_test_button.configure(text="", width=0)
            self.test_button.configure(text="", width=0)
            self.device_button.configure(text="", width=0)
            self.preferences_button.configure(text="", width=0)
            self.info_button.configure(text="", width=0)
            self.help_button.configure(text="", width=0)
        else: 
            self.inner_frame.configure(width=170)
            Icons.start_image.configure(size=(40,40))
            Icons.test_image.configure(size=(40,40))
            Icons.device_image.configure(size=(40,40))
            Icons.stop_image.configure(size=(40,40))
            Icons.settings_image.configure(size=(40,40))
            Icons.info_image.configure(size=(40,40))
            Icons.help_image.configure(size=(40,40))
            Icons.disabled_test_image.configure(size=(40,40))
            Icons.disabled_device_image.configure(size=(40,40))
            if self.start_test_button.cget("image") == Icons.start_image: self.start_test_button.configure(text="Start Test", width=150)
            else: self.start_test_button.configure(text="Stop Test", width=150)
            self.test_button.configure(text="Test Settings", width=150)
            self.device_button.configure(text="Devices", width=150)
            self.preferences_button.configure(text="Preferences", width=150)
            self.info_button.configure(text="App Info", width=150)
            self.help_button.configure(text="Help", width=150)

    def update_frame(self):
        self.outer_frame.configure(fg_color=Theme.accent)
        self.start_test_button.configure(hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"))
        self.test_button.configure(hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"))
        self.device_button.configure(hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"))
        self.preferences_button.configure(hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"))
        self.info_button.configure(hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"))
        self.help_button.configure(hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"))

class OptionsFrame:
    def __init__(self, master):
        self.master = master

        self.ts_name_value = ctk.StringVar(value="my_test")
        self.ts_location_value = ctk.StringVar(value="default")
        self.ts_valid_file_types: list = [".txt", ".csv"]
        self.ts_file_value = ctk.StringVar(value=".txt")
        self.ts_packet_value = ctk.StringVar(value="0")
        self.ts_indicator_value = ctk.StringVar(value="Packet")
        self.ts_stop_value = ctk.StringVar(value=">>>end_of_test")
        
        self.ds_selected_device: str|None = ""

    def create_frame(self):
        self.outer_frame = ctk.CTkFrame(self.master, fg_color=Theme.accent, corner_radius=0, width=0)
        self.inner_frame = ctk.CTkFrame(self.outer_frame, fg_color=Theme.fg_color, corner_radius=0, width=0)

        self.ts_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="Test Settings", font=(Theme.font_type,20,"bold"), width=160)
        self.ts_name_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="Test Name", corner_radius=10, fg_color=Theme.sfg_color, font=(Theme.font_type,15,"normal"))
        self.ts_name_entry = ctk.CTkEntry(self.inner_frame, text_color=Theme.text_color, fg_color=Theme.sfg_color, textvariable=self.ts_name_value, justify="center", font=(Theme.font_type,15,"normal"), height=30, width=200, corner_radius=10, border_width=1, border_color=Theme.accent)
        self.ts_save_location_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="Save Location", corner_radius=10, fg_color=Theme.sfg_color, font=(Theme.font_type,15,"normal"))
        self.ts_save_location_entry = ctk.CTkEntry(self.inner_frame, text_color=Theme.text_color, fg_color=Theme.sfg_color, textvariable=self.ts_location_value, justify="center", font=(Theme.font_type,15,"normal"), height=30, width=200, corner_radius=10, border_width=1, border_color=Theme.accent)
        self.ts_save_location_browse = ctk.CTkButton(self.inner_frame, text_color=Theme.text_color, font=(Theme.font_type,15,"normal"), height=30, width=150, text="Browse", corner_radius=10, hover_color=Theme.accent_hover, fg_color=Theme.sfg_color, command=self._browse_local_files)
        self.ts_file_type_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="File Type", font=(Theme.font_type,15,"normal"), corner_radius=10, fg_color=Theme.sfg_color)
        self.ts_file_type_dropdown = ctk.CTkComboBox(self.inner_frame, text_color=Theme.text_color, fg_color=Theme.sfg_color, values=self.ts_valid_file_types, variable=self.ts_file_value, justify="center", width=200, height=30, corner_radius=10, border_width=1, border_color=Theme.accent, button_color=Theme.accent, button_hover_color=Theme.accent_hover)
        self.ts_track_progress_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="Track Progress", font=(Theme.font_type,15,"normal"), corner_radius=10, fg_color=Theme.sfg_color)
        self.ts_track_progress_switch = ctk.CTkSwitch(self.inner_frame, fg_color=Theme.sfg_color, text="", switch_height=30, switch_width=70, button_color="white", button_hover_color=Theme.accent_hover, progress_color=Theme.accent, command=self._toggle_packet_count)
        self.ts_packet_count_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text_color_disabled=Theme.disabled_text_color, text="Packet Count", font=(Theme.font_type,15,"normal"), corner_radius=10, fg_color=Theme.sfg_color)
        self.ts_packet_count_entry = ctk.CTkEntry(self.inner_frame, font=(Theme.font_type,15,"normal"), text_color=Theme.text_color, textvariable=self.ts_packet_value, justify="center", corner_radius=10, border_width=1, border_color=Theme.accent, fg_color=Theme.sfg_color, width=200, height=30)
        self.ts_packet_indicator_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text_color_disabled=Theme.disabled_text_color, text="Packet Indicator", font=(Theme.font_type,15,"normal"), corner_radius=10, fg_color=Theme.sfg_color)
        self.ts_packet_indicator_entry = ctk.CTkEntry(self.inner_frame, font=(Theme.font_type,15,"normal"), text_color=Theme.text_color, textvariable=self.ts_indicator_value, justify="center", corner_radius=10, border_width=1, border_color=Theme.accent, fg_color=Theme.sfg_color, width=200, height=30)
        self.ts_packet_stop_label = ctk.CTkLabel(self.inner_frame, wraplength=100, text_color=Theme.text_color, text_color_disabled=Theme.disabled_text_color, text="Packet Count Stops Test", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.ts_packet_stop_switch = ctk.CTkSwitch(self.inner_frame, text="", switch_height=30, switch_width=70, button_color="white", button_hover_color=Theme.accent_hover, progress_color=Theme.accent)
        self.ts_stop_value_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="Auto Stop Value", corner_radius=10, font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color)
        self.ts_stop_value_entry = ctk.CTkEntry(self.inner_frame, text_color=Theme.text_color, font=(Theme.font_type,15,"normal"), textvariable=self.ts_stop_value, justify="center", corner_radius=10, border_width=1, border_color=Theme.accent, fg_color=Theme.sfg_color, width=200, height=30)
        self.ts_custom_test_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text_color_disabled=Theme.disabled_text_color, text="Enable Custom Test", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.ts_custom_test_switch = ctk.CTkSwitch(self.inner_frame, fg_color=Theme.sfg_color, text="", switch_height=30, switch_width=70, button_color="white", button_hover_color=Theme.accent_hover, progress_color=Theme.accent)
        self._toggle_packet_count()

        self.ds_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="Devices", font=(Theme.font_type,20,"bold"), width=160)
        self.ds_button_list = CTkListbox(self.inner_frame, fg_color=Theme.bg_color, scrollbar_fg_color=Theme.accent_hover, width=270, scrollbar_hover_color=Theme.accent, corner_radius=10, border_width=1, border_color=Theme.accent, header_fg_color=Theme.bg_color, header_text="Select Device", header_font=(Theme.font_type,17,"bold"), header_text_color=Theme.text_color)
        self.ds_button_list._parent_frame._scrollbar.grid_configure(padx=6)
        self.ds_check_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="No device to check!", font=(Theme.font_type,15,"normal"))
        self.ds_check_progressbar = ctk.CTkProgressBar(self.inner_frame, progress_color=Theme.accent, width=290, fg_color=Theme.bg_color, height=15)
        self.ds_check_progressbar.set(0)
        self.ds_check_progressbar_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, font=(Theme.font_type,15,"bold"), text="0%")

        self.if_label = ctk.CTkLabel(self.inner_frame, text_color=Theme.text_color, text="App Information", font=(Theme.font_type,20,"bold"), width=160)
        self.if_app_name_label = ctk.CTkLabel(self.inner_frame, wraplength=300, text_color=Theme.text_color, text="App Name: XBee Sniffer Interface (XSI)", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.if_version_label = ctk.CTkLabel(self.inner_frame, wraplength=300, text_color=Theme.text_color, text=f"Version #: {__version__}", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.if_UI_engine_label = ctk.CTkLabel(self.inner_frame, wraplength=300, text_color=Theme.text_color, text="UI Framework: Tcl/Tkinter/Customtkinter [Python 3.14]", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.if_license_agr_label = ctk.CTkLabel(self.inner_frame, wraplength=300, text_color=Theme.text_color, text="License: MIT Agreement", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.if_os_label = ctk.CTkLabel(self.inner_frame, wraplength=300, text_color=Theme.text_color, text=f"Operating System: {__system__}", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
         
    def place_frame(self):
        self.outer_frame.pack(side="left", fill="y")
        self.inner_frame.pack(side="left", fill="y", expand=True, padx=(0,3))

    def hide_frame(self):
        self.outer_frame.configure(fg_color=Theme.fg_color)
        self.inner_frame.pack_configure(padx=0)
        self.inner_frame.configure(width=0)

    def show_frame(self):
        self.outer_frame.configure(fg_color=Theme.accent)
        self.inner_frame.pack_configure(padx=(0,3))

    def display_test_settings(self):
        self.ts_label.grid(row=0, column=0, padx=100, pady=(10,20), columnspan=10)
        self.ts_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_name_entry.grid(row=1, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_save_location_label.grid(row=2, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_save_location_entry.grid(row=2, column=1, sticky="w", pady=(15,0))
        self.ts_save_location_browse.grid(row=3, column=1, sticky="w", padx=25, pady=(15,0))
        self.ts_file_type_label.grid(row=4, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_file_type_dropdown.grid(row=4, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_track_progress_label.grid(row=5, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_track_progress_switch.grid(row=5, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_packet_count_label.grid(row=6, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_packet_count_entry.grid(row=6, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_packet_indicator_label.grid(row=7, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_packet_indicator_entry.grid(row=7, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_packet_stop_label.grid(row=8, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_packet_stop_switch.grid(row=8, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_stop_value_label.grid(row=9, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_stop_value_entry.grid(row=9, column=1, sticky="w", padx=(0,10), pady=(15,0))
        self.ts_custom_test_label.grid(row=10, column=0, sticky="w", padx=10, pady=(15,0))
        self.ts_custom_test_switch.grid(row=10, column=1, sticky="w", padx=(0,10), pady=(15,0))
    
    def hide_test_settings(self):
        self.ts_label.grid_forget()
        self.ts_name_label.grid_forget()
        self.ts_name_entry.grid_forget()
        self.ts_save_location_label.grid_forget()
        self.ts_save_location_entry.grid_forget()
        self.ts_save_location_browse.grid_forget()
        self.ts_file_type_label.grid_forget()
        self.ts_file_type_dropdown.grid_forget()
        self.ts_track_progress_label.grid_forget()
        self.ts_track_progress_switch.grid_forget()
        self.ts_packet_count_label.grid_forget()
        self.ts_packet_count_entry.grid_forget()
        self.ts_packet_indicator_label.grid_forget()
        self.ts_packet_indicator_entry.grid_forget()
        self.ts_packet_stop_label.grid_forget()
        self.ts_packet_stop_switch.grid_forget()
        self.ts_stop_value_label.grid_forget()
        self.ts_stop_value_entry.grid_forget()
        self.ts_custom_test_label.grid_forget()
        self.ts_custom_test_switch.grid_forget()

    def display_devices(self):
        self.ds_label.grid(row=0, column=0, padx=100, pady=(10,20), columnspan=10)
        self.ds_button_list.grid(row=1, column=0, columnspan=10, padx=20, pady=(15,0))
        self._find_devices()
        self.ds_check_label.grid(row=2, column=0, sticky="w", padx=15, pady=(60,0))
        self.ds_check_progressbar.grid(row=3, column=0, columnspan=5, sticky="w", padx=(15,5), pady=(15,0))
        self.ds_check_progressbar_label.grid(row=3, column=6, sticky="w", pady=(15,0))

    def hide_devices(self):
        self.ds_label.grid_forget()
        self.ds_button_list.clear()
        self.ds_button_list.grid_forget()
        self.ds_check_label.grid_forget()
        self.ds_check_progressbar.grid_forget()
        self.ds_check_progressbar_label.grid_forget()
        
        self.ds_check_label.configure(text="No device to check!")
        self.ds_check_progressbar.set(0)
        self.ds_check_progressbar_label.configure(text="0%")

    def display_app_info(self):
        self.if_label.grid(row=0, column=0, padx=100, pady=(10,20), columnspan=10)
        self.if_app_name_label.grid(row=1, column=0, sticky="w", padx=20, pady=(15,0))
        self.if_version_label.grid(row=2, column=0, sticky="w", padx=20, pady=(15,0))
        self.if_UI_engine_label.grid(row=3, column=0, sticky="w", padx=20, pady=(15,0))
        self.if_license_agr_label.grid(row=4, column=0, sticky="w", padx=20, pady=(15,0))
        self.if_os_label.grid(row=5, column=0, sticky="w", padx=20, pady=(15,0))

    def hide_app_info(self):
        self.if_label.grid_forget()
        self.if_app_name_label.grid_forget()
        self.if_version_label.grid_forget()
        self.if_UI_engine_label.grid_forget()
        self.if_license_agr_label.grid_forget()
        self.if_os_label.grid_forget()

    def update_frame(self):
        self.outer_frame.configure(fg_color=Theme.accent)
        self.ts_label.configure(font=(Theme.font_type,20,"bold"))
        self.ts_name_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_name_entry.configure(font=(Theme.font_type,15,"normal"), border_color=Theme.accent)
        self.ts_save_location_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_save_location_entry.configure(font=(Theme.font_type,15,"normal"), border_color=Theme.accent)
        self.ts_save_location_browse.configure(font=(Theme.font_type,15,"normal"), hover_color=Theme.accent_hover)
        self.ts_file_type_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_file_type_dropdown.configure(border_color=Theme.accent, button_color=Theme.accent, button_hover_color=Theme.accent_hover)
        self.ts_track_progress_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_track_progress_switch.configure(button_hover_color=Theme.accent_hover, progress_color=Theme.accent)
        self.ts_packet_count_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_packet_count_entry.configure(font=(Theme.font_type,15,"normal"), border_color=Theme.accent)
        self.ts_packet_indicator_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_packet_indicator_entry.configure(font=(Theme.font_type,15,"normal"), border_color=Theme.accent)
        self.ts_packet_stop_label.configure(font=(Theme.font_type,15,"normal")) 
        self.ts_packet_stop_switch.configure(button_hover_color=Theme.accent_hover, progress_color=Theme.accent)
        self.ts_stop_value_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_stop_value_entry.configure(font=(Theme.font_type,15,"normal"), border_color=Theme.accent)
        self.ts_custom_test_label.configure(font=(Theme.font_type,15,"normal"))
        self.ts_custom_test_switch.configure(button_hover_color=Theme.accent_hover, progress_color=Theme.accent)

        self.ds_label.configure(font=(Theme.font_type,20,"bold"))
        self.ds_button_list.configure(border_color=Theme.accent, header_font=(Theme.font_type,20,"bold"), scrollbar_hover_color=Theme.accent, scrollbar_fg_color=Theme.accent_hover)
        self.ds_check_label.configure(font=(Theme.font_type,15,"normal"))
        self.ds_check_progressbar.configure(progress_color=Theme.accent)
        self.ds_check_progressbar_label.configure(font=(Theme.font_type,15,"bold"))

        try: 
            for button in self._button_device_list:
                try: button.configure(font=(Theme.font_type,15,"normal"), hover_color=Theme.accent_hover)
                except: pass
        except: pass

        self.if_label.configure(font=(Theme.font_type,20,"bold"))
        self.if_app_name_label.configure(font=(Theme.font_type,15,"normal"))
        self.if_version_label.configure(font=(Theme.font_type,15,"normal"))
        self.if_UI_engine_label.configure(font=(Theme.font_type,15,"normal"))
        self.if_license_agr_label.configure(font=(Theme.font_type,15,"normal"))
        self.if_os_label.configure(font=(Theme.font_type,15,"normal"))

    def _toggle_packet_count(self):
        match self.ts_track_progress_switch.get():
            case 0:
                self.ts_packet_count_label.configure(state="disabled")
                self.ts_packet_count_entry.configure(state="disabled", text_color=Theme.disabled_text_color)
                self.ts_packet_indicator_label.configure(state="disabled")
                self.ts_packet_indicator_entry.configure(state="disabled", text_color=Theme.disabled_text_color)
                self.ts_packet_value.set(value="0")
                self.ts_packet_stop_label.configure(state="disabled")
                self.ts_packet_stop_switch.configure(state="disabled", fg_color=Theme.bg_color, progress_color=Theme.bg_color)
            case 1:
                self.ts_packet_count_label.configure(state="normal")
                self.ts_packet_count_entry.configure(state="normal", text_color=Theme.text_color)
                self.ts_packet_indicator_label.configure(state="normal")
                self.ts_packet_indicator_entry.configure(state="normal", text_color=Theme.text_color)
                self.ts_packet_value.set(value="1")
                self.ts_packet_stop_label.configure(state="normal")
                self.ts_packet_stop_switch.configure(state="normal", fg_color=Theme.sfg_color, progress_color=Theme.accent)

    def _browse_local_files(self):
        _local_path: str = ctk.filedialog.askdirectory(initialdir=__file_dir__)
        if len(_local_path) > 0: self.ts_location_value.set(_local_path)

    def _find_devices(self):
        self.devices: list = [p[0] for p in comports() if p[1] != 'n/a']
        _button_id: int = 0
        self._button_device_list: list[ctk.CTkButton] = []
        
        for device in self.devices:
            button = ctk.CTkButton(self.ds_button_list.cget("parent_frame"), font=(Theme.font_type,15,"normal"), text_color_disabled=Theme.text_color, height=50, text=device, fg_color=Theme.fg_color, hover_color=Theme.accent_hover, text_color=Theme.text_color, command=lambda id=_button_id: self._find_device_button(id))
            self.ds_button_list.insert_ctkobject(button, fill="x", padx=10, pady=(20,0))
            _button_id += 1
            self._button_device_list.append(button)

    def _find_device_button(self, button_id:int):
        for button_index in range(0,len(self._button_device_list)):
            if button_index == button_id: 
                self._button_device_list[button_index].configure(state="disabled", fg_color=Theme.accent)
                self.ds_selected_device = self._button_device_list[button_index].cget("text")
            else: self._button_device_list[button_index].configure(state="normal", fg_color=Theme.fg_color)
            
        Thread(target=self._check_device).start()

    def _check_device(self):
        self.ds_check_progressbar.set(0)
        try:
            self.ds_check_label.configure(text="Searching for device...")
            self.ds_check_progressbar.set(1/4)
            self.ds_check_progressbar_label.configure(text="25%")

            _attention = serial.Serial(self.ds_selected_device, 9600, timeout=3)
            _progress: int = 0
            _passed: str = ""

            self.ds_check_label.configure(text=f"Sending '+++' to {self.ds_selected_device}")
            self.ds_check_progressbar.set(2/4)
            self.ds_check_progressbar_label.configure(text="50%")

            _attention.write(bytes("+++", "utf-8"))

            self.ds_check_label.configure(text="Waiting for response...")
            self.ds_check_progressbar.set(3/4)
            self.ds_check_progressbar_label.configure(text="75%")

            while _progress < 5:
                _passed = _attention.readline().decode(errors="ignore")
                if _passed == "OK\r":
                    break
                _progress += 1

            _attention.close()

            if _passed == "OK\r": 
                self.ds_check_label.configure(text="Device Response: OK!")
                self.ds_check_progressbar.set(1)
                self.ds_check_progressbar_label.configure(text="100%")
            else: raise
        except:
            self.ds_check_label.configure(text="Device Response: FAILED")
            self.ds_check_progressbar.set(1)
            self.ds_check_progressbar_label.configure(text="100%")
            for button in self._button_device_list:
                if button.cget("text") == self.ds_selected_device:
                    button.configure(state="normal", fg_color=Theme.fg_color)
            self.ds_selected_device = None

    def get_all_option_values(self):
        return [self.ts_name_value.get(), self.ts_location_value.get(), self.ts_file_value.get(), int(self.ts_packet_value.get()), self.ts_indicator_value.get(), self.ts_packet_stop_switch.get(), self.ts_stop_value.get(), self.ds_selected_device, self.ts_custom_test_switch.get()]
    
class TestingFrame:
    def __init__(self, master):
        self.master = master

        self.details_on: bool = False

    def create_frame(self):
        self.frame = ctk.CTkFrame(self.master, corner_radius=7, fg_color=Theme.fg_color, border_color=Theme.accent, border_width=1)
        self.inner_frame = ctk.CTkFrame(self.frame, corner_radius=0, fg_color=Theme.fg_color)
        self.previous_test_label = ctk.CTkLabel(self.inner_frame, text="Previous Test: None", font=(Theme.font_type,25,"bold"), text_color=Theme.text_color)
        self.test_parameters_frame = ctk.CTkFrame(self.inner_frame, corner_radius=0, fg_color=Theme.fg_color)
        self.test_device_status = ctk.CTkLabel(self.test_parameters_frame, text_color=Theme.text_color, corner_radius=10, fg_color=Theme.sfg_color, font=(Theme.font_type,12,"normal"), text="Device Status: None")
        self.test_packets = ctk.CTkLabel(self.test_parameters_frame, text_color=Theme.text_color, corner_radius=10, fg_color=Theme.sfg_color, font=(Theme.font_type,12,"normal"), text="Packet Count: None")
        self.test_type = ctk.CTkLabel(self.test_parameters_frame, text_color=Theme.text_color, corner_radius=10, fg_color=Theme.sfg_color, font=(Theme.font_type,12,"normal"), text="Test Type: Normal")
        self.progressbar_frame = ctk.CTkFrame(self.inner_frame, corner_radius=0, fg_color=Theme.fg_color)
        self.progressbar = ctk.CTkProgressBar(self.progressbar_frame, height=25, fg_color=Theme.bg_color, progress_color=Theme.accent)
        self.progressbar.set(0)
        self.progressbar_label = ctk.CTkLabel(self.progressbar_frame, text_color=Theme.text_color, text="0%", font=(Theme.font_type, 25, "bold"), width=30)
        self.button_frame = ctk.CTkFrame(self.inner_frame, corner_radius=0, fg_color=Theme.fg_color, height=0)
        self.time_left_label = ctk.CTkLabel(self.button_frame, anchor="e", text="Estimated Time: -- seconds", corner_radius=0, fg_color=Theme.fg_color, font=(Theme.font_type,15,"normal"), text_color=Theme.text_color)
        self.view_details_button = ctk.CTkButton(self.button_frame, corner_radius=10, image=Icons.view_more_image, width=180, height=40, text="Show more details", font=(Theme.font_type,15,"normal"), fg_color=Theme.sfg_color, hover_color=Theme.accent_hover, text_color=Theme.text_color, cursor="hand2", command=self._show_more)
        self.details_listbox = CTkListbox(self.frame, item_fg_color=Theme.bg_color, corner_radius=10, max_items=50, header_text="", fg_color=Theme.bg_color, item_text_color=Theme.text_color, border_width=1, border_color=Theme.accent, item_font=(Theme.font_type,16,"normal"), scrollbar_fg_color=Theme.accent_hover, scrollbar_hover_color=Theme.accent)
        self.details_listbox._parent_frame._scrollbar.grid_configure(padx=5)

    def place_frame(self):
        self.frame.pack(side="left", padx=40, pady=30, expand=True, fill="both")
        self.inner_frame.pack(expand=True, padx=5, pady=5, fill="x")
        self.previous_test_label.pack()
        self.test_parameters_frame.pack(pady=15)
        self.test_device_status.pack(side="left", padx=5)
        self.test_packets.pack(side="left", padx=5)
        self.test_type.pack(side="left", padx=5)
        self.progressbar_frame.pack(pady=(30,20), fill="x")
        self.progressbar.pack(side="left", fill="x", padx=(30,0), expand=True)
        self.progressbar_label.pack(side="left", padx=20)
        self.button_frame.pack(padx=20, fill="x")
        self.view_details_button.pack(side="left")
        self.time_left_label.pack(side="left", fill="x", expand=True)

    def _show_more(self):
        self.details_listbox.pack(expand=True, padx=20, pady=(0,20), fill="both")
        self.view_details_button.configure(text="Show less details", image=Icons.view_less_image, command=self._show_less)
        self.details_on = True

    def _show_less(self):
        self.details_listbox.pack_forget()
        self.view_details_button.configure(text="Show more details", image=Icons.view_more_image, command=self._show_more)
        self.details_on = False

    def update_frame(self):
        self.frame.configure(border_color=Theme.accent)
        self.previous_test_label.configure(font=(Theme.font_type,25,"bold"))
        self.test_device_status.configure(font=(Theme.font_type,12,"normal"))
        self.test_packets.configure(font=(Theme.font_type,12,"normal"))
        self.test_type.configure(font=(Theme.font_type,12,"normal"))
        self.progressbar.configure(progress_color=Theme.accent)
        self.progressbar_label.configure(font=(Theme.font_type, 25, "bold"))
        self.view_details_button.configure(font=(Theme.font_type,15,"normal"), hover_color=Theme.accent_hover)
        self.details_listbox.configure(border_color=Theme.accent, item_font=(Theme.font_type,16,"normal"), scrollbar_fg_color=Theme.accent_hover, scrollbar_hover_color=Theme.accent)
        self.time_left_label.configure(font=(Theme.font_type,15,"normal"))

class PreferencesWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("XSI - Preferences")
        self.geometry(f"400x400+{int(self.winfo_screenwidth()/2 - 200)}+{int(self.winfo_screenheight()/2.2 - 200)}")
        self.minsize(400,400)
        self.maxsize(400,400)

        if __system__.startswith("win"): self.grab_set()

        self.top_root = ctk.CTkFrame(self, corner_radius=0, fg_color=Theme.bg_color)
        self.top_root.pack(expand=True, fill="both")

        self.theme_value = ctk.StringVar(value=Theme.theme_name_selected)
        self.detail_indicator_value = ctk.StringVar(value=Theme.detail_indicator)
        self.font_value = ctk.StringVar(value=Theme.font_type)
        self.apply_settings: bool = False

        self.create_frame()
        self.place_frame()

    def create_frame(self):
        self.frame = ctk.CTkFrame(self.top_root, corner_radius=10, fg_color=Theme.fg_color, border_width=3, border_color=Theme.accent)
        self.label = ctk.CTkLabel(self.frame, text_color=Theme.text_color, text="Preferences", font=(Theme.font_type,20,"bold"), width=160)
        self.theme_label = ctk.CTkLabel(self.frame, text_color=Theme.text_color, text="Theme", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.theme_dropdown = ctk.CTkComboBox(self.frame, values=Theme.theme_names, variable=self.theme_value, text_color=Theme.text_color, fg_color=Theme.sfg_color, corner_radius=10, border_width=1, border_color=Theme.accent, button_color=Theme.accent, button_hover_color=Theme.accent_hover, font=(Theme.font_type,12,"normal"), width=170)
        self.detail_indicator_label = ctk.CTkLabel(self.frame, text_color=Theme.text_color, text="Details Indicator", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.detail_indicator_dropdown = ctk.CTkComboBox(self.frame, values=Theme.detail_indicators, variable=self.detail_indicator_value, text_color=Theme.text_color, fg_color=Theme.sfg_color, corner_radius=10, border_width=1, border_color=Theme.accent, button_color=Theme.accent, button_hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"), width=170)
        self.font_label = ctk.CTkLabel(self.frame, text_color=Theme.text_color, text="Application Font", fg_color=Theme.sfg_color, corner_radius=10, font=(Theme.font_type,15,"normal"))
        self.font_dropdown = ctk.CTkComboBox(self.frame, values=Theme.theme_fonts, variable=self.font_value, text_color=Theme.text_color, fg_color=Theme.sfg_color, border_width=1, corner_radius=10, border_color=Theme.accent, button_color=Theme.accent, button_hover_color=Theme.accent_hover, font=(Theme.font_type,15,"normal"), width=170)
        self.save_button = ctk.CTkButton(self.frame, text_color=Theme.text_color, fg_color=Theme.sfg_color, hover_color=Theme.accent_hover, text="Apply Settings", corner_radius=10, height=40, width=170, font=(Theme.font_type,15,"normal"), command=self.destroy_window)

    def place_frame(self):
        self.frame.pack(fill="both", padx=20, pady=20, expand=True)
        self.label.grid(row=0, column=0, columnspan=10, padx=100, pady=(20,0))
        self.theme_label.grid(row=1, column=0, sticky="w", padx=15, pady=(15,0))
        self.theme_dropdown.grid(row=1, column=1, sticky="w", pady=(15,0))
        self.detail_indicator_label.grid(row=2, column=0, sticky="w", padx=15, pady=(15,0))
        self.detail_indicator_dropdown.grid(row=2, column=1, sticky="w", pady=(15,0))
        self.font_label.grid(row=3, column=0, sticky="w", padx=15, pady=(15,0))
        self.font_dropdown.grid(row=3, column=1, sticky="w", pady=(15,0))
        self.save_button.grid(row=4, column=0, columnspan=10, pady=(100,0))
        
    def destroy_window(self):
        self.apply_settings = True
        self.destroy()

    def get_preferences(self):
        return [self.theme_value.get(), self.detail_indicator_value.get(), self.font_value.get()]
    
class App(Base):
    def __init__(self):
        super().__init__()

        self.nf = NavigationFrame(self.root)
        self.of = OptionsFrame(self.root)
        self.tf = TestingFrame(self.root)

        self.create_all_frames()

        self.nf.place_frame()
        self.of.place_frame()
        self.of.hide_frame()
        self.tf.place_frame()

        self.nf.test_button.configure(command=self.show_testing_frame_settings)
        self.nf.device_button.configure(command=self.show_device_frame)
        self.nf.start_test_button.configure(command=self.start_test)
        self.nf.info_button.configure(command=self.show_app_info_frame)
        self.nf.preferences_button.configure(command=self.open_preferences_window)

        # Testing Parameters
        self.file_name: str = ""
        self.file_type: str = ""
        self.file_location: str = ""
        self.packet_amount: int = 0
        self.packet_indicator: str = ""
        self.auto_stop_value: str = ""
        self.device_name: str = ""
        self.custom_test_on: bool = False
        
        self.dial: str = "/"
        self.test_on: bool = True
        self.progressbar_loop: bool = False
        self.packets_stop_test: bool = True
        self.custom_options: list = []

        self.progress_queue: Queue = Queue()
        self.details_queue: Queue = Queue()
        self.dial_queue: Queue = Queue()
        self.time_left_queue: Queue = Queue()
        
        self.bind("<Configure>", self.resize_nav_frame)
        self.bind("<<ChangeProgressBar>>", self.update_progress)
        self.bind("<<UpdateListbox>>", self.update_listbox)
        self.bind("<<ChangeDial>>", self.switch_dial)
        self.bind("<<ChangeTimeLeft>>", self.update_remaining_time)

    def create_all_frames(self):
        self.nf.create_frame()
        self.of.create_frame()
        self.tf.create_frame()

    def resize_nav_frame(self, event):
        if event.widget == self.root:
            self.nf.resize_frame(root_size=event.width)

    def show_testing_frame_settings(self):
        self.of.place_frame()
        self.of.show_frame()
        self.of.hide_devices()
        self.of.hide_app_info()
        self.of.display_test_settings()

        self.nf.test_button.configure(command=self.hide_all_options)
        self.nf.device_button.configure(command=self.show_device_frame)
        self.nf.info_button.configure(command=self.show_app_info_frame)

    def show_device_frame(self):
        self.of.place_frame()
        self.of.show_frame()
        self.of.hide_test_settings()
        self.of.hide_app_info()
        self.of.display_devices()

        self.nf.device_button.configure(command=self.hide_all_options)
        self.nf.test_button.configure(command=self.show_testing_frame_settings)
        self.nf.info_button.configure(command=self.show_app_info_frame)

    def show_app_info_frame(self):
        self.of.place_frame()
        self.of.show_frame()
        self.of.hide_test_settings()
        self.of.hide_devices()
        self.of.display_app_info()
        
        self.nf.info_button.configure(command=self.hide_all_options)
        self.nf.test_button.configure(command=self.show_testing_frame_settings)
        self.nf.device_button.configure(command=self.show_device_frame)

    def hide_all_options(self):
        self.of.hide_test_settings()
        self.of.hide_devices()
        self.of.hide_frame()
        self.of.hide_app_info()

        self.nf.test_button.configure(command=self.show_testing_frame_settings)
        self.nf.device_button.configure(command=self.show_device_frame)
        self.nf.info_button.configure(command=self.show_app_info_frame)

    def configure_test_parameters(self):
        options: list = self.of.get_all_option_values()

        self.file_name = options[0]
        if options[1] == "default": self.file_location = __file_dir__
        else: self.file_location = options[1]
        self.file_type = options[2]
        if options[3] < 0: self.packet_amount = 1
        else: self.packet_amount = options[3]
        self.packet_indicator = options[4]
        self.packets_stop_test = options[5]
        self.auto_stop_value = options[6]
        self.device_name = options[7]
        self.custom_test_on = options[8]

    def open_preferences_window(self):
        pw = PreferencesWindow()
        pw.wait_window()

        if pw.apply_settings == True:
            options: list = pw.get_preferences()
            
            Theme.change_theme(theme_name=options[0], font_name=options[2])
            Theme.detail_indicator = options[1]

            self.nf.update_frame()
            self.of.update_frame()
            self.tf.update_frame()
            self.update()

    def start_test(self):
        self.test_on = True
        self.configure_test_parameters()
        self.hide_all_options()
        self.nf.test_button.configure(state="disabled", image=Icons.disabled_test_image)
        self.nf.device_button.configure(state="disabled", image=Icons.disabled_device_image)
        if self.winfo_width() >= 1000: self.nf.start_test_button.configure(image=Icons.stop_image, text="Stop Test", command=self.stop_test)
        else: self.nf.start_test_button.configure(image=Icons.stop_image, command=self.stop_test)
        
        if self.custom_test_on: 
            try:
                if ct.show_options:
                    co = ct.CustomOptions()
                    co.wait_window()
                    if co.items_saved:
                        self.custom_options = co.get_values()
                    else: ct.raise_error = True
            except: pass

        self.setup_test()

        Thread(target=self.read_stream, daemon=True).start()

    def stop_test(self, ask:bool=True):
        match ask:
            case True:
                if messagebox.askyesno("XSI - Stop Test?", "Are you sure you want to stop the current test (your test file will still be saved)?", icon="warning"):
                    self.test_on = False
                    self.progressbar_loop = False
                    self.nf.test_button.configure(state="normal", image=Icons.test_image)
                    self.nf.device_button.configure(state="normal", image=Icons.device_image)
                    if self.winfo_width() >= 1000: self.nf.start_test_button.configure(image=Icons.start_image, text="Start Test", command=self.start_test)
                    else: self.nf.start_test_button.configure(image=Icons.start_image, command=self.start_test)
                    self.tf.previous_test_label.configure(text=f"Previous Test: {self.file_name}")
            case False:
                self.test_on = False
                self.progressbar_loop = False
                self.nf.test_button.configure(state="normal", image=Icons.test_image)
                self.nf.device_button.configure(state="normal", image=Icons.device_image)
                if self.winfo_width() >= 1000: self.nf.start_test_button.configure(image=Icons.start_image, text="Start Test", command=self.start_test)
                else: self.nf.start_test_button.configure(image=Icons.start_image, command=self.start_test)
                self.tf.previous_test_label.configure(text=f"Previous Test: {self.file_name}")

        try: 
            if self.custom_test_on: self.custom_test.end_file_output()
        except: pass

    def read_stream(self):
        try:
            xbee = serial.Serial(self.device_name, 9600)
            packet_count: int = 0
            line_count: int = 0

            packet_start: int = 0
            time_start: float = datetime.timestamp(datetime.now())
            time_end: float = 0.0
            time_left: float = 0.0
            
            if self.custom_test_on:
                if ct.raise_error: raise RuntimeError
                try: self.custom_test = ct.Loop(self.custom_options, file_path=self.file_location+__path_separator__+self.file_name+self.file_type)
                except: pass

            with open(self.file_location+__path_separator__+self.file_name+self.file_type, "w") as file: 
                file.write("================== Test Parameters ==================\n")
                file.write(f"Test Info:\n")
                file.write(f"file_name: {self.file_name}\n")
                if self.packet_amount: file.write(f"packet_count: {self.packet_amount}\n")
                else: file.write("packet_count: None\n")
                file.write(f"xbee_device_port: {self.device_name}\n")
                file.write(f"time_started: {clk.get_computer_time(format=24, disable_seconds=True)}\n")
                file.write(f"date_conducted: {clk.get_computer_date()}\n")
                file.write("\n================== Data Collected ==================\n")

            if self.packet_amount == 0:
                self.progressbar_loop = True
                Thread(target=self.run_progressbar_loop, daemon=True).start()
                self.tf.time_left_label.configure(text=f"Time Started: {clk.get_computer_time(disable_seconds=True, format=24)}")

            while self.test_on:
                try: data = xbee.readline().decode(errors="ignore").rstrip()
                except serial.serialutil.SerialException: raise serial.serialutil.SerialException
                except: data = "Error"
 
                line_count += 1
                if self.custom_test_on: self.custom_test.loop(data, packet_count)

                with open(self.file_location+__path_separator__+self.file_name+self.file_type, "a") as file:
                    if self.custom_test_on: 
                        if self.custom_test.write_to_file == True: file.write(f"{datetime.now()},{line_count},{self.custom_test.file_output(data)}\n")
                    else: file.write(f"{datetime.now()},{line_count},{data}\n")

                if self.packet_indicator in data and self.packet_amount != 0: 
                    packet_count += 1

                    if (packet_count - packet_start == 5):
                        time_end = datetime.timestamp(datetime.now())
                        time_left = ((time_end-time_start)/(packet_count-packet_start))*(self.packet_amount-packet_count)
                        time_start = time_end
                        packet_start = packet_count
                        if time_left >= 0:
                            self.time_left_queue.put(f"Estimated Time: {clk.convert_seconds(time_left)}")
                            self.event_generate("<<ChangeTimeLeft>>")

                    self.progress_queue.put(packet_count/self.packet_amount)
                    self.event_generate("<<ChangeProgressBar>>")
                        
                if self.packet_amount == 0: 
                    self.dial_queue.put(self.dial)
                    self.event_generate("<<ChangeDial>>")

                if self.tf.details_on:
                    try:
                        if self.custom_test_on: 
                            if self.custom_test.write_to_file: 
                                self.details_queue.put(f"{Theme.detail_indicator} {datetime.now()},{line_count},{self.custom_test.file_output(data)}")
                                self.event_generate("<<UpdateListbox>>")
                        else: 
                            self.details_queue.put(f"{Theme.detail_indicator} {datetime.now()},{line_count},{data}")
                            self.event_generate("<<UpdateListbox>>")
                    except: pass

                if packet_count == self.packet_amount and self.packet_amount > 0 and self.packets_stop_test == True: 
                    self.stop_test(ask=False)
                    messagebox.showinfo("XSI - Test Completed", f"Test {self.file_name} completed successfully! You can find it at {self.file_location}")

                if self.auto_stop_value in data: 
                    self.stop_test(ask=False)
                    messagebox.showinfo("XSI - Test Completed", f"Test {self.file_name} completed successfully! You can find it at {self.file_location}")
        except serial.serialutil.SerialException:
            messagebox.showerror("XSI - Device Error", "The device selected either disconnected or does not exist!", icon="error")
            self.tf.test_device_status.configure(text="Device Status: Disconnected")
            self.stop_test(ask=False)
        except RuntimeError:
            messagebox.showerror("XSI - Runtime Error", "The custom test could not be completed or was cancelled!", icon="error")
            self.stop_test(ask=False)
        except: 
            messagebox.showerror("XSI - Runtime Error", "Unknown Error has occurred, shutting down test!", icon="error")
            self.stop_test(ask=False)

    def setup_test(self):
        self.tf.previous_test_label.configure(text=f"Test Running: {self.file_name}")
        self.tf.test_device_status.configure(text="Device Status: Connected")
        self.tf.test_packets.configure(text=f"Packet Count: {self.packet_amount}")
        if self.custom_test_on: self.tf.test_type.configure(text="Test Type: Custom")
        else: self.tf.test_type.configure(text="Test Type: Normal")
        self.tf.details_listbox.clear()
        self.tf.progressbar.configure(fg_color=Theme.bg_color, progress_color=Theme.accent)
        self.tf.progressbar.set(0)
        self.tf.time_left_label.configure(text="Estimated Time: -- seconds")

    def update_progress(self, event=None):
        progress: float = self.progress_queue.get()
        if progress > 1: progress = 1
        self.tf.progressbar.set(progress)
        self.tf.progressbar_label.configure(text=f"{progress*100:.1f}%")

    def run_progressbar_loop(self):
        while self.progressbar_loop:
            self.tf.progressbar.configure(fg_color=Theme.bg_color, progress_color=Theme.accent)
            self.tf.progressbar.set(0)
            for i in range(0,100,1):
                self.tf.progressbar.set(i/100)
                clk.sleep(0.01)
            self.tf.progressbar.configure(fg_color=Theme.accent, progress_color=Theme.accent)
            self.tf.progressbar.set(1)
            clk.sleep(1)
            self.tf.progressbar.set(0)
            self.tf.progressbar.configure(fg_color=Theme.accent, progress_color=Theme.bg_color)
            for i in range(0,100,1):
                self.tf.progressbar.set(i/100)
                clk.sleep(0.01)
            self.tf.progressbar.configure(fg_color=Theme.bg_color, progress_color=Theme.bg_color)
            self.tf.progressbar.set(1)
            clk.sleep(1)

    def switch_dial(self, event=None):
        dial = self.dial_queue.get()
        match dial:
            case "\\": 
                self.dial = "|"
                self.tf.progressbar_label.configure(text=self.dial)
            case "|": 
                self.dial = "/"
                self.tf.progressbar_label.configure(text=self.dial)
            case "/": 
                self.dial = "-"
                self.tf.progressbar_label.configure(text=self.dial)
            case "-": 
                self.dial = "\\"
                self.tf.progressbar_label.configure(text=self.dial)

    def update_listbox(self, event=None):
        self.tf.details_listbox.insert_item(self.details_queue.get())
        self.tf.details_listbox.see()

    def update_remaining_time(self, event=None):
        self.tf.time_left_label.configure(text=self.time_left_queue.get())

if __name__ == "__main__":
    xsi = App()
    xsi.mainloop()