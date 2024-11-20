import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI.Widgets.Visualization.charts.baseChart import BaseChart


class PieChart(BaseChart):
    def __init__(self, parent, switch_page):
        super().__init__(parent, switch_page, chart_type="Pie Chart", has_y_axis=False)
        self.plot_chart()

    def plot_chart(self):
        visualizer = super().plot_chart()
        fig = visualizer.plot_pie(self.selected_x_column)
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()
