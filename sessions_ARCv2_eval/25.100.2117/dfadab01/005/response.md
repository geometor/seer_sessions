```python
import numpy as np
from typing import List, Tuple, Set

"""
Transforms an input grid based on specific digit patterns and locations:

1.  Determine the dimensions (height H, width W) of the input grid.
2.  Initialize an output grid of dimensions HxW, filled with zeros.
3.  Create lists of locations for all '3's and '5's in the input grid. Initialize an empty set `used_threes_in_rectangle` to track '3's used in Rule 4.
4.  Apply Rule 4 (FiveThreeRectangle):
    a.  Iterate through all pairs of '5' locations to find potential horizontal top edges (r1, c1) and (r1, c2) where c1 < c2.
    b.  For each potential top edge, iterate through all pairs of '3' locations to find potential corresponding bottom edges (r2, c1) and (r2, c2) where r2 > r1.
    c.  If a valid rectangle is found (matching coordinates r1, r2, c1, c2):
        i.  Add the locations (r2, c1) and (r2, c2) to the `used_threes_in_rectangle` set.
        ii. Draw a 2x2 block of '6's in the output grid starting at (r1, c1).
        iii. Draw a 2x2 block of '6's in the output grid starting at (r1, c2).
        iv. Draw a 2x2 block of '6's in the output grid starting at (r2 - 3, c1).
        v.  Draw a 2x2 block of '6's in the output grid starting at (r2 - 3, c2).
        (Ensure drawing stays within grid boundaries).
5.  Apply Rule 1 (TwoMarker):
    a.  Iterate through every cell (r, c) of the input grid.
    b.  If the cell contains the digit '2', draw a 4x4 hollow square of '4's in the output grid, with the top-left corner at (r, c). (Ensure boundaries).
6.  Apply Rule 2 (SixBlock):
    a.  Iterate through potential top-left corners (r, c) such that r < H-1 and c < W-1.
    b.  Check if the 2x2 block starting at (r, c) in the input grid consists entirely of '6's.
    c.  If it does, draw a 2x2 block of '6's in the output grid starting at (r - 1, c - 1). (Ensure boundaries).
7.  Apply Rule 3 (OneSquare):
    a.  Iterate through potential top-left corners (r, c) such that r < H-3 and c < W-3.
    b.  Check if the 4x4 area starting at (r, c) in the input grid forms a hollow square of '1's (using the `is_hollow_square` helper function).
    c.  If it does, draw a 4x4 hollow square of '1's in the output grid, with the top-left corner at (r, c + 1). (Ensure boundaries).
8.  Apply Rule 5 (TriggerOneSquareFromThree):
    a.  Create a list `EligibleThrees` containing locations of all '3's from the initial list (step 3) that are *not* in the `used_threes_in_rectangle` set.
    b.  If `EligibleThrees` is not empty:
        i.  Search `EligibleThrees` for vertical pairs: locations (r_a, c) and (r_b, c) where r_a < r_b.
        ii. If vertical pairs exist: Find the pair where `r_b` is minimized. Set the trigger location to this (r_b, c).
        iii. If no vertical pairs exist: Sort `EligibleThrees` first by row index, then by column index. Set the trigger location to the first element (r_min, c_min).
        iv. If a trigger location (r_trigger, c_trigger) was determined, draw a 4x4 hollow square of '1's in the output grid, with the top-left corner at (r_trigger, c_trigger). (Ensure boundaries).
9.  Return the resulting output grid. (Note: The order of rule application determines final pixel values in case of overlap between non-zero digits from different rules).
"""


# Helper function to check grid boundaries
def _is_valid(r, c, height, width):
    """Checks if coordinates (r, c) are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

# Helper function to draw a filled block
def _draw_block(grid: np.ndarray, r: int, c: int, h: int, w: int, value: int):
    """Draws a solid h x w block with top-left at (r, c) using 'value'."""
    height, width = grid.shape
    for i in range(r, r + h):
        for j in range(c, c + w):
            if _is_valid(i, j, height, width):
                grid[i, j] = value

# Helper function to draw a hollow square
def _draw_hollow_square(grid: np.ndarray, r: int, c: int, size: int, value: int):
    """Draws a hollow square of 'size' x 'size' with top-left at (r, c) using 'value'."""
    height, width = grid.shape
    # Draw top and bottom edges
    for j in range(c, c + size):
        if _is_valid(r, j, height, width):
            grid[r, j] = value
        if _is_valid(r + size - 1, j, height, width):
            grid[r + size - 1, j] = value
    # Draw side edges (excluding corners already drawn)
    for i in range(r + 1, r + size - 1):
        if _is_valid(i, c, height, width):
            grid[i, c] = value
        if _is_valid(i, c + size - 1, height, width):
            grid[i, c + size - 1] = value

# Helper function to check for a specific block pattern
def _is_block(grid: np.ndarray, r: int, c: int, h: int, w: int, value: int) -> bool:
    """Checks if an h x w block of 'value' exists with top-left at (r, c)."""
    height, width = grid.shape
    if not (_is_valid(r, c, height, width) and _is_valid(r + h - 1, c + w - 1, height, width)):
        return False
    for i in range(r, r + h):
        for j in range(c, c + w):
            if grid[i, j] != value:
                return False
    return True

# Helper function to check for a hollow square pattern
def _is_hollow_square(grid: np.ndarray, r: int, c: int, size: int, value: int) -> bool:
    """Checks if a hollow 'size' x 'size' square of 'value' exists with top-left at (r, c)."""
    height, width = grid.shape
    if not (_is_valid(r, c, height, width) and _is_valid(r + size - 1, c + size - 1, height, width)):
        return False
        
    # Check perimeter
    for j in range(c, c + size): # Top and bottom edges
        if not _is_valid(r, j, height, width) or grid[r, j] != value: return False
        if not _is_valid(r+size-1, j, height, width) or grid[r+size-1, j] != value: return False
    for i in range(r + 1, r + size - 1): # Left and right edges
        if not _is_valid(i, c, height, width) or grid[i, c] != value: return False
        if not _is_valid(i, c+size-1, height, width) or grid[i, c+size-1] != value: return False
        
    # Check interior (must not be the 'value')
    for i in range(r + 1, r + size - 1):
        for j in range(c + 1, c + size - 1):
            # Need to check boundary before accessing grid[i,j]
            if not _is_valid(i, j, height, width): return False # Should not happen if outer boundary check passed, but safety first
            if grid[i, j] == value: # Interior cell must NOT match the perimeter value
                 return False
    return True


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    # Initialize output grid with zeros
    output_array = np.zeros_like(input_array)

    # --- Step 3: Find initial locations of '3's and '5's ---
    three_locations: List[Tuple[int, int]] = []
    five_locations: List[Tuple[int, int]] = []
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 3:
                three_locations.append((r, c))
            elif input_array[r, c] == 5:
                five_locations.append((r, c))
    
    used_threes_in_rectangle: Set[Tuple[int, int]] = set()

    # --- Step 4: Apply Rule 4 (FiveThreeRectangle -> Four 2x2 '6' blocks) ---
    # Iterate through pairs of '5's to find potential top edges
    for i in range(len(five_locations)):
        for j in range(i + 1, len(five_locations)):
            r1_1, c1_1 = five_locations[i]
            r1_2, c1_2 = five_locations[j]

            # Check if they form a horizontal top edge (same row)
            if r1_1 == r1_2:
                r1 = r1_1
                c1 = min(c1_1, c1_2)
                c2 = max(c1_1, c1_2)
                if c1 == c2: continue # Need distinct columns

                # Now look for pairs of '3's forming the bottom edge
                for k in range(len(three_locations)):
                    for l in range(k + 1, len(three_locations)):
                        r2_1, c2_1 = three_locations[k]
                        r2_2, c2_2 = three_locations[l]

                        # Check if they form the bottom edge corresponding to the top edge
                        if r2_1 == r2_2 and r2_1 > r1 and \
                           min(c2_1, c2_2) == c1 and max(c2_1, c2_2) == c2:
                            r2 = r2_1
                            # Found a FiveThreeRectangle!
                            p3_loc = three_locations[k] if three_locations[k][1] == c1 else three_locations[l]
                            p4_loc = three_locations[k] if three_locations[k][1] == c2 else three_locations[l]
                            
                            # Mark the '3's as used
                            used_threes_in_rectangle.add(p3_loc)
                            used_threes_in_rectangle.add(p4_loc)

                            # Draw the four 2x2 blocks of '6' (using CORRECTED r2-3 logic)
                            _draw_block(output_array, r1, c1, 2, 2, 6)
                            _draw_block(output_array, r1, c2, 2, 2, 6)
                            _draw_block(output_array, r2 - 3, c1, 2, 2, 6) # Corrected
                            _draw_block(output_array, r2 - 3, c2, 2, 2, 6) # Corrected

    # --- Step 5: Apply Rule 1 ('2' -> 4x4 hollow '4' square) ---
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 2:
                _draw_hollow_square(output_array, r, c, 4, 4)

    # --- Step 6: Apply Rule 2 (2x2 '6' block -> shifted 2x2 '6' block) ---
    for r in range(height - 1): # Check potential top-left corners
        for c in range(width - 1):
            if _is_block(input_array, r, c, 2, 2, 6):
                _draw_block(output_array, r - 1, c - 1, 2, 2, 6)

    # --- Step 7: Apply Rule 3 (4x4 hollow '1' square -> shifted 4x4 hollow '1' square) ---
    for r in range(height - 3): # Check potential top-left corners
        for c in range(width - 3):
             if _is_hollow_square(input_array, r, c, 4, 1):
                 _draw_hollow_square(output_array, r, c + 1, 4, 1)

    # --- Step 8: Apply Rule 5 (Conditional '3' -> 4x4 hollow '1' square) ---
    eligible_threes = [loc for loc in three_locations if loc not in used_threes_in_rectangle]
    trigger_location = None

    if eligible_threes:
        vertical_pairs = []
        # Find vertical pairs among eligible '3's
        eligible_threes.sort() # Sort by row, then col helps in deterministic selection
        eligible_set = set(eligible_threes) # For faster lookup
        
        min_rb = float('inf')
        best_pair = None

        for r_a, c_a in eligible_threes:
             # Check if there's a '3' directly below it within the eligible set
             potential_rb = r_a + 1
             while potential_rb < height:
                 lower_loc = (potential_rb, c_a)
                 if lower_loc in eligible_set:
                      # Found a vertical pair ((r_a, c_a), (potential_rb, c_a))
                      if potential_rb < min_rb:
                          min_rb = potential_rb
                          best_pair = ((r_a, c_a), lower_loc)
                      # Since we iterate through eligible_threes sorted by r_a,
                      # the first pair found for a given c_a starting from the lowest r_a
                      # guarantees finding the lowest r_b for that column. We just need the overall lowest r_b.
                      break # Move to next upper point
                 potential_rb += 1


        if best_pair:
            # Found vertical pairs, use the one with the minimum bottom row index (r_b)
            trigger_location = best_pair[1] # Location of the bottom '3'
        else:
            # No vertical pairs, find the topmost, then leftmost eligible '3'
            # eligible_threes is already sorted by row, then column
            trigger_location = eligible_threes[0]

    # Draw the '1' square if a trigger location was found
    if trigger_location:
        r_trigger, c_trigger = trigger_location
        _draw_hollow_square(output_array, r_trigger, c_trigger, 4, 1)

    # Convert the result back to a list of lists
    return output_array.tolist()
```