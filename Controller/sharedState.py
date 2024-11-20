class SharedState:
    def __init__(self):
        self.file_uploaded = False
        self.test_file_uploaded = False
        self.has_target = True # Default value for the checkbox
        self.target_culumn = None  # Default value for the checkbox
        self.has_split= False # Default value for the checkbox
        self.training_finish = False
        self.testing_finish = False

    # Setters

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

    # Getters

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
