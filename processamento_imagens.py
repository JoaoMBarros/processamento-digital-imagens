from math import log2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

"""Draws a plot graph of the image histogram"""
def draw_histogram_graph(list_pixels):
    plt.plot(list_pixels) #Plotting the list of pixels
    skip = 5 #Skip is the gap of values in the x-axis
    plt.xticks(range(0, len(list_pixels))[::skip])
    
    plt.show()

"""Writes a file with the values of all pixels of the image"""
def write_pixels_file(image):
    list_of_pixels = list(image.getdata())
    str_of_pixels = ', '.join(str(e) for e in list_of_pixels)

    f = open('pixels.txt', 'a')
    f.write(str_of_pixels)
    f.close()

"""This function returns an image with only the pixels of the edge in a adjacency-8 path. Works exactly like the adjacency-4 path function"""
def get_8_neighbour_path(image):
    img_height, img_width = image.size
    background = (0, 0, 0, 255)
    new_8_path_image = Image.new('RGB', (img_height, img_width), background)
    new_image = new_8_path_image.load()

    for x in range(img_height):
        for y in range(img_width):

            if(image.getpixel((x, y)) == (255, 255, 255, 255)):
                neighbours_coord = [[x, y+1], [x, y-1], [x-1, y], [x+1, y], [x+1, y+1], [x+1, y-1], [x-1, y+1], [x-1, y-1]] #Coordinates of the neighbours-8 of every pixel

                for neighbour in neighbours_coord:
                    out_of_range = False #Variable that indicates if the neighbour's position is valid

                    for aux in neighbour:
                        if aux < 0 or aux > img_width-1 or aux > img_height-1:
                            out_of_range = True

                    if (not out_of_range and image.getpixel(tuple(neighbour)) == background):
                        new_image[x, y] = (255, 255, 255, 255)
    
    new_8_path_image.save('caminho_8.png')

    return new_8_path_image

"""This function returns an image with only the pixels of the edge in a adjacency-4 path."""
def get_4_neighbour_path(image):
    img_height, img_width = image.size
    background = (0, 0, 0, 255)
    new_4_path_image = Image.new('RGB', (img_height, img_width), background)
    new_image = new_4_path_image.load()

    #Two for loops iterating through all pixels
    for x in range(img_height):
        for y in range(img_width):

            #Checking if the pixel is part of the path that we want
            if(image.getpixel((x, y)) == (255, 255, 255, 255)):
                neighbours_coord = [[x, y+1], [x, y-1], [x-1, y], [x+1, y]]

                #Checking each neighbour
                for neighbour in neighbours_coord:
                    out_of_range = False
 
                    #Validating neighbour position
                    for aux in neighbour:
                        if aux < 0 or aux > img_width-1 or aux > img_height-1:
                            out_of_range = True

                    #If the neighbour of the pixel we are currently on (white) is valid and is part of the background, we know that that pixel is part of the edge
                    if (not out_of_range and image.getpixel(tuple(neighbour)) == background):
                        new_image[x, y] = (255, 255, 255, 255)

    new_4_path_image.save('caminho_4.png')

    return new_4_path_image

"""This function returns a dictionary with the amount of pixels in each level of color"""    
def count_image_pixels(image):
    aux = {}
    dict_image_pixels = aux.fromkeys(range(256), 0)

    for i in list(image.getdata()):
        dict_image_pixels[i] = dict_image_pixels[i] + 1
    
    return dict_image_pixels

"""Normalized histogram"""
def get_image_pixels_percentage(dict_pixels, total_pixels):
    dict_pixels_percentage = {}

    for key, value in dict_pixels.items():
        aux = round((value/total_pixels), 3) #Calculating the percentage of pixels in each level
        dict_pixels_percentage[key] = round(aux, 3)
        
    return dict_pixels_percentage

"""Cumulative histogram"""
def get_image_pixels_cumulative_percentage(dict_pixels, total_pixels):
    dict_pixels_cumulative_percentage = {}
    before = 0

    for key, value in dict_pixels.items():
        aux = round((value/total_pixels), 3) + before #Calculating the percentage of pixels in the current level plus the sum of the previous percentages
        dict_pixels_cumulative_percentage[key] = round(aux, 3)
        before = dict_pixels_cumulative_percentage[key]

    return dict_pixels_cumulative_percentage

def get_equalized_image(dict_pixels_percentage, pixels, size):
    dict_equalized_pixels_levels = {}
    new_pixel_data = []
    highest_pixel_level = list(dict_pixels_percentage.keys()) #List of all percentages of pixels
    
    #Getting the new pixel level for each pixel level of the original image
    for key, value in dict_pixels_percentage.items():
        dict_equalized_pixels_levels[key] = round((highest_pixel_level[-1] * value)) #[-1] to get the value of the last index of the pixel percentage list

    #Appending each pixel with its new value in a list
    for pixel in pixels:
        new_pixel_data.append(dict_equalized_pixels_levels.get(pixel))

    #Creating a new image and putting the new pixel list in it
    equalized_image = Image.new('L', ((size[0], size[1])))
    equalized_image.putdata(new_pixel_data)
    
    return equalized_image

def get_specified_image(dict_pixels_specified_percentage, dict_pixels_original_percentage, pixels, size):
    dict_specified_equalized_pixels_levels = {}
    dict_equalized_levels = {}
    new_pixels = np.arange(256)
    new_pixel_data = []
    highest_pixel_level = list(dict_pixels_specified_percentage.keys()) 
    
    for key, value in dict_pixels_specified_percentage.items():
        dict_specified_equalized_pixels_levels[key] = round((highest_pixel_level[-1] * value))
    
    for key, value in dict_pixels_original_percentage.items():
        dict_equalized_levels[key] = round((highest_pixel_level[-1] * value))
    
    close_values = np.interp(list(dict_pixels_specified_percentage.values()), list(dict_pixels_original_percentage.values()), new_pixels)
    close_values = list(close_values)

    for pixel in pixels:
        new_pixel_data.append(close_values[pixel])

    specified_image = Image.new('L', ((size[0], size[1])))
    specified_image.putdata(new_pixel_data)
    
    specified_image.save('image1 com histograma da lena_gray.png')

    return close_values
    
"""Apply the pixel transformation formula s = c * f + b"""
def get_linear_transformation(pixels, img_size):
    new_pixels = []
    c = 1
    b = 5

    for pixel in pixels:
        new_pixels.append(c * pixel + b)
    
    new_image = Image.new('L', (img_size[0], img_size[1]))
    new_image.putdata(new_pixels)

    return new_image

"""Apply the pixel transformation formula s = c * log2(r + 1)"""
def get_logaritmic_transformation(pixels, img_size):
    new_pixels = []
    c = 35

    for pixel in pixels:
        new_pixels.append(round(c * (log2(pixel + 1))))
    
    new_image = Image.new('L', (img_size[0], img_size[1]))
    new_image.putdata(new_pixels)

    return new_image

"""Apply the pixel transformation formula s = c * r ^ Y"""
def get_pot_transformation(pixels, img_size):
    new_pixels = []
    gamma = 1.0
    c = 2
    
    for pixel in pixels:
        new_pixels.append(c * ((pixel + 1)**gamma))
    
    new_image = Image.new('L', (img_size[0], img_size[1]))
    new_image.putdata(new_pixels)

    return new_image