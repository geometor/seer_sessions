```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Transforms an input grid based on the following rules:
1. Define a target value (8).
2. Identify connected components (objects) composed solely of the target value using 8-way connectivity. These are 'target_objects'.
3. Independently, identify connected components composed of non-zero, non-target values using 8-way connectivity. These are 'pattern_objects'.
4. Sort both target_objects and pattern_objects based on their top-most, then left-most cell coordinate.
5. If no pattern_objects exist, return an empty grid (all zeros).
6. Initialize an empty output grid (all zeros).
7. Iterate through the sorted target_objects. For each target_object, select the next pattern_object from the sorted list, cycling through the patterns if necessary (using modulo arithmetic).
8. Determine the top-left corner coordinate of the current target_object.
9. Copy the selected pattern_object onto the output grid, aligning the pattern's top-left corner (relative to its own bounding box) with the target_object's top-left corner coordinate. The values copied are the original values from the pattern object.
10. The original pattern_objects and target_objects are not directly copied to the output grid; only the transformed patterns are placed at target locations.
"""

def _find_objects_by_mask(grid: np.ndarray, mask: np.ndarray) -> list[dict]:
    """
    Finds connected components based on a provided mask and extracts object details.

    Args:
        grid: The original input NumPy array containing cell values.
        mask: A boolean NumPy array of the same shape as grid, where True
              indicates cells belonging to potential objects.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys:
        'cells': list of (row, col, value) tuples from the original grid.
        'top_left': (min_row, min_col) tuple, the top-left corner coordinate.
    """
    # Define 8-way connectivity
    structure = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]], dtype=bool)

    # Label connected components in the mask
    labeled_mask, num_labels = label(mask, structure=structure)
    
    # Find the bounding box slices for each labeled object
    object_slices = find_objects(labeled_mask)

    objects = []

    if object_slices is None: # Handle case with no objects found
        return objects

    for i in range(num_labels):
        label_id = i + 1
        slices = object_slices[i]
        
        # Extract coordinates within the bounding box that match the current label
        local_coords = np.argwhere(labeled_mask[slices] == label_id)
        
        # Convert local coordinates to absolute grid coordinates
        abs_coords = local_coords + np.array([slices[0].start, slices[1].start])

        obj_cells = []
        abs_rows = []
        abs_cols = []

        # Get original values and track absolute coordinates
        for r_abs, c_abs in abs_coords:
            value = grid[r_abs, c_abs]
            obj_cells.append((r_abs, c_abs, value))
            abs_rows.append(r_abs)
            abs_cols.append(c_abs)

        # If object has cells (it should, but check just in case)
        if obj_cells:
            # Determine the actual top-left corner based on absolute coordinates
            obj_min_row = min(abs_rows)
            obj_min_col = min(abs_cols)
            
            obj_data = {
                'cells': obj_cells,
                'top_left': (obj_min_row, obj_min_col),
            }
            objects.append(obj_data)

    return objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    target_value = 8

    # Initialize output grid with zeros
    output_grid_np = np.zeros_like(grid_np)

    # --- Step 1 & 2: Identify Target Objects ---
    target_mask = (grid_np == target_value)
    target_objects = _find_objects_by_mask(grid_np, target_mask)

    # --- Step 3: Identify Pattern Objects ---
    pattern_mask = (grid_np != 0) & (grid_np != target_value)
    pattern_objects = _find_objects_by_mask(grid_np, pattern_mask)

    # --- Step 5: Handle case with no patterns ---
    if not pattern_objects:
        return output_grid_np.tolist() # Return empty grid

    # --- Step 4 & 7: Sort objects ---
    sort_key = lambda obj: obj['top_left']
    pattern_objects.sort(key=sort_key)
    target_objects.sort(key=sort_key)

    # --- Step 8, 9, 10: Perform Transformation ---
    num_patterns = len(pattern_objects)

    # Iterate through the sorted target objects
    for i, target_obj in enumerate(target_objects):
        # Select the pattern object to use, cycling through the list
        pattern_obj = pattern_objects[i % num_patterns]

        # Get top-left coordinates for placement calculation
        target_top_left_row, target_top_left_col = target_obj['top_left']
        pattern_origin_row, pattern_origin_col = pattern_obj['top_left']

        # Place the selected pattern onto the output grid
        for r_pat, c_pat, value in pattern_obj['cells']:
            # Calculate relative position within the pattern object
            rel_row = r_pat - pattern_origin_row
            rel_col = c_pat - pattern_origin_col

            # Calculate the destination position in the output grid
            dest_row = target_top_left_row + rel_row
            dest_col = target_top_left_col + rel_col

            # Place the pattern cell value if within grid bounds
            if 0 <= dest_row < rows and 0 <= dest_col < cols:
                output_grid_np[dest_row, dest_col] = value

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
```