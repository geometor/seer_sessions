
Previous Code:
```python
import numpy as np

"""
Recolors pixels within a bounded area based on their quadrant, using a 2x2 color key found elsewhere.

1.  **Locate the Key:** Find the unique 2x2 block of pixels in the input grid where none of the four pixels are white (0) or azure (8). Record the four colors (Key-TL, Key-TR, Key-BL, Key-BR) and the key's location.
2.  **Identify the Target Area:** Determine the rectangular region where modifications occur. This area is typically enclosed by a single-pixel-thick frame of azure (8) pixels. Find the bounding box of all non-azure (8) pixels; if it's framed by azure (8), the Target Area consists of all pixels strictly *inside* this frame. Record its boundaries (top, bottom, left, right) and dimensions (height, width).
3.  **Identify the Source Color:** Find the single color value that is present both within the 2x2 Key and also appears at least once within the identified Target Area in the input grid (excluding white (0)). This is the Source Color.
4.  **Determine Quadrants:** Calculate the center of the Target Area. The midpoint row is `top + height // 2` and the midpoint column is `left + width // 2`. Pixels with row index `< midpoint_row` are in the top half; pixels with column index `< midpoint_col` are in the left half. This divides the Target Area into four quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), Bottom-Right (BR).
5.  **Apply Transformation:** Create a copy of the input grid. Iterate through each pixel within the Target Area's boundaries. If a pixel in the input grid has the Source Color:
    *   Determine which quadrant it falls into (TL, TR, BL, BR).
    *   Change the color of this pixel in the copied grid to the corresponding Key color: Key-TL for TL quadrant, Key-TR for TR, Key-BL for BL, Key-LR for BR.
6.  **Output:** The modified grid.
"""

def find_key(grid):
    """Finds the 2x2 key block (non-0, non-8 colors) and its top-left coordinates."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            # Check if all elements are not 0 and not 8
            if np.all((subgrid != 0) & (subgrid != 8)):
                return subgrid, (r, c)
    return None, None # Key not found

def find_target_area(grid):
    """
    Identifies the target area, assuming it's framed by azure (8) pixels.
    Returns the boundaries (top, left, bottom, right) of the area *inside* the frame.
    """
    rows, cols = grid.shape
    azure_color = 8

    # Find coordinates of all non-azure pixels
    non_azure_coords = np.argwhere(grid != azure_color)

    if non_azure_coords.size == 0:
        return None # No non-azure pixels found

    # Determine the bounding box of non-azure pixels
    min_r, min_c = non_azure_coords.min(axis=0)
    max_r, max_c = non_azure_coords.max(axis=0)

    # Define potential frame coordinates
    frame_top_r = min_r - 1
    frame_bottom_r = max_r + 1
    frame_left_c = min_c - 1
    frame_right_c = max_c + 1

    # Check if frame coordinates are within grid bounds
    if frame_top_r < 0 or frame_bottom_r >= rows or frame_left_c < 0 or frame_right_c >= cols:
        # print(f"Warning: Bounding box touches grid edge ({min_r, min_c} to {max_r, max_c}). Cannot confirm frame.")
        # Fallback: maybe the target area IS the bounding box? Let's return the bbox for now.
        # Based on examples, a frame seems required. Returning None indicates failure.
        return None 


    # Check if the surrounding 1-pixel border is entirely azure
    is_framed = True
    # Check top row of frame
    if not np.all(grid[frame_top_r, frame_left_c : frame_right_c + 1] == azure_color):
        is_framed = False
    # Check bottom row of frame
    if is_framed and not np.all(grid[frame_bottom_r, frame_left_c : frame_right_c + 1] == azure_color):
         is_framed = False
    # Check left column of frame (excluding corners already checked)
    if is_framed and not np.all(grid[frame_top_r + 1 : frame_bottom_r, frame_left_c] == azure_color):
        is_framed = False
    # Check right column of frame (excluding corners already checked)
    if is_framed and not np.all(grid[frame_top_r + 1 : frame_bottom_r, frame_right_c] == azure_color):
        is_framed = False

    if is_framed:
        # Target area is inside the frame
        target_top = min_r
        target_left = min_c
        target_bottom = max_r
        target_right = max_c
        return target_top, target_left, target_bottom, target_right
    else:
        # print("Warning: Non-azure bounding box is not fully framed by azure.")
        # If no frame, the logic fails based on examples.
        return None

def find_source_color(grid, key_colors, target_area_bounds):
    """
    Finds the unique color present in the key and within the target area (non-0).
    """
    if target_area_bounds is None:
        return -1 # Indicate error

    target_top, target_left, target_bottom, target_right = target_area_bounds
    
    target_area_colors = set()
    # Iterate only within the target area
    for r in range(target_top, target_bottom + 1):
        for c in range(target_left, target_right + 1):
             pixel_color = grid[r, c]
             if pixel_color != 0: # Exclude white background
                 target_area_colors.add(pixel_color)

    # Find colors present in both the key and the target area (excluding 0)
    valid_source_colors = key_colors.intersection(target_area_colors)

    if len(valid_source_colors) == 1:
        return list(valid_source_colors)[0]
    else:
        # print(f"Warning: Found {len(valid_source_colors)} potential source colors: {valid_source_colors}")
        return -1 # Indicate error or ambiguous source


def transform(input_grid):
    """
    Transforms the input grid by recoloring pixels based on their quadrant
    within a framed target area, using a 2x2 color key.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify and return
    output_grid = np.copy(grid)

    # 1. Locate the Key
    key_matrix, key_coords = find_key(grid)
    if key_matrix is None:
        # print("Error: Could not find the 2x2 key.")
        return input_grid # Return original if key is missing

    key_colors = set(key_matrix.flatten())
    key_ul = key_matrix[0, 0]
    key_ur = key_matrix[0, 1]
    key_ll = key_matrix[1, 0]
    key_lr = key_matrix[1, 1]

    # 2. Identify the Target Area (inside the azure frame)
    target_area_bounds = find_target_area(grid)
    if target_area_bounds is None:
        # print("Error: Could not identify a framed target area.")
        return input_grid # Return original if target area is not found as expected

    target_top, target_left, target_bottom, target_right = target_area_bounds
    target_height = target_bottom - target_top + 1
    target_width = target_right - target_left + 1

    # Check for valid dimensions
    if target_height <= 0 or target_width <= 0:
        # print("Error: Identified target area has invalid dimensions.")
        return input_grid

    # 3. Identify the Source Color
    source_color = find_source_color(grid, key_colors, target_area_bounds)
    if source_color == -1:
        # print("Error: Could not uniquely identify the source color.")
        return input_grid # Return original if source color is ambiguous or missing

    # 4. Determine Quadrants boundaries (midpoints are exclusive)
    # Pixels with row index < mid_row_exclusive are Top
    # Pixels with col index < mid_col_exclusive are Left
    mid_row_exclusive = target_top + target_height // 2
    mid_col_exclusive = target_left + target_width // 2

    # 5. Apply Transformation
    # Iterate through each pixel *only* within the identified Target Area
    for r in range(target_top, target_bottom + 1):
        for c in range(target_left, target_right + 1):
            # Check if the pixel in the original grid is the source color
            if grid[r, c] == source_color:
                # Determine quadrant
                is_top = r < mid_row_exclusive
                is_left = c < mid_col_exclusive

                new_color = -1 # Default invalid color
                if is_top and is_left:         # Top-Left
                    new_color = key_ul
                elif is_top and not is_left:   # Top-Right
                    new_color = key_ur
                elif not is_top and is_left:   # Bottom-Left
                    new_color = key_ll
                elif not is_top and not is_left:# Bottom-Right
                    new_color = key_lr

                if new_color != -1:
                   output_grid[r, c] = new_color
                # No else needed, if quadrant determination failed somehow, pixel remains unchanged

    # 6. Output: Convert back to list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 4 8 8 8 8 8 8 8 8
3 2 8 8 8 8 8 8 8 8
8 8 0 0 0 0 1 0 0 0
8 8 0 1 0 0 0 0 0 0
8 8 0 0 0 0 0 1 0 1
8 8 0 0 0 0 0 0 0 0
8 8 0 0 1 0 0 1 0 0
8 8 0 0 0 0 0 1 0 0
8 8 0 1 0 0 1 0 0 0
8 8 0 0 0 0 0 0 0 1
```
Expected Output:
```
1 4 8 8 8 8 8 8 8 8
3 2 8 8 8 8 8 8 8 8
8 8 0 0 0 0 4 0 0 0
8 8 0 1 0 0 0 0 0 0
8 8 0 0 0 0 0 4 0 4
8 8 0 0 0 0 0 0 0 0
8 8 0 0 3 0 0 2 0 0
8 8 0 0 0 0 0 2 0 0
8 8 0 3 0 0 2 0 0 0
8 8 0 0 0 0 0 0 0 2
```
Transformed Output:
```
1 4 8 8 8 8 8 8 8 8
3 2 8 8 8 8 8 8 8 8
8 8 0 0 0 0 1 0 0 0
8 8 0 1 0 0 0 0 0 0
8 8 0 0 0 0 0 1 0 1
8 8 0 0 0 0 0 0 0 0
8 8 0 0 1 0 0 1 0 0
8 8 0 0 0 0 0 1 0 0
8 8 0 1 0 0 1 0 0 0
8 8 0 0 0 0 0 0 0 1
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.0

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 4 6
8 8 8 8 8 8 8 8 8 8 1 2
0 0 0 0 2 0 0 0 0 0 8 8
0 2 0 0 0 0 0 0 2 0 8 8
0 0 0 0 0 0 0 0 0 0 8 8
2 0 0 0 0 0 2 2 0 0 8 8
0 0 0 0 0 0 0 0 2 0 8 8
0 0 0 2 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 8 8
0 2 0 0 0 0 0 2 0 0 8 8
0 2 0 0 0 0 0 0 0 0 8 8
0 0 0 0 2 0 0 0 0 2 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 4 6
8 8 8 8 8 8 8 8 8 8 1 2
0 0 0 0 4 0 0 0 0 0 8 8
0 4 0 0 0 0 0 0 6 0 8 8
0 0 0 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 6 6 0 0 8 8
0 0 0 0 0 0 0 0 6 0 8 8
0 0 0 1 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 8 8
0 1 0 0 0 0 0 2 0 0 8 8
0 1 0 0 0 0 0 0 0 0 8 8
0 0 0 0 1 0 0 0 0 2 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 4 6
8 8 8 8 8 8 8 8 8 8 1 2
0 0 0 0 2 0 0 0 0 0 8 8
0 2 0 0 0 0 0 0 2 0 8 8
0 0 0 0 0 0 0 0 0 0 8 8
2 0 0 0 0 0 2 2 0 0 8 8
0 0 0 0 0 0 0 0 2 0 8 8
0 0 0 2 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 8 8
0 2 0 0 0 0 0 2 0 0 8 8
0 2 0 0 0 0 0 0 0 0 8 8
0 0 0 0 2 0 0 0 0 2 8 8
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 15.277777777777771
## General Assessment

The provided code failed to replicate the transformations shown in the training examples. In both examples, the `transform` function returned the input grid unchanged. This suggests that one of the preliminary steps—locating the key, identifying the target area, or determining the source color—failed and caused the function to exit prematurely before applying the color changes.

The core logic of the transformation (mapping pixels of a specific source color within a framed area to new colors based on quadrant, using a 2x2 key) appears correct based on the initial analysis of the examples. The failure likely lies in the implementation details of the helper functions used to identify these components.

Specifically, the `find_target_area` function seems suspect. It relies on finding a bounding box of non-azure pixels and then checking if this box is perfectly framed by azure pixels. This might be too restrictive or contain edge case errors.

Strategy:
1.  Execute the helper functions (`find_key`, `find_target_area`, `find_source_color`) individually on the input grids of the failing examples using `tool_code`.
2.  Analyze the output of these functions to pinpoint the exact point of failure.
3.  Refine the logic, particularly for `find_target_area`, to correctly identify the components in all examples.
4.  Update the natural language program to reflect any necessary adjustments to the transformation logic or component identification steps.

## Metrics and Analysis



*code_execution:*
```python
import numpy as np

# --- Paste the helper functions here ---
def find_key(grid):
    """Finds the 2x2 key block (non-0, non-8 colors) and its top-left coordinates."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            subgrid = grid[r:r+2, c:c+2]
            # Check if all elements are not 0 and not 8
            if np.all((subgrid != 0) & (subgrid != 8)):
                return subgrid, (r, c)
    return None, None # Key not found

def find_target_area(grid):
    """
    Identifies the target area, assuming it's framed by azure (8) pixels.
    Returns the boundaries (top, left, bottom, right) of the area *inside* the frame.
    """
    rows, cols = grid.shape
    azure_color = 8

    # Find coordinates of all non-azure pixels
    non_azure_coords = np.argwhere(grid != azure_color)

    if non_azure_coords.size == 0:
        return None # No non-azure pixels found

    # Determine the bounding box of non-azure pixels
    min_r, min_c = non_azure_coords.min(axis=0)
    max_r, max_c = non_azure_coords.max(axis=0)

    # Define potential frame coordinates
    frame_top_r = min_r - 1
    frame_bottom_r = max_r + 1
    frame_left_c = min_c - 1
    frame_right_c = max_c + 1

    # Check if frame coordinates are within grid bounds
    if frame_top_r < 0 or frame_bottom_r >= rows or frame_left_c < 0 or frame_right_c >= cols:
        # Based on examples, a frame seems required. Returning None indicates failure.
        return None


    # Check if the surrounding 1-pixel border is entirely azure
    is_framed = True
    # Check top row of frame
    if not np.all(grid[frame_top_r, frame_left_c : frame_right_c + 1] == azure_color):
        is_framed = False
    # Check bottom row of frame
    if is_framed and not np.all(grid[frame_bottom_r, frame_left_c : frame_right_c + 1] == azure_color):
         is_framed = False
    # Check left column of frame (excluding corners already checked)
    if is_framed and not np.all(grid[frame_top_r + 1 : frame_bottom_r, frame_left_c] == azure_color):
        is_framed = False
    # Check right column of frame (excluding corners already checked)
    if is_framed and not np.all(grid[frame_top_r + 1 : frame_bottom_r, frame_right_c] == azure_color):
        is_framed = False

    if is_framed:
        # Target area is inside the frame
        target_top = min_r
        target_left = min_c
        target_bottom = max_r
        target_right = max_c
        return target_top, target_left, target_bottom, target_right
    else:
        # If no frame, the logic fails based on examples.
        return None

def find_source_color(grid, key_colors, target_area_bounds):
    """
    Finds the unique color present in the key and within the target area (non-0).
    """
    if target_area_bounds is None:
        return -1 # Indicate error

    target_top, target_left, target_bottom, target_right = target_area_bounds

    target_area_colors = set()
    # Iterate only within the target area
    for r in range(target_top, target_bottom + 1):
        for c in range(target_left, target_right + 1):
             pixel_color = grid[r, c]
             if pixel_color != 0: # Exclude white background
                 target_area_colors.add(pixel_color)

    # Find colors present in both the key and the target area (excluding 0)
    valid_source_colors = key_colors.intersection(target_area_colors)

    if len(valid_source_colors) == 1:
        return list(valid_source_colors)[0]
    else:
        return -1 # Indicate error or ambiguous source

# --- Input Data ---
input_grid_1 = np.array([
    [1, 4, 8, 8, 8, 8, 8, 8, 8, 8],
    [3, 2, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 0, 0, 0, 0, 1, 0, 0, 0],
    [8, 8, 0, 1, 0, 0, 0, 0, 0, 0],
    [8, 8, 0, 0, 0, 0, 0, 1, 0, 1],
    [8, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 0, 0, 1, 0, 0, 1, 0, 0],
    [8, 8, 0, 0, 0, 0, 0, 1, 0, 0],
    [8, 8, 0, 1, 0, 0, 1, 0, 0, 0],
    [8, 8, 0, 0, 0, 0, 0, 0, 0, 1]
])

input_grid_2 = np.array([
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 6],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 2],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 8, 8],
    [0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8],
    [2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 8, 8],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8],
    [0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 8, 8],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 8, 8]
])

# --- Test Example 1 ---
print("--- Example 1 Analysis ---")
key_matrix_1, key_coords_1 = find_key(input_grid_1)
print(f"Key Found: {key_matrix_1 is not None}, Coords: {key_coords_1}")
if key_matrix_1 is not None:
    key_colors_1 = set(key_matrix_1.flatten())
    target_area_bounds_1 = find_target_area(input_grid_1)
    print(f"Target Area Bounds: {target_area_bounds_1}")
    if target_area_bounds_1 is not None:
        source_color_1 = find_source_color(input_grid_1, key_colors_1, target_area_bounds_1)
        print(f"Source Color: {source_color_1}")
    else:
        print("Source Color: Not calculated (Target Area not found)")
else:
    print("Target Area Bounds: Not calculated (Key not found)")
    print("Source Color: Not calculated (Key not found)")


# --- Test Example 2 ---
print("\n--- Example 2 Analysis ---")
key_matrix_2, key_coords_2 = find_key(input_grid_2)
print(f"Key Found: {key_matrix_2 is not None}, Coords: {key_coords_2}")
if key_matrix_2 is not None:
    key_colors_2 = set(key_matrix_2.flatten())
    target_area_bounds_2 = find_target_area(input_grid_2)
    print(f"Target Area Bounds: {target_area_bounds_2}")
    if target_area_bounds_2 is not None:
        source_color_2 = find_source_color(input_grid_2, key_colors_2, target_area_bounds_2)
        print(f"Source Color: {source_color_2}")
    else:
        print("Source Color: Not calculated (Target Area not found)")
else:
    print("Target Area Bounds: Not calculated (Key not found)")
    print("Source Color: Not calculated (Key not found)")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Analysis ---
Key Found: True, Coords: (0, 0)
Target Area Bounds: None
Source Color: Not calculated (Target Area not found)

--- Example 2 Analysis ---
Key Found: True, Coords: (0, 10)
Target Area Bounds: None
Source Color: Not calculated (Target Area not found)

```
The code execution confirms the hypothesis: `find_key` works correctly for both examples, but `find_target_area` returns `None`. This causes `find_source_color` not to be called and the main `transform` function to return the input grid prematurely.

Let's re-examine the `find_target_area` logic and the grids:

**Example 1 Input Grid:**

```
1 4 8 8 8 8 8 8 8 8  <- Key TL, Key TR, Frame
3 2 8 8 8 8 8 8 8 8  <- Key BL, Key BR, Frame
8 8 0 0 0 0 1 0 0 0  <- Frame, Target Area ....., Frame
8 8 0 1 0 0 0 0 0 0  <- Frame, Target Area ....., Frame
8 8 0 0 0 0 0 1 0 1  <- Frame, Target Area ....., Frame
8 8 0 0 0 0 0 0 0 0  <- Frame, Target Area ....., Frame
8 8 0 0 1 0 0 1 0 0  <- Frame, Target Area ....., Frame
8 8 0 0 0 0 0 1 0 0  <- Frame, Target Area ....., Frame
8 8 0 1 0 0 1 0 0 0  <- Frame, Target Area ....., Frame
8 8 0 0 0 0 0 0 0 1  <- Frame, Target Area ....., Frame
```

- Non-azure (8) pixels include the key (1, 4, 3, 2) at (0,0) and (1,0), and the target area pixels (0s and 1s) from (2,2) to (9,9).
- The bounding box of *all* non-azure pixels is (0, 0) to (9, 9).
- `min_r=0`, `min_c=0`, `max_r=9`, `max_c=9`.
- Potential frame coordinates: `frame_top_r = -1`, `frame_left_c = -1`, `frame_bottom_r = 10`, `frame_right_c = 10`.
- The function checks `if frame_top_r < 0 ...`: Since `frame_top_r` is -1, the condition is true, and the function returns `None`.

**Example 2 Input Grid:**

```
8 8 8 8 8 8 8 8 8 8 4 6 <- Frame ................... Key TL, Key TR
8 8 8 8 8 8 8 8 8 8 1 2 <- Frame ................... Key BL, Key BR
0 0 0 0 2 0 0 0 0 0 8 8 <- Target Area ............, Frame
...                      <- Target Area ............, Frame
0 0 0 0 2 0 0 0 0 2 8 8 <- Target Area ............, Frame
```

- Non-azure (8) pixels include the key (4, 6, 1, 2) at (0,10) and (1,10), and the target area pixels (0s and 2s) from (2,0) to (11,9).
- The bounding box of *all* non-azure pixels is (0, 0) to (11, 11). (Because the 0s start at (2,0) and the key starts at (0,10)).
- `min_r=0`, `min_c=0`, `max_r=11`, `max_c=11`.
- Potential frame coordinates: `frame_top_r = -1`, `frame_left_c = -1`, `frame_bottom_r = 12`, `frame_right_c = 12`.
- The function checks `if frame_top_r < 0 ...`: Since `frame_top_r` is -1, the condition is true, and the function returns `None`.

**Conclusion:** The issue is that `find_target_area` calculates the bounding box based on *all* non-azure pixels, which incorrectly includes the key. The bounding box should only consider the pixels *potentially* inside the frame, excluding the key.

**Revised `find_target_area` Strategy:**
1. Find the coordinates of all azure (8) pixels. These form the frame.
2. Determine the bounding box of the azure (8) pixels.
3. The target area is likely the region *inside* this azure bounding box.
4. Calculate the inner bounds: `target_top = azure_min_r + 1`, `target_left = azure_min_c + 1`, `target_bottom = azure_max_r - 1`, `target_right = azure_max_c - 1`.
5. Add checks to ensure the frame is at least 3x3 pixels to have an interior.
6. Optionally, verify that the pixels along these inner boundaries are not azure, confirming it's the content area.

This approach avoids the problem of the key interfering with the bounding box calculation.

## Facts


```yaml
task_description: Recolors specific pixels within a bounded area based on their quadrant relative to the area's center, using colors defined by a separate 2x2 key.

components:
  - object: Grid
    description: A 2D array of pixels with colors represented by integers 0-9.
  - object: Key
    description: A 2x2 block of pixels located somewhere in the input grid.
    properties:
      - All four pixels have colors other than white (0) and azure (8).
      - Its position is constant between input and output.
      - Contains four colors defining the transformation: Key-TL, Key-TR, Key-BL, Key-BR.
  - object: Frame
    description: A rectangular border, one pixel thick, composed entirely of azure (8) pixels.
    properties:
      - Encloses the Target Area.
      - Its position and color (azure) are constant between input and output.
  - object: Target Area
    description: The rectangular region strictly inside the Frame.
    properties:
      - Contains pixels that may be modified.
      - Background pixels are typically white (0).
      - Contains pixels of the Source Color.
      - Center point determines the four quadrants (TL, TR, BL, BR).
      - Dimensions (height, width) are used to calculate the center.
  - object: Source Color Pixels
    description: Pixels within the Target Area having the Source Color.
    properties:
      - Their color value matches exactly one of the colors present in the Key.
      - They are not white (0).
  - object: Quadrants
    description: Four equal or near-equal rectangular regions dividing the Target Area based on its center.
    properties:
      - Top-Left (TL)
      - Top-Right (TR)
      - Bottom-Left (BL)
      - Bottom-Right (BR)
      - A pixel belongs to one quadrant based on its row and column relative to the center row/column.

actions:
  - action: Locate Key
    actor: System
    input: Input Grid
    output: 4 key colors (Key-TL, Key-TR, Key-BL, Key-BR), Key location (optional)
    description: Find the unique 2x2 block where no pixel is white (0) or azure (8).
  - action: Identify Frame Bounds
    actor: System
    input: Input Grid
    output: Frame bounding box (min_row, min_col, max_row, max_col)
    description: Find the minimum and maximum row/column indices of all azure (8) pixels.
  - action: Define Target Area
    actor: System
    input: Frame bounding box
    output: Target Area bounds (top, left, bottom, right)
    description: Calculate the area strictly inside the frame (frame_min_row+1, frame_min_col+1, frame_max_row-1, frame_max_col-1).
  - action: Identify Source Color
    actor: System
    input: Input Grid, Key colors, Target Area bounds
    output: Source Color value
    description: Find the unique color (not white 0) present both within the Key colors and within the Target Area pixels.
  - action: Determine Quadrant Mapping
    actor: System
    input: Target Area bounds
    output: Center row/column, Quadrant definitions
    description: Calculate the center of the Target Area. Define which row/column ranges correspond to TL, TR, BL, BR quadrants. Midpoint row = top + height // 2. Midpoint col = left + width // 2. Rows < midpoint row are Top. Columns < midpoint col are Left.
  - action: Recolor Pixels
    actor: System
    input: Input Grid (copied), Source Color, Target Area bounds, Quadrant Mapping, Key Colors
    output: Output Grid
    description: Iterate through pixels within the Target Area. If a pixel matches the Source Color, change its color in the copied grid to the Key color corresponding to its quadrant (TL -> Key-TL, TR -> Key-TR, BL -> Key-BL, BR -> Key-BR).
```


## Natural Language Program

1.  **Copy Input:** Create a mutable copy of the input grid to serve as the output grid.
2.  **Locate the Key:** Find the unique 2x2 block of pixels in the input grid where none of the four pixels are white (0) or azure (8). Record the four colors as Key-TL, Key-TR, Key-BL, Key-BR based on their relative positions. Store the set of these four key colors.
3.  **Identify Frame Bounds:** Find the coordinates of all azure (8) pixels. Determine the minimum and maximum row and column indices (`azure_min_r`, `azure_min_c`, `azure_max_r`, `azure_max_c`) among these azure pixels.
4.  **Define Target Area:** Calculate the boundaries of the area strictly inside the azure frame: `target_top = azure_min_r + 1`, `target_left = azure_min_c + 1`, `target_bottom = azure_max_r - 1`, `target_right = azure_max_c - 1`. Calculate the height and width of this area.
5.  **Identify the Source Color:** Find the single color value (which is not white (0)) that is present in the set of key colors (from step 2) AND also appears at least once within the identified Target Area (pixels from `target_top` to `target_bottom` and `target_left` to `target_right`) in the input grid. This is the Source Color.
6.  **Determine Quadrants:** Calculate the center dividing lines of the Target Area. The row dividing Top and Bottom is `mid_row_exclusive = target_top + target_height // 2`. The column dividing Left and Right is `mid_col_exclusive = target_left + target_width // 2`.
7.  **Apply Transformation:** Iterate through each pixel within the Target Area's boundaries (`r` from `target_top` to `target_bottom`, `c` from `target_left` to `target_right`). If the pixel at `(r, c)` in the *input* grid has the Source Color:
    *   Determine its quadrant:
        *   If `r < mid_row_exclusive` and `c < mid_col_exclusive`: Quadrant is TL.
        *   If `r < mid_row_exclusive` and `c >= mid_col_exclusive`: Quadrant is TR.
        *   If `r >= mid_row_exclusive` and `c < mid_col_exclusive`: Quadrant is BL.
        *   If `r >= mid_row_exclusive` and `c >= mid_col_exclusive`: Quadrant is BR.
    *   Change the color of the pixel at `(r, c)` in the *output* grid to the corresponding Key color (Key-TL for TL, Key-TR for TR, Key-BL for BL, Key-BR for BR).
8.  **Output:** Return the modified output grid.
