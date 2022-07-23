from PIL import Image

def write_pixels_file(image):
    list_of_pixels = list(image.getdata())
    str_of_pixels = ', '.join(str(e) for e in list_of_pixels)

    f = open('pixels.txt', 'a')
    f.write(str_of_pixels)
    f.close()

"""This function returns a dictionary with the amount of pixels in each level of color"""    
def count_image_pixels(image):
    aux = {}
    dict_image_pixels = aux.fromkeys(range(256), 0)

    for i in list(image.getdata()):
        if i in dict_image_pixels.keys():
            dict_image_pixels[i] = dict_image_pixels[i] + 1
    
    return dict_image_pixels

"""Normalized histogram"""
def get_image_pixels_percentage(dict_pixels, total_pixels):
    dict_pixels_percentage = {}

    for key, value in dict_pixels.items():
        aux = round((value/total_pixels), 3)
        dict_pixels_percentage[key] = round(aux, 3)
        
    return dict_pixels_percentage

"""Cumulative histogram"""
def get_image_pixels_cumulative_percentage(dict_pixels, total_pixels):
    dict_pixels_cumulative_percentage = {}
    before = 0

    for key, value in dict_pixels.items():
        aux = round((value/total_pixels), 3) + before
        dict_pixels_cumulative_percentage[key] = round(aux, 3)
        before = dict_pixels_cumulative_percentage[key]

    return dict_pixels_cumulative_percentage

def get_equalized_pixels_percentage(dict_pixels):
    dict_equalized_pixels_percentage = {}
    highest_pixel_level = list(dict_pixels.keys())

    for key, value in dict_pixels.items():
        dict_equalized_pixels_percentage[key] = round((highest_pixel_level[-1] * value), 3)

    return dict_equalized_pixels_percentage

im = Image.open('PDI/lena_gray.bmp')
#A imagem tem 65536 pixels

conjunto = (0)
pixels_per_level = count_image_pixels(im)
pixels_percentage = get_image_pixels_percentage(pixels_per_level, 65536)
pixels_cumulative_percentage = get_image_pixels_cumulative_percentage(pixels_per_level, 65536)
pixels_cumulative_equalized = get_equalized_pixels_percentage(pixels_cumulative_percentage)
#percentage_pixels_per_level
#print(x.quantize(Decimal('0.001'), ROUND_HALF_UP))
#print(pixels_per_level)
#print(pixels_percentage)
#print(pixels_cumulative_percentage)
print(pixels_cumulative_equalized)