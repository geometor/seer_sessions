import numpy as np

"""
Identify all 3x3 subgrids within the input grid composed entirely of non-white (non-zero) pixels. 
For each such 3x3 subgrid, count the number of unique non-white colors it contains.
Select the 3x3 subgrid that has exactly 3 unique non-white colors.
The output grid is this selected 3x3 subgrid.
"""

def find_potential_objects(grid):
    """
    Finds all 3x3 subgrids that do not contain the background color (0).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (row, col, subgrid).
              row, col are the top-left coordinates of the 3x3 subgrid.
              subgrid is the 3x3 np.array.
    """
    potential_objects = []
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            # Check if the subgrid contains any background pixels (0)
            if 0 not in subgrid:
                potential_objects.append((r, c, subgrid))
    return potential_objects

def count_unique_colors(subgrid):
    """
    Counts the number of unique non-zero colors in a subgrid.

    Args:
        subgrid (np.array): The subgrid to analyze.

    Returns:
        int: The number of unique non-zero colors.
    """
    # Flatten the subgrid to easily iterate through pixels
    pixels = subgrid.flatten()
    # Filter out background color (0) although find_potential_objects should ensure this
    non_white_pixels = pixels[pixels != 0]
    # Find unique colors
    unique_colors = set(non_white_pixels)
    return len(unique_colors)

def transform(input_grid):
    """
    Finds and returns the 3x3 non-white object with exactly 3 unique colors.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The 3x3 output grid, or None if no such object is found.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Find all potential 3x3 objects (no white pixels)
    potential_objects = find_potential_objects(grid_np)
    
    # Initialize variable to store the target object
    output_grid_np = None
    
    # Iterate through potential objects to find the one with 3 unique colors
    for r, c, subgrid in potential_objects:
        # Count the unique non-white colors in the subgrid
        unique_color_count = count_unique_colors(subgrid)
        
        # Check if the count is exactly 3
        if unique_color_count == 3:
            # Found the target object, store it and break (assuming only one)
            output_grid_np = subgrid
            break
            
    # Convert the result back to list of lists format if found
    if output_grid_np is not None:
        return output_grid_np.tolist()
    else:
        # Handle case where no suitable object is found (return None or empty list based on expected behavior)
        # Based on examples, we expect one object to always match.
        # Returning None might be appropriate if the problem guarantees a solution exists.
        # For robustness, we could return an empty grid or raise an error.
        # Let's return None for now.
        return None 
