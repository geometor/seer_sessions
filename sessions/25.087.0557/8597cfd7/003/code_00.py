import numpy as np

"""
This program transforms an input grid based on the counts of red (2) and yellow (4) 
pixels located *below* a horizontal gray (5) line within the grid. 
The output is a 2x2 grid filled with a single color: yellow (4) if the count of 
yellow pixels below the gray line exceeds the count of red pixels below the gray 
line by more than 1; otherwise, the output color is red (2).
"""

def find_gray_line_row(grid):
    """
    Finds the row index of the horizontal line made entirely of gray (5) pixels.

    Args:
        grid (np.ndarray): The input grid as a numpy array.

    Returns:
        int: The row index of the gray line. Returns -1 if no such line is found.
    """
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 5):
            return r
    return -1 # Should not happen based on examples, but good practice

def count_colors_below_row(grid, row_index, color_value):
    """
    Counts the occurrences of a specific color in the grid below a given row index.

    Args:
        grid (np.ndarray): The input grid as a numpy array.
        row_index (int): The index of the row *above* the region to count in.
        color_value (int): The color value to count.

    Returns:
        int: The count of the specified color below the given row index.
    """
    if row_index < 0 or row_index >= grid.shape[0] - 1:
        # No region below if gray line is last row or not found
        return 0 
        
    region_below = grid[row_index + 1:, :]
    return np.count_nonzero(region_below == color_value)

def transform(input_grid):
    """
    Transforms the input grid based on counts of red/yellow pixels below the gray line.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2x2 list of lists filled with the determined color.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)

    # 1. Find the horizontal gray line
    gray_line_index = find_gray_line_row(grid)

    # Handle case where gray line might not be found (although unlikely based on task)
    if gray_line_index == -1:
        # Default behavior or error handling - based on examples, let's assume it exists.
        # For robustness, perhaps return a default grid or raise an error.
        # Based on analysis, maybe default to red if unsure? Let's stick to the rule.
        # If the structure is violated, the rule cannot apply. Let's return an empty 2x2.
         return np.full((2, 2), 0, dtype=int).tolist() # Default to white 

    # 2. Isolate the region below (implicitly done in counting function)
    
    # 3. Count red pixels below the gray line
    red_count_below = count_colors_below_row(grid, gray_line_index, 2)

    # 4. Count yellow pixels below the gray line
    yellow_count_below = count_colors_below_row(grid, gray_line_index, 4)

    # 5. & 6. Determine the output color based on the comparison rule
    if yellow_count_below - red_count_below > 1:
        output_color = 4 # Yellow
    else:
        output_color = 2 # Red

    # 7. Construct the 2x2 output grid
    output_grid = np.full((2, 2), output_color, dtype=int)

    # Convert back to list of lists for ARC format
    return output_grid.tolist()