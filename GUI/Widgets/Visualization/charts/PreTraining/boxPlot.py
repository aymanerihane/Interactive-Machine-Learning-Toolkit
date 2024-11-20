from GUI.Widgets.Visualization.charts.baseChart import BaseChart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

class BoxPlot(BaseChart):
    def __init__(self, parent, switch_page):
        super().__init__(parent, switch_page, chart_type="Box Plot", has_y_axis=True)
        self.plot_chart()

    def plot_chart(self):
        visualizer = super().plot_chart()
        fig = visualizer.plot_box(self.selected_x_column, self.selected_y_column)
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()

    # def create_box_plot(self):
    #     if self.selected_x_column is None or self.selected_y_column is None:
    #         self.selected_x_column = self.columns[0]
    #         self.selected_y_column = self.columns[1]

    #     data_for_plot = self.data[[self.selected_x_column, self.selected_y_column]]
        
    #     plt.figure(figsize=(10, 6))
    #     sns.boxplot(x=self.selected_x_column, y=self.selected_y_column, data=data_for_plot)
        
    #     plt.title(f"Box Plot: {self.selected_x_column} vs {self.selected_y_column}", fontsize=14)
    #     plt.xlabel(self.selected_x_column, fontsize=12)
    #     plt.ylabel(self.selected_y_column, fontsize=12)

    #     # Clear previous chart
    #     for widget in self.plot_frame.winfo_children():
    #         widget.destroy()

    #     canvas = FigureCanvasTkAgg(plt.gcf(), self.plot_frame)
    #     canvas.get_tk_widget().pack(fill="both", expand=True)
    #     canvas.draw()

