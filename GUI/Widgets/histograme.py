import customtkinter as ctk

class Histograme(ctk.CTkFrame):  # Inherit from CTkFrame for a reusable widget
    def __init__(self, parent, switch_page):
        super().__init__(parent)

        self.switch_page = switch_page

        # Configure the frame
        self.grid_columnconfigure(0, weight=1)  # Ensure widgets are centered
        self.grid_rowconfigure(0, weight=1)

        # Add a label to indicate the histogram section
        title_label = ctk.CTkLabel(self, text="Histogram Visualization", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=10, padx=10)

        # Add a button for switching pages
        switch_button = ctk.CTkButton(self, text="Switch Page", command=self.switch_page)
        switch_button.grid(row=1, column=0, pady=10)

