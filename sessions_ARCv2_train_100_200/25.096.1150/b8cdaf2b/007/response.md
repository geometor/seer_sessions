```python
import numpy as np
import copy

"""
The transformation rule identifies a specific pattern in the lowest non-zero row ('r') of the input grid and adds new colored cells based on this pattern. The original cells are preserved.

1. Find the bottom-most row 'r' containing any non-zero values. If r is 0 or no non-zero row exists, the grid remains unchanged.
2. Identify all unique non-zero colors present in row 'r'. Iterate through these colors as potential flanker colors 'F'.
3. For the *first* color 'F' encountered in this iteration that allows the formation of a valid pattern (detailed below), proceed to step 4. If no color 'F' leads to a valid pattern, return the original grid copy.
    a. Find the minimum column index 'c_left' and the maximum column index 'c_right' such that input_grid[r, c_left] == F and input_grid[r, c_right] == F. If 'c_left >= c_right - 1', this 'F' cannot form a valid pattern with sufficient space between flankers.
    b. Search for the *first* contiguous horizontal segment of a single non-zero color 'C' (where C != F) located strictly between 'c_left' and 'c_right' (i.e., in columns 'c_left + 1' to 'c_right - 1'). Let this segment span columns 'c_start' to 'c_end'. If no such segment 'C' is found, this 'F' cannot form a valid pattern.
    c. Verify that all cells in row 'r' between 'c_left' and 'c_start' (i.e., columns 'c_left + 1' to 'c_start - 1', if any) have the color 'F'. If not, this 'F' is invalid.
    d. Verify that all cells in row 'r' between 'c_end' and 'c_right' (i.e., columns 'c_end + 1' to 'c_right - 1', if any) have the color 'F'. If not, this 'F' is invalid.
    e. Verify that all cells in row 'r-1' directly above the contained segment 'C' (i.e., columns 'c_start' to 'c_end') have the color 'F'. If not, this 'F' is invalid.
    f. If all checks (a-e) pass, then this 'F' forms a valid pattern using the identified 'c_left', 'c_right', 'C', 'c_start', 'c_end'. Store these details.
4. Determine if the found contained segment 'C' touches both flankers 'F' based on the widest pair coordinates: 'touches_flankers = (c_start == c_left + 1 AND c_end == c_right - 1)'.
5. Apply the placement rule based on 'touches_flankers':
    a. If 'touches_flankers' is true (Rule Type 1):
        i. Set output_grid[r-2, c_left] = C (if r-2 >= 0 and c_left is within bounds).
        ii. Set output_grid[r-2, c_right] = C (if r-2 >= 0 and c_right is within bounds).
    b. If 'touches_flankers' is false (Rule Type 2):
        i. Set output_grid[r-3, c_left] = C (if r-3 >= 0 and c_left is within bounds).
        ii. Set output_grid[r-3, c_right] = C (if r-3 >= 0 and c_right is within bounds).
        iii. Set output_grid[r-2, c_left + 1] = C (if r-2 >= 0 and c_left + 1 is within bounds).
        iv. Set output_grid[r-2, c_right - 1] = C (if r-2 >= 0 and c_right - 1 is within bounds).
6. Return the modified output_grid.
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

def find_widest_flanker_pair(grid_row: np.ndarray, flanker_color: int) -> tuple[int, int]:
    """Finds the min and max column indices for a given flanker color."""
    indices = np.where(grid_row == flanker_color)[0]
    if len(indices) >= 2:
        return indices[0], indices[-1]
    else:
        return -1, -1 # Not enough flankers found

def find_first_contained_segment(grid_row: np.ndarray, c_left: int, c_right: int, flanker_color: int) -> tuple[int, int, int]:
    """Finds the first contiguous segment of a color different from flanker_color between c_left and c_right."""
    for c in range(c_left + 1, c_right):
        cell_color = grid_row[c]
        if cell_color != 0 and cell_color != flanker_color:
            # Found the start of a potential C segment
            contained_color = cell_color
            c_start = c
            c_end = c
            # Extend the segment to find its end
            for c_extend in range(c + 1, c_right):
                if grid_row[c_extend] == contained_color:
                    c_end = c_extend
                else:
                    break # End of contiguous C segment found
            return contained_color, c_start, c_end # Return first found segment
    return -1, -1, -1 # No contained segment found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Find the lowest non-zero row 'r'
    r = find_lowest_non_zero_row(grid)

    # Pattern requires checks in r-1, so r must be at least 1.
    if r <= 0:
        return output_grid.tolist() # Return the original grid copy

    # 2. Identify potential flanker colors and iterate
    row_r = grid[r]
    potential_flanker_colors = np.unique(row_r[row_r != 0])
    
    found_pattern = None

    for F in potential_flanker_colors:
        # 3a. Find widest flanker pair for this color F
        c_left, c_right = find_widest_flanker_pair(row_r, F)

        # Need at least one cell between the widest flankers
        if c_left == -1 or c_left >= c_right - 1:
            continue # This color F cannot form a valid wide pair

        # 3b. Find the first contained segment C between the widest flankers
        C, c_start, c_end = find_first_contained_segment(row_r, c_left, c_right, F)

        if C == -1:
            continue # No contained segment C found for this F

        # 3c. Verify intermediate F's before C
        if not check_row_segment(grid, r, c_left + 1, c_start - 1, F):
            continue # Failed check

        # 3d. Verify intermediate F's after C
        if not check_row_segment(grid, r, c_end + 1, c_right - 1, F):
            continue # Failed check

        # 3e. Verify F's in row r-1 above C
        if not check_row_segment(grid, r - 1, c_start, c_end, F):
            continue # Failed check

        # --- Pattern Confirmed for this F ---
        # Store details and break the loop (process only the first valid F found)
        found_pattern = {
            "F": F, "C": C, "r": r,
            "c_left": c_left, "c_right": c_right,
            "c_start": c_start, "c_end": c_end
        }
        break

    # 4, 5. If a valid pattern was found, apply placement rules
    if found_pattern:
        # Extract pattern details
        C = found_pattern["C"]
        r = found_pattern["r"]
        c_left = found_pattern["c_left"]
        c_right = found_pattern["c_right"]
        c_start = found_pattern["c_start"]
        c_end = found_pattern["c_end"]

        # Determine if C touches the *widest* flankers
        touches_flankers = (c_start == c_left + 1 and c_end == c_right - 1)

        # Apply Rule Type 1 or 2 based on whether C touches the flankers
        if touches_flankers:
            # Rule Type 1: Add C at (r-2, c_left) and (r-2, c_right)
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
                if 0 <= c_right - 1 < cols: # Check both bounds for c_right-1
                     output_grid[r - 2, c_right - 1] = C

    # 6. Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```