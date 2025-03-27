```python
import numpy as np
from typing import List, Tuple

"""
Move gray pixels (color 5) towards the nearest part of a static red object (color 2) 
until they become adjacent (including diagonals) to any part of the red object.
The red object and background (color 0) remain unchanged.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def is_adjacent(p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
    """Checks if two points are adjacent (including diagonals)."""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])) == 1

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Moves gray pixels towards the nearest red pixel until adjacency is reached.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # 1. Identify all pixels belonging to the static red (2) object
    red_pixels = find_pixels(grid, 2)

    # 2. Identify all gray (5) pixels in the input grid
    gray_pixels_initial = find_pixels(grid, 5)

    # Handle cases with no red or no gray pixels
    if not red_pixels or not gray_pixels_initial:
        return output_grid.tolist() # Return the original grid

    # 3. For each identified gray pixel:
    for initial_pos in gray_pixels_initial:
        r_init, c_init = initial_pos

        # a. Remove the gray pixel from its original position in the output grid
        output_grid[r_init, c_init] = 0

        # b. Calculate distances to red pixels
        min_dist = float('inf')
        target_red_pixels = []
        for red_pos in red_pixels:
            dist = manhattan_distance(initial_pos, red_pos)
            if dist < min_dist:
                min_dist = dist
                target_red_pixels = [red_pos]
            elif dist == min_dist:
                target_red_pixels.append(red_pos)

        # c. Select one target red pixel consistently (e.g., smallest row, then col)
        target_red_pixels.sort()
        target_red_pos = target_red_pixels[0]
        r_target, c_target = target_red_pos

        # d. Set the gray pixel's current position to its initial position
        current_pos = initial_pos

        # e. Start a movement loop:
        while True:
            # i. Check adjacency to *any* red pixel
            is_adj = False
            for red_pos in red_pixels:
                if is_adjacent(current_pos, red_pos):
                    is_adj = True
                    break
            
            # ii. If adjacent, exit the loop
            if is_adj:
                break

            # Check if we are already at the target (can happen if initial pos is the target)
            # Although the problem description implies movement towards, this handles a theoretical edge case.
            # More importantly, stops if movement calculation yields (0,0) but not adjacent.
            if current_pos == target_red_pos:
                 break # Should ideally not happen unless initial pos is target itself.

            # iii. Calculate the next step direction towards the target red pixel
            r_curr, c_curr = current_pos
            dr = np.sign(r_target - r_curr) # -1, 0, or 1
            dc = np.sign(c_target - c_curr) # -1, 0, or 1

            # iv. Update the gray pixel's current position
            next_r, next_c = r_curr + dr, c_curr + dc
            
            # Boundary check (should not be strictly necessary if target is within grid, but good practice)
            next_r = max(0, min(height - 1, next_r))
            next_c = max(0, min(width - 1, next_c))
            
            current_pos = (next_r, next_c)
            
            # Safety break to prevent infinite loops in unforeseen circumstances
            # (e.g., if somehow dr=0 and dc=0 but not adjacent)
            if dr == 0 and dc == 0:
                 # print(f"Warning: Stuck at {current_pos} for target {target_red_pos}")
                 break


        # f. Place the gray (5) color at the final position in the output grid
        final_r, final_c = current_pos
        # Ensure the final position is within bounds (redundant with boundary check above but safe)
        if 0 <= final_r < height and 0 <= final_c < width:
             # Check if the final spot is occupied by the static red object itself. 
             # If so, we shouldn't overwrite it (although the adjacency check should prevent this).
             # It's more likely another gray pixel might end up here. We allow overwriting white.
             # Based on examples, gray pixels can end up next to each other, possibly overwriting previous gray final spots.
             # Let's assume the last gray pixel processed 'wins' the spot if there's overlap.
            if output_grid[final_r, final_c] != 2: # Don't overwrite red
                 output_grid[final_r, final_c] = 5


    # 4. Return the modified output grid as a list of lists
    return output_grid.tolist()
```