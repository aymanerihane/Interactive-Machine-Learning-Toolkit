import customtkinter as ctk
from home import HomePage
from Widgets.Visualization.visualization import VisualizationPage
from Widgets.header_wgt import HeaderWidget
from Widgets.histograme import Histograme
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

    def initialize_pages(self):
        """Initialize all pages and store them in a dictionary."""
        self.pages["home"] = HomePage(self, switch_page=self.show_page)
        self.pages["visualization"] = VisualizationPage(self, switch_page=self.show_page)
        self.pages["Histograms"] = Histograme(self,switch_page=self.show_page)

        # charts = self.load_data(self)
        # for category, data in charts.items():
        #     for data_type, chart_data in data.items():
        #         self.pages[chart_data] = chart_data["class"](self, switch_page=self.show_page)
        

        # Show the home page by default
        self.show_page("home")
        

    def show_page(self, page_name):
        """Switch to a specific page."""
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages
        self.pages[page_name].pack(expand=True, fill="both")  # Show the selected page

        # Update the header text dynamically using the page name
        self.header.update_text(page_name.capitalize())  # Capitalize to make it look cleaner


    def load_data(self):
        with open("data.json", "r") as file:
            data = json.load(file)
        return data



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
