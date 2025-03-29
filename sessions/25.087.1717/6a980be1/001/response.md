```python
import numpy as np

"""
Transformation Rule:
1. Identify the border color from the input grid's corner (e.g., input_grid[0, 0]).
2. Determine the vertical span (minimum and maximum row indices) of the non-white pattern located within the input grid's content area (i.e., excluding the 1-pixel border).
3. Initialize an output grid of the same dimensions as the input grid.
4. Process each row of the output grid based on its relationship to the pattern's vertical span:
    a. If the current row index is within the determined pattern's vertical span:
        i. Check if the corresponding input row's content area (columns between 1 and width-2) contains any red pixels (color code 2).
        ii. Determine the background color for this output row: use the identified border color if red pixels were present in the input row's content, otherwise use white (color code 0).
        iii. Fill the entire output row with this determined background color.
        iv. Copy the non-white pixels (the actual pattern elements, typically green and red) from the input row's content area to the corresponding positions in the output row, overwriting the background fill.
    b. If the current row index is outside the determined pattern's vertical span:
        i. Check if the pattern found in step 2 was "tall", meaning it spanned exactly from row index 1 to row index height-2.
        ii. If the pattern was "tall", fill the current output row entirely with white (0). (This condition applies specifically to the top row (index 0) and the bottom row (index height-1) of the grid).
        iii. If the pattern was "short" (did not span the full height minus borders) or if no pattern existed at all, fill the current output row by repeating the horizontal sequence [white (0), border_color, border_color] across the width of the row.
5. Return the completed output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by selectively filling the background based on
    the presence of a specific color (red=2) within a central pattern area,
    preserving the pattern itself, and applying different fill rules for rows
    outside the pattern's vertical extent.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int) # Work with numpy array for efficiency
    height, width = input_grid_np.shape

    # Handle grids too small to have a border and content area
    if height < 3 or width < 3:
        # Default behavior for small grids might need specific definition,
        # but based on examples, they likely follow the "short pattern" rule.
        # Identify border color safely
        border_color = input_grid_np[0, 0] if height > 0 and width > 0 else 0
        output_grid = np.zeros((height, width), dtype=int)
        outside_pattern = np.array([0, border_color, border_color])
        if width > 0 : # Check width before resizing
             for r in range(height):
                 output_grid[r, :] = np.resize(outside_pattern, width)
        return output_grid.tolist()


    # 1. Identify border color
    border_color = input_grid_np[0, 0]

    # Initialize output grid
    output_grid = np.zeros((height, width), dtype=int)

    # 2. Determine vertical span (min/max rows) of the non-white pattern
    #    within the input grid's content area [1:-1, 1:-1]
    pattern_min_r = height
    pattern_max_r = -1
    for r in range(1, height - 1):
        # Check if any non-white pixel exists in the content part of the row
        if np.any(input_grid_np[r, 1:-1] != 0):
            pattern_min_r = min(pattern_min_r, r)
            pattern_max_r = max(pattern_max_r, r)

    pattern_exists = (pattern_max_r != -1) # True if any pattern was found

    # Determine if the pattern fills the full height available (excluding borders)
    is_tall_pattern = pattern_exists and pattern_min_r == 1 and pattern_max_r == height - 2

    # Define the repeating pattern used for filling rows outside a short pattern's span
    outside_pattern = np.array([0, border_color, border_color])

    # 4. Process each row to build the output grid
    for r in range(height):
        # Case a: Row is within the pattern's vertical span
        if pattern_exists and pattern_min_r <= r <= pattern_max_r:
            # i. Check if the input row's content area contains red (2)
            has_red = np.any(input_grid_np[r, 1:-1] == 2)

            # ii. Determine background color for this output row
            row_bg_color = border_color if has_red else 0

            # iii. Fill the output row with this background color initially
            output_grid[r, :] = row_bg_color

            # iv. Copy the non-white pixels (pattern) from the input row's content area
            # Find column indices of non-white pixels in the content slice [1:-1]
            content_slice = input_grid_np[r, 1:-1]
            pattern_indices_in_slice = np.where(content_slice != 0)[0]
            # Convert these slice indices to indices in the full row
            pattern_indices_in_row = pattern_indices_in_slice + 1
            # Copy the original pattern pixel values to the output grid at these indices
            output_grid[r, pattern_indices_in_row] = input_grid_np[r, pattern_indices_in_row]

        # Case b: Row is outside the pattern's vertical span (or no pattern exists)
        else:
            # i/ii. Check if the pattern was "tall"
            if is_tall_pattern:
                # If tall, the outside rows (0 and height-1) become white
                output_grid[r, :] = 0
            # iii. If pattern was "short" or didn't exist, use the repeating pattern
            else:
                if width > 0 : # Check width before resizing pattern
                    output_grid[r, :] = np.resize(outside_pattern, width)

    # 5. Return the output grid as a list of lists
    return output_grid.tolist()
```