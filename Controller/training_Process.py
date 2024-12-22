
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
        self.data = self.sharedState.get_data().copy()
        self.X = self.data.drop([self.sharedState.get_target_column()] + [col for col in self.data.columns if 'id' in col.lower()], axis=1)
        self.y = self.data[self.sharedState.get_target_column()]


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
        self.model_name = model_name
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
                        self.model = RandomForestRegressor()
                    else:
                        self.model = RandomForestClassifier()
                case 'Decision Tree':
                    from sklearn.tree import DecisionTreeClassifier
                    from sklearn.tree import DecisionTreeRegressor
                    if task == 'regression':
                        self.model = DecisionTreeRegressor()
                    else:
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
                    from xgboost import XGBRegressor
                    if task == 'regression':
                        self.model = XGBRegressor()
                    else:
                        self.model = XGBClassifier()
                case 'LightGBM':
                    from lightgbm import LGBMClassifier
                    from lightgbm import LGBMRegressor
                    if task == 'regression':
                        self.model = LGBMRegressor()
                    else:
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
            print("PetalWidthCm" in self.X_train.columns)
            print(self.X_train.columns)
            self.model.fit(self.X_train,self.y_train)
            self.sharedState.set_model(self.model)
            self.model_and_train[model_name] = self.model
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

        test = example if data is not None else self.X_test
        # Remove id column from X_test if it exists
        # Ensure the test data has the same feature names as the training data
        if data is not None:
            test = test[self.X_test.columns]
            print(test)
        
        if data is None:
            self.y_pred = self.model.predict(test)
            y_pred = self.y_pred
            self.sharedState.set_y_pred(self.y_pred)
        else:
            y_pred = self.model.predict(test)
        self.sharedState.set_prediction_finish(True)

        return y_pred

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

    # def predict_sample(self,sample):
    #     """
    #     Predict the target value for a sample input.
    #     """
    #     # Ensure the model has been trained
    #     if self.model is None:
    #         raise ValueError("Model has not been trained. Please train the model before making predictions.")
    #     process = PreD(sharedState=self.sharedState,file_path=self.sharedState.get_file_path())
    #     self.sharedState.set_test_new_data(sample)
    #     X_test = self.sharedState.get_test_new_data()
    #     if 'id' in [col.lower() for col in X_test.columns]:
    #         X_test.drop(columns=[col for col in X_test.columns if col.lower() == 'id'], inplace=True)
    #         self.sharedState.set_test_new_data(X_test)
        
    #     example = process.apply_to_test(self.sharedState.get_test_new_data(),sample = True)
    #     print(example)
        
    #    # sample is pdframe
    #     pred = self.model.predict(example)
    #     return pred