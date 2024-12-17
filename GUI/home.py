import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os
from Widgets.HomePage.data_info import DataInfo
from Widgets.HomePage.functionality import FunctionalitySection
from Widgets.HomePage.data_stats import DataStats

class HomePage(ctk.CTkFrame):
    def __init__(self, parent,switch_page,sharedState):
        super().__init__(parent)
        self.sharedState = sharedState

        self.statTestDataUpload = "disabled" 
        self.theme = "white"
        

        # Set CustomTkinter Theme
        ctk.set_appearance_mode(self.theme)  # Modes: "light", "dark"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", 


        self.switch_page = switch_page  # Function to switch pages





        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        
        
        ####################################
        #       Info Section
        ####################################
        self.data_info = DataInfo(self,self.sharedState,self.refresh_data_stats)
        self.data_info.pack(pady=0, padx=0, fill="x")
        
        ####################################
        #       Functionality Section
        ####################################

        # self.functionality = FunctionalitySection(self,self.sharedState)
        # self.functionality.pack(pady=0, padx=0, fill="x")


        ####################################
        #       Details Section
        ####################################
        self.data_stat = DataStats(self,self.sharedState)
        self.data_stat.pack(pady=0, padx=0, fill="x")

    def refresh_data_stats(self):
        """Refresh the DataStats widget."""
        self.data_stat.update_stats()












