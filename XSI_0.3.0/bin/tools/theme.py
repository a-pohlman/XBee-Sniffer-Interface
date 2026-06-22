from customtkinter import CTkImage
from PIL import Image

try: from tools.__init__ import __icon_dir__
except: from __init__ import __icon_dir__

class Theme:
    bg_color: str = "#101010"
    fg_color: str = "#1C1C1C"
    sfg_color: str = "#2A2A2A"
    text_color: str = "#F1F1F1"
    accent: str = "#58DBA5"
    accent_hover: str = "#207954"
    text_color: str = "white"
    disabled_text_color: str = "#5E5E5E"
    font_type: str = "Arial"
    detail_indicator: str = ">>"
    theme_name_selected: str = "XSI Green"

    theme_names: list = ["XSI Green", "Witchlight Purple", "Strawberry Red", "Traffic Cone Orange", "Navy Blue", "Boring Grey"]
    detail_indicators: list = [">>", ">", "::", "#", "$", "&"]

    themes: dict = {"XSI Green":"#58DBA5", "Witchlight Purple":"#8E15FF", "Strawberry Red":"#F5203D", "Traffic Cone Orange":"#FD8310", "Navy Blue":"#0C10F7", "Boring Grey":"#CCCCCC"}
    theme_accents: dict = {"XSI Green":"#207954", "Witchlight Purple":"#4C1D79", "Strawberry Red":"#661822", "Traffic Cone Orange":"#704923", "Navy Blue":"#212275", "Boring Grey":"#888888"}
    theme_fonts: list = ["Arial","Palatino", "Trebuchet MS", "Tahoma"]

    def change_theme(theme_name:str, font_name:str):
        Theme.accent = Theme.themes[theme_name]
        Theme.accent_hover = Theme.theme_accents[theme_name]
        Theme.font_type = font_name
        Theme.theme_name_selected = theme_name

class Icons:
    test_image = CTkImage(Image.open(__icon_dir__+"test.png"), size=(40,40))
    start_image = CTkImage(Image.open(__icon_dir__+"start.png"), size=(40,40))
    stop_image = CTkImage(Image.open(__icon_dir__+"stop.png"), size=(40,40))
    device_image = CTkImage(Image.open(__icon_dir__+"device.png"), size=(40,40))
    view_more_image = CTkImage(Image.open(__icon_dir__+"view_more.png"), size=(30,30))
    view_less_image = CTkImage(Image.open(__icon_dir__+"view_less.png"), size=(30,30))
    info_image = CTkImage(Image.open(__icon_dir__+"info.png"), size=(40,40))
    help_image = CTkImage(Image.open(__icon_dir__+"help.png"), size=(40,40))
    settings_image = CTkImage(Image.open(__icon_dir__+"settings.png"), size=(40,40))
    disabled_test_image = CTkImage(Image.open(__icon_dir__+"disabled_test.png"), size=(40,40))
    disabled_device_image = CTkImage(Image.open(__icon_dir__+"disabled_device.png"), size=(40,40))