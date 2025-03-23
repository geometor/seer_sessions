"""
The transformation rule is as follows:
1. Examine the input grid.
2. Identify all non-zero (non-black) pixels.
3. Count the occurrences of each distinct non-zero pixel color.
4. Create output array using the non-zero pixel and the product of it's dimensions.
5. Fill output array with the found pixel.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Extracts and returns a list of non-zero pixel values from the input grid.
    """
    return [pixel for row in grid for pixel in row if pixel != 0]

def construct_output_grid(pixel_counts):
    """Constructs the output grid based on the counts of non-zero pixels."""
    output = []

    for pixel, count in pixel_counts.items():
        rows = 0
        cols = 0
        
        if count == 1:
            rows = 1
            cols = 1
        elif count == 2:
            rows = 1
            cols = 2
        elif count == 3:
            rows = 1
            cols = 3            
        elif count == 4:
            rows = 2
            cols = 2
        elif count == 6:
            rows = 2
            cols = 3
        elif count == 9:
            rows = 3
            cols = 3

        
        output_grid = np.full((rows, cols), pixel)      
        output.append(output_grid)
    
    if (len(output) == 0):
        return np.array([])
    if (len(output) == 1):
        return output[0]    
    # for this challenge, assume that we always return only one output.  
    # may require future generalization.    
    return output[0]

def transform(input_grid):
    # initialize output_grid
    
    #get non-zero pixels
    non_zero_pixels = get_nonzero_pixels(input_grid)
   
    #count occurences of each non-zero pixel
    pixel_counts = {}
    for pixel in non_zero_pixels:
        if pixel in pixel_counts:
            pixel_counts[pixel] += 1
        else:
            pixel_counts[pixel] = 1

    # construct output grid
    output_grid = construct_output_grid(pixel_counts)

    return output_grid