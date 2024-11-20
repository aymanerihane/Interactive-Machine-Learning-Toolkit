from GUI.Widgets.Visualization.charts.baseChart import BaseChart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

class BoxPlot(BaseChart):
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent, switch_page,sharedState, chart_type="Box Plot", has_y_axis=True, just_cat=True)
        self.plot_chart()

    def plot_chart(self):
        visualizer = super().plot_chart()
        fig = visualizer.plot_box(self.selected_x_column, self.selected_y_column)
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()


