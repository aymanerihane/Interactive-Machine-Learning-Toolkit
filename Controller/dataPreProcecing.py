import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from Controller.sharedState import SharedState

class DataPreProcessor:
    
    def __init__(self, file_path,sharedState = None):
        if sharedState is None:
            print("shared state is none")
            self.sharedState = SharedState()

        else:
            self.sharedState = sharedState
        self.df = pd.read_csv(file_path)
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



    def set_original_data(self):
        self.sharedState.set_original_data(self.df)


    def set_data(self):
        self.sharedState.set_data(self.df)

    def set_data_stats(self,refresh_data_stats):
        """
        Set the data statistics in the shared state.
        """
        nan_values = self.df.isnull().sum().sum()
        missing_values = self.df.isna().sum().sum()
        num_classes = len(self.df[self.sharedState.target_culumn].unique()) if self.sharedState.target_culumn is not None else 0
        data_shape = self.df.shape
        num_categorical_cols = self.df.select_dtypes(include=['object']).shape[1]
        num_numerical_cols = self.df.select_dtypes(include=['float64', 'int64']).shape[1]
        balanced = 'Yes' if num_classes > 1 and self.df[self.sharedState.target_culumn].value_counts(normalize=True).min() > 0.05 else 'No'
        
        self.sharedState.set_data_stats(nan_values, missing_values, num_classes, data_shape,balanced, num_categorical_cols, num_numerical_cols)
        print("Data stats set")
        print("Nan values: ", nan_values, "Missing values: ", missing_values, "Number of classes: ", num_classes, "Data shape: ", data_shape, "Number of categorical columns: ", num_categorical_cols, "Number of numerical columns: ", num_numerical_cols)

        refresh_data_stats()

    def reduce_features(self, threshold=0.9):
        """
        Reduce the number of features using correlation.
        """
        # Calculate the correlation matrix
        corr_matrix = self.df.corr().abs()
        
        # Select upper triangle of correlation matrix
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        
        # Find index of feature columns with correlation greater than threshold
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
        
        # Drop features
        self.df.drop(columns=to_drop, inplace=True)
        
        return self.df


    
    
    def clean_data(self):
        """
        Clean missing values in numerical and categorical columns.

        """
        # Categorical columns
        for column in self.df.select_dtypes(include=['object']).columns:
            self.df[column] = self.imputer.fit_transform(self.df[column].values.reshape(-1, 1)).ravel()
        
        # Numerical columns
        for column in self.df.select_dtypes(include=['number']).columns:
            self.df[column] = self.num_imputer.fit_transform(self.df[column].values.reshape(-1, 1))
        
        self.sharedState.set_data(self.df)
        return self.df

    def scale_data(self):
        """
        Apply scaling to numerical columns.
        """
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if len(num_cols) > 0:
            self.df[num_cols] = self.scaler.fit_transform(self.df[num_cols])
        
        self.sharedState.set_data(self.df)

        return self.df


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

    def label_encode(self):
        """
        Apply label encoding to categorical columns.
        """
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            self.df[col] = self.label_encoder.fit_transform(self.df[col])
        
        self.sharedState.set_data(self.df)

        return self.df

    def handle_dates(self):
        """
        Convert date columns to datetime and extract features like day, month, year.
        """
        date_cols = self.df.select_dtypes(include=['object']).columns
        for col in date_cols:
            try:
                # Try to convert to datetime
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                # Extract date features
                self.df[col + '_day'] = self.df[col].dt.day
                self.df[col + '_month'] = self.df[col].dt.month
                self.df[col + '_year'] = self.df[col].dt.year
                self.df[col + '_weekday'] = self.df[col].dt.weekday
                self.df.drop(columns=[col], inplace=True)  # Drop original date column
            except:
                continue  # If not a valid date, skip
        self.sharedState.set_data(self.df)
        return self.df

    def process_text(self, text_column):
        """
        Apply TF-IDF vectorization to textual data.
        """
        if text_column in self.df.columns:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df[text_column])
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=self.tfidf_vectorizer.get_feature_names_out())
            self.df = self.df.drop(text_column, axis=1).join(tfidf_df)
        self.sharedState.set_data(self.df)
        return self.df

    def set_data_info(self):
        """task (str): 'regression' or 'classification'.
            data_type (str): 'continuous', 'categorical', or 'mixed'.
            size (str): 'small' or 'large'.
            features (str): 'low' or 'high'.
            balance (str, optional): 'balanced' or 'imbalanced' (only for classification).
            """
        #find the task using the target column
        if self.sharedState.get_target_column() is not None:
            if self.df[self.sharedState.get_target_column()].dtype == 'object' or len(self.df[self.sharedState.get_target_column()].unique()) < 10:
                task = 'classification'    
            else:
                task = 'regression'
        else:
            task = None

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
        print("Task: ", task, "Type: ", type, "Size: ", size, "Features: ", features, "Balance: ", balance)

    # auto preprocess methods
    def auto_preprocessing(self):
        """
        Automatically apply the best preprocessing steps based on dataset characteristics.
        """

        # delete id column if exisct
        if 'id' in [col.lower() for col in self.df.columns]:
            self.df.drop(columns=[col for col in self.df.columns if col.lower() == 'id'], inplace=True)

        self.unique_categorical_values = self.get_unique_categorical_values()
        # Retrieve dataset characteristics
        data_type, balance, _, features, task = self.sharedState.get_data_info()
        print("Data type: ", data_type, "Balance: ", balance, "Features: ", features, "Task: ", task)

        applied_steps = []

        # Step 1: Handle missing values
        applied_steps.append("Handling missing values")
        self.clean_data()

        # Step 2: Handle data type-specific preprocessing
        if data_type == 'categorical':
            applied_steps.append("Applying label encoding for categorical data")
            self.df = self.label_encode()
        elif data_type == 'continuous':
            applied_steps.append("Scaling numerical data")
            self.scale_data()
        elif data_type == 'mixed':
            applied_steps.append("Scaling numerical data and encoding categorical data")
            self.scale_data()
            self.df = self.label_encode()

        # Step 3: Feature count considerations
        if features == 'high':
            applied_steps.append("Applying feature selection or dimensionality reduction")
            self.reduce_features(threshold=0.85)
        elif features == 'low':
            applied_steps.append("Applying feature augmentation")
            self.df = self.apply_feature_augmentation()

        # Step 4: Handle imbalanced data (only for classification)
        if task == 'classification' and balance == 'imbalanced':
            applied_steps.append("Balancing classes (e.g., using SMOTE or class weighting)")
            self.df = self.balance_classes()

        # Step 5: Handle outliers (only for continuous features)
        if data_type in ['continuous', 'mixed']:
            applied_steps.append("Handling outliers IQR)")
            self.df = self.handle_outliers()

        # Step 6: Task-specific preprocessing
        if task == 'classification':
            applied_steps.append("Binarizing target column for binary classification tasks")
            target = self.sharedState.get_target_column()   
            if len(self.df[target].unique()) == 2:
                print('intred')
                self.df = self.binarize_target()
        elif task == 'regression':
            applied_steps.append("Applying log transformation for skewed continuous features")
            self.df = self.transform_skewed_features()

        # Step 7: General preprocessing
        applied_steps.append("Removing duplicate rows")
        self.df.drop_duplicates(inplace=True)
        applied_steps.append("Checking and standardizing data types")
        self.standardize_data_types()

        print("Applied preprocessing steps:")
        for step in applied_steps:
            print(f"- {step}")

        # sort column by name and make the target the last column
        target_col = self.sharedState.get_target_column()
        cols = sorted([col for col in self.df.columns if col != target_col]) + [target_col]
        self.df = self.df[cols]
        
        self.sharedState.set_data(self.df)
        return self.df,self.unique_categorical_values

    # def apply_categorical_preprocessing(self):
    #     """
    #     Apply encoding for categorical data.
    #     """
    #     cat_cols = self.df.select_dtypes(include=['object']).columns # Select categorical columns
    #     for col in cat_cols:
    #         if len(self.df[col].unique()) <= 10:  # Use one-hot encoding for low cardinality
    #             onehot_encoded = self.onehot_encoder.fit_transform(self.df[[col]])
    #             onehot_df = pd.DataFrame(onehot_encoded, columns=self.onehot_encoder.get_feature_names_out([col]))
    #             self.df = pd.concat([self.df.drop(columns=[col]), onehot_df], axis=1)
    #         else:  # Use label encoding for high cardinality
    #             self.df[col] = self.label_encoder.fit_transform(self.df[col])
    #     return self.df

    def apply_feature_augmentation(self):
        """
        Apply feature augmentation for low feature count datasets.
        """
        # Add polynomial features
        poly_features = self.df.select_dtypes(include=['float64', 'int64']).columns
        for col in poly_features:
            self.df[col + '_squared'] = self.df[col] ** 2
            self.df[col + '_cubed'] = self.df[col] ** 3
        return self.df
    
    def balance_classes(self):
        """
        Balance imbalanced classes using SMOTE.
        """
        from imblearn.over_sampling import SMOTE
        
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(self.df.drop(columns=[self.target_column]), self.df[self.target_column])
        self.df = pd.concat([X_resampled, y_resampled], axis=1)
        return self.df
    
    def handle_outliers(self):
        """
        Handle outliers in numerical columns using the IQR method.
        """
        num_cols = self.get_numerical_columns()
        for col in num_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.df[col] = np.where(self.df[col] < lower_bound, lower_bound, self.df[col])
            self.df[col] = np.where(self.df[col] > upper_bound, upper_bound, self.df[col])
        return self.df

    def transform_skewed_features(self):
        """
        Apply log transformation to skewed numerical columns.
        """
        num_cols = self.get_numerical_columns()
        for col in num_cols:
            if self.df[col].skew() > 1:  # Check if skewness > 1 (highly skewed)
                self.df[col] = np.log1p(self.df[col])  # Apply log(1+x) transformation
        return self.df
    
    def standardize_data_types(self):
        """
        Ensure all columns have appropriate data types.
        """
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].astype('string')  # Standardize text columns as 'string'
            elif self.df[col].dtype in ['float64', 'int64']:
                self.df[col] = self.df[col].astype('float64')  # Standardize numerical columns as 'float64'
        return self.df

    def get_numerical_columns(self):
        """
        Get the names of numerical columns in the dataset.
        """
        return self.df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    def binarize_target(self):
        """
        Binarize the target column for binary classification tasks.
        """
        target_col = self.sharedState.get_target_column()
        self.df[target_col] = self.df[target_col].apply(lambda x: 1 if x == self.df[target_col].mode()[0] else 0)

        return self.df
    

    def reset(self):
        self.sharedState.set_data(self.sharedState.get_original_data())
        self.df = self.sharedState.get_original_data()