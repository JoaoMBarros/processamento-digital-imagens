from PIL import Image

def write_pixels_file(image):
    list_of_pixels = list(image.getdata())
    str_of_pixels = ', '.join(str(e) for e in list_of_pixels)

    f = open('pixels.txt', 'a')
    f.write(str_of_pixels)
    f.close()

def get_4_neighbour_path(image):
    img_height = image.height
    img_width = image.width

    background = (0, 0, 0, 255)
    new_4_path_image = Image.new('RGB', (256, 256), background)
    new_image = new_4_path_image.load()

    for x in range(img_height):
        for y in range(img_width):
            coordenadas_vizinhas = [[x, y+1], [x, y-1], [x-1, y], [x+1, y]]

            for vizinho in coordenadas_vizinhas:
                out_of_range = False

                for aux in vizinho:
                    if aux < 0 or aux > img_width-1 or aux > img_height-1:
                        out_of_range = True
                
                if(image.getpixel((x, y)) == (255, 255, 255, 255)):
                    if (not out_of_range and image.getpixel(tuple(vizinho)) == background):
                        new_image[x, y] = (255, 255, 255, 255)

    new_4_path_image.show()

def get_8_neighbour_path(image):
    img_height = image.height
    img_width = image.width

    background = (0, 0, 0, 255)
    new_8_path_image = Image.new('RGB', (256, 256), background)
    new_image = new_8_path_image.load()

    for x in range(img_height):
        for y in range(img_width):
            coordenadas_vizinhas = [[x, y+1], [x, y-1], [x-1, y], [x+1, y], [x+1, y+1], [x+1, y-1], [x-1, y+1], [x-1, y-1]]

            for vizinho in coordenadas_vizinhas:
                out_of_range = False

                for aux in vizinho:
                    if aux < 0 or aux > img_width-1 or aux > img_height-1:
                        out_of_range = True
                
                if(image.getpixel((x, y)) == (255, 255, 255, 255)):
                    if (not out_of_range and image.getpixel(tuple(vizinho)) == background):
                        new_image[x, y] = (255, 255, 255, 255)

    new_8_path_image.show()

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

im = Image.open('PDI/folha.png')
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
#print(pixels_cumulative_equalized)
#get_4_neighbour_path(im)
#get_8_neighbour_path(im)