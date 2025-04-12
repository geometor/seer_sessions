
Previous Code:
```python
import copy
import math

"""
Transforms an input grid based on monochromatic square blocks (MSBs).

Default Rule:
- Change all '0's to '1's.
- Change all '2's to '0's.
- '1's and '3's (typically borders) remain unchanged.

Exception Condition:
- This rule applies ONLY if the largest valid MSB of '0's (size N0 >= 2)
  and the largest valid MSB of '2's (size N2 >= 2) both exist AND have the
  exact same size (N0 = N2 = N). A 'valid' MSB is one that is >= 2x2
  and contains no cells with the value '3'.

Exception Actions:
- If the exception condition is met:
    1. Find all valid N x N MSBs of '1's.
    2. Select the target 1s block (L1_target) from these candidates based
       on the minimum Euclidean distance between its center and the grid's
       geometric center (tie-breaking by reading order).
    3. Apply rules cell by cell:
        a. If cell is in the largest valid 2-MSB (L2_MSB): output = 2.
        b. Else if cell is in the target 1-MSB (L1_target): output = 0.
        c. Else (covers largest valid 0-MSB and all others): Apply the
           Default Rule mapping to the input cell value (0->1, 2->0, 1->1, 3->3).

If the exception condition is NOT met, the Default Rule applies globally.
"""

def _is_valid_msb(grid: list[list[int]], r: int, c: int, size: int, digit: int) -> bool:
    """Checks if an NxN block starting at (r, c) is a valid MSB of 'digit'.
       Valid means all cells == digit and no cell == 3.
    """
    rows, cols = len(grid), len(grid[0])
    # Check bounds first
    if r + size > rows or c + size > cols:
        return False
    # Check cells
    for i in range(r, r + size):
        for j in range(c, c + size):
            # Check for incorrect digit or presence of border value '3'
            if grid[i][j] != digit or grid[i][j] == 3:
                return False
    return True

def find_largest_valid_msb(grid: list[list[int]], digit: int) -> tuple[tuple[int, int] | None, int]:
    """
    Finds the largest valid MSB (size>=2, no 3s) of a given digit.
    Returns the top-left coord and size (N). Prioritizes largest N,
    then first in reading order for ties. Returns (None, 0) if none found.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    max_size = 0
    best_coord = None

    # Iterate possible sizes from largest possible down to 2
    for size in range(min(rows, cols), 1, -1):
        found_at_this_size = False
        # Iterate through possible top-left corners in reading order
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                if _is_valid_msb(grid, r, c, size, digit):
                    # Found a valid MSB of the current size
                    if size > max_size:
                        max_size = size
                        best_coord = (r, c)
                        found_at_this_size = True
                        # Optimization: Since we search largest size first,
                        # the first one we find *is* the largest. We only need
                        # to complete the loops for (r,c) at this size to respect
                        # reading-order tie-breaking if needed later, but can
                        # break the outer size loop once this size is processed.
                        # Correction: We need the FIRST one found at the MAX size.
                        # So once we find one, we record it and continue checking
                        # this size row by row, col by col, but DON'T update if
                        # another of the same max size is found.
                        # Simpler: break inner loops and outer loop immediately
                        # once the first block of the current 'size' is found,
                        # because we iterate 'size' downwards.
                        break # Found first block at this size
            if found_at_this_size:
                 break # Found first block for the largest possible size
        if found_at_this_size:
             break # Break size loop if found

    # If we found a best_coord, ensure max_size > 0
    if best_coord is not None:
        max_size = max(2, max_size) # Ensure size is at least 2 if coord found
    else:
        max_size = 0 # Ensure size is 0 if no coord found

    return best_coord, max_size


def find_all_valid_msb_of_size(grid: list[list[int]], digit: int, size: int) -> list[tuple[int, int]]:
    """
    Finds all valid MSBs (size>=2, no 3s) of a given digit and exact size.
    Returns a list of top-left coordinates in reading order.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    found_coords = []

    if size < 2 or size > min(rows, cols):
        return []

    # Iterate through possible top-left corners in reading order
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if _is_valid_msb(grid, r, c, size, digit):
                found_coords.append((r, c))
    return found_coords


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return [] # Handle empty grid case

    # --- Check for Exception Condition ---
    # Find the largest valid MSBs for 0 and 2
    coord0, N0 = find_largest_valid_msb(input_grid, 0)
    coord2, N2 = find_largest_valid_msb(input_grid, 2)

    # Determine if the exception applies
    exception_applies = (N0 >= 2 and N2 >= 2 and N0 == N2)

    # --- Apply Transformations ---
    if exception_applies:
        N = N0 # The common size

        # Find the target 1s block
        coord1_target = None
        l1_candidates_coords = find_all_valid_msb_of_size(input_grid, 1, N)

        if l1_candidates_coords:
            # Calculate grid center
            grid_center_r = (rows - 1) / 2.0
            grid_center_c = (cols - 1) / 2.0
            min_dist_sq = float('inf')
            best_candidate_coord = None

            # Find the candidate closest to the grid center
            for r1, c1 in l1_candidates_coords:
                # Calculate block center
                block_center_r = r1 + N / 2.0 - 0.5
                block_center_c = c1 + N / 2.0 - 0.5
                # Calculate squared distance
                dist_sq = (block_center_r - grid_center_r)**2 + (block_center_c - grid_center_c)**2

                # Update if closer distance found
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    best_candidate_coord = (r1, c1)
                # Tie-breaking is implicit: first one encountered with min_dist_sq is kept

            coord1_target = best_candidate_coord

        # Apply transformations cell by cell for the exception case
        for r in range(rows):
            for c in range(cols):
                # Check if cell is within the L2_MSB (coord2 is guaranteed not None here)
                is_in_L2_MSB = (r >= coord2[0] and r < coord2[0] + N and
                                c >= coord2[1] and c < coord2[1] + N)

                # Check if cell is within the L1_target
                is_in_L1_target = (coord1_target is not None and
                                   r >= coord1_target[0] and r < coord1_target[0] + N and
                                   c >= coord1_target[1] and c < coord1_target[1] + N)

                if is_in_L2_MSB:
                    # Exception rule: 2s in L2_MSB remain 2
                    output_grid[r][c] = 2
                elif is_in_L1_target:
                    # Exception rule: 1s in L1_target become 0
                    output_grid[r][c] = 0
                else:
                    # Apply default rules for all other cells (including L0_MSB)
                    if input_grid[r][c] == 0:
                        output_grid[r][c] = 1
                    elif input_grid[r][c] == 2:
                        output_grid[r][c] = 0
                    # else: 1s and 3s remain as copied initially

    else:
        # Apply default transformations globally if exception doesn't apply
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 0:
                    output_grid[r][c] = 1
                elif input_grid[r][c] == 2:
                    output_grid[r][c] = 0
                # else: 1s and 3s remain as copied initially

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 2 2 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 0 0 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 2 2 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 0 0 3 1 1 1 3 3
3 1 1 3 0 0 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 22.22222222222223

## Example 2:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 0 0 3 3 3 3 3 3 3
3 3 3 3 3 0 0 1 1 1 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 4.081632653061234

## Example 3:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 4:
Input:
```
3 3 3 3 3 3 3 3 3 3
3 0 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 2 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
