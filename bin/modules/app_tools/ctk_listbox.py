__version__ = "0.1.6"

from customtkinter import CTk, CTkScrollableFrame, CTkLabel, CTkButton
from typing import Any, Tuple, List
from tkinter import Listbox

class CTkListbox:
    def __init__(self, 
                 master,
                 width:int=200,
                 height:int=200,
                 header_text:str="CTkListbox",
                 header_text_color:str="white",
                 header_font:Tuple[str,int,str]=("Arial", 20, "bold"),
                 header_fg_color:str="#202020",
                 fg_color:str="#202020",
                 border_color:str|None=None,
                 border_width:int=0,
                 scrollbar_fg_color:str|None=None,
                 scrollbar_hover_color:str|None=None,
                 corner_radius:int=0,
                 item_fg_color:str="#202020",
                 item_text_color:str="white",
                 item_font:Tuple[str,int,str]=("Arial",10,"normal"),
                 item_anchor:str="w",
                 item_wraplength:int=0,
                 item_height:int=24,
                 max_items:int|None=None) -> None:
        self._master = master

        self._width = width
        self._height = height
        self._header_text = header_text
        self._header_text_color = header_text_color
        self._header_font = header_font
        self._header_fg_color = header_fg_color
        self._fg_color = fg_color
        self._border_color = border_color
        self._border_width = border_width
        self._scrollbar_color = scrollbar_fg_color
        self._scrollbar_hover_color = scrollbar_hover_color
        self._corner_radius = corner_radius
        self._item_fg_color = item_fg_color
        self._item_text_color = item_text_color
        self._item_font = item_font
        self._item_anchor = item_anchor
        self._item_wraplength = item_wraplength
        self._item_height = item_height
        self._max_items = max_items
        
        self._create_listbox()

        self._index: List = []

    def _create_listbox(self) -> None:
        self._parent_frame = CTkScrollableFrame(self._master, 
                                                width=self._width, 
                                                height=self._height, 
                                                label_text=self._header_text, 
                                                label_text_color=self._header_text_color, 
                                                label_font=self._header_font, 
                                                label_fg_color=self._header_fg_color, 
                                                fg_color=self._fg_color, 
                                                corner_radius=self._corner_radius, 
                                                border_width=self._border_width)
        
        if self._border_width > 0 and self._border_color:
            self._parent_frame.configure(border_color=self._border_color)

        if self._scrollbar_color != None: self._parent_frame.configure(scrollbar_button_color=self._scrollbar_color)
        if self._scrollbar_hover_color != None: self._parent_frame.configure(scrollbar_button_hover_color=self._scrollbar_hover_color)

    def insert_item(self, text:str="") -> None:
        """ Inserts a item (text) into listbox """
        if len(self._index) == self._max_items:
           self._index[0].pack_forget()
           self._index[0].destroy()
           del self._index[0]
        _label = CTkLabel(self._parent_frame, height=self._item_height, anchor=self._item_anchor, text=text, text_color=self._item_text_color, fg_color=self._item_fg_color, font=self._item_font, wraplength=self._item_wraplength) 

        _label.pack(fill="x")
        self._index.append(_label)

    def insert_ctkobject(self, ctkobject, **pack_params) -> None:
        """ Inserts an available ctk widget into listbox [NOTE: In order to put ctk items into listbox, use cget to get the parent frame for the master parameter] """
        if self._index.__len__() == self._max_items:
            self._index[0].pack_forget()
            self._index[0].destroy()
            del self._index[0]
        ctkobject.pack(**pack_params)
        self._index.append(ctkobject)

    def see(self, to:str|float="end") -> None:
        """ Scrolls to a fractional part of the listbox """
        if to == "end": self._parent_frame._parent_canvas.yview_moveto(1)
        elif to <= 1 and to >= 0: self._parent_frame._parent_canvas.yview_moveto(to)
    
    def clear(self) -> None:
        """ Deletes all items from listbox index """
        try: 
            for item in self._index: 
                item.pack_forget()
                item.destroy()
            self._index.clear()
        except: pass

    def delete(self, index:tuple=(0,5)) -> None:
        """ Deletes a select amount of items from the current listbox index """
        for i in range(index[0], index[1]): self._index.pop(i)

    def configure(self, **kwargs) -> None:
        """ Configures various aspects about widget """
        if "width" in kwargs: self._width = kwargs.pop("width")
        if "height" in kwargs: self._height = kwargs.pop("height")
        if "header_text" in kwargs: self._header_text = kwargs.pop("header_text")
        if "header_text_color" in kwargs: self._header_text_color = kwargs.pop("header_text_color")
        if "header_font" in kwargs: self._header_font = kwargs.pop("header_font")
        if "header_fg_color" in kwargs: self._header_fg_color = kwargs.pop("header_fg_color")
        if "fg_color" in kwargs: self._fg_color = kwargs.pop("fg_color")
        if "border_color" in kwargs: self._fg_color = kwargs.pop("border_color")
        if "border_width" in kwargs: self._border_width = kwargs.pop("border_width")
        if "scrollbar_fg_color" in kwargs: self._scrollbar_color = kwargs.pop("scrollbar_fg_color")
        if "scrollbar_hover_color" in kwargs: self._scrollbar_hover_color = kwargs.pop("scrollbar_hover_color")
        if "corner_radius" in kwargs: self._corner_radius in kwargs.pop("corner_radius")
        if "item_fg_color" in kwargs: self._item_fg_color = kwargs.pop("item_fg_color")
        if "item_text_color" in kwargs: self._item_text_color = kwargs.pop("item_text_color")
        if "item_font" in kwargs: self._item_font = kwargs.pop("item_font")
        if "item_anchor" in kwargs: self._item_anchor = kwargs.pop("item_anchor")
        if "max_items" in kwargs: self._max_items = kwargs.pop("max_items")
        
        self._update_widget()

    def cget(self, attribute_name:str) -> Any:
        """ Returns a specified attribute (including parent_frame) """
        if attribute_name == "parent_frame": return self._parent_frame
        elif attribute_name == "width": return self._width
        elif attribute_name == "height": return self._height
        elif attribute_name == "header_text": return self._header_text
        elif attribute_name == "header_text_color": return self._header_text_color
        elif attribute_name == "header_font": return self._header_font
        elif attribute_name == "header_fg_color": return self._header_fg_color
        elif attribute_name == "fg_color": return self._fg_color
        elif attribute_name == "border_color": return self._border_color
        elif attribute_name == "border_width": return self._border_width
        elif attribute_name == "scrollbar_fg_color": return self._scrollbar_color
        elif attribute_name == "scrollbar_hover_color": return self._scrollbar_hover_color
        elif attribute_name == "corner_radius": return self._corner_radius
        elif attribute_name == "item_fg_color": return self._item_fg_color
        elif attribute_name == "item_text_color": return self._item_text_color
        elif attribute_name == "item_font": return self._item_font
        elif attribute_name == "item_anchor": return self._item_anchor
        elif attribute_name == "max_items": return self._max_items 

    def place(self, **kwargs) -> None:
        """
        Place a widget in the parent widget. Use as options:
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0 relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0 relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        bordermode="inside" or "outside" - whether to take border width of master widget into account
        """
        self._parent_frame.place(**kwargs)

    def place_forget(self) -> None:
        """ Unmap this widget. """
        self._parent_frame.place_forget()

    def pack(self, **kwargs) -> None:
        """
        Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        self._parent_frame.pack(**kwargs)

    def pack_forget(self) -> None:
        """ Unmap this widget. """
        self._parent_frame.pack_forget()

    def grid(self, **kwargs) -> None:
        """
        Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this widget stick to the cell boundary
        """
        self._parent_frame.grid(**kwargs)

    def grid_forget(self) -> None:
        """ Unmap this widget. """
        self._parent_frame.grid_forget()

    def _update_widget(self):
        self._parent_frame.configure(width=self._width, 
                                     height=self._height,
                                     label_text=self._header_text, 
                                     label_text_color=self._header_text_color, 
                                     label_font=self._header_font, 
                                     label_fg_color=self._header_fg_color, 
                                     fg_color=self._fg_color, 
                                     border_width=self._border_width)
        if self._border_width > 0 and self._border_color:
            self._parent_frame.configure(border_color=self._border_color)

        if self._scrollbar_color != None: self._parent_frame.configure(scrollbar_button_color=self._scrollbar_color)
        if self._scrollbar_hover_color != None: self._parent_frame.configure(scrollbar_button_hover_color=self._scrollbar_hover_color)

# Demonstration
if __name__ == "__main__":
    count: int = 0
    root = CTk()
    root.geometry(f"500x500+{int(root.winfo_screenwidth()/2 - 250)}+{int(root.winfo_screenheight()/2.2 - 250)}")
    root.title("CTklistbox")

    listbox = CTkListbox(root, header_text="Running: None", item_font=("Arial",20,"normal"), corner_radius=20, max_items=50)
    listbox.pack(expand=True, fill="y", pady=100, padx=60)

    def add_item(event=None):
        global count
        count += 1
        listbox.insert_item(f"Current count is: {count}")
        listbox.see()
        listbox.configure(header_text=count)

    def add_entry(event=None):
        listbox.insert_ctkobject(CTkButton(listbox.cget("parent_frame")))
        listbox.see()

    root.bind("<Return>", add_item)
    root.bind("<q>", add_entry)

    root.mainloop()