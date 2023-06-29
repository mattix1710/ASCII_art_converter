import imageio.v2 as imageio
import numpy as np

# represent ASCII characters in the decimal form - for easier extracting purposes
SIGNS_EXTENDED = ['36', '64', '66', '37', '56', '38', '87', '77', '35', '42', '111', '97', '104', '107', '98', '100', '112', '113', '119', '109', '90', '79', '48', '81', '76', '67', '74', '85', '89', '88', '122', '99', '118', '117', '110', '120', '114', '106', '102', '116', '47', '92', '124', '40', '41', '49', '123', '125', '91', '93', '63', '45', '95', '43', '126', '60', '62', '105', '33', '108', '73', '59', '58', '44', '34', '94', '96', '39', '46', '32']
SIGNS_SHORT = ['32', '46', '58', '45', '61', '43', '42', '35', '37', '64']

class Converter_ASCII:
    def __init__(self, image = None, extended = None):
        self.image = image
        self.image_grey = image
        self.extended = extended
        
    def greyscale_convert(self):
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
    
    # Thanks to: https://stackoverflow.com/a/16858283
    def blockshaped(self, arr, nrows, ncols):
        """
        Return an array of shape (n, nrows, ncols) where
        n * nrows * ncols = arr.size

        If arr is a 2D array, the returned array should look like n subblocks with
        each subblock preserving the "physical" layout of arr.
        """
        h, w = arr.shape
        assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
        assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
        return (arr.reshape(h//nrows, nrows, -1, ncols)
                .swapaxes(1,2)
                .reshape(-1, nrows, ncols))
    
    def convert_to_ASCII(self):
        self.image_grey = self.greyscale_convert()
        PIXELS = 8
        IMG_WIDTH = self.image_grey.shape[1]
        IMG_HEIGHT = self.image_grey.shape[0]
        
        # take 64-pixel chunks
        chunks = self.blockshaped(self.image_grey, PIXELS, PIXELS)
        for chunk in chunks:
            mean_val = int(np.mean(chunk))
            if mean_val >= 50 and mean_val <= 206:
                curr_val = 3 * ((mean_val-50) / 3)
        
    def mean_chunk(self, chunk):
        print("Hello")