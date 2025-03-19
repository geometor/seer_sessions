"""
The program extracts a diagonal sequence of azure pixels from the input, starting from the top-left and going down. It creates a new grid based on those selected pixels.
"""

import numpy as np

def get_azure_pixels(grid):
    # find coordinates of all azure pixels
    azure_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 8:
                azure_pixels.append((row_index, col_index))
    return azure_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # find azure pixels
    azure_pixels = get_azure_pixels(input_grid)
    
    # select pixels for output
    selected_pixels = []
    if azure_pixels:
        current_pixel = azure_pixels[0]
        selected_pixels.append(current_pixel)
        
        for _ in range(3): #max 3 additional pixels for 4x4 grid
            next_pixel = None
            for pixel in azure_pixels:
                if pixel[0] > current_pixel[0] and pixel[1] > current_pixel[1]:
                    if next_pixel is None:
                        next_pixel = pixel
                    elif (pixel[0] - current_pixel[0]) + (pixel[1] - current_pixel[1]) < (next_pixel[0] - current_pixel[0]) + (next_pixel[1] - current_pixel[1]) :
                        next_pixel = pixel;

            if next_pixel is not None:
                selected_pixels.append(next_pixel)
                current_pixel = next_pixel
            else:
                break

    # fill output grid
    for i, pixel_coord in enumerate(selected_pixels):
        if i < 4:
            output_grid[i,i] = 8


    return output_grid