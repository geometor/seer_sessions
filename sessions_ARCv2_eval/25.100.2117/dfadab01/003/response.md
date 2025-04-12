```python
import numpy as np
from typing import List, Tuple, Set

"""
Transforms an input grid based on specific digit patterns and locations:

1.  Finds all occurrences of digit '2' and draws a 4x4 hollow square using '4' at each location in the output.
2.  Finds all top-left corners (r, c) of 2x2 blocks filled with '6' and draws a 2x2 block of '6' at (r-1, c-1) in the output.
3.  Finds all top-left corners (r, c) of 4x4 hollow squares filled with '1' and draws a 4x4 hollow square of '1' at (r, c+1) in the output.
4.  Identifies "FiveThreeRectangles" formed by '5's in the top row and '3's in the bottom row. For each rectangle defined by corners (r1, c1), (r1, c2), (r2, c1), (r2, c2), it draws four 2x2 blocks of '6' in the output at locations (r1, c1), (r1, c2), (r2-3, c1), and (r2-3, c2). It tracks the '3's used in these rectangles.
5.  Processes remaining '3's (not part of FiveThreeRectangles). If vertical pairs exist, it finds the pair with the lowest bottom '3' and draws a 4x4 hollow square of '1' at that bottom '3's location. If no vertical pairs exist, it finds the topmost, then leftmost '3' and draws the '1' square there. Only one '1' square is drawn based on this rule.
6.  Overlapping patterns are overlaid; non-zero digits overwrite zeros.
"""

# Helper function to check grid boundaries
def is_valid(r, c, height, width):
    return 0 <= r < height and 0 <= c < width

# Helper function to draw a filled block
def draw_block(grid: np.ndarray, r: int, c: int, h: int, w: int, value: int):
    height, width = grid.shape
    for i in range(r, r + h):
        for j in range(c, c + w):
            if is_valid(i, j, height, width):
                grid[i, j] = value

# Helper function to draw a hollow square
def draw_hollow_square(grid: np.ndarray, r: int, c: int, size: int, value: int):
    height, width = grid.shape
    # Draw top and bottom edges
    for j in range(c, c + size):
        if is_valid(r, j, height, width):
            grid[r, j] = value
        if is_valid(r + size - 1, j, height, width):
            grid[r + size - 1, j] = value
    # Draw side edges (excluding corners already drawn)
    for i in range(r + 1, r + size - 1):
        if is_valid(i, c, height, width):
            grid[i, c] = value
        if is_valid(i, c + size - 1, height, width):
            grid[i, c + size - 1] = value

# Helper function to check for a specific block pattern
def is_block(grid: np.ndarray, r: int, c: int, h: int, w: int, value: int) -> bool:
    height, width = grid.shape
    if not (is_valid(r, c, height, width) and is_valid(r + h - 1, c + w - 1, height, width)):
        return False
    for i in range(r, r + h):
        for j in range(c, c + w):
            if grid[i, j] != value:
                return False
    return True

# Helper function to check for a hollow square pattern
def is_hollow_square(grid: np.ndarray, r: int, c: int, size: int, value: int) -> bool:
    height, width = grid.shape
    if not (is_valid(r, c, height, width) and is_valid(r + size - 1, c + size - 1, height, width)):
        return False
    # Check corners
    if grid[r, c] != value or \
       grid[r, c + size - 1] != value or \
       grid[r + size - 1, c] != value or \
       grid[r + size - 1, c + size - 1] != value:
           return False
    # Check edges
    for j in range(c + 1, c + size - 1): # Top and bottom edges
        if grid[r, j] != value or grid[r + size - 1, j] != value:
            return False
    for i in range(r + 1, r + size - 1): # Left and right edges
        if grid[i, c] != value or grid[i, c + size - 1] != value:
            return False
    # Check interior (should be background or different value, assuming 0 for now)
    for i in range(r + 1, r + size - 1):
        for j in range(c + 1, c + size - 1):
            if grid[i, j] == value: # Should not be the perimeter value
                 return False
    return True


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    output_array = np.zeros_like(input_array)
    
    three_locations: List[Tuple[int, int]] = []
    five_locations: List[Tuple[int, int]] = []
    used_threes_in_rectangle: Set[Tuple[int, int]] = set()

    # --- Find initial locations of relevant digits ---
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 3:
                three_locations.append((r, c))
            elif input_array[r, c] == 5:
                five_locations.append((r, c))

    # --- Rule 4: FiveThreeRectangles -> Four 2x2 '6' blocks ---
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
                            # Mark the '3's as used
                            used_threes_in_rectangle.add(three_locations[k])
                            used_threes_in_rectangle.add(three_locations[l])
                            
                            # Draw the four 2x2 blocks of '6'
                            draw_block(output_array, r1, c1, 2, 2, 6)
                            draw_block(output_array, r1, c2, 2, 2, 6)
                            draw_block(output_array, r2 - 3, c1, 2, 2, 6)
                            draw_block(output_array, r2 - 3, c2, 2, 2, 6)


    # --- Rule 1: '2' -> 4x4 hollow '4' square ---
    for r in range(height):
        for c in range(width):
            if input_array[r, c] == 2:
                draw_hollow_square(output_array, r, c, 4, 4)

    # --- Rule 2: 2x2 '6' block -> shifted 2x2 '6' block ---
    for r in range(height - 1):
        for c in range(width - 1):
            if is_block(input_array, r, c, 2, 2, 6):
                draw_block(output_array, r - 1, c - 1, 2, 2, 6)

    # --- Rule 3: 4x4 hollow '1' square -> shifted 4x4 hollow '1' square ---
    for r in range(height - 3):
        for c in range(width - 3):
             if is_hollow_square(input_array, r, c, 4, 1):
                 draw_hollow_square(output_array, r, c + 1, 4, 1)


    # --- Rule 5: Conditional '3' -> 4x4 hollow '1' square ---
    eligible_threes = [loc for loc in three_locations if loc not in used_threes_in_rectangle]
    trigger_location = None

    if eligible_threes:
        vertical_pairs = []
        # Find vertical pairs among eligible '3's
        eligible_threes.sort() # Sort by row, then col
        for i in range(len(eligible_threes)):
            for j in range(i + 1, len(eligible_threes)):
                r_a, c_a = eligible_threes[i]
                r_b, c_b = eligible_threes[j]
                if c_a == c_b and r_a < r_b:
                    vertical_pairs.append(((r_a, c_a), (r_b, c_b)))

        if vertical_pairs:
            # Find the pair with the minimum bottom row index (r_b)
            vertical_pairs.sort(key=lambda pair: pair[1][0]) # Sort by r_b
            trigger_location = vertical_pairs[0][1] # Location of the bottom '3'
        else:
            # No vertical pairs, find the topmost, then leftmost eligible '3'
            # Already sorted by row, then col
            trigger_location = eligible_threes[0]

    # Draw the '1' square if a trigger location was found
    if trigger_location:
        r_trigger, c_trigger = trigger_location
        draw_hollow_square(output_array, r_trigger, c_trigger, 4, 1)


    return output_array.tolist()
```