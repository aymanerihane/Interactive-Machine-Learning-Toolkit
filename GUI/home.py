import customtkinter as ctk
from tkinter import Scrollbar
import os
from PIL import Image
from Widgets.HomePage.data_info import DataInfo
from Widgets.HomePage.functionality import FunctionalitySection
from Widgets.HomePage.data_stats import DataStats
import customtkinter as ctk
from tkinter import Scrollbar
from functools import partial

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, switch_page, sharedState):
        super().__init__(parent)

        # Shared state and theme initialization
        self.sharedState = sharedState
        self.switch_page = switch_page  # Function to switch between pages

        self.statTestDataUpload = "disabled"
        self.theme = "white"
        
        # Set CustomTkinter Theme
        ctk.set_appearance_mode(self.theme)  # Modes: "light", "dark"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green"

        # Image directory path
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        # Create a transparent scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")  # Create a scrollable frame with a transparent background
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)  # Add padding and expand it to fill space


        # Info Section
        self.data_info = DataInfo(self, self.sharedState, self.refresh_data_stats)
        self.data_info.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        # Details Section (Data Statistics)
        self.data_stats = DataStats(self, self.sharedState,self.data_info.get_pre_process)
        self.data_stats.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        # Functionality Section
        self.functionality = FunctionalitySection(self, self.sharedState)
        self.functionality.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        # Bind mouse wheel event to scrollable frame
        self.bind_mousewheel(self.scrollable_frame)

    def bind_mousewheel(self, widget):
        """Bind mouse wheel scrolling to the given widget."""
        widget.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(widget, event))  # Windows/Unix
        widget.bind_all("<Button-4>", lambda event: self.on_mousewheel(widget, event))   # macOS/Linux (scroll up)
        widget.bind_all("<Button-5>", lambda event: self.on_mousewheel(widget, event))   # macOS/Linux (scroll down)

    def on_mousewheel(self, widget, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:  # Scroll up
            widget.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            widget.yview_scroll(1, "units")

    def refresh_data_stats(self):
        """Refresh the DataStats widget."""
        if hasattr(self.data_stats, 'update_stats'):
            self.data_stats.update_stats()
        else:
            print("Error: The DataStats widget does not have an 'update_stats' method.")
