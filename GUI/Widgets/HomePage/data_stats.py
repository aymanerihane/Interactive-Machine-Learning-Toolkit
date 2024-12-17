
import customtkinter as ctk


class DataStats(ctk.CTkFrame):
    def __init__(self, parent, sharedState):
        super().__init__(parent)
        self.statTestDataUpload = "disabled"
        self.sharedState = sharedState

        

        # Define the fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")
        self.FONT_LABEL = ctk.CTkFont(size=12)
        self.FONT_BUTTON = ctk.CTkFont(size=14)

        self.infoFrame = ctk.CTkFrame(self, fg_color=self.sharedState.SECONDARY_COLOR)
        self.infoFrame.pack(pady=10, padx=20, fill="x")
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure((0, 1), weight=1)


        #######################################################
        #       First Column in Data Detail (data stats)
        #######################################################
        """
        this part will include some data information like:
            number of nan values
            number of missing values
            number of classes
            data shape
            data balanced 
            number of categorical column 
            number of numerical column 
        """

        nbr_nan, nbr_missing, nbr_classes, data_shape, data_balanced, nbr_cat, nbr_num = 0, 0, 0, "(0,0)", "None", 0, 0

        #create a frame for the first column with a light border and transparent background 
        self.dataStatsFrame = ctk.CTkFrame(self.infoFrame, fg_color=self.sharedState.PRIMARY_COLOR)
        self.dataStatsFrame.configure(border_color=self.sharedState.DARK_COLOR, border_width=1, fg_color="transparent")
        self.dataStatsFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.dataStatsFrame.grid_columnconfigure(0, weight=1)
        self.dataStatsFrame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Title
        self.dataStatsTitle = ctk.CTkLabel(self.dataStatsFrame, text="Data Stats", font=self.FONT_TITLE, anchor="w")
        self.dataStatsTitle.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # Number of nan values
        self.nanValuesLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of NaN values: ", font=self.FONT_LABEL)
        self.nanValuesLabel.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        ## value for the nan values
        self.nanValues = ctk.CTkLabel(self.dataStatsFrame, text=nbr_nan, font=self.FONT_LABEL)
        self.nanValues.grid(row=1, column=1, sticky="w", padx=10, pady=5)


        # Number of missing values
        self.missingValuesLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of missing values: ", font=self.FONT_LABEL)
        self.missingValuesLabel.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        ## value for the missing values
        self.missingValues = ctk.CTkLabel(self.dataStatsFrame, text=nbr_missing, font=self.FONT_LABEL)
        self.missingValues.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Number of classes
        self.classesLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of classes: ", font=self.FONT_LABEL)
        self.classesLabel.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        ## value for the classes
        self.classes = ctk.CTkLabel(self.dataStatsFrame, text=nbr_classes, font=self.FONT_LABEL)
        self.classes.grid(row=3, column=1, sticky="w", padx=10, pady=10)

        # Data shape
        self.dataShapeLabel = ctk.CTkLabel(self.dataStatsFrame, text="Data shape: ", font=self.FONT_LABEL)
        self.dataShapeLabel.grid(row=4, column=0, sticky="w", padx=10, pady=10)

        ## value for the data shape
        self.dataShape = ctk.CTkLabel(self.dataStatsFrame, text=data_shape, font=self.FONT_LABEL)
        self.dataShape.grid(row=4, column=1, sticky="w", padx=10, pady=10)

        # Data balanced
        self.dataBalancedLabel = ctk.CTkLabel(self.dataStatsFrame, text="Data balanced: ", font=self.FONT_LABEL)
        self.dataBalancedLabel.grid(row=5, column=0, sticky="w", padx=10, pady=10)

        ## value for the data balanced
        self.dataBalanced = ctk.CTkLabel(self.dataStatsFrame, text=data_balanced, font=self.FONT_LABEL)
        self.dataBalanced.grid(row=5, column=1, sticky="w", padx=10, pady=10)

        # Number of categorical columns
        self.categoricalColumnsLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of categorical columns: ", font=self.FONT_LABEL)
        self.categoricalColumnsLabel.grid(row=6, column=0, sticky="w", padx=10, pady=10)

        ## value for the number of categorical columns
        self.categoricalColumns = ctk.CTkLabel(self.dataStatsFrame, text=nbr_cat, font=self.FONT_LABEL)
        self.categoricalColumns.grid(row=6, column=1, sticky="w", padx=10, pady=10)

        # Number of numerical columns
        self.numericalColumnsLabel = ctk.CTkLabel(self.dataStatsFrame, text="Number of numerical columns: ", font=self.FONT_LABEL)
        self.numericalColumnsLabel.grid(row=7, column=0, sticky="w", padx=10, pady=10)

        ## value for the number of numerical columns
        self.numericalColumns = ctk.CTkLabel(self.dataStatsFrame, text=nbr_num, font=self.FONT_LABEL)
        self.numericalColumns.grid(row=7, column=1, sticky="w", padx=10, pady=10)

        
        
    def update_stats(self):
        """Update the data stats."""
        print("Updating data stats...")
        nbr_nan, nbr_missing, nbr_classes, data_shape, data_balanced, nbr_cat, nbr_num = self.sharedState.get_data_stats()
        
        self.nanValues.configure(text=nbr_nan)
        self.missingValues.configure(text=nbr_missing)
        self.classes.configure(text=nbr_classes)
        self.dataShape.configure(text=data_shape)
        self.dataBalanced.configure(text=data_balanced)
        self.categoricalColumns.configure(text=nbr_cat)
        self.numericalColumns.configure(text=nbr_num)

        print("Data stats updated.")

        # Force the GUI to refresh
        self.update_idletasks()
        
        

        


        
        

        #######################################################
        #       Second Column in Data Detrail (preprocessing)
        #######################################################
       