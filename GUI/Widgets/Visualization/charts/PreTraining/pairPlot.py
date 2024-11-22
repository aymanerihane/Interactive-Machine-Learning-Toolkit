from GUI.Widgets.Visualization.charts.baseChart import BaseChart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PairPlots(BaseChart):
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent, switch_page,sharedState, chart_type="Pair Plot", has_y_axis=False,no_x_y=True)

    def plot_chart(self):
        visualizer = super().plot_chart()
        taregt_column = self.sharedState.get_target_column()
        fig = visualizer.plot_pair(taregt_column)

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()