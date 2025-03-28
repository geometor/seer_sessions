
Previous Code:
```python
import numpy as np

"""
The transformation determines the output grid by applying the first matching rule from the following prioritized list, using red (2) as the key color and white (0) as the background color:

1.  **Solid Row Separation Rule:** Check if the input grid contains exactly three unique colors AND if it has a horizontal row composed entirely of the key color (red). If both conditions are true:
    *   Identify the 'third color' (neither white nor red).
    *   Find the row index (`sr`) of the topmost solid red row.
    *   Create the output grid by filling rows above `sr` with white, row `sr` with red, and rows below `sr` with the 'third color'.

2.  **Fixed Diagonal Pattern Rule:** If Rule 1 does not apply, check if the input grid contains exactly three unique colors AND if *all* red pixels are located at positions `(r, c)` where `r = c + 1` or `r = c + 2`. If both conditions are true:
    *   Identify the 'third color'.
    *   Create the output grid with a fixed pattern: pixels where `r < c + 1` are white, pixels where `r == c + 1` or `r == c + 2` are red, and pixels where `r > c + 2` are the 'third color'.

3.  **Column Filter with Downward Propagation Rule:** If neither Rule 1 nor Rule 2 applies, perform the following for each column independently:
    *   Find the row index (`mr`) of the topmost red pixel in the input column.
    *   If no red pixel exists in the column, the output column is identical to the input column.
    *   If a topmost red pixel exists at `mr`:
        *   Initialize the output column corresponding to the input column.
        *   Set rows `0` to `mr-1` in the output column to white.
        *   The pixel at `(mr, col)` remains red (or its original color if already red).
        *   Process rows from `mr + 1` downwards: If a pixel in the output column is white, change its color to match the color of the pixel directly above it in the output column. Otherwise, keep its current color (which was copied from the input initially). This propagates the color found at or above `mr` downwards through any original white space below `mr`.
"""

# --- Helper Functions ---

def find_unique_colors(grid):
    """Identifies unique colors in the grid."""
    return set(grid.flatten())

def find_solid_row(grid, color):
    """Finds the index of the first row consisting entirely of the specified color. Returns -1 if none found."""
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == color):
            return r
    return -1

def check_all_key_on_diag(grid, key_color):
    """Checks if all occurrences of key_color are on diagonals r=c+1 or r=c+2."""
    key_locations = np.argwhere(grid == key_color)
    if len(key_locations) == 0:
        # If no key color, it doesn't fit the pattern requirement for Rule 2.
        # Rule 2 requires 3 colors, so there must be key_color pixels present.
        return False
    for r, c in key_locations:
        if not (r == c + 1 or r == c + 2):
            return False
    return True

# --- Rule Application Functions ---

def apply_row_separation(grid_shape, key_color, background_color, third_color, solid_row_index):
    """Applies Rule 1: Row Separation."""
    height, width = grid_shape
    output_grid = np.full(grid_shape, background_color, dtype=int) # Fill above with background initially

    # Set the separator row
    output_grid[solid_row_index, :] = key_color

    # Fill below with third color, only if there are rows below
    if solid_row_index < height - 1:
        output_grid[solid_row_index + 1:, :] = third_color

    return output_grid

def apply_fixed_pattern(grid_shape, key_color, background_color, third_color):
    """Applies Rule 2: Fixed Diagonal Pattern Generation."""
    height, width = grid_shape
    output_grid = np.full(grid_shape, background_color, dtype=int) # Default to background

    for r in range(height):
        for c in range(width):
            # Key color diagonal band
            if r == c + 1 or r == c + 2:
                output_grid[r, c] = key_color
            # Third color below the band
            elif r > c + 2:
                output_grid[r, c] = third_color
            # Background color above the band (already set by default)
            # else: output_grid[r, c] = background_color

    return output_grid

def apply_column_filter_propagation(grid, key_color, background_color):
    """Applies Rule 3: Column Filtering with Downward Propagation."""
    height, width = grid.shape
    output_grid = np.copy(grid) # Start with a copy of the input

    for c in range(width):
        # Find the row index of the highest occurrence (minimum row index) of the key color in the input column
        key_color_indices = np.where(grid[:, c] == key_color)[0]

        if len(key_color_indices) > 0:
            min_row = np.min(key_color_indices)

            # 1. Set pixels above the highest key color to background in the output
            output_grid[:min_row, c] = background_color

            # 2. Propagate non-background colors downwards starting from min_row + 1
            for r in range(min_row + 1, height):
                # If the current cell in the output grid is background,
                # fill it with the color of the cell directly above it in the output grid.
                if output_grid[r, c] == background_color:
                    output_grid[r, c] = output_grid[r - 1, c]
                # If it's not background, it keeps its copied value from the input.

        # If key color not in column, the column remains unchanged (already copied)

    return output_grid

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid based on the prioritized rules described in the module docstring.
    """
    # Convert input list of lists to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    grid_shape = (height, width)

    # Define constants
    BACKGROUND_COLOR = 0
    KEY_COLOR = 2

    # 1. Analyze Input Grid Properties
    unique_colors = find_unique_colors(input_np)
    other_colors = unique_colors - {BACKGROUND_COLOR, KEY_COLOR}
    # Determine the 'third_color' only if exactly 3 unique colors exist
    third_color = next(iter(other_colors), None) if len(unique_colors) == 3 else None
    num_unique_colors = len(unique_colors)

    # 2. Check Rule 1: Solid Row Separation
    solid_row_index = find_solid_row(input_np, KEY_COLOR)
    # Rule 1 requires a solid key row AND exactly 3 unique colors (implying third_color is not None)
    if solid_row_index != -1 and third_color is not None:
        # Apply Rule 1
        output_grid = apply_row_separation(grid_shape, KEY_COLOR, BACKGROUND_COLOR, third_color, solid_row_index)
        
    # 3. Check Rule 2: Fixed Diagonal Pattern Generation
    # Rule 2 requires NO solid key row, exactly 3 unique colors, AND all key pixels on specific diagonals
    elif solid_row_index == -1 and third_color is not None:
        all_key_on_diag = check_all_key_on_diag(input_np, KEY_COLOR)
        if all_key_on_diag:
            # Apply Rule 2
            output_grid = apply_fixed_pattern(grid_shape, KEY_COLOR, BACKGROUND_COLOR, third_color)
        else:
            # Conditions for Rule 1 & 2 not met, proceed to Rule 3
            output_grid = apply_column_filter_propagation(input_np, KEY_COLOR, BACKGROUND_COLOR)

    # 4. Apply Rule 3: Column Filter (Default)
    else:
        # Conditions for Rule 1 & 2 not met (e.g., not 3 colors, or rule 2 diag condition failed)
        output_grid = apply_column_filter_propagation(input_np, KEY_COLOR, BACKGROUND_COLOR)

    # Convert final numpy array back to list of lists for the required output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
5 5 5 0 5 0 0 0 5 5
5 0 0 5 5 0 5 0 5 5
0 5 5 0 5 5 0 5 0 0
2 0 5 5 2 0 5 0 2 5
5 2 0 2 0 2 0 2 0 2
0 0 2 5 5 5 2 0 5 0
5 5 0 0 0 5 5 5 5 5
0 5 0 5 5 0 5 0 5 5
0 5 5 0 5 0 5 0 5 5
5 5 0 0 5 5 5 5 5 5
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 2 0
5 2 0 2 5 2 0 2 5 2
5 5 2 5 5 5 2 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 2 0
5 2 0 2 2 2 0 2 2 2
5 2 2 5 5 5 2 2 5 2
5 5 2 5 5 5 5 5 5 5
5 5 2 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.0

## Example 2:
Input:
```
1 0 1 1 1 1 1 1 1 0
0 0 1 0 1 1 0 1 0 1
1 1 0 0 1 1 1 1 1 0
2 2 2 2 2 2 2 2 2 2
0 0 1 1 0 0 0 0 0 0
1 1 0 1 0 0 0 0 1 0
0 1 1 1 0 1 1 0 1 0
1 1 0 0 0 1 0 0 1 0
0 0 1 0 0 0 1 1 0 0
0 1 1 1 0 1 1 0 0 1
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
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
0 8 8 0 8 0 8 8 0 0
2 0 8 8 0 8 0 0 0 8
2 2 8 0 0 0 0 0 0 0
0 2 2 0 8 0 0 0 0 0
8 8 2 2 0 0 0 8 8 0
8 8 8 2 2 8 0 0 0 0
0 0 0 0 2 2 8 8 8 0
8 0 8 0 0 2 2 8 8 8
8 8 0 0 0 0 2 2 8 0
0 8 0 8 0 8 8 2 2 8
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
8 2 2 0 0 0 0 0 0 0
8 8 2 2 0 0 0 0 0 0
8 8 8 2 2 0 0 0 0 0
8 8 8 8 2 2 0 0 0 0
8 8 8 8 8 2 2 0 0 0
8 8 8 8 8 8 2 2 0 0
8 8 8 8 8 8 8 2 2 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
8 2 2 0 0 0 0 0 0 0
8 8 2 2 0 0 0 0 0 0
8 8 8 2 2 0 0 0 0 0
8 8 8 8 2 2 0 0 0 0
8 8 8 8 8 2 2 0 0 0
8 8 8 8 8 8 2 2 0 0
8 8 8 8 8 8 8 2 2 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
**Assessment and Strategy**

1.  **Assessment:** The provided code successfully solved Examples 2 and 3 by applying Rule 1 (Solid Row Separation) and Rule 2 (Fixed Diagonal Pattern), respectively. However, it failed on Example 1, which defaulted to Rule 3 (Column Filter). The transformed output for Example 1 differs from the expected output in the way colors are handled *below* the topmost red pixel in certain columns. Specifically, the propagation logic seems incorrect; it appears to be overwriting non-background colors with the propagated color when it should only be filling in original background (white) pixels.
2.  **Strategy:**
    *   Confirm that Rules 1 and 2 are correctly identifying their respective cases and producing the correct output based on Examples 2 and 3. This seems to be the case.
    *   Focus on refining Rule 3 based on the discrepancy observed in Example 1.
    *   Analyze the difference between the input, expected output, and transformed output for Example 1, column by column, paying close attention to the pixels below the topmost red pixel.
    *   Modify the description of Rule 3's downward propagation step: the propagation should only fill pixels that were *originally* white (0) in the input grid; other pixels below the topmost red should retain their original color from the input grid.
    *   Update the Natural Language Program and Facts to reflect this refined understanding of Rule 3.

**Metrics**

Let's analyze Example 1 where the failure occurred:


*code_execution:*
```python
import numpy as np

input_grid = np.array([
    [5, 5, 5, 0, 5, 0, 0, 0, 5, 5],
    [5, 0, 0, 5, 5, 0, 5, 0, 5, 5],
    [0, 5, 5, 0, 5, 5, 0, 5, 0, 0],
    [2, 0, 5, 5, 2, 0, 5, 0, 2, 5],
    [5, 2, 0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 2, 5, 5, 5, 2, 0, 5, 0],
    [5, 5, 0, 0, 0, 5, 5, 5, 5, 5],
    [0, 5, 0, 5, 5, 0, 5, 0, 5, 5],
    [0, 5, 5, 0, 5, 0, 5, 0, 5, 5],
    [5, 5, 0, 0, 5, 5, 5, 5, 5, 5]
])

expected_output = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
    [5, 2, 0, 2, 0, 2, 0, 2, 0, 2],
    [5, 5, 2, 5, 5, 5, 2, 5, 5, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])

transformed_output = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
    [5, 2, 0, 2, 2, 2, 0, 2, 2, 2],
    [5, 5, 2, 5, 5, 5, 2, 2, 5, 2],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
])

diff = transformed_output != expected_output
diff_indices = np.argwhere(diff)
num_diff = np.sum(diff)

print(f"Example 1:")
print(f"  Input unique colors: {np.unique(input_grid)}")
print(f"  Expected unique colors: {np.unique(expected_output)}")
print(f"  Transformed unique colors: {np.unique(transformed_output)}")
print(f"  Number of different pixels: {num_diff}")
print(f"  Indices of different pixels (row, col):\n{diff_indices}")

# Analyze differences in specific columns based on previous thought
print("\nAnalysis of differing pixels:")
for r, c in diff_indices:
    in_val = input_grid[r, c]
    exp_val = expected_output[r, c]
    trans_val = transformed_output[r, c]
    above_trans_val = transformed_output[r-1, c] if r > 0 else -1 # Use -1 to indicate no pixel above
    topmost_red_row = np.min(np.where(input_grid[:, c] == 2)[0]) if 2 in input_grid[:,c] else -1
    print(f"  Pixel ({r}, {c}):")
    print(f"    Input Value: {in_val}")
    print(f"    Expected Output Value: {exp_val}")
    print(f"    Transformed Output Value: {trans_val}")
    print(f"    Topmost Red Row in Input Col {c}: {topmost_red_row}")
    print(f"    Value Above in Transformed Col {c}: {above_trans_val}")
    if in_val == 0:
        print(f"    Input pixel was white (0). Expected {exp_val}, got {trans_val}. Should be value from above in transformed ({above_trans_val}).")
        if exp_val != above_trans_val:
             print(f"    -> Mismatch: Expected {exp_val} but value above was {above_trans_val}.")
    else:
        print(f"    Input pixel was NOT white ({in_val}). Expected {exp_val}, got {trans_val}. Should be input value ({in_val}).")
        if exp_val != in_val:
            print(f"    -> Mismatch: Expected {exp_val} but input was {in_val}.")

# Verify Rule 1 applies to Example 2
input_ex2 = np.array([[1,0,1,1,1,1,1,1,1,0],[0,0,1,0,1,1,0,1,0,1],[1,1,0,0,1,1,1,1,1,0],[2,2,2,2,2,2,2,2,2,2],[0,0,1,1,0,0,0,0,0,0],[1,1,0,1,0,0,0,0,1,0],[0,1,1,1,0,1,1,0,1,0],[1,1,0,0,0,1,0,0,1,0],[0,0,1,0,0,0,1,1,0,0],[0,1,1,1,0,1,1,0,0,1]])
colors_ex2 = np.unique(input_ex2)
solid_red_row_ex2 = -1
for r in range(input_ex2.shape[0]):
    if np.all(input_ex2[r,:] == 2):
        solid_red_row_ex2 = r
        break
print(f"\nExample 2 Analysis:")
print(f"  Unique colors: {colors_ex2}")
print(f"  Solid red row index: {solid_red_row_ex2}")
print(f"  Rule 1 conditions met: {len(colors_ex2) == 3 and solid_red_row_ex2 != -1}")


# Verify Rule 2 applies to Example 3
input_ex3 = np.array([[0,8,8,0,8,0,8,8,0,0],[2,0,8,8,0,8,0,0,0,8],[2,2,8,0,0,0,0,0,0,0],[0,2,2,0,8,0,0,0,0,0],[8,8,2,2,0,0,0,8,8,0],[8,8,8,2,2,8,0,0,0,0],[0,0,0,0,2,2,8,8,8,0],[8,0,8,0,0,2,2,8,8,8],[8,8,0,0,0,0,2,2,8,0],[0,8,0,8,0,8,8,2,2,8]])
colors_ex3 = np.unique(input_ex3)
solid_red_row_ex3 = -1
for r in range(input_ex3.shape[0]):
    if np.all(input_ex3[r,:] == 2):
        solid_red_row_ex3 = r
        break
red_locations_ex3 = np.argwhere(input_ex3 == 2)
all_red_on_diag_ex3 = True
if len(red_locations_ex3) == 0:
    all_red_on_diag_ex3 = False
else:
    for r, c in red_locations_ex3:
        if not (r == c + 1 or r == c + 2):
            all_red_on_diag_ex3 = False
            break
print(f"\nExample 3 Analysis:")
print(f"  Unique colors: {colors_ex3}")
print(f"  Solid red row index: {solid_red_row_ex3}")
print(f"  All red pixels on r=c+1 or r=c+2: {all_red_on_diag_ex3}")
print(f"  Rule 2 conditions met: {len(colors_ex3) == 3 and solid_red_row_ex3 == -1 and all_red_on_diag_ex3}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1:
  Input unique colors: [0 2 5]
  Expected unique colors: [0 2 5]
  Transformed unique colors: [0 2 5]
  Number of different pixels: 4
  Indices of different pixels (row, col):
[[4 4]
 [4 8]
 [5 7]
 [5 9]]

Analysis of differing pixels:
  Pixel (4, 4):
    Input Value: 0
    Expected Output Value: 0
    Transformed Output Value: 2
    Topmost Red Row in Input Col 4: 3
    Value Above in Transformed Col 4: 2
    Input pixel was white (0). Expected 0, got 2. Should be value from above in transformed (2).
    -> Mismatch: Expected 0 but value above was 2.
  Pixel (4, 8):
    Input Value: 0
    Expected Output Value: 0
    Transformed Output Value: 2
    Topmost Red Row in Input Col 8: 3
    Value Above in Transformed Col 8: 2
    Input pixel was white (0). Expected 0, got 2. Should be value from above in transformed (2).
    -> Mismatch: Expected 0 but value above was 2.
  Pixel (5, 7):
    Input Value: 0
    Expected Output Value: 5
    Transformed Output Value: 2
    Topmost Red Row in Input Col 7: 4
    Value Above in Transformed Col 7: 2
    Input pixel was white (0). Expected 5, got 2. Should be value from above in transformed (2).
    -> Mismatch: Expected 5 but value above was 2.
  Pixel (5, 9):
    Input Value: 0
    Expected Output Value: 0
    Transformed Output Value: 2
    Topmost Red Row in Input Col 9: 4
    Value Above in Transformed Col 9: 2
    Input pixel was white (0). Expected 0, got 2. Should be value from above in transformed (2).
    -> Mismatch: Expected 0 but value above was 2.

Example 2 Analysis:
  Unique colors: [0 1 2]
  Solid red row index: 3
  Rule 1 conditions met: True

Example 3 Analysis:
  Unique colors: [0 2 8]
  Solid red row index: -1
  All red pixels on r=c+1 or r=c+2: True
  Rule 2 conditions met: True

```
**Facts (YAML)**


```yaml
task_context:
  primary_color: red (2)
  background_color: white (0)
  grid_dimensions: variable (up to 30x30)
  rules_prioritized: true

rule_1_conditions:
  - property: unique_colors_count
    value: 3
  - property: solid_row_exists
    color: red (2)
    value: true

rule_1_actions:
  - action: identify_third_color
    inputs: [unique_colors, primary_color, background_color]
  - action: find_topmost_solid_row
    color: red (2)
    output: solid_row_index
  - action: create_output_grid
    dimensions: input_grid_dimensions
  - action: fill_rows
    target: output_grid
    rows: 0 to solid_row_index - 1
    color: background_color (0)
  - action: fill_row
    target: output_grid
    row: solid_row_index
    color: primary_color (2)
  - action: fill_rows
    target: output_grid
    rows: solid_row_index + 1 to end
    color: third_color

rule_2_conditions:
  - property: unique_colors_count
    value: 3
  - property: solid_row_exists
    color: red (2)
    value: false
  - property: all_pixels_of_color_satisfy_condition
    color: red (2)
    condition: row == col + 1 OR row == col + 2

rule_2_actions:
  - action: identify_third_color
    inputs: [unique_colors, primary_color, background_color]
  - action: create_output_grid
    dimensions: input_grid_dimensions
  - action: fill_by_position
    target: output_grid
    condition: row < col + 1
    color: background_color (0)
  - action: fill_by_position
    target: output_grid
    condition: row == col + 1 OR row == col + 2
    color: primary_color (2)
  - action: fill_by_position
    target: output_grid
    condition: row > col + 2
    color: third_color

rule_3_conditions: # Default rule if Rule 1 and Rule 2 do not apply
  - property: default
    value: true

rule_3_actions:
  - action: process_columns_independently
    target: input_grid
    output: output_grid
  - sub_action: find_topmost_pixel_in_column
    color: red (2)
    input: input_column
    output: topmost_red_row_index
  - sub_action_conditional: if topmost_red_row_index is found
    - sub_action: fill_column_rows
      target: output_column
      rows: 0 to topmost_red_row_index - 1
      color: background_color (0)
    - sub_action: set_pixel
      target: output_column
      row: topmost_red_row_index
      color: primary_color (2) # Overwrite original color at this position
    - sub_action: process_column_rows_downward
      target: output_column
      start_row: topmost_red_row_index + 1
      logic: |
        For each pixel (r, c) from start_row downwards:
        If input_grid[r, c] is background_color (0):
          output_grid[r, c] = output_grid[r - 1, c] (propagate from above)
        Else:
          output_grid[r, c] = input_grid[r, c] (keep original color)
  - sub_action_conditional: if topmost_red_row_index is not found
    - sub_action: copy_column
      source: input_column
      target: output_column

```


**Natural Language Program**

The transformation determines the output grid by applying the first matching rule from the following prioritized list, using red (2) as the primary color and white (0) as the background color:

1.  **Solid Row Separation Rule:** Check if the input grid contains exactly three unique colors AND if it has a horizontal row composed entirely of the primary color (red). If both conditions are true:
    *   Identify the 'third color' (neither white nor red).
    *   Find the row index (`sr`) of the topmost solid red row.
    *   Create the output grid by filling rows `0` to `sr-1` with white, row `sr` with red, and rows `sr+1` to the bottom with the 'third color'.

2.  **Fixed Diagonal Pattern Rule:** If Rule 1 does not apply, check if the input grid contains exactly three unique colors AND if *all* red pixels are located at positions `(r, c)` where `r = c + 1` or `r = c + 2`. If both conditions are true:
    *   Identify the 'third color'.
    *   Create the output grid with a fixed pattern: pixels where `r < c + 1` are white, pixels where `r == c + 1` or `r == c + 2` are red, and pixels where `r > c + 2` are the 'third color'.

3.  **Column Filter with Conditional Downward Propagation Rule:** If neither Rule 1 nor Rule 2 applies, construct the output grid by processing each column independently based on the input grid:
    *   Find the row index (`mr`) of the topmost red pixel in the input column.
    *   If no red pixel exists in the input column, the output column is identical to the input column.
    *   If a topmost red pixel exists at `mr` in the input column:
        *   Initialize the corresponding output column.
        *   Set rows `0` to `mr-1` in the output column to white.
        *   Set the pixel at `(mr, col)` in the output column to red.
        *   For each row `r` from `mr + 1` downwards to the bottom of the grid:
            *   Examine the pixel at `(r, col)` in the *input* grid.
            *   If the input pixel `input_grid[r, col]` is white (0), set the output pixel `output_grid[r, col]` to the color of the pixel directly above it in the *output* grid (`output_grid[r - 1, col]`).
            *   Otherwise (if `input_grid[r, col]` is not white), set the output pixel `output_grid[r, col]` to its original color from the input grid (`input_grid[r, col]`).
