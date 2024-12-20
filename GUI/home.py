import customtkinter as ctk
from tkinter import Scrollbar
import os
from PIL import Image
from Widgets.HomePage.data_info import DataInfo
from Widgets.HomePage.functionality import FunctionalitySection
from Widgets.HomePage.data_stats import DataStats
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

        # Configure grid layout to make the scrollable frame take all available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a transparent scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")  # Create a scrollable frame with a transparent background
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Info Section
        self.data_info = DataInfo(self, self.sharedState, self.refresh_data_stats)
        self.data_info.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        # Details Section (Data Statistics)
        self.data_stats = DataStats(self, self.sharedState,self.refresh_data_training_button)
        self.data_stats.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        # Functionality Section
        self.functionality = FunctionalitySection(self, self.sharedState)
        self.functionality.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

    def refresh_data_stats(self):
        """Refresh the DataStats widget."""
        if hasattr(self.data_stats, 'update_stats'):
            self.data_stats.update_stats(first=True)
        else:
            print("Error: The DataStats widget does not have an 'update_stats' method.")
    
    def refresh_data_training_button(self):
        """Refresh the DataStats widget."""
        if hasattr(self.functionality, 'update_button'):
            self.functionality.update_button()
        else:
            print("Error: The Fonctionality widget does not have an 'update_button' method.")
    