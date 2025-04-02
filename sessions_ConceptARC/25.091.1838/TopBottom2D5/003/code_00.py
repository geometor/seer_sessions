import numpy as np
from scipy.ndimage import label

"""
Identifies all distinct objects in the input grid, where an object is defined 
as an orthogonally connected group of pixels of the same non-background color. 
Determines the bottom-most row index (maximum row index) for each object. 
Finds the maximum bottom-most row index among all objects across the grid. 
Constructs an output grid containing only the object(s) whose bottom-most row 
index matches this overall maximum value, preserving their original colors and positions. 
All other objects are removed (replaced by the background color).
"""

def transform(input_grid):
    """
    Filters the input grid to keep only the object(s) reaching the lowest row index.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)
    background_color = 0
    
    # Define orthogonal connectivity structure (no diagonals)
    connectivity_structure = np.array([[0, 1, 0],
                                       [1, 1, 1],
                                       [0, 1, 0]])

    # Find unique non-background colors present in the grid
    unique_colors = np.unique(input_grid[input_grid != background_color])

    # Store properties of all identified objects
    all_objects = []
    max_overall_bottom_row = -1 # Initialize to track the lowest point reached by any object

    # Iterate through each unique non-background color to find its objects
    for color in unique_colors:
        # Create a mask for the current color
        color_mask = (input_grid == color)
        
        # Find connected components (objects) for this specific color using orthogonal connectivity
        labeled_array, num_features = label(color_mask, structure=connectivity_structure)
        
        # If objects of this color are found
        if num_features > 0:
            # Process each object of the current color
            for i in range(1, num_features + 1):
                # Create a mask for the individual object
                object_mask = (labeled_array == i)
                # Find the coordinates of the object's pixels
                rows, _ = np.where(object_mask)
                # Determine the bottom-most row index for this object
                bottom_row = np.max(rows)
                
                # Store the object's properties
                all_objects.append({
                    'color': color,
                    'mask': object_mask,
                    'bottom_row': bottom_row
                })
                
                # Update the overall maximum bottom row found so far
                if bottom_row > max_overall_bottom_row:
                    max_overall_bottom_row = bottom_row

    # If no non-background objects were found at all, return the empty grid
    if max_overall_bottom_row == -1:
        return output_grid

    # Filter the objects: keep only those whose bottom row matches the overall maximum
    objects_to_keep = [obj for obj in all_objects if obj['bottom_row'] == max_overall_bottom_row]

    # Construct the output grid by drawing the selected objects
    for obj in objects_to_keep:
        # Apply the object's mask and color to the output grid
        output_grid[obj['mask']] = obj['color']
        
    return output_grid