"""
Identify the horizontal separator band consisting entirely of white pixels (0) that spans the full width of the input grid. Extract the region of the grid located entirely below this separator band. The output grid is this extracted lower region.
"""

import numpy as np

def find_separator_end(grid):
    """
    Finds the index of the row immediately following the last row of the first 
    continuous horizontal separator band made entirely of white pixels (0).
    Returns -1 if no such separator is found or if it's at the very bottom.
    """
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    first_separator_row = -1
    last_separator_row = -1

    # Find the first row that is all white
    for r in range(grid_height):
        if all(grid[r][c] == 0 for c in range(grid_width)):
            first_separator_row = r
            break # Found the start of the separator

    if first_separator_row == -1:
        return -1 # No separator found

    # Find the end of this continuous separator band
    last_separator_row = first_separator_row
    for r in range(first_separator_row + 1, grid_height):
        if all(grid[r][c] == 0 for c in range(grid_width)):
            last_separator_row = r
        else:
            break # End of the separator band

    # The lower region starts on the row after the last separator row
    start_of_lower_region = last_separator_row + 1

    # Check if the separator extends to the bottom or if there's nothing below it
    if start_of_lower_region >= grid_height:
        return -1 # Nothing below the separator

    return start_of_lower_region


def transform(input_grid):
    """
    Transforms the input grid by extracting the portion below the first
    horizontal all-white separator band.
    
    Args:
        input_grid (list of lists or numpy array): The input grid.
        
    Returns:
        numpy array: The extracted lower portion of the grid.
    """
    # Convert input to numpy array for easier slicing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find the starting row index of the lower region
    start_row = find_separator_end(grid_np.tolist()) # Use list version for iteration convenience

    # Check if a valid lower region was found
    if start_row == -1:
        # Handle cases where no separator is found or nothing is below it
        # Based on examples, this shouldn't happen, but returning an empty grid or raising an error might be options.
        # For now, let's assume a valid structure based on examples and return the original if structure is unexpected.
        # A better approach might be needed if test cases violate this structure.
         print("Warning: Separator or lower region not found as expected.")
         # Returning an empty array might be safer depending on expected behavior for edge cases
         return np.array([[]], dtype=int) 

    # Extract the lower region
    # Slicing starts from start_row to the end of the array
    output_grid = grid_np[start_row:, :]

    return output_grid
