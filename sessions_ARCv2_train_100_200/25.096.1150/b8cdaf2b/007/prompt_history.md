
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
```python
import numpy as np
import copy

"""
The transformation rule identifies a specific pattern in the lowest non-zero row ('r') of the input grid and adds new elements based on this pattern.

1. Find the bottom-most row 'r' containing any non-zero values. If r is 0 or non-existent, return the input grid unchanged.
2. In row 'r', search for a pattern consisting of two identical non-zero "flanker" cells (color F) at columns c_left and c_right (c_left < c_right - 1).
3. Between these flankers, identify the first contiguous segment of a *different* non-zero color 'C' (from column c_start to c_end).
4. Verify structural integrity:
    a. All cells in row 'r' between the left flanker and the start of the contained segment (columns c_left + 1 to c_start - 1, if any) must have color F.
    b. All cells in row 'r' between the end of the contained segment and the right flanker (columns c_end + 1 to c_right - 1, if any) must have color F.
    c. All cells in the row directly above the contained segment (row r-1, columns c_start to c_end) must have color F.
5. If such a valid pattern is found:
    a. Rule Type 1: If the contained segment 'C' directly touches both flankers (i.e., c_start == c_left + 1 and c_end == c_right - 1), add two new cells of color C at positions (r-2, c_left) and (r-2, c_right), checking grid boundaries.
    b. Rule Type 2: Otherwise (if there are intermediate F cells between flankers and the contained segment in row r), add four new cells of color C at positions (r-3, c_left), (r-3, c_right), (r-2, c_left + 1), and (r-2, c_right - 1), checking grid boundaries.
6. The original input grid cells remain unchanged. Add the new cells to a copy of the input grid.
7. Stop searching after finding and applying the first valid pattern.
8. Return the modified grid. If no pattern is found, return the original grid copy.
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
    # If the segment is empty (c_start > c_end), it's vacuously true.
    if c_start > c_end:
        return True
        
    rows, cols = grid.shape
    # Check row bounds first
    if r < 0 or r >= rows:
        return False 
    # Check column bounds
    if c_start < 0 or c_end >= cols:
        return False

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
    # Pattern requires checks in r-1, r-2, r-3 potentially, so r must be >= 1 (at least).
    # Rule Type 2 requires r >= 3. Rule Type 1 requires r >= 2.
    # Simplest check: if r <= 0, no pattern requiring r-1 check is possible.
    if r <= 0: 
        return output_grid.tolist()

    # 2. Search for the pattern in row 'r'
    pattern_found_and_applied = False
    for c_left in range(cols - 1):
        flanker_color = grid[r, c_left]
        # Flanker must be non-zero
        if flanker_color == 0:
            continue 

        # Look for the right flanker
        for c_right in range(c_left + 2, cols): # Need at least one cell between flankers
            if grid[r, c_right] == flanker_color:
                # Found potential flankers F at (r, c_left) and (r, c_right)

                # 3. Identify the *first* contiguous contained segment 'C' between flankers
                contained_start_col = -1
                contained_end_col = -1
                contained_color = -1
                segment_found = False

                for c in range(c_left + 1, c_right):
                    cell_color = grid[r, c]
                    if cell_color != 0 and cell_color != flanker_color:
                         # Found the start of a potential C segment
                         contained_color = cell_color
                         contained_start_col = c
                         contained_end_col = c
                         # Extend the segment
                         for c_extend in range(c + 1, c_right):
                              if grid[r, c_extend] == contained_color:
                                   contained_end_col = c_extend
                              else:
                                   break # End of contiguous C segment
                         segment_found = True
                         break # Found the first C segment, stop searching for C
                    elif cell_color == flanker_color:
                         continue # Still in potential leading F segment
                    elif cell_color == 0:
                        # If we encounter 0 before finding C, this pair won't work for this definition
                        # Or if 0 is within C segment (based on examples C seems solid non-zero)
                        # For simplicity, let's assume C must be solid non-zero.
                        # If 0 appears before C is found, break inner C search.
                        break 


                # If no valid C segment was found between these flankers, try next c_right
                if not segment_found:
                    continue

                # 4. Verify structural integrity
                # a. Check intermediate F's before C
                if not check_row_segment(grid, r, c_left + 1, contained_start_col - 1, flanker_color):
                    continue 
                # b. Check intermediate F's after C
                if not check_row_segment(grid, r, contained_end_col + 1, c_right - 1, flanker_color):
                    continue 
                # c. Check F's in row r-1 above C
                if not check_row_segment(grid, r - 1, contained_start_col, contained_end_col, flanker_color):
                    continue 

                # --- Pattern Confirmed ---

                # 5. Determine placement rule and apply
                contained_touches_flankers = (contained_start_col == c_left + 1 and contained_end_col == c_right - 1)

                if contained_touches_flankers:
                    # Rule Type 1: Add C at (r-2, c_left) and (r-2, c_right)
                    # Check bounds before assignment
                    if r - 2 >= 0:
                        if 0 <= c_left < cols:
                             output_grid[r - 2, c_left] = contained_color
                        if 0 <= c_right < cols:
                             output_grid[r - 2, c_right] = contained_color
                else:
                    # Rule Type 2: Add C at (r-3, c_left), (r-3, c_right), (r-2, c_left+1), (r-2, c_right-1)
                    # Check bounds before assignment
                    if r - 3 >= 0:
                        if 0 <= c_left < cols:
                            output_grid[r - 3, c_left] = contained_color
                        if 0 <= c_right < cols:
                            output_grid[r - 3, c_right] = contained_color
                    if r - 2 >= 0:
                        if 0 <= c_left + 1 < cols:
                            output_grid[r - 2, c_left + 1] = contained_color
                        if 0 <= c_right - 1 < cols: # Ensure c_right-1 is also >= 0 implicitly
                             output_grid[r - 2, c_right - 1] = contained_color

                # 7. Stop searching after finding and applying the first valid pattern.
                pattern_found_and_applied = True
                break # Exit inner loop (c_right) once pattern is found and applied

        if pattern_found_and_applied:
            break # Exit outer loop (c_left) once pattern is found and applied


    # Convert back to list of lists for the final output
    return output_grid.tolist()
```
```python
import numpy as np
import copy

"""
The transformation rule identifies a specific pattern in the lowest non-zero row ('r') of the input grid and adds new colored cells based on this pattern. The original cells are preserved.

1. Find the bottom-most row 'r' containing any non-zero values. If r is 0 or no non-zero row exists, the grid remains unchanged.
2. Search row 'r' for the first occurrence (scanning left-to-right for the left boundary, then the right boundary) of a specific pattern:
    a. Two identical non-zero "flanker" cells (color F) at columns c_left and c_right (c_left < c_right - 1).
    b. Between these flankers (columns c_left + 1 to c_right - 1), the *first* contiguous horizontal segment of a single *different* non-zero color 'C' (C != F). Let this segment span columns c_start to c_end.
    c. Structural Validity Checks:
        i. All cells in row 'r' from column c_left + 1 to c_start - 1 (if any) must have color F.
        ii. All cells in row 'r' from column c_end + 1 to c_right - 1 (if any) must have color F.
        iii. All cells in row 'r-1' from column c_start to c_end must have color F.
3. If a valid pattern instance is found:
    a. Determine if the contained segment 'C' directly touches both flankers (i.e., c_start == c_left + 1 AND c_end == c_right - 1).
    b. Apply Placement Rule:
        i. If 'C' touches both flankers (Rule Type 1): Add color C at (r-2, c_left) and (r-2, c_right), checking grid boundaries.
        ii. Otherwise (Rule Type 2): Add color C at (r-3, c_left), (r-3, c_right), (r-2, c_left + 1), and (r-2, c_right - 1), checking grid boundaries.
4. The search stops after the first valid pattern is found and applied.
5. Return the modified grid.
"""

def find_lowest_non_zero_row(grid: np.ndarray) -> int:
    """Finds the index of the lowest row containing at least one non-zero value."""
    rows, _ = grid.shape
    for r in range(rows - 1, -1, -1):
        if np.any(grid[r, :] != 0):
            return r
    return -1 # No non-zero row found

def check_row_segment(grid: np.ndarray, r: int, c_start: int, c_end: int, expected_color: int) -> bool:
    """Checks if all cells in a horizontal segment have the expected color, handling boundaries."""
    # If the segment is empty (c_start > c_end), it's vacuously true.
    if c_start > c_end:
        return True

    rows, cols = grid.shape
    # Check row bounds first
    if r < 0 or r >= rows:
        return False
    # Check column bounds - ensure the entire segment is within grid limits
    if c_start < 0 or c_end >= cols:
        return False

    return np.all(grid[r, c_start:c_end+1] == expected_color)

def find_pattern_in_row(grid: np.ndarray, r: int):
    """
    Searches for the first valid F-C-F pattern in the specified row 'r'.
    Returns a dictionary with pattern details if found, otherwise None.
    """
    rows, cols = grid.shape

    # Iterate through potential left flanker columns
    for c_left in range(cols - 1):
        flanker_color = grid[r, c_left]
        # Flanker must be non-zero
        if flanker_color == 0:
            continue

        # Iterate through potential right flanker columns
        for c_right in range(c_left + 2, cols): # Need at least one cell between flankers
            if grid[r, c_right] == flanker_color:
                # Found potential flankers F at (r, c_left) and (r, c_right)

                # Identify the *first* contiguous contained segment 'C' between flankers
                contained_start_col = -1
                contained_end_col = -1
                contained_color = -1
                segment_found = False

                # Scan between flankers for the start of the C segment
                for c in range(c_left + 1, c_right):
                    cell_color = grid[r, c]
                    if cell_color != 0 and cell_color != flanker_color:
                         # Found the start of a potential C segment
                         contained_color = cell_color
                         contained_start_col = c
                         contained_end_col = c
                         # Extend the segment to find its end
                         for c_extend in range(c + 1, c_right):
                              if grid[r, c_extend] == contained_color:
                                   contained_end_col = c_extend
                              else:
                                   break # End of contiguous C segment found
                         segment_found = True
                         break # Found the first C segment, stop searching for C within this F-F pair
                    elif cell_color == flanker_color:
                         continue # Still in potential leading F segment
                    elif cell_color == 0:
                        # Encountering a 0 before finding C breaks the required structure for this F-F pair based on examples
                        break # Stop searching for C within this F-F pair


                # If no valid C segment was found between *these* flankers, continue to the next c_right
                if not segment_found:
                    continue

                # Verify structural integrity
                # a. Check intermediate F's before C
                if not check_row_segment(grid, r, c_left + 1, contained_start_col - 1, flanker_color):
                    continue # Failed check, try next c_right
                # b. Check intermediate F's after C
                if not check_row_segment(grid, r, contained_end_col + 1, c_right - 1, flanker_color):
                    continue # Failed check, try next c_right
                # c. Check F's in row r-1 above C (Row r-1 must exist)
                if r == 0 or not check_row_segment(grid, r - 1, contained_start_col, contained_end_col, flanker_color):
                    continue # Failed check, try next c_right

                # --- Pattern Confirmed ---
                # Determine if C touches flankers
                touches_flankers = (contained_start_col == c_left + 1 and contained_end_col == c_right - 1)

                # Return details of the first valid pattern found
                return {
                    "flanker_color": flanker_color,
                    "contained_color": contained_color,
                    "r": r,
                    "c_left": c_left,
                    "c_right": c_right,
                    "c_start": contained_start_col,
                    "c_end": contained_end_col,
                    "touches_flankers": touches_flankers
                }
    # No valid pattern found in the row
    return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Find the lowest non-zero row 'r'
    r = find_lowest_non_zero_row(grid)

    # Pattern requires checks in r-1, so r must be at least 1.
    # If r <= 0, no valid pattern possible.
    if r <= 0:
        return output_grid.tolist() # Return the original grid copy

    # 2. Search for the first valid pattern instance in row 'r'
    pattern = find_pattern_in_row(grid, r)

    # 3. If a valid pattern was found, apply placement rules
    if pattern:
        # Extract pattern details
        C = pattern["contained_color"]
        r = pattern["r"]
        c_left = pattern["c_left"]
        c_right = pattern["c_right"]
        touches_flankers = pattern["touches_flankers"]

        # Apply Rule Type 1 or 2 based on whether C touches the flankers
        if touches_flankers:
            # Rule Type 1: Add C at (r-2, c_left) and (r-2, c_right)
            # Check bounds before assignment
            if r - 2 >= 0:
                if 0 <= c_left < cols:
                     output_grid[r - 2, c_left] = C
                if 0 <= c_right < cols:
                     output_grid[r - 2, c_right] = C
        else:
            # Rule Type 2: Add C at (r-3, c_left), (r-3, c_right), (r-2, c_left+1), (r-2, c_right-1)
            # Check bounds before assignment for row r-3
            if r - 3 >= 0:
                if 0 <= c_left < cols:
                    output_grid[r - 3, c_left] = C
                if 0 <= c_right < cols:
                    output_grid[r - 3, c_right] = C
            # Check bounds before assignment for row r-2
            if r - 2 >= 0:
                if 0 <= c_left + 1 < cols:
                    output_grid[r - 2, c_left + 1] = C
                # Ensure c_right - 1 is also a valid column index
                if 0 <= c_right - 1 < cols:
                     output_grid[r - 2, c_right - 1] = C

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
import copy

"""
The transformation rule identifies a specific pattern in the lowest non-zero row ('r') of the input grid and adds new colored cells based on this pattern. The original cells are preserved.

1. Find the bottom-most row 'r' containing any non-zero values. If r is 0 or no non-zero row exists, the grid remains unchanged.
2. Search row 'r' for the first occurrence (scanning left-to-right for the left boundary, then the right boundary) of a specific pattern:
    a. Two identical non-zero "flanker" cells (color F) at columns c_left and c_right (c_left < c_right - 1).
    b. Between these flankers (columns c_left + 1 to c_right - 1), the *first* contiguous horizontal segment of a single *different* non-zero color 'C' (C != F). Let this segment span columns c_start to c_end.
    c. Structural Validity Checks:
        i. All cells in row 'r' from column c_left + 1 to c_start - 1 (if any) must have color F.
        ii. All cells in row 'r' from column c_end + 1 to c_right - 1 (if any) must have color F.
        iii. All cells in row 'r-1' from column c_start to c_end must have color F.
3. If a valid pattern instance is found:
    a. Determine if the contained segment 'C' directly touches both flankers (i.e., c_start == c_left + 1 AND c_end == c_right - 1).
    b. Apply Placement Rule:
        i. If 'C' touches both flankers (Rule Type 1): Add color C at (r-2, c_left) and (r-2, c_right), checking grid boundaries.
        ii. Otherwise (Rule Type 2): Add color C at (r-3, c_left), (r-3, c_right), (r-2, c_left + 1), and (r-2, c_right - 1), checking grid boundaries.
4. The search stops after the first valid pattern is found and applied.
5. Return the modified grid.
"""

def find_lowest_non_zero_row(grid: np.ndarray) -> int:
    """Finds the index of the lowest row containing at least one non-zero value."""
    rows, _ = grid.shape
    for r in range(rows - 1, -1, -1):
        if np.any(grid[r, :] != 0):
            return r
    return -1 # No non-zero row found

def check_row_segment(grid: np.ndarray, r: int, c_start: int, c_end: int, expected_color: int) -> bool:
    """Checks if all cells in a horizontal segment have the expected color, handling boundaries."""
    # If the segment is empty (c_start > c_end), it's vacuously true.
    if c_start > c_end:
        return True

    rows, cols = grid.shape
    # Check row bounds first
    if r < 0 or r >= rows:
        return False
    # Check column bounds - ensure the entire segment is within grid limits
    if c_start < 0 or c_end >= cols:
        return False

    return np.all(grid[r, c_start:c_end+1] == expected_color)

def find_pattern_in_row(grid: np.ndarray, r: int):
    """
    Searches for the first valid F-C-F pattern in the specified row 'r'.
    Returns a dictionary with pattern details if found, otherwise None.
    """
    rows, cols = grid.shape

    # Iterate through potential left flanker columns
    for c_left in range(cols - 1):
        flanker_color = grid[r, c_left]
        # Flanker must be non-zero
        if flanker_color == 0:
            continue

        # Iterate through potential right flanker columns
        for c_right in range(c_left + 2, cols): # Need at least one cell between flankers
            if grid[r, c_right] == flanker_color:
                # Found potential flankers F at (r, c_left) and (r, c_right)

                # Identify the *first* contiguous contained segment 'C' between flankers
                contained_start_col = -1
                contained_end_col = -1
                contained_color = -1
                segment_found = False

                # Scan between flankers for the start of the C segment
                for c in range(c_left + 1, c_right):
                    cell_color = grid[r, c]
                    if cell_color != 0 and cell_color != flanker_color:
                         # Found the start of a potential C segment
                         contained_color = cell_color
                         contained_start_col = c
                         contained_end_col = c
                         # Extend the segment to find its end
                         for c_extend in range(c + 1, c_right):
                              if grid[r, c_extend] == contained_color:
                                   contained_end_col = c_extend
                              else:
                                   break # End of contiguous C segment found
                         segment_found = True
                         break # Found the first C segment, stop searching for C within this F-F pair
                    elif cell_color == flanker_color:
                         continue # Still in potential leading F segment
                    elif cell_color == 0:
                        # Encountering a 0 before finding C breaks the required structure for this F-F pair based on examples
                        break # Stop searching for C within this F-F pair


                # If no valid C segment was found between *these* flankers, continue to the next c_right
                if not segment_found:
                    continue

                # Verify structural integrity
                # a. Check intermediate F's before C
                if not check_row_segment(grid, r, c_left + 1, contained_start_col - 1, flanker_color):
                    continue # Failed check, try next c_right
                # b. Check intermediate F's after C
                if not check_row_segment(grid, r, contained_end_col + 1, c_right - 1, flanker_color):
                    continue # Failed check, try next c_right
                # c. Check F's in row r-1 above C (Row r-1 must exist)
                if r == 0 or not check_row_segment(grid, r - 1, contained_start_col, contained_end_col, flanker_color):
                    continue # Failed check, try next c_right

                # --- Pattern Confirmed ---
                # Determine if C touches flankers
                touches_flankers = (contained_start_col == c_left + 1 and contained_end_col == c_right - 1)

                # Return details of the first valid pattern found
                return {
                    "flanker_color": flanker_color,
                    "contained_color": contained_color,
                    "r": r,
                    "c_left": c_left,
                    "c_right": c_right,
                    "c_start": contained_start_col,
                    "c_end": contained_end_col,
                    "touches_flankers": touches_flankers
                }
    # No valid pattern found in the row
    return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Find the lowest non-zero row 'r'
    r = find_lowest_non_zero_row(grid)

    # Pattern requires checks in r-1, so r must be at least 1.
    # If r <= 0, no valid pattern possible.
    if r <= 0:
        return output_grid.tolist() # Return the original grid copy

    # 2. Search for the first valid pattern instance in row 'r'
    pattern = find_pattern_in_row(grid, r)

    # 3. If a valid pattern was found, apply placement rules
    if pattern:
        # Extract pattern details
        C = pattern["contained_color"]
        r = pattern["r"]
        c_left = pattern["c_left"]
        c_right = pattern["c_right"]
        touches_flankers = pattern["touches_flankers"]

        # Apply Rule Type 1 or 2 based on whether C touches the flankers
        if touches_flankers:
            # Rule Type 1: Add C at (r-2, c_left) and (r-2, c_right)
            # Check bounds before assignment
            if r - 2 >= 0:
                if 0 <= c_left < cols:
                     output_grid[r - 2, c_left] = C
                if 0 <= c_right < cols:
                     output_grid[r - 2, c_right] = C
        else:
            # Rule Type 2: Add C at (r-3, c_left), (r-3, c_right), (r-2, c_left+1), (r-2, c_right-1)
            # Check bounds before assignment for row r-3
            if r - 3 >= 0:
                if 0 <= c_left < cols:
                    output_grid[r - 3, c_left] = C
                if 0 <= c_right < cols:
                    output_grid[r - 3, c_right] = C
            # Check bounds before assignment for row r-2
            if r - 2 >= 0:
                if 0 <= c_left + 1 < cols:
                    output_grid[r - 2, c_left + 1] = C
                # Ensure c_right - 1 is also a valid column index
                if 0 <= c_right - 1 < cols:
                     output_grid[r - 2, c_right - 1] = C

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```
Expected Output:
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```
Transformed Output:
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```
Expected Output:
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```
Transformed Output:
```
0 0 0 0 0
3 0 0 3 0
0 3 3 0 0
0 0 8 0 0
8 8 3 8 8
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 16.0

## Example 3:
Input:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```
Expected Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```
Transformed Output:
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 4 0
0 4 0 0 4 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 8.16326530612244

## Example 4:
Input:
```
0 0 0
0 2 0
2 4 2
```
Expected Output:
```
4 0 4
0 2 0
2 4 2
```
Transformed Output:
```
4 0 4
0 2 0
2 4 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
**General Assessment and Strategy**

The initial code correctly identifies and processes the pattern in Examples 1 and 4, where the "contained" element (C) directly touches the "flanker" elements (F) in the lowest non-zero row (`r`). However, it fails on Examples 2 and 3, which represent the second pattern type where intermediate F cells exist between the flankers and the contained C segment in row `r`.

The failure analysis indicates that the code incorrectly identifies the `c_right` flanker boundary in Examples 2 and 3. Instead of using the outermost matching flanker (e.g., column 4 in Ex 2, column 6 in Ex 3), it stops at the first `c_right` that completes *a* valid pattern structure with the current `c_left` (column 3 in Ex 2, column 5 in Ex 3). This leads to incorrect placement coordinates for Rule Type 2.

**Strategy:**

1.  Refine the pattern identification logic within `find_pattern_in_row`. Instead of iterating `c_right` and stopping at the first match, the logic should identify the *widest* possible pair `(c_left, c_right)` for a given flanker color `F` in row `r`.
2.  Once the widest potential `(c_left, c_right)` pair for *a* specific color `F` is identified, the checks for the contained segment `C` and the structural validity (intermediate F's in row `r`, F's in row `r-1` above `C`) should be performed relative to this widest pair.
3.  The search should likely prioritize finding the pattern based on the overall structure in row `r`, potentially finding the widest pair for *each* candidate flanker color `F` present in the row and selecting the first one that satisfies all conditions.

**Metrics**


*code_execution:*
```python
import numpy as np

def calculate_metrics(input_grid, expected_output, actual_output):
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)
    actual_np = np.array(actual_output)

    metrics = {}
    metrics["input_shape"] = input_np.shape
    metrics["expected_output_shape"] = expected_np.shape
    metrics["actual_output_shape"] = actual_np.shape

    metrics["size_correct"] = (expected_np.shape == actual_np.shape)

    if metrics["size_correct"]:
        metrics["match"] = np.array_equal(expected_np, actual_np)
        metrics["pixels_off"] = np.sum(expected_np != actual_np)
    else:
        metrics["match"] = False
        metrics["pixels_off"] = expected_np.size # Or some other large penalty

    metrics["input_colors"] = sorted(list(np.unique(input_np)))
    metrics["expected_output_colors"] = sorted(list(np.unique(expected_np)))
    metrics["actual_output_colors"] = sorted(list(np.unique(actual_np)))
    metrics["color_palette_correct"] = (metrics["expected_output_colors"] == metrics["actual_output_colors"])

    expected_counts = dict(zip(*np.unique(expected_np, return_counts=True)))
    actual_counts = dict(zip(*np.unique(actual_np, return_counts=True)))
    metrics["color_count_correct"] = (expected_counts == actual_counts)

    metrics["score"] = metrics["pixels_off"] * 1.0 # Simple score based on diff

    # Analyze pattern specifics based on rules described
    metrics["analysis"] = {}
    r = -1
    rows, cols = input_np.shape
    for idx in range(rows - 1, -1, -1):
        if np.any(input_np[idx, :] != 0):
            r = idx
            break
    metrics["analysis"]["lowest_non_zero_row"] = r

    if r > 0:
      row_r = input_np[r]
      non_zero_indices = np.where(row_r != 0)[0]
      if len(non_zero_indices) >= 2:
          c_left = non_zero_indices[0]
          c_right = non_zero_indices[-1]
          flanker_color = row_r[c_left]
          # Simplistic check - assumes outermost non-zero are flankers
          if row_r[c_right] == flanker_color:
              metrics["analysis"]["potential_flanker_color"] = int(flanker_color)
              metrics["analysis"]["potential_c_left"] = int(c_left)
              metrics["analysis"]["potential_c_right"] = int(c_right)

              # Find first C segment
              c_start, c_end, contained_color = -1, -1, -1
              for c in range(c_left + 1, c_right):
                  if row_r[c] != 0 and row_r[c] != flanker_color:
                      contained_color = int(row_r[c])
                      c_start = c
                      c_end = c
                      for c_ext in range(c+1, c_right):
                          if row_r[c_ext] == contained_color:
                              c_end = c_ext
                          else: break
                      break
              metrics["analysis"]["potential_contained_color"] = contained_color
              metrics["analysis"]["potential_c_start"] = c_start
              metrics["analysis"]["potential_c_end"] = c_end

              if contained_color != -1:
                  touches = (c_start == c_left + 1 and c_end == c_right - 1)
                  metrics["analysis"]["rule_type_expected"] = 1 if touches else 2
              else:
                   metrics["analysis"]["rule_type_expected"] = "N/A (No C found)"


    return metrics


inputs = [
    [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,6,6,6,0],[6,1,1,1,6]],
    [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,8,0,0],[8,8,3,8,8]],
    [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,2,2,2,0,0],[2,2,4,4,4,2,2]],
    [[0,0,0],[0,2,0],[2,4,2]]
]

expected_outputs = [
    [[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,6,6,6,0],[6,1,1,1,6]],
    [[0,0,0,0,0],[3,0,0,0,3],[0,3,0,3,0],[0,0,8,0,0],[8,8,3,8,8]],
    [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[4,0,0,0,0,0,4],[0,4,0,0,0,4,0],[0,0,2,2,2,0,0],[2,2,4,4,4,2,2]],
    [[4,0,4],[0,2,0],[2,4,2]]
]

# Provided actual outputs from the execution report
actual_outputs = [
    [[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,6,6,6,0],[6,1,1,1,6]],
    [[0,0,0,0,0],[3,0,0,3,0],[0,3,3,0,0],[0,0,8,0,0],[8,8,3,8,8]], # Failed one
    [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[4,0,0,0,0,4,0],[0,4,0,0,4,0,0],[0,0,2,2,2,0,0],[2,2,4,4,4,2,2]], # Failed one
    [[4,0,4],[0,2,0],[2,4,2]]
]

results = []
for i in range(len(inputs)):
    print(f"--- Example {i+1} ---")
    metrics = calculate_metrics(inputs[i], expected_outputs[i], actual_outputs[i])
    results.append(metrics)
    for key, value in metrics.items():
        if key != "analysis":
           print(f"{key}: {value}")
    print("Analysis:")
    if "analysis" in metrics:
        for a_key, a_value in metrics["analysis"].items():
             print(f"  {a_key}: {a_value}")


```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 ---
input_shape: (5, 5)
expected_output_shape: (5, 5)
actual_output_shape: (5, 5)
size_correct: True
match: True
pixels_off: 0
input_colors: [np.int64(0), np.int64(1), np.int64(6)]
expected_output_colors: [np.int64(0), np.int64(1), np.int64(6)]
actual_output_colors: [np.int64(0), np.int64(1), np.int64(6)]
color_palette_correct: True
color_count_correct: True
score: 0.0
Analysis:
  lowest_non_zero_row: 4
  potential_flanker_color: 6
  potential_c_left: 0
  potential_c_right: 4
  potential_contained_color: 1
  potential_c_start: 1
  potential_c_end: 3
  rule_type_expected: 1
--- Example 2 ---
input_shape: (5, 5)
expected_output_shape: (5, 5)
actual_output_shape: (5, 5)
size_correct: True
match: False
pixels_off: 4
input_colors: [np.int64(0), np.int64(3), np.int64(8)]
expected_output_colors: [np.int64(0), np.int64(3), np.int64(8)]
actual_output_colors: [np.int64(0), np.int64(3), np.int64(8)]
color_palette_correct: True
color_count_correct: True
score: 4.0
Analysis:
  lowest_non_zero_row: 4
  potential_flanker_color: 8
  potential_c_left: 0
  potential_c_right: 4
  potential_contained_color: 3
  potential_c_start: 2
  potential_c_end: 2
  rule_type_expected: 2
--- Example 3 ---
input_shape: (7, 7)
expected_output_shape: (7, 7)
actual_output_shape: (7, 7)
size_correct: True
match: False
pixels_off: 4
input_colors: [np.int64(0), np.int64(2), np.int64(4)]
expected_output_colors: [np.int64(0), np.int64(2), np.int64(4)]
actual_output_colors: [np.int64(0), np.int64(2), np.int64(4)]
color_palette_correct: True
color_count_correct: True
score: 4.0
Analysis:
  lowest_non_zero_row: 6
  potential_flanker_color: 2
  potential_c_left: 0
  potential_c_right: 6
  potential_contained_color: 4
  potential_c_start: 2
  potential_c_end: 4
  rule_type_expected: 2
--- Example 4 ---
input_shape: (3, 3)
expected_output_shape: (3, 3)
actual_output_shape: (3, 3)
size_correct: True
match: True
pixels_off: 0
input_colors: [np.int64(0), np.int64(2), np.int64(4)]
expected_output_colors: [np.int64(0), np.int64(2), np.int64(4)]
actual_output_colors: [np.int64(0), np.int64(2), np.int64(4)]
color_palette_correct: True
color_count_correct: True
score: 0.0
Analysis:
  lowest_non_zero_row: 2
  potential_flanker_color: 2
  potential_c_left: 0
  potential_c_right: 2
  potential_contained_color: 4
  potential_c_start: 1
  potential_c_end: 1
  rule_type_expected: 1

```
**YAML Facts**


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
        - lowest_row_index: r (must be > 0 for pattern to be possible)
        - flanker_color: F (non-zero)
        # Widest pair of F in row r defines boundaries
        - flanker_left_col: c_left (minimum column index where grid[r, col] == F)
        - flanker_right_col: c_right (maximum column index where grid[r, col] == F)
        # First C segment found between *widest* flankers
        - contained_color: C (C != F, C != 0)
        - contained_start_col: c_start
        - contained_end_col: c_end
        - structure_valid: boolean # Aggregates checks below
        - check_intermediate_left: boolean (cells grid[r, c_left+1 : c_start] must all be F)
        - check_intermediate_right: boolean (cells grid[r, c_end+1 : c_right] must all be F)
        - check_above_contained: boolean (cells grid[r-1, c_start : c_end+1] must all be F)
        - contained_touches_flankers: boolean (c_start == c_left + 1 AND c_end == c_right - 1) # Based on widest flankers

Relationships:
  - spatial: [above, below, left_of, right_of, between, adjacent_to, contained_within]
  - value: [equal_color, different_color, non_zero]

Actions:
  - Find Lowest Non-Zero Row: Identify index 'r'.
  - Find Widest Flanker Pair: For a color F in row r, find min(c) and max(c) where grid[r,c]==F.
  - Scan Segment: Iterate through cells in a horizontal segment.
  - Identify Contained Segment: Find the first contiguous non-zero segment with color != F between flankers.
  - Validate Structure: Perform the three checks (intermediate left, intermediate right, above contained).
  - Copy Grid: Duplicate input to create initial output.
  - Place Elements: Modify output grid by setting cell colors based on pattern type and coordinates (c_left, c_right, C).

Placement Rules:
  - Rule_Type_1 (if contained_touches_flankers is true):
      - Add color C at (r-2, c_left)
      - Add color C at (r-2, c_right)
      - Constraints: Placement occurs only if target rows/columns are within grid bounds.
  - Rule_Type_2 (if contained_touches_flankers is false):
      - Add color C at (r-3, c_left)
      - Add color C at (r-3, c_right)
      - Add color C at (r-2, c_left + 1)
      - Add color C at (r-2, c_right - 1)
      - Constraints: Placement occurs only if target rows/columns are within grid bounds.
```


**Natural Language Program**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Find the index `r` of the bottom-most row in the `input_grid` that contains at least one non-zero value. If `r` is 0 or no such row exists, return the `output_grid` unchanged.
3.  Identify all unique non-zero colors present in row `r`. Iterate through these colors as potential flanker colors `F`.
4.  For the *first* color `F` encountered in this iteration that allows the formation of a valid pattern (detailed below), proceed to step 5. If no color `F` leads to a valid pattern, return the `output_grid` unchanged.
    *   To check if `F` forms a valid pattern:
        a.  Find the minimum column index `c_left` and the maximum column index `c_right` such that `input_grid[r, c_left] == F` and `input_grid[r, c_right] == F`. If `c_left >= c_right - 1`, this `F` cannot form a valid pattern.
        b.  Search for the *first* contiguous horizontal segment of a single non-zero color `C` (where `C != F`) located strictly between `c_left` and `c_right` (i.e., in columns `c_left + 1` to `c_right - 1`). Let this segment span columns `c_start` to `c_end`. If no such segment `C` is found, this `F` cannot form a valid pattern.
        c.  Verify that all cells in row `r` between `c_left` and `c_start` (i.e., columns `c_left + 1` to `c_start - 1`, if `c_start > c_left + 1`) have the color `F`. If not, this `F` is invalid.
        d.  Verify that all cells in row `r` between `c_end` and `c_right` (i.e., columns `c_end + 1` to `c_right - 1`, if `c_end < c_right - 1`) have the color `F`. If not, this `F` is invalid.
        e.  Verify that all cells in row `r-1` directly above the contained segment `C` (i.e., columns `c_start` to `c_end`) have the color `F`. If not, this `F` is invalid.
        f.  If all checks (a-e) pass, then this `F` forms a valid pattern using the identified `c_left`, `c_right`, `C`, `c_start`, `c_end`. Store these details.
5.  Determine if the found contained segment `C` touches both flankers `F` based on the widest pair coordinates: `touches_flankers = (c_start == c_left + 1 AND c_end == c_right - 1)`.
6.  Apply the placement rule based on `touches_flankers`:
    *   If `touches_flankers` is true (Rule Type 1):
        *   Set `output_grid[r-2, c_left] = C` (if `r-2 >= 0` and `c_left` is within bounds).
        *   Set `output_grid[r-2, c_right] = C` (if `r-2 >= 0` and `c_right` is within bounds).
    *   If `touches_flankers` is false (Rule Type 2):
        *   Set `output_grid[r-3, c_left] = C` (if `r-3 >= 0` and `c_left` is within bounds).
        *   Set `output_grid[r-3, c_right] = C` (if `r-3 >= 0` and `c_right` is within bounds).
        *   Set `output_grid[r-2, c_left + 1] = C` (if `r-2 >= 0` and `c_left + 1` is within bounds).
        *   Set `output_grid[r-2, c_right - 1] = C` (if `r-2 >= 0` and `c_right - 1` is within bounds).
7.  Return the modified `output_grid`.
