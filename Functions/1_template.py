########################################
"""
Function Library
Example Usage:
from pa_common.<python_filename> import <your class>
"""
########################################
# REQUIREMENTS
########################################
from dotenv import load_dotenv
import os

########################################
# FUNCTION GOES IN CLASS
########################################


class EXAMPLE_CLASS():
    def __init__(self, env_filepath,PARAM1):
        #INITIALIZE YOUR PARAMETERS HERE
        self.env_filepath = env_filepath
        self.PARAM1 = PARAM1

        self.TEMPLATE_FUNCTION()

    def TEMPLATE_FUNCTION(self):
        load_dotenv(self.env_filepath)
    

        try:
            print("Sucessfully Ran")
        except:
            print("Error")





  



   
