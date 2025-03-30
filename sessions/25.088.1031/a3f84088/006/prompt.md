
Previous Code:
```python
import numpy as np

"""
Transforms the pixels within a gray rectangular frame based on adjacency rules and the presence of internal gray pixels.

1.  Identify the gray (5) rectangular frame and the area it encloses.
2.  Check if any gray (5) pixels exist within the enclosed area (excluding the frame itself).
3.  If no internal gray pixels exist (Case 1):
    a.  Initialize the first layer of pixels adjacent to the frame (inside) as red (2).
    b.  Iteratively fill inwards: pixels adjacent (8-connectivity) to the last colored layer are colored with the alternate color (gray (5) if the last was red, red (2) if the last was gray).
    c.  This continues until no more white (0) pixels inside the frame can be colored.
4.  If internal gray pixels exist (Case 2):
    a.  Change white (0) pixels inside the frame that are adjacent (8-connectivity) to *any* gray pixel (frame or internal) to red (2).
    b.  Leave all other pixels unchanged (including internal grays).
5.  If no gray frame is found, return the input grid unchanged.
"""

def _find_frame_and_internal_gray(input_array):
    """
    Finds the bounding box of gray pixels and checks for internal grays.

    Args:
        input_array (np.array): The input grid.

    Returns:
        tuple: (frame_coords, has_internal_gray)
               frame_coords is (min_r, max_r, min_c, max_c) or None if no frame.
               has_internal_gray is bool.
    """
    height, width = input_array.shape
    gray_pixels = np.argwhere(input_array == 5)

    if gray_pixels.size == 0:
        return None, False # No gray pixels at all

    min_r = np.min(gray_pixels[:, 0])
    max_r = np.max(gray_pixels[:, 0])
    min_c = np.min(gray_pixels[:, 1])
    max_c = np.max(gray_pixels[:, 1])

    # Basic check: does it look like a frame boundary?
    # A more robust check could verify all boundary pixels are gray,
    # but min/max might be sufficient for this task's examples.
    is_plausible_frame = (np.any(gray_pixels[:, 0] == min_r) and
                         np.any(gray_pixels[:, 0] == max_r) and
                         np.any(gray_pixels[:, 1] == min_c) and
                         np.any(gray_pixels[:, 1] == max_c))

    if not is_plausible_frame:
         # It might be scattered gray pixels, not a frame boundary
         # Check if ALL gray pixels lie *only* on the boundary box lines
         is_only_boundary = True
         for r, c in gray_pixels:
             if not (r == min_r or r == max_r or c == min_c or c == max_c):
                 is_only_boundary = False
                 break
         if not is_only_boundary:
             # Found gray pixels inside the bounding box defined by gray pixels,
             # treat this as Case 2 even if not a perfect frame.
             # Find all white pixels adjacent to any gray pixel.
             pass # Logic handled in main transform function's Case 2 path
         else:
              # Grays only on boundary lines, but maybe not a full frame.
              # For this problem, let's assume if gray exists, it forms the intended frame.
              # If required, add stricter frame validation here.
              pass


    frame_coords = (min_r, max_r, min_c, max_c)

    # --- Check for Internal Grays ---
    has_internal_gray = False
    if max_r > min_r + 1 and max_c > min_c + 1: # Check if there's a potential inside
        internal_area = input_array[min_r + 1:max_r, min_c + 1:max_c]
        if np.any(internal_area == 5):
            has_internal_gray = True

    return frame_coords, has_internal_gray


def _get_adjacent_white_pixels(grid, target_coords_set, internal_coords):
    """
    Finds white pixels within internal_coords adjacent to pixels in target_coords_set.

    Args:
        grid (np.array): The current state of the grid.
        target_coords_set (set): Set of (r, c) tuples to check adjacency against.
        internal_coords (tuple): (min_r, max_r, min_c, max_c) defining the internal area boundaries.

    Returns:
        set: Set of (r, c) tuples of adjacent white pixels found.
    """
    height, width = grid.shape
    adjacent_white_pixels = set()
    min_r, max_r, min_c, max_c = internal_coords

    # Iterate through the bounding box of the target coordinates for efficiency
    if not target_coords_set:
        return adjacent_white_pixels

    # Calculate bounds of potential neighbours to check
    rows_to_check = set()
    cols_to_check = set()
    for r,c in target_coords_set:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                # Check if neighbour is within the internal area bounds
                if min_r < nr < max_r and min_c < nc < max_c:
                     rows_to_check.add(nr)
                     cols_to_check.add(nc)

    # Check only the relevant internal pixels
    for r in rows_to_check:
         for c in cols_to_check:
              # Ensure it's strictly inside
              if not (min_r < r < max_r and min_c < c < max_c):
                  continue
                  
              if grid[r, c] == 0: # Check if it's white
                   # Check 8 neighbours
                   is_adj = False
                   for dr in [-1, 0, 1]:
                       for dc in [-1, 0, 1]:
                           if dr == 0 and dc == 0:
                               continue
                           nr, nc = r + dr, c + dc
                           if (nr, nc) in target_coords_set:
                               is_adj = True
                               break
                       if is_adj:
                           break
                   if is_adj:
                       adjacent_white_pixels.add((r, c))

    return adjacent_white_pixels

def transform(input_grid):
    """
    Applies the iterative fill or single-layer red fill based on internal grays.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # --- 1. Identify Frame and Internal Grays ---
    frame_coords, has_internal_gray = _find_frame_and_internal_gray(input_array)

    if frame_coords is None:
        # No gray pixels found, or couldn't determine a frame
        return input_grid # Return original grid

    min_r, max_r, min_c, max_c = frame_coords
    internal_bounds = (min_r, max_r, min_c, max_c) # Use frame coords for internal area boundary checks

    # --- 2. Apply Transformation based on Case ---

    if has_internal_gray:
        # --- Case 2: Internal Grays Exist ---
        # Find all gray pixel coordinates (frame and internal)
        all_gray_coords_set = set(tuple(coord) for coord in np.argwhere(input_array == 5))

        # Find white pixels inside the frame adjacent to *any* gray pixel
        pixels_to_red = set()
        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                if input_array[r, c] == 0: # Only consider white pixels
                    is_adj_to_gray = False
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            # Check bounds implicitly via set lookup
                            if (nr, nc) in all_gray_coords_set:
                                is_adj_to_gray = True
                                break
                        if is_adj_to_gray:
                            break
                    if is_adj_to_gray:
                        pixels_to_red.add((r,c))

        # Apply the changes
        for r, c in pixels_to_red:
            output_array[r, c] = 2 # Red

    else:
        # --- Case 1: No Internal Grays ---
        # Get initial frame coordinates
        frame_pixels_set = set()
        for r in range(min_r, max_r + 1):
             for c in range(min_c, max_c + 1):
                  if input_array[r,c] == 5:
                      # Check if it's actually part of the boundary frame lines
                      if r == min_r or r == max_r or c == min_c or c == max_c:
                           frame_pixels_set.add((r,c))
        
        if not frame_pixels_set: # Should not happen if frame_coords is not None, but safety check
             return output_array.tolist()

        last_colored_pixels_set = frame_pixels_set
        color_to_place = 2 # Start with Red

        while True:
            # Find white pixels inside the frame adjacent to the last colored layer
            current_pixels_to_color = _get_adjacent_white_pixels(
                output_array, # Check against the current state of the output grid
                last_colored_pixels_set,
                internal_bounds
            )

            # If no more white pixels can be colored, stop
            if not current_pixels_to_color:
                break

            # Color the found pixels
            for r, c in current_pixels_to_color:
                output_array[r, c] = color_to_place

            # Prepare for the next iteration
            last_colored_pixels_set = current_pixels_to_color
            color_to_place = 5 if color_to_place == 2 else 2 # Toggle color

    # Convert back to list of lists for the expected output format
    return output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0 5 0 0 0
0 5 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 0 0 0
0 5 2 2 2 2 2 2 2 5 0 0 0
0 5 2 5 5 5 5 5 2 5 0 0 0
0 5 2 5 0 0 0 5 2 5 0 0 0
0 5 2 5 0 0 0 5 2 5 0 0 0
0 5 2 5 0 0 0 5 2 5 0 0 0
0 5 2 5 5 5 5 5 2 5 0 0 0
0 5 2 2 2 2 2 2 2 5 0 0 0
0 5 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 0 0 0
0 5 2 2 2 2 2 2 2 5 0 0 0
0 5 2 5 5 5 5 5 2 5 0 0 0
0 5 2 5 2 2 2 5 2 5 0 0 0
0 5 2 5 2 5 2 5 2 5 0 0 0
0 5 2 5 2 2 2 5 2 5 0 0 0
0 5 2 5 5 5 5 5 2 5 0 0 0
0 5 2 2 2 2 2 2 2 5 0 0 0
0 5 5 5 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.650887573964496

## Example 2:
Input:
```
5 5 5 5 5 5
5 0 0 0 0 5
5 0 0 0 0 5
5 0 0 0 0 5
5 0 0 0 0 5
5 5 5 5 5 5
```
Expected Output:
```
5 5 5 5 5 5
5 2 2 2 2 5
5 2 5 5 2 5
5 2 5 5 2 5
5 2 2 2 2 5
5 5 5 5 5 5
```
Transformed Output:
```
5 5 5 5 5 5
5 2 2 2 2 5
5 2 5 5 2 5
5 2 5 5 2 5
5 2 2 2 2 5
5 5 5 5 5 5
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 5 2 2 2 2 2 2 2 2 2 2 5 0
0 0 0 5 2 5 5 5 5 5 5 5 5 2 5 0
0 0 0 5 2 5 0 0 0 0 0 0 5 2 5 0
0 0 0 5 2 5 0 5 5 5 5 0 5 2 5 0
0 0 0 5 2 5 0 5 2 2 5 0 5 2 5 0
0 0 0 5 2 5 0 5 2 2 5 0 5 2 5 0
0 0 0 5 2 5 0 5 5 5 5 0 5 2 5 0
0 0 0 5 2 5 0 0 0 0 0 0 5 2 5 0
0 0 0 5 2 5 5 5 5 5 5 5 5 2 5 0
0 0 0 5 2 2 2 2 2 2 2 2 2 2 5 0
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 5 2 2 2 2 2 2 2 2 2 2 5 0
0 0 0 5 2 5 5 5 5 5 5 5 5 2 5 0
0 0 0 5 2 5 2 2 2 2 2 2 5 2 5 0
0 0 0 5 2 5 2 5 5 5 5 2 5 2 5 0
0 0 0 5 2 5 2 5 2 2 5 2 5 2 5 0
0 0 0 5 2 5 2 5 2 2 5 2 5 2 5 0
0 0 0 5 2 5 2 5 5 5 5 2 5 2 5 0
0 0 0 5 2 5 2 2 2 2 2 2 5 2 5 0
0 0 0 5 2 5 5 5 5 5 5 5 5 2 5 0
0 0 0 5 2 2 2 2 2 2 2 2 2 2 5 0
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 15.625

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
0 5 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 0
0 5 2 5 5 5 5 5 5 5 5 5 5 5 5 5 2 5 0
0 5 2 5 0 0 0 0 0 0 0 0 0 0 0 5 2 5 0
0 5 2 5 0 5 5 5 5 5 5 5 5 5 0 5 2 5 0
0 5 2 5 0 5 2 2 2 2 2 2 2 5 0 5 2 5 0
0 5 2 5 0 5 2 5 5 5 5 5 2 5 0 5 2 5 0
0 5 2 5 0 5 2 5 0 0 0 5 2 5 0 5 2 5 0
0 5 2 5 0 5 2 5 0 5 0 5 2 5 0 5 2 5 0
0 5 2 5 0 5 2 5 0 0 0 5 2 5 0 5 2 5 0
0 5 2 5 0 5 2 5 5 5 5 5 2 5 0 5 2 5 0
0 5 2 5 0 5 2 2 2 2 2 2 2 5 0 5 2 5 0
0 5 2 5 0 5 5 5 5 5 5 5 5 5 0 5 2 5 0
0 5 2 5 0 0 0 0 0 0 0 0 0 0 0 5 2 5 0
0 5 2 5 5 5 5 5 5 5 5 5 5 5 5 5 2 5 0
0 5 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 0
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
0 5 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 0
0 5 2 5 5 5 5 5 5 5 5 5 5 5 5 5 2 5 0
0 5 2 5 2 2 2 2 2 2 2 2 2 2 2 5 2 5 0
0 5 2 5 2 5 5 5 5 5 5 5 5 5 2 5 2 5 0
0 5 2 5 2 5 2 2 2 2 2 2 2 5 2 5 2 5 0
0 5 2 5 2 5 2 5 5 5 5 5 2 5 2 5 2 5 0
0 5 2 5 2 5 2 5 2 2 2 5 2 5 2 5 2 5 0
0 5 2 5 2 5 2 5 2 5 2 5 2 5 2 5 2 5 0
0 5 2 5 2 5 2 5 2 2 2 5 2 5 2 5 2 5 0
0 5 2 5 2 5 2 5 5 5 5 5 2 5 2 5 2 5 0
0 5 2 5 2 5 2 2 2 2 2 2 2 5 2 5 2 5 0
0 5 2 5 2 5 5 5 5 5 5 5 5 5 2 5 2 5 0
0 5 2 5 2 2 2 2 2 2 2 2 2 2 2 5 2 5 0
0 5 2 5 5 5 5 5 5 5 5 5 5 5 5 5 2 5 0
0 5 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 0
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 48
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.59279778393352
