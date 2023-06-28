import imageio.v2 as imageio
import numpy as np

# represent ASCII characters in the decimal form - for easier extracting purposes
SIGNS_EXTENDED = ['36', '64', '66', '37', '56', '38', '87', '77', '35', '42', '111', '97', '104', '107', '98', '100', '112', '113', '119', '109', '90', '79', '48', '81', '76', '67', '74', '85', '89', '88', '122', '99', '118', '117', '110', '120', '114', '106', '102', '116', '47', '92', '124', '40', '41', '49', '123', '125', '91', '93', '63', '45', '95', '43', '126', '60', '62', '105', '33', '108', '73', '59', '58', '44', '34', '94', '96', '39', '46', '32']
SIGNS_SHORT = ['32', '46', '58', '45', '61', '43', '42', '35', '37', '64']

class Converter_ASCII:
    def __init__(self, image, extended):
        self.image = image
        self.extended = extended
        
    def greyscale(self):
        grey_img = self.image
        return grey_img