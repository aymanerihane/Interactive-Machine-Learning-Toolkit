import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
from scipy.cluster.hierarchy import dendrogram, linkage

class ChartHandler:
    def __init__(self, df):
        self.df = df

    def get_unique_categorical_values(self):
        """
        Get the unique values from categorical columns in their original form.
        This method helps retrieve the categorical values before encoding, so they can be used in plotting.
        """
        # Select categorical columns
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        # Create a dictionary to hold the unique values of each categorical column
        unique_values_dict = {}
        
        for col in cat_cols:
            # Retrieve unique values for each categorical column
            unique_values_dict[col] = self.df[col].unique().tolist()
        
        return unique_values_dict

    def plot_table(self):
        # Display a table with the first 10 rows of the dataframe
        fig, ax = plt.subplots(figsize=(12, 4))  # Set the size of the table
        ax.axis('off')  # Remove axes
        table = ax.table(cellText=self.df.head(10).values, colLabels=self.df.columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        return plt.gcf()

    def plot_histogram(self, column):
        # Plot histogram for a given column
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df[column], kde=True)
        plt.title(f"Histogram of {column}")
        return plt.gcf()

    def plot_scatter(self, x_column, y_column, categorical_column=None):
        """
        Scatter plot for two numerical columns. Optionally, you can provide a categorical column to color the points.
        
        :param x_column: The column for the x-axis.
        :param y_column: The column for the y-axis.
        :param categorical_column: Optional categorical column to color points.
        """
        plt.figure(figsize=(10, 6))

        if categorical_column:
            # Get unique values from the categorical column
            unique_values_dict = self.get_unique_categorical_values()
            unique_values = unique_values_dict.get(categorical_column, [])

            # Assign colors to each unique category
            palette = sns.color_palette("Set2", len(unique_values))
            sns.scatterplot(data=self.df, x=x_column, y=y_column, hue=self.df[categorical_column], palette=palette, legend="full")

            # Add a custom legend with category names
            plt.legend(title=categorical_column, labels=unique_values)
        else:
            sns.scatterplot(x=self.df[x_column], y=self.df[y_column])

        plt.title(f"Scatter Plot of {x_column} vs {y_column}")
        return plt.gcf()

    def plot_box(self, categorical_column, numerical_column):
        """
        Box plot for a numerical column, grouped by a categorical column.
        
        :param categorical_column: The column to group the numerical data by (usually a category or label).
        :param numerical_column: The numerical column to display the box plot for.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=self.df[categorical_column], y=self.df[numerical_column])
        plt.title(f"Box Plot of {numerical_column} by {categorical_column}")
        return plt.gcf()
    
    # def plot_scatter(self, x_column, y_column, categorical_column=None):
    #     """
    #     Scatter plot for two numerical columns. Optionally, you can provide a categorical column to color the points.
        
    #     :param x_column: The column for the x-axis.
    #     :param y_column: The column for the y-axis.
    #     :param categorical_column: Optional dictionary with categorical columns and their unique values.
    #     """
    #     plt.figure(figsize=(10, 6))

    #     if categorical_column:
    #         # Loop through the categorical columns provided in the dictionary
    #         for category, unique_values in categorical_column.items():
    #             # Map each unique value in the categorical column to a color using Seaborn's color palette
    #             palette = sns.color_palette("Set2", len(unique_values))
    #             # Create a mask for the categorical column values
    #             for idx, value in enumerate(unique_values):
    #                 # Apply scatterplot only for each unique value of the category
    #                 mask = self.df[category] == value
    #                 sns.scatterplot(x=self.df.loc[mask, x_column], 
    #                                 y=self.df.loc[mask, y_column], 
    #                                 label=f'{category}: {value}', 
    #                                 color=palette[idx])

    #         # Add a custom legend
    #         plt.legend(title="Categories")
    #     else:
    #         # Simple scatter plot if no categorical column is provided
    #         sns.scatterplot(x=self.df[x_column], y=self.df[y_column])

    #     plt.title(f"Scatter Plot of {x_column} vs {y_column}")
    #     return plt.gcf()


    def plot_heatmap(self):
        # Heatmap for the correlation matrix
        plt.figure(figsize=(10, 6))
        corr_matrix = self.df.corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
        plt.title("Correlation Heatmap")
        return plt.gcf()

    def plot_pie(self, column):
        # Pie chart for categorical data
        plt.figure(figsize=(10, 6))
        self.df[column].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
        plt.title(f"Pie Chart of {column}")
        plt.ylabel('')  # Remove y-label
        return plt.gcf()

    def plot_violin(self, column):
        # Violin plot for a given column
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=self.df[column])
        plt.title(f"Violin Plot of {column}")
        return plt.gcf()

    def plot_pair(self):
        # Pair plot (scatter matrix) of the dataframe
        plt.figure(figsize=(10, 10))
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

    def plot_confusion_matrix(self, y_true, y_pred):
        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=['Predicted Negative', 'Predicted Positive'], yticklabels=['True Negative', 'True Positive'])
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
        return plt.gcf()

    def plot_dendrogram(self):
        # Dendrogram for hierarchical clustering
        linked = linkage(self.df, 'ward')
        plt.figure(figsize=(10, 7))
        dendrogram(linked, orientation='top', labels=self.df.index, distance_sort='descending')
        plt.title("Dendrogram")
        return plt.gcf()

    def plot_cluster_scatter(self, x_column, y_column, labels):
        # Cluster scatter plot (after clustering algorithms like k-means)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.df[x_column], y=self.df[y_column], hue=labels, palette='Set2')
        plt.title(f"Cluster Scatter Plot of {x_column} vs {y_column}")
        return plt.gcf()
