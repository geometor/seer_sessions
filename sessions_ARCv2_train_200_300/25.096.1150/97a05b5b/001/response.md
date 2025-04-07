```python
"""
Identify all connected components (shapes) in the input grid consisting of non-zero cells.
Calculate the area (count of non-zero cells) for each shape.
Select the shape with the largest area.
Determine the bounding box (minimum rectangle) containing the selected shape.
Extract the subgrid from the input corresponding to this bounding box as the output.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts the largest connected non-zero object from the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the subgrid containing the largest object.
        Returns an empty list if the input grid contains no non-zero elements.
    """
    # Convert input to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Check if the grid contains any non-zero elements
    if np.sum(grid_np) == 0:
        return [] # Or handle as appropriate, e.g., return [[]] or original

    # Label connected components of non-zero elements
    # structure defines connectivity (4-connectivity in this case)
    structure = np.array([[0,1,0], [1,1,1], [0,1,0]], dtype=bool) 
    labeled_array, num_features = label(grid_np > 0, structure=structure)

    # Handle case where no features are found (should be caught by the sum check, but good practice)
    if num_features == 0:
        return []

    # Calculate the size (area) of each component
    component_sizes = np.bincount(labeled_array.ravel())

    # Find the label of the largest component (ignoring background label 0)
    # component_sizes[0] is the count of background pixels (0s)
    if len(component_sizes) > 1:
        largest_component_label = np.argmax(component_sizes[1:]) + 1
    else:
        # This case should ideally not be reached if num_features > 0 and grid has non-zeros
        # but handles edge cases like a grid with only one non-zero cell labeled '1'.
         largest_component_label = 1 if num_features == 1 else -1 # -1 indicates error or unexpected state
         if largest_component_label == -1:
             # Handle error or return empty if no valid component found despite num_features > 0
             print("Warning: No valid component found despite non-zero elements.")
             return []


    # Find the bounding box of the largest component
    # find_objects returns a list of slice objects for each labeled feature
    objects_slices = find_objects(labeled_array)
    
    # Ensure the largest component label is valid index for objects_slices
    if largest_component_label - 1 < len(objects_slices):
        bounding_box = objects_slices[largest_component_label - 1]
    else:
        # Handle error: label mismatch or issue with find_objects
        print(f"Error: Largest component label {largest_component_label} out of bounds for slices.")
        return []

    # Extract the subgrid corresponding to the bounding box from the *original* input grid
    output_grid_np = grid_np[bounding_box]

    # Convert the numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```