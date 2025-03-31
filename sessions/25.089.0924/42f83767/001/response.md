Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from scipy.ndimage import label, find_objects
import sys
import os

# Optional: Add utils directory if helpers were external
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from utils.object_utils import find_connected_components # Assuming a utility function exists


def find_connected_components_with_coords(grid, background_color=0):
    """
    Finds connected components of non-background pixels using scipy.ndimage.label.
    Returns a list of slices corresponding to the bounding boxes of the components
    and a list of their top-left (row, col) coordinates.
    Components are implicitly sorted by find_objects based on label number, 
    which usually corresponds to a raster scan order.
    """
    binary_grid = (grid != background_color).astype(int)
    # structure=np.ones((3,3)) default connectivity includes diagonals
    labeled_array, num_features = label(binary_grid)

    if num_features == 0:
        return [], [] # No objects found

    # find_objects returns a list of tuples of slices
    objects_slices = find_objects(labeled_array)

    # Filter out potential None entries if any object label was skipped (shouldn't typically happen)
    valid_slices = [s for s in objects_slices if s is not None]

    # Extract top-left coordinates (row, col) from the slices
    coords = [(s[0].start, s[1].start) for s in valid_slices]

    return valid_slices, coords


def find_separator_rows_cols(grid):
    """
    Finds the index of the first row and the first column that consist entirely
    of the background color (0). These act as separators between zones.
    Raises ValueError if separators are not found within the grid boundaries,
    as this indicates an unexpected input format for this specific task.
    """
    rows, cols = grid.shape
    split_row = -1
    split_col = -1

    # Find the first all-zero row
    for r in range(rows):
        if np.all(grid[r, :] == 0):
            split_row = r
            break

    # Find the first all-zero column
    for c in range(cols):
        if np.all(grid[:, c] == 0):
            split_col = c
            break

    # Check if separators were found and are not at the very edge (index 0)
    # which would imply a missing zone based on the task's structure.
    if split_row <= 0 or split_col <= 0:
        # Allow separators at the end if grid dimensions match split row/col?
        # For this task, the examples show clear internal separators.
        # If split_row/col is -1 (not found) or 0, raise error.
         raise ValueError(f"Separator row/column not found or is at edge (row={split_row}, col={split_col}). Expected internal separators.")

    return split_row, split_col


"""
Transformation Rule: Tile an output grid based on a color-to-pattern mapping and an arrangement grid derived from the input.

1.  **Analyze Input & Split:** The input grid is divided into four quadrants by the first fully white (0) row and column.
    - Top-Left (TL): Contains color keys (small solid squares).
    - Top-Right (TR): Contains value patterns (5x5 shapes, initially gray).
    - Bottom-Left (BL): Contains the arrangement grid (uses key colors).
    - Bottom-Right (BR): Unused.
2.  **Extract Keys:** Find all distinct colored objects in the TL zone. Record their colors and top-left positions. Sort the colors based on position (top-to-bottom, then left-to-right).
3.  **Extract Values:** Find all 5x5 patterns in the TR zone. Record the patterns (as 5x5 numpy arrays) and their top-left positions. Sort the patterns based on position. Assume patterns are exactly 5x5 starting from the detected top-left corner.
4.  **Establish Mapping:** Create a dictionary mapping each sorted key color to the corresponding sorted value pattern. Ensure the number of keys matches the number of values.
5.  **Extract Arrangement:** The BL zone *is* the arrangement grid.
6.  **Construct Output:**
    - Calculate output dimensions: (height of arrangement grid * 5) x (width of arrangement grid * 5).
    - Initialize an output grid of this size with white (0).
    - Iterate through each cell `(r, c)` of the arrangement grid:
        - Get the `key_color` at `(r, c)`.
        - If `key_color` is not white (0):
            - Retrieve the corresponding `value_pattern` (5x5) from the mapping.
            - Create a `recolored_pattern` by replacing all non-white pixels in the `value_pattern` with the `key_color`. White pixels remain white.
            - Place this `recolored_pattern` into the output grid at the top-left position `(r * 5, c * 5)`.
7.  **Return:** The final constructed output grid as a list of lists.
"""
def transform(input_grid):
    """
    Applies the tiling transformation based on color-pattern mapping.

    Args:
        input_grid (list of lists): The input grid representation.

    Returns:
        list of lists: The transformed output grid. Returns input grid on critical error.
    """
    try:
        input_array = np.array(input_grid, dtype=int)
        rows, cols = input_array.shape
        background_color = 0

        # --- Step 1: Analyze Input & Split ---
        split_row, split_col = find_separator_rows_cols(input_array)

        top_left_zone = input_array[0:split_row, 0:split_col]
        top_right_zone = input_array[0:split_row, split_col+1:cols]
        bottom_left_zone = input_array[split_row+1:rows, 0:split_col]
        # bottom_right_zone = input_array[split_row+1:rows, split_col+1:cols] # Unused

        # --- Step 2: Extract Keys ---
        key_slices, key_coords = find_connected_components_with_coords(top_left_zone, background_color)
        key_colors_with_coords = []
        if not key_slices:
            print("Warning: No key objects found in Top-Left zone.")
        else:
             for i, slc in enumerate(key_slices):
                # Extract the component grid based on the slice
                component_grid = top
---
