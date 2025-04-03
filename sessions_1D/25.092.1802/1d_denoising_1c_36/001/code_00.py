import numpy as np
from collections import defaultdict

"""
Identify all contiguous horizontal blocks of non-background (non-zero) color in the input 1D grid.
Calculate the size (length) of each block.
Find the maximum size among all blocks.
Create an output grid of the same dimensions as the input, initialized with the background color (0).
Copy only the block(s) that have the maximum size to the output grid, maintaining their original positions and color.
"""

def find_objects_1d(grid_row):
    """
    Finds contiguous blocks of non-zero colors in a 1D grid row.

    Args:
        grid_row: A list representing a single row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys 'color', 'indices' (list of column indices), and 'size'.
    """
    objects = []
    n = len(grid_row)
    visited = [False] * n
    
    for i, pixel in enumerate(grid_row):
        # Check for a non-background pixel that hasn't been visited
        if pixel != 0 and not visited[i]:
            color = pixel
            current_object_indices = []
            q = [i] # Use a queue or stack for potential expansion (though simple iteration works for 1D)
            visited[i] = True
            
            # Explore contiguous pixels of the same color
            start_index = i
            end_index = i
            while end_index + 1 < n and grid_row[end_index + 1] == color:
                end_index += 1
                visited[end_index] = True

            # Store indices for this object
            current_object_indices = list(range(start_index, end_index + 1))

            # Add the found object to the list
            if current_object_indices:
                 objects.append({
                     "color": color,
                     "indices": current_object_indices, 
                     "size": len(current_object_indices)
                 })
                 # Ensure loop continues after the found object
                 # The outer loop's 'i' will naturally increment past the visited indices
    return objects


def transform(input_grid):
    """
    Filters a 1D grid to keep only the largest contiguous block(s) of non-background color.

    Args:
        input_grid: A list representing the 1xN input grid.

    Returns:
        A list representing the 1xN output grid.
    """
    # Ensure input is treated as a single row (list)
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         # If input looks like [[...]], extract the first row
         grid_row = input_grid[0]
    elif isinstance(input_grid, list):
         # Assume it's already a flat list
         grid_row = input_grid
    elif isinstance(input_grid, np.ndarray):
         # Handle numpy array input
         if input_grid.ndim == 2 and input_grid.shape[0] == 1:
              grid_row = input_grid[0].tolist()
         elif input_grid.ndim == 1:
              grid_row = input_grid.tolist()
         else:
              raise ValueError("Input grid must be 1-dimensional or 1xN")
    else:
        raise TypeError("Input grid must be a list or numpy array")

    # Find all contiguous non-background objects
    objects = find_objects_1d(grid_row)

    # If no objects found, return a grid of zeros with the same size
    if not objects:
        return [0] * len(grid_row) # Or return grid_row if input was already all zeros

    # Find the maximum size among the objects
    max_size = 0
    for obj in objects:
        if obj['size'] > max_size:
            max_size = obj['size']

    # Initialize the output grid with background color (0)
    output_grid_row = [0] * len(grid_row)

    # Copy only the largest object(s) to the output grid
    for obj in objects:
        if obj['size'] == max_size:
            color = obj['color']
            for index in obj['indices']:
                output_grid_row[index] = color

    # Return the modified grid row
    # The expected ARC format might be [[...]], so wrap it if needed.
    # Based on the examples provided, the output is also a flat list.
    return output_grid_row