import constants

big_css_list = ["/image_gallery.css"]
style_tag = "<style>"

def load_page_from_request(request_data):
    path = constants.PAGE_FOLDER + request_data
    response = ''
    print("Try open page at: ", path)
 
    success, data = get_page_text(request_data)
    style_start_pure = data.find(style_tag)
    style_start_offset = style_start_pure + len(style_tag)

    style_string = get_styles(style_start_pure)

    if success:
        first_half_data = data[0: style_start_offset]
        second_half_data = data[style_start_offset:]
        print("\n", style_string, "\n")
        return constants.HEADER200 + first_half_data + style_string + second_half_data
    else:
        return constants.HEADER404 + 'This page does not exist'
    '''
    try:
        with open(path, "r", encoding="utf-8") as file:
            response = file.read()
        print("SUCCESSFUL OPEN")
        return constants.HEADER200 + response
    except:
        return constants.HEADER404 + 'This page does not exist'
    '''
def get_page_text(css_name):
    path = constants.PAGE_FOLDER + css_name
    try:
        with open(path, "r", encoding="utf-8") as file:
            response = file.read()
        print("SUCCESSFUL OPEN", path)
        return True, response
    except:
        print("FAILED OPEN", path)
        return False, ""
    
def get_styles(start):
    super_string = ""
    if start != -1:
        for list_point in big_css_list:
            super_string += get_page_text(list_point)[1]
        return super_string
    else:
        return ""