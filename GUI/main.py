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
from GUI.Widgets.Visualization.charts.PostTraining.dendrograms import Dendrograms
from GUI.Widgets.Visualization.charts.PostTraining.bar_graphs import BarGraphs
from GUI.Widgets.Visualization.charts.PostTraining.lineGraphs import LineGraphs
from GUI.Widgets.Visualization.charts.PostTraining.cluster_scatter_plots import ClusterScatterPlots
from GUI.Widgets.Visualization.charts.PostTraining.confusion_matrix import ConfusionMatrix
from GUI.Widgets.Visualization.charts.PostTraining.rocCurve import ROCCurve
from GUI.Widgets.Visualization.charts.PostTraining.precision_recall_curve import Precision_RecallCurve
from Controller.sharedState import SharedState

class MainApp(ctk.CTk):
    def __init__(self, sharedState):
        super().__init__()
        self.sharedState = sharedState
        self.title("Multi-Page Application")
        self.geometry("1100x700")
        self.configure(fg_color="#F5F5F5")  # Set background to light gray

        # Add HeaderWidget to the main window
        self.header = HeaderWidget(self, text="HOME")
        self.header.pack(pady=10, padx=10, fill="x")

        self.pages = {}  # Store page instances
        self.show_page("home")  # Initially show the home page

        # Bind the close event to the destroy method
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self):
        """Override the destroy method to handle any cleanup before closing."""
        print("Destroying the application...")
        for widget in self.winfo_children():
            try:
                widget.after_cancel(widget.winfo_id())
            except:
                pass
        super().destroy()

    def initialize_page(self, page_name, reinitialize=False):
        if reinitialize or page_name not in self.pages:
            if page_name in self.pages:
                # Remove the old page instance if reinitializing
                self.pages[page_name].destroy()
                del self.pages[page_name]

        # Initialize and store the page in the dictionary if not already initialized
        if page_name == "home":
            self.pages[page_name] = HomePage(self, switch_page=self.show_page, sharedState=self.sharedState)
        elif page_name == "visualization":
            self.pages[page_name] = VisualizationPage(self, switch_page=self.show_page, sharedState=self.sharedState)
        else:
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
                "dendrograms": Dendrograms,
                "bargraphs": BarGraphs,
                "linegraphs": LineGraphs,
                "clusterscatterplots": ClusterScatterPlots,
                "confusionmatrix": ConfusionMatrix,
                "roccurve": ROCCurve,
                "precision_recallcurve": Precision_RecallCurve
                
            }
            if page_name in chart_classes:
                self.pages[page_name] = chart_classes[page_name](self, switch_page=self.show_page, sharedState=self.sharedState)

    def show_page(self, page_name):
        page_name = page_name.replace(" ", "").lower()
        dynamic_pages = [
            "histograme", "scatterplot", "piechart", "boxplot", 
            "heatmap", "table", "pairplots", "violinplots", "stackedbarcharts","dendrograms","bargraphs","linegraphs","clusterscatterplots","confusionmatrix","roccurve","precision_recallcurve"
        ]
        if page_name in dynamic_pages:
            self.initialize_page(page_name, reinitialize=True)
        if page_name not in self.pages:
            self.initialize_page(page_name)
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(expand=True, fill="both")
        self.header.update_text(page_name.capitalize())

if __name__ == "__main__":
    sharedState = SharedState()
    app = MainApp(sharedState)
    app.mainloop()
