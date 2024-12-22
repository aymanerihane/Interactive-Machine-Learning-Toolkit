import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from Controller.sharedState import SharedState
import os

class DataPreProcessor:
    
    def __init__(self, file_path = None ,sharedState = None, just_for_method_use = False):
        if sharedState is None:
            print("shared state is none")
            self.sharedState = SharedState()

        else:
            self.sharedState = sharedState
        if not just_for_method_use:
            self.df = pd.read_csv(file_path)
            self.sharedState.set_data(self.df,first = True)



            try:
                self.sharedState.set_file_uploaded(True)
                self.set_data_info()
                
            except FileNotFoundError:
                raise FileNotFoundError(f"CSV file not found at: {file_path}")
        
        # Initialize the preprocessing steps
        self.imputer = SimpleImputer(strategy="most_frequent")  # For missing categorical data
        self.num_imputer = SimpleImputer(strategy="mean")  # For missing numerical data
        self.label_encoder = LabelEncoder()  # For label encoding categorical variables
        self.scaler = StandardScaler()  # For scaling numerical data
        self.onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)  # For one-hot encoding
        self.tfidf_vectorizer = TfidfVectorizer()  # For text data



    def set_data(self,data):
        self.df = data
        self.set_data_info()
        self.sharedState.set_data(self.df)

    def set_data_stats(self,refresh_data_stats,refreach = True):
        """
        Set the data statistics in the shared state.
        """
        nan_values = self.df.isnull().sum().sum()
        missing_values = self.df.isna().sum().sum()
        num_classes = len(self.df[self.sharedState.target_culumn].unique()) if self.sharedState.target_culumn is not None else 0
        data_shape = self.df.shape
        num_categorical_cols = self.df.select_dtypes(include=['object']).shape[1]
        num_numerical_cols = self.df.select_dtypes(include=['float64', 'int64','int32']).shape[1]
        balanced = 'Yes' if num_classes > 1 and self.df[self.sharedState.target_culumn].value_counts(normalize=True).min() > 0.05 else 'No'
        

        #find duplicate columns number
        duplicate_columns = self.df.columns.duplicated().sum()
        print("Data stats set")
        print("Nan values: ", nan_values, "Missing values: ", missing_values, "Number of classes: ", num_classes, "Data shape: ", data_shape, "Number of categorical columns: ", num_categorical_cols, "Number of numerical columns: ", num_numerical_cols, duplicate_columns)

        self.sharedState.set_data_stats(nan_values, missing_values, num_classes, data_shape,balanced, num_categorical_cols, num_numerical_cols,duplicate_columns)

        if refreach:
            refresh_data_stats()

    def reduce_features(self, threshold=0.9,data = None):
        """
        Reduce the number of features using correlation.
        """
        df = data.copy() if data is not None else self.df.copy()
        # Calculate the correlation matrix
        corr_matrix = df.corr().abs()
        
        # Select upper triangle of correlation matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        
        # Find index of feature columns with correlation greater than threshold
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
        
        # Drop features
        df.drop(columns=to_drop, inplace=True)
        self.sharedState.set_preprocessing_finish(True)
        if data is None:
            self.sharedState.set_data(df)

        return df


    
    
    def clean_data(self,data = None):
        """
        Clean missing values in numerical and categorical columns.

        """
        df = data.copy() if data is not None else self.df.copy()
        if 'id' in [col.lower() for col in df.columns]:
            df.drop(columns=[col for col in df.columns if col.lower() == 'id'], inplace=True)
        # Categorical columns
        for column in df.select_dtypes(include=['object']).columns:
            df[column] = self.imputer.fit_transform(self.df[column].values.reshape(-1, 1)).ravel()
        
        # Numerical columns
        for column in self.df.select_dtypes(include=['number']).columns:
            df[column] = self.num_imputer.fit_transform(self.df[column].values.reshape(-1, 1))
        
        if data is None:
            self.sharedState.set_data(df)
            self.sharedState.set_preprocessing_finish(True)

        return df

    def scale_data(self,data=None):
        """
        Apply scaling to numerical columns.
        """
        df = data.copy() if data is not None else self.df.copy()
        
        num_cols = df.select_dtypes(include=['float64', 'int64','int32']).columns
        if len(num_cols) > 0:
            self.scaler.fit_transform(df[num_cols])
        
        if data is None:
            self.sharedState.set_data(self.df)
        self.sharedState.set_preprocessing_finish(True)


        return df

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

    def label_encode(self,data=None):
        """
        Apply label encoding to categorical columns.
        """
        df = data.copy() if data is not None else self.df
        cat_cols = df.select_dtypes(include=['object']).columns
        print(cat_cols)
        for col in cat_cols:
            df[col] = self.label_encoder.fit_transform(df[col])
        
        if data is None:
            self.sharedState.set_data(df)

        self.sharedState.set_preprocessing_finish(True)
        return df
    
    def apply_to_test(self, test_df,sample = False):
        if 'id' in [col.lower() for col in test_df.columns]:
            test_df.drop(columns=[col for col in test_df.columns if col.lower() == 'id'], inplace=True)
        test_df_copy = test_df.copy()
        if not sample : 
            self.sharedState.set_test_data(test_df)
        else :
            self.sharedState.set_test_new_data(test_df)

        print("process_done: ", self.sharedState.get_process_done())
        for process in self.sharedState.get_process_done():
            match process:
                case "Scale Data":
                    test_df = self.scale_data(data=test_df)
                    print("test after scale",test_df)
                case "Label Encode":
                    test_df = self.label_encode(data=test_df)
                    print("test after label",test_df)
                case "Handle Dates":
                    test_df = self.handle_dates(data=test_df)
                    print("test after dates",test_df)
                case "Reduce Features":
                    test_df = self.reduce_features(data=test_df)
                    print("test after reduce",test_df)
                case "Transform Skewed Features":
                    test_df = self.transform_skewed_features(data=test_df)
                    print("test after skewed",test_df)
                case "Standardize Data Types":
                    test_df = self.standardize_data_types(data=test_df)
                    print("test after stand",test_df)
                case "Binarize Target":
                    test_df = self.binarize_target(data=test_df)
                case "Apply Feature Augmentation":
                    test_df = self.apply_feature_augmentation(data=test_df,ignore_target=True)
                case "Reset":
                    test_df = test_df_copy
                case _:
                    print(process)
        
        target_col = target_col = self.sharedState.get_target_column()
        # Sort columns by name, ensuring the target column is last
        if sample :
            cols = sorted([col for col in test_df.columns if col != target_col]) 
        else:
            cols = sorted([col for col in test_df.columns if col != target_col]) + [target_col]
        test_df = test_df[cols]

        if not sample:
            self.sharedState.set_test_data(test_df)
        else :
            self.sharedState.set_test_new_data(test_df)

        print("test: ",test_df)
        return test_df

    def handle_dates(self,data=None):
        """
        Convert date columns to datetime and extract features like day, month, year.
        """
        df = data.copy() if data is not None else self.df.copy()
        date_cols = df.select_dtypes(include=['object']).columns
        for col in date_cols:
            try:
                # Try to convert to datetime
                df[col] = pd.to_datetime(self.df[col], errors='coerce')
                # Extract date features
                df[col + '_day'] = df[col].dt.day
                df[col + '_month'] = df[col].dt.month
                df[col + '_year'] = df[col].dt.year
                df[col + '_weekday'] = df[col].dt.weekday
                df.drop(columns=[col], inplace=True)  # Drop original date column
            except:
                continue  # If not a valid date, skip
        if data is None:
            self.sharedState.set_data(df)
        self.sharedState.set_preprocessing_finish(True)
        return df

    def process_text(self,data=None):
        """
        Apply TF-IDF vectorization to textual data.
        """
        df = data.copy() if data is not None else self.df.copy()
        text_column = df.select_dtypes(include=['object']).columns[0]
        if text_column in df.columns:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(df[text_column])
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=self.tfidf_vectorizer.get_feature_names_out())
            df = df.drop(text_column, axis=1).join(tfidf_df)
        if data is None:
            self.sharedState.set_data(df)
        self.sharedState.set_preprocessing_finish(True)
        return df

    def set_data_info(self):
        """task (str): 'regression' or 'classification'.
            data_type (str): 'continuous', 'categorical', or 'mixed'.
            size (str): 'small' or 'large'.
            features (str): 'low' or 'high'.
            balance (str, optional): 'balanced' or 'imbalanced' (only for classification).
            """
        #find the task using the target column
        try:
            if self.sharedState.get_has_target():
                if self.df[self.sharedState.get_target_column()].dtype == 'object' or len(self.df[self.sharedState.get_target_column()].unique()) < 10 :
                    task = 'classification'    
                else:
                    task = 'regression'
            else:
                task = "clustering"
        except ValueError:
            raise ValueError("Target column not found")
            
            

        print("Task: ", task)

        
        
        #find the data type
        if self.df.select_dtypes(include=['object']).shape[1] == self.df.shape[1]:
            type = 'categorical'
        elif self.df.select_dtypes(include=['float64', 'int64']).shape[1] == self.df.shape[1]:
            type = 'continuous'
        else:
            type = 'mixed'

        #find the size of the data
        if self.df.shape[0] < 1000:
            size = 'small'
        else:
            size = 'large'

        #find the number of features
        if self.df.shape[1] < 50:
            features = 'low'
        else:
            features = 'high'   

        #find the balance of the data
        if task == 'classification':
            if self.df[self.sharedState.get_target_column()].value_counts(normalize=True).min() < 0.05:
                balance = 'imbalanced'
            else:
                balance = 'balanced'
        else:
            balance = None

        


        self.sharedState.set_data_info(task, type, size, features, balance)
        print("Data info set")
        print("Task: ", task, "Type: ", type, "Size: ", size, "Features: ", features, "Balance: ", balance,)

    # auto preprocess methods
    def auto_preprocessing(self, data=None):
        """
        Automatically apply the best preprocessing steps based on dataset characteristics.
        """

        # delete id column if it exists
        target_col = self.sharedState.get_target_column()
        if 'id' in [col.lower() for col in self.df.columns]:
            # Drop the 'id' column (case-insensitive) and the target column
            self.df.drop(columns=[col for col in self.df.columns if col.lower() == 'id'], inplace=True)

            self.sharedState.set_data(self.df)

        self.unique_categorical_values = self.get_unique_categorical_values()
        # Retrieve dataset characteristics
        data_type, balance, _, features, task = self.sharedState.get_data_info()
        print("Data type: ", data_type, "Balance: ", balance, "Features: ", features, "Task: ", task)

        applied_steps = []

        # Step 1: Handle missing values
        applied_steps.append("Handling missing values")
        self.clean_data(data)

        # Step 2: Handle data type-specific preprocessing
        if data_type == 'categorical':
            applied_steps.append("Applying label encoding for categorical data")
            self.df = self.label_encode(data)
            self.sharedState.add_process("Label Encode")
        elif data_type == 'continuous':
            applied_steps.append("Scaling numerical data")
            self.scale_data(data)
            
            self.sharedState.add_process("Scale Data")
        elif data_type == 'mixed':
            applied_steps.append("Scaling numerical data and encoding categorical data")
            self.scale_data(data)
            self.df = self.label_encode(data)
            self.sharedState.add_process("Scale Data")
            self.sharedState.add_process("Label Encode")

        # Step 3: Feature count considerations
        if features == 'high':
            applied_steps.append("Applying feature selection or dimensionality reduction")
            self.reduce_features(threshold=0.85)
            self.sharedState.add_process("Reduce Features")
        elif features == 'low':
            applied_steps.append("Applying feature augmentation")
            self.df = self.apply_feature_augmentation(data)
            self.sharedState.add_process("Apply Feature Augmentation")

        # Step 4: Handle imbalanced data (only for classification)
        if task == 'classification' and balance == 'imbalanced':
            applied_steps.append("Balancing classes (e.g., using SMOTE or class weighting)")
            self.df = self.balance_classes(data)
            
            self.sharedState.add_process("Balance Classes")

        # Step 5: Handle outliers (only for continuous features)
        if data_type in ['continuous', 'mixed']:
            applied_steps.append("Handling outliers (IQR)")
            self.df = self.handle_outliers(data)
            
            self.sharedState.add_process("Handle Outliers")

        # Step 6: Task-specific preprocessing
        if task == 'classification':
            # Binarizing target column for binary classification tasks
            if len(self.sharedState.get_original_data()[self.sharedState.get_target_column()].unique()) == 2:
                applied_steps.append("Binarizing target column for binary classification")
                self.df = self.binarize_target(data)  # Only binarize if necessary
                
                self.sharedState.add_process("Binarize Target")
        elif task == 'regression':
            applied_steps.append("Applying log transformation for skewed continuous features")
            self.df = self.transform_skewed_features(data)
            
            self.sharedState.add_process("Transform Skewed Features")

        # Step 7: General preprocessing
        applied_steps.append("Removing duplicate rows")
        self.df.drop_duplicates(inplace=True)
        self.sharedState.add_process("Remove Duplicates")
        applied_steps.append("Checking and standardizing data types")
        self.standardize_data_types(data)
        self.sharedState.add_process("Standardize Data Types")

        print("Applied preprocessing steps:")
        for step in applied_steps:
            print(f"- {step}")

        # Add the target column back to the dataframe if it was removed for processing
        target_col = self.sharedState.get_target_column()

        # Sort columns by name, ensuring the target column is last
        cols = sorted([col for col in self.df.columns if col != target_col]) + [target_col]
        self.df = self.df[cols]
        self.sharedState.add_process("Sorted")
        
        self.sharedState.set_data(self.df)
        self.sharedState.set_preprocessing_finish(True)
        return self.df, self.unique_categorical_values

    def apply_feature_augmentation(self,data=None,ignore_target = False):
        """
        Apply feature augmentation for low feature count datasets.
        """
        df = data.copy() if data is not None else self.df.copy()

        if not ignore_target:
            target_data = df[self.sharedState.get_target_column()]
            # Drop the target column
            df.drop(columns=[self.sharedState.get_target_column()], inplace=True)
        # Add polynomial features
        poly_features = df.select_dtypes(include=['float64', 'int64','int32']).columns
        for col in poly_features:
            df[col + '_squared'] = df[col] ** 2
            df[col + '_cubed'] = df[col] ** 3
        
        # Add the target column back to the dataframe
        if not ignore_target:

            df[self.sharedState.get_target_column()] = target_data
        
        if data is None:
            self.sharedState.set_data(df)

        self.sharedState.set_preprocessing_finish(True)
        return df
    
    def balance_classes(self,data=None):
        """
        Balance imbalanced classes using SMOTE.
        """
        from imblearn.over_sampling import SMOTE
        
        df = data.copy() if data is not None else self.df.copy()
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(df.drop(columns=[self.get]), df[self.sharedState.get_target_column()])
        df = pd.concat([X_resampled, y_resampled], axis=1)

        if data is None:
            self.sharedState.set_data(df)
        self.sharedState.set_preprocessing_finish(True)
        return df
    
    def handle_outliers(self,data = None):
        """
        Handle outliers in numerical columns using the IQR method.
        """
        df = data.copy() if data is not None else self.df.copy()
        num_cols = self.get_numerical_columns(data=df)
        for col in num_cols:
            if 'id' == col.lower():
                num_cols.remove(col)

        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[col] = np.where(df[col] < lower_bound, lower_bound,df[col])
            df[col] = np.where(df[col] > upper_bound, upper_bound,df[col])

        if data is None:
            self.sharedState.set_data(df)
        self.sharedState.set_preprocessing_finish(True)
        return df

    def transform_skewed_features(self,data=None):
        """
        Apply log transformation to skewed numerical columns.
        """
        df = data.copy() if data is not None else self.df.copy()
        num_cols = self.get_numerical_columns(data = df)
        for col in num_cols:
            if df[col].skew() > 1:  # Check if skewness > 1 (highly skewed)
                df[col] = np.log1p(df[col])  # Apply log(1+x) transformation

        if data is None:
            self.sharedState.set_data(df)
        self.sharedState.set_preprocessing_finish(True)
        return df
    
    def standardize_data_types(self,data=None):
        """
        Ensure all columns have appropriate data types.
        """
        df = data.copy() if data is not None else self.df.copy()
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype('string')  # Standardize text columns as 'string'
            elif df[col].dtype in ['float64', 'int64','int32']:
                df[col] = df[col].astype('float64')  # Standardize numerical columns as 'float64'
        if data is None:
            self.sharedState.set_data(df)
        self.sharedState.set_preprocessing_finish(True)
        return df

    def get_numerical_columns(self,data = None):
        """
        Get the names of numerical columns in the dataset.
        """
        df = data.copy() if data is not None else self.df.copy()
        return df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def binarize_target(self,data=None):
        """
        Binarize the target column for binary classification tasks.
        """
        df = data.copy() if data is not None else self.df.copy()

        if data is None:
            target_col = self.sharedState.get_target_column()
            df[target_col] = df[target_col].apply(lambda x: 1 if x == df[target_col].mode()[0] else 0)
            self.sharedState.set_data(df)

        self.sharedState.set_preprocessing_finish(True)
        return df
    
    def reset(self):
        self.sharedState.set_data(self.sharedState.get_original_data())
        self.df = self.sharedState.get_original_data().copy()
        self.sharedState.set_preprocessing_finish(False)
        self.sharedState.set_new_process()
        self.sharedState.add_process("Reset")
        print("## Data reset")