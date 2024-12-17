import os
import customtkinter as ctk
from Controller.dataPreProcecing import DataPreProcessor as PreD
from Controller.ChartHandler import ChartHandler
from tkinter import messagebox

class BaseChart(ctk.CTkFrame):
    def __init__(self, parent, switch_page,sharedState, chart_type ,has_y_axis=True,no_x_y=False,just_num=False,just_cat=False):
        super().__init__(parent)  # Correct usage of super        
        self.switch_page = switch_page
        self.selected_x_column = None
        self.selected_y_column = None
        self.chart_type = chart_type
        self.has_y_axis = has_y_axis
        self.no_x_y = no_x_y
        self.just_num = just_num
        self.just_cat = just_cat
        self.sharedState = sharedState

        # File structure
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..", "..", "..", "..")
        self.csv_file = os.path.join(root_dir, "Data/csv_file.csv")
        self.preprocess = PreD(self.csv_file)

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        if not self.no_x_y:
            self.grid_rowconfigure(1, weight=0)
            if self.has_y_axis:
                self.grid_rowconfigure(2, weight=0)
                self.grid_rowconfigure(3, weight=1)
            else:
                self.grid_rowconfigure(2, weight=1)
        else:
            self.grid_rowconfigure(1, weight=1)

        # Return Button
        self.return_button = ctk.CTkButton(
            self, text="Return", width=20, command=self.return_to_previous_page
        )
        self.return_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        if not self.no_x_y:
            print("x_y")
            # Create axis selection rows based on the chart type
            self.column_button_frame_1 = ctk.CTkScrollableFrame(self, orientation="horizontal", corner_radius=10, height=35)
            self.column_button_frame_1.grid(row=1, column=0, pady=0, sticky="ew")

            if self.has_y_axis:
                self.column_button_frame_2 = ctk.CTkScrollableFrame(self, orientation="horizontal", corner_radius=10, height=35)
                self.column_button_frame_2.grid(row=2, column=0, pady=0, sticky="ew")

            self.plot_frame = ctk.CTkFrame(self, corner_radius=10)

            if self.has_y_axis:

                self.plot_frame.grid(row=3, column=0, padx=20, pady=20, sticky="new")
            else:
                self.plot_frame.grid(row=2, column=0, padx=20, pady=20, sticky="new")
        else:
            print("no_x_y")
            self.plot_frame = ctk.CTkFrame(self, corner_radius=10)
            self.plot_frame.grid(row=1, column=0, padx=20, pady=20, sticky="new")


        self.load_data()
        if just_num:
            if not self.no_x_y:
                self.load_columns(True,just_num=True)
                if self.has_y_axis:
                    self.load_columns(False,just_num=True)
        elif just_cat:
            if not self.no_x_y:
                self.load_columns(True,just_cat=True)
                if self.has_y_axis:
                    self.load_columns(False,just_cat=True)
        else:
            if not self.no_x_y:
                self.load_columns(True)
                if self.has_y_axis:
                    self.load_columns(False)
        self.plot_chart()

    def load_data(self):
        """Load and preprocess data"""
        try:

            self.data,self.mappings  = self.preprocess.auto_preprocessing()
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {self.csv_file}")

    def load_columns(self, is_axis, just_num=False, just_cat=False):
        """Load column names from the CSV file and create buttons."""
        
        # Filter columns based on the flags
        data = self.preprocess.return_original_data()
        if just_num:
            print("just_num")
            columns = data.select_dtypes(include=['number']).columns # Filter numerical columns
            print("*******************")
            print(columns)
            print("*******************")
        elif just_cat:
            print("just_cat")
            columns = data.select_dtypes(exclude=['number']).columns 
            print("*******************")
            print(columns)
            print("*******************")
        else:
            print("all")
            columns = data.columns
            print("*******************")
            print(columns)
            print("*******************")

        if len(columns) == 0:
            error_message = "No type needed of columns found in the data"
            # prompt
            messagebox.showerror("Error", error_message)
            raise ValueError(error_message)

        # Creating the appropriate label based on axis
        if is_axis:
            label = ctk.CTkLabel(self.column_button_frame_1, text="Select X Axis", font=("Arial", 12, "bold"))
            label.pack(side="left", padx=10)

            # Create buttons for each column based on the filtered columns list
            for column in columns:
                button = ctk.CTkButton(
                    self.column_button_frame_1,
                    text=column,
                    width=100,
                    command=lambda col=column: self.update_axis(col, 'x')  # Ensure correct column reference is passed
                )
                button.pack(side="left", padx=10)
        else:
            label = ctk.CTkLabel(self.column_button_frame_2, text="Select Y Axis", font=("Arial", 12, "bold"))
            label.pack(side="left", padx=10)

            # Create buttons for each column based on the filtered columns list
            for column in columns:
                button = ctk.CTkButton(
                    self.column_button_frame_2,
                    text=column,
                    width=100,
                    command=lambda col=column: self.update_axis(col, 'y')  # Ensure correct column reference is passed
                )
                button.pack(side="left", padx=10)

    def update_axis(self, column, axis):
        """Update the selected column for the chart."""
        if axis == 'x':
            self.selected_x_column = column
        elif axis == 'y':
            self.selected_y_column = column
        self.plot_chart()

    def plot_chart(self):
        """Plot scatter plot"""

        

        if self.just_num or self.just_cat:
            data = self.preprocess.return_original_data()
            if self.just_num:
                data = data.select_dtypes(include=['number']) # Filter numerical columns
            elif self.just_cat:
                data = data.select_dtypes(exclude=['number'])
            
            if not self.selected_x_column :
                self.selected_x_column = data.columns[0]
            if not self.selected_y_column :
                if not len(data.columns) < 2:
                    self.selected_y_column = data.columns[1]
                else:
                    error_message = "No Numerical columns found in the data"
                    # prompt
                    messagebox.showerror("Error", error_message)
                    raise ValueError(error_message)
                    # self.selected_y_column = data.columns[0]
                    
        else:
            data = self.data
            if not self.selected_x_column :
                self.selected_x_column = data.columns[0]
            if not self.selected_y_column :
                self.selected_y_column = data.columns[1]

        if not self.no_x_y:
            # Clear any previous chart
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

        visualizer = ChartHandler(self.data,self.mappings)
        return visualizer

    def return_to_previous_page(self):
        """Handle the return button press to navigate back."""
        if self.switch_page:
            self.switch_page("visualization")  # Call the switch page function to return


