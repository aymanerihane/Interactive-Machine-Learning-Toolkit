
from Controller.dataPreProcecing import DataPreProcessor
from Controller.sharedState import SharedState
from sklearn.model_selection import train_test_split
from Controller.dataPreProcecing import DataPreProcessor as PreD
import os


class TrainingProcess():
    def __init__(self,file_path,sharedState):
        self.file_path = file_path
        self.sharedState = sharedState

        # initialize data preprocessor
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..")
        self.csv_file = os.path.join(root_dir, "Data/csv_file.csv")
        self.dataPreProcessor = DataPreProcessor(self.csv_file)


        self.model = None
        self.model_name = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None

        # Evaluation metrics
        self.accuracy = None
        self.classification_report = None
        self.confusion_matrix = None

        
        self.target_column = self.sharedState.target_column
        self.original_data = self.sharedState.get_original_data()
        self.dataPreProcessor.auto_preprocessing()
        self.X = self.dataPreProcessor.df.drop(columns=[self.target_column])
        self.y = self.dataPreProcessor.df[self.target_column]

        self.split_data()


    def split_data(self):
        if self.X.shape[1] > 100:
            self.dataPreProcessor.reduce_features()

        if not self.sharedState.get_has_split():
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        else:
            self.X_train = self.X
            self.y_train = self.y
            self.X_test = self.dataPreProcessor.test_data.drop(columns=[self.target_column])
            self.y_test = self.dataPreProcessor.test_data[self.target_column]


    def choose_best_model(self):
        """
        Chooses the best model based on dataset characteristics and task.

        Parameters:
            task (str): 'regression' or 'classification'.
            data_type (str): 'continuous', 'categorical', or 'mixed'.
            size (str): 'small' or 'large'.
            features (str): 'low' or 'high'.
            balance (str, optional): 'balanced' or 'imbalanced' (only for classification).
        
        Returns:
            list: Recommended models with explanations.
        """
        try :
            task, data_type, size, features, balance= self.sharedState.get_data_info()
        except:
            raise "Data not imported"
        recommendations = []

        # Classification task
        if task == 'classification':
            if data_type == 'continuous':
                if size == 'small':
                    recommendations.append("SVM (works well with continuous, small datasets)")
                else:
                    recommendations.append("Random Forest (robust to continuous data)")

            elif data_type == 'categorical':
                recommendations.append("Naive Bayes (handles categorical data well)")
                if size == 'large':
                    recommendations.append("XGBoost (handles categorical and large datasets well)")

            elif data_type == 'mixed':
                recommendations.append("Random Forest or Gradient Boosting (handles mixed data)")

            # Handle class imbalance
            if balance == 'imbalanced':
                recommendations.append("Random Forest or XGBoost (good for imbalanced data)")
            elif balance == 'balanced':
                recommendations.append("Logistic Regression (effective for balanced data)")

            # High-dimensional feature space
            if features == 'high':
                recommendations.append("SVM (performs well on high-dimensional data)")
            elif features == 'low':
                recommendations.append("Logistic Regression or Naive Bayes (simple for low-dimensional data)")

        # Regression task
        elif task == 'regression':
            if data_type == 'continuous':
                if size == 'small':
                    recommendations.append("Linear Regression (best for small continuous data)")
                else:
                    recommendations.append("Random Forest or Gradient Boosting (effective for large datasets)")

            elif data_type == 'categorical':
                recommendations.append("Tree-based methods (e.g., Decision Tree, Random Forest)")

            elif data_type == 'mixed':
                recommendations.append("Gradient Boosting or Random Forest (handles mixed data well)")

            # High-dimensional feature space
            if features == 'high':
                recommendations.append("Neural Networks (best for high-dimensional regression tasks)")
            elif features == 'low':
                recommendations.append("Linear Regression or Decision Tree (simple for low-dimensional data)")

        # General recommendations
        if size == 'large':
            recommendations.append("Consider Neural Networks for large datasets")
        elif size == 'small':
            recommendations.append("Simple models like Naive Bayes or Logistic Regression for small datasets")

        return list(set(recommendations))  # Return unique suggestions

    # Example usage
    # classification_models = choose_best_model(
    #     task='classification',
    #     data_type='mixed',
    #     size='large',
    #     features='high',
    #     balance='imbalanced'
    # )

    # regression_models = choose_best_model(
    #     task='regression',
    #     data_type='continuous',
    #     size='small',
    #     features='low'
    # )

    # print("Classification Models:", classification_models)
    # print("Regression Models:", regression_models)


        

    def train_model(self,model_name):
        self.model_name = model_name
        match model_name:
            case 'Random Forest':
                from sklearn.ensemble import RandomForestClassifier
                self.model = RandomForestClassifier()
            case 'Decision Tree':
                from sklearn.tree import DecisionTreeClassifier
                self.model = DecisionTreeClassifier()
            case 'Logistic Regression':
                from sklearn.linear_model import LogisticRegression
                self.model = LogisticRegression()
            case 'KNN':
                from sklearn.neighbors import KNeighborsClassifier
                self.model = KNeighborsClassifier()
            case 'SVM':
                from sklearn.svm import SVC
                self.model = SVC()
            case 'Naive Bayes':
                from sklearn.naive_bayes import GaussianNB
                self.model = GaussianNB()
            case 'XGBoost':
                from xgboost import XGBClassifier
                self.model = XGBClassifier()
            case 'LightGBM':
                from lightgbm import LGBMClassifier
                self.model = LGBMClassifier()
            case 'CatBoost':   
                from catboost import CatBoostClassifier
                self.model = CatBoostClassifier()
            case 'clustering':
                from sklearn.cluster import KMeans
                self.model = KMeans(n_clusters=3)
            case 'Linear Regression':
                from sklearn.linear_model import LinearRegression
                self.model = LinearRegression()
            case _:
                print('Invalid model name')
        self.model.fit(self.X_train,self.y_train)
        self.sharedState.set_training_finish(True)


    def predict(self):
        self.y_pred = self.model.predict(self.X_test)

        self.sharedState.set_prediction_finish(True)

    # Evaluate the model with difirent methode 

    def k_fold_cross_validation(self):
        from sklearn.model_selection import cross_val_score
        scores = cross_val_score(self.model, self.X, self.y, cv=10)
        self.sharedState.set_testing_finish(True)
        return scores.mean()
    
    
    def classification_report(self):
        from sklearn.metrics import classification_report
        self.sharedState.set_testing_finish(True)

        return classification_report(self.y_test, self.y_pred)



    def evaluate(self):
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        self.accuracy = accuracy_score(self.y_test, self.y_pred)
        self.classification_report = classification_report(self.y_test, self.y_pred)
        self.confusion_matrix = confusion_matrix(self.y_test, self.y_pred)

        self.sharedState.set_testing_finish(True)

    def run(self):
        self.train_model(self.model_name)
        self.predict()
        self.evaluate()




    

    