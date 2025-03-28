
Previous Code:
```python
import numpy as np
import math

"""
Transforms a grid containing a unique 3x3 pattern of blue (1) and azure (8) pixels, and potentially scattered yellow (4) pixels, against a white (0) background.

1.  **Find Pattern:** Locate the unique 3x3 subgrid composed entirely of blue (1) and azure (8) pixels. Record its top-left coordinates (`pattern_r`, `pattern_c`).
2.  **Analyze Pattern:**
    a. Extract the 3x3 pattern.
    b. Count the total number of blue pixels (`count_blue`) and azure pixels (`count_azure`).
    c. Identify the four corner pixels (top-left, top-right, bottom-left, bottom-right).
    d. Count how many corner pixels are blue (`count_corner_blue`).
3.  **Rotate Pattern:** Modify the pattern *in place* within an output grid copy based on counts:
    a. If `count_azure > count_blue`: Rotate the pattern 180 degrees.
    b. If `count_blue > count_azure`:
        i.  If `count_corner_blue` is 4: Rotate 90 degrees clockwise.
        ii. If `count_corner_blue` is 3: Rotate 90 degrees counter-clockwise.
        iii. If `count_corner_blue` is 2: Rotate 180 degrees.
    (Other counts for `corner_blue` when `count_blue > count_azure` are not expected based on examples).
4.  **Consolidate Yellow Markers (if present):**
    a. Find coordinates of all yellow (4) pixels in the original input grid.
    b. If yellow pixels exist:
        i. Calculate median row (`median_row`) and column (`median_col`).
        ii. Determine pattern center (`center_r`, `center_c`).
        iii. Calculate target coordinates (`target_r`, `target_c`) using custom rounding for medians ending in .5 (round towards pattern center), standard rounding otherwise.
        iv. In the output grid, remove all original yellow pixels (set to white 0).
        v. In the output grid, place a single yellow pixel at (`target_r`, `target_c`).
5.  **Output:** Return the modified grid.
"""

def find_pattern_location(grid_np):
    """Finds the top-left corner of the 3x3 pattern of blue(1)/azure(8) pixels."""
    height, width = grid_np.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid_np[r:r+3, c:c+3]
            # Check if the subgrid contains only 1s and 8s and is not uniform
            # and is exactly 3x3
            if subgrid.shape == (3, 3) and \
               np.all(np.isin(subgrid, [1, 8])) and \
               len(np.unique(subgrid)) > 1:
                 return r, c
    return None # Should not happen based on task description but good practice

def analyze_pattern_corners(pattern):
    """Counts the number of blue pixels in the corners of a 3x3 pattern."""
    corners = [pattern[0, 0], pattern[0, 2], pattern[2, 0], pattern[2, 2]]
    count_corner_blue = sum(1 for pixel in corners if pixel == 1)
    return count_corner_blue

def custom_round(median_val, center_val):
    """Applies the custom rounding rule for medians ending in .5."""
    if median_val % 1 == 0.5:
        # If median is exactly halfway, round towards the center coordinate
        if center_val > median_val:
            return math.ceil(median_val)
        elif center_val < median_val:
             return math.floor(median_val)
        else: # center_val == median_val - should not happen if median ends in .5
             # but if it does, standard rounding is fine.
             return int(round(median_val))
    else:
        # Standard rounding for non-.5 cases (round half up)
        return int(round(median_val))


def transform(input_grid):
    """
    Applies the transformation: rotates a 3x3 pattern based on corner counts
    and consolidates yellow pixels using median and custom rounding.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = output_grid.shape

    # --- 1. Find Pattern ---
    pattern_loc = find_pattern_location(input_grid_np)
    pattern_center_r, pattern_center_c = -1, -1 # Initialize pattern center

    if pattern_loc:
        pattern_r, pattern_c = pattern_loc
        pattern_center_r = pattern_r + 1
        pattern_center_c = pattern_c + 1

        # --- 2. Analyze Pattern ---
        pattern = input_grid_np[pattern_r:pattern_r+3, pattern_c:pattern_c+3]
        count_blue = np.count_nonzero(pattern == 1)
        count_azure = np.count_nonzero(pattern == 8)
        count_corner_blue = analyze_pattern_corners(pattern)

        # --- 3. Rotate Pattern ---
        rotated_pattern = pattern # Default to no rotation if conditions aren't met
        if count_azure > count_blue:
            # Rotate 180 degrees
            rotated_pattern = np.rot90(pattern, k=2)
        elif count_blue > count_azure:
            if count_corner_blue == 4:
                # Rotate 90 degrees clockwise
                rotated_pattern = np.rot90(pattern, k=3) # k=3 is 270 CCW = 90 CW
            elif count_corner_blue == 3:
                 # Rotate 90 degrees counter-clockwise
                rotated_pattern = np.rot90(pattern, k=1)
            elif count_corner_blue == 2:
                 # Rotate 180 degrees
                rotated_pattern = np.rot90(pattern, k=2)
            # else: No rotation defined for other corner counts if B > A

        # Place the rotated pattern back into the output grid
        output_grid[pattern_r:pattern_r+3, pattern_c:pattern_c+3] = rotated_pattern
    else:
        # Handle case where pattern is not found (though examples suggest it's always present)
        print("Warning: 3x3 blue/azure pattern not found.")
        # Continue without rotation, yellow consolidation might use standard rounding if pattern center unknown

    # --- 4. Consolidate Yellow Markers (if present) ---
    yellow_pixels = np.where(input_grid_np == 4)
    yellow_rows, yellow_cols = yellow_pixels

    if len(yellow_rows) > 0:
        # a. Found yellow pixels coordinates

        # b.i Calculate Median Coordinates
        median_row = np.median(yellow_rows)
        median_col = np.median(yellow_cols)

        # Check if pattern was found before trying to use its center for custom rounding
        if pattern_loc:
            # b.ii Find Pattern Center (already done above)

            # b.iii Apply Custom Rounding Rule
            target_r = custom_round(median_row, pattern_center_r)
            target_c = custom_round(median_col, pattern_center_c)
        else:
            # Fallback if pattern wasn't found - cannot use custom rounding relative to center
            # Use standard rounding
            target_r = int(round(median_row))
            target_c = int(round(median_col))
            print("Warning: Yellow pixels consolidated using standard rounding due to missing pattern.")

        # Ensure target coordinates are within grid bounds (safety check)
        target_r = max(0, min(height - 1, target_r))
        target_c = max(0, min(width - 1, target_c))

        # b.iv Remove all original yellow pixels from the output grid
        output_grid[yellow_rows, yellow_cols] = 0

        # b.v Place a single new yellow pixel at the target location in the output grid
        output_grid[target_r, target_c] = 4
    # Else: No yellow pixels found, do nothing.

    # --- 5. Final Output ---
    # Convert back to list of lists format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 4 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 1 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 8 1 1 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 8 8 1 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 3.6363636363636402

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 4 0 1 1 1 0 0 0 0
0 0 0 8 1 8 0 0 0 0
0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 1 8 1 0 0 0 0
0 0 0 1 1 1 0 0 0 0
0 0 0 1 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
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
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 1 8 1 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 8 8 1 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 8 8 1 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 1 1 8 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 8 1 1 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 8 1 1 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 8 1 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
## General Assessment

The provided code successfully transforms Examples 2, 3, and 4, indicating that the core logic for identifying the 3x3 pattern, consolidating yellow pixels (including the custom rounding rule), and most rotation conditions are likely correct.

The failure on Example 1 points to an error specifically in the rotation rule applied when `count_blue > count_azure` and `count_corner_blue == 2`. The code applied a 180-degree rotation, but the expected output requires a 90-degree counter-clockwise rotation.

The strategy is to:
1.  Verify the pattern analysis (counts) for Example 1.
2.  Confirm the required rotation for Example 1 by comparing the input pattern to the expected output pattern.
3.  Update the specific rotation rule that failed.
4.  Ensure the updated rule does not conflict with the conditions for the successful examples.
5.  Refine the natural language program and YAML facts based on the corrected logic.

## Metrics and Analysis

Let's gather detailed metrics for each example's pattern to verify the conditions leading to rotation.



*code_execution:*
```python
import numpy as np

def find_pattern_location(grid_np):
    height, width = grid_np.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid_np[r:r+3, c:c+3]
            if subgrid.shape == (3, 3) and \
               np.all(np.isin(subgrid, [1, 8])) and \
               len(np.unique(subgrid)) > 1:
                 return r, c
    return None

def analyze_pattern_corners(pattern):
    corners = [pattern[0, 0], pattern[0, 2], pattern[2, 0], pattern[2, 2]]
    count_corner_blue = sum(1 for pixel in corners if pixel == 1)
    return count_corner_blue

def get_rotation(k):
    if k == 0: return "0 degrees"
    if k == 1: return "90 degrees CCW"
    if k == 2: return "180 degrees"
    if k == 3: return "90 degrees CW"
    return "Unknown"

# --- Define Inputs ---
inputs = [
    [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,0],[0,0,0,8,1,8,0,0,0,0],[0,0,0,1,8,8,0,0,0,0],[0,4,0,1,1,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,4,0,4,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]], # Ex 1
    [[0,0,0,0,0,0,0,0,0,0],[0,4,0,4,0,0,0,0,0,0],[0,0,0,0,0,0,4,0,0,0],[0,4,0,1,1,1,0,0,0,0],[0,0,0,8,1,8,0,0,0,0],[0,0,0,8,1,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]], # Ex 2
    [[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,4,0,0,0],[0,0,0,0,1,1,1,0,0,0,0],[0,0,0,0,8,8,8,0,0,0,0],[0,0,0,0,1,8,1,0,4,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,4,0,4,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]], # Ex 3
    [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,4,0,4,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,4,0,8,1,8,0,0,0],[0,0,0,0,8,1,8,0,0,0],[0,0,0,0,1,1,8,0,0,0],[0,0,0,0,0,0,0,4,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]] # Ex 4
]

# --- Define Expected Rotations (from visual inspection) ---
# Based on comparing input pattern to expected output pattern
expected_rotations_k = [1, 1, 3, 2] # k values for np.rot90 (1=90ccw, 2=180, 3=90cw)

# --- Analyze each example ---
results = []
for i, input_grid in enumerate(inputs):
    input_grid_np = np.array(input_grid, dtype=int)
    pattern_loc = find_pattern_location(input_grid_np)
    if pattern_loc:
        pattern_r, pattern_c = pattern_loc
        pattern = input_grid_np[pattern_r:pattern_r+3, pattern_c:pattern_c+3]
        count_blue = np.count_nonzero(pattern == 1)
        count_azure = np.count_nonzero(pattern == 8)
        count_corner_blue = analyze_pattern_corners(pattern)

        # Determine rotation based on original code's logic
        applied_rotation_k = 0 # Default 0 degrees
        if count_azure > count_blue:
            applied_rotation_k = 2 # 180
        elif count_blue > count_azure:
            if count_corner_blue == 4:
                applied_rotation_k = 3 # 90 CW
            elif count_corner_blue == 3:
                applied_rotation_k = 1 # 90 CCW
            elif count_corner_blue == 2:
                applied_rotation_k = 2 # 180 (This was the incorrect rule)

        results.append({
            "Example": i + 1,
            "Pattern Location": pattern_loc,
            "Blue Count": count_blue,
            "Azure Count": count_azure,
            "Corner Blue Count": count_corner_blue,
            "Condition": f"Azure > Blue" if count_azure > count_blue else (f"Blue > Azure, Corners={count_corner_blue}" if count_blue > count_azure else "Equal/Other"),
            "Applied Rotation (k)": applied_rotation_k,
            "Applied Rotation (Desc)": get_rotation(applied_rotation_k),
            "Expected Rotation (k)": expected_rotations_k[i],
            "Expected Rotation (Desc)": get_rotation(expected_rotations_k[i]),
            "Code Match Expected": applied_rotation_k == expected_rotations_k[i]
        })
    else:
         results.append({"Example": i + 1, "Error": "Pattern not found"})

import json
print(json.dumps(results, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
[
  {
    "Example": 1,
    "Pattern Location": [
      3,
      3
    ],
    "Blue Count": 5,
    "Azure Count": 4,
    "Corner Blue Count": 2,
    "Condition": "Blue > Azure, Corners=2",
    "Applied Rotation (k)": 2,
    "Applied Rotation (Desc)": "180 degrees",
    "Expected Rotation (k)": 1,
    "Expected Rotation (Desc)": "90 degrees CCW",
    "Code Match Expected": false
  },
  {
    "Example": 2,
    "Pattern Location": [
      3,
      3
    ],
    "Blue Count": 6,
    "Azure Count": 3,
    "Corner Blue Count": 3,
    "Condition": "Blue > Azure, Corners=3",
    "Applied Rotation (k)": 1,
    "Applied Rotation (Desc)": "90 degrees CCW",
    "Expected Rotation (k)": 1,
    "Expected Rotation (Desc)": "90 degrees CCW",
    "Code Match Expected": true
  },
  {
    "Example": 3,
    "Pattern Location": [
      4,
      4
    ],
    "Blue Count": 5,
    "Azure Count": 4,
    "Corner Blue Count": 4,
    "Condition": "Blue > Azure, Corners=4",
    "Applied Rotation (k)": 3,
    "Applied Rotation (Desc)": "90 degrees CW",
    "Expected Rotation (k)": 3,
    "Expected Rotation (Desc)": "90 degrees CW",
    "Code Match Expected": true
  },
  {
    "Example": 4,
    "Pattern Location": [
      5,
      4
    ],
    "Blue Count": 4,
    "Azure Count": 5,
    "Corner Blue Count": 1,
    "Condition": "Azure > Blue",
    "Applied Rotation (k)": 2,
    "Applied Rotation (Desc)": "180 degrees",
    "Expected Rotation (k)": 2,
    "Expected Rotation (Desc)": "180 degrees",
    "Code Match Expected": true
  }
]

```
**Analysis Summary:**

*   The metrics confirm the initial assessment.
*   Example 1 failed because the code applied a 180-degree rotation (k=2) when the condition was `Blue > Azure, Corners=2`, but the expected rotation is 90 degrees CCW (k=1).
*   Examples 2, 3, and 4 were correctly handled by the code's rotation logic.
*   The yellow pixel consolidation logic was not the source of the error in Example 1.

## YAML Facts

```yaml
task_description: Transforms a grid containing a unique 3x3 pattern and optional yellow markers.
objects:
  - object: grid
    properties:
      - type: 2D array of integers (0-9)
      - size: variable (1x1 to 30x30)
      - background_color: white (0)
  - object: pattern
    properties:
      - type: subgrid
      - size: 3x3
      - composition: contains only blue (1) and azure (8) pixels
      - uniqueness: exactly one such pattern exists per input grid
      - location: variable within the main grid
      - derived_properties:
          - count_blue: number of blue pixels
          - count_azure: number of azure pixels
          - count_corner_blue: number of blue pixels at the four corners (0,0), (0,2), (2,0), (2,2) relative to the pattern's top-left
          - center_coords: row and column index of the pattern's central pixel
  - object: markers
    properties:
      - type: collection of pixels
      - color: yellow (4)
      - count: zero or more
      - distribution: scattered within the main grid
      - derived_properties:
          - median_row: median row index of all yellow pixels
          - median_col: median column index of all yellow pixels
          - target_location: final consolidated location (row, col)

actions:
  - action: find_pattern
    inputs: grid
    outputs: pattern object (including location and derived properties)
    description: Locate the unique 3x3 subgrid composed of only blue (1) and azure (8) pixels. Calculate counts and center coordinates.
  - action: determine_rotation
    inputs: pattern object (count_blue, count_azure, count_corner_blue)
    outputs: rotation_type (0, 90_CCW, 180, 90_CW)
    description: |
      Compare counts to determine rotation:
      - If count_azure > count_blue, rotation is 180 degrees.
      - If count_blue > count_azure:
        - If count_corner_blue is 4, rotation is 90 degrees CW.
        - If count_corner_blue is 3, rotation is 90 degrees CCW.
        - If count_corner_blue is 2, rotation is 90 degrees CCW.
        - (Other corner counts when Blue > Azure not observed in examples)
      - Otherwise (counts equal or pattern invalid), rotation is 0 degrees (no rotation).
  - action: apply_rotation
    inputs: pattern object, rotation_type, output_grid
    outputs: modified output_grid
    description: Rotate the identified 3x3 pattern according to the determined rotation_type and update the corresponding area in the output_grid.
  - action: consolidate_markers
    inputs: markers object (locations, median_row, median_col), pattern object (center_coords), output_grid
    outputs: modified output_grid
    description: |
      If yellow markers exist:
      1. Calculate median row and column.
      2. Determine target row/column using custom rounding:
         - If median coordinate ends in .5, round towards the pattern's center coordinate.
         - Otherwise, use standard rounding (round half up).
      3. Set all original yellow marker locations in output_grid to white (0).
      4. Set the calculated target location in output_grid to yellow (4).

output: The final modified grid after applying rotation and marker consolidation.
```


## Natural Language Program

1.  **Initialize:** Create a copy of the input grid to serve as the output grid.
2.  **Find Pattern:** Scan the input grid to locate the unique 3x3 subgrid composed entirely of blue (1) and azure (8) pixels. Record its top-left coordinates. If no such pattern is found, skip steps 3-4 and proceed to step 5.
3.  **Analyze Pattern:**
    a.  Extract the 3x3 pattern.
    b.  Count the total number of blue pixels (`count_blue`) and azure pixels (`count_azure`) within the pattern.
    c.  Identify the four corner pixels (top-left, top-right, bottom-left, bottom-right) relative to the pattern's start.
    d.  Count how many of these corner pixels are blue (`count_corner_blue`).
    e.  Determine the coordinates of the pattern's central pixel (`center_r`, `center_c`).
4.  **Rotate Pattern:**
    a.  Determine the rotation needed based on the counts:
        *   If `count_azure > count_blue`, rotate the pattern 180 degrees.
        *   If `count_blue > count_azure`:
            *   If `count_corner_blue` is 4, rotate 90 degrees clockwise.
            *   If `count_corner_blue` is 3, rotate 90 degrees counter-clockwise.
            *   If `count_corner_blue` is 2, rotate 90 degrees counter-clockwise.
            *   *(No rotation specified for other `count_corner_blue` values when `count_blue > count_azure` based on examples).*
        *   Otherwise (e.g., counts are equal), do not rotate the pattern.
    b.  Apply the determined rotation to the extracted 3x3 pattern.
    c.  Overwrite the original pattern's location in the *output grid* with the rotated pattern.
5.  **Consolidate Yellow Markers:**
    a.  Find the coordinates (rows and columns) of all yellow (4) pixels in the *original input grid*.
    b.  If one or more yellow pixels were found:
        i.   Calculate the median of the row coordinates (`median_row`) and the median of the column coordinates (`median_col`).
        ii.  Determine the target row (`target_r`) and target column (`target_c`) for the consolidated yellow pixel:
            *   For the row: If `median_row` ends in .5 *and* a pattern was found (providing `center_r`), round `median_row` towards `center_r` (floor if `center_r < median_row`, ceil if `center_r > median_row`). Otherwise, round `median_row` using standard rounding (half up).
            *   For the column: If `median_col` ends in .5 *and* a pattern was found (providing `center_c`), round `median_col` towards `center_c`. Otherwise, round `median_col` using standard rounding.
            *   Ensure `target_r` and `target_c` are within the grid boundaries.
        iii. Set the color of all original yellow pixel locations in the *output grid* to white (0).
        iv. Set the color of the pixel at (`target_r`, `target_c`) in the *output grid* to yellow (4).
6.  **Output:** Return the modified output grid.
