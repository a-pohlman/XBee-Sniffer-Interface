"""

Developer: Aaron Pohlman
Final Date Modified: 02/14/2026
Name: XBee Sniffer Interface (Beta)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from webbrowser import open as open_file
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkProgressBar
from tkinter import messagebox
from serial.tools.list_ports import comports
from serial import Serial
from threading import Thread
from queue import Queue
from datetime import datetime

import modules.app_tools.clock as clk
import modules.app_tools.tools as tools
from modules.app_tools.ctk_listbox import CTkListbox

from modules.xsi_windows import ProgressbarWindow, SetupWindow, DeviceWindow, SettingsWindow, InfoWindow
from modules.theme import ThemeManager, IconManager

__version__ = "0.2.5"
__app_name__ = "XBee Sniffer Interface (Beta)"
__base_dir__ = tools.parse_dir_path(__file__, "bin")

class TestParameters:
    file_name: str = "my_test"
    file_location: str = "default"
    file_type: str = ".txt"
    enable_progressbar: bool = True
    packet_count: int = 5000
    packet_indicator: str = "."
    stop_value: str = ">>>end_of_test"
    device_selected: str|None = None
    percent: int = 0

    def configure_parameters(self, params:dict={}) -> None:
        if "file_name" in params: self.file_name = params.pop("file_name")
        if "file_location" in params: self.file_location = params.pop("file_location")
        if "file_type" in params: self.file_type = params.pop("file_type")
        if "enable_progressbar" in params: self.enable_progressbar = params.pop("enable_progressbar")
        if "packet_count" in params: self.packet_count = params.pop("packet_count")
        if "packet_indicator" in params: self.packet_indicator = params.pop("packet_indicator")
        if "stop_value" in params: self.stop_value = params.pop("stop_value")
        if "device_selected" in params: self.device_selected = params.pop("device_selected")
        if "percent" in params: self.percent = params.pop("percent")

class Base(CTk, ThemeManager, IconManager):
    def __init__(self) -> None:
        super().__init__()

        self.geometry(f"1000x600+{int(self.winfo_screenwidth()/2 - 500)}+{int(self.winfo_screenheight()/2.2 - 300)}")
        self.title("XBee Sniffer Interface")

        self.master_frame = CTkFrame(self, fg_color=ThemeManager.color["bg"], corner_radius=0)
        self.master_frame.pack(expand=True, fill="both")

    def update_master_frame(self) -> None:
        self.master_frame.configure(fg_color=ThemeManager.color["bg"])

class DeviceWidget(Base):
    def __init__(self) -> None:
        super().__init__()

    def create_device_widget_objects(self) -> None:
        self.dof = CTkFrame(self.master_frame, fg_color=ThemeManager.color["secondary"], corner_radius=0, width=53)
        self.dif = CTkFrame(self.dof, fg_color=ThemeManager.color["bg_light"], corner_radius=0, width=50) # ds = device_frame
        self.df_status_label = CTkLabel(self.dif, width=50, height=50, text="", text_color=ThemeManager.text_color["normal"], image=self.device_disconnected, corner_radius=0, fg_color=ThemeManager.color["bg_light"])
        self.df_info_button = CTkButton(self.dif, width=50, height=50, text="", text_color=ThemeManager.text_color["normal"], image=self.info_image, corner_radius=0, fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"], command=lambda: InfoWindow(__version__, __app_name__))
        self.df_help_button = CTkButton(self.dif, width=50, height=50, text="", text_color=ThemeManager.text_color["normal"], image=self.help_image, corner_radius=0, fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"], command=lambda: open_file(__base_dir__+"\\help.pdf"))

    def place_device_widget(self) -> None:
        self.dof.pack(side="left", fill="y") 
        self.dif.pack(side="left", fill="y", padx=(0,3))
        self.df_status_label.pack()
        self.df_help_button.pack(side="bottom")
        self.df_info_button.pack(side="bottom")

    def update_device_widget(self) -> None:
        self.dof.configure(fg_color=ThemeManager.color["secondary"])
        self.dif.configure(self.dof, fg_color=ThemeManager.color["bg_light"], corner_radius=0, width=50)
        self.df_status_label.configure(text_color=ThemeManager.text_color["normal"], fg_color=ThemeManager.color["bg_light"])
        self.df_info_button.configure(text_color=ThemeManager.text_color["normal"], fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"], image=self.info_image)
        self.df_help_button.configure(text_color=ThemeManager.text_color["normal"], fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"], image=self.help_image)

    def update_device_status(self, state:str) -> None:
        match state:
            case "connected": self.df_status_label.configure(image=self.device_connected)
            case "disconnected": self.df_status_label.configure(image=self.device_disconnected)

class SettingsWidget(Base):
    def __init__(self) -> None:
        super().__init__()

        self.clock_on: bool = True
        self._queue_clock_data: Queue = Queue()
        self.bind("<<update_clock>>", self._update_clock)
        self.start_clock()

    def start_clock(self) -> None:
        Thread(target=self._clock, daemon=True).start()

    def stop_clock(self) -> None:
        self.clock_on = False

    def _clock(self) -> None:
        self.clock_on = True
        self._queue_clock_data.put(clk.get_computer_time(disable_seconds=True))
        self.event_generate("<<update_clock>>")
        while self.clock_on:
            self._queue_clock_data.put(clk.get_computer_time(disable_seconds=True))
            self.event_generate("<<update_clock>>")
            clk.sleep(1)

    def _update_clock(self, event=None) -> None:
        self.sf_clock_label.configure(text=self._queue_clock_data.get())

    def create_settings_widget_objects(self) -> None:
        self.sf = CTkFrame(self.master_frame, fg_color=ThemeManager.color["bg"], corner_radius=0, height=80) # sf = settings_frame
        self.sf_configurations_button = CTkButton(self.sf, text="Test Configurations", text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["menu_button"], height=60, border_width=1, border_color=ThemeManager.color["secondary"], corner_radius=10, fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"])
        self.sf_devices_button = CTkButton(self.sf, height=60, text="Select Device", font=ThemeManager.font["menu_button"], border_width=1, text_color=ThemeManager.text_color["normal"], border_color=ThemeManager.color["secondary"], corner_radius=10, fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"])
        self.sf_settings_button = CTkButton(self.sf, height=60, text="Settings", text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["menu_button"], border_width=1, border_color=ThemeManager.color["secondary"], corner_radius=10, fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"])
        self.sf_clock_label = CTkLabel(self.sf, text="01:00 AM", text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["clock"], corner_radius=10, height=60, fg_color=ThemeManager.color["bg_light"])
        self.sf_test_in_progress_label = CTkLabel(self.sf, text="Test In Progress", text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["menu_button"], height=60, fg_color=ThemeManager.color["secondary"], corner_radius=10)
    
    def place_settings_widget(self) -> None:
        self.sf.pack(side="top", fill="x")
        self.sf_configurations_button.pack(padx=(20,10), pady=10, side="left")
        self.sf_devices_button.pack(padx=10, pady=10, side="left")
        self.sf_settings_button.pack(padx=10, pady=10, side="left")
        self.sf_clock_label.pack(padx=20, pady=10, side="right")

    def place_clock_frame(self) -> None:
        self.sf_clock_label.pack(padx=20, pady=10, side="right")
        
    def place_testing_frame(self) -> None:
        self.sf_configurations_button.pack_forget()
        self.sf_devices_button.pack_forget()
        self.sf_settings_button.pack_forget()
        if ThemeManager.enable_clock_frame: self.sf_test_in_progress_label.pack(side="left", fill="x", expand=True, padx=(20,0), pady=10)
        else: self.sf_test_in_progress_label.pack(side="left", fill="x", expand=True, padx=20, pady=10)

    def forget_clock_frame(self) -> None: 
        self.sf_clock_label.pack_forget()

    def forget_testing_frame(self) -> None:
        self.sf_test_in_progress_label.pack_forget()
        self.sf_configurations_button.pack(padx=(20,10), pady=10, side="left")
        self.sf_devices_button.pack(padx=10, pady=10, side="left")
        self.sf_settings_button.pack(padx=10, pady=10, side="left")

    def update_settings_widget(self) -> None:
        self.sf.configure(fg_color=ThemeManager.color["bg"])
        self.sf_configurations_button.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["menu_button"], border_color=ThemeManager.color["secondary"],fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"])
        self.sf_devices_button.configure(font=ThemeManager.font["menu_button"],  text_color=ThemeManager.text_color["normal"], border_color=ThemeManager.color["secondary"], fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"])
        self.sf_settings_button.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["menu_button"], border_color=ThemeManager.color["secondary"], fg_color=ThemeManager.color["bg_light"], hover_color=ThemeManager.color["secondary"])
        self.sf_clock_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["clock"], fg_color=ThemeManager.color["bg_light"])
        self.sf_test_in_progress_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["menu_button"], fg_color=ThemeManager.color["secondary"])

    def update_sf_button_states(self, state:str) -> None:
        self.sf_configurations_button.configure(state=state)
        self.sf_devices_button.configure(state=state)
        self.sf_settings_button.configure(state=state)

class TestingWidget(Base):
    def __init__(self) -> None:
        super().__init__()

    def create_testing_widget_object(self) -> None:
        self.tf = CTkFrame(self.master_frame, fg_color=ThemeManager.color["bg_light"], border_width=1, border_color=ThemeManager.color["secondary"], corner_radius=10, width=400) # tf = testing_frame
        self.tf_terminal_frame = CTkListbox(self.tf, header_text="Previous Test: None", scrollbar_fg_color=ThemeManager.color["bg_light"], scrollbar_hover_color=ThemeManager.color["secondary"], fg_color=ThemeManager.color["bg"], header_fg_color=ThemeManager.color["bg"], header_text_color=ThemeManager.text_color["normal"], item_fg_color=ThemeManager.color["bg"], item_text_color=ThemeManager.text_color["normal"], corner_radius=20, item_font=ThemeManager.font["terminal"], item_height=20, max_items=35)
        self.tf_progress_frame = CTkFrame(self.tf, corner_radius=0, fg_color=ThemeManager.color["bg_light"])
        self.tf_progressbar = CTkProgressBar(self.tf_progress_frame, height=15, fg_color=ThemeManager.color["bg"], progress_color=ThemeManager.color["bg"])
        self.tf_progress_text = CTkLabel(self.tf_progress_frame, text="0.0%", text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["test_button"])
        self.tf_detach_progressbar = CTkButton(self.tf_progress_frame, text="", image=self.detach_image, fg_color=ThemeManager.color["bg"], corner_radius=50, width=50, height=30, hover_color=ThemeManager.color["secondary"])
        self.tf_button_frame = CTkFrame(self.tf, corner_radius=0, fg_color=ThemeManager.color["bg_light"])
        self.tf_start_button = CTkButton(self.tf_button_frame, image=self.play_image, text_color=ThemeManager.text_color["normal"], text_color_disabled=ThemeManager.text_color["disabled"], text="Start Test", font=ThemeManager.font["test_button"], height=40, corner_radius=10, fg_color=ThemeManager.color["bg"], hover_color=ThemeManager.color["secondary"])
        self.tf_stop_button = CTkButton(self.tf_button_frame, image=self.stop_image, text_color=ThemeManager.text_color["normal"], text_color_disabled=ThemeManager.text_color["disabled"], text="End Test", font=ThemeManager.font["test_button"], height=40, corner_radius=10, fg_color=ThemeManager.color["bg"], hover_color=ThemeManager.color["secondary"], state="disabled")
        self.tf_progressbar.set(0)
        self.tf_terminal_frame._parent_frame._scrollbar.grid_configure(padx=3)

    def place_testing_widget(self) -> None:
        self.tf.pack(expand=True, fill="both", side="left", padx=(20,10), pady=(10,20))
        self.tf_terminal_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.tf_progress_frame.pack(fill="x", padx=10, pady=10)
        self.tf_progress_text.pack(side="left", padx=10)
        self.tf_progressbar.pack(fill="x", expand=True, side="left")
        self.tf_detach_progressbar.pack(padx=10)
        self.tf_button_frame.pack(padx=10, pady=(10,20))
        self.tf_start_button.pack(side="left")
        self.tf_stop_button.pack(side="right", padx=10)

    def update_testing_widget(self) -> None:
        self.tf.configure(fg_color=ThemeManager.color["bg_light"], border_color=ThemeManager.color["secondary"])
        self.tf_terminal_frame.configure(scrollbar_fg_color=ThemeManager.color["bg_light"], scrollbar_hover_color=ThemeManager.color["secondary"], fg_color=ThemeManager.color["bg"], header_fg_color=ThemeManager.color["bg"], header_text_color=ThemeManager.text_color["normal"], item_fg_color=ThemeManager.color["bg"], item_text_color=ThemeManager.text_color["normal"], item_font=ThemeManager.font["terminal"])
        self.tf_progress_frame.configure(fg_color=ThemeManager.color["bg_light"])
        self.tf_progressbar.configure(fg_color=ThemeManager.color["bg"], progress_color=ThemeManager.color["bg"])
        self.tf_progress_text.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["test_button"])
        self.tf_detach_progressbar.configure(image=self.detach_image, fg_color=ThemeManager.color["bg"], hover_color=ThemeManager.color["secondary"])
        self.tf_button_frame.configure(fg_color=ThemeManager.color["bg_light"])
        self.tf_start_button.configure(text_color=ThemeManager.text_color["normal"], text_color_disabled=ThemeManager.text_color["disabled"], font=ThemeManager.font["test_button"], fg_color=ThemeManager.color["bg"], hover_color=ThemeManager.color["secondary"], image=self.play_image)
        self.tf_stop_button.configure(text_color=ThemeManager.text_color["normal"], text_color_disabled=ThemeManager.text_color["disabled"], font=ThemeManager.font["test_button"], fg_color=ThemeManager.color["bg"], hover_color=ThemeManager.color["secondary"], image=self.stop_image)

    def update_progressbar(self) -> None:
        if TestParameters.enable_progressbar is False: self.tf_progress_frame.pack_forget()
        else:
            self.tf_terminal_frame.pack_forget()
            self.tf_progress_frame.pack_forget()
            self.tf_button_frame.pack_forget()
            self.tf_terminal_frame.pack(expand=True, fill="both", padx=10, pady=10)
            self.tf_progress_frame.pack(fill="x", padx=10, pady=10)
            self.tf_button_frame.pack(padx=10, pady=(10,20))
            self.tf_progressbar.configure(progress_color=ThemeManager.color["bg"])
            self.tf_progress_text.configure(text="0.0%")

class StatisticsWidget(Base):
    def __init__(self):
        super().__init__()

    def create_statistics_widget_objects(self) -> None:
        self.stf = CTkFrame(self.master_frame, fg_color=ThemeManager.color["bg_light"], border_width=1, border_color=ThemeManager.color["secondary"], corner_radius=10) # stf = statistics_frame
        self.stf_parameters_label = CTkLabel(self.stf, text="Test Parameters", text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat_title"], fg_color=ThemeManager.color["bg"], corner_radius=10, width=210)
        self.stf_test_title_label = CTkLabel(self.stf, justify="left", text="File Name: my_test", text_color=ThemeManager.text_color["normal"], wraplength=200, font=ThemeManager.font["stat"])
        self.stf_test_file_path_label = CTkLabel(self.stf, justify="left", text="File Path: default", text_color=ThemeManager.text_color["normal"], wraplength=200, font=ThemeManager.font["stat"])
        self.sft_test_file_type_label = CTkLabel(self.stf, justify="left", text="File Type: .txt", text_color=ThemeManager.text_color["normal"], wraplength=200, font=ThemeManager.font["stat"])
        self.stf_stats_label = CTkLabel(self.stf, text="Test Info", font=ThemeManager.font["stat_title"], text_color=ThemeManager.text_color["normal"], fg_color=ThemeManager.color["bg"], corner_radius=10, width=210)
        self.stf_test_time_start_label = CTkLabel(self.stf, justify="left", text="Test Start Time: None", text_color=ThemeManager.text_color["normal"], wraplength=200, font=ThemeManager.font["stat"])
        self.stf_error_readings_label = CTkLabel(self.stf, justify="left", text="Errors Read: 0", text_color=ThemeManager.text_color["normal"], wraplength=200, font=ThemeManager.font["stat"])

    def place_statistics_widget(self) -> None:
        self.stf.pack(fill="y", side="left", padx=(10,20), pady=(10,20))
        self.stf_parameters_label.pack(pady=10, padx=10)
        self.stf_test_title_label.pack(anchor="w", padx=10)
        self.stf_test_file_path_label.pack(anchor="w", padx=10)
        self.sft_test_file_type_label.pack(anchor="w", padx=10)
        self.stf_stats_label.pack(pady=10, padx=10)
        self.stf_test_time_start_label.pack(anchor="w", padx=10)
        self.stf_error_readings_label.pack(anchor="w", padx=10)

    def place_statistics_frame(self) -> None:
        self.stf.pack(fill="y", side="left", padx=(10,20), pady=(10,20))

    def forget_statistics_frame(self) -> None:
        self.stf.pack_forget()

    def update_statistics_widget(self) -> None:
        self.stf.configure(fg_color=ThemeManager.color["bg_light"], border_color=ThemeManager.color["secondary"])
        self.stf_parameters_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat_title"], fg_color=ThemeManager.color["bg"])
        self.stf_test_title_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat"])
        self.stf_test_file_path_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat"])
        self.sft_test_file_type_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat"])
        self.stf_stats_label.configure(font=ThemeManager.font["stat_title"], text_color=ThemeManager.text_color["normal"], fg_color=ThemeManager.color["bg"])
        self.stf_test_time_start_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat"])
        self.stf_error_readings_label.configure(text_color=ThemeManager.text_color["normal"], font=ThemeManager.font["stat"])

    def update_stf_test_params(self, **params) -> None:
        if "test_name" in params: self.stf_test_title_label.configure(text=f"File Name: {params.pop("test_name")}")
        if "test_location" in params: self.stf_test_file_path_label.configure(text=f"File Path: {params.pop("test_location")}")
        if "file_type" in params: self.sft_test_file_type_label.configure(text=f"File Type: {params.pop("file_type")}")

    def update_stf_test_info(self, **params) -> None:
        if "start_time" in params: self.stf_test_time_start_label.configure(text=f"Test Start Time: {params.pop("start_time")}")
        if "errors_read" in params: self.stf_error_readings_label.configure(text=f"Errors Read: {params.pop("errors_read")}")

class App(DeviceWidget, SettingsWidget, TestingWidget, StatisticsWidget):
    def __init__(self) -> None:
        super().__init__()

        self._create_all_objects()
        self._create_all_bindings()
        self._configure_necessary_objects()
        self._place_all()
        
        self._test_active: bool = False
        self._queue_test_percent: Queue = Queue()
        self._queue_data: Queue = Queue()
        self._errors_read: int = 0
        self._progressbar_detached: bool = False

    def _create_all_bindings(self) -> None:
        self.bind("<<update_progressbar>>", self._update_progressbar)
        self.bind("<<update_terminal>>", self._update_terminal)
        self.bind("<<update_stat_error>>", self._update_stat_error)

    def _create_all_objects(self) -> None:
        self.create_device_widget_objects()
        self.create_settings_widget_objects()
        self.create_testing_widget_object()
        self.create_statistics_widget_objects()   

    def _configure_necessary_objects(self):
        self.sf_configurations_button.configure(command=self._get_test_parameters)
        self.sf_devices_button.configure(command=self._get_device)
        self.sf_settings_button.configure(command=self._get_settings)
        self.tf_start_button.configure(command=self._run_test)
        self.tf_stop_button.configure(command=self._ask_to_stop)
        self.tf_detach_progressbar.configure(command=self._detach_progressbar)

    def _place_all(self) -> None:
        self.place_device_widget()
        self.place_settings_widget()
        self.place_testing_widget()
        self.place_statistics_widget()
        
    def _update_window_theme(self):
        self.update_master_frame()
        self.update_device_widget()
        self.update_settings_widget()
        self.update_testing_widget()
        self.update_statistics_widget()

    def _update_progressbar(self, event=None) -> None:
        percent = self._queue_test_percent.get()
        TestParameters.percent = percent
        self.tf_progress_text.configure(text=f"{round(percent*100,1)}%")
        self.tf_progressbar.set(round(percent,3))
        self.update()

    def _update_terminal(self, event=None) -> None:
        while self._queue_data.empty() != True:
            self.tf_terminal_frame.insert_item(self._queue_data.get_nowait())
            self.tf_terminal_frame.see()
            self.update()
        
    def _update_stat_error(self, event=None) -> None:
        self._errors_read += 1
        self.update_stf_test_info(errors_read=self._errors_read)
        self.update()

    def _get_test_parameters(self) -> None:
        self.update_sf_button_states("disabled")
        sw = SetupWindow(TestParameters.file_name, TestParameters.file_location, TestParameters.file_type, TestParameters.enable_progressbar, TestParameters.packet_count, TestParameters.packet_indicator, TestParameters.stop_value)
        sw.wait_window()
        TestParameters.configure_parameters(TestParameters, sw.get_test_parameters())
        self.update_sf_button_states("normal")

        self.update_stf_test_params(test_name=TestParameters.file_name, test_location=TestParameters.file_location, file_type=TestParameters.file_type)
        if self._progressbar_detached == True:
            TestParameters.enable_progressbar = False
        self.update_progressbar()

    def _get_device(self) -> None:
        self.update_sf_button_states("disabled")
        dw = DeviceWindow()
        dw.wait_window()
        TestParameters.device_selected = dw.get_device_selected()
        self.update_sf_button_states("normal")
        if TestParameters.device_selected != None: self.update_device_status("connected")
        else: self.update_device_status("disconnected")

    def _get_settings(self) -> None:
        self.update_sf_button_states("disabled")
        SettingsWindow().wait_window()
        self.update_sf_button_states("normal")

        if ThemeManager.enable_clock_frame == 0: 
            self.forget_clock_frame()
            self.stop_clock()
        else: 
            self.place_clock_frame()
            self.stop_clock()
            self.after(1000, self.start_clock)

        self._update_window_theme()

        if TestParameters.device_selected != None: self.update_device_status("connected")
        else: self.update_device_status("disconnected")

        if ThemeManager.enable_stat_frame == 0: 
            self.forget_statistics_frame()
            self.tf.pack_configure(padx=20)
        else: 
            self.place_statistics_frame()
            self.tf.pack_configure(padx=(20,10))

        self.tf_terminal_frame.clear()

    def _detach_progressbar(self):
        TestParameters.enable_progressbar = False
        self.update_progressbar()
        self._progressbar_detached = True
        pw = ProgressbarWindow(TestParameters)
        pw.wait_window()
        pw.stop_check()
        self._progressbar_detached = False
        TestParameters.enable_progressbar = True
        self.update_progressbar()
        self.tf_progressbar.configure(progress_color=ThemeManager.color["secondary"])

    def _check_file_path_default(self) -> None:
        if TestParameters.file_location == "default": TestParameters.file_location = __base_dir__+"\\cache"

    def _run_test(self) -> None:
        self.tf_terminal_frame.clear()
        self.tf_terminal_frame.configure(header_text=f"Running: {TestParameters.file_name}")
        self.tf_progressbar.set(0)
        self.tf_progressbar.configure(progress_color=ThemeManager.color["secondary"])
        self.tf_progress_text.configure(text="0.0%")
        self._test_active = True
        self._check_file_path_default()
        self._errors_read = 0
        self.update_stf_test_info(start_time=clk.get_computer_time(), errors_read=self._errors_read)
        self.place_testing_frame()
        self.tf_start_button.configure(state="disabled")
        self.tf_stop_button.configure(state="normal")
        TestParameters.percent = 0
        Thread(target=self._read_stream, daemon=True).start()

    def _ask_to_stop(self) -> None:
        if messagebox.askyesno("XSI - Stop Test", "Are you sure you want to stop the test?"): 
            self._stop_test()
            self.tf_terminal_frame.configure(header_text=f"Previous Test: {TestParameters.file_name}")
            messagebox.showinfo("XSI - Test Status", f"Test '{TestParameters.file_name}' has finished successfully!")

    def _stop_test(self) -> None:
        self._test_active = False
        self.tf_start_button.configure(state="normal")
        self.tf_stop_button.configure(state="disabled")
        self.forget_testing_frame()

    def _read_stream(self) -> None:
        try:
            device = Serial(TestParameters.device_selected, 9600)
            count: int = 0
            with open(TestParameters.file_location+"\\"+TestParameters.file_name+TestParameters.file_type, "w") as file: 
                file.write("!=================================!\n")
                file.write(f"Test Info:\n")
                file.write(f"file_name: {TestParameters.file_name}\n")
                if TestParameters.enable_progressbar == True or self._progressbar_detached == True: file.write(f"packet_count: {TestParameters.packet_count}\n")
                else: file.write("packet_count: None\n")
                file.write(f"verified_device: {TestParameters.device_selected}\n")
                file.write(f"time_started: {clk.get_computer_time(format=24, disable_seconds=True)}\n")
                file.write(f"date_conducted: {clk.get_computer_date()}\n")
                file.write("!=================================!\n")

            while self._test_active is not False:
                _available_ports: list = [p[0] for p in comports()]
                for port in _available_ports:
                    if port == TestParameters.device_selected: break
                
                if port != TestParameters.device_selected: raise

                count += 1

                try: 
                    data = f"{device.readline().decode().rstrip()}"
                    with open(TestParameters.file_location+"\\"+TestParameters.file_name+TestParameters.file_type, "a") as file: file.write(f"{datetime.now()},{count},{data}\n")
                except: 
                    data = "error_reading_data"
                    with open(TestParameters.file_location+"\\"+TestParameters.file_name+TestParameters.file_type, "a") as file: file.write(f"{datetime.now()},{count},{data}\n")
                    self.event_generate("<<update_stat_error>>")

                if data == TestParameters.stop_value:
                    self.tf_terminal_frame.configure(header_text=f"Previous Test: {TestParameters.file_name}")
                    messagebox.showinfo("XSI - Test Status", f"Test '{TestParameters.file_name}' has finished successfully!")
                    self._stop_test()
                    break

                if len(data) > 0:
                    if (TestParameters.enable_progressbar is not False or self._progressbar_detached is not False) and data[0] == TestParameters.packet_indicator:
                        self._queue_test_percent.put(tools.parse_packet_info(data)/TestParameters.packet_count)
                        self.event_generate("<<update_progressbar>>")

                self._queue_data.put_nowait(f" {ThemeManager.terminal_indicator} {datetime.now()},{count},{data}")
                self.event_generate("<<update_terminal>>")
                self.update()
        except:
            self.tf_terminal_frame.insert_item(f" {ThemeManager.terminal_indicator} Exception occurred!")
            self.tf_terminal_frame.insert_item(f" {ThemeManager.terminal_indicator} View Traceback for debugging info.")
            self.update()
            self.tf_terminal_frame.see()
            self._stop_test() 
            self.update_device_status("disconnected")
            self.tf_terminal_frame.configure(header_text=f"Failed Test: {TestParameters.file_name}")
            messagebox.showerror("XSI - Test Status", f"Test '{TestParameters.file_name}' finished with errors!")

if __name__ == "__main__":
    App().mainloop()