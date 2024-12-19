import customtkinter as ctk


class DataStats(ctk.CTkFrame):
    def __init__(self, parent, sharedState,preprocess):
        super().__init__(parent)
        self.sharedState = sharedState
        self.preprocess = preprocess

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

        self.preProcessingFrame = ctk.CTkFrame(self.infoFrame, fg_color="transparent")
        self.preProcessingFrame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Preprocessing title
        self.preProcessingTitle = ctk.CTkLabel(self.preProcessingFrame, text="Preprocessing Options", font=self.FONT_TITLE, anchor="center")
        self.preProcessingTitle.grid(row=0, column=0, columnspan=3, padx=5, pady=10)


        button_name = ["Clean Data", "Process Text", "Reduce Features", "Handle Dates", "Encode Labels", "Scale Data", "Reset", "Auto Pre-Processing"]
        for i, name in enumerate(button_name):
            button = ctk.CTkButton(self.preProcessingFrame, text=name, command=lambda n=name: self.preprocessing(n))
            button.grid(row=i+1, column=0, padx=5, pady=5, sticky="ew")

        # Add divider
        self.divider = ctk.CTkLabel(self.infoFrame, text="", fg_color=self.sharedState.DARK_COLOR, width=2)
        self.divider.grid(row=0, column=1, sticky="ns", padx=0, pady=30)  # Use pady to subtract 10 pixels (5 on top, 5 on bottom)


    def preprocessing(self,name):
        match name:
            case "Clean Data":
                self.preprocess.clean_data()
            case "Process Text":
                self.preprocess.process_text()
            case "Reduce Features":
                self.preprocess.reduce_features()
            case "Handle Dates":
                self.preprocess.handle_dates()
            case "Encode Labels":
                self.preprocess.encode_labels()
            case "Scale Data":
                self.preprocess.scale_data()
            case "Reset":
                self.preprocess.reset()
            case "Auto Pre-Processing":
                self.preprocess.auto_preprocessing()
            case _:
                print(f"Unknown preprocessing option: {name}")

        self.update_stats()

    def update_stats(self):
        number_of_nan_values, number_of_missing_values, number_of_classes,data_shape,data_balanced,number_of_categorical_columns,number_of_numerical_columns=self.sharedState.get_data_stats()

        # Update the labels with the new stats values
        self.nanValues.configure(text=number_of_nan_values)
        self.missingValues.configure(text=number_of_missing_values)
        self.classes.configure(text=number_of_classes)
        self.dataShape.configure(text=data_shape)
        self.dataBalanced.configure(text=data_balanced)
        self.categoricalColumns.configure(text=number_of_categorical_columns)
        self.numericalColumns.configure(text=number_of_numerical_columns)