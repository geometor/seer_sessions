import numpy as np
from collections import Counter

def find_horizontal_line(grid, color):
    """Finds the row index of the first complete horizontal line of a given color."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == color):
            return r
    return -1 # Return -1 if no such line is found

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Find the row index of the solid gray (5) horizontal line ('gray_row').
    2. Determine the 'height' parameter by counting the number of azure (8) pixels in the first row (row 0).
    3. Identify the 'data_row', which is two rows below the 'gray_row'.
    4. Count the occurrences of each non-white (0) color in the 'data_row'.
    5. For each color 'c' whose count in the 'data_row' equals the 'height' parameter:
       a. Identify the column indices where 'c' appears in the 'data_row'.
       b. In the output grid, draw vertical lines of color 'c' and length 'height' in these columns.
       c. These vertical lines start from the row immediately above the 'gray_row' (gray_row - 1) and extend upwards for 'height' rows.
    6. The output grid is initialized as a copy of the input grid, and the vertical lines are drawn onto this copy.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height_grid, width_grid = input_grid_np.shape

    # 1. Find the gray line row index
    gray_color = 5
    gray_row = find_horizontal_line(input_grid_np, gray_color)
    if gray_row == -1:
        # Handle cases where the gray line might not exist as expected
        # For this specific task based on examples, assume it always exists.
        print("Warning: Gray line not found.")
        return output_grid.tolist() 

    # 2. Determine the height parameter from the first row
    azure_color = 8
    draw_height = np.count_nonzero(input_grid_np[0, :] == azure_color)
    if draw_height == 0:
         # If no azure pixels, no drawing happens based on the observed pattern
         return output_grid.tolist()

    # 3. Identify the data row (assuming it's 2 rows below the gray line)
    data_row_index = gray_row + 2
    if data_row_index >= height_grid:
        # Handle cases where data row is outside grid bounds
        print("Warning: Data row index out of bounds.")
        return output_grid.tolist()
    data_row = input_grid_np[data_row_index, :]

    # 4. Count occurrences of each non-white color in the data row
    color_counts = Counter(c for c in data_row if c != 0)

    # 5. Iterate through colors, check counts, and draw lines
    for color, count in color_counts.items():
        if count == draw_height:
            # Find columns where this color appears
            color_indices = np.where(data_row == color)[0]
            
            # Determine the rows for drawing
            start_row = gray_row - draw_height
            end_row = gray_row # Exclusive endpoint for slicing

            # Ensure drawing rows are within grid bounds
            if start_row < 0:
                print(f"Warning: Drawing starts above grid for color {color}.")
                start_row = 0 # Clamp to top edge if necessary
            
            if start_row >= end_row:
                print(f"Warning: Invalid drawing row range for color {color}.")
                continue # Skip drawing if range is invalid

            # Draw the vertical lines
            for col in color_indices:
                output_grid[start_row:end_row, col] = color

    return output_grid.tolist()