from customtkinter import CTkToplevel, CTkFrame, CTkProgressBar, CTkButton, CTkEntry, CTkComboBox, CTkSwitch, CTkLabel, CTkScrollableFrame, StringVar, filedialog
from modules.app_tools.ctk_listbox import CTkListbox
from queue import Queue
from threading import Thread
from serial import Serial
from serial.tools.list_ports import comports
from time import sleep

from modules.theme import ThemeManager, IconManager
import modules.app_tools.tools as tools

__base_dir__ = tools.parse_dir_path(__file__, "bin_windows")

class ProgressbarWindow(CTkToplevel, ThemeManager, IconManager):
    def __init__(self, classname) -> None:
        super().__init__()

        self.geometry(f"400x100+{int(self.winfo_screenwidth()/2 - 200)}+{int(self.winfo_screenheight()/2.2 - 50)}")
        self.title("XSI - Test Progress")
        
        self.classname = classname

        self._queue_percent: Queue = Queue()
        self.bind("<<update_progressbar>>", self._update_progress_bar)
        self._check_on: bool = True

        self.orientation: str = "horizontal"

        self._parent_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self._progress_text = CTkLabel(self._parent_frame, text="0.0%", text_color=self.text_color["normal"], font=("Arial", 17, "bold"))
        self._progressbar = ...
        self._progress_switch_view = CTkButton(self._parent_frame, text="", image=self.rotate_image, width=30, height=30, fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"], corner_radius=20, command=self._switch_view)
        
        self._parent_frame.pack(expand=True, fill="both")
        self._switch_view()
        self._start_check_progress()

    def _switch_view(self):
        if self.orientation == "horizontal":
            self._place_progressbar(self.orientation)
            self.orientation = "vertical"
        elif self.orientation == "vertical":
            self._place_progressbar(self.orientation)
            self.orientation = "horizontal"

    def _place_progressbar(self, orientation:str):
        try: self._progressbar.destroy()
        except: pass
        self._progress_text.pack_forget()
        self._progress_switch_view.pack_forget()

        match orientation:
            case "horizontal": 
                self.maxsize(0,60)
                self._progress_text.pack(side="left", padx=(20,5), pady=(10,0))
                self._progressbar = CTkProgressBar(self._parent_frame, height=20, orientation=orientation, fg_color=self.color["bg_light"], progress_color=self.color["secondary"])
                self._progressbar.set(0)
                self._progressbar.pack(fill="x", expand=True, side="left", padx=5, pady=(10,0))
                self._progress_switch_view.pack(side="left", padx=(5,20), pady=(10,0))
            case "vertical":
                self.maxsize(300,0)
                self._progress_text.pack(side="top", padx=(10,0), pady=(20,5))
                self._progressbar = CTkProgressBar(self._parent_frame, width=20, orientation=orientation, fg_color=self.color["bg_light"], progress_color=self.color["secondary"])
                self._progressbar.set(0)
                self._progressbar.pack(fill="y", expand=True, side="top", padx=(10,0), pady=5)
                self._progress_switch_view.pack(side="top", padx=(10,0), pady=(5,20))

    def _start_check_progress(self):
        Thread(target=self._check_progress, daemon=True).start()

    def _check_progress(self):
        while self._check_on:
            try:
                self._queue_percent.put(self.classname.percent)
                self.event_generate("<<update_progressbar>>")
                sleep(1)
            except: pass

    def _update_progress_bar(self, event=None) -> None:
        percent = self._queue_percent.get()
        self._progress_text.configure(text=f"{eval(f"{round(percent*100,1)}")}%")
        self._progressbar.set(eval(f"{round(percent,3)}"))

    def stop_check(self):
        self._check_on = False
            
class SetupWindow(CTkToplevel, ThemeManager):
    def __init__(self, file_name:str, file_location:str, file_type:str, enable_progressbar:bool, packet_count:int, packet_indicator:str, stop_value:str) -> None:
        super().__init__()

        self.geometry(f"430x500+{int(self.winfo_screenwidth()/2 - 215)}+{int(self.winfo_screenheight()/2.2 - 300)}")
        self.grab_set()
        self.title("XSI - Test Configurations")
        self.maxsize(430,500)
        self.minsize(430,500)
        
        self.file_name = file_name
        self.file_location = file_location
        self.file_type = file_type
        self.enable_progressbar = enable_progressbar
        self.packet_count = packet_count
        self.packet_indicator = packet_indicator
        self.stop_value = stop_value

        self._parent_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self._parent_frame.pack(expand=True, fill="both")

        self._file_name_value = StringVar(value=self.file_name)
        self._file_loc_value = StringVar(value=self.file_location)
        self._file_type_value = StringVar(value=self.file_type)
        self._track_test_progress_value = StringVar(value=self.enable_progressbar)
        self._packet_value = StringVar(value=f"{self.packet_count}")
        self._packet_indicator_value = StringVar(value=self.packet_indicator)
        self._end_lookout_value = StringVar(value=self.stop_value)

        self._create_setup_window_objects()
        self._place_setup_window()

        self._track_test_progress_switch.toggle()
        self._switch_track_test_progress()

    def _create_setup_window_objects(self) -> None:
        _file_type_values: list = [".txt", ".csv"]
        _packet_indicator_values: list = [".", "/", "\\", ">", "<", ",", "!", "&", "#", "@", "*"]
        
        self._settings_frame = CTkScrollableFrame(self._parent_frame, label_text="Test Configurations", label_fg_color=self.color["bg"], label_font=self.font["toplevel_title"], label_text_color=self.text_color["normal"], border_width=3, scrollbar_button_color=self.color["bg_light"], scrollbar_button_hover_color=self.color["secondary"], border_color=self.color["secondary"], fg_color=self.color["bg"], corner_radius=10)
        self._file_name_label = CTkLabel(self._settings_frame, text="Test Name", text_color=self.text_color["normal"], font=self.font["toplevel_option"], height=30, fg_color=self.color["bg_light"], corner_radius=10)
        self._file_loc_label = CTkLabel(self._settings_frame, text="Save Location", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10)
        self._file_type_label = CTkLabel(self._settings_frame, text="File Type", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10)
        self._track_test_progress_label = CTkLabel(self._settings_frame, text="Track Progress", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10)
        self._packet_label = CTkLabel(self._settings_frame, text="Test Packets", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10)
        self._packet_indicator_label = CTkLabel(self._settings_frame, text="Packet Indicator", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10)
        self._end_lookout_label = CTkLabel(self._settings_frame, text="Stop Value", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10)
        self._file_name_entry = CTkEntry(self._settings_frame, width=200, height=30, text_color=self.text_color["normal"], textvariable=self._file_name_value, fg_color=self.color["bg_light"], border_color=self.color["secondary"], border_width=1, corner_radius=5)
        self._file_loc_entry = CTkEntry(self._settings_frame, width=100, height=30, text_color=self.text_color["normal"], textvariable=self._file_loc_value, fg_color=self.color["bg_light"], border_color=self.color["secondary"], border_width=1, corner_radius=5)
        self._file_loc_button = CTkButton(self._settings_frame, text="Browse", text_color=self.text_color["normal"], width=70, height=30, fg_color=self.color["bg_light"], hover_color=self.color["secondary"], corner_radius=5, command=self._browse_dir)
        self._file_type_dropdown = CTkComboBox(self._settings_frame, width=200, height=30, text_color=self.text_color["normal"], variable=self._file_type_value, values=_file_type_values, fg_color=self.color["bg_light"], justify="center", border_width=1, border_color=self.color["secondary"], button_color=self.color["secondary"], button_hover_color=self.color["bg_light"])
        self._track_test_progress_switch = CTkSwitch(self._settings_frame, switch_width=60, switch_height=25, variable=self._track_test_progress_value, text="", progress_color=self.color["secondary"], button_hover_color=self.color["hover_light"], command=self._switch_track_test_progress)
        self._packet_entry = CTkEntry(self._settings_frame, width=200, height=30, text_color=self.text_color["normal"], textvariable=self._packet_value, fg_color=self.color["bg_light"], border_color=self.color["secondary"], border_width=1, corner_radius=5)
        self._packet_indicator_dropdown = CTkComboBox(self._settings_frame, width=200, text_color=self.text_color["normal"], height=30, variable=self._packet_indicator_value, values=_packet_indicator_values, font=self.font["toplevel_option"], justify="center", fg_color=self.color["bg_light"], border_color=self.color["secondary"], border_width=1, button_color=self.color["secondary"], button_hover_color=self.color["bg_light"], corner_radius=5)
        self._end_lookout_entry = CTkEntry(self._settings_frame, width=200, height=30, text_color=self.text_color["normal"], textvariable=self._end_lookout_value, border_width=1, border_color=self.color["secondary"], fg_color=self.color["bg_light"], corner_radius=5)
        self._save_button = CTkButton(self._parent_frame, width=150, height=40, text="Save", text_color=self.text_color["normal"], font=self.font["toplevel_option"], fg_color=self.color["bg_light"], hover_color=self.color["secondary"], corner_radius=10, command=self._save_test_parameters)

        self._settings_frame._scrollbar.grid_configure(padx=5)

    def _place_setup_window(self) -> None:
        self._settings_frame.pack(expand=True, fill="both", padx=15, pady=(10,0))
        self._file_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))
        self._file_name_entry.grid(row=0, column=1, columnspan=10, sticky="w", pady=(10,0))
        self._file_loc_label.grid(row=1, column=0, sticky="w", padx=10, pady=(20,0))
        self._file_loc_entry.grid(row=1, column=1, pady=(20,0), sticky="w")
        self._file_loc_button.grid(row=1, column=2, padx=10, pady=(20,0), sticky="w")
        self._file_type_label.grid(row=2, column=0, sticky="w", padx=(10,40), pady=(20,0))
        self._file_type_dropdown.grid(row=2, column=1, sticky="w", columnspan=10, pady=(20,0))
        self._track_test_progress_label.grid(row=3, column=0, sticky="w", padx=10, pady=(20,0))
        self._track_test_progress_switch.grid(row=3, column=1, sticky="w", pady=(20,0))
        self._packet_label.grid(row=4, column=0, sticky="w", padx=10, pady=(20,0))
        self._packet_entry.grid(row=4, column=1, columnspan=10, sticky="w", pady=(20,0))
        self._packet_indicator_label.grid(row=5, column=0, sticky="w", padx=10, pady=(20,0))
        self._packet_indicator_dropdown.grid(row=5, column=1, columnspan=10, sticky="w", pady=(20,0))
        self._end_lookout_label.grid(row=6, column=0, sticky="w", padx=10, pady=(20,0))
        self._end_lookout_entry.grid(row=6, column=1, columnspan=10, sticky="w", pady=(20,0))
        self._save_button.pack(pady=10)

    def _switch_track_test_progress(self) -> None:
        _state = int(self._track_test_progress_value.get())
        match _state:
            case 0:
                self._packet_entry.configure(state="disabled", text_color=self.text_color["disabled"])
                self._packet_label.configure(text_color=self.text_color["disabled"])
                self._packet_indicator_dropdown.configure(state="disabled", text_color=self.text_color["disabled"])
                self._packet_indicator_label.configure(text_color=self.text_color["disabled"])
            case 1:
                self._packet_entry.configure(state="normal", text_color=self.text_color["normal"])
                self._packet_label.configure(text_color=self.text_color["normal"])
                self._packet_indicator_dropdown.configure(state="normal", text_color=self.text_color["normal"])
                self._packet_indicator_label.configure(text_color=self.text_color["normal"])

    def _browse_dir(self) -> None:
        self._file_loc_value.set(filedialog.askdirectory(initialdir=__base_dir__+"\\cache"))

    def _save_test_parameters(self) -> None:
        _state = int(self._track_test_progress_value.get())
        self.file_name = self._file_name_value.get()
        self.file_location = self._file_loc_value.get()
        self.file_type = self._file_type_value.get()
        match _state:
            case 0: self.enable_progressbar = False
            case 1:
                self.enable_progressbar = True
                self.packet_count = int(self._packet_value.get())
                self.packet_indicator = self._packet_indicator_value.get()
        self.stop_value = self._end_lookout_value.get()

        self.destroy()

    def get_test_parameters(self) -> dict:
        return {"file_name":self.file_name,"file_location":self.file_location,"file_type":self.file_type,"enable_progressbar":self.enable_progressbar,"packet_count":self.packet_count,"packet_indicator":self.packet_indicator,"stop_value":self.stop_value}

class DeviceWindow(CTkToplevel, ThemeManager, IconManager):
    def __init__(self) -> None:
        super().__init__()

        self.geometry(f"430x500+{int(self.winfo_screenwidth()/2 - 215)}+{int(self.winfo_screenheight()/2.2 - 300)}")
        self.grab_set()
        self.title("XSI - Devices")
        self.maxsize(430,500)
        self.minsize(430,500)

        self.device_selected: str|None = None

        self._parent_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self._parent_frame.pack(expand=True, fill="both")

        self._devices: list = [(port[0],port[1]) for port in comports()]
        self._devices_objects: list = []
        self._button_id: int = 0

        self._create_device_window_objects()
        self._place_device_window()
        
    def _create_device_window_objects(self) -> None:
        _index: int = 0
        self._device_frame = CTkListbox(self._parent_frame, border_width=3, header_fg_color=self.color["bg"], header_font=self.font["toplevel_title"], header_text_color=self.text_color["normal"], header_text="Select a Device", scrollbar_fg_color=self.color["bg_light"], scrollbar_hover_color=self.color["secondary"], border_color=self.color["secondary"], fg_color=self.color["bg"], corner_radius=10)
        for device_tuple in self._devices:
            _index += 1   
            _button = CTkButton(self._device_frame.cget("parent_frame"), text=f"{device_tuple[0]} || {device_tuple[1]}", text_color=self.text_color["normal"], width=300, height=50, corner_radius=10, font=self.font["device_button"], hover_color=self.color["hover_light"], fg_color=self.color["bg_light"], command=lambda id=_index: self._select_button(id))
            self._devices_objects.append(_button)
        self.df_refresh_button = CTkButton(self._parent_frame, width=60, height=40, text="", image=self.refresh_image, text_color=self.text_color["normal"], corner_radius=50, fg_color=self.color["bg_light"], hover_color=self.color["secondary"], command=self._refresh_devices)
        self.df_submit_button = CTkButton(self._parent_frame, width=160, height=40, text="Save Device", text_color=self.text_color["normal"], corner_radius=10, font=self.font["toplevel_option"], fg_color=self.color["bg_light"], hover_color=self.color["secondary"], command=self._save_device)
        
        self._device_frame._parent_frame._scrollbar.grid_configure(padx=5)

    def _refresh_devices(self):
        self._devices.clear()
        self._devices_objects.clear()
        self._device_frame.clear()

        self.devices = [(port[0],port[1]) for port in comports()]
        _index: int = 0
        
        for device_tuple in self.devices:
            _index += 1   
            _button = CTkButton(self._device_frame.cget("parent_frame"), text=f"{device_tuple[0]} || {device_tuple[1]}", text_color=self.text_color["normal"], width=300, height=50, corner_radius=10, font=self.font["device_button"], hover_color=self.color["hover_light"], fg_color=self.color["bg_light"], command=lambda id=_index: self._select_button(id))
            self._devices_objects.append(_button)

        self._place_device_window()

    def _place_device_window(self) -> None:
        self.df_refresh_button.pack(anchor="e", padx=10, pady=10)
        self._device_frame.pack(expand=True, fill="both", padx=15)

        _index: int = 0
        for object in self._devices_objects: 
            _index += 1
            self._device_frame.insert_ctkobject(object, fill="x", padx=10, pady=10)

        self.df_submit_button.pack(pady=20)
        
    def _select_button(self, button_id) -> None:
        for id in range(1,len(self._devices_objects)+1):
            if id == button_id: 
                self._devices_objects[button_id-1].configure(state="active", fg_color=self.color["secondary"])
                self._button_id = button_id
            else: self._devices_objects[id-1].configure(state="normal", fg_color=self.color["bg_light"])
            
    def _save_device(self) -> None: 
        self.device_selected = tools.read_until(self._devices_objects[self._button_id-1].cget("text"), "|").rstrip().lstrip()
        if self.device_selected != None: 
            dw = DeviceCheckWindow(self.device_selected)
            dw.wait_window()
            self.device_selected = dw.get_device_selected()

        if self.device_selected != None: self.destroy()

    def get_device_selected(self) -> str:
        return self.device_selected

class DeviceCheckWindow(CTkToplevel, ThemeManager):
    def __init__(self, device_selected:str) -> None:
        super().__init__()

        self.geometry(f"250x250+{int(self.winfo_screenwidth()/2 - 125)}+{int(self.winfo_screenheight()/2.2 - 125)}")
        self.grab_set()
        self.title("XSI - Devices")
        self.maxsize(250,250)
        self.minsize(250,250)
        
        self.device_selected = device_selected

        self._parent_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self._parent_frame.pack(expand=True, fill="both")

        self._create_device_window_objects()
        self._place_device_window()
        self._run_check()

    def _create_device_window_objects(self) -> None:
        self._device_response = CTkLabel(self._parent_frame, text="Device Response: None", text_color=self.text_color["normal"], font=self.font["device_check"], corner_radius=10, wraplength=160, fg_color=self.color["bg_light"], width=160, height=120)
        self._device_progress = CTkProgressBar(self._parent_frame, width=200, height=10, progress_color=self.color["bg_light"], fg_color=self.color["bg_light"])
        self._device_progress.set(0)

    def _place_device_window(self) -> None:
        self._device_response.pack(pady=(50,20))
        self._device_progress.pack()
    
    def _run_check(self) -> None:
        Thread(target=self._check_device, daemon=True).start()

    def _check_device(self) -> None:
        self._device_progress.set(0)
        self._device_progress.configure(progress_color=self.color["secondary"])
        try:
            _attention = Serial(self.device_selected, 9600, timeout=3)
            _progress: int = 0
            _passed: str = ""
            self._device_response.configure(text="Device Response: Loading")

            _attention.write(bytes("+++", "utf-8"))
            while _progress < 5:
                _passed = _attention.readline().decode()
                if _passed == "OK\r":
                    self._device_progress.set(1)
                    break
                _progress += 1
                self._device_progress.set(eval(f"{round(_progress/5,2)}"))

            _attention.close()

            if _passed == "OK\r": self._device_response.configure(text="Device Response: OK!")
            else: raise
        except:
            self._device_response.configure(text="Device Response: FAILED")
            self.device_selected = None

        self.after(2000, self.destroy)

    def get_device_selected(self) -> str:
        return self.device_selected

class SettingsWindow(CTkToplevel, ThemeManager):
    def __init__(self) -> None:
        super().__init__()

        self.geometry(f"430x500+{int(self.winfo_screenwidth()/2 - 215)}+{int(self.winfo_screenheight()/2.2 - 300)}")
        self.grab_set()
        self.title("XSI - Settings")
        self.maxsize(430,500)
        self.minsize(430,500)

        match self.color["secondary"]:
            case "#9A00FF": _app_theme = "Witchlight Purple"
            case "#00BF85": _app_theme = "Lily Pad Green"
            case "#FF501B": _app_theme = "Moody Orange"
            case "#FF1B67": _app_theme = "Strawberry Red"

        match self.color["bg"]:
            case "#202020": _app_dark_mode = 1
            case "#FDFDFD": _app_dark_mode = 0

        self._app_theme_value = StringVar(value=_app_theme)
        self._app_dark_mode_value = StringVar(value=_app_dark_mode)
        self._app_terminal_newline_value = StringVar(value=self.terminal_indicator)
        self._app_enable_stats_value = StringVar(value=self.enable_stat_frame)
        self._app_enable_clk_value = StringVar(value=self.enable_clock_frame)

        self.master_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)
        self.master_frame.pack(expand=True, fill="both")

        self._create_settings_window_objects()
        self._place_settings_window()
        
        if int(self._app_dark_mode_value.get()) == 1: self.sf_app_dark_mode_switch.toggle()
        if int(self._app_enable_stats_value.get()) == 1: self.sf_app_enable_stats_switch.toggle()
        if int(self._app_enable_clk_value.get()) == 1: self.sf_app_enable_clk_switch.toggle()

    def _create_settings_window_objects(self) -> None:
        _app_theme_values: list = ["Strawberry Red", "Lily Pad Green", "Moody Orange", "Witchlight Purple"]
        _app_terminal_indicator_values: list = [">", "&", "$", "@", ">>", ":"]
        
        self.sf = CTkScrollableFrame(self.master_frame, border_width=3, label_fg_color=self.color["bg"], label_font=self.font["toplevel_title"], label_text_color=self.text_color["normal"], label_text="Settings", scrollbar_button_color=self.color["bg_light"], scrollbar_button_hover_color=self.color["secondary"], border_color=self.color["secondary"], fg_color=self.color["bg"], corner_radius=10)
        self.sf_app_theme_label = CTkLabel(self.sf, text="App Color Theme", fg_color=self.color["bg_light"], height=30, corner_radius=10, text_color=self.text_color["normal"], font=self.font["toplevel_option"])
        self.sf_app_dark_mode_label = CTkLabel(self.sf, text="Dark Mode", fg_color=self.color["bg_light"], corner_radius=10, height=30, text_color=self.text_color["normal"], font=self.font["toplevel_option"])
        self.sf_app_terminal_newline_label = CTkLabel(self.sf, text="Terminal Indicator", fg_color=self.color["bg_light"], corner_radius=10, height=30, text_color=self.text_color["normal"], font=self.font["toplevel_option"])
        self.sf_app_enable_stats_label = CTkLabel(self.sf, text="Enable Statistics", font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10, height=30, text_color=self.text_color["normal"])
        self.sf_app_enable_clk_label = CTkLabel(self.sf, text="Enable Clock", font=self.font["toplevel_option"], fg_color=self.color["bg_light"], corner_radius=10, height=30, text_color=self.text_color["normal"])
        self.sf_app_theme_dropdown = CTkComboBox(self.sf, fg_color=self.color["bg_light"], variable=self._app_theme_value, justify="center", values=_app_theme_values, width=200, height=30, border_width=1, border_color=self.color["secondary"], text_color=self.text_color["normal"], button_color=self.color["secondary"], button_hover_color=self.color["bg_light"], font=self.font["toplevel_option"])
        self.sf_app_dark_mode_switch = CTkSwitch(self.sf, button_hover_color=self.color["hover_light"], switch_width=60, switch_height=25, text="", progress_color=self.color["secondary"], variable=self._app_dark_mode_value)
        self.sf_app_terminal_newline_dropdown = CTkComboBox(self.sf, fg_color=self.color["bg_light"], variable=self._app_terminal_newline_value, justify="center", values=_app_terminal_indicator_values, width=200, height=30, border_width=1, border_color=self.color["secondary"], text_color=self.text_color["normal"], button_color=self.color["secondary"], button_hover_color=self.color["bg_light"], font=self.font["toplevel_option"])
        self.sf_app_enable_stats_switch = CTkSwitch(self.sf, button_hover_color=self.color["hover_light"], switch_width=60, switch_height=25, text="", progress_color=self.color["secondary"], variable=self._app_enable_stats_value)
        self.sf_app_enable_clk_switch = CTkSwitch(self.sf, button_hover_color=self.color["hover_light"], switch_width=60, switch_height=25, text="", progress_color=self.color["secondary"], variable=self._app_enable_clk_value)
        self.sf_save_button = CTkButton(self.master_frame, text="Save", text_color=self.text_color["normal"], width=160, height=40, corner_radius=10, fg_color=self.color["bg_light"], hover_color=self.color["secondary"], font=self.font["toplevel_option"], command=self._save_settings)
        
        self.sf._scrollbar.grid_configure(padx=5)

    def _place_settings_window(self) -> None:
        self.sf.pack(expand=True, fill="both", padx=15, pady=(30,0))
        self.sf_app_theme_label.grid(row=0, column=0, sticky="w", padx=10, pady=(30,0))
        self.sf_app_theme_dropdown.grid(row=0, column=1, sticky="w", pady=(30,0))
        self.sf_app_dark_mode_label.grid(row=1, column=0, sticky="w", padx=10, pady=(20,0))
        self.sf_app_dark_mode_switch.grid(row=1, column=1, sticky="w", pady=(20,0))
        self.sf_app_terminal_newline_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20,0))
        self.sf_app_terminal_newline_dropdown.grid(row=2, column=1, sticky="w", pady=(20,0))
        self.sf_app_enable_stats_label.grid(row=3, column=0, sticky="w", padx=10, pady=(20,0))
        self.sf_app_enable_stats_switch.grid(row=3, column=1, sticky="w", pady=(20,0))
        self.sf_app_enable_clk_label.grid(row=4, column=0, sticky="w", padx=10, pady=(20,0))
        self.sf_app_enable_clk_switch.grid(row=4, column=1, sticky="w", pady=(20,0))
        self.sf_save_button.pack(pady=20)

    def _save_settings(self) -> None:
        ThemeManager.change_theme_color(ThemeManager, self._app_theme_value.get())
        ThemeManager.change_mode(ThemeManager, int(self._app_dark_mode_value.get()))
        ThemeManager.terminal_indicator = self._app_terminal_newline_value.get()
        ThemeManager.enable_stat_frame = int(self._app_enable_stats_value.get())
        ThemeManager.enable_clock_frame = int(self._app_enable_clk_value.get())
        IconManager.change_icon_theme(IconManager, self._app_theme_value.get())
        IconManager.change_icon_mode(IconManager, int(self._app_dark_mode_value.get()))
        self.destroy()

class InfoWindow(CTkToplevel, ThemeManager):
    def __init__(self, app_version, app_name) -> None:
        super().__init__()

        self.geometry(f"430x500+{int(self.winfo_screenwidth()/2 - 215)}+{int(self.winfo_screenheight()/2.2 - 300)}")
        self.maxsize(430,500)
        self.minsize(430,500)
        self.title("XSI - Information")
        self.grab_set()

        self._app_version = app_version
        self._app_name = app_name

        self._bg_frame = CTkFrame(self, fg_color=self.color["bg"], corner_radius=0)

        self._info_title = CTkLabel(self._bg_frame, text="App Information", font=self.font["toplevel_title"], text_color=self.text_color["normal"])
        self._info_build_name = CTkLabel(self._bg_frame, text=f"App Name: {self._app_name}", font=self.font["toplevel_option"], text_color=self.text_color["normal"], wraplength=390, compound="left")
        self._info_build_version = CTkLabel(self._bg_frame, text=f"Version: {self._app_version}", font=self.font["toplevel_option"], text_color=self.text_color["normal"], wraplength=390, compound="left")
        self._info_build_gui = CTkLabel(self._bg_frame, text="Built with: Tkinter, CustomTkinter", font=self.font["toplevel_option"], text_color=self.text_color["normal"], wraplength=390, compound="left")
        self._info_build_modules = CTkLabel(self._bg_frame, text="Required Python External Modules: tkinter (on Linux), customtkinter, pillow (on Windows 11), pyserial", font=self.font["toplevel_option"], text_color=self.text_color["normal"], wraplength=390, compound="left")

        self._bg_frame.pack(expand=True, fill="both")
        self._info_title.grid(row=0, column=0, sticky="W", padx=10, pady=(20,0))
        self._info_build_name.grid(row=1, column=0, sticky="W", padx=10, pady=(20,0))
        self._info_build_version.grid(row=2, column=0, sticky="W", padx=10, pady=(20,0))
        self._info_build_gui.grid(row=3, column=0, sticky="W", padx=10, pady=(20,0))
        self._info_build_modules.grid(row=4, column=0, sticky="W", padx=10, pady=(20,0))