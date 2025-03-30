```python
import numpy as np
from scipy.ndimage import label

"""
Transformation Rule:
1. Identify all distinct objects in the input grid. An object is a group of orthogonally connected non-white (0) pixels (colors 1 and 8).
2. Count the number of azure (8) pixels within each object.
3. Create an output grid of the same dimensions as the input, initialized to white (0).
4. Copy objects from the input to the output grid only if they contain zero (0) or one (1) azure (8) pixel. Objects with two or more azure pixels are discarded (left as white in the output).
"""

def get_objects(grid_np, diagonal=False):
    """
    Identifies connected objects of non-background pixels in a grid.

    Args:
        grid_np: A NumPy array representing the grid.
        diagonal: Boolean indicating if diagonal connections count.

    Returns:
        A list of objects, where each object is a dictionary containing:
        'id': A unique integer identifier.
        'coords': A list of [row, col] coordinates for the object's pixels.
        'values': A list of pixel values for the object.
    """
    background_color = 0
    objects_mask = grid_np != background_color
    # Define connectivity structure: 4-connectivity (orthogonal) or 8-connectivity (diagonal)
    structure = np.array([[0,1,0],[1,1,1],[0,1,0]]) if not diagonal else np.array([[1,1,1],[1,1,1],[1,1,1]])
    
    labeled_array, num_features = label(objects_mask, structure=structure)
    
    objects = []
    if num_features > 0:
        # Find coordinates for each labeled feature
        coords_map = {i: [] for i in range(1, num_features + 1)}
        for r, row in enumerate(labeled_array):
            for c, label_val in enumerate(row):
                if label_val > 0:
                    coords_map[label_val].append([r, c])

        # Create object dictionaries
        for i in range(1, num_features + 1):
            coords = coords_map[i]
            values = [grid_np[r, c] for r, c in coords]
            objects.append({"id": i, "coords": coords, "values": values})
            
    return objects

def count_color(obj, color_code):
    """Counts the occurrences of a specific color code within an object's values."""
    return obj['values'].count(color_code)

def transform(input_grid):
    """
    Filters objects in the input grid based on the count of azure (8) pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with filtered objects.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    output_grid_np = np.zeros_like(input_grid_np) # Initialize output with background color 0

    marker_color = 8
    max_allowed_markers = 1

    # 1. Identify all distinct objects (orthogonal connectivity)
    objects = get_objects(input_grid_np, diagonal=False)

    # 2. Iterate through objects, count marker color, and filter
    for obj in objects:
        # 3. Count how many azure (8) pixels the object contains
        azure_count = count_color(obj, marker_color)

        # 4. If the count is 0 or 1, keep the object
        if azure_count <= max_allowed_markers:
            # 5. Copy the kept object's pixels to the output grid
            for r, c in obj['coords']:
                output_grid_np[r, c] = input_grid_np[r, c]

    # Convert back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()
    return output_grid
```