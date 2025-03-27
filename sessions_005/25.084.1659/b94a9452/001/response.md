```python
import numpy as np

"""
Identify the bounding box of the non-white object in the input grid.
Extract this object.
Identify the two distinct non-white colors within the object.
Create a new grid of the same dimensions as the extracted object.
Fill the new grid by swapping the two identified non-white colors from the extracted object.
Return the new grid.
"""

def find_bounding_box(grid):
    """Finds the minimum bounding box containing non-zero elements."""
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return None # No object found
    min_row, min_col = non_zero_coords.min(axis=0)
    max_row, max_col = non_zero_coords.max(axis=0)
    return min_row, min_col, max_row, max_col

def extract_subgrid(grid, bbox):
    """Extracts the subgrid defined by the bounding box."""
    min_row, min_col, max_row, max_col = bbox
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    """
    Extracts a multi-colored object from the input grid and swaps its two
    constituent non-background colors to produce the output grid.
    """
    input_np = np.array(input_grid, dtype=int)

    # 1. & 2. Identify all non-white pixels and determine their bounding box.
    bbox = find_bounding_box(input_np)
    if bbox is None:
        # Handle cases where there's no object (e.g., return empty or input)
        # Based on examples, there's always an object. If not, error or empty return.
        return [] # Or raise an error

    # 3. Extract the subgrid corresponding to this bounding box.
    extracted_subgrid = extract_subgrid(input_np, bbox)

    # 4. Identify the two distinct non-white colors.
    unique_colors = np.unique(extracted_subgrid)
    non_white_colors = unique_colors[unique_colors != 0]

    if len(non_white_colors) != 2:
        # This case shouldn't happen based on the examples provided.
        # Could raise an error or handle differently if needed.
        print(f"Warning: Expected 2 non-white colors, found {len(non_white_colors)}: {non_white_colors}")
        # Decide on fallback behavior - maybe return extracted grid as is?
        # For now, assume it's always 2.
        if len(non_white_colors) < 2:
             return extracted_subgrid.tolist() # Or handle error

    color_A = non_white_colors[0]
    color_B = non_white_colors[1]

    # 5. Create a new output grid with the same dimensions.
    # Make a copy to modify, or create a new one to fill. Creating new is safer.
    output_grid = np.zeros_like(extracted_subgrid)
    rows, cols = extracted_subgrid.shape

    # 6. Iterate through the extracted subgrid and swap colors into the output grid.
    for r in range(rows):
        for c in range(cols):
            pixel_color = extracted_subgrid[r, c]
            if pixel_color == color_A:
                output_grid[r, c] = color_B
            elif pixel_color == color_B:
                output_grid[r, c] = color_A
            else: # Handle background color if it's within the bounding box (unlikely based on examples)
                output_grid[r, c] = pixel_color # Keep background as is

    # 7. Return the newly created output grid as a list of lists.
    return output_grid.tolist()
```