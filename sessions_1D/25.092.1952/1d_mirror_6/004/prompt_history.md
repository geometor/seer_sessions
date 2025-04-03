
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
```python
import numpy as np

def find_anchor_in_row(row_data, anchor_color=9):
    """
    Finds the column index of the first occurrence of the anchor pixel 
    in a given 1D array (row).
    Returns the column index or None if not found.
    """
    # Iterate through the row data with index
    for c_idx, pixel in enumerate(row_data):
        # Check if the pixel matches the anchor color
        if pixel == anchor_color:
            # Return the column index if found
            return c_idx
    # Return None if the loop completes without finding the anchor
    return None 

def find_payload_in_row(row_data, background_color=0, anchor_color=9):
    """
    Finds the first contiguous horizontal line of non-background, non-anchor 
    color in a given 1D array (row).
    Returns its color, starting column index, and length, or (None, None, None) 
    if not found.
    """
    width = len(row_data)
    # Iterate through the row data to find the start of the payload
    for c_idx in range(width):
        pixel = row_data[c_idx]
        # Check if the pixel is a potential payload color
        if pixel != background_color and pixel != anchor_color:
            # Check if this is the actual start of the line 
            # (i.e., it's the first pixel or the previous pixel is different)
            if c_idx == 0 or row_data[c_idx-1] != pixel:
                payload_color = pixel
                payload_col_start_in = c_idx
                payload_length = 0
                # Measure the length of the contiguous line of this color
                for k in range(c_idx, width):
                    if row_data[k] == payload_color:
                        payload_length += 1
                    else:
                        # Stop counting when the color changes or end of row
                        break 
                # Return the found payload details
                return payload_color, payload_col_start_in, payload_length
    # Return None if no payload line is found in the row
    return None, None, None 


def transform(input_grid):
    """
    Transforms an input grid based on finding an anchor pixel (maroon, 9) and a 
    horizontal payload line (any other non-white color) in the first row. 
    The payload line is moved to a new row (assumed to be row 1 in a 2-row 
    output grid) and its horizontal position is adjusted relative to the anchor.

    The transformation rule identified from examples is:
    The horizontal distance from the anchor's column to the END column of the 
    payload line in the input determines the horizontal distance from the 
    anchor's column to the START column of the payload line in the output.

    Assumptions derived from the provided examples:
    1. The anchor pixel (9) and the payload line exist and are located in the 
       first row/list element of the input_grid data structure.
    2. The required output grid always has a height of 2.
    3. The output grid has the same width as the input row where objects were found.
    4. The anchor's final position in the output grid is in row index 1, at the 
       same column index it occupied in the input row.
    5. The entire payload line moves to row index 1 in the output grid.
    """
    
    # --- Input Validation and Analysis ---
    # Check if input_grid is a list, is not empty, and its first element is also a list
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        print("Warning: Invalid input grid format. Expecting List[List[int]].")
        # Return an empty structure that matches the expected output format (2 rows)
        return [[], []] 
        
    # Attempt to convert the first row to a NumPy array for easier processing
    try:
        # Assume relevant objects are only in the first row/list element
        input_row_data = np.array(input_grid[0], dtype=int)
    except (ValueError, TypeError):
         print("Warning: Could not convert first input row to numpy array.")
         return [[], []] 

    input_width = len(input_row_data)
    # Handle case where the first row is empty
    if input_width == 0:
         print("Warning: Input row is empty.")
         return [[], []] # Return empty 2-row grid

    # --- Define Output Structure ---
    # Define expected output dimensions based on consistent example pattern
    output_height = 2 
    output_width = input_width
    # Define the assumed output row index for both anchor & payload based on examples
    r_output = 1 

    # --- Find Input Objects ---
    # Find the column index ('c_anchor') of the anchor pixel in the input row
    c_anchor = find_anchor_in_row(input_row_data, anchor_color=9)
    
    # Find payload details ('payload_color', 'c_payload_start_in', 'l_payload') in the input row
    payload_color, c_payload_start_in, l_payload = find_payload_in_row(input_row_data)

    # --- Handle Missing Objects ---
    # Check if either the anchor or the payload was not found
    if c_anchor is None or payload_color is None:
        # If essential components are missing, create a default output grid.
        print(f"Warning: Anchor {'found' if c_anchor is not None else 'NOT FOUND'}, Payload {'found' if payload_color is not None else 'NOT FOUND'}. Returning default grid.")
        # Create a 2xWidth grid filled with the background color (0).
        output_grid = np.zeros((output_height, output_width), dtype=int)
        # If the anchor *was* found, place it in its assumed output position.
        if c_anchor is not None:
            # Check bounds before placing anchor (should be safe given width calculation)
            if 0 <= r_output < output_height and 0 <= c_anchor < output_width:
                 output_grid[r_output, c_anchor] = 9 
        # Return the default grid (empty or with only anchor)
        return output_grid.tolist()

    # --- Transformation Calculation ---
    # Calculate the column index of the last pixel of the payload line in the input row
    c_payload_end_in = c_payload_start_in + l_payload - 1

    # Calculate the key horizontal distance: from anchor column to payload end column
    dist = c_anchor - c_payload_end_in
    
    # Calculate the starting column for the payload line in the output grid
    # The rule is: output_start_column = anchor_column + distance
    c_payload_start_out = c_anchor + dist
    
    # --- Populate Output Grid ---
    # Initialize the final output grid with the background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the anchor pixel in its assumed output position (row 'r_output', same column 'c_anchor')
    # Include basic bounds check for robustness, although should be valid by construction
    if 0 <= r_output < output_height and 0 <= c_anchor < output_width:
        output_grid[r_output, c_anchor] = 9
    
    # Draw the payload line at its new position in the output grid
    # The row is 'r_output', starting column is 'c_payload_start_out'
    for i in range(l_payload):
        current_col = c_payload_start_out + i
        # Check if the current column index is within the grid's width bounds
        if 0 <= current_col < output_width:
            # Place the payload pixel in the calculated position (row 'r_output')
            # This will overwrite the background '0'
            output_grid[r_output, current_col] = payload_color
            
    # Convert the final NumPy array grid back to a list of lists for the return value
    return output_grid.tolist()
```
