import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transforms an input grid based on specific digit patterns and locations, following a defined order of operations:

1.  **Rule 4 (FiveThreeRectangle):** Identifies rectangles formed by '5's in the top row and '3's in the bottom row. For each rectangle defined by corners (r1, c1), (r1, c2), (r2, c1), (r2, c2), it draws four 2x2 blocks of '6' in the output at locations (r1, c1), (r1, c2), (r2-3, c1), and (r2-3, c2). Tracks the '3's used.
2.  **Rule 1 (TwoMarker):** Finds all occurrences of digit '2' and draws a 4x4 hollow square using '4' at each location (r, c) in the output, anchored at (r, c).
3.  **Rule 2 (SixBlock):** Finds all top-left corners (r, c) of 2x2 blocks filled with '6' and draws a 2x2 block of '6' at (r-1, c-1) in the output.
4.  **Rule 3 (OneSquare):** Finds all top-left corners (r, c) of perfect 4x4 hollow squares filled with '1' (perimeter is '1', interior is not '1') and draws a 4x4 hollow square of '1' at (r, c+1) in the output.
5.  **Rule 5 (TriggerOneSquareFromThree):** Processes remaining '3's (not part of FiveThreeRectangles). If vertical pairs exist among these '3's, it finds the pair with the lowest bottom '3' (minimum r_b) and draws a 4x4 hollow square of '1' at that bottom '3's location. If no vertical pairs exist, it finds the topmost, then leftmost remaining '3' and draws the '1' square there. Only one '1' square is drawn based on this rule per grid.
6.  Overlapping patterns are overlaid based on the rule application order; non-zero digits overwrite zeros. Boundary checks are applied.
"""

# ============================================
# Helper Functions
# ============================================

def _is_valid(r: int, c: int, height: int, width: int) -> bool:
    """Checks if coordinates (r, c) are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def _draw_block(grid: np.ndarray, r: int, c: int, h: int, w: int, value: int):
    """Draws a solid h x w block with top-left at (r, c) using 'value'."""
    height, width = grid.shape
    for i in range(r, r + h):
        for j in range(c, c + w):
            if _is_valid(i, j, height, width):
                grid[i, j] = value

def _draw_hollow_square(grid: np.ndarray, r: int, c: int, size: int, value: int):
    """Draws a hollow square of 'size' x 'size' with top-left at (r, c) using 'value'."""
    height, width = grid.shape
    # Draw top and bottom edges
    for j in range(c, c + size):
        if _is_valid(r, j, height, width):
            grid[r, j] = value
        if _is_valid(r + size - 1, j, height, width):
            # Avoid double drawing the bottom-left corner if size=1
            if size > 1 or i == r :
                 grid[r + size - 1, j] = value
            
    # Draw side edges (excluding corners already drawn if size > 1)
    for i in range(r + 1, r + size - 1):
        if _is_valid(i, c, height, width):
            grid[i, c] = value
        if _is_valid(i, c + size - 1, height, width):
            grid[i, c + size - 1] = value

def _is_block(grid: np.ndarray, r: int, c: int, h: int, w: int, value: int) -> bool:
    """Checks if an h x w block of 'value' exists with top-left at (r, c)."""
    height, width = grid.shape
    # Check if the entire block fits within the grid
    if not (_is_valid(r, c, height, width) and _is_valid(r + h - 1, c + w - 1, height, width)):
        return False
    # Check if all cells within the block have the specified value
    for i in range(r, r + h):
        for j in range(c, c + w):
            if grid[i, j] != value:
                return False
    return True

def _is_hollow_square(grid: np.ndarray, r: int, c: int, size: int, value: int) -> bool:
    """Checks if a perfect hollow 'size' x 'size' square of 'value' exists with top-left at (r, c)."""
    height, width = grid.shape
    # Check if the square fits within the grid
    if not (_is_valid(r, c, height, width) and _is_valid(r + size - 1, c + size - 1, height, width)):
        return False
        
    # Check perimeter cells have the correct value
    for j in range(c, c + size): # Top edge
        if not _is_valid(r, j, height, width) or grid[r, j] != value: return False
    for j in range(c, c + size): # Bottom edge
        if not _is_valid(r+size-1, j, height, width) or grid[r+size-1, j] != value: return False
    for i in range(r + 1, r + size - 1): # Left edge (excl corners)
        if not _is_valid(i, c, height, width) or grid[i, c] != value: return False
    for i in range(r + 1, r + size - 1): # Right edge (excl corners)
        if not _is_valid(i, c+size-1, height, width) or grid[i, c+size-1] != value: return False
        
    # Check interior cells do NOT have the perimeter value (size > 2)
    if size > 2:
        for i in range(r + 1, r + size - 1):
            for j in range(c + 1, c + size - 1):
                # Boundary check for interior cell (should always be valid if perimeter is)
                if not _is_valid(i, j, height, width): return False 
                if grid[i, j] == value: # Interior cell must NOT match the perimeter value
                    return False
    return True

# ============================================
# Main Transformation Function
# ============================================

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a series of transformations to the input grid based on detected patterns.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    # Initialize output grid with zeros
    output_array = np.zeros_like(input_array)

    # --- Pre-scan: Find initial locations of '3's and '5's ---
    three_locations: List[Tuple[int, int]] = []
    five_locations: List[Tuple[int, int]] = []
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 3:
                three_locations.append((r, c))
            elif input_array[r, c] == 5:
                five_locations.append((r, c))
    
    used_threes_in_rectangle: Set[Tuple[int, int]] = set()

    # --- Rule 4: FiveThreeRectangle -> Four 2x2 '6' blocks ---
    # Iterate through pairs of '5's to find potential top edges
    five_loc_set = set(five_locations) # Faster lookups
    three_loc_set = set(three_locations) # Faster lookups

    processed_rectangles = set() # Avoid processing same rectangle multiple times

    for r1, c1 in five_locations:
        # Look for a '5' to the right in the same row
        for c2 in range(c1 + 1, width):
             p2 = (r1, c2)
             if p2 in five_loc_set:
                 # Found potential top edge (r1, c1) to (r1, c2)
                 # Look for corresponding bottom edge '3's
                 for r2 in range(r1 + 1, height):
                     p3 = (r2, c1)
                     p4 = (r2, c2)
                     if p3 in three_loc_set and p4 in three_loc_set:
                         # Found a FiveThreeRectangle!
                         rect_key = tuple(sorted([ (r1,c1), p2, p3, p4]))
                         if rect_key not in processed_rectangles:
                             processed_rectangles.add(rect_key)
                             
                             # Mark the '3's as used
                             used_threes_in_rectangle.add(p3)
                             used_threes_in_rectangle.add(p4)
                             
                             # Draw the four 2x2 blocks of '6'
                             _draw_block(output_array, r1, c1, 2, 2, 6)
                             _draw_block(output_array, r1, c2, 2, 2, 6)
                             _draw_block(output_array, r2 - 3, c1, 2, 2, 6) # Corrected
                             _draw_block(output_array, r2 - 3, c2, 2, 2, 6) # Corrected
                         # Found the matching bottom row, no need to check further down for this top edge
                         break 

    # --- Rule 1: '2' -> 4x4 hollow '4' square ---
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 2:
                _draw_hollow_square(output_array, r, c, 4, 4)

    # --- Rule 2: 2x2 '6' block -> shifted 2x2 '6' block ---
    for r in range(height - 1): # Check potential top-left corners
        for c in range(width - 1):
            if _is_block(input_array, r, c, 2, 2, 6):
                _draw_block(output_array, r - 1, c - 1, 2, 2, 6)

    # --- Rule 3: 4x4 hollow '1' square -> shifted 4x4 hollow '1' square ---
    for r in range(height - 3): # Check potential top-left corners
        for c in range(width - 3):
             if _is_hollow_square(input_array, r, c, 4, 1):
                 _draw_hollow_square(output_array, r, c + 1, 4, 1)

    # --- Rule 5: Conditional '3' -> 4x4 hollow '1' square ---
    eligible_threes = [loc for loc in three_locations if loc not in used_threes_in_rectangle]
    trigger_location: Optional[Tuple[int, int]] = None

    if eligible_threes:
        # Sort for consistent tie-breaking (topmost, then leftmost)
        eligible_threes.sort() 
        eligible_set = set(eligible_threes) 
        
        min_rb = float('inf')
        best_pair_bottom_loc: Optional[Tuple[int, int]] = None

        # Check for vertical pairs and find the one with the minimum bottom row (r_b)
        processed_cols = set()
        for r_a, c_a in eligible_threes:
            if c_a in processed_cols: continue # Already found lowest pair for this column

            # Look downwards for another eligible '3' in the same column
            for r_b in range(r_a + 1, height):
                 lower_loc = (r_b, c_a)
                 if lower_loc in eligible_set:
                      # Found a vertical pair ((r_a, c_a), lower_loc)
                      if r_b < min_rb:
                          min_rb = r_b
                          best_pair_bottom_loc = lower_loc
                      # Mark column as processed since we found the first (and thus lowest r_b) pair starting from the top for this column
                      processed_cols.add(c_a)
                      break # Move to next eligible '3' in the sorted list

        if best_pair_bottom_loc:
            # Found vertical pairs, use the bottom location of the pair with the overall minimum r_b
            trigger_location = best_pair_bottom_loc 
        else:
            # No vertical pairs found, use the topmost, then leftmost eligible '3'
            # eligible_threes is already sorted, so the first element is the one.
            trigger_location = eligible_threes[0]

    # Draw the '1' square if a trigger location was determined
    if trigger_location:
        r_trigger, c_trigger = trigger_location
        _draw_hollow_square(output_array, r_trigger, c_trigger, 4, 1)

    # Convert the result back to a standard list of lists
    return output_array.tolist()