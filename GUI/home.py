import customtkinter as ctk
import os
from Widgets.HomePage.data_info import DataInfo
from Widgets.HomePage.functionality import FunctionalitySection
from Widgets.HomePage.data_stats import DataStats
from Widgets.HomePage.prediction import PredictionSection

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, switch_page, sharedState,sharedState_seter=None):
        super().__init__(parent)

        # Shared state and theme initialization
        self.sharedState = sharedState
        self.sharedState_seter = sharedState_seter
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

        # Initialize attributes
        self.data_stats = None
        self.functionality = None

        # Info Section
        self.data_info = DataInfo(self, self.sharedState, self.refresh_data_stats,self.refresh_data_training_button,self.update_predection,sharedState_seter=self.sharedState_seter)
        self.data_info.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        # Functionality Section
        self.functionality = FunctionalitySection(self, self.sharedState,sharedState_setter=self.sharedState_seter,create_prediction_widget=self.create_prediction_widget)

        # self.prediction =None

        # Prediction Section
        self.prediction = PredictionSection(self, self.sharedState,sharedState_setter=self.sharedState_seter)  

              

        
    def create_data_stats_section(self):
        if self.data_stats :
            self.data_stats.destroy()
        # Details Section (Data Statistics)
        self.data_stats = DataStats(self, self.sharedState,self.refresh_data_training_button)
        self.data_stats.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)

        self.functionality.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)
        


    def refresh_data_stats(self,first=False):
        """Refresh the DataStats widget."""
        if first:
            self.create_data_stats_section()
        
        if hasattr(self.data_stats, 'update_stats'):
            self.data_stats.update_stats(first=True)
        else:
            print("Error: The DataStats widget does not have an 'update_stats' method.")
    
    def refresh_data_training_button(self,first=False):
        """Refresh the DataStats widget."""
        if hasattr(self.functionality, 'update_button'):
            self.functionality.update_button()
        else:
            print("Error: The Fonctionality widget does not have an 'update_button' method.")

    def create_prediction_widget(self):
        
        self.prediction.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)   
        self.prediction.create_prediction_widget()

    def update_predection(self):
        if self.prediction is None:
            self.prediction = PredictionSection(self, self.sharedState,sharedState_setter=self.sharedState_seter,)  
            self.prediction.pack(pady=0, padx=0, fill="x", in_=self.scrollable_frame)   
            self.prediction.create_prediction_widget(is_model=True)
        self.prediction.update_prediction_widget()
    