class SharedState():
    def __init__(self):
        super().__init__()
        self.file_uploaded = False
        self.file_path = None
        self.test_file_uploaded = False
        self.has_target = True 
        self.target_culumn = None  
        self.has_split= False 
        self.training_finish = False
        self.testing_finish = False
        self.preprocessing_finish = False
        self.prediction_finish = False
        labels = None

        #data info
        self.data_type = None
        self.balance = None
        self.size = None
        self.features = None
        self.task = None
        self.duplicate_columns = None
        

        ##data stats
        self.number_of_nan_values = None
        self.number_of_missing_values = None
        self.number_of_classes = None
        self.data_shape = None
        self.data_balanced = None 
        self.number_of_categorical_columns = None
        self.number_of_numerical_columns = None
        
        


        # Data
        self.data = None
        self.original_data = None
        self.columns = None
        self.original_columns = None
        self.test_data = None
        self.process_done=[]
        self.model_name = None

        

        # Define color palette and fonts
        self.PRIMARY_COLOR = "#497AAD"
        self.HOVER_COLOR = "#357ABD"
        self.SECONDARY_COLOR = "#F5F5F5"
        self.TEXT_COLOR = "#4A4A4A"
        self.WHITE = "#FFFFFF"
        self.ERROR_COLOR = "#FF5A5F"
        self.DARK_COLOR = "#333333"

        

    # Setters
    def set_y_test(self, y_test):
        self.y_test = y_test

    def set_y_pred(self, y_pred):
        self.y_pred = y_pred
        
    def set_labels(self, labels):
        self.labels = labels

    def set_model_name(self, name):
        self.model_name = name

    def set_file_path(self, path):
        self.file_path = path

    def set_test_data(self, data):
        self.test_data = data

    def add_process(self, value):
        self.process_done.append(value)

    def set_new_process(self):
        self.process_done = []

    def set_preprocessing_finish(self,value):
        self.preprocessing_finish = value

    def set_original_columns(self,value):
        self.original_columns = value
        self.set_preprocessing_finish(False)

    def set_data_stats(self, nan, missing, classes, shape, balanced, cat, num,duplicate_columns):
        self.number_of_nan_values = nan
        self.number_of_missing_values = missing
        self.number_of_classes = classes
        self.data_shape = shape
        self.data_balanced = balanced
        self.number_of_categorical_columns = cat
        self.number_of_numerical_columns = num
        self.duplicate_columns = duplicate_columns

    def set_columns(self, columns):
        self.columns = columns

    def set_data_info(self, task, type, size, features, balance):
        self.data_type = type
        self.balance = balance
        self.size = size
        self.features = features
        self.task = task

    def set_data(self, data,first = False):
        self.data = data
        self.set_columns(data.columns)
        if first:
            print("First time")
            print("Columns: ", data.columns)
            self.set_target_column(data.columns[-1])
    
    def set_original_data(self, data):
        self.original_data = data.copy()
        # self.original_columns(data.columns)

    def set_file_uploaded(self, value):
        self.file_uploaded = value

    def set_test_file_uploaded(self, value):
        self.test_file_uploaded = value

    def set_has_target(self, value):
        self.has_target = value
        print("Has target: ", self.has_target)
    
    def set_target_column(self, value):
        print("value: ",value)
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

    def get_original_columns(self):
        return self.original_columns

    def get_data_stats(self):
        return self.number_of_nan_values, self.number_of_missing_values, self.number_of_classes, self.data_shape, self.data_balanced, self.number_of_categorical_columns, self.number_of_numerical_columns, self.duplicate_columns
    

    def get_columns(self):
        print("Columns: ", self.columns)
        return self.columns

    def get_data(self):
        return self.data
    
    def get_original_data(self):
        return self.original_data

    def get_data_info(self):
        return self.data_type, self.balance, self.size, self.features, self.task

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
    
    def get_preprocessing_finish(self):
        return self.preprocessing_finish

    def get_target_column_index(self):
        return self.index_of_target
    
    def get_process_done(self):
        return self.process_done
    
    def get_test_data(self):
        return self.test_data
    
    def get_file_path(self):
        return self.file_path
    
    def get_model_name(self):
        return self.model_name
    
    def get_labels(self):
        return self.labels
    
    def get_y_test(self):
        return self.y_test
    def get_y_pred(self):
        return self.y_pred