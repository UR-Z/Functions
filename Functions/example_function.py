########################################
"""
Function Library
Example Usage:
from pa_common.Functions.<python_filename> import EXAMPLE_CLASS
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
    def __init__(self, env_filepath,print_message):
        #INITIALIZE YOUR PARAMETERS HERE
        self.env_filepath = env_filepath
        self.print_message = print_message

        self.TEMPLATE_FUNCTION()

    def TEMPLATE_FUNCTION(self):
        load_dotenv(self.env_filepath)
        try:
            print(self.print_message)
            print("Sucessfully Ran")
        except:
            print("Error")





  



   
