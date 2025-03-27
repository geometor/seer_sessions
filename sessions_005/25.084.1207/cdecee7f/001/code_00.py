"""
Extract all non-white pixels from the input grid using a column-major scan (top-to-bottom within each column, then left-to-right across columns). If 6 or more colors are extracted, swap the 4th and 6th colors in the extracted sequence. Fill a 3x3 output grid with these colors sequentially (row-major: left-to-right, top-to-bottom), padding with white (0) if fewer than 9 colors were extracted.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed 3x3 output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Initialize an empty list to store the colors of non-white pixels
    extracted_colors = []

    # 2. Iterate through columns (left to right)
    for col in range(width):
        # 3. Iterate through rows (top to bottom)
        for row in range(height):
            # 4. If a cell contains a non-white color, append its value
            if grid[row, col] != 0:
                extracted_colors.append(grid[row, col])

    # 5. Check if 6 or more colors were collected and swap if necessary
    if len(extracted_colors) >= 6:
        # Swap element at index 3 (4th color) with element at index 5 (6th color)
        extracted_colors[3], extracted_colors[5] = extracted_colors[5], extracted_colors[3]

    # 6. Create a new 3x3 grid, initially filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # 7. Iterate through the cells of the 3x3 output grid (row-major order)
    color_index = 0
    for r_out in range(3):
        for c_out in range(3):
            # 8. & 9. Place the next available color or leave as white
            if color_index < len(extracted_colors):
                output_grid[r_out, c_out] = extracted_colors[color_index]
                color_index += 1
            else:
                # No more colors left, cell remains 0 (white)
                break # Optimization: can break inner loop once colors run out
        if color_index >= len(extracted_colors):
             break # Optimization: can break outer loop once colors run out


    # 10. Return the resulting 3x3 grid as a list of lists
    return output_grid.tolist()
