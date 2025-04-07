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