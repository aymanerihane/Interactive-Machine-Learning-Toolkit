if page_name == "home":
            self.pages[page_name] = HomePage(self, switch_page=self.show_page, sharedState=self.sharedState)
        elif page_name == "visualization":
            self.pages[page_name] = VisualizationPage(self, switch_page=self.show_page, sharedState=self.sharedState)
        else:
            # Dynamically initialize other pages
            chart_classes = {
                "histograme": Histograme,
                "scatterplot": ScatterPlot,
                "piechart": PieChart,
                "boxplot": BoxPlot,
                "heatmap": Heatmap,
                "table": Table,
                "pairplots": PairPlots,
                "violinplots": ViolinPlots,
                "stackedbarcharts": StackedBarCharts,
            }
            if page_name in chart_classes:
                self.pages[page_name] = chart_classes[page_name](
                    self, switch_page=self.show_page, sharedState=self.sharedState
                )