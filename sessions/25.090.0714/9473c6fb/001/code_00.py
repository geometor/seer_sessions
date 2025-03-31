"""
Transformation Logic:

1.  Initialize the output grid as a copy of the input grid.
2.  Find all pixels in the input grid that are not Orange (7). Create a list of their coordinates (row, column).
3.  Sort this list of coordinates first by row index (ascending) and then by column index (ascending) to establish the scanline order.
4.  If the list of non-Orange pixel coordinates is empty, stop and return the initial output grid copy.
5.  Identify the coordinates of the last pixel in the sorted list. Look up the color of this pixel in the *input* grid.
6.  Choose a sequence of three colors (the cycle) based on the color of that last pixel:
    *   If the last pixel's color is Magenta (6), the color cycle is [Red (2), Gray (5), Azure (8)].
    *   Otherwise (if the last pixel's color is not Magenta (6)), the color cycle is [Red (2), Azure (8), Gray (5)].
7.  Iterate through the sorted list of non-Orange pixel coordinates, keeping track of the position (index `i`, starting from 0) of each coordinate in the list.
8.  For each coordinate at index `i`, determine the replacement color by selecting the color from the chosen cycle at position `i modulo 3`.
9.  Update the pixel at the current coordinate in the *output* grid with this replacement color.
10. After iterating through all non-Orange pixel coordinates, return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a conditional cyclical color replacement rule
    for non-background pixels.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    
    background_color = 7  # Orange

    # Find coordinates of non-background pixels
    non_background_coords = []
    rows, cols = input_array.shape
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] != background_color:
                non_background_coords.append((r, c))

    # If there are no non-background pixels, return the original grid copy
    if not non_background_coords:
        return output_array.tolist() # Return as list of lists

    # Sort coordinates by row, then column (scanline order)
    # Note: Python's default tuple sorting achieves this naturally
    non_background_coords.sort() 

    # Get the color of the last non-background pixel in the scanline order
    last_coord = non_background_coords[-1]
    last_pixel_color = input_array[last_coord[0], last_coord[1]]

    # Determine the color cycle based on the last pixel's color
    magenta_color = 6
    red_color = 2
    gray_color = 5
    azure_color = 8
    
    if last_pixel_color == magenta_color:
        color_cycle = [red_color, gray_color, azure_color] # Cycle B: [2, 5, 8]
    else:
        color_cycle = [red_color, azure_color, gray_color] # Cycle A: [2, 8, 5]

    # Iterate through the sorted non-background pixels and apply the cyclical replacement
    for i, (r, c) in enumerate(non_background_coords):
        replacement_color = color_cycle[i % 3]
        output_array[r, c] = replacement_color

    # Convert the result back to a list of lists
    return output_array.tolist()