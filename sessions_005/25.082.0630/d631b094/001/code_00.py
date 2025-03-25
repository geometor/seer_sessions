"""
The transformation rule isolates the non-zero colored pixels and then constructs new grid from them. The rule seems to count non-zero value in rows, then columns, if value are present, construct a new row, and do the same with columns.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Find non-zero pixels and their counts in rows and columns
    non_zero_pixels = []
    row_counts = {}
    col_counts = {}

    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            pixel_value = input_array[i, j]
            if pixel_value != 0:
                if pixel_value not in non_zero_pixels:
                    non_zero_pixels.append(pixel_value)
                row_counts.setdefault(pixel_value, 0)
                col_counts.setdefault(pixel_value, 0)

    for pixel_value in non_zero_pixels:
        for i in range(input_array.shape[0]):
            if pixel_value in input_array[i,:]:
                row_counts[pixel_value]+=1

        for j in range(input_array.shape[1]):
             if pixel_value in input_array[:,j]:
                col_counts[pixel_value]+=1
    
    # Determine output grid size and color
    output_rows = 0
    output_cols = 0
    output_color = 0

    for pixel in non_zero_pixels:
        output_rows = max(output_rows,row_counts[pixel])
        output_cols = max(output_cols, col_counts[pixel])
        output_color = pixel #all the same color, arbitrary pick last
    # Construct output grid
    if output_rows > 0 and output_cols > 0 :
        output_grid = np.full((output_rows, output_cols), output_color)
    elif output_rows > 0:
        output_grid = np.full((output_rows, ), output_color)
    elif output_cols > 0 :
        output_grid = np.full((output_cols,), output_color)
    else:
        output_grid = np.array([])

    return output_grid.tolist()