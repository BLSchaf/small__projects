from PIL import Image
import numpy


image = Image.open('assets\miu_origin.png', 'r') # Can be many different formats.
width, height = image.size
#print(image.mode)
pixels = image.load()


#pixels = list(image.getdata()) #pixels[width*row+col]
# instead of one long list, convert to numpy array
#pixels = numpy.array(pixels).reshape((width, height, 3))
#print(pixels.shape)

for row in range(width):
    for col in range(height):
        #print(pixels[width*row+col])
        brightness = int(pixels[col, row][0]*0.299 \
                         + pixels[col, row][1]*0.587 \
                         + pixels[col, row][2]*0.114)
        
        pixels[col, row] = (brightness, brightness, brightness)
##        pixels[row,col,1] = brightness
##        pixels[row,col,2] = brightness
        
#print(pixels[:10])
image.save('assets\miu_converted.png')  # Save the modified pixels as .png

''' # create image from pixel values
from PIL import Image
data = ""
for i in range( 128**2 ):
    data += chr(255) + chr(0) + chr(0)
im = Image.fromstring("RGB", (128,128), data)
im.save("test.png", "PNG")
'''
