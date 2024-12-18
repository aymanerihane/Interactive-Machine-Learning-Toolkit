import customtkinter as ctk
import os
from Controller.dataPreProcecing import DataPreProcessor as PreD
import pandas as pd
from tkinter import ttk


class Table(ctk.CTkFrame):
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent)  # Correct usage of super        
        self.switch_page = switch_page
        self.selected_x_column = None
        self.selected_y_column = None
        self.sharedState = sharedState

        # File structure
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..", "..", "..", "..", "..")
        self.csv_file = os.path.join(root_dir, "Data/csv_file.csv")

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # Return Button
        self.return_button = ctk.CTkButton(
            self, text="Return", width=20, command=self.return_to_previous_page
        )
        self.return_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        #see data preprocess or original data
        self.data_option = ctk.StringVar(value="original")  # Default to preprocessed data
        # Option menu to select data type
        self.data_option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.data_option,
            values=["original","preprocessed"],
            command=self.switch_data
        )
        self.data_option_menu.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # Load data
        # self.data = self.load_data()
        self.data = self.sharedState.get_data()

        if self.data is not None:
            # Create checkboxes for columns
            self.column_checkboxes = {}
            self.create_column_checkboxes()

            # Create table
            self.create_table()

        

        

    def switch_data(self , *args):
        """Switch between preprocessed and original data"""
        print("starting switching data type...")
        if self.data_option.get() == "preprocessed":
            self.data = self.sharedState.get_data()
        else:
            self.data = self.sharedState.get_original_data()

        # Update table with new data
        self.update_table_columns()
        

    def create_column_checkboxes(self):
        """Create checkboxes for each column to toggle visibility"""

        checkbox_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", corner_radius=10, height=35)  # Frame for checkboxes
        checkbox_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for col in self.data.columns:
            var = ctk.BooleanVar(value=True)  # Checkbox starts checked
            checkbox = ctk.CTkCheckBox(
                checkbox_frame,
                text=col,
                variable=var,
                command=lambda col=col: self.toggle_column(col)
            )
            checkbox.pack(side="left", padx=5, pady=5)
            self.column_checkboxes[col] = var

    def create_table(self):
        """Create a table to display the data using ttk.Treeview"""
        tree_frame = ctk.CTkFrame(self)  # Frame for the table
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Treeview widget for displaying data
        self.treeview = ttk.Treeview(tree_frame, show="headings")
        self.treeview.pack(fill="both", expand=True)

        # Add scrollbars
        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.treeview.xview)
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")

        # Set initial columns and headings
        # self.update_table_columns()

        # Initially show all columns
        self.treeview["columns"] = list(self.data.columns)

        # Set column headers
        for col in self.data.columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor="center")

        # Insert data into the table
        for _, row in self.data.iterrows():
            self.treeview.insert("", "end", values=list(row))

    def toggle_column(self, col):
        """Toggle visibility of a column based on checkbox state"""
        if self.column_checkboxes[col].get():  # If checked, show the column
            self.treeview["columns"] = list(self.treeview["columns"]) + [col]
        else:  # If unchecked, hide the column
            self.treeview["columns"] = [c for c in self.treeview["columns"] if c != col]

        # Update column headings
        self.update_table_columns()

    def update_table_columns(self):
        """Update table columns and populate rows"""
        current_columns = list(self.treeview["columns"])

        # Clear existing columns and rows
        self.treeview.delete(*self.treeview.get_children())
        for col in self.treeview["columns"]:
            self.treeview.heading(col, text="")

        # Set columns and headings
        self.treeview["columns"] = current_columns
        for col in current_columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor="center")  # Adjust column width

        # Insert data into the table
        for _, row in self.data.iterrows():
            self.treeview.insert("", "end", values=[row[col] for col in current_columns])

    # def load_data(self):
    #     """Load and preprocess data"""
    #     try:
    #         preprocessor = PreD(self.csv_file,sharedState=self.sharedState)
    #         nw_data = preprocessor.auto_preprocessing()
    #         # return preprocessor.return_original_data()
    #         return nw_data
    #     except FileNotFoundError:
    #         raise FileNotFoundError(f"CSV file not found at: {self.csv_file}")
    #     except Exception as e:
    #         print(f"Error loading data: {e}")
    #         return None

    def return_to_previous_page(self):
        self.switch_page("visualization")
