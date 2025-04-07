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