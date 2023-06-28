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
        #BT.709
        tempR = self.image[:,:,0]
        tempG = self.image[:,:,1]
        tempB = self.image[:,:,2]
        # luminance probably well written
        Y   = (0.21260*tempR     + 0.71520*tempG + 0.07220*tempB).round()
        Cb  = (-0.11457*tempR    - 0.38543*tempG + 0.5*tempB).round()
        Cr  = (0.5*tempR         - 0.45415*tempG - 0.04585*tempB).round()

        imageYCbCr = np.empty_like(self.image)
        imageYCbCr[:,:,0] = Y.astype('uint8')
        imageYCbCr[:,:,1] = Cb.astype('uint8')
        imageYCbCr[:,:,2] = Cr.astype('uint8')
        
        # return only luminance - returns image in greyscale
        return imageYCbCr[:,:,0]