
from sklearn.model_selection import train_test_split
from tkinter import messagebox
from Controller.dataPreProcecing import DataPreProcessor as PreD

class TrainingProcess():
    def __init__(self,sharedState):
        self.sharedState = sharedState


        self.model = None
        self.model_name = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None

        # Evaluation metrics
        self.accuracy = None
        self.classification_report = None
        self.confusion_matrix = None

        
        self.target_column = self.sharedState.get_target_column()
        self.original_data = self.sharedState.get_original_data()
        self.data = self.sharedState.get_data()


        self.best_model=None
        self.model_and_train = {}

    def get_y_test(self):
        return self.y_test
    
    def get_y_pred(self):
        return self.y_pred

    def get_model_name(self):
        return self.model_name

    def set_best_model(self,model_name):
        self.best_model = model_name

    def split_data(self):
        self.data= self.sharedState.get_data()
        self.X = self.data.drop(self.sharedState.get_target_column(), axis=1)
        self.y = self.data[self.sharedState.get_target_column()]


        #if id column exist drop it
        id_columns = self.X.columns[self.X.columns.str.contains('id', case=False)]
        if not id_columns.empty:
            self.X = self.X.drop(id_columns[0], axis=1)


        if not self.sharedState.get_has_split():
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        else:
            self.X_train = self.X
            self.y_train = self.y
            process = PreD(sharedState=self.sharedState,file_path=self.sharedState.get_file_path())
            self.X_test = self.sharedState.get_test_data().drop(self.sharedState.get_target_column(), axis=1)
            id_columns = self.X_test.columns[self.X_test.columns.str.contains('id', case=False)]
            if not id_columns.empty:
                self.X_test = self.X_test.drop(id_columns[0], axis=1)
            self.y_test = self.sharedState.get_test_data()[self.sharedState.get_target_column()]
            process.apply_to_test(self.sharedState.get_test_data())
        
        self.sharedState.set_y_test(self.y_test)
        
        return self.X_train, self.X_test, self.y_train, self.y_test

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
            str: The best recommended model based on dataset characteristics.
        """
        try:
            task, data_type, size, features, balance = self.sharedState.get_data_info()
        except:
            raise ValueError("Data not imported")

        # Default best model initialization
        best_model = None

        # Classification task
        if task == 'classification':
            # Priority rules for classification
            if data_type == 'continuous':
                if size == 'small':
                    best_model = "SVM"  # Small dataset with continuous data, use SVM
                else:
                    best_model = "Random Forest"  # Large dataset with continuous data, use Random Forest

            elif data_type == 'categorical':
                best_model = "Naive Bayes"  # Categorical data, Naive Bayes
                if size == 'large':
                    best_model = "XGBoost"  # For large datasets with categorical data, prefer XGBoost

            elif data_type == 'mixed':
                best_model = "Random Forest"  # Mixed data type, prefer Random Forest

            # Handle class imbalance
            if balance == 'imbalanced' and best_model != "XGBoost":
                best_model = "Random Forest"  # For imbalanced classes, use Random Forest
            elif balance == 'balanced' and best_model != "Logistic Regression":
                best_model = "Logistic Regression"  # For balanced classes, prefer Logistic Regression

            # High-dimensional feature space
            if features == 'high' and best_model != "SVM":
                best_model = "SVM"  # For high-dimensional data, use SVM
            elif features == 'low' and best_model != "Logistic Regression":
                best_model = "Logistic Regression"  # For low-dimensional data, use Logistic Regression

        # Regression task
        elif task == 'regression':
            # Priority rules for regression
            if data_type == 'continuous':
                if size == 'small':
                    best_model = "Linear Regression"  # Small dataset with continuous data, use Linear Regression
                else:
                    best_model = "Random Forest"  # Large dataset with continuous data, use Random Forest

            elif data_type == 'categorical':
                best_model = "Decision Tree"  # Categorical data for regression, Decision Tree
                if size == 'large':
                    best_model = "Random Forest"  # For large datasets with categorical data, prefer Random Forest

            elif data_type == 'mixed':
                best_model = "Gradient Boosting"  # Mixed data type for regression, prefer Gradient Boosting

            # High-dimensional feature space
            if features == 'high' and best_model != "LightGBM":
                best_model = "LightGBM"  # For high-dimensional data, use LightGBM
            elif features == 'low' and best_model != "Linear Regression":
                best_model = "Linear Regression"  # For low-dimensional data, use Linear Regression

        # General model recommendations based on size
        if size == 'large' and best_model != "Random Forest":
            best_model = "Random Forest"  # For large datasets, prefer Random Forest
        elif size == 'small' and best_model != "Decision Tree":
            best_model = "Decision Tree"  # For small datasets, prefer Decision Tree
        
        if task == 'clustering':
            best_model = "clustering"

        self.set_best_model(best_model)
        return best_model  # Return the single best model

        

    def train_model(self,model_name):
        self.model_name = model_name
        self.sharedState.set_model_name(model_name)
        self.split_data()
        probleme = 0
        try :
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
                case 'clustering':
                    from sklearn.cluster import KMeans
                    self.model = KMeans(n_clusters=3)
                    # get labels
                    self.sharedState.set_labels(self.model.fit_predict(self.X))
                case 'Linear Regression':
                    from sklearn.linear_model import LinearRegression
                    self.model = LinearRegression()
                case 'SVR':
                    from sklearn.svm import SVR
                    self.model = SVR()
                case 'Auto Model Selection':
                    best_model = self.choose_best_model()
                    self.train_model(best_model)
                case _:
                    print('Invalid model name')
            self.model.fit(self.X_train,self.y_train)
            self.model_and_train[model_name] = self.model
        except Exception as e:
            probleme = 1
            messagebox.showerror("Error", f"An error occurred during training: {str(e)}")


        if probleme == 0 and not model_name == 'Auto Model Selection':
            messagebox.showinfo("Training Complete", f"Model '{model_name}' has been successfully trained!")
        self.sharedState.set_training_finish(True)
        print("Model Trained")
        return probleme


    def predict(self):
        # Remove id column from X_test if it exists
        self.y_pred = self.model.predict(self.X_test)
        
        self.sharedState.set_y_pred(self.y_pred)
        self.sharedState.set_prediction_finish(True)

    # Evaluate the model with difirent methode 

    def k_fold_cross_validation(self):
        from sklearn.model_selection import cross_val_score
        scores = cross_val_score(self.model, self.X, self.y, cv=10)
        self.sharedState.set_testing_finish(True)
        return scores.mean()
    
    
    def classification_report(self):
        """
        Generate and return a structured classification report as a dictionary.
        """
        from sklearn.metrics import classification_report

        # Ensure y_test and y_pred exist and are not None
        if self.y_test is None or self.y_pred is None:
            raise ValueError("y_test or y_pred is not defined. Ensure the model has been trained and tested.")

        try:
            # Generate the classification report as a dictionary
            report = classification_report(self.y_test, self.y_pred, output_dict=True)

            # Set a flag indicating the testing process has finished
            self.sharedState.set_testing_finish(True)

            # Return the structured report
            return report

        except Exception as e:
            raise ValueError(f"Error generating classification report: {str(e)}")


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




    

    