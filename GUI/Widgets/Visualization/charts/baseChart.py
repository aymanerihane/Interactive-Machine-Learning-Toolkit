import os
import customtkinter as ctk
from Controller.dataPreProcecing import DataPreProcessor as PreD
from Controller.ChartHandler import ChartHandler


class BaseChart(ctk.CTkFrame):
    def __init__(self, parent, switch_page, chart_type ,has_y_axis=True,no_x_y=False):
        super().__init__(parent)  # Correct usage of super        
        self.switch_page = switch_page
        self.selected_x_column = None
        self.selected_y_column = None
        self.chart_type = chart_type
        self.has_y_axis = has_y_axis
        self.no_x_y = no_x_y

        # File structure
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..", "..", "..", "..")
        self.csv_file = os.path.join(root_dir, "Data/csv_file.csv")

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
            self.plot_frame = ctk.CTkFrame(self, corner_radius=10)
            self.plot_frame.grid(row=1, column=0, padx=20, pady=20, sticky="new")

        self.load_data()
        if not self.no_x_y:
            self.load_columns(True)
            if self.has_y_axis:
                self.load_columns(False)
        self.plot_chart()

    def load_data(self):
        """Load and preprocess data"""
        try:

            self.data,self.unique_categorical_values = PreD(self.csv_file).preprocess()
            print(self.unique_categorical_values)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {self.csv_file}")

    def load_columns(self, is_axis):
        """Load column names from the CSV file and create buttons."""
        if is_axis:
            label = ctk.CTkLabel(self.column_button_frame_1, text="Select X Axis", font=("Arial", 12, "bold"))
            label.pack(side="left", padx=10)

            for column in self.data:
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
        """Update the selected column for the chart."""
        if axis == 'x':
            self.selected_x_column = column
        elif axis == 'y':
            self.selected_y_column = column
        self.plot_chart()

    def plot_chart(self):
        """Plot scatter plot"""
        if not self.selected_x_column :
            self.selected_x_column = self.data.columns[0]
        if not self.selected_y_column :
            self.selected_y_column = self.data.columns[1]

        if not self.no_x_y:
            # Clear any previous chart
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

        

        visualizer = ChartHandler(self.data)
        return visualizer

    def return_to_previous_page(self):
        """Handle the return button press to navigate back."""
        if self.switch_page:
            self.switch_page("visualization")  # Call the switch page function to return


