import json
from load_page_request import load_page_from_request
from TestFillForm import TestFillForm
def request_handler(request_data, adress): # Эта штука должна определять тип реквеста и вызывать соответствующую функцию наверное из словаря функций?
    start_index = request_data. find("{")
    end_index   = request_data.rfind("}")
    #function_data = ""
    my_dictionary = {}
    if start_index != -1 and end_index != 1:
        function_data = request_data[start_index : end_index + 1]
        my_dictionary = json.loads(function_data)
    #print("REQ_DATA: ", function_data)
    #print("ADRESS:   ", adress)
    
    split_data = request_data.split(" ")

    main_request = {
        "TYPE": split_data[0],
        "Adress": split_data[1]
    }
    print("MAIN DATA:  ", main_request)
    print("ADD ARGS:   ", my_dictionary)
    return main_request, my_dictionary


def function_picker(main_request, my_dictionary): # Эта штука должна выбирать функцию на освнове типа POST/GET и названия функции из my_dictionary
    if main_request["TYPE"] == "GET":
        return load_page_from_request(main_request["Adress"])
    
    if main_request["TYPE"] == "POST":
        return TestFillForm(my_dictionary["params"])
    


    print("FAILED: operation not pickled")
    return "failed to pick a function"
