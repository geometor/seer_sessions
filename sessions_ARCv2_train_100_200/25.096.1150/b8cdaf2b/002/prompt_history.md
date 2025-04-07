
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

Okay, let's analyze the transformation.

**1. Perception of Elements:**

*   **Input/Output:** Both are 2D grids containing single-digit non-negative integers. 0 represents the background.
*   **Transformation:** The transformation adds new non-zero cells to the grid. The original non-zero cells from the input remain unchanged in the output.
*   **Key Structure:** The process seems triggered by a specific pattern found in the lowest rows of the input grid. This pattern involves a pair of identical non-zero numbers ("flankers") in the lowest non-zero row, enclosing a different non-zero number ("contained"), with specific values required in the row directly above.
*   **Added Elements:** The color (number) added matches the "contained" color. The positions of the added elements depend on the positions of the "flankers" and potentially the structure between the flankers and the contained element.
*   **Two Placement Patterns:** Two distinct patterns emerge for placing the new elements, observed across the examples. One pattern places two elements two rows above the flankers, aligned horizontally with them. The other pattern places four elements: two elements three rows above the flankers (aligned horizontally) and two elements two rows above, horizontally adjacent inwards from the flankers.
*   **Pattern Trigger Detail:** The core pattern requires:
    *   Lowest row `r` with non-zero cells.
    *   Identical flanker cells `F` at `(r, c_left)` and `(r, c_right)`.
    *   A contained segment of cells `C` (where `C != F`) between `c_left` and `c_right` in row `r`. Let the contained segment span columns `c_start` to `c_end`.
    *   Any cells between the flankers and the contained segment in row `r` must be color `F`.
    *   The cells in row `r-1` directly above the contained segment (columns `c_start` to `c_end`) must all be color `F`.
*   **Distinguishing Placement Rules:** The crucial factor determining which placement rule applies seems to be whether the contained segment `C` directly touches *both* flankers `F` in row `r` (i.e., if `c_start == c_left + 1` and `c_end == c_right - 1`).

**2. YAML Facts:**


```yaml
Grid:
  type: 2D array
  elements: integers (0-9)
  background_color: 0

Objects:
  - Cell:
      properties: [row, column, color (integer value)]
  - HorizontalSegment:
      properties: [row, start_column, end_column, color, length]
  - PatternInstance:
      properties:
        - lowest_row_index: r
        - flanker_color: F
        - flanker_left_col: c_left
        - flanker_right_col: c_right
        - contained_color: C (C != F)
        - contained_start_col: c_start
        - contained_end_col: c_end
        - structure_valid: boolean (checks intermediate F's in row r, and F's above C in row r-1)
        - contained_touches_flankers: boolean (c_start == c_left + 1 AND c_end == c_right - 1)

Relationships:
  - spatial: [above, below, left_of, right_of, between, adjacent_to]
  - value: [equal_color, different_color]

Actions:
  - Find Lowest Non-Zero Row: Identify index 'r'.
  - Scan Row: Iterate through cells in a row.
  - Identify Pattern: Match the specific structure (Flankers, Contained, Intermediates, Above).
  - Copy Grid: Duplicate input to create initial output.
  - Place Elements: Modify output grid by setting cell colors based on pattern type.

Placement Rules:
  - Rule_Type_1 (if contained_touches_flankers is true):
      - Add color C at (r-2, c_left)
      - Add color C at (r-2, c_right)
  - Rule_Type_2 (if contained_touches_flankers is false):
      - Add color C at (r-3, c_left)
      - Add color C at (r-3, c_right)
      - Add color C at (r-2, c_left + 1)
      - Add color C at (r-2, c_right - 1)
```


**3. Natural Language Program:**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Find the index `r` of the bottom-most row in the `input_grid` that contains at least one non-zero value.
3.  Iterate through all possible pairs of columns `
```python
import copy
import numpy as np

"""
The transformation rule identifies a specific pattern in the lowest rows of the input grid and adds new elements based on this pattern.

1.  Find the bottom-most row 'r' containing any non-zero values.
2.  In row 'r', search for a pattern consisting of two identical non-zero "flanker" cells (color F) at columns c_left and c_right.
3.  Between these flankers (from c_left + 1 to c_right - 1), identify a contiguous segment of a different non-zero color 'C' (from column c_start to c_end).
4.  Verify that any cells in row 'r' between the left flanker and the start of the contained segment (columns c_left + 1 to c_start - 1) have color F.
5.  Verify that any cells in row 'r' between the end of the contained segment and the right flanker (columns c_end + 1 to c_right - 1) have color F.
6.  Verify that all cells in the row directly above the contained segment (row r-1, columns c_start to c_end) have color F.
7.  If such a pattern is found:
    a. If the contained segment 'C' directly touches both flankers (i.e., c_start == c_left + 1 and c_end == c_right - 1), add two new cells of color C at positions (r-2, c_left) and (r-2, c_right).
    b. Otherwise (if there are intermediate F cells between flankers and the contained segment in row r), add four new cells of color C at positions (r-3, c_left), (r-3, c_right), (r-2, c_left + 1), and (r-2, c_right - 1).
8.  The original input grid cells remain unchanged. Add the new cells to a copy of the input grid.
9.  Return the modified grid. If no pattern is found, return the original grid copy.
"""

def find_lowest_non_zero_row(grid: np.ndarray) -> int:
    """Finds the index of the lowest row containing at least one non-zero value."""
    rows, _ = grid.shape
    for r in range(rows - 1, -1, -1):
        if np.any(grid[r, :] != 0):
            return r
    return -1 # No non-zero row found

def check_row_segment(grid: np.ndarray, r: int, c_start: int, c_end: int, expected_color: int) -> bool:
    """Checks if all cells in a horizontal segment have the expected color."""
    if r < 0 or r >= grid.shape[0]:
        return False # Row out of bounds
    # Ensure columns are within bounds and c_start <= c_end
    if c_start < 0 or c_end >= grid.shape[1] or c_start > c_end:
         # If c_start > c_end, the segment is empty, which is vacuously true
         # Handle potential out-of-bounds if checking an empty segment at boundary
         return c_start > c_end

    return np.all(grid[r, c_start:c_end+1] == expected_color)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the identified pattern.
    """
    # Convert input to numpy array for easier slicing and operations
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Find the lowest non-zero row 'r'
    r = find_lowest_non_zero_row(grid)
    if r <= 0: # Pattern requires at least one row above, so r must be > 0
        return output_grid.tolist()

    # 2. Search for the pattern in row 'r'
    pattern_found = False
    for c_left in range(cols - 1):
        flanker_color = grid[r, c_left]
        if flanker_color == 0:
            continue # Flanker must be non-zero

        for c_right in range(c_left + 2, cols): # Need at least one cell between flankers
            if grid[r, c_right] == flanker_color:
                # Found potential flankers F at (r, c_left) and (r, c_right)

                # 3. Identify the contained segment 'C' between flankers
                contained_start_col = -1
                contained_end_col = -1
                contained_color = -1
                valid_segment = True
                first_non_zero_found = False

                for c in range(c_left + 1, c_right):
                    cell_color = grid[r, c]
                    if cell_color != 0:
                        if not first_non_zero_found:
                            # First non-zero cell in the segment
                            if cell_color == flanker_color:
                                # Segment starts with F, continue checking
                                continue
                            else:
                                # Segment starts with C
                                contained_color = cell_color
                                contained_start_col = c
                                contained_end_col = c
                                first_non_zero_found = True
                        elif first_non_zero_found:
                             # We are inside or just after the C segment
                             if cell_color == contained_color:
                                 contained_end_col = c # Extend the C segment
                             elif cell_color == flanker_color:
                                 # End of C segment, start of potential trailing F segment
                                 break # Move to check trailing Fs
                             else:
                                 # Invalid structure (e.g., F C X ... or F F C X...)
                                 valid_segment = False
                                 break
                    elif first_non_zero_found:
                        # Found a 0 after starting the C segment - invalid structure?
                        # Based on examples, the C segment seems contiguous non-zero
                        valid_segment = False
                        break

                # Check if a valid C segment was found
                if not valid_segment or contained_color == -1 or contained_color == flanker_color:
                    continue

                # 4. Verify intermediate F's before C
                if contained_start_col > c_left + 1:
                    if not check_row_segment(grid, r, c_left + 1, contained_start_col - 1, flanker_color):
                        continue # Invalid intermediate cells before C

                # 5. Verify intermediate F's after C
                if contained_end_col < c_right - 1:
                    if not check_row_segment(grid, r, contained_end_col + 1, c_right - 1, flanker_color):
                        continue # Invalid intermediate cells after C

                # 6. Verify F's in row r-1 above C
                if r == 0: continue # Cannot check row above if r=0
                if not check_row_segment(grid, r - 1, contained_start_col, contained_end_col, flanker_color):
                    continue # Cells above C are not all F

                # --- Pattern Confirmed ---
                pattern_found = True

                # 7. Determine placement rule and apply
                contained_touches_flankers = (contained_start_col == c_left + 1 and contained_end_col == c_right - 1)

                if contained_touches_flankers:
                    # Rule Type 1: Add C at (r-2, c_left) and (r-2, c_right)
                    if r - 2 >= 0:
                        if 0 <= c_left < cols:
                             output_grid[r - 2, c_left] = contained_color
                        if 0 <= c_right < cols:
                             output_grid[r - 2, c_right] = contained_color
                else:
                    # Rule Type 2: Add C at (r-3, c_left), (r-3, c_right), (r-2, c_left+1), (r-2, c_right-1)
                    if r - 3 >= 0:
                        if 0 <= c_left < cols:
                            output_grid[r - 3, c_left] = contained_color
                        if 0 <= c_right < cols:
                            output_grid[r - 3, c_right] = contained_color
                    if r - 2 >= 0:
                        if 0 <= c_left + 1 < cols:
                            output_grid[r - 2, c_left + 1] = contained_color
                        if 0 <= c_right - 1 < cols:
                             output_grid[r - 2, c_right - 1] = contained_color

                # Assuming only one pattern instance needs to be processed per grid
                break # Exit inner loop once pattern is found and applied
        if pattern_found:
            break # Exit outer loop once pattern is found and applied


    # Convert back to list of lists for the final output
    return output_grid.tolist()

```
