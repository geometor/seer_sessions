import numpy as np

"""
Transforms a 1xN input grid by identifying a single contiguous horizontal line 
of a non-white color. This line is then shifted 3 positions to the right in the 
output grid, while maintaining its original color and length. The rest of the 
output grid is filled with the background color (white, 0). The input line is 
consistently observed to start at index 1 in the provided examples.
"""

def find_line_properties(grid_row):
    """
    Finds the start index, color, and length of the first non-white horizontal line segment.

    Args:
        grid_row (list): A list representing the single row of the grid.

    Returns:
        tuple: (start_index, color, length) or (None, None, None) if no line is found.
    """
    start_index = -1
    color = 0
    length = 0
    
    # Iterate through the row to find the first non-white pixel
    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found the start of the line
            start_index = i
            color = pixel
            length = 1
            # Continue to find the end of this contiguous segment of the same color
            for j in range(i + 1, len(grid_row)):
                if grid_row[j] == color:
                    length += 1
                else:
                    break # End of the line segment
            # Assuming only one line exists based on examples, return immediately
            return start_index, color, length 
            
    # Return None if no non-white pixel was found
    return None, None, None 

def transform(input_grid):
    """
    Applies the line shifting transformation to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid (expected 1xN).

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Ensure input is not empty
    if not input_grid or not input_grid[0]:
        # Return an empty grid or handle error appropriately
        return [[]] 

    # Determine grid dimensions (assuming 1 row based on task)
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize output_grid with background color (0)
    # Creates a new list of lists, crucial for not modifying the input
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # --- Core Transformation Logic ---
    # As the grid is 1xN, we work directly with the first (and only) row
    input_row = input_grid[0]
    output_row = output_grid[0] # Get a reference to the output row to modify

    # 1. Object Identification: Find the line in the input row
    start_index_input, line_color, line_length = find_line_properties(input_row)

    # 2. Proceed only if a line was actually found
    if start_index_input is not None:
        # 3. Transformation Calculation: Define the shift and calculate new start
        shift_distance = 3
        start_index_output = start_index_input + shift_distance

        # 4. Output Generation: Draw the shifted line in the output row
        for i in range(line_length):
            # Calculate the column index in the output grid for the current pixel of the line
            current_col_output = start_index_output + i
            
            # Check bounds: Ensure the pixel position is within the grid width
            if 0 <= current_col_output < cols:
                output_row[current_col_output] = line_color
                
    # The output_grid (specifically its output_row) has been modified in place
    return output_grid