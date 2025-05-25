import constants
class ImageManager():
    def __init__(self):
        self.counter = 0
        return None
    
    def update_photo_list(self):
        self.counter += 1
        print("photo list updated" + str(self.counter))
        return constants.HEADER200 + "googoo gaga"