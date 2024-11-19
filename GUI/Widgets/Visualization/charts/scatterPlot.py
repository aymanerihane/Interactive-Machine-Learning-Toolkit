import customtkinter as ctk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Controller.ChartHandler import ChartHandler
from Controller.dataPreProcecing import DataPreProcessor as PreD
import os

class ScatterPlot(ctk.CTkFrame):
    def __init__(self, parent, switch_page):
        super().__init__(parent)
        self.switch_page = switch_page
        self.selected_x_column = None
        self.selected_y_column = None
        
        # File structure
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..", "..", "..", "..")
        self.csv_file = os.path.join(root_dir, "Data/csv_file.csv")

         # Configure the frame layout
        self.grid_columnconfigure(0, weight=1)  # Ensure the first column stretches
        self.grid_rowconfigure(0, weight=0)  # Row for buttons, no stretching
        self.grid_rowconfigure(1, weight=0)  # Row for buttons, no stretching
        self.grid_rowconfigure(2, weight=0)  # Row for plot, stretches to take 
        self.grid_rowconfigure(3, weight=1)  # Row for plot, stretches to take 

        # Create a button to return to the previous page
        self.return_button = ctk.CTkButton(
            self, text="Return", width=20, command=self.return_to_previous_page
        )
        self.return_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.column_button_frame_1 = ctk.CTkScrollableFrame(self,horizontalscroll=True)
        self.column_button_frame_1.grid(row=1, column=0, pady=0, sticky="ew")


        self.column_button_frame_2 = ctk.CTkFrame(self)
        self.column_button_frame_2.grid(row=2, column=0, pady=0, sticky="ew")


        self.plot_frame = ctk.CTkFrame(self, corner_radius=10)
        self.plot_frame.grid(row=3, column=0, padx=20, pady=20, sticky="new")

        self.load_data()
        self.plot_scatter()
        self.load_columns(False)
        self.load_columns(True)

    def load_data(self):
        """Load and preprocess data"""
        try:
            self.data = PreD(self.csv_file).clean_data()
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {self.csv_file}")

    def load_columns(self, is_axis):
        """Load column names from the CSV file and create buttons."""
        # # Clean both frames before adding new buttons
        # for widget in self.column_button_frame_1.winfo_children():
        #     widget.destroy()

        # for widget in self.column_button_frame_2.winfo_children():
        #     widget.destroy()

        if is_axis:
            for column in self.data.columns:
                label = ctk.CTkLabel(self.column_button_frame_1, text="Select X Axis", font=("Arial", 12, "bold"))
                label.pack(side="left", padx=10)
                label = ctk.CTkLabel(self.column_button_frame_1, text="Select X Axis", font=("Arial", 12, "bold"))
                label.pack(side="left", padx=10)
                button = ctk.CTkButton(
                    self.column_button_frame_1,
                    text=column,
                    width=100,
                    command=lambda col=column: self.update_axis(col, 'x')
                )
                button.pack(side="left", padx=10)
        else:
            label = ctk.CTkLabel(self.column_button_frame_2, text="Select Y Axis", font=("Arial", 12, "bold"))
            label.pack(side="left", padx=10)
            for column in self.data.columns:
                button = ctk.CTkButton(
                    self.column_button_frame_2,
                    text=column,
                    width=100,
                    command=lambda col=column: self.update_axis(col, 'y')
                )
                button.pack(side="left", padx=10)

    def update_axis(self, column, axis):
        """Update the selected column for the scatter plot."""
        if axis == 'x':
            self.selected_x_column = column
        elif axis == 'y':
            self.selected_y_column = column
        self.plot_scatter()

    def plot_scatter(self):
        """Plot scatter plot"""
        if not self.selected_x_column :
            self.selected_x_column = self.data.columns[0]
        if not self.selected_y_column :
            self.selected_y_column = self.data.columns[1]

        # Clear any previous chart
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        visualizer = ChartHandler(self.data)
        fig = visualizer.plot_scatter(self.selected_x_column, self.selected_y_column)

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

        
    def return_to_previous_page(self):
        """Handle the return button press to navigate back."""
        if self.switch_page:
            self.switch_page("visualization")  # Call the switch page function to return

