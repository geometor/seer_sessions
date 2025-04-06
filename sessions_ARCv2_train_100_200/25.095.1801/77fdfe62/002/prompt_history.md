
## train_1

**input:**
```
9 1 0 0 1 4
1 1 1 1 1 1
0 1 8 8 1 0
0 1 8 0 1 0
1 1 1 1 1 1
2 1 0 0 1 3
```


**output:**
```
9 4
2 0
```


## train_2

**input:**
```
2 1 0 0 0 0 1 3
1 1 1 1 1 1 1 1
0 1 0 8 0 0 1 0
0 1 8 8 0 8 1 0
0 1 0 0 8 0 1 0
0 1 8 0 8 8 1 0
1 1 1 1 1 1 1 1
4 1 0 0 0 0 1 6
```


**output:**
```
0 2 0 0
2 2 0 3
0 0 6 0
4 0 6 6
```


## train_3

**input:**
```
6 1 0 0 0 0 1 2
1 1 1 1 1 1 1 1
0 1 0 8 0 8 1 0
0 1 8 8 8 0 1 0
0 1 8 0 8 8 1 0
0 1 8 8 8 0 1 0
1 1 1 1 1 1 1 1
7 1 0 0 0 0 1 4
```


**output:**
```
0 6 0 2
6 6 2 0
7 0 4 4
7 7 4 0
```

Okay, let's analyze the provided examples.

**Perception of Elements:**

1.  **Input/Output Format:** Both inputs and outputs are grids (matrices) of single-digit integers.
2.  **Grid Size Transformation:** The output grid is consistently smaller than the input grid.
3.  **Key Numbers:**
    *   `1`: Appears to form a rectangular boundary or frame within the input grid.
    *   `8`: Appears within the region enclosed by the `1`s.
    *   `0`: Appears both inside and outside the `1` boundary.
    *   Other numbers (`2`, `3`, `4`, `6`, `7`, `9` in the examples): Appear outside the `1` boundary, typically at or near the four absolute corners of the input grid.
4.  **Core Structure:** The input seems to consist of four "corner" values located outside a frame of `1`s, and an "internal pattern" of `0`s and `8`s located inside the frame.
5.  **Output Construction:** The output grid's structure and values appear derived from the "internal pattern" (`0`s and `8`s), where the `8`s are selectively replaced by the "corner" values from the input. The `0`s from the internal pattern seem to carry over directly to the output.

**YAML Facts:**


```yaml
task_elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - contains: boundary_frame, internal_pattern, corner_values
  - object: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: smaller than input_grid, matches dimensions of internal_pattern
  - object: boundary_frame
    properties:
      - composed_of: integer 1
      - shape: rectangle
      - location: within input_grid
      - function: separates corner_values from internal_pattern
  - object: internal_pattern
    properties:
      - composed_of: integers 0 and 8
      - location: inside boundary_frame in input_grid
      - structure: defines the structure and size of the output_grid
  - object: corner_values
    properties:
      - quantity: 4
      - type: integers (non-1, non-8, potentially 0)
      - location: outside boundary_frame, typically at the absolute corners of input_grid (e.g., top-left, top-right, bottom-left, bottom-right)
      - role: values used to replace '8's in the output_grid based on position
  - relationship: internal_pattern_to_output
    properties:
      - action: transform
      - rule: Iterate through internal_pattern cells. If cell value is 0, copy 0 to corresponding output cell. If cell value is 8, determine the cell's quadrant (TL, TR, BL, BR) within the internal_pattern and copy the corresponding corner_value (TL, TR, BL, BR) from the input_grid to the output cell.
```


**Natural Language Program:**

1.  **Identify Components:**
    *   Locate the four corner values from the absolute corners of the input grid: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), and Bottom-Right (BR).
    *   Identify the rectangular frame composed of `1`s within the input grid.
    *   Extract the subgrid located strictly inside the `1` frame; this is the "internal pattern" grid, composed of `0`s and `8`s. Note its dimensions (height `h`, width `w`).
2.  **Initialize Output:** Create a new grid (the output grid) with the same dimensions (`h` x `w`) as the internal pattern grid.
3.  **Populate Output Grid:** Iterate through each cell `(r, c)` (row `r`, column `c`) of the internal pattern grid:
    *   Get the value `v` at `(r, c)` from the internal pattern.
    *   If `v` is `0`, set the value of the output grid at `(r, c)` to `0`.
    *   If `v` is `8`, determine the quadrant of the cell `(r, c)` within the internal pattern grid:
        *   If `r < h/2` and `c < w/2` (Top-Left quadrant), set the output grid value at `(r, c)` to the TL corner value.
        *   If `r < h/2` and `c >= w/2` (Top-Right quadrant), set the output grid value at `(r, c)` to the TR corner value.
        *   If `r >= h/2` and `c < w/2` (Bottom-Left quadrant), set the output grid value at `(r, c)` to the BL corner value.
        *   If `r >= h/2` and `c >= w/2` (Bottom-Right quadrant), set the output grid value at `(r, c)` to the BR corner value.
4.  **Return Output:** The fully populated grid is the final output.
```python
"""
Transforms an input grid based on the following logic:
1. Identifies four corner values from the absolute corners of the input grid (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
2. Locates a rectangular frame composed of '1's within the input grid.
3. Extracts the subgrid (internal pattern) located strictly inside the '1' frame, which consists of '0's and '8's.
4. Creates an output grid with the same dimensions as the internal pattern grid.
5. Populates the output grid by iterating through the internal pattern:
   - If a cell in the internal pattern is '0', the corresponding cell in the output grid is set to '0'.
   - If a cell in the internal pattern is '8', the corresponding cell in the output grid is set to one of the corner values based on the cell's quadrant within the internal pattern (TL quadrant maps to TL corner value, TR to TR, BL to BL, BR to BR).
"""

import numpy as np
from typing import List, Tuple

def find_frame_boundaries(grid: np.ndarray) -> Tuple[int, int, int, int]:
    """Finds the row and column indices defining the inner boundary of the '1' frame."""
    rows, cols = grid.shape
    min_row, max_row = -1, -1
    min_col, max_col = -1, -1

    # Find first and last rows containing non-1s (to identify frame roughly)
    # This assumes the frame isn't at the absolute edge, which holds for examples
    for r in range(rows):
        if not np.all(grid[r] == 1):
            if min_row == -1:
                min_row = r
            max_row = r

    for c in range(cols):
         if not np.all(grid[:, c] == 1):
            if min_col == -1:
                min_col = c
            max_col = c

    # The internal pattern is *inside* the frame, so boundaries are +1/-1
    # Note: This logic assumes a frame of thickness 1 surrounding the internal pattern.
    # Based on examples, the frame seems to be exactly at row/col `min_row`, `max_row`, `min_col`, `max_col`.
    # So the internal pattern starts at row `min_row + 1` and col `min_col + 1`.
    frame_top = min_row
    frame_bottom = max_row
    frame_left = min_col
    frame_right = max_col

    # The internal pattern is between these frame boundaries
    internal_top = frame_top + 1
    internal_bottom = frame_bottom -1 # Exclusive index for slicing
    internal_left = frame_left + 1
    internal_right = max_col - 1 # Exclusive index for slicing

    # Return the start/end indices for slicing the internal pattern
    return internal_top, internal_bottom + 1, internal_left, internal_right + 1


def extract_internal_pattern(grid: np.ndarray, top: int, bottom: int, left: int, right: int) -> np.ndarray:
    """Extracts the subgrid within the given boundaries."""
    return grid[top:bottom, left:right]

def get_corner_values(grid: np.ndarray) -> Tuple[int, int, int, int]:
    """Extracts the four corner values from the absolute corners of the grid."""
    rows, cols = grid.shape
    tl = grid[0, 0]
    tr = grid[0, cols - 1]
    bl = grid[rows - 1, 0]
    br = grid[rows - 1, cols - 1]
    return tl, tr, bl, br

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)

    # --- Identify Components ---
    # 1. Get the four corner values
    tl_corner, tr_corner, bl_corner, br_corner = get_corner_values(grid_np)

    # 2. Find the boundaries of the internal pattern (inside the '1' frame)
    # We need to locate the frame first. Frame rows/cols usually contain only '1's
    # except where they intersect the internal pattern area.
    # A simpler approach for the given examples: find the first/last row/col
    # that is *not* entirely composed of '1's. The internal pattern is inside this.
    
    rows_with_non_ones = [r for r in range(grid_np.shape[0]) if not np.all(grid_np[r] == 1)]
    cols_with_non_ones = [c for c in range(grid_np.shape[1]) if not np.all(grid_np[:, c] == 1)]
    
    if not rows_with_non_ones or not cols_with_non_ones:
         # Handle cases where no clear frame/internal pattern is found (e.g., all 1s)
         # Based on examples, this shouldn't happen.
         # Let's assume frame exists and find its boundaries more directly
         # Find rows/cols that contain a '1' but are not *all* '1's - these define the frame boundary adjacent to the pattern
         
         frame_rows = []
         for r in range(grid_np.shape[0]):
             row = grid_np[r,:]
             if 1 in row and not np.all(row == 1):
                 frame_rows.append(r)
         frame_cols = []
         for c in range(grid_np.shape[1]):
              col = grid_np[:,c]
              if 1 in col and not np.all(col == 1):
                  frame_cols.append(c)
         
         if not frame_rows or not frame_cols:
            # Fallback or raise error if frame isn't found
            # Based on structure, the core pattern should be bounded by 1s
            # Let's try the boundary finding function
             try:
                 internal_top, internal_bottom, internal_left, internal_right = find_frame_boundaries(grid_np)
             except: # If boundary finding fails, maybe it's a simpler case?
                 raise ValueError("Could not determine frame boundaries.") # Or return empty?
         else:
             internal_top = min(frame_rows) + 1
             internal_bottom = max(frame_rows) # Exclusive index for slicing
             internal_left = min(frame_cols) + 1
             internal_right = max(frame_cols) # Exclusive index for slicing

    else:
        # The internal pattern rows/cols are between the min/max row/col containing non-1s
        internal_top = min(rows_with_non_ones)
        internal_bottom = max(rows_with_non_ones) + 1 # Exclusive index for slicing
        internal_left = min(cols_with_non_ones)
        internal_right = max(cols_with_non_ones) + 1 # Exclusive index for slicing


    # 3. Extract the internal pattern subgrid
    internal_pattern = grid_np[internal_top:internal_bottom, internal_left:internal_right]

    # --- Initialize Output ---
    # Get dimensions of the internal pattern
    h, w = internal_pattern.shape
    # Create output grid with the same dimensions, initialized perhaps with zeros
    output_grid_np = np.zeros((h, w), dtype=int)

    # --- Populate Output Grid ---
    # Iterate through each cell (r, c) of the internal pattern
    for r in range(h):
        for c in range(w):
            # Get the value 'v' from the internal pattern
            v = internal_pattern[r, c]

            # If v is 0, copy 0 to the output
            if v == 0:
                output_grid_np[r, c] = 0
            # If v is 8, determine the quadrant and assign the corresponding corner value
            elif v == 8:
                # Determine quadrant (using floating point division for midpoint)
                # Top-Left quadrant
                if r < h / 2 and c < w / 2:
                    output_grid_np[r, c] = tl_corner
                # Top-Right quadrant
                elif r < h / 2 and c >= w / 2:
                    output_grid_np[r, c] = tr_corner
                # Bottom-Left quadrant
                elif r >= h / 2 and c < w / 2:
                    output_grid_np[r, c] = bl_corner
                # Bottom-Right quadrant
                elif r >= h / 2 and c >= w / 2:
                    output_grid_np[r, c] = br_corner
            # Handle unexpected values if necessary (though examples only show 0 and 8)
            # else:
            #    output_grid_np[r, c] = v # or some error value?

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    # --- Return Output ---
    return output_grid
```
