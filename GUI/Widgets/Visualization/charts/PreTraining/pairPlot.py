from GUI.Widgets.Visualization.charts.baseChart import BaseChart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PairPlots(BaseChart):
    def __init__(self, parent, switch_page):
        super().__init__(parent, switch_page, chart_type="Pair Plot", has_y_axis=False,no_x_y=True)

    def plot_chart(self):
        visualizer = super().plot_chart()
        fig = visualizer.plot_pair()

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()