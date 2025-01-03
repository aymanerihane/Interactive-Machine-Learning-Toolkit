from GUI.Widgets.Visualization.charts.baseChart import BaseChart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns

class Heatmap(BaseChart):
    def __init__(self, parent, switch_page,sharedState):
        super().__init__(parent, switch_page,sharedState, chart_type="Heatmap", has_y_axis=False, no_x_y=True)
        self.plot_chart()

    def plot_chart(self):
        visualizer = super().plot_chart()
        fig = visualizer.plot_heatmap()
        self.canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.draw()

    # def create_heatmap(self):
    #     if self.selected_x_column is None:
    #         self.selected_x_column = self.columns[0]

    #     print(self.data)

    #     # If there are categorical columns, you can convert them to numeric values if necessary
    #     # For example, converting 'Yes'/'No' to 1/0 in case of binary categorical columns
    #     for column in self.data.columns:
    #         if self.data[column].dtype == 'object':  # Check if the column is categorical
    #             self.data[column] = self.data[column].apply(lambda x: 1 if x == 'Yes' else (0 if x == 'No' else x))

    #     # Recalculate correlation matrix with numeric data
    #     corr = self.data.corr()  # Correlation matrix for heatmap
        
    #     plt.figure(figsize=(10, 6))
    #     sns.heatmap(corr, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
        
    #     plt.title("Heatmap: Feature Correlation", fontsize=14)

    #     # Clear previous chart
    #     for widget in self.plot_frame.winfo_children():
    #         widget.destroy()

    #     canvas = FigureCanvasTkAgg(plt.gcf(), self.plot_frame)
    #     canvas.get_tk_widget().pack(fill="both", expand=True)
    #     canvas.draw()