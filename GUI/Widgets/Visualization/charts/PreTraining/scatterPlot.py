from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI.Widgets.Visualization.charts.baseChart import BaseChart

class ScatterPlot(BaseChart):
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent, switch_page,sharedState, chart_type="Scatter Plot", has_y_axis=True,no_x_y=False)
        self.sharedState = sharedState

    def plot_chart(self):
        visualizer = super().plot_chart()
        fig = visualizer.plot_scatter(self.selected_x_column, self.selected_y_column,self.sharedState.get_target_column())

        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()


