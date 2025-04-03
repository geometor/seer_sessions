
## train_1

**input:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 3 3 3 3 3 3 3 3 0
```


## train_3

**input:**
```
0 0 2 2 2 2 2 2 2 2 2 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Task Elements:**

1.  **Input Grid Structure:** The input grids consistently feature two distinct non-white elements:
    *   A single maroon (9) pixel.
    *   A horizontal line segment composed of pixels of another single color (red '2' or green '3' in the examples).
    *   The rest of the grid is white (0).
2.  **Object Identification:**
    *   **Anchor Object:** The single maroon pixel acts as a fixed reference point or an anchor. Its position seems crucial.
    *   **Payload Object:** The horizontal line segment is the object that undergoes transformation. Its color and length are preserved.
3.  **Transformation Pattern:**
    *   The anchor (maroon pixel) remains unchanged in position from input to output.
    *   The payload (horizontal line) changes its position significantly.
    *   **Vertical Movement:** The payload line moves from its original row (row 0 in all examples) to the row containing the anchor pixel (row 1 in all examples).
    *   **Horizontal Movement:** The payload line shifts horizontally to the right. The amount of this shift appears to be directly determined by the column index of the anchor pixel.
4.  **Rule Inference:** The transformation rule seems to involve using the anchor pixel's coordinates to determine the final position of the payload line. The anchor's row dictates the payload's final row, and the anchor's column dictates the magnitude of the payload's horizontal shift.

**YAML Facts:**


```yaml
Task: Reposition a horizontal line based on an anchor pixel.

Input_Objects:
  - Type: Pixel
    Color: Maroon (9)
    Identifier: Anchor
    Quantity: 1
  - Type: Line
    Orientation: Horizontal
    Color: Any (non-Maroon, non-White)
    Identifier: Payload
    Quantity: 1
  - Type: Background
    Color: White (0)

Anchor_Properties:
  - Position: (row, column) - denoted as (R_anchor, C_anchor)

Payload_Properties:
  - Color: C_payload (constant)
  - Length: L_payload (constant)
  - Input_Position:
      Row: R_payload_in
      Column_Start: C_payload_start_in
      Column_End: C_payload_end_in

Relationships:
  - The Anchor pixel is unique (only one maroon pixel).
  - The Payload line is unique (only one horizontal line of a specific non-maroon color).
  - In the input examples, R_payload_in is different from R_anchor.

Actions:
  - Identify the Anchor pixel and its position (R_anchor, C_anchor).
  - Identify the Payload line, its color (C_payload), length (L_payload), and its input starting column (C_payload_start_in).
  - The Anchor pixel's position in the output remains (R_anchor, C_anchor).
  - Calculate the Payload line's output starting column: C_payload_start_out = C_payload_start_in + C_anchor
  - The Payload line's output position is:
      Row: R_anchor
      Column_Start: C_payload_start_out
      Column_End: C_payload_start_out + L_payload - 1
  - Reconstruct the output grid with the Anchor and the repositioned Payload line on a white background.

Output_Objects:
  - Type: Pixel
    Identifier: Anchor
    Position: (R_anchor, C_anchor) # Unchanged from input
    Color: Maroon (9)
  - Type: Line
    Identifier: Payload
    Orientation: Horizontal
    Color: C_payload # Unchanged from input
    Length: L_payload # Unchanged from input
    Position:
      Row: R_anchor
      Column_Start: C_payload_start_out
      Column_End: C_payload_start_out + L_payload - 1
  - Type: Background
    Color: White (0)

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, or as an empty grid of the same dimensions filled with white pixels.
2.  Find the single maroon pixel (the anchor) in the input grid and record its row (`R_anchor`) and column (`C_anchor`). Keep this pixel at (`R_anchor`, `C_anchor`) in the output grid.
3.  Find the contiguous horizontal line of non-white, non-maroon pixels (the payload) in the input grid. Record its color (`C_payload`), its starting column (`C_payload_start_in`), and its length (`L_payload`).
4.  Remove the payload line from its original position in the (initially copied or empty) output grid (if necessary, ensure these locations are white).
5.  Calculate the new starting column for the payload line in the output grid: `C_payload_start_out = C_payload_start_in + C_anchor`.
6.  Draw the payload line in the output grid using its original color (`C_payload`) and length (`L_payload`), starting at row `R_anchor` and column `C_payload_start_out`, extending `L_payload` pixels to the right.
```python
"""
Transforms the input grid by repositioning a horizontal line based on the 
position of a single anchor pixel (maroon, 9).

1. Find the single maroon (9) pixel (the anchor) and record its row and 
   column (R_anchor, C_anchor).
2. Find the contiguous horizontal line of non-white (0), non-maroon (9) 
   pixels (the payload). Record its color (C_payload), starting column 
   (C_payload_start_in), and length (L_payload).
3. Initialize an output grid of the same dimensions as the input, filled 
   with white (0).
4. Place the anchor pixel at its original position (R_anchor, C_anchor) in 
   the output grid.
5. Calculate the new starting column for the payload line: 
   C_payload_start_out = C_payload_start_in + C_anchor.
6. Draw the payload line in the output grid using its color (C_payload) and 
   length (L_payload), starting at row R_anchor and column C_payload_start_out.
"""

import numpy as np

def find_anchor(grid, anchor_color=9):
    """Finds the coordinates of the first pixel with the anchor_color."""
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == anchor_color:
                return r_idx, c_idx
    return None # Should not happen based on task description

def find_payload_line(grid, background_color=0, anchor_color=9):
    """
    Finds the horizontal payload line (non-background, non-anchor color).
    Returns its color, input row, input starting column, and length.
    """
    height, width = grid.shape
    for r_idx in range(height):
        for c_idx in range(width):
            pixel = grid[r_idx, c_idx]
            if pixel != background_color and pixel != anchor_color:
                # Found the start of the payload line
                payload_color = pixel
                payload_row_in = r_idx
                payload_col_start_in = c_idx
                payload_length = 0
                # Measure length
                for k in range(c_idx, width):
                    if grid[r_idx, k] == payload_color:
                        payload_length += 1
                    else:
                        break # End of line
                return payload_color, payload_row_in, payload_col_start_in, payload_length
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with white background
    output_grid = np.zeros_like(input_np) # Default value is 0 (white)

    # 1. Find the anchor pixel
    anchor_pos = find_anchor(input_np)
    if anchor_pos is None:
        # Handle error or return input/empty grid if anchor not found
        return output_grid.tolist() 
    anchor_row, anchor_col = anchor_pos
    
    # 2. Find the payload line
    payload_info = find_payload_line(input_np)
    if payload_info is None:
        # Handle error or return grid with just anchor if payload not found
        output_grid[anchor_row, anchor_col] = 9 # Still place anchor
        return output_grid.tolist()
    payload_color, payload_row_in, payload_col_start_in, payload_length = payload_info

    # 3. Place the anchor in the output grid
    output_grid[anchor_row, anchor_col] = 9

    # 4. Calculate the new starting column for the payload
    payload_col_start_out = payload_col_start_in + anchor_col

    # 5. Draw the payload line in the output grid at the new position
    # The new row is the anchor's row
    payload_row_out = anchor_row
    
    # Ensure drawing stays within bounds (horizontally)
    for i in range(payload_length):
        current_col = payload_col_start_out + i
        if 0 <= payload_row_out < height and 0 <= current_col < width:
            output_grid[payload_row_out, current_col] = payload_color
        # else: pixel would be out of bounds, skip drawing it
        # Based on examples, this shouldn't be necessary, but good practice

    return output_grid.tolist()
```
