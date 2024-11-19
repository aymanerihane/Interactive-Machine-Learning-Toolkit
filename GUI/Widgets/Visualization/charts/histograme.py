import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

# Add the project directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))


# Import the DataVisualizer class from the Controller module
from Controller.ChartHandler import ChartHandler
from Controller.dataPreProcecing import DataPreProcessor as PreD

class Histograme(ctk.CTkFrame):  # Inherit from CTkFrame for a reusable widget
    def __init__(self, parent, switch_page):
        super().__init__(parent)
        self.data = None

        # Store the parent page switch function
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

        # Create a button to return to the previous page
        self.return_button = ctk.CTkButton(
            self, text="Return", width=20, command=self.return_to_previous_page
        )
        self.return_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.column_button_frame_1 = ctk.CTkFrame(self)
        self.column_button_frame_1.grid(row=1, column=0, pady=0, sticky="ew")


        self.plot_frame = ctk.CTkFrame(self, corner_radius=10)
        self.plot_frame.grid(row=2, column=0, padx=20, pady=20, sticky="new")

        # Initialize x_axis choice and y_axis settings
        self.selected_column = None
        self.y_limit = None

        # Populate column buttons

        try:
                
            # Load the CSV data
            self.data = PreD(self.csv_file).clean_data()
            print("Data after Preprocessing************",self.data)
            print("type of data",type(self.data))
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {self.csv_file}")
        self.plot_histogram()
        self.load_columns(self.column_button_frame_1)


    def load_columns(self, frame):
        """Load column names from the CSV file and create buttons."""
        try:
             # Use the reusable load_data function
            # column_names = self.data.columns.tolist()

            # Clear previous buttons
            for widget in frame.winfo_children():
                widget.destroy()

            # Create buttons for each column and place them horizontally
            label = ctk.CTkLabel(frame, text="Select a column to plot:")
            label.pack(side="left", padx=10)
            for column in self.data.columns:
                button = ctk.CTkButton(
                    frame,
                    text=column,
                    width=100,
                    command=lambda col=column: self.update_axis(col)  # Set the selected column
                )
                button.pack(side="left", padx=10)  # Pack buttons horizontally

            # Add a horizontal scrollbar to the frame
            self.scrollbar = ctk.CTkScrollbar(frame, orientation="horizontal")
            self.scrollbar.pack(side="bottom", fill="x", expand=True, padx=10, pady=0)

        except Exception as e:
            raise ValueError(f"An error occurred while loading the columns: {e}")

    def update_axis(self, column):
        """Update the selected column for the histogram."""
        self.selected_x_column = column  # Only need one axis for a histogram
        self.plot_histogram()  # Refresh the plot


    def plot_histogram(self):
        """Plot a histogram for the selected column using the DataVisualizer class."""
        if not self.winfo_exists():  # Check if the frame exists
            return  # Avoid performing actions on a destroyed widget

        if not self.selected_x_column:
            self.selected_x_column = self.data.columns[0]  # Default to the first column

        # Clear any existing plots in the frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        try:
            

            if self.selected_x_column not in self.data.columns:
                raise ValueError(f"Column not found in CSV file: {self.selected_x_column}")

            # Create an instance of the DataVisualizer class with the loaded data
            visualizer = ChartHandler(self.data)

            # Call the plot_histogram method from DataVisualizer to plot the histogram
            fig = visualizer.plot_histogram(self.selected_x_column)
            self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
            self.canvas.draw()

        except Exception as e:
            raise ValueError(f"An error occurred while plotting the histogram: {e}")

    def return_to_previous_page(self):
        """Handle the return button press to navigate back."""
        if self.switch_page:
            self.switch_page("visualization")  # Call the switch page function to return

    def destroy(self):
        """Override the destroy method to handle any cleanup before closing."""
        print("Destroying the application...")

        # Cancel any ongoing 'after' events (such as timeouts or scheduled actions)
        for widget in self.winfo_children():
            widget.after_cancel(widget.winfo_id())  # Cancel any active 'after' events on widgets
        
        # Perform other cleanup tasks if needed (e.g., stop background threads)
        super().destroy()  # Call the parent class's destroy method to ensure the app closes properly
