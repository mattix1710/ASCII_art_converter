import imageio.v2 as imageio
import numpy as np

# represent ASCII characters in the decimal form - for easier extracting purposes
SIGNS_EXTENDED = {0 : 36, 4 : 64, 8 : 66, 12 : 37, 16 : 56, 20 : 38, 24 : 87, 28 : 77, 32 : 35, 36 : 42, 40 : 111, 44 : 97, 48 : 104, 52 : 107, 56 : 98, 60 : 100, 64 : 112, 68 : 113, 72 : 119, 76 : 109, 80 : 90, 84 : 79, 88 : 48, 92 : 81, 96 : 76, 100 : 67, 104 : 74, 108 : 85, 112 : 89, 116 : 88, 118 : 122, 120 : 99, 122 : 118, 124 : 117, 126 : 110, 128 : 120, 130 : 114, 132 : 106, 134 : 102, 136 : 116, 140 : 47, 144 : 92, 148 : 124, 152 : 40, 156 : 41, 160 : 49, 164 : 123, 168 : 125, 172 : 91, 176 : 93, 180 : 63, 184 : 45, 188 : 95, 192 : 43, 196 : 126, 200 : 60, 204 : 62, 208 : 105, 212 : 33, 216 : 108, 220 : 73, 224 : 59, 228 : 58, 232 : 44, 236 : 34, 240 : 94, 244 : 96, 248 : 39, 252 : 46, 256 : 32}
# SIGNS_SHORT = ['32', '46', '58', '45', '61', '43', '42', '35', '37', '64']
SIGNS_SHORT = {0 : 32, 29 : 46, 58 : 58, 87 : 45, 116 : 61, 145 : 43, 174 : 42, 203 : 35, 232 : 37, 261 : 64}

class Converter_ASCII:
    def __init__(self, image: str = None, extended: bool = True):
        self.image = imageio.imread(image)
        self.image_grey = image
        self.extended = extended
        
    def get_image_shape(self):
        return self.image.shape
        
    def display_as_array(self):
        print(self.image)
        
    def display_as_greyscale_array(self):
        print(self.greyscale_convert())
        
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
    
    # TODO
    def convert_to_ASCII_chunks(self):
        self.image_grey = self.greyscale_convert()
        PIXELS = 8
        IMG_WIDTH = self.image_grey.shape[1]
        IMG_HEIGHT = self.image_grey.shape[0]
        
        # take 64-pixel chunks
        chunks = self.blockshaped(self.image_grey, PIXELS, PIXELS)
        for chunk in chunks:
            # count mean value and decide which number to take
            # 
            #         4         2           4
            # /^^^^^^^^^^^^^\/^^^^^\/^^^^^^^^^^^^^\
            # |-------------|------|--------------|
            # 0            116    136            256
            
            
            mean_val = int(np.mean(chunk))
            if mean_val >= 50 and mean_val <= 206:
                curr_val = 3 * round((mean_val-50) / 3)
        
    def convert_to_ASCII(self):
        self.image_grey = self.greyscale_convert()
        IMG_WIDTH = self.image_grey.shape[1]
        IMG_HEIGHT = self.image_grey.shape[0]
        image_ASCII = np.zeros_like(self.image_grey)
        
        # if extended version chosen (70 characters):
        if self.extended:
        # convert pixels to ASCII characters based on its greyscale
        # 
        #         4           2           4
        # /^^^^^^^^^^^^^\/^^^^^^^^^\/^^^^^^^^^^^^^\
        # |-------------|----------|--------------|
        # 0   -=30=-   116 -=10=- 136   -=30=-   256
        
            for x, it_x in zip(self.image_grey, range(len(image_ASCII))):
                for y, it_y in zip(x, range(len(x))):
                    aux = 0
                    if y < 116 or y >= 136:
                        aux = y // 4 * 4
                    elif y >= 116 and y < 136:
                        aux = y // 2 * 2
                    
                    if aux == 0:
                        aux = 256
                        
                    image_ASCII[it_x][it_y] = SIGNS_EXTENDED[aux]
        else:
            for x, it_x in zip(self.image_grey, range(len(image_ASCII))):
                for y, it_y in zip(x, range(len(x))):
                    aux = round(y / 29) * 29
                    image_ASCII[it_x][it_y] = SIGNS_SHORT[aux]
            
        
        return image_ASCII
        
    def display_ASCII_converted(self):
        converted = self.convert_to_ASCII()
        for x in converted:
            for y in x:
                print(chr(y), end="")
            print("")
    
    def mean_chunk(self, chunk):
        print("Hello")