from PIL import Image
from decimal import Decimal, ROUND_HALF_UP

def write_pixels_file(image):
    list_of_pixels = list(image.getdata())
    str_of_pixels = ', '.join(str(e) for e in list_of_pixels)

    f = open('pixels.txt', 'a')
    f.write(str_of_pixels)
    f.close()

"""
This function returns a dictionary with the amount of pixels in each level of color
"""    
def count_image_pixels(image):
    aux = {}
    dict_image_pixels = aux.fromkeys(range(256), 0)

    for i in list(image.getdata()):
        if i in dict_image_pixels.keys():
            dict_image_pixels[i] = dict_image_pixels[i] + 1
    
    return dict_image_pixels

def get_image_pixels_percentage(dict_pixels, total_pixels):
    dict_image_pixels_percentage = {}

    for key, value in dict_pixels:
        float()



im = Image.open('PDI/lena_gray.bmp')
#A imagem tem 65536 pixels

x = Decimal(630/65536)

conjunto = (0)
pixels_per_level = count_image_pixels(im)
#percentage_pixels_per_level
#print(x.quantize(Decimal('0.001'), ROUND_HALF_UP))
print(pixels_per_level)