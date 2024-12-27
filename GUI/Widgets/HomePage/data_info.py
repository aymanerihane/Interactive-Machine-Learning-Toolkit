
import customtkinter as ctk
from tkinter import filedialog
import shutil
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from Controller.dataPreProcecing import DataPreProcessor as PreD
import pandas as pd
from tkinter import messagebox
import platform


class DataInfo(ctk.CTkFrame):
    def __init__(self, parent, sharedState, refresh_data_stats,refresh_data_training_button,update_predection,sharedState_seter = None):
        super().__init__(parent)
        self.sharedState_setter = sharedState_seter
        self.update_predection = update_predection
        self.sharedState = sharedState
        self.refresh_data_training_button = refresh_data_training_button
        self.statTestDataUpload = "disabled"
        self.switch_page = parent.switch_page
        self.refresh_data_stats = refresh_data_stats
        # Define the fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")
        self.FONT_LABEL = ctk.CTkFont(size=14)
        self.FONT_BUTTON = ctk.CTkFont(size=14)

        self.infoFrame = ctk.CTkFrame(self, fg_color=self.sharedState.SECONDARY_COLOR)
        self.infoFrame.pack(pady=10, padx=20, fill="x")
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_rowconfigure(1, weight=1)
        self.infoFrame.grid_columnconfigure((0, 1), weight=1)


        ##################################
        #       First Row in Data Info
        ##################################
        self.data_info_frame1 = ctk.CTkFrame(self.infoFrame, corner_radius=10, fg_color=self.sharedState.WHITE)
        self.data_info_frame1.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")
        self.data_info_frame1.grid_columnconfigure(1, weight=2)
        self.data_info_frame1.grid_rowconfigure((0, 1), weight=1)

        # Label and button for "Data Upload"
        self.label1 = ctk.CTkLabel(self.data_info_frame1, text="Upload Data :", text_color=self.sharedState.TEXT_COLOR, font=self.FONT_LABEL)
        self.label1.grid(row=0, column=0, padx=0, pady=10)

        self.buttonUploadFrame = ctk.CTkFrame(self.data_info_frame1, corner_radius=10, fg_color="transparent")
        self.buttonUploadFrame.grid(row=0, column=1, padx=0)
        self.button1 = ctk.CTkButton(
            self.buttonUploadFrame,
            text="Upload Data",
            command=self.upload_file,
            fg_color=self.sharedState.PRIMARY_COLOR,
            hover_color=self.sharedState.HOVER_COLOR,
            text_color=self.sharedState.WHITE,
            font=self.FONT_BUTTON
        )
        self.button1.grid(row=0, column=0, padx=10)
        self.button2 = ctk.CTkButton(
            self.buttonUploadFrame,
            text="Upload Model",
            command=self.upload_file_model,
            fg_color=self.sharedState.PRIMARY_COLOR,
            hover_color=self.sharedState.HOVER_COLOR,
            text_color=self.sharedState.WHITE,
            font=self.FONT_BUTTON
        )
        self.button2.grid(row=1, column=0, padx=10)



        # Second row inside data_info_frame1
        self.data_info_frame2 = ctk.CTkFrame(self.data_info_frame1, corner_radius=10, fg_color=self.sharedState.PRIMARY_COLOR)
        self.data_info_frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
        self.data_info_frame2.grid_columnconfigure((0, 1), weight=1)

        # "Data Info" label and button
        self.label2 = ctk.CTkLabel(self.data_info_frame2, text="Upload Test Data :", text_color=self.sharedState.WHITE, font=self.FONT_LABEL)
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
            text="Test File ?",
            text_color=self.sharedState.WHITE,
            command=self.update_button_state,
            variable=self.split_var,
            font=self.FONT_LABEL
        ).grid(row=1, column=0, padx=10)

        #button for download documentation
        self.documentation_frame = ctk.CTkFrame(self.data_info_frame1, corner_radius=10, fg_color="transparent")
        self.documentation_frame.grid(row=1, column=1, padx=0)

        self.documentation_frame.grid_rowconfigure(0, weight=1)
        self.documentation_frame.grid_rowconfigure(1, weight=1)


        self.view_documentation = ctk.CTkButton(self.documentation_frame, text="View\nDocumentation", command=lambda: self.switch_page("documentation"))
        self.view_documentation.grid(row=0, column=0, padx=0)

        self.downloadButton = ctk.CTkButton(self.documentation_frame, text="Download\nDocumentation", command=self.download_documentation)
        self.downloadButton.grid(row=1, column=0, padx=0,pady=5)


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
        

        
    def upload_file_model(self):
        """
        Upload a model file and update the shared state.
        """
        # Ask the user to select a file
        file = filedialog.askopenfilename(title="Select a File")

        if file:
            print(f"File uploaded: {file}")

            # Load the shared state using the setter
            try:
                self.sharedState_setter()
                # Update the label to indicate success
                self.label1.configure(text="Model uploaded successfully", text_color="green")

                # Trigger any additional updates (e.g., predictions)
                self.update_predection()
            except Exception as e:
                print(f"Error while processing the uploaded file: {e}")
                self.label1.configure(text="Failed to upload the model", text_color="red")
        else:
            print("No file selected.")
            self.label1.configure(text="No file selected", text_color="red")


    def download_documentation(self):
        print("Download Documentation clicked!")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..", "..", "..")
        documentation_file = os.path.join(root_dir, "documentation", "documentation.pdf")
        
        # Check if the file exists
        if os.path.exists(documentation_file):
            # Open the documentation based on the OS
            if platform.system() == "Darwin":  # macOS
                os.system(f"open \"{documentation_file}\"")
            elif platform.system() == "Windows":  # Windows
                os.system(f"start \"\" \"{documentation_file}\"")
            else:  # Linux or other systems
                os.system(f"xdg-open \"{documentation_file}\"")
        else:
            print("Documentation file not found.")


    def visualize_data(self):
        print("Visualize Data clicked!")
        if self.sharedState.get_file_uploaded():
            self.switch_page("visualization")
        else:
            error_message = "Please upload a file first!"
            #prompt
            messagebox.showerror("Error", error_message)


    def load_file(self):
        

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.join(current_dir,"..", "..","..")
            self.csv_file = os.path.join(root_dir, "data/csv_file.csv")
            
            
        except Exception as e:
            print(f"the file <{self.csv_file} > can't be loaded")
            raise e
            # return
        data = pd.read_csv(self.csv_file)

        self.label1.configure(text="Data uploaded successfully", text_color="green")
        #make the has taget checkbox active
        self.target_var.set(True)
        self.sharedState.set_has_target(True)
        self.refresh_data_training_button()
        
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
        i = 0
        for column in columns:
            #add a radio button 
            
            ctk.CTkRadioButton(self.scrollable_frame, 
                                        text=f"{column}", text_color="white",
                                        value=column,
                                        command=lambda value=column : self.sharedState.set_target_column(value),  # Set the target column and the index
                                        variable=self.radio_var).grid(row=i, column=0, pady=(0, 10))
            i += 1
        
        #setting the default radio value by the last column
        self.radio_var.set(columns[-1])
        self.sharedState.set_target_column(columns[-1])

        ##title 
        self.visualizeTitle = ctk.CTkLabel(self.infoFrame, text="Visualization:", font=self.FONT_TITLE, anchor="center")
        self.visualizeTitle.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ##button
        self.VisualizeButton = ctk.CTkButton(self.infoFrame, text="Visualize Data", command=self.visualize_data)
        self.VisualizeButton.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



        
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
        
        if self.target_var.get():
            # Enable widgets in self.scrollable_frame
            for widget in self.scrollable_frame.winfo_children():
                if isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(state="normal")
            self.sharedState.set_has_target(True)
        else:
            # Disable widgets in self.scrollable_frame
            for widget in self.scrollable_frame.winfo_children():
                if isinstance(widget, ctk.CTkRadioButton):
                    widget.configure(state="disabled")
            self.sharedState.set_has_target(False)
        self.refresh_data_training_button()

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

            

            

            # Destroy any existing PreD instance
            if not test:
                # Set the file path
                self.preprocess = PreD(file_path = save_path,sharedState=self.sharedState)
                data = pd.read_csv(save_path)
                print(data)
                self.sharedState.set_original_data(data)
                self.sharedState.set_original_columns(data.columns)
                self.sharedState.set_data(data,first=True)
                self.preprocess.set_data_stats(self.refresh_data_stats,first = True)
                self.sharedState.set_file_path(save_path)
            else:
                data = pd.read_csv(save_path)
                self.label2.configure(text="uploaded successfully", text_color="green")
                self.sharedState.set_test_data(data)

            self.update_Scrollable_frame()
            if test:
                self.sharedState.set_test_file_uploaded(True)

            else:
                self.sharedState.set_file_uploaded(True)
    
          

            





