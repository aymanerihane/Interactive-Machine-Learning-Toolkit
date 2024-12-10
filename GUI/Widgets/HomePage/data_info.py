
import customtkinter as ctk
from tkinter import filedialog
import shutil
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from Controller.dataPreProcecing import DataPreProcessor as PreD



class DataInfo(ctk.CTkFrame):
    def __init__(self, parent, sharedState):
        super().__init__(parent)
        self.statTestDataUpload = "disabled"
        self.sharedState = sharedState

        # Define the fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")
        self.FONT_LABEL = ctk.CTkFont(size=14)
        self.FONT_BUTTON = ctk.CTkFont(size=14)

        self.infoFrame = ctk.CTkFrame(self, fg_color=self.sharedState.SECONDARY_COLOR)
        self.infoFrame.pack(pady=10, padx=20, fill="x")
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure((0, 1), weight=1)


        ##################################
        #       First Row in Data Info
        ##################################
        self.data_info_frame1 = ctk.CTkFrame(self.infoFrame, corner_radius=10, fg_color=self.sharedState.WHITE)
        self.data_info_frame1.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")
        self.data_info_frame1.grid_rowconfigure((0, 1), weight=1)

        # Label and button for "Data Upload"
        self.label1 = ctk.CTkLabel(self.data_info_frame1, text="Data Upload", text_color=self.sharedState.TEXT_COLOR, font=self.FONT_LABEL)
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.button1 = ctk.CTkButton(
            self.data_info_frame1,
            text="Upload Data",
            command=self.upload_file,
            fg_color=self.sharedState.PRIMARY_COLOR,
            hover_color=self.sharedState.HOVER_COLOR,
            text_color=self.sharedState.WHITE,
            font=self.FONT_BUTTON
        )
        self.button1.grid(row=0, column=1, padx=10)

        # Second row inside data_info_frame1
        self.data_info_frame2 = ctk.CTkFrame(self.data_info_frame1, corner_radius=10, fg_color=self.sharedState.PRIMARY_COLOR)
        self.data_info_frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
        self.data_info_frame2.grid_columnconfigure((0, 1), weight=1)

        # "Data Info" label and button
        self.label2 = ctk.CTkLabel(self.data_info_frame2, text="Data Info", text_color=self.sharedState.WHITE, font=self.FONT_LABEL)
        self.label2.grid(row=1, column=1, padx=10, pady=10)
        self.button2 = ctk.CTkButton(
            self.data_info_frame2,
            state="disabled",
            text="Upload Test Data",
            command=self.upload_test_file,
            fg_color=self.sharedState.HOVER_COLOR,
            hover_color=self.sharedState.SECONDARY_COLOR,
            text_color=self.sharedState.WHITE,
            font=self.FONT_BUTTON
        )
        self.button2.grid(row=1, column=2, padx=10)

        # Checkbox for "Need to split?"
        self.split_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self.data_info_frame2,
            text="Need to split?",
            text_color=self.sharedState.WHITE,
            command=self.update_button_state,
            variable=self.split_var,
            font=self.FONT_LABEL
        ).grid(row=1, column=0, padx=10)

        #####################################
        #       Second Column in Data Info
        #####################################
        self.target_frame = ctk.CTkFrame(self.infoFrame, corner_radius=10, fg_color=self.sharedState.WHITE)
        self.target_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.target_frame.grid_columnconfigure((0, 1), weight=1)

        # Checkbox for "Has Target?"
        self.target_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            self.target_frame,
            text="Has Target?",
            text_color=self.sharedState.TEXT_COLOR,
            command=self.update_target,
            variable=self.target_var,
            font=self.FONT_LABEL
        ).grid(row=0, column=0, padx=10)

        # Scrollable frame for columns
        self.scrollable_frame = ctk.CTkScrollableFrame(self.target_frame, corner_radius=10, fg_color=self.sharedState.PRIMARY_COLOR)
        self.scrollable_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)

        self.label_no_file = ctk.CTkLabel(self.scrollable_frame, text="No file uploaded yet", text_color=self.sharedState.WHITE, font=self.FONT_LABEL)
        self.label_no_file.grid(row=0, column=0, padx=10, pady=10)


    def load_file(self):
        

        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir,"..", "..","..")
        self.csv_file = os.path.join(root_dir, "Data/csv_file.csv")
        try:
            self.preprocess = PreD(self.csv_file)
        except:
            print("No file has uploaded yet")
            return
        data = self.preprocess.return_original_data()
        return data

        
            

    def update_Scrollable_frame(self):
        self.file_uploaded = True
        #remove all the widgets in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        #load data
        data = self.load_file()
        columns = data.columns
        #add radio buttons for each column
        self.radio_var = ctk.StringVar()
        for i,column in enumerate(columns):
            #add a radio button 
            
            ctk.CTkRadioButton(self.scrollable_frame, 
                            text=column, text_color="white",
                            value=column,
                            command=lambda value=column: self.sharedState.set_target_column(value), 
                            variable=self.radio_var).grid(row=i, column=0, pady=(0, 10))
        
        #setting the default radio value by the last column
        self.radio_var.set(columns[-1])
        self.sharedState.set_target_column(columns[-1])




        
####################################
#         Methods Section
####################################

    def upload_test_file(self):
        self.upload_file(test=True)


    # Method to update button state
    def update_button_state(self):
        self.sharedState.set_has_split(self.split_var.get())
        
        if self.split_var.get():
            self.statTestDataUpload = "normal"
            self.button2.configure(state="normal")  # Enable button
        else:
            self.statTestDataUpload = "disabled"
            self.button2.configure(state="disabled")  # Disable button
        print(f"Button state updated to: {self.statTestDataUpload}")
        

    def update_target(self):
        self.sharedState.set_has_target(self.target_var.get())
        if self.target_var.get():
            # Enable widgets in self.scrollable_frame
            for widget in self.scrollable_frame.winfo_children():
                if isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(state="normal")
        else:
            # Disable widgets in self.scrollable_frame
            for widget in self.scrollable_frame.winfo_children():
                if isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(state="disabled")

    def upload_file(self,test=False):
        # Ask the user to select a file
        file = filedialog.askopenfilename(title="Select a File")

        if file:
            print(f"File uploaded: {file}")

            # Define the target directory (../../../data)
            target_dir = os.path.join(os.path.dirname(__file__), "../../../data")

            # Ensure the target directory exists
            os.makedirs(target_dir, exist_ok=True)

            # Get the filename from the selected file
            if test:
                filename = "test_csv_file"
            else:
                filename = "csv_file"

            # Ensure the new file has a .csv extension
            new_filename = os.path.splitext(filename)[0] + ".csv"

            # Define the full path where the file will be saved
            save_path = os.path.join(target_dir, new_filename)

            # Copy the file to the target directory with a .csv extension
            shutil.copy(file, save_path)

            print(f"File saved as: {save_path}")
            self.update_Scrollable_frame()
            if test:
                self.sharedState.set_test_file_uploaded(True)
            else:
                self.sharedState.set_file_uploaded(True)
        



