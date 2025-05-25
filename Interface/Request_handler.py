import json
import constants
from load_page_request import load_page_from_request
from TestFillForm import TestFillForm
from ImageManager import ImageManager
import cgi


global one_and_only_image_manager 
one_and_only_image_manager = ImageManager()
def request_handler(request_data, adress): # Эта штука должна определять тип реквеста и вызывать соответствующую функцию наверное из словаря функций?
    print(request_data)
    start_index = request_data. find("{")
    end_index   = request_data.rfind("}")
    my_dictionary = {}
    if start_index != -1 and end_index != 1:
        function_data = request_data[start_index : end_index + 1]
        my_dictionary = json.loads(function_data)
    
    split_data = request_data.split(" ")

    main_request = {
        "TYPE": split_data[0],
        "Adress": split_data[1]
    }
    print("MAIN DATA:  ", main_request)
    print("ADD ARGS:   ", my_dictionary)
    return main_request, my_dictionary

def normal_request():
    return True

def function_picker(main_request, my_dictionary): # Эта штука должна выбирать функцию на освнове типа POST/GET и названия функции из my_dictionary
    if main_request["TYPE"] == "GET":
        return load_page_from_request(main_request["Adress"])
    
    if main_request["TYPE"] == "POST":
        if my_dictionary.get("images", False) != False:
            return one_and_only_image_manager.update_photo_list()
        elif my_dictionary.get("params", False) != False:
            return TestFillForm(my_dictionary["params"])
    


    print("FAILED: я где то обосрался")
    return constants.HEADER200 + "failed to pick a function кастомка"
