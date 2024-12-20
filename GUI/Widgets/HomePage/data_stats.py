import customtkinter as ctk
from Controller.dataPreProcecing import DataPreProcessor as PreD

class DataStats(ctk.CTkFrame):
    def __init__(self, parent, sharedState,refresh_data_training_button):
        super().__init__(parent)
        self.sharedState = sharedState
        self.refresh_data_training_button = refresh_data_training_button
        self.preprocess = PreD(sharedState=self.sharedState,just_for_method_use=True)

        # Define fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")
        self.FONT_LABEL = ctk.CTkFont(size=12)

        # Main info frame with border
        self.infoFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.infoFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.infoFrame.configure(border_color=self.sharedState.DARK_COLOR, border_width=2)

        # Configure grid for the main frame (self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Configure grid inside infoFrame
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure(1, weight=1)
        self.infoFrame.grid_columnconfigure(2, weight=1)

        #######################################################
        #       First Column in Data Detail (Data Stats)
        #######################################################

        # Default stats values
        nbr_nan, nbr_missing, nbr_classes, data_shape, data_balanced, nbr_cat, nbr_num = 0, 0, 0, "(0,0)", "None", 0, 0

        # Data stats frame
        self.dataStatsFrame = ctk.CTkFrame(self.infoFrame, fg_color="transparent")
        self.dataStatsFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Title
        self.dataStatsTitle = ctk.CTkLabel(self.dataStatsFrame, text="Data Stats", font=self.FONT_TITLE, anchor="center")
        self.dataStatsTitle.grid(row=0, column=0, columnspan=2, sticky="n", padx=10, pady=10)

        # Number of NaN values
        self.nanValuesLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of NaN values:", font=self.FONT_LABEL)
        self.nanValuesLabel.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.nanValues = ctk.CTkLabel(self.dataStatsFrame, text=nbr_nan, font=self.FONT_LABEL)
        self.nanValues.grid(row=1, column=1, padx=10, pady=2, sticky="w")

        # Number of missing values
        self.missingValuesLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of missing values:", font=self.FONT_LABEL)
        self.missingValuesLabel.grid(row=2, column=0, padx=10, pady=2, sticky="w")
        self.missingValues = ctk.CTkLabel(self.dataStatsFrame, text=nbr_missing, font=self.FONT_LABEL)
        self.missingValues.grid(row=2, column=1, padx=10, pady=2, sticky="w")

        # Number of classes
        self.classesLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of classes:", font=self.FONT_LABEL)
        self.classesLabel.grid(row=3, column=0, padx=10, pady=2, sticky="w")
        self.classes = ctk.CTkLabel(self.dataStatsFrame, text=nbr_classes, font=self.FONT_LABEL)
        self.classes.grid(row=3, column=1, padx=10, pady=2, sticky="w")

        # Data shape
        self.dataShapeLabel = ctk.CTkLabel(self.dataStatsFrame, text="Data shape:", font=self.FONT_LABEL)
        self.dataShapeLabel.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        self.dataShape = ctk.CTkLabel(self.dataStatsFrame, text=data_shape, font=self.FONT_LABEL)
        self.dataShape.grid(row=4, column=1, padx=10, pady=2, sticky="w")

        # Data balanced
        self.dataBalancedLabel = ctk.CTkLabel(self.dataStatsFrame, text="Data balanced:", font=self.FONT_LABEL)
        self.dataBalancedLabel.grid(row=5, column=0, padx=10, pady=2, sticky="w")
        self.dataBalanced = ctk.CTkLabel(self.dataStatsFrame, text=data_balanced, font=self.FONT_LABEL)
        self.dataBalanced.grid(row=5, column=1, padx=10, pady=2, sticky="w")

        # Number of categorical columns
        self.categoricalColumnsLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of categorical columns:", font=self.FONT_LABEL)
        self.categoricalColumnsLabel.grid(row=6, column=0, padx=10, pady=2, sticky="w")
        self.categoricalColumns = ctk.CTkLabel(self.dataStatsFrame, text=nbr_cat, font=self.FONT_LABEL)
        self.categoricalColumns.grid(row=6, column=1, padx=10, pady=2, sticky="w")

        # Number of numerical columns
        self.numericalColumnsLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of numerical columns:", font=self.FONT_LABEL)
        self.numericalColumnsLabel.grid(row=7, column=0, padx=10, pady=2, sticky="w")
        self.numericalColumns = ctk.CTkLabel(self.dataStatsFrame, text=nbr_num, font=self.FONT_LABEL)
        self.numericalColumns.grid(row=7, column=1, padx=10, pady=2, sticky="w")

        #######################################################
        #       Second Column in Data Detail (Preprocessing)
        #######################################################

        self.preProcessingFrame = ctk.CTkFrame(self.infoFrame, fg_color="transparent",width=550)
        self.preProcessingFrame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Preprocessing title
        self.preProcessingTitle = ctk.CTkLabel(self.preProcessingFrame, text="Preprocessing Options", font=self.FONT_TITLE, anchor="center")
        self.preProcessingTitle.grid(row=0, column=0, columnspan=3, padx=5, pady=10)


        # check if data is loaded
        if self.sharedState.get_data() is not None:
            self.create_preprocessing_buttons()
        else:
            print("Data is not loaded yet")
            self.label_no_file = ctk.CTkLabel(self.preProcessingFrame, text="No file uploaded yet", text_color=self.sharedState.WHITE, font=self.FONT_LABEL)


        # Add divider
        self.divider = ctk.CTkLabel(self.infoFrame, text="", fg_color=self.sharedState.DARK_COLOR, width=2)
        self.divider.grid(row=0, column=1, sticky="ns", padx=0, pady=30)  


    def create_preprocessing_buttons(self):
        """
        Create a scrollable frame with buttons for preprocessing steps.
        Dynamically enable or disable buttons based on conditions.
        Disable buttons after they are clicked, and re-enable all after Reset.
        """
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.preProcessingFrame, width=500, height=200)
        scroll_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Button names and associated preprocessing conditions
        button_names = [
            "Clean Data",
            "Scale Data",
            "Label Encode",
            "Handle Dates",
            "Reduce Features",
            "Balance Classes",
            "Handle Outliers",
            "Transform Skewed Features",
            "Standardize Data Types",  # Always enabled
            "Binarize Target",
            "Apply Feature Augmentation",
            "Reset",
            "Auto Pre-Processing",  # Always enabled
        ]

        # Enable/disable conditions for each step
        data_type, balance, _, features, task = self.sharedState.get_data_info()
        enable_conditions = {
            "Clean Data": True,  # Always enabled
            "Scale Data": data_type in ["continuous", "mixed"],
            "Label Encode": data_type in ["categorical", "mixed"],
            "Handle Dates": any("date" in col.lower() for col in self.sharedState.get_data().columns),
            "Reduce Features": features == "high",
            "Balance Classes": task == "classification" and balance == "imbalanced",
            "Handle Outliers": data_type in ["continuous", "mixed"],
            "Transform Skewed Features": data_type in ["continuous", "mixed"],
            "Standardize Data Types": True,  # Always enabled
            "Binarize Target": task == "classification" and len(self.sharedState.get_data()[self.sharedState.get_target_column()].unique()) == 2,
            "Apply Feature Augmentation": features == "low",
            "Reset": True,  # Always enabled
            "Auto Pre-Processing": True,  # Always enabled
        }

        # Store references to buttons for enabling/disabling
        self.buttons = {}

        def on_button_click(name):
            """Handle button click and disable the button."""
            if name == "Reset":
                # Re-enable all buttons after reset
                for btn_name, btn in self.buttons.items():
                    btn.configure(state=ctk.NORMAL if enable_conditions.get(btn_name, False) else ctk.DISABLED)
            else:
                # Disable the clicked button
                self.buttons[name].configure(state=ctk.DISABLED)

            # Perform preprocessing action
            self.preprocessing(name)

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


    def preprocessing(self, name):
        """
        Main preprocessing function with conditions based on dataset characteristics and user preferences.
        """
        # Fetch the dataset and dataset info
        self.preprocess.set_data(self.sharedState.get_data())
        data_type, balance, _, features, task = self.sharedState.get_data_info()

        # Enable/Disable conditions for each step
        enable_steps = {
            "Clean Data": True,  # Always enabled
            "Scale Data": data_type in ["continuous", "mixed"],
            "Label Encode": data_type in ["categorical", "mixed"],
            "Handle Dates": any("date" in col.lower() for col in self.sharedState.get_data().columns),
            "Reduce Features": features == "high",
            "Balance Classes": task == "classification" and balance == "imbalanced",
            "Handle Outliers": data_type in ["continuous", "mixed"],
            "Transform Skewed Features": data_type in ["continuous", "mixed"],
            "Standardize Data Types": True,  # Always enabled
            "Binarize Target": task == "classification" and len(self.sharedState.get_data()[self.sharedState.get_target_column()].unique()) == 2,
            "Apply Feature Augmentation": features == "low",
            "Reset": True,  # Always enabled
            "Auto Pre-Processing": True,  # Always enabled
        }

        # Action map
        actions = {
            "Clean Data": self.preprocess.clean_data,
            "Scale Data": self.preprocess.scale_data,
            "Label Encode": self.preprocess.label_encode,
            "Handle Dates": self.preprocess.handle_dates,
            "Reduce Features": lambda: self.preprocess.reduce_features(threshold=0.85),
            "Balance Classes": self.preprocess.balance_classes,
            "Handle Outliers": self.preprocess.handle_outliers,
            "Transform Skewed Features": self.preprocess.transform_skewed_features,
            "Standardize Data Types": self.preprocess.standardize_data_types,
            "Binarize Target": self.preprocess.binarize_target,
            "Apply Feature Augmentation": self.preprocess.apply_feature_augmentation,
            "Reset": self.preprocess.reset,
            "Auto Pre-Processing": self.preprocess.auto_preprocessing,
        }

        # Perform the selected action if enabled
        if name in enable_steps and enable_steps[name]:
            print(f"Executing '{name}' preprocessing step.")
            try:
                actions[name]()
                # Update the shared state after the preprocessing step
                self.sharedState.set_data(self.preprocess.df)
                self.sharedState.add_process(name)
                print(f"'{name}' step completed successfully.")
            except Exception as e:
                print(f"Error occurred while executing '{name}': {e}")
        else:
            print(f"'{name}' step is either disabled or not recognized.")

        # Update dataset statistics after preprocessing
        self.preprocess.set_data_stats(None,refreach=False)
        self.update_stats()
        self.sharedState.set_preprocessing_finish(True)


    def update_stats(self,first=False):
        number_of_nan_values, number_of_missing_values, number_of_classes,data_shape,data_balanced,number_of_categorical_columns,number_of_numerical_columns=self.sharedState.get_data_stats()

        # Update the labels with the new stats values
        self.nanValues.configure(text=number_of_nan_values)
        self.missingValues.configure(text=number_of_missing_values)
        self.classes.configure(text=number_of_classes)
        self.dataShape.configure(text=data_shape)
        self.dataBalanced.configure(text=data_balanced)
        self.categoricalColumns.configure(text=number_of_categorical_columns)
        self.numericalColumns.configure(text=number_of_numerical_columns)

        if first:
            self.create_preprocessing_buttons()
            self.refresh_data_training_button()
        