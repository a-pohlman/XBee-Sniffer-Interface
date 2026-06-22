import customtkinter as ctk
try: from tools.theme import Theme # Use the Theme class to get theme colors, font
except: from theme import Theme

#import any extra modules needed for Loop class

# Use show_options to show the CustomOptions window when starting new test
show_options: bool = True

raise_error: bool = False # DO NOT CHANGE

# Toplevel window to open to get extra options for custom test
class CustomOptions(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("XSI - Statistics for Models")
        self.geometry(f"425x450+{int(self.winfo_screenwidth()/2 - 212.5)}+{int(self.winfo_screenheight()/2.2 - 212.5)}")
        self.minsize(425,450) # Change window size here
        self.maxsize(425,450) # Change window size here
        self.items_saved: bool = False

        self.root = ctk.CTkFrame(self, corner_radius=0, fg_color=Theme.bg_color)
        self.root.pack(expand=True, fill="both")

        self.frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color=Theme.fg_color, border_color=Theme.accent, border_width=3)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.frame, text="Statistics for Models", font=(Theme.font_type,20,"bold"), text_color=Theme.text_color)
        self.title_label.grid(row=0, column=0, columnspan=10, pady=(20,0), padx=100)

        # Add customtkinter code below (use the grid method to place object down)


        # Add customtkinter code above

        self.save_button = ctk.CTkButton(self.frame, text="Save", corner_radius=10, fg_color=Theme.sfg_color, hover_color=Theme.accent_hover, text_color=Theme.text_color, font=(Theme.font_type,15,"normal"), command=self.save_values)
        self.save_button.grid(row=1, column=0, columnspan=10, pady=(30,0)) # Up row count to keep consistency with items

    # DO NOT CHANGE 
    def save_values(self): 
        self.items_saved = True
        self.destroy()

    def get_values(self):
        return [] # Get values from ctk.StringVar variables and put them into list
        # These will then be passed to the values parameter in the Loop class

# Loop class that XSI uses during the test thread
class Loop:
    def __init__(self, values:list=[], file_path:str=""):
        self.values = values
        self.file_path = file_path
        self.write_to_file: bool = False
        self.output: str = ""

    # Use the loop function to run code every time data is received. 
    # The data and packet_count parameters are automatically passed to the loop function
    def loop(self, data:str, packet_count:int):
        pass
    
    # Use this function to write data every time data is collected
    def file_output(self, data:str) -> str:
        return self.output

    # Use this function for when the test ends
    def end_file_output(self):
        pass

# Run this python file to test the toplevel window and see how it looks
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Test Frame")

    co = CustomOptions()

    root.mainloop()