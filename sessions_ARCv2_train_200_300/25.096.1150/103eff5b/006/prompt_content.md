
Previous Code:
```python
import numpy as np

"""
Transforms an input grid by mapping a "pattern" region onto a "template" region based on relative pixel positions within their respective bounding boxes.

1.  Identifies two regions:
    - Pattern Region: Cells with values other than 0 and 8.
    - Template Region: Cells with the value 8.
2.  Calculates the minimum bounding box for both regions.
3.  Iterates through each cell (r, c) marked as template (value 8).
4.  Calculates the normalized position of (r, c) within the template's bounding box.
5.  Maps this normalized position to a corresponding coordinate (src_r, src_c) within the pattern's bounding box.
6.  Determines the nearest integer coordinates to (src_r, src_c) within the pattern bounding box bounds.
7.  Copies the color from the input grid at these nearest source coordinates to the output grid at position (r, c), effectively replacing the original 8.
8.  Cells outside the template region remain unchanged.
"""

def get_bounding_box(coords: np.ndarray) -> tuple | None:
    """
    Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of coordinates.

    Args:
        coords: A NumPy array of shape (N, 2) where N is the number of points,
                and each row is [row, col].

    Returns:
        A tuple (min_r, min_c, max_r, max_c) or None if coords is empty.
    """
    if coords.shape[0] == 0:
        return None
    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)
    return int(min_r), int(min_c), int(max_r), int(max_c)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the pattern-to-template pixel mapping transformation.

    Args:
        input_grid: The input grid as a list of lists of integers.

    Returns:
        The transformed grid as a list of lists of integers.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # --- 1. Identify Pattern and Template Cells ---
    pattern_mask = (grid != 0) & (grid != 8)
    template_mask = (grid == 8)

    pattern_coords = np.argwhere(pattern_mask)
    template_coords = np.argwhere(template_mask)

    # --- 2. Handle Empty Regions ---
    if pattern_coords.shape[0] == 0 or template_coords.shape[0] == 0:
        # If either region is missing, no transformation can be applied
        return output_grid.tolist()

    # --- 3. Calculate Bounding Boxes ---
    p_bbox = get_bounding_box(pattern_coords)
    t_bbox = get_bounding_box(template_coords)

    # This check should be redundant due to the check above, but included for safety
    if p_bbox is None or t_bbox is None:
         return output_grid.tolist()

    p_min_r, p_min_c, p_max_r, p_max_c = p_bbox
    t_min_r, t_min_c, t_max_r, t_max_c = t_bbox

    # --- 4. Calculate Bounding Box Dimensions (adding 1 because bounds are inclusive) ---
    # Note: We use max-min directly for scaling factor. Add 1 if thinking about number of pixels.
    # For normalization/scaling, height/width = (max_coord - min_coord) is correct.
    p_height = p_max_r - p_min_r
    p_width = p_max_c - p_min_c
    t_height = t_max_r - t_min_r
    t_width = t_max_c - t_min_c

    # --- 5. Iterate and Map Template Pixels ---
    # Loop only through the template coordinates identified earlier
    for r, c in template_coords:
        # The check 'if grid[r, c] == 8' is implicitly true for these coords

        # --- 6. Calculate Normalized Position within Template BBox ---
        # Avoid division by zero for single-pixel-wide/high boxes
        norm_r = 0.5 if t_height == 0 else (r - t_min_r) / t_height
        norm_c = 0.5 if t_width == 0 else (c - t_min_c) / t_width

        # --- 7. Map to Source Coordinates within Pattern BBox ---
        src_r_float = p_min_r + norm_r * p_height
        src_c_float = p_min_c + norm_c * p_width

        # --- 8. Find Nearest Integer Source Coordinates and Clamp ---
        # Use np.round for nearest integer, then clamp to pattern bbox bounds
        nearest_src_r = int(np.round(src_r_float))
        nearest_src_c = int(np.round(src_c_float))

        # Clamp coordinates to be within the source pattern bounding box
        nearest_src_r = np.clip(nearest_src_r, p_min_r, p_max_r)
        nearest_src_c = np.clip(nearest_src_c, p_min_c, p_max_c)
        
        # --- 9. Get Source Color and Update Output ---
        source_color = grid[nearest_src_r, nearest_src_c]
        
        # Ensure we don't accidentally sample a 0 or 8 if the nearest pixel wasn't part of the original pattern
        # This could happen if the pattern is sparse within its bounding box.
        # A better approach might be needed if sampling background/template is forbidden.
        # Option 1: Use original pattern_mask to ensure sampled pixel is valid pattern
        # Option 2: If sampled pixel is not valid pattern, find nearest *valid* pattern pixel (more complex)
        # Let's stick to simple nearest neighbor for now as per the NL program.
        
        output_grid[r, c] = source_color

    # --- 10. Finalize ---
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 3 4 0 0 0 0 0 0 0
0 0 2 1 1 0 0 0 0 0 0 0 0
0 0 2 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 8 8 0 0 8 8 0 0 0 0 0
0 0 8 8 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 3 4 0 0 0 0 0 0 0
0 0 2 1 1 0 0 0 0 0 0 0 0
0 0 2 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 1 1 3 3 3 3 0 0 0
0 0 0 0 1 1 3 3 3 3 0 0 0
0 0 4 4 0 0 4 4 0 0 0 0 0
0 0 4 4 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 3 4 0 0 0 0 0 0 0
0 0 2 1 1 0 0 0 0 0 0 0 0
0 0 2 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 0 0 0 0 0
0 0 0 0 1 1 1 1 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 20.512820512820497

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 1 0 0 0 0 0 0
0 0 0 4 3 0 0 0 0 0 0 0
0 0 0 2 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 8 8 8 8 8 8 0 0
0 8 8 8 0 0 0 8 8 8 0 0
0 8 8 8 0 0 0 8 8 8 0 0
0 8 8 8 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 1 0 0 0 0 0 0
0 0 0 4 3 0 0 0 0 0 0 0
0 0 0 2 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 4 4 4 0 0 0 0 0
0 2 2 2 4 4 4 0 0 0 0 0
0 2 2 2 4 4 4 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 3 3 3 0 0
0 4 4 4 0 0 0 1 1 1 0 0
0 4 4 4 0 0 0 1 1 1 0 0
0 4 4 4 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 1 0 0 0 0 0 0
0 0 0 4 3 0 0 0 0 0 0 0
0 0 0 2 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 4 4 3 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0
0 4 4 3 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 0 4 4 0 0
0 2 2 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 40
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.30303030303031
