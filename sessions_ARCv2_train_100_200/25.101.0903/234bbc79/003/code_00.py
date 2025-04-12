import numpy as np
import copy

"""
Transformation Rule Hypothesis:

1.  Find the bounding box (min_row, min_col, max_row, max_col) encompassing all non-white (0) pixels in the input grid.
2.  Create a working copy of the input grid.
3.  Initialize an empty set `columns_to_remove`.
4.  Iterate through each pixel (r, c) of the input grid:
    a.  If the pixel `input_grid[r][c]` is gray (5):
        i.   Find its 8 neighbors (orthogonal and diagonal).
        ii.  Identify the unique non-white (0), non-gray (5) color `C` among the neighbors. (Based on analysis of training data, there is always exactly one such color).
        iii. Apply color change: Set `working_grid[r, c] = C`. If no such neighbor color exists (e.g., isolated gray), it becomes white (0).
        iv.  Check Bounding Box condition for removal: If the gray pixel's position (r, c) is strictly inside the bounding box (min_row < r < max_row AND min_col < c < max_col), add the column index `c` to the `columns_to_remove` set.
5.  Construct the final output grid by taking the columns from the `working_grid` whose indices are *not* in the `columns_to_remove` set, preserving the order of the remaining columns.

Note: This hypothesis worked perfectly for Example 4, partially for Example 1, but failed for Example 2 during analysis. It represents the best simple geometric rule identified so far. Example 3 seems to follow a different pattern and is not fully explained by this rule.
"""

def get_neighbors(grid: np.ndarray, r: int, c: int) -> list[tuple[int, int, int]]:
    """Gets the 8 neighbours (value, row, col) of a pixel at (r, c), handling grid boundaries."""
    neighbours = []
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbours.append((grid[nr, nc], nr, nc))
    return neighbours

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on gray pixel interactions and bounding box context.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if input_array.size == 0:
        return []
        
    working_grid = np.copy(input_array)
    rows, cols = input_array.shape
    columns_to_remove = set()

    # Step 1: Find bounding box of non-white pixels
    non_white_coords = np.argwhere(input_array != 0)
    has_bb = False
    min_r, min_c, max_r, max_c = -1, -1, -1, -1 # Default values
    if non_white_coords.size > 0:
        min_r = non_white_coords[:, 0].min()
        min_c = non_white_coords[:, 1].min()
        max_r = non_white_coords[:, 0].max()
        max_c = non_white_coords[:, 1].max()
        has_bb = True

    # Step 4: Iterate through pixels to find gray ones
    gray_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == 5:
                gray_pixels.append(((r, c)))

    # Process each gray pixel
    for r, c in gray_pixels:
        # Step 4.a.i: Find neighbors
        neighbours = get_neighbors(input_array, r, c)
        
        # Step 4.a.ii: Identify unique neighbor color C
        # Filter for neighbours that are not white (0) and not gray (5)
        colored_neighbours = [n for n in neighbours if n[0] != 0 and n[0] != 5]
        distinct_colors = set(n[0] for n in colored_neighbours)
        
        the_color = 0 # Default to white if no valid neighbor found
        if len(distinct_colors) == 1:
            # If exactly one distinct non-white/non-gray neighbor color exists
            the_color = list(distinct_colors)[0]
        # Note: Based on training examples, len(distinct_colors) is always 1 for gray pixels
        # If it could be 0 or >1, the behavior is assumed to default to becoming white (0)
        
        # Step 4.a.iii: Apply color change to the working grid
        working_grid[r, c] = the_color
        
        # Step 4.a.iv: Check bounding box condition for column removal
        if has_bb: # Only check if a bounding box exists
             # Condition: gray pixel is strictly inside the bounding box
             if min_r < r < max_r and min_c < c < max_c:
                columns_to_remove.add(c)

    # Step 5: Construct output grid by removing marked columns
    # Create a list of column indices to keep
    output_cols_indices = [c for c in range(cols) if c not in columns_to_remove]
    
    if not output_cols_indices:
         # If all columns are removed (or no columns existed), return empty grid of correct height
        output_grid_array = np.empty((rows, 0), dtype=int)
    else:
        # Select only the columns that are not marked for removal
        output_grid_array = working_grid[:, output_cols_indices]

    # Convert final numpy array back to list of lists
    return output_grid_array.tolist()