import customtkinter as ctk
from home import HomePage
from Widgets.Visualization.visualization import VisualizationPage
from Widgets.header_wgt import HeaderWidget
from Widgets.Visualization.charts.PreTraining.histograme import Histograme
from Widgets.Visualization.charts.PreTraining.scatterPlot import ScatterPlot
from Widgets.Visualization.charts.PreTraining.piechart import PieChart
from Widgets.Visualization.charts.PreTraining.boxPlot import BoxPlot
from Widgets.Visualization.charts.PreTraining.heatmap import Heatmap
from Widgets.Visualization.charts.PreTraining.table import Table
from Widgets.Visualization.charts.PreTraining.pairPlot import PairPlots

import json

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page Application")
        self.geometry("1100x700")

        # Add HeaderWidget to the main window
        self.header = HeaderWidget(self, text="HOME")
        self.header.pack(pady=10, padx=10, fill="both")

        self.pages = {}  # Store page instances
        self.initialize_pages()

        # Bind the close event to the destroy method
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def initialize_pages(self):
        """Initialize all pages and store them in a dictionary."""
        self.pages["home"] = HomePage(self, switch_page=self.show_page)
        self.pages["visualization"] = VisualizationPage(self, switch_page=self.show_page)

        for charts in [Histograme, ScatterPlot, PieChart, BoxPlot, Heatmap,Table,PairPlots]:
            self.pages[charts.__name__.lower()] = charts(self, switch_page=self.show_page)



        # Show the home page by default
        self.show_page("home")

    def destroy(self):
        """Override the destroy method to handle any cleanup before closing."""
        print("Destroying the application...")
        
        # Cancel any ongoing events (like 'after' events)
        for widget in self.winfo_children():
            widget.after_cancel(widget.winfo_id())  # Cancel any active 'after' events on widgets
        
        # Perform other cleanup tasks if needed (e.g., stop any background threads, etc.)

        super().destroy()  # Call the parent class's destroy method to ensure the app closes properly
        

    def show_page(self, page_name):
        """Switch to a specific page."""
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages
        page_name = page_name.replace(" ", "")
        self.pages[page_name.lower()].pack(expand=True, fill="both")  # Show the selected page
        # Update the header text dynamically using the page name
        self.header.update_text(page_name.capitalize())  # Capitalize to make it look cleaner

    def load_json(self, file_path):
        """Load JSON data from a file."""
        with open(file_path, "r") as file:
            return json.load(file)



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
