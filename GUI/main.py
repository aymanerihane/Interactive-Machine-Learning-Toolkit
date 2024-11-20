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
from GUI.Widgets.Visualization.charts.PreTraining.violin_Plots import ViolinPlots
from GUI.Widgets.Visualization.charts.PreTraining.stacked_Bar_Charts import StackedBarCharts
from Controller.sharedState import SharedState

class MainApp(ctk.CTk):
    def __init__(self, sharedState):
        super().__init__()
        self.sharedState = sharedState
        self.title("Multi-Page Application")
        self.geometry("1100x700")

        # Add HeaderWidget to the main window
        self.header = HeaderWidget(self, text="HOME")
        self.header.pack(pady=10, padx=10, fill="both")

        self.pages = {}  # Store page instances
        self.show_page("home")  # Initially show the home page

        # Bind the close event to the destroy method
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self):
        """Override the destroy method to handle any cleanup before closing."""
        print("Destroying the application...")
        
        # Cancel any ongoing events (like 'after' events)
        for widget in self.winfo_children():
            widget.after_cancel(widget.winfo_id())  # Cancel any active 'after' events on widgets
        
        # Perform other cleanup tasks if needed (e.g., stop any background threads, etc.)

        super().destroy()  # Call the parent class's destroy method to ensure the app closes properly

    def initialize_page(self, page_name):
        """Initialize and store the page in the dictionary if not already initialized."""
        if page_name == "home":
            self.pages[page_name] = HomePage(self, switch_page=self.show_page,sharedState=self.sharedState)
        elif page_name == "visualization":
            self.pages[page_name] = VisualizationPage(self, switch_page=self.show_page,sharedState=self.sharedState)
        else:
            # Dynamically initialize other pages
            chart_classes = {
                "histograme": Histograme,
                "scatterplot": ScatterPlot,
                "piechart": PieChart,
                "boxplot": BoxPlot,
                "heatmap": Heatmap,
                "table": Table,
                "pairplots": PairPlots,
                "violinplots": ViolinPlots,
                "stackedbarcharts": StackedBarCharts,
            }
            if page_name in chart_classes:
                self.pages[page_name] = chart_classes[page_name](self, switch_page=self.show_page, sharedState=self.sharedState)

    def show_page(self, page_name):
        """Switch to a specific page, initializing it if necessary."""
        page_name = page_name.replace(" ", "").lower()  # Normalize page name
        
        # Initialize the page if it hasn't been initialized yet
        if page_name not in self.pages:
            self.initialize_page(page_name)

        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()

        # Show the selected page
        self.pages[page_name].pack(expand=True, fill="both")

        # Update the header text dynamically using the page name
        self.header.update_text(page_name.capitalize())  # Capitalize to make it look cleaner

if __name__ == "__main__":
    sharedState = SharedState()
    app = MainApp(sharedState)
    app.mainloop()
