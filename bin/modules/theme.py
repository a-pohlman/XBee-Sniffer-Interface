from customtkinter import CTkImage
from PIL import Image
from modules.app_tools.tools import parse_dir_path

__base_dir__ = parse_dir_path(__file__, "bin_windows")

print(__base_dir__)
class ThemeManager:
    color: dict = {
                   "bg":"#202020", 
                   "bg_light":"#2A2A2A",
                   "hover_light":"#404040", 
                   "secondary":"#FF1B67"
                  }
    
    text_color: dict = {
                        "disabled":"#505050", 
                        "normal":"#FFFFFF"
                       }
    
    font: dict = {
                  "toplevel_title":("Arial", 20, "bold"), 
                  "toplevel_option":("Arial", 16, "normal"), 
                  "device_check":("Arial", 16, "bold"), 
                  "device_button":("Arial",14,"normal"), 
                  "terminal":("Arial", 18, "normal"), 
                  "stat_title":("Arial", 17, "bold"), 
                  "stat":("Arial",15,"normal"), 
                  "test_button":("Arial", 14, "bold"),
                  "menu_button":("Arial", 18, "bold"),
                  "clock":("Arial", 18, "normal")
                 }
    
    terminal_indicator: str = ">"
    enable_stat_frame: int = 1
    enable_clock_frame: int = 1
    
    def change_theme_color(self, new_color:str) -> None:
        match new_color:
            case "Witchlight Purple": self.color.update(secondary="#9A00FF")
            case "Lily Pad Green": self.color.update(secondary="#00BF85")
            case "Moody Orange": self.color.update(secondary="#FF501B")
            case "Strawberry Red": self.color.update(secondary="#FF1B67")

    def change_mode(self, mode:int) -> None:
        match mode:
            case 1: 
                self.color.update(bg="#202020", bg_light="#2A2A2A", hover_light="#404040")
                self.text_color.update(normal="#FFFFFF", disabled="#505050")
            case 0: 
                self.color.update(bg="#FDFDFD", bg_light="#B5B5B5", hover_light="#C8C8C8")
                self.text_color.update(normal="#1F1F1F", disabled="#808080")

class IconManager:
    play_image = CTkImage(Image.open(__base_dir__+"\\icons\\play_15px_dark.png"), size=(15,15))
    stop_image = CTkImage(Image.open(__base_dir__+"\\icons\\stop_15px_dark.png"), size=(15,15))
    help_image = CTkImage(Image.open(__base_dir__+"\\icons\\help_40px_dark.png"), size=(40,40))
    info_image = CTkImage(Image.open(__base_dir__+"\\icons\\info_40px_dark.png"), size=(40,40))
    refresh_image = CTkImage(Image.open(__base_dir__+"\\icons\\refresh_30px_dark.png"), size=(30,30))
    detach_image = CTkImage(Image.open(__base_dir__+"\\icons\\detach_20px_dark.png"), size=(20,20))
    rotate_image = CTkImage(Image.open(__base_dir__+"\\icons\\rotate_20px_dark.png"), size=(20,20))
    device_disconnected = CTkImage(Image.open(__base_dir__+"\\icons\\device_disconnected_40px_dark.png"), size=(40,40))
    device_connected = CTkImage(Image.open(__base_dir__+"\\icons\\device_connected_40px_strawberry_red.png"), size=(40,40))

    def change_icon_theme(self, new_theme:str) -> None:
        match new_theme:
            case "Strawberry Red": self.device_connected = CTkImage(Image.open(__base_dir__+"\\icons\\device_connected_40px_strawberry_red.png"), size=(40,40))
            case "Lily Pad Green": self.device_connected = CTkImage(Image.open(__base_dir__+"\\icons\\device_connected_40px_lily_pad_green.png"), size=(40,40))
            case "Moody Orange": self.device_connected = CTkImage(Image.open(__base_dir__+"\\icons\\device_connected_40px_moody_orange.png"), size=(40,40))
            case "Witchlight Purple": self.device_connected = CTkImage(Image.open(__base_dir__+"\\icons\\device_connected_40px_witchlight_purple.png"), size=(40,40))

    def change_icon_mode(self, mode:int) -> None:
        match mode:
            case 0: 
                self.play_image = CTkImage(Image.open(__base_dir__+"\\icons\\play_15px_light.png"), size=(15,15))
                self.stop_image = CTkImage(Image.open(__base_dir__+"\\icons\\stop_15px_light.png"), size=(15,15))
                self.help_image = CTkImage(Image.open(__base_dir__+"\\icons\\help_40px_light.png"), size=(40,40))
                self.info_image = CTkImage(Image.open(__base_dir__+"\\icons\\info_40px_light.png"), size=(40,40))
                self.refresh_image = CTkImage(Image.open(__base_dir__+"\\icons\\refresh_30px_light.png"), size=(30,30))
                self.detach_image = CTkImage(Image.open(__base_dir__+"\\icons\\detach_20px_light.png"), size=(20,20))
                self.rotate_image = CTkImage(Image.open(__base_dir__+"\\icons\\rotate_20px_light.png"), size=(20,20))
                self.device_disconnected = CTkImage(Image.open(__base_dir__+"\\icons\\device_disconnected_40px_light.png"), size=(40,40))
            case 1: 
                self.play_image = CTkImage(Image.open(__base_dir__+"\\icons\\play_15px_dark.png"), size=(15,15))
                self.stop_image = CTkImage(Image.open(__base_dir__+"\\icons\\stop_15px_dark.png"), size=(15,15))
                self.help_image = CTkImage(Image.open(__base_dir__+"\\icons\\help_40px_dark.png"), size=(40,40))
                self.info_image = CTkImage(Image.open(__base_dir__+"\\icons\\info_40px_dark.png"), size=(40,40))
                self.refresh_image = CTkImage(Image.open(__base_dir__+"\\icons\\refresh_30px_dark.png"), size=(30,30))
                self.detach_image = CTkImage(Image.open(__base_dir__+"\\icons\\detach_20px_dark.png"), size=(20,20))
                self.rotate_image = CTkImage(Image.open(__base_dir__+"\\icons\\rotate_20px_dark.png"), size=(20,20))
                self.device_disconnected = CTkImage(Image.open(__base_dir__+"\\icons\\device_disconnected_40px_dark.png"), size=(40,40))

