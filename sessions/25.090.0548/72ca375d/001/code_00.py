import numpy as np
from scipy.ndimage import label

"""
Identifies all distinct non-white objects in the input grid.
Sorts these objects based on their color index in ascending order.
Selects the object corresponding to the middle color in the sorted list.
Calculates the bounding box of the selected object.
Returns the portion of the input grid defined by this bounding box as the output grid.
"""

def find_colored_objects(grid):
    """
    Finds all distinct colored objects and their properties (color, pixels, bounding box).
    
    Args:
        grid (np.array): The input grid.

    Returns:
        dict: A dictionary where keys are colors and values are dicts
              containing 'coords' (list of pixel coordinates) and 
              'bounding_box' (min_row, min_col, max_row, max_col).
    """
    objects = {}
    # Identify all unique non-background (non-zero) colors present in the grid
    unique_colors = np.unique(grid[grid != 0]) 
    
    for color in unique_colors:
        # Create a binary mask isolating pixels of the current color
        mask = (grid == color)
        
        # Find coordinates of all pixels for this color
        coords = np.argwhere(mask)
        
        # If pixels of this color exist, calculate the bounding box
        if coords.size > 0:
             min_row = np.min(coords[:, 0])
             max_row = np.max(coords[:, 0])
             min_col = np.min(coords[:, 1])
             max_col = np.max(coords[:, 1])
             bounding_box = (min_row, min_col, max_row, max_col)
             
             # Store the object's properties
             objects[color] = {
                 'coords': coords,
                 'bounding_box': bounding_box
             }
             
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule:
    1. Find all distinct non-white objects.
    2. Sort the objects by their color index.
    3. Select the object with the middle color index.
    4. Output the subgrid defined by the selected object's bounding box.
    
    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find all colored objects and their properties using the helper function
    objects = find_colored_objects(grid_np)
    
    # Get the unique colors present (which are the keys of the 'objects' dictionary)
    colors = sorted(list(objects.keys()))
    
    # Handle edge case: if no non-white objects are found, return an empty grid
    if not colors:
        # Note: Returning empty list of lists might be ambiguous.
        # Depending on expected format, might return [[]] or handle differently.
        # For now, returning based on common ARC patterns.
        return [[]] 

    # Determine the middle color from the sorted list of colors.
    # Integer division // handles both odd and even lengths correctly,
    # selecting the lower-middle element for even lengths (e.g., index 1 for length 4).
    # Based on examples, we expect an odd number (3).
    middle_index = len(colors) // 2
    selected_color = colors[middle_index]
    
    # Retrieve the bounding box information for the object with the selected middle color
    selected_object = objects[selected_color]
    min_row, min_col, max_row, max_col = selected_object['bounding_box']
    
    # Extract the subgrid (crop) from the original input grid 
    # using the calculated bounding box coordinates.
    # Slicing is exclusive of the end index, so add 1 to max_row and max_col.
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]
    
    # Convert the resulting NumPy array back to a list of lists format for the output
    return output_grid_np.tolist() 