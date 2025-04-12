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
    # Handle edge case for size 2 squares where interior check isn't needed
    elif size == 2:
        pass # Already checked perimeter
    # Squares of size < 2 are not considered hollow in the typical sense
    elif size < 2:
        return False # Or handle as per specific requirements for size 1

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

    # Pre-scan: Find initial locations of '3's and '5's for efficiency
    three_locations: List[Tuple[int, int]] = []
    five_locations: List[Tuple[int, int]] = []
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 3:
                three_locations.append((r, c))
            elif input_array[r, c] == 5:
                five_locations.append((r, c))
    
    # Keep track of '3's used in the FiveThreeRectangle rule
    used_threes_in_rectangle: Set[Tuple[int, int]] = set()

    # --- Apply Rule 4: FiveThreeRectangle -> Four 2x2 '6' blocks ---
    five_loc_set = set(five_locations) # Use sets for faster lookups
    three_loc_set = set(three_locations)
    processed_rectangles = set() # Avoid processing the same rectangle multiple times

    # Iterate through potential top-left '5' corners
    for r1, c1 in five_locations:
        # Look for a '5' to the right in the same row (potential P2)
        for c2 in range(c1 + 1, width):
             p2 = (r1, c2)
             if p2 in five_loc_set:
                 # Found potential top edge (r1, c1) to (r1, c2)
                 # Look downwards for corresponding bottom edge '3's (P3 and P4)
                 for r2 in range(r1 + 1, height):
                     p3 = (r2, c1)
                     p4 = (r2, c2)
                     if p3 in three_loc_set and p4 in three_loc_set:
                         # Found a valid FiveThreeRectangle
                         # Use a canonical key for the rectangle to handle detection order
                         rect_key = tuple(sorted([(r1,c1), p2, p3, p4])) 
                         if rect_key not in processed_rectangles:
                             processed_rectangles.add(rect_key)
                             
                             # Mark the involved '3's as used for Rule 5
                             used_threes_in_rectangle.add(p3)
                             used_threes_in_rectangle.add(p4)
                             
                             # Draw the four required 2x2 blocks of '6's
                             _draw_block(output_array, r1, c1, 2, 2, 6)
                             _draw_block(output_array, r1, c2, 2, 2, 6)
                             _draw_block(output_array, r2 - 3, c1, 2, 2, 6) # Corrected offset
                             _draw_block(output_array, r2 - 3, c2, 2, 2, 6) # Corrected offset
                         # Found the correct bottom row for this top edge, stop searching lower
                         break 

    # --- Apply Rule 1: '2' -> 4x4 hollow '4' square ---
    # Iterate through all cells to find '2's
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 2:
                # Draw the hollow square anchored at the '2's position
                _draw_hollow_square(output_array, r, c, 4, 4)

    # --- Apply Rule 2: 2x2 '6' block -> shifted 2x2 '6' block ---
    # Iterate through possible top-left corners of 2x2 blocks
    for r in range(height - 1): 
        for c in range(width - 1):
            # Check if a 2x2 block of '6's exists here
            if _is_block(input_array, r, c, 2, 2, 6):
                # Draw the shifted block in the output
                _draw_block(output_array, r - 1, c - 1, 2, 2, 6)

    # --- Apply Rule 3: 4x4 hollow '1' square -> shifted 4x4 hollow '1' square ---
    # Iterate through possible top-left corners of 4x4 squares
    for r in range(height - 3): 
        for c in range(width - 3):
             # Check if a perfect hollow 4x4 square of '1's exists here
             if _is_hollow_square(input_array, r, c, 4, 1):
                 # Draw the shifted hollow square in the output
                 _draw_hollow_square(output_array, r, c + 1, 4, 1)

    # --- Apply Rule 5: Conditional '3' -> single 4x4 hollow '1' square ---
    # Filter '3' locations to exclude those used in Rule 4
    eligible_threes = [loc for loc in three_locations if loc not in used_threes_in_rectangle]
    trigger_location: Optional[Tuple[int, int]] = None # Stores the single location for the '1' square

    if eligible_threes:
        # Sort eligible '3's for consistent tie-breaking (topmost, then leftmost)
        eligible_threes.sort() 
        eligible_set = set(eligible_threes) # Use set for efficient checking of vertical pairs
        
        min_rb = float('inf') # Track the minimum bottom-row index found in any vertical pair
        best_pair_bottom_loc: Optional[Tuple[int, int]] = None # Track the location of the bottom '3' in the best pair

        # Check for vertical pairs among eligible '3's
        processed_cols = set() # Avoid re-checking columns where a pair was already found
        for r_a, c_a in eligible_threes:
            # Skip if we've already found the defining vertical pair for this column
            if c_a in processed_cols: continue 

            # Look downwards from the current '3' for another eligible '3' in the same column
            for r_b in range(r_a + 1, height):
                 lower_loc = (r_b, c_a)
                 if lower_loc in eligible_set:
                      # Found a vertical pair: ((r_a, c_a), lower_loc)
                      # Check if this pair's bottom '3' is the lowest found so far
                      if r_b < min_rb:
                          min_rb = r_b
                          best_pair_bottom_loc = lower_loc
                      # Mark column as processed; we only care about the pair starting with the topmost '3' in the column
                      processed_cols.add(c_a) 
                      break # Move to the next eligible '3' in the sorted list

        # Determine the trigger location based on whether a vertical pair was found
        if best_pair_bottom_loc:
            # Case 1: Vertical pair(s) exist. Use the bottom location of the pair with the overall minimum r_b.
            trigger_location = best_pair_bottom_loc 
        else:
            # Case 2: No vertical pairs found. Use the topmost, then leftmost eligible '3'.
            # Since eligible_threes is sorted, the first element is the correct one.
            trigger_location = eligible_threes[0]

    # Draw the single '1' square if a trigger location was determined
    if trigger_location:
        r_trigger, c_trigger = trigger_location
        _draw_hollow_square(output_array, r_trigger, c_trigger, 4, 1)

    # Convert the final numpy array back to a standard list of lists for the return value
    return output_array.tolist()