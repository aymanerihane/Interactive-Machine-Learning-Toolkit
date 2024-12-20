from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))

from GUI.Widgets.Visualization.charts.baseChart import BaseChart

class BarGraphs(BaseChart):  # Inherit from CTkFrame for a reusable widget
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent, switch_page,sharedState, chart_type="Bar Graphs", has_y_axis=False,no_x_y=False,just_num=True)



    def plot_chart(self):
        visualizer = super().plot_chart()

        # Call the plot_histogram method from DataVisualizer to plot the histogram
        fig = visualizer.plot_bar_graph(self.selected_x_column)
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()


