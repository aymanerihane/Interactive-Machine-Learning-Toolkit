from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))

from GUI.Widgets.Visualization.charts.baseChart import BaseChart

class PrecisionRecallCurve(BaseChart):  # Inherit from CTkFrame for a reusable widget
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent, switch_page,sharedState, chart_type="Precision_Recall Curve", has_y_axis=False,no_x_y=True,just_num=True)



    def plot_chart(self):
        visualizer = super().plot_chart()

        # Call the plot_histogram method from DataVisualizer to plot the histogram
        fig = visualizer.plot_precision_recall_curve(self.sharedState.get_y_test(), self.sharedState.get_y_pred())
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()


