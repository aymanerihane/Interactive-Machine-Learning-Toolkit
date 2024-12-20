import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
from scipy.cluster.hierarchy import dendrogram, linkage

class ChartHandler:
    def __init__(self, df,categorical_mappings=None):
        self.df = df
        self.categorical_mappings = categorical_mappings or {}
    

    # def plot_table(self):
    #     # Display a table with the first 10 rows of the dataframe
    #     fig, ax = plt.subplots(figsize=(12, 4))  # Set the size of the table
    #     ax.axis('off')  # Remove axes
    #     table = ax.table(cellText=self.df.head(10).values, colLabels=self.df.columns, loc='center', cellLoc='center')
    #     table.auto_set_font_size(False)
    #     table.set_fontsize(10)
    #     return plt.gcf()

    def plot_histogram(self, column):
        # Plot histogram for a given column
        plt.figure(figsize=(10, 6))
        #take just the numerical columns
        sns.histplot(self.df[column], kde=True)
        plt.title(f"Histogram of {column}")
        return plt.gcf()

    def plot_scatter(self, x_column, y_column,target):
        """
        Scatter plot for two numerical columns. If a column is encoded and present in 
        self.categorical_mappings, it uses the original values for coloring.
        
        :param x_column: The column for the x-axis.
        :param y_column: The column for the y-axis.
        """
        # Initialize the plot
        plt.figure(figsize=(10, 6))

        # Check if either of the columns is mapped to categorical values
        color_labels = None
        legend_title = None

        for column in [x_column, y_column]:
            if column in self.categorical_mappings:
                # Decode the categorical column using the mappings
                unique_values = self.categorical_mappings[target]
                color_labels = self.df[target].map({i: val for i, val in enumerate(unique_values)})
                legend_title = target
                break  # Use the first categorical column found

        if color_labels is not None:
            # Scatter plot with hue based on decoded labels
            sns.scatterplot(
                x=self.df[x_column],
                y=self.df[y_column],
                hue=color_labels,
                palette='Set2'
            )
            plt.legend(title=legend_title, loc='upper left')
        else:
            # Simple scatter plot if no categorical mappings are found
            sns.scatterplot(x=self.df[x_column], y=self.df[y_column])

        # Add title and labels
        plt.title(f"Scatter Plot of {x_column} vs {y_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        return plt.gcf()


    def plot_box(self, categorical_column, numerical_column):
        """
        Box plot for a numerical column, grouped by a categorical column.
        Automatically decodes categorical column values using self.categorical_mappings if available.

        :param categorical_column: The categorical column to group the numerical data by.
        :param numerical_column: The numerical column to display the box plot for.
        """
        plt.figure(figsize=(10, 6))

        # Decode the categorical column if mappings are available
        if categorical_column in self.categorical_mappings:
            unique_values = self.categorical_mappings[categorical_column]
            decoded_categories = self.df[categorical_column].map({i: val for i, val in enumerate(unique_values)})
            sns.boxplot(x=decoded_categories, y=self.df[numerical_column])
            plt.xlabel(f"{categorical_column} (decoded)")
        else:
            sns.boxplot(x=self.df[categorical_column], y=self.df[numerical_column])

        # Add title and labels
        plt.title(f"Box Plot of {numerical_column} by {categorical_column}")
        plt.ylabel(numerical_column)
        return plt.gcf()

   

    def plot_heatmap(self):
        # Heatmap for the correlation matrix
        plt.figure(figsize=(10, 6))
        corr_matrix = self.df.corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
        plt.title("Correlation Heatmap")
        return plt.gcf()

    def plot_pie(self, column):
        """
        Plot a pie chart for a categorical column, using original unique values as the legend.
        """
        # Get original unique values using the method
        unique_values_dict = self.categorical_mappings
        
        # Reverse the encoding (assume the column is already encoded)
        if unique_values_dict and column in unique_values_dict:
            legend_labels = unique_values_dict[column]
        else:
            legend_labels = self.df[column].unique()  # Fallback if no mapping is found

        # Plot the pie chart
        plt.figure(figsize=(10, 6))
        self.df[column].value_counts().plot.pie(
            autopct='%1.1f%%', startangle=90, cmap='Set3'
        )
        plt.title(f"Pie Chart of {column}")
        plt.ylabel('')  # Remove y-label
        
        # Use original unique values as legend
        plt.legend(labels=legend_labels, title=column, loc='upper left')
        return plt.gcf()
    

    def plot_violin(self, column):
        # Violin plot for a given column
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=self.df[column])
        plt.title(f"Violin Plot of {column}")
        return plt.gcf()

    def plot_pair(self,sharedState):
        # Pair plot (scatter matrix) of the dataframe
        plt.figure(figsize=(10, 6))
        if len(self.df.columns) > 3:
            # take just the 5 first columns and make the hue the target column
            df = self.df.iloc[:, :3]
            sns.pairplot(df, hue="Species")
            plt.title("Pair Plot for First 3 Columns")
        else:
            sns.pairplot(self.df)
            plt.title("Pair Plot")

        return plt.gcf()

    def plot_stacked_bar(self):
        # Stacked bar chart (suitable for categorical data)
        plt.figure(figsize=(10, 6))
        self.df.groupby(self.df.columns[0]).sum().T.plot(kind='bar', stacked=True)
        plt.title("Stacked Bar Chart")
        return plt.gcf()

    def plot_line(self, x_column, y_column):
        # Line plot for two numerical columns
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=self.df[x_column], y=self.df[y_column])
        plt.title(f"Line Plot of {x_column} vs {y_column}")
        return plt.gcf()

    def plot_confusion_matrix(self, y_true, y_pred,labels):
        # Confusion Matrix
        
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=labels, yticklabels=labels)
        plt.title("Confusion Matrix")
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        return plt.gcf()

    def plot_roc_curve(self, y_true, y_score):
        # ROC Curve
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        plt.figure(figsize=(10, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC)')
        plt.legend(loc="lower right")
        return plt.gcf()

    def plot_precision_recall_curve(self, y_true, y_score):
        # Precision-Recall Curve
        precision, recall, _ = precision_recall_curve(y_true, y_score)
        plt.figure(figsize=(10, 6))
        plt.plot(recall, precision, color='b', lw=2)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        return plt.gcf()

    def plot_bar_graph(self, column):
        # Bar chart for categorical data
        plt.figure(figsize=(10, 6))
        sns.countplot(x=self.df[column])
        plt.title(f"Bar Graph of {column}")
        #rotate x-axis labels
        plt.xticks(rotation=45)
        return plt.gcf()

    def plot_dendrogram(self):
        # Dendrogram for hierarchical clustering
        linked = linkage(self.df, 'ward')
        plt.figure(figsize=(10, 7))
        dendrogram(linked, orientation='top', labels=self.df.index, distance_sort='descending')
        plt.title("Dendrogram")
        plt.xticks(rotation=45) 
        return plt.gcf()

    def plot_cluster_scatter(self, x_column, y_column, labels):
        """
        Scatter plot for two numerical columns with cluster labels.
        params:
        x_column: The column for the x-axis.
        y_column: The column for the y-axis.
        labels: The cluster labels obtained from clustering algorithms like k-means.
        """
        # Cluster scatter plot (after clustering algorithms like k-means)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.df[x_column], y=self.df[y_column], hue=labels, palette='Set2')
        plt.title(f"Cluster Scatter Plot of {x_column} vs {y_column}")
        plt.xticks(rotation=45)  
        return plt.gcf()
