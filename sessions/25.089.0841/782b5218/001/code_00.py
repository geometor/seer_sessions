import numpy as np
from collections import Counter

"""
Identify the 'separator' row, which is the first row from the top containing at least one red (2) pixel.
Initialize the output grid with the same dimensions as the input, filled with white (0).
Copy only the red (2) pixels from the input's separator row to the output's separator row.
Determine the 'fill_color' by finding the most frequent non-white (0) color in the region of the input grid *strictly below* the separator row. If there's a tie in frequency, choose the color with the smallest numerical index.
Fill all rows in the output grid *below* the separator row entirely with this 'fill_color'. If no non-white pixels exist below the separator row, these rows remain white (0).
Rows above the separator row in the output grid remain white (0).
"""

def find_separator_row(grid_np):
    """Finds the index of the first row containing the color red (2)."""
    height = grid_np.shape[0]
    for r in range(height):
        if 2 in grid_np[r, :]:
            return r
    return -1 # Indicate not found

def find_fill_color(grid_np, separator_row_index):
    """Finds the most frequent non-white color below the separator row."""
    height = grid_np.shape[0]
    
    # Check if there are rows below the separator
    if separator_row_index + 1 >= height:
        return None # No rows below

    # Extract the subgrid below the separator row
    subgrid = grid_np[separator_row_index + 1 :, :]
    
    # Flatten and filter out white (0) pixels
    non_white_pixels = subgrid[subgrid != 0].flatten()

    if non_white_pixels.size == 0:
        return None # No non-white pixels below

    # Count frequencies
    counts = Counter(non_white_pixels)
    
    # Find the maximum frequency
    max_freq = 0
    for color in counts:
        if counts[color] > max_freq:
            max_freq = counts[color]
            
    # Find all colors with the maximum frequency
    most_frequent_colors = []
    for color in counts:
        if counts[color] == max_freq:
            most_frequent_colors.append(color)
            
    # If multiple colors have the same max frequency, return the smallest index
    fill_color = min(most_frequent_colors)
    
    return fill_color

def transform(input_grid):
    """
    Transforms the input grid based on a red separator line and the most 
    frequent color below it.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np)

    # 1. Find the separator row index
    separator_row_index = find_separator_row(input_np)

    # If no separator row found, return the empty white grid (or input?)
    # Based on examples, a separator row seems guaranteed. 
    # If not found, current logic returns all white grid which might be reasonable.
    if separator_row_index == -1:
         # Or perhaps return input_np.tolist() ? Let's stick to all white for now.
         return output_grid.tolist() 

    # 3. Copy red (2) pixels from the separator row in input to output
    for c in range(width):
        if input_np[separator_row_index, c] == 2:
            output_grid[separator_row_index, c] = 2

    # 4. Find the fill color from the region below the separator row in the input
    fill_color = find_fill_color(input_np, separator_row_index)

    # 5. Fill rows below the separator row in the output grid with the fill color
    # Only fill if a valid fill_color was found and if there are rows below
    if fill_color is not None and separator_row_index + 1 < height:
        output_grid[separator_row_index + 1 :, :] = fill_color
        
    # 2. & 6. Initialization already handles making rows above white.

    # Return the result as a list of lists
    return output_grid.tolist()