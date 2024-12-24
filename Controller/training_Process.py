
from sklearn.model_selection import train_test_split
from tkinter import messagebox
from Controller.dataPreProcecing import DataPreProcessor as PreD

class TrainingProcess():
    def __init__(self,sharedState):
        self.sharedState = sharedState


        self._model = None
        self._model_name = None
        self._X = None
        self._y = None
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None
        self._y_pred = None

        # Evaluation metrics
        self._accuracy = None
        self._classification_report = None
        self._confusion_matrix = None

        
        self._target_column = self.sharedState.get_target_column()
        self._original_data = self.sharedState.get_original_data()
        self._data = self.sharedState.get_data()


        self.best_model=None
        self.model_and_train = {}

    def get_y_test(self):
        return self._y_test
    
    def get_y_pred(self):
        return self._y_pred

    def get_model_name(self):
        return self._model_name

    def set_best_model(self,model_name):
        self.best_model = model_name

    def split_data(self):
        self._data = self.sharedState.get_data()
        self._X = self._data.drop([self.sharedState.get_target_column()] + [col for col in self._data.columns if 'id' in col.lower()], axis=1)
        self._y = self._data[self.sharedState.get_target_column()]


        if not self.sharedState.get_has_split():
            self._X_train, self._X_test, self._y_train, self._y_test = train_test_split(self._X, self._y, test_size=0.2, random_state=42)
        else:
            self._X_train = self._X
            self._y_train = self._y
            process = PreD(sharedState=self.sharedState,file_path=self.sharedState.get_file_path())
            self._X_test = self.sharedState.get_test_data().drop(self.sharedState.get_target_column(), axis=1)
            id_columns = self._X_test.columns[self._X_test.columns.str.contains('id', case=False)]
            if not id_columns.empty:
                self._X_test = self._X_test.drop(id_columns[0], axis=1)
            self._y_test = self.sharedState.get_test_data()[self.sharedState.get_target_column()]
            process.apply_to_test(self.sharedState.get_test_data())
        
        self.sharedState.set_y_test(self._y_test)
        
        return self._X_train, self._X_test, self._y_train, self._y_test

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

        best_model = None

        # Classification task
        if task == 'classification':
            # Main model recommendations
            if data_type == 'continuous':
                if size == 'small':
                    best_model = "SVM"
                else:  # size == 'large'
                    best_model = "Random Forest"
            elif data_type == 'categorical':
                if size == 'small':
                    best_model = "Naive Bayes"
                else:  # size == 'large'
                    best_model = "XGBoost"
            elif data_type == 'mixed':
                best_model = "Random Forest"

            # Adjustments based on class balance
            if balance == 'imbalanced':
                if best_model not in ["XGBoost", "Random Forest"]:
                    best_model = "Random Forest"
            elif balance == 'balanced':
                if best_model not in ["Logistic Regression", "SVM"]:
                    best_model = "Logistic Regression"

            # Adjustments for high-dimensional feature space
            if features == 'high' and best_model != "SVM":
                best_model = "SVM"

        # Regression task
        elif task == 'regression':
            # Main model recommendations
            if data_type == 'continuous':
                if size == 'small':
                    best_model = "Linear Regression"
                else:  # size == 'large'
                    best_model = "Random Forest"
            elif data_type == 'categorical':
                if size == 'small':
                    best_model = "Decision Tree"
                else:  # size == 'large'
                    best_model = "Random Forest"
            elif data_type == 'mixed':
                best_model = "Gradient Boosting"

            # Adjustments for high-dimensional feature space
            if features == 'high' and best_model not in ["LightGBM", "Gradient Boosting"]:
                best_model = "LightGBM"

        # Catch-all for general dataset size recommendations
        if size == 'large' and best_model not in ["Random Forest", "XGBoost", "LightGBM"]:
            best_model = "Random Forest"
        elif size == 'small' and best_model not in ["Decision Tree", "SVM", "Linear Regression"]:
            best_model = "Decision Tree"

        # Handle clustering (if misclassified in task)
        if self.sharedState.get_has_target() == False:
            best_model = "clustering"

        self.set_best_model(best_model)
        return best_model


    def train_model(self,model_name):
        self._model_name = model_name
        self.sharedState.set_model_name(model_name)
        self.split_data()
        probleme = 0
        _,_,_,_,task = self.sharedState.get_data_info()
        try :
            match model_name:
                case 'Random Forest':
                    from sklearn.ensemble import RandomForestClassifier
                    from sklearn.ensemble import RandomForestRegressor
                    if task == 'regression':
                        self._model = RandomForestRegressor()
                    else:
                        self._model = RandomForestClassifier()
                case 'Decision Tree':
                    from sklearn.tree import DecisionTreeClassifier
                    from sklearn.tree import DecisionTreeRegressor
                    if task == 'regression':
                        self._model = DecisionTreeRegressor()
                    else:
                        self._model = DecisionTreeClassifier()
                case 'Logistic Regression':
                    from sklearn.linear_model import LogisticRegression
                    self._model = LogisticRegression()
                case 'KNN':
                    from sklearn.neighbors import KNeighborsClassifier
                    self._model = KNeighborsClassifier()
                case 'SVM':
                    from sklearn.svm import SVC
                    self._model = SVC()
                case 'Naive Bayes':
                    from sklearn.naive_bayes import GaussianNB
                    self._model = GaussianNB()
                case 'XGBoost':
                    from xgboost import XGBClassifier
                    from xgboost import XGBRegressor
                    if task == 'regression':
                        self._model = XGBRegressor()
                    else:
                        self._model = XGBClassifier()
                case 'LightGBM':
                    from lightgbm import LGBMClassifier
                    from lightgbm import LGBMRegressor
                    if task == 'regression':
                        self._model = LGBMRegressor()
                    else:
                        self._model = LGBMClassifier()
                case 'clustering':
                    from sklearn.cluster import KMeans
                    self._model = KMeans(n_clusters=3)
                    # get labels
                    self.sharedState.set_labels(self._model.fit_predict(self._X))
                case 'Linear Regression':
                    from sklearn.linear_model import LinearRegression
                    self._model = LinearRegression()
                case 'SVR':
                    from sklearn.svm import SVR
                    self._model = SVR()
                case 'Auto Model Selection':
                    best_model = self.choose_best_model()
                    self.train_model(best_model)
                case _:
                    print('Invalid model name')
            print("PetalWidthCm" in self._X_train.columns)
            print(self._X_train.columns)
            self._model.fit(self._X_train,self._y_train)
            self.sharedState.set_model(self._model)
            self.model_and_train[model_name] = self._model
        except Exception as e:
            probleme = 1
            messagebox.showerror("Error", f"An error occurred during training: {str(e)}")


        if probleme == 0 and not model_name == 'Auto Model Selection':
            messagebox.showinfo("Training Complete", f"Model '{model_name}' has been successfully trained!")
        self.sharedState.set_training_finish(True)
        print("Model Trained")
        return probleme


    def predict(self,data = None):
        if data is not None:
            process = PreD(sharedState=self.sharedState,file_path=self.sharedState.get_file_path())
            self.sharedState.set_test_new_data(data)
            X_test = self.sharedState.get_test_new_data()
            if 'id' in [col.lower() for col in X_test.columns]:
                X_test.drop(columns=[col for col in X_test.columns if col.lower() == 'id'], inplace=True)
                self.sharedState.set_test_new_data(X_test)
            
            example = process.apply_to_test(self.sharedState.get_test_new_data(),sample = True)

        test = example if data is not None else self._X_test
        # Remove id column from X_test if it exists
        # Ensure the test data has the same feature names as the training data
        if data is not None:
            test = test[self._X_test.columns]
            print(test)
        
        y_pred = [round(pred, 2) for pred in self._model.predict(test)] 

        if data is None:
            self._y_pred = y_pred
            self.sharedState.set_y_pred(self._y_pred)
        self.sharedState.set_prediction_finish(True)

        return y_pred

    # Evaluate the model with difirent methode 

    def k_fold_cross_validation(self):
        from sklearn.model_selection import cross_val_score
        scores = cross_val_score(self._model, self._X, self._y, cv=10)
        self.sharedState.set_testing_finish(True)
        return scores.mean()
    
    
    def classification_report(self):
        """
        Generate and return a structured classification report as a dictionary.
        """
        from sklearn.metrics import classification_report

        # Ensure y_test and y_pred exist and are not None
        if self._y_test is None or self._y_pred is None:
            raise ValueError("y_test or y_pred is not defined. Ensure the model has been trained and tested.")

        try:
            # Generate the classification report as a dictionary
            report = classification_report(self._y_test, self._y_pred, output_dict=True)

            # Set a flag indicating the testing process has finished
            self.sharedState.set_testing_finish(True)

            # Return the structured report
            return report

        except Exception as e:
            raise ValueError(f"Error generating classification report: {str(e)}")


    def evaluate(self):
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        self._accuracy = accuracy_score(self._y_test, self._y_pred)
        self._classification_report = classification_report(self._y_test, self._y_pred)
        self._confusion_matrix = confusion_matrix(self._y_test, self._y_pred)

        self.sharedState.set_testing_finish(True)

    def run(self):
        self.train_model(self._model_name)
        self.predict()
        self.evaluate()

  