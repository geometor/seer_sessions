```python
import numpy as np

"""
Transforms the pixels within a gray rectangular frame based on adjacency rules and the presence of internal gray pixels.

1.  Identify the gray (5) rectangular frame and the area it encloses.
2.  Check if any gray (5) pixels exist within the enclosed area (excluding the frame itself).
3.  If no internal gray pixels exist (Case 1):
    a.  Change white (0) pixels inside the frame that are adjacent (8-connectivity) to the frame pixels (gray=5) to red (2).
    b.  Change remaining white (0) pixels inside the frame that are adjacent (8-connectivity) to the newly colored red (2) pixels to gray (5).
    c.  Leave other pixels unchanged.
4.  If internal gray pixels exist (Case 2):
    a.  Change white (0) pixels inside the frame that are adjacent (8-connectivity) to *any* gray pixel (frame or internal) to red (2).
    b.  Leave all other pixels unchanged (including internal grays).
5.  If no gray frame is found, return the input grid unchanged.
"""

def is_adjacent(grid, r, c, target_color):
    """
    Checks 8 neighbors (including diagonals) of the pixel at (r, c)
    in the grid for the target_color.

    Args:
        grid (np.array): The grid to check within.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        target_color (int): The color value to look for in neighbors.

    Returns:
        bool: True if any neighbor has the target_color, False otherwise.
    """
    height, width = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check bounds and color
            if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] == target_color:
                return True
    return False

def transform(input_grid):
    """
    Applies the transformation rules based on the presence of internal gray pixels
    within a gray frame.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # --- 1. Identify the Frame ---
    gray_pixels = np.argwhere(input_array == 5)
    if gray_pixels.size == 0:
        # Edge Case: No gray pixels, return original grid
        return input_grid

    # Assume the frame defines the min/max boundaries of all gray pixels
    min_r = np.min(gray_pixels[:, 0])
    max_r = np.max(gray_pixels[:, 0])
    min_c = np.min(gray_pixels[:, 1])
    max_c = np.max(gray_pixels[:, 1])

    # --- 2. Define Internal Area ---
    # Ensure ranges are valid even for thin frames (max could be min+1)
    internal_rows = range(min_r + 1, max_r)
    internal_cols = range(min_c + 1, max_c)

    # --- 3. Check for Internal Grays ---
    has_internal_gray = False
    for r in internal_rows:
        for c in internal_cols:
            if input_array[r, c] == 5:
                has_internal_gray = True
                break
        if has_internal_gray:
            break

    # --- 4/5. Apply Transformation ---

    if has_internal_gray:
        # --- Case 2: Internal Grays Exist ---
        pixels_to_red = []
        # Iterate through the defined internal area
        for r in internal_rows:
            for c in internal_cols:
                # Target only white pixels
                if input_array[r, c] == 0:
                    # Check adjacency to ANY gray pixel (frame or internal) in the original input
                    if is_adjacent(input_array, r, c, 5):
                        pixels_to_red.append((r, c))

        # Apply the changes to the output grid
        for r, c in pixels_to_red:
            output_array[r, c] = 2
            
        # Other pixels (internal grays, non-adjacent whites) remain unchanged by default

    else:
        # --- Case 1: No Internal Grays ---
        pixels_to_red = []
        pixels_to_gray = []

        # --- Pass 1: Find white pixels adjacent to the frame (which are the only grays) ---
        for r in internal_rows:
            for c in internal_cols:
                if input_array[r, c] == 0:
                    # Check adjacency to frame pixels (color 5) in the original input
                    if is_adjacent(input_array, r, c, 5):
                        pixels_to_red.append((r, c))

        # Create a temporary grid reflecting the red changes for the next adjacency check
        temp_output_after_red = np.copy(output_array)
        for r, c in pixels_to_red:
            temp_output_after_red[r, c] = 2

        # --- Pass 2: Find remaining white pixels adjacent to the NEWLY red pixels ---
        for r in internal_rows:
            for c in internal_cols:
                # Check if it was originally white AND wasn't marked to become red
                is_original_white = (input_array[r, c] == 0)
                # Check if the coordinate pair is not in the list of pixels to turn red
                # Converting list to set for faster lookup if necessary, but for typical ARC sizes, list search is fine.
                is_not_red = ((r,c) not in pixels_to_red) 

                if is_original_white and is_not_red:
                    # Check adjacency to RED pixels (2) in the grid *after* the first pass
                    if is_adjacent(temp_output_after_red, r, c, 2):
                         pixels_to_gray.append((r, c))

        # --- Apply all changes to the final output grid ---
        for r, c in pixels_to_red:
            output_array[r, c] = 2
        for r, c in pixels_to_gray:
            output_array[r, c] = 5
            
        # White pixels not adjacent to frame or new red pixels remain white by default

    # Convert back to list of lists for the expected output format
    return output_array.tolist()
```