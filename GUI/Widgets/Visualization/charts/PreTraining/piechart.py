import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI.Widgets.Visualization.charts.baseChart import BaseChart


class PieChart(BaseChart):
    def __init__(self, parent, switch_page):
        super().__init__(parent, switch_page, chart_type="Pie Chart", has_y_axis=False)
        self.create_pie_chart()

    def create_pie_chart(self):
        if self.selected_x_column is None:
            return  # Ensure X axis is selected

        # Data preparation for the pie chart (count the occurrences)
        data_for_plot = self.data[self.selected_x_column].value_counts()

        plt.figure(figsize=(10, 6))
        plt.pie(data_for_plot, labels=data_for_plot.index, autopct='%1.1f%%', startangle=90)
        
        plt.title(f"Pie Chart: {self.selected_x_column}", fontsize=14)

        # Clear previous chart
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(plt.gcf(), self.plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
