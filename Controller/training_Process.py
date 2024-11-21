
from Controller.dataPreProcecing import DataPreProcessor
from Controller.sharedState import SharedState
from sklearn.model_selection import train_test_split

class TrainingProcess():
    def __init__(self,file_path,sharedState):
        self.file_path = file_path
        self.sharedState = sharedState
        self.dataPreProcessor = DataPreProcessor(file_path)
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
        self.accuracy = None
        self.classification_report = None
        self.confusion_matrix = None
        self.feature_importance = None
        self.model_name = None
        self.target_column = self.sharedState.target_column
        self.original_data = self.dataPreProcessor.return_original_data()
        self.dataPreProcessor.preprocess()
        self.X = self.dataPreProcessor.df.drop(columns=[self.target_column])
        self.y = self.dataPreProcessor.df[self.target_column]
        self.split_data()


    def split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

    

    