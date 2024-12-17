
class SharedState():
    def __init__(self):
        super().__init__()
        self.file_uploaded = False
        self.test_file_uploaded = False
        self.has_target = True 
        self.target_culumn = None  
        self.has_split= False 
        self.training_finish = False
        self.testing_finish = False
        self.prediction_finish = False

        #data info
        self.data_type = None
        self.balance = None
        self.size = None
        self.features = None
        self.task = None
        
        

        # Data
        self.data = None
        self.original_data = None
        self.columns = None

        

        # Define color palette and fonts
        self.PRIMARY_COLOR = "#497AAD"
        self.HOVER_COLOR = "#357ABD"
        self.SECONDARY_COLOR = "#F5F5F5"
        self.TEXT_COLOR = "#4A4A4A"
        self.WHITE = "#FFFFFF"
        self.ERROR_COLOR = "#FF5A5F"

        

    # Setters

    def set_columns(self, columns):
        self.columns = columns

    def set_data_info(self, task, type, size, features, balance):
        self.data_type = type
        self.balance = balance
        self.size = size
        self.features = features
        self.task = task

    def set_data(self, data):
        self.data = data
    
    def set_original_data(self, data):
        self.original_data = data

    def set_file_uploaded(self, value):
        self.file_uploaded = value

    def set_test_file_uploaded(self, value):
        self.test_file_uploaded = value

    def set_has_target(self, value):
        self.has_target = value
        print("Has target: ", self.has_target)
    
    def set_target_column(self, value):
        self.target_culumn = value
        print("Target column: ", self.target_culumn)
    
    def set_has_split(self, value): 
        self.has_split = value
    
    def set_training_finish(self, value):
        self.training_finish = value
    
    def set_testing_finish(self, value):
        self.testing_finish = value

    def set_prediction_finish(self, value):
        self.prediction_finish = value

    # Getters

    def get_columns(self):
        print("Columns: ", self.columns)
        return self.columns

    def get_data(self):
        return self.data
    
    def get_original_data(self):
        return self.original_data

    def get_data_info(self):
        return self.data_type, self.balance, self.size, self.features

    def get_test_file_uploaded(self):
        return self.test_file_uploaded
    

    def get_file_uploaded(self):
        return self.file_uploaded

    def get_has_target(self):
        return self.has_target
    
    def get_target_column(self):
        return self.target_culumn
    
    def get_has_split(self):
        return self.has_split
    
    def get_training_finish(self):
        return self.training_finish
    
    def get_testing_finish(self):
        return self.testing_finish
    
    def get_prediction_finish(self):
        return self.prediction_finish
