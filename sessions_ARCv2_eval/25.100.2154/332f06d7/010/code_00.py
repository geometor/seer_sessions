import copy
import math

"""
Transforms an input grid based on the following rules:

Default Rule:
- Change all '0's to '1's.
- Change all '2's to '0's.
- '1's and '3's remain unchanged.

Exception Condition:
- Find the largest "valid" Monochromatic Square Block (MSB) for digit '0' (size N0).
- Find the largest "valid" MSB for digit '2' (size N2).
- A "valid" MSB must have size N >= 2 and be fully contained within the
  non-border area (i.e., all its cells (r, c) must satisfy 0 < r < rows-1
  and 0 < c < cols-1).
- The exception applies ONLY if N0 >= 2 AND N2 >= 2 AND N0 == N2.

Exception Actions:
- If the exception condition is met (let N = N0 = N2):
    1. Find all valid N x N MSBs of '1's.
    2. Select the target 1s block (L1_target) from these candidates based
       on the minimum Euclidean distance between its geometric center and the
       grid's geometric center. Ties are broken by choosing the block whose
       top-left corner appears first in reading order.
    3. Apply transformations cell by cell:
        a. If cell is in the largest valid 2-MSB (L2_MSB): output = 2.
        b. Else if cell is in the target 1-MSB (L1_target): output = 0.
        c. Else (covers largest valid 0-MSB and all others): Apply the
           Default Rule mapping to the input cell value (0->1, 2->0, 1->1, 3->3).

If the exception condition is NOT met, the Default Rule applies globally to all cells.
"""

def _is_within_border(r, c, rows, cols):
    """Checks if a coordinate is strictly within the border."""
    return r > 0 and r < rows - 1 and c > 0 and c < cols - 1

def _is_valid_msb(grid: list[list[int]], r: int, c: int, size: int, digit: int) -> bool:
    """
    Checks if an NxN block starting at (r, c) is a valid MSB of 'digit'.
    Valid means:
    1. All cells == digit.
    2. All cells are strictly within the non-border area (not row 0/max, col 0/max).
    """
    rows, cols = len(grid), len(grid[0])
    # Check bounds first
    if r + size > rows or c + size > cols:
        return False

    # Check cells for correct digit and position
    for i in range(r, r + size):
        for j in range(c, c + size):
            # Check if cell is strictly within border and has the correct digit
            if not _is_within_border(i, j, rows, cols) or grid[i][j] != digit:
                return False
    return True

def find_largest_valid_msb(grid: list[list[int]], digit: int) -> tuple[tuple[int, int] | None, int]:
    """
    Finds the largest valid MSB (size>=2, strictly within border) of a given digit.
    Returns the top-left coord and size (N). Prioritizes largest N,
    then first in reading order for ties. Returns (None, 0) if none found.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    max_size = 0
    best_coord = None

    # Iterate possible sizes from largest possible down to 2
    # Max possible size must fit within the inner grid dimensions
    max_possible_size = min(rows - 2, cols - 2) if rows > 2 and cols > 2 else 0
    for size in range(max_possible_size, 1, -1):
        found_at_this_size = False
        # Iterate through possible top-left corners (must start within inner grid)
        # Top-left corner must be at least (1,1) and allow the block to end before the border
        for r in range(1, rows - size):
            for c in range(1, cols - size):
                # We only need to check _is_valid_msb if the top-left is valid
                # But _is_valid_msb already checks full containment
                if _is_valid_msb(grid, r, c, size, digit):
                    # Found a valid MSB of the current size
                    if size > max_size:
                        max_size = size
                        best_coord = (r, c)
                        found_at_this_size = True
                        # Since we iterate size downwards, the first size we find
                        # a block for is the max size. We just need the first coord.
                        break # Found first block at this size
            if found_at_this_size:
                 break # Found first block for this size (which is max size found so far)
        if found_at_this_size:
             break # Break size loop if found max size

    # Ensure consistency: size is 0 if no block found
    if best_coord is None:
        max_size = 0

    return best_coord, max_size


def find_all_valid_msb_of_size(grid: list[list[int]], digit: int, size: int) -> list[tuple[int, int]]:
    """
    Finds all valid MSBs (size>=2, strictly within border) of a given digit and exact size.
    Returns a list of top-left coordinates in reading order.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    found_coords = []

    if size < 2 or size > min(rows - 2, cols - 2): # Check if size can fit inside border
        return []

    # Iterate through possible top-left corners (must start within inner grid)
    for r in range(1, rows - size):
        for c in range(1, cols - size):
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

        # Find the target 1s block (L1_target)
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

                # Update if strictly closer distance found
                # Tie-breaking (first in reading order) handled implicitly
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    best_candidate_coord = (r1, c1)

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
                    # else: 1s and 3s remain as copied initially from input_grid

    else:
        # --- Apply Default Transformations Globally ---
        # Apply default transformations globally if exception doesn't apply
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 0:
                    output_grid[r][c] = 1
                elif input_grid[r][c] == 2:
                    output_grid[r][c] = 0
                # else: 1s and 3s remain as copied initially from input_grid

    return output_grid