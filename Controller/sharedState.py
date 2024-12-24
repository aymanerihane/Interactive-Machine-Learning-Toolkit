class SharedState():
    def __init__(self):
        super().__init__()
        self._file_uploaded = False
        self._file_path = None
        self._test_file_uploaded = False
        self._has_target = True 
        self._target_culumn = None  
        self._has_split= False 
        self._training_finish = False
        self._testing_finish = False
        self._preprocessing_finish = False
        self._prediction_finish = False
        self._labels = None

        #data info
        self._data_type = None
        self._balance = None
        self._size = None
        self._features = None
        self._task = None
        self._duplicate_columns = None
        

        ##data stats
        self._number_of_nan_values = None
        self._number_of_missing_values = None
        self._number_of_classes = None
        self._data_shape = None
        self._data_balanced = None 
        self._number_of_categorical_columns = None
        self._number_of_numerical_columns = None
        
        


        # Data
        self._data = None
        self._original_data = None
        self._columns = None
        self._original_columns = None
        self._test_data = None
        self._process_done=[]
        self._model_name = None
        self._model = None
        self._test_new_data = None

        

        # Define color palette and fonts
        self.PRIMARY_COLOR = "#497AAD"
        self.HOVER_COLOR = "#357ABD"
        self.SECONDARY_COLOR = "#F5F5F5"
        self.TEXT_COLOR = "#4A4A4A"
        self.WHITE = "#FFFFFF"
        self.ERROR_COLOR = "#FF5A5F"
        self.DARK_COLOR = "#333333"

    # Setters

    def set_test_new_data(self,new):
        self._test_new_data = new

    def set_model(self,model):
        self._model = model
    def set_y_test(self, y_test):
        self.y_test = y_test

    def set_y_pred(self, y_pred):
        self.y_pred = y_pred
        
    def set_labels(self, labels):
        self._labels = labels

    def set_model_name(self, name):
        self._model_name = name

    def set_file_path(self, path):
        self._file_path = path

    def set_test_data(self, data):
        self._test_data = data

    def add_process(self, value):
        self._process_done.append(value)

    def set_new_process(self):
        self._process_done = []

    def set_preprocessing_finish(self,value):
        self._preprocessing_finish = value

    def set_original_columns(self,value):
        self._original_columns = value
        self.set_preprocessing_finish(False)

    def set_data_stats(self, nan, missing, classes, shape, balanced, cat, num,duplicate_columns):
        self._number_of_nan_values = nan
        self._number_of_missing_values = missing
        self._number_of_classes = classes
        self._data_shape = shape
        self._data_balanced = balanced
        self._number_of_categorical_columns = cat
        self._number_of_numerical_columns = num
        self._duplicate_columns = duplicate_columns

    def set_columns(self, columns):
        self._columns = columns

    def set_data_info(self, task, type, size, features, balance):
        self._data_type = type
        self._balance = balance
        self._size = size
        self._features = features
        self._task = task

    def set_data(self, data,first = False):
        self._data = data
        # self.set_columns(data.columns)
        if first:
            print("First time")
            print("Columns: ", data.columns)
            col = data.columns
            self.set_target_column(col[-1])
    
    def set_original_data(self, data):
        self._original_data = data.copy()
        # self._original_columns(data.columns)

    def set_file_uploaded(self, value):
        self._file_uploaded = value

    def set_test_file_uploaded(self, value):
        self._test_file_uploaded = value

    def set_has_target(self, value):
        self._has_target = value
        print("Has target: ", self._has_target)
    
    def set_target_column(self, value):
        print("value: ",value)
        self._target_culumn = value
        print("Target column: ", self._target_culumn)
    
    def set_has_split(self, value): 
        self._has_split = value
    
    def set_training_finish(self, value):
        self._training_finish = value
    
    def set_testing_finish(self, value):
        self._testing_finish = value

    def set_prediction_finish(self, value):
        self._prediction_finish = value

    # Getters

    def get_original_columns(self):
        return self._original_columns

    def get_data_stats(self):
        return self._number_of_nan_values, self._number_of_missing_values, self._number_of_classes, self._data_shape, self._data_balanced, self._number_of_categorical_columns, self._number_of_numerical_columns, self._duplicate_columns
    

    def get_columns(self):
        print("Columns: ", self._columns)
        return self._columns

    def get_data(self):
        return self._data
    
    def get_original_data(self):
        return self._original_data

    def get_data_info(self):
        return self._data_type, self._balance, self._size, self._features, self._task

    def get_test_file_uploaded(self):
        return self._test_file_uploaded
    

    def get_file_uploaded(self):
        return self._file_uploaded

    def get_has_target(self):
        return self._has_target
    
    def get_target_column(self):
        return self._target_culumn
    
    def get_has_split(self):
        return self._has_split
    
    def get_training_finish(self):
        return self._training_finish
    
    def get_testing_finish(self):
        return self._testing_finish
    
    def get_prediction_finish(self):
        return self._prediction_finish
    
    def get_preprocessing_finish(self):
        return self._preprocessing_finish

    def get_target_column_index(self):
        return self.index_of_target
    
    def get_process_done(self):
        return self._process_done
    
    def get_test_data(self):
        return self._test_data
    
    def get_file_path(self):
        return self._file_path
    
    def get_model_name(self):
        return self._model_name
    
    def get_labels(self):
        return self._labels
    
    def get_y_test(self):
        return self.y_test
    def get_y_pred(self):
        return self.y_pred
    
    def get_model(self):
        return self._model 
    
    def get_test_new_data(self):
        return self._test_new_data