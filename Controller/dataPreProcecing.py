import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

class DataPreProcessor:
    
    def __init__(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {file_path}")
        
        # Initialize the preprocessing steps
        self.imputer = SimpleImputer(strategy="most_frequent")  # For missing categorical data
        self.num_imputer = SimpleImputer(strategy="mean")  # For missing numerical data
        self.label_encoder = LabelEncoder()  # For label encoding categorical variables
        self.scaler = StandardScaler()  # For scaling numerical data
        self.onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)  # For one-hot encoding
        self.tfidf_vectorizer = TfidfVectorizer()  # For text data


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
        
        return self.df

    def scale_data(self):
        """
        Apply scaling to numerical columns.
        """
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if len(num_cols) > 0:
            self.df[num_cols] = self.scaler.fit_transform(self.df[num_cols])
        return self.df

    def encode_categorical(self):
        """
        Apply one-hot encoding to categorical columns.
        """
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            onehot = self.onehot_encoder.fit_transform(self.df[[col]])
            onehot_df = pd.DataFrame(onehot, columns=self.onehot_encoder.get_feature_names_out([col]))
            self.df = pd.concat([self.df, onehot_df], axis=1)
            self.df.drop(columns=[col], inplace=True)
        return self.df

    def label_encode(self):
        """
        Apply label encoding to categorical columns.
        """
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            self.df[col] = self.label_encoder.fit_transform(self.df[col])
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
        return self.df

    def process_text(self, text_column):
        """
        Apply TF-IDF vectorization to textual data.
        """
        if text_column in self.df.columns:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df[text_column])
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=self.tfidf_vectorizer.get_feature_names_out())
            self.df = self.df.drop(text_column, axis=1).join(tfidf_df)
        return self.df

    def preprocess(self):
        """
        Apply all preprocessing steps.
        """
        # Clean missing data
        self.df = self.clean_data()
        # Scale numerical data
        self.df = self.scale_data()
        # Encode categorical variables
        self.df = self.encode_categorical()
        # Label encode if needed
        self.df = self.label_encode()
        # Handle date columns
        self.df = self.handle_dates()
        
        print(self.df.head())  # Print the processed DataFrame
        return self.df
