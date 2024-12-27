import customtkinter as ctk
import os
from tkinter import messagebox
from Controller.dataPreProcecing import DataPreProcessor as PreD
from Controller.training_Process import TrainingProcess
import threading
import pandas as pd
from sklearn.metrics import classification_report

class PredictionSection(ctk.CTkFrame):
    def __init__(self, parent, sharedState,sharedState_setter=None):
        super().__init__(parent)
        self.sharedState = sharedState
        self.switch_page = parent.switch_page
        self.sharedState_setter = sharedState_setter


        self.preprocess = PreD(sharedState=self.sharedState,just_for_method_use=True)
        self.training = TrainingProcess(sharedState=self.sharedState)

        # Define fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")
        self.FONT_LABEL = ctk.CTkFont(size=12)

        #new frame with border in self for prediction new data
        self.PredictionFrame1 = ctk.CTkFrame(self, fg_color="transparent", border_color=self.sharedState.DARK_COLOR, border_width=2)
        self.PredictionFrame1.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        # self.create_prediction_widget()
        self.PredictionFrame= None

    def create_prediction_widget(self,is_model = False):
        """
        Create a widget for making new predictions based on user input.
        """

        # destrot the old prediction widget
        # destroy all the widgets in the file
        # for widget in self.winfo_children():
        #     widget.destroy()
        # update sharedState
        if is_model:
            self.sharedState = self.sharedState_setter()
        

        # Destroy all children of PredictionFrame1
        for widget in self.PredictionFrame1.winfo_children():
            widget.destroy()
        # Prediction Frame
        self.PredictionFrame = ctk.CTkFrame(self.PredictionFrame1, fg_color="transparent")
        self.PredictionFrame.grid(row=4, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        # Title
        self.PredictionTitle = ctk.CTkLabel(
            self.PredictionFrame,
            text="Make a New Prediction",
            font=self.FONT_TITLE,
            anchor="center"
        )
        self.PredictionTitle.pack(fill="x", pady=10)

        # Fetch feature names
        feature_names = [
            col for col in self.sharedState.get_original_data().columns
            if col != self.sharedState.get_target_column()
        ]

        # Create entry fields for each feature
        self.feature_entries = {}
        for feature in feature_names:
            if not feature.lower() == 'id':
                # Horizontal container for label and entry
                feature_container = ctk.CTkFrame(self.PredictionFrame, fg_color="transparent")
                feature_container.pack(fill="x", padx=10, pady=5)

                # Feature label
                label = ctk.CTkLabel(
                    feature_container,
                    text=feature,
                    font=self.FONT_LABEL
                )
                label.pack(side="left", padx=10)

                # Check if the feature is categorical
                if pd.api.types.is_categorical_dtype(self.sharedState.get_original_data()[feature]) or \
                        self.sharedState.get_original_data()[feature].dtype == object:
                    # Create a dropdown menu for categorical features
                    unique_values = self.sharedState.get_original_data()[feature].unique()
                    entry = ctk.CTkComboBox(feature_container, values=unique_values)
                else:
                    # Create an entry field for numerical features
                    entry = ctk.CTkEntry(feature_container)

                # Pack the entry field to the right of the label
                entry.pack(side="left", fill="x", expand=True, padx=5)
                self.feature_entries[feature] = entry

        # Predict Button
        _, _,_,_,task = self.sharedState.get_data_info()

        self.PredictButton = ctk.CTkButton(
            self.PredictionFrame,
            text="Predict class : " if task.lower() == 'classification' else ('Predict Value : ' if task.lower() == 'regression'else 'Cluster Predicted : ') ,
            command=self.make_prediction
        )
        self.PredictButton.pack(pady=10)

        # Prediction Result Label
        self.PredictionResultLabel = ctk.CTkLabel(
            self.PredictionFrame,
            text="",
            font=self.FONT_LABEL,
            anchor="center"
        )
        self.PredictionResultLabel.pack(pady=10)

    def update_prediction_widget(self):
        """
        Update the prediction widget with new features.
        """
        # Destroy the existing prediction widget
        # for widget in self.PredictionFrame.winfo_children():
            # widget.destroy()
        # Create a new prediction widget
        self.create_prediction_widget()

    def make_prediction(self):
        """
        Make a prediction based on user input and display the result.
        """
        try:
            # Collect input data from entry fields
            input_data = []
            
            for feature, entry in self.feature_entries.items():
                value = entry.get()
                print("value", value)
                if value == "":
                    messagebox.showerror("Error", f"Value for {feature} is missing.")
                    raise ValueError(f"Value for {feature} is missing.")
                
                # Check if the feature is categorical
                if pd.api.types.is_categorical_dtype(self.sharedState.get_original_data()[feature]) or self.sharedState.get_original_data()[feature].dtype == object:
                    input_data.append(value)
                else:
                    input_data.append(float(value))

            # Convert input data to DataFrame
            input_df = pd.DataFrame([input_data], columns=self.feature_entries.keys())

            # Make prediction
            prediction = self.training.predict(data = input_df)

            # If it's a classification task, map the prediction to the original class label
            _, _,_,_,task = self.sharedState.get_data_info()

            print(task)

            if task.lower() == "classification":
                original_classes = self.sharedState.get_original_data()[self.sharedState.get_target_column()].unique()
                prediction = [original_classes[int(pred)] for pred in prediction]
            elif task.lower() == "clustering":
                prediction = [self.sharedState.get_labels()[int(pred)] for pred in prediction]

            # Display prediction result
            self.PredictionResultLabel.configure(text=f"Prediction: {prediction[0]}", text_color="green")


        except Exception as e:
            # Display error message if an exception occurs
            self.PredictionResultLabel.configure(text=f"Error: {str(e)}", text_color="red")
            print(f"Error: {str(e)}")