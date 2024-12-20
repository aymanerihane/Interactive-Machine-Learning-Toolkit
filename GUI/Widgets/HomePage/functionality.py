import customtkinter as ctk
import os
from tkinter import messagebox
from Controller.dataPreProcecing import DataPreProcessor as PreD
from Controller.training_Process import TrainingProcess
import threading
import pandas as pd
from sklearn.metrics import classification_report

class FunctionalitySection(ctk.CTkFrame):
    def __init__(self, parent, sharedState):
        super().__init__(parent)
        self.sharedState = sharedState
        self.switch_page = parent.switch_page

        self.preprocess = PreD(sharedState=self.sharedState,just_for_method_use=True)
        self.training = TrainingProcess(sharedState=self.sharedState)

        # Define fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")
        self.FONT_LABEL = ctk.CTkFont(size=12)

        # Main info frame with border
        self.trainingFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.trainingFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.trainingFrame.configure(border_color=self.sharedState.DARK_COLOR, border_width=2)

        # Configure grid for the main frame (self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Configure grid inside trainingFrame
        self.trainingFrame.grid_rowconfigure(0, weight=1)
        self.trainingFrame.grid_columnconfigure(0, weight=1)
        self.trainingFrame.grid_columnconfigure(1, weight=1)
        self.trainingFrame.grid_columnconfigure(2, weight=1)
        self.trainingFrame.grid_rowconfigure(0, weight=1)
        self.trainingFrame.grid_rowconfigure(1, weight=1)
        

        #######################################################
        #       First Column in Data Detail (Data Stats)
        #######################################################

        # Data Training Frame
        self.TrainDataFrame = ctk.CTkFrame(self.trainingFrame, fg_color="transparent")
        self.TrainDataFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Configure grid for the data training frame
        self.TrainDataFrame.grid_rowconfigure(0, weight=1)
        self.TrainDataFrame.grid_rowconfigure(1, weight=1)
        self.TrainDataFrame.grid_rowconfigure(2, weight=1)

        # Title
        self.TrainDataTitle = ctk.CTkLabel(self.TrainDataFrame, text="Data Training", font=self.FONT_TITLE, anchor="center")
        self.TrainDataTitle.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        if self.sharedState.get_data() is not None:
            self.update_button()

        # divider
        # self.divider = ctk.CTkLabel(self.trainingFrame, text="", fg_color=self.sharedState.DARK_COLOR, width=2)
        # self.divider.grid(row=0, column=1, sticky="ns", padx=0, pady=30)  


        #######################################################
        #       Second Column in Functionality (Evaluation)
        #######################################################

        # Evaluation Frame
        self.EvaluationFrame = ctk.CTkFrame(self.trainingFrame, fg_color="transparent")
        self.EvaluationFrame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Classification Report Frame
        self.ClassificationReportFrame = ctk.CTkFrame(self.EvaluationFrame, fg_color="transparent")
        self.ClassificationReportFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Title
        self.ClassificationReportTitle = ctk.CTkLabel(self.ClassificationReportFrame, text="Classification Report", font=self.FONT_TITLE, anchor="center")
        self.ClassificationReportTitle.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        self.ClassificationReportContainer = ctk.CTkFrame(self.trainingFrame, fg_color="transparent")
        self.ClassificationReportContainer.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)

        ############################################################
        #       Second Row in Functionality (export and visiualize)
        ############################################################

        #scond row frame
        self.SecondRowFrame = ctk.CTkFrame(self.trainingFrame, fg_color="transparent")
        self.SecondRowFrame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        

    def create_classification_report_table(self):
        """
        Create a table for the classification report and display it inside the ClassificationReportFrame.
        """
        

        print("Creating classification report table...")

        # Clear existing widgets in the ClassificationReportFrame
        for widget in self.ClassificationReportFrame.winfo_children():
            widget.destroy()

        # Add title to the frame
        self.ClassificationReportTitle = ctk.CTkLabel(
            self.ClassificationReportFrame,
            text="Classification Report",
            font=self.FONT_TITLE,
            anchor="center"
        )
        self.ClassificationReportTitle.grid(row=0, column=0, columnspan=5, sticky="n", padx=10, pady=10)

        try:
            # Fetch the predictions and true labels
            y_test = self.training.get_y_test()
            y_pred = self.training.get_y_pred()

            # Validate that y_test and y_pred are not None
            if y_test is None or y_pred is None:
                raise ValueError("y_test or y_pred is not set. Ensure the model has been tested.")

            # Generate the classification report as a dictionary
            report_dict = classification_report(y_test, y_pred, output_dict=True)

            # Validate the classification report
            if not report_dict:
                raise ValueError("Classification report is empty.")

            print("Report Dict:", report_dict)

            # Convert the dictionary to a pandas DataFrame
            report_df = pd.DataFrame(report_dict).transpose()

            


            # Add table headers
            headers = ["Class"] + list(report_df.columns)
            for col_index, header in enumerate(headers):
                header_label = ctk.CTkLabel(
                    self.ClassificationReportContainer,
                    text=header,
                    font=self.FONT_LABEL,
                    width=50
                )
                header_label.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")

            # Populate the table with classification report data
            original_classes = self.sharedState.get_original_data()[self.sharedState.get_target_column()].unique()

            for row_index, (class_name, row) in enumerate(report_df.iterrows(), start=2):
                # Map the index to the original class label if possible
                original_class_name = (
                    original_classes[int(class_name)] 
                    if class_name.isdigit() and int(class_name) < len(original_classes) 
                    else class_name
                )

                # Add class name
                class_label = ctk.CTkLabel(
                    self.ClassificationReportContainer,
                    text=original_class_name,
                    font=self.FONT_LABEL
                )
                class_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")

                # Add row values
                for col_index, value in enumerate(row):
                    data_label = ctk.CTkLabel(
                        self.ClassificationReportContainer,
                        text=f"{value:.2f}" if isinstance(value, float) else str(value),
                        font=self.FONT_LABEL
                    )
                    data_label.grid(row=row_index, column=col_index + 1, padx=5, pady=5, sticky="ew")
                
            # Enable the export button
            self.ExportButton.configure(state=ctk.NORMAL)
            


        except Exception as e:
            # Display error message if an exception occurs
            error_label = ctk.CTkLabel(
                self.ClassificationReportFrame,
                text=f"Error generating report: {str(e)}",
                font=self.FONT_LABEL,
                text_color=self.sharedState.ERROR_COLOR,
            )
            error_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            print(f"Error: {str(e)}")

      
    def create_training_buttons(self):
        """
        Create a scrollable frame with buttons for training steps.
        Dynamically enable or disable buttons based on conditions.
        Disable buttons after they are clicked, and re-enable all after Reset.

        """
        #remove divider
        # self.divider.destroy()
        
        #remove all the widgets in the scrollable frame
        for widget in self.TrainDataFrame.winfo_children():
            widget.destroy()

        #create Training Title
        self.TrainDataTitle = ctk.CTkLabel(self.TrainDataFrame, text="Data Training", font=self.FONT_TITLE, anchor="center")
        self.TrainDataTitle.grid(row=0, column=0, sticky="n", padx=10, pady=10)


        #progress bar
        self.progressBar = ctk.CTkProgressBar(self.TrainDataFrame,mode = "indeterminate", indeterminate_speed=5,width=400)
        self.progressBar.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        #scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.trainingFrame, width=200, height=200)
        scroll_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Button names and associated training conditions
        button_names = [
            "Random Forest",
            "Decision Tree",
            "Logistic Regression",
            "KNN",
            "SVM",
            "Naive Bayes",
            "XGBoost",
            "lightgbm",
            "clustering",
            "Linear Regression",
            "SVR",
            "Auto Model Selection",
            "Reset",
        ]

        # Enable/disable conditions for each step
        _, _,_,_,task = self.sharedState.get_data_info()
        preprocess_done = self.sharedState.get_process_done()
        print("Preprocess done: ", preprocess_done)
        print("Task: ", task)
        enable_conditions = {
            "Random Forest": task == "classification" ,
            "Decision Tree": task == "classification" ,
            "Logistic Regression": task == "classification",
            "KNN": task == "classification" ,
            "SVM": task == "classification" ,
            "Naive Bayes": task == "classification",
            "XGBoost": task == "classification" ,
            "lightgbm": task == "classification" ,
            "clustering": task == "clustering" ,
            "Linear Regression": task == "regression",
            "SVR": task == "regression",
            "Auto Model Selection": True,
            "Reset": True,
        }

        # Store references to buttons for enabling/disabling
        self.buttons = {}

        def on_button_click(name):
            """Handle button click and manage the progress bar."""
            def train_model():
                """Run the model training in a separate thread."""
                try:
                    # Start the progress bar
                    self.progressBar.start()

                    # Perform the training action
                    probleme = self.training.train_model(name)
                    self.training.predict()

                    # Stop the progress bar after training
                    self.progressBar.stop()
                    self.create_classification_report_table()

                except Exception as e:
                    # Stop the progress bar in case of an error
                    self.progressBar.stop()
                    messagebox.showerror("Error", f"An error occurred during training: {str(e)}")
                    # Re-enable the button if training is not successful
                    if probleme:
                        self.buttons[name].configure(state=ctk.NORMAL)

            if name == "Reset":
                # Reset all buttons to their initial enabled/disabled state
                for btn_name, btn in self.buttons.items():
                    btn.configure(state=ctk.NORMAL if enable_conditions.get(btn_name, False) else ctk.DISABLED)
            else:
                # Permanently disable the clicked button
                self.buttons[name].configure(state=ctk.DISABLED)

                # Start a new thread for model training
                training_thread = threading.Thread(target=train_model)
                training_thread.start()

        
        # Create buttons dynamically
        j = 0
        for i, name in enumerate(button_names):
            # Determine if the button should be enabled
            is_enabled = enable_conditions.get(name, False)

            # Create button
            button = ctk.CTkButton(
                scroll_frame,
                text=name,
                command=lambda n=name: on_button_click(n),
                state=ctk.NORMAL if is_enabled else ctk.DISABLED,  # Set state based on condition
            )
            if i % 3 == 0:
                j += 1
            button.grid(row=j, column=i%3, padx=5, pady=5, sticky="ew")

            # Store button reference
            self.buttons[name] = button

        #recreate divider
        self.divider = ctk.CTkLabel(self.trainingFrame, text="", fg_color=self.sharedState.DARK_COLOR, width=2)
        self.divider.grid(row=0, column=1, sticky="ns", padx=0, pady=30, rowspan=3)


        #Visualization Button
        ##title 
        self.visualizeTitle = ctk.CTkLabel(self.SecondRowFrame, text="Visualization", font=self.FONT_TITLE, anchor="center")
        self.visualizeTitle.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        ##button
        self.VisualizeButton = ctk.CTkButton(self.SecondRowFrame, text="Visualize Data", command=self.visualize_data)
        self.VisualizeButton.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Export Button
        ##title
        self.exportTitle = ctk.CTkLabel(self.SecondRowFrame, text="Export", font=self.FONT_TITLE, anchor="center")
        self.exportTitle.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        ##button
        self.ExportButton = ctk.CTkButton(self.SecondRowFrame, text="Export Result", command=self.export_Result, state = ctk.DISABLED)
        self.ExportButton.grid(row=0, column=3, padx=5, pady=5, sticky="ew")



    def update_button(self):
        #remove all the widgets in the scrollable frame
        for widget in self.TrainDataFrame.winfo_children():
            widget.destroy()
        # Clear existing widgets in the ClassificationReportFrame
        for widget in self.ClassificationReportFrame.winfo_children():
            widget.destroy()
        if self.ClassificationReportContainer:
            for widget in self.ClassificationReportContainer.winfo_children():
                widget.destroy()

        self.create_training_buttons()
        
        
     
    def visualize_data(self):
        print("Visualize Data clicked!")
        if self.sharedState.get_file_uploaded():
            self.switch_page("visualization")
        else:
            error_message = "Please upload a file first!"
            #prompt
            messagebox.showerror("Error", error_message)
    
    def export_Result(self):
        """
        Export the classification report to a CSV file.
        """
        try:
            # Fetch the predictions and true labels
            y_test = self.training.get_y_test()
            y_pred = self.training.get_y_pred()

            # Validate that y_test and y_pred are not None
            if y_test is None or y_pred is None:
                raise ValueError("y_test or y_pred is not set. Ensure the model has been tested.")

            # Generate the classification report as a dictionary
            report_dict = classification_report(y_test, y_pred, output_dict=True)

            # Convert the dictionary to a pandas DataFrame
            report_df = pd.DataFrame(report_dict).transpose()

            # Define the file path for the CSV file
            file_path = os.path.join(os.getcwd(), "classification_report.csv")

            # Export the DataFrame to a CSV file
            report_df.to_csv(file_path, index=True)

            # Show a success message
            messagebox.showinfo("Export Successful", f"Classification report exported to {file_path}")

        except Exception as e:
            # Display error message if an exception occurs
            messagebox.showerror("Error", f"An error occurred while exporting the report: {str(e)}")