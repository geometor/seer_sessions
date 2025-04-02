import numpy as np

"""
Identify the vertical yellow line (color 4) that acts as a separator in the input grid. 
Extract the portion of the grid to the right of this yellow line. 
This extracted subgrid becomes the output grid.
"""

def find_delimiter_column(grid_array):
    """Finds the index of the first column consisting entirely of a single color (acting as a delimiter)."""
    height, width = grid_array.shape
    for c in range(width):
        column = grid_array[:, c]
        # Check if all elements in the column are the same and non-zero (usually background is 0)
        # In this specific task, the delimiter is yellow (4)
        if np.all(column == 4):
            return c
    return -1 # Indicate not found, though examples suggest it's always present

def transform(input_grid):
    """
    Extracts the part of the grid to the right of the vertical yellow line.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input grid to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Find the column index of the vertical yellow delimiter line
    delimiter_col = -1
    height, width = input_array.shape
    for c in range(width):
        if np.all(input_array[:, c] == 4):
            delimiter_col = c
            break
            
    # If no delimiter is found (shouldn't happen based on examples), return empty or original?
    # Based on the task structure, we expect a delimiter. Let's proceed assuming it's found.
    if delimiter_col == -1:
        # Fallback or error handling - returning an empty grid for now
        # Or perhaps return the original if no clear delimiter? 
        # Let's assume delimiter is always present as per examples.
        # A more robust solution might be needed if this assumption fails.
        print("Warning: Delimiter column (yellow line) not found.")
        # Returning the input might be safer if the pattern isn't met
        # return input_grid 
        # For now, stick to the observed pattern: extract right side
        # If no delimiter, maybe the whole grid is the 'right side'? Unlikely.
        # Let's try returning an empty grid of the same height.
        return [[] for _ in range(height)]


    # Extract the portion of the grid to the right of the delimiter column
    # The slice starts from the column *after* the delimiter
    output_array = input_array[:, delimiter_col + 1:]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
