
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
- This rule applies ONLY if the largest MSB of '0's (size N0 >= 2)
  and the largest MSB of '2's (size N2 >= 2), both located strictly
  within the non-border area (i.e., not containing any '3's),
  exist AND have the exact same size (N0 = N2 = N).

Exception Actions:
- If the exception condition is met:
    1. The '0's within the N x N 0-MSB change to '1's.
    2. The '2's within the N x N 2-MSB remain '2's (overriding default).
    3. Find all N x N MSBs of '1's within the non-border area. Select the
       one whose geometric center is closest to the grid's geometric center.
       The '1's in this target 1-MSB change to '0's (overriding default).
       (Tie-breaking: choose the first one found in reading order).
    4. All other digits *outside* these three specific MSBs follow the
       default rule (0->1, 2->0, 1->1, 3->3).

If the exception condition is NOT met, the Default Rule applies globally.
"""

def _is_valid_msb(grid: list[list[int]], r: int, c: int, size: int, digit: int) -> bool:
    """Checks if an NxN block starting at (r, c) is a valid MSB of 'digit' (contains no 3s)."""
    rows, cols = len(grid), len(grid[0])
    if r + size > rows or c + size > cols:
        return False # Out of bounds
    for i in range(r, r + size):
        for j in range(c, c + size):
            if grid[i][j] != digit or grid[i][j] == 3: # Check digit and ensure no border value 3
                return False
    return True

def find_largest_msb(grid: list[list[int]], digit: int) -> tuple[tuple[int, int] | None, int]:
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
        # Iterate through possible top-left corners
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                if _is_valid_msb(grid, r, c, size, digit):
                    # Found a valid MSB of the current size
                    if size > max_size:
                        max_size = size
                        best_coord = (r, c)
                        found_at_this_size = True
                        # Optimization: Since we go largest to smallest,
                        # the first one we find of this size IS the largest.
                        # For tie-breaking, we stop searching smaller sizes
                        # and ensure we keep the first coord found at this max size.
                        break # Found the largest size for this digit
                    # If size == max_size, we keep the first coord found (implicit)
            if found_at_this_size and size == max_size:
                 break # Break outer loop if we found the first largest
        if found_at_this_size and size == max_size:
             break # Break size loop as well

    return best_coord, max_size


def find_all_msb_of_size(grid: list[list[int]], digit: int, size: int) -> list[tuple[int, int]]:
    """
    Finds all valid MSBs (size>=2, no 3s) of a given digit and exact size.
    Returns a list of top-left coordinates in reading order.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    found_coords = []

    if size < 2:
        return []

    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if _is_valid_msb(grid, r, c, size, digit):
                found_coords.append((r, c))
    return found_coords


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Get grid dimensions
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0
    if rows == 0 or cols == 0:
        return []

    # Find the largest MSBs for 0 and 2
    coord0, N0 = find_largest_msb(input_grid, 0)
    coord2, N2 = find_largest_msb(input_grid, 2)

    # Initialize output grid
    output_grid = copy.deepcopy(input_grid)

    # Check if the exception condition is met
    exception_applies = (N0 >= 2 and N2 >= 2 and N0 == N2)

    if exception_applies:
        N = N0 # The common size
        # Find all candidate 1s-MSBs of size N
        l1_candidates_coords = find_all_msb_of_size(input_grid, 1, N)
        coord1_target = None

        if l1_candidates_coords:
            # Calculate grid center
            grid_center_r = (rows - 1) / 2.0
            grid_center_c = (cols - 1) / 2.0
            min_dist_sq = float('inf')

            # Find the candidate closest to the grid center
            for r1, c1 in l1_candidates_coords:
                block_center_r = r1 + N / 2.0 - 0.5
                block_center_c = c1 + N / 2.0 - 0.5
                dist_sq = (block_center_r - grid_center_r)**2 + (block_center_c - grid_center_c)**2
                
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    coord1_target = (r1, c1)
            # Tie-breaking is implicit: the first one checked with min_dist_sq is kept.

        # Apply transformations for the exception case
        for r in range(rows):
            for c in range(cols):
                # Check if cell is within the 2-MSB (coord2 is guaranteed not None here)
                is_in_L2_MSB = (r >= coord2[0] and r < coord2[0] + N and
                                c >= coord2[1] and c < coord2[1] + N)

                # Check if cell is within the target 1-MSB
                is_in_L1_target = (coord1_target is not None and
                                   r >= coord1_target[0] and r < coord1_target[0] + N and
                                   c >= coord1_target[1] and c < coord1_target[1] + N)

                if is_in_L2_MSB:
                    # Rule 2: 2s in the 2-MSB remain 2
                    output_grid[r][c] = 2
                elif is_in_L1_target:
                    # Rule 3: 1s in the target 1-MSB become 0
                    output_grid[r][c] = 0
                else:
                    # Apply default rules for all other cells
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
