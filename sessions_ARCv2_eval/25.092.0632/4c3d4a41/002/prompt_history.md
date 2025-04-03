
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 3 0 2 0 5 0 5 0 5
0 5 0 0 0 0 0 5 0 5 0 3 0 2 0 4 0 7 0 5
0 5 0 5 0 0 0 5 0 5 0 3 0 2 0 4 0 7 0 5
0 5 0 5 0 5 0 5 0 0 0 0 0 2 0 4 0 0 0 5
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 3 0 2 0 4 0 7 0 5
0 0 0 0 0 0 0 0 0 5 0 5 0 2 0 4 0 5 0 5
0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 4 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 5 0 5 0 4 0 5 0 5 0 8 0 5
0 5 0 0 0 0 0 5 0 5 0 4 0 6 0 7 0 8 0 5
0 5 0 5 0 5 0 5 0 0 0 0 0 6 0 7 0 0 0 5
0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 5 0 4 0 5 0 5 0 8 0 5
0 0 0 0 0 0 0 0 0 5 0 4 0 6 0 7 0 5 0 5
0 0 0 0 0 0 0 0 0 5 0 5 0 6 0 7 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0 5
0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5
```

**Perception of Task Elements:**

1.  **Grid Structure:** The input and output grids are consistently 8 rows by 20 columns. They are visually divided into two halves: a left side (columns 0-8) and a right side (columns 9-19).
2.  **Right Frame:** The right side contains a permanent gray (5) rectangular frame along its perimeter (row 0/col 9-19, row 7/col 9-19, col 9/row 0-7, col 19/row 0-7).
3.  **Right Internal Columns:** Inside the frame, columns 11, 13, 15, and 17 contain vertical arrangements of colored pixels (or white pixels), separated by columns of mostly white pixels (10, 12, 14, 16, 18). These colored columns vary between examples.
4.  **Left Gray Pixels:** The left side (columns 0-8) contains scattered gray (5) pixels. The pattern of these gray pixels differs between examples.
5.  **Transformation - Left Side:** In the output, all gray (5) pixels originally present in columns 0-8 of the input grid are removed (changed to white (0)).
6.  **Transformation - Right Side:** Specific pixels within the internal columns (11, 13, 15, 17) on the right side are changed to gray (5). This change appears to be triggered by the presence of gray pixels in specific columns on the *left* side of the input grid.
7.  **Mapping:** There's a positional correspondence:
    *   Gray pixels in input column 1 affect output column 11.
    *   Gray pixels in input column 3 affect output column 13.
    *   Gray pixels in input column 5 affect output column 15.
    *   Gray pixels in input column 7 affect output column 17.
8.  **Conditional Change:** The change to gray (5) in the target right columns (11, 13, 15, 17) only occurs if the *original* color of the target pixel in the input grid is *not* magenta (6) and *not* orange (7). If a gray pixel exists in the corresponding trigger column (1, 3, 5, or 7) on the left, but the target pixel on the right is magenta (6) or orange (7), the target pixel remains unchanged. If the target pixel is any other color (including white (0)), it changes to gray (5).

**YAML Facts:**

```
yaml
Grid:
  Properties:
    Size: Fixed 8 rows x 20 columns
    Background: Primarily white (0)
  Subregions:
    - Left_Half: Columns 0-8
    - Right_Half: Columns 9-19

Objects:
  - Type: Frame
    Location: Right_Half perimeter (rows 0 & 7, cols 9 & 19)
    Color: Gray (5)
    Persistence: Unchanged between input and output

  - Type: Trigger_Pixels
    Location: Left_Half, specifically columns 1, 3, 5, 7
    Color: Gray (5)
    Role: Initiate changes in the Right_Half

  - Type: Target_Pixels
    Location: Right_Half, specifically columns 11, 13, 15, 17 (corresponding to Trigger_Pixels)
    Color: Varies (can be any color 0-9)
    Role: Potentially modified based on Trigger_Pixels and own color

Relationships:
  - Type: Mapping
    Source: Trigger_Pixels at (row, col_left) where col_left is in {1, 3, 5, 7}
    Target: Target_Pixels at (row, col_right)
    Rule:
      - If col_left = 1, then col_right = 11
      - If col_left = 3, then col_right = 13
      - If col_left = 5, then col_right = 15
      - If col_left = 7, then col_right = 17

Actions:
  - Action: Remove_Left_Grays
    Target: All Gray (5) pixels in Left_Half (columns 0-8)
    Result: Change target pixels to White (0)

  - Action: Conditional_Update_Right
    Condition_Source: Presence of a Trigger_Pixel at (row, col_left) in input
    Condition_Target: Color of the corresponding Target_Pixel at (row, col_right) in input
    Rule:
      - IF a Gray (5) pixel exists at (row, col_left) where col_left is in {1, 3, 5, 7} in the input
      - AND IF the color of the pixel at the mapped position (row, col_right) in the input is NOT Magenta (6) AND NOT Orange (7)
      - THEN change the pixel at (row, col_right) to Gray (5) in the output.
    Otherwise: The pixel at (row, col_right) retains its original input color.

  - Action: Copy_Unchanged
    Target: All pixels not affected by Remove_Left_Grays or Conditional_Update_Right (including the Frame and unaffected Target_Pixels)
    Result: Pixel color remains the same as in the input.

```python
import numpy as np

"""
The transformation involves two main operations based on the input grid structure, which is consistently 8x20 and visually divided into left (cols 0-8) and right (cols 9-19) halves.

1.  **Clear Left Grays:** All gray (5) pixels located in the left half (columns 0 through 8) of the input grid are changed to white (0) in the output grid.

2.  **Conditional Right Update:** The presence of gray (5) pixels in specific columns of the left half (1, 3, 5, 7) triggers potential changes in corresponding columns of the right half (11, 13, 15, 17, respectively).
    - For each row:
      - If input_grid[row][1] is gray (5), check input_grid[row][11]. If input_grid[row][11] is NOT magenta (6) and NOT orange (7), change output_grid[row][11] to gray (5).
      - If input_grid[row][3] is gray (5), check input_grid[row][13]. If input_grid[row][13] is NOT magenta (6) and NOT orange (7), change output_grid[row][13] to gray (5).
      - If input_grid[row][5] is gray (5), check input_grid[row][15]. If input_grid[row][15] is NOT magenta (6) and NOT orange (7), change output_grid[row][15] to gray (5).
      - If input_grid[row][7] is gray (5), check input_grid[row][17]. If input_grid[row][17] is NOT magenta (6) and NOT orange (7), change output_grid[row][17] to gray (5).
    - Pixels in the right half that do not meet these trigger and color conditions, or are not in the target columns (11, 13, 15, 17), remain unchanged from the input. The gray frame on the right is also preserved.

All other pixels (those not cleared in the left half and not conditionally updated in the right half) retain their original color from the input grid.
"""

def transform(input_grid):
    """
    Applies the described transformation rules to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    rows, cols = input_np.shape

    # 1. Clear Left Grays (Columns 0-8)
    for r in range(rows):
        for c in range(min(cols, 9)): # Iterate only through columns 0 to 8
            if input_np[r, c] == 5: # Check if the pixel is gray
                output_grid[r, c] = 0 # Change it to white in the output

    # 2. Conditional Right Update (Based on cols 1, 3, 5, 7 influencing 11, 13, 15, 17)
    # Define the mapping from trigger columns (left) to target columns (right)
    trigger_target_map = {
        1: 11,
        3: 13,
        5: 15,
        7: 17
    }

    # Define the colors that block the update
    blocking_colors = {6, 7} # Magenta and Orange

    for r in range(rows):
        for trigger_col, target_col in trigger_target_map.items():
            # Ensure trigger and target columns are within grid bounds
            if trigger_col < cols and target_col < cols:
                # Check if the trigger pixel in the *input* grid is gray
                if input_np[r, trigger_col] == 5:
                    # Check if the target pixel in the *input* grid is NOT a blocking color
                    target_pixel_color = input_np[r, target_col]
                    if target_pixel_color not in blocking_colors:
                        # Change the corresponding pixel in the output grid to gray
                        output_grid[r, target_col] = 5

    return output_grid.tolist() # Return as list of lists as per ARC standard output format
```
