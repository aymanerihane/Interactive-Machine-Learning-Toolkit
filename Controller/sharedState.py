
class SharedState():
    def __init__(self):
        super().__init__()
        self.file_uploaded = False
        self.test_file_uploaded = False
        self.has_target = True # Default value for the checkbox
        self.target_culumn = None  # Default value for the checkbox
        self.has_split= False # Default value for the checkbox
        self.training_finish = False
        self.testing_finish = False
        

        # Define color palette and fonts
        self.PRIMARY_COLOR = "#497AAD"
        self.HOVER_COLOR = "#357ABD"
        self.SECONDARY_COLOR = "#F5F5F5"
        self.TEXT_COLOR = "#4A4A4A"
        self.WHITE = "#FFFFFF"
        self.ERROR_COLOR = "#FF5A5F"

        

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
