import numpy as np

"""
1. Find the horizontal line made entirely of gray pixels (color 5) in the input grid.
2. Isolate the region of the grid that lies below this gray line.
3. Count the total number of red pixels (color 2) within this lower region.
4. Count the total number of yellow pixels (color 4) within this lower region.
5. Compare the count of red pixels to the count of yellow pixels.
6. If the red pixel count is greater than or equal to the yellow pixel count, create a 2x2 output grid filled entirely with red pixels (color 2).
7. Otherwise (if the yellow pixel count is strictly greater than the red pixel count), create a 2x2 output grid filled entirely with yellow pixels (color 4).
"""

def find_separator_row(grid):
    """Finds the row index of the horizontal gray separator line."""
    for r_idx, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return r_idx
    return -1 # Should not happen based on examples

def count_color_in_region(grid, color):
    """Counts the occurrences of a specific color in a grid region."""
    return np.count_nonzero(grid == color)

def transform(input_grid):
    """
    Transforms the input grid based on comparing red and yellow pixel counts
    below a gray separator line.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # 1. Find the horizontal line made entirely of gray pixels (color 5)
    separator_row_index = -1
    for r in range(height):
        if np.all(grid_np[r, :] == 5):
            separator_row_index = r
            break
    
    # Handle cases where separator might not be found (though unlikely based on examples)
    if separator_row_index == -1:
        # Default or error handling - maybe return an empty grid or raise error
        # Based on examples, let's assume it's always found.
        # If it's the last row, the region below is empty.
        pass 

    # 2. Isolate the region of the grid that lies below this gray line.
    # The region starts from the row immediately after the separator
    lower_region = grid_np[separator_row_index + 1:, :]

    # 3. Count the total number of red pixels (color 2) within this lower region.
    red_count = count_color_in_region(lower_region, 2)

    # 4. Count the total number of yellow pixels (color 4) within this lower region.
    yellow_count = count_color_in_region(lower_region, 4)

    # 5. Compare the count of red pixels to the count of yellow pixels.
    # 6. & 7. Determine the output color and create the output grid.
    if red_count >= yellow_count:
        output_color = 2  # Red
    else:
        output_color = 4  # Yellow

    # Create a 2x2 output grid filled entirely with the determined color.
    output_grid_np = np.full((2, 2), output_color, dtype=int)

    # Convert back to list of lists format for the ARC standard
    output_grid = output_grid_np.tolist()

    return output_grid