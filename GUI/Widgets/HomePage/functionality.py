import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox

class FunctionalitySection(ctk.CTkFrame):
    def __init__(self, parent, sharedState):
        super().__init__(parent)
        self.switch_page = parent.switch_page
        self.sharedState = sharedState
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../images")
        # Functionality Section
        self.function_frame = ctk.CTkFrame(self, corner_radius=10)
        self.function_frame.pack(pady=20, padx=20, fill="x")

        #devide function_frame into 3 columns
        self.function_frame.grid_columnconfigure(1, weight=1)
        self.function_frame.grid_columnconfigure(0, weight=1)
        self.function_frame.grid_columnconfigure(2, weight=1)

        # function_frame.pack(fill="both", expand=True)

        # Button with image    
        try:

            image = Image.open(os.path.join(image_path, "training_image.png"))
            self.bg_image_tr = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))
            image = Image.open(os.path.join(image_path, "visualization.png"))
            self.bg_image_visi = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 200))

            # Button with image
            # self.home_frame_button_1 = ctk.CTkButton(self.function_frame, image=self.bg_image)
             # Button with image
            self.buttonTraining = ctk.CTkButton(
                self.function_frame,
                text="",
                image=self.bg_image_tr,
                state="normal",
                command=self.visualize_data,
                height=200,  # Match the image height to the button height
                fg_color="transparent",  # Match the parent background color
            ).grid(row=0, column=0, padx=10, pady=0, sticky="ew")
            

            ctk.CTkButton(
                self.function_frame,
                text="",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=200,
                image=self.bg_image_visi,
                # compound="center",
                command=self.visualize_data,
                fg_color="transparent",  # Match the parent background color
            ).grid(row=0, column=1, padx=10, pady=0, sticky="ew")

            ctk.CTkButton(
                self.function_frame,
                text="",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=200,
                image=self.bg_image_visi,
                fg_color="transparent",
                command=self.export_result,
            ).grid(row=0, column=2, padx=10, pady=0, sticky="ew")

        except FileNotFoundError:
            print(f"Error: The image file was not found.")
            ctk.CTkButton(
            self.function_frame,
            text="Training Data",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=200,
            command=self.train_model).grid(row=0, column=0, padx=5, pady=10,sticky="ew")

            ctk.CTkButton(
                self.function_frame,
                text="Visualize Data",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=200,
                command=self.visualize_data,
            ).grid(row=0, column=1, padx=5, pady=10,sticky="ew")

            ctk.CTkButton(
                self.function_frame,
                text="Export Result",
                font=ctk.CTkFont(size=16, weight="bold"),
                height=200,
                command=self.export_result,
                state="disabled",
            ).grid(row=0, column=2, padx=5, pady=10, sticky="ew")



    def train_model(self):
        print("Train Model clicked!")
        if self.sharedState.get_file_uploaded():
            self.switch_page("Training")
        else:
            error_message = "Please upload a file first!"
            #prompt
            messagebox.showerror("Error", error_message)

    def visualize_data(self):
        print("Visualize Data clicked!")
        if self.sharedState.get_file_uploaded():
            self.switch_page("visualization")
        else:
            error_message = "Please upload a file first!"
            #prompt
            messagebox.showerror("Error", error_message)
            

    def export_result(self):
        print("Export Result clicked!")
