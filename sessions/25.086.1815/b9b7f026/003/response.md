```python
import numpy as np
from scipy import ndimage

"""
Identify the color of the unique object within the input grid that contains an internal white hole.
An internal white hole consists of one or more white pixels completely surrounded (cardinally) by pixels of the object's color.
The output is a 1x1 grid containing the color of this unique object.
"""

def find_color_of_object_with_hole(input_grid):
    """
    Finds the unique object containing an internal white hole and returns its color.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        int: The color of the object with a hole, or None if no such object is found.
    """
    unique_colors = np.unique(input_grid)
    rows, cols = input_grid.shape

    # Structure for connectivity (cardinal directions)
    connectivity_structure = np.array([[0, 1, 0],
                                       [1, 1, 1],
                                       [0, 1, 0]], dtype=bool)

    # Iterate through each non-background color present in the grid
    for color in unique_colors:
        if color == 0:  # Skip background
            continue

        # Create a mask for all pixels of the current color
        color_mask = (input_grid == color)

        # Label connected components (objects) of this color
        # Background=0 ensures only components within color_mask are labeled
        labeled_array, num_labels = ndimage.label(color_mask, structure=connectivity_structure)

        # Iterate through each distinct object found for this color
        for label in range(1, num_labels + 1):
            # Create a mask for the specific object
            obj_mask = (labeled_array == label)

            # --- Detect Holes ---
            # Fill holes within the object's boolean mask
            filled_mask = ndimage.binary_fill_holes(obj_mask, structure=connectivity_structure)
            
            # Identify pixels that were filled (potential hole locations)
            hole_mask = filled_mask & ~obj_mask
            
            # Check if any of these filled locations correspond to white pixels (0) in the original grid
            # and ensure the hole_mask is not empty
            if hole_mask.any() and np.any(input_grid[hole_mask] == 0):
                 # Found the object with a white hole, return its color
                 return int(color)

    # Should not be reached based on task examples, but included for robustness
    print("Warning: No object with an internal white hole found.")
    return None


def transform(input_grid):
    """
    Identifies the unique object with an internal white hole and returns its color in a 1x1 grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 1x1 numpy array containing the selected color.
    """
    # Find the color of the object containing a hole
    target_color = find_color_of_object_with_hole(input_grid)

    # Handle case where no object with a hole is found (return background color 0)
    if target_color is None:
        target_color = 0

    # Create the 1x1 output grid
    output_grid = np.array([[target_color]])

    return output_grid
```