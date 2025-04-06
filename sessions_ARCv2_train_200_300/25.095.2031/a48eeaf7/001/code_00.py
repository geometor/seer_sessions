import math
import numpy as np

"""
Relocates objects ('5's) in a grid towards the nearest cell of a static 2x2 block ('2's),
stopping just before colliding with the block. The movement follows the shortest path 
(Manhattan distance) step by step. The final positions of the '5's and the original 
position of the '2' block are placed in an otherwise zeroed grid.
"""

def find_element_coords(grid: list[list[int]], value: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of cells with a specific value."""
    coords = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == value:
                coords.append((r, c))
    return coords

def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_nearest_target(position: tuple[int, int], target_coords: list[tuple[int, int]]) -> tuple[int, int]:
    """Finds the target coordinate closest to the given position."""
    min_dist = float('inf')
    nearest_target = None
    for target in target_coords:
        dist = manhattan_distance(position, target)
        if dist < min_dist:
            min_dist = dist
            nearest_target = target
        # Optional: Tie-breaking (e.g., prefer smaller row, then smaller col) - not strictly needed based on examples
        elif dist == min_dist:
             if nearest_target is None or target[0] < nearest_target[0] or (target[0] == nearest_target[0] and target[1] < nearest_target[1]):
                 nearest_target = target
    return nearest_target

def get_step_direction(current: tuple[int, int], target: tuple[int, int]) -> tuple[int, int]:
    """Calculates the (dr, dc) step direction towards the target."""
    dr = 0
    if target[0] > current[0]:
        dr = 1
    elif target[0] < current[0]:
        dr = -1
        
    dc = 0
    if target[1] > current[1]:
        dc = 1
    elif target[1] < current[1]:
        dc = -1
        
    # Prioritize moving along the axis with greater distance difference?
    # The description implies moving one step in row and/or column direction simultaneously if needed.
    # Let's stick to the simple sign calculation for now.
    # If we want diagonal moves, dr and dc can be non-zero simultaneously.
    # If we want cardinal moves only, prioritize one axis. The NL program implies simultaneous moves.
    
    return dr, dc

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Moves each '5' towards the nearest '2' cell, stopping just before collision.
    
    Args:
        input_grid: A 2D list of integers representing the input state.

    Returns:
        A 2D list of integers representing the final state after movement.
    """
    if not input_grid:
        return []
        
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Use numpy for easier grid manipulation if allowed, otherwise stick to lists
    output_grid_np = np.zeros((rows, cols), dtype=int)
    input_grid_np = np.array(input_grid, dtype=int)

    # Locate the target block ('2's) and the movers ('5's)
    target_coords = find_element_coords(input_grid, 2)
    mover_start_coords = find_element_coords(input_grid, 5)

    # Place the static target block in the output grid
    if target_coords:
        for r, c in target_coords:
             if 0 <= r < rows and 0 <= c < cols:
                output_grid_np[r, c] = 2
    else:
        # Handle case with no target block? Return input or empty grid? 
        # Based on examples, target always exists. Assume it does.
        pass # Or raise an error, depending on requirements

    # Process each mover
    for start_pos in mover_start_coords:
        curr_pos = start_pos
        
        # Check if the mover starts adjacent to a target
        is_adjacent_start = False
        if target_coords:
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]: # Check 8 neighbors
                 check_r, check_c = start_pos[0] + dr, start_pos[1] + dc
                 if (check_r, check_c) in target_coords:
                     is_adjacent_start = True
                     break
        
        # If starting next to a target, it doesn't move
        if is_adjacent_start:
            final_pos = start_pos
        elif not target_coords:
             # If no target, mover stays put
             final_pos = start_pos
        else:
             # Simulate movement step-by-step
            while True:
                # Find the closest target cell from the current position
                nearest_target = find_nearest_target(curr_pos, target_coords)
                if nearest_target is None: # Should not happen if target_coords is not empty
                     break 

                # Calculate the next step direction
                dr, dc = get_step_direction(curr_pos, nearest_target)

                # If no move needed (already at optimal non-colliding spot relative to nearest), break
                if dr == 0 and dc == 0: 
                    # This case happens if the mover is already at a position where the nearest target
                    # is in the same row/col and moving would collide, OR if the mover is equidistant 
                    # to multiple targets and the step calculation results in (0,0) - though this shouldn't happen with sign().
                    # More likely: the mover has reached its closest possible non-adjacent spot.
                    break 

                # Determine the next potential position
                next_r, next_c = curr_pos[0] + dr, curr_pos[1] + dc

                # Check if the next position is valid and if it contains a target ('2')
                if not (0 <= next_r < rows and 0 <= next_c < cols):
                     # Moved off grid - stop at current position (shouldn't happen if target is on grid)
                     break 
                
                # Check for collision: Is the *next* cell a target cell?
                if input_grid_np[next_r, next_c] == 2:
                    # Stop movement *before* entering the target cell
                    break 
                else:
                    # Update current position and continue the loop
                    curr_pos = (next_r, next_c)

            # The loop terminated, curr_pos holds the final position
            final_pos = curr_pos

        # Place the mover at its final position in the output grid
        if 0 <= final_pos[0] < rows and 0 <= final_pos[1] < cols:
             # Ensure we don't overwrite the target block if a 5 ends up there (shouldn't happen)
             if output_grid_np[final_pos[0], final_pos[1]] == 0:
                 output_grid_np[final_pos[0], final_pos[1]] = 5
             # Handle potential overlap of final positions if multiple '5's land on the same spot?
             # Current logic: Last one wins. Requirements might specify differently.


    # Convert back to list of lists if necessary
    output_grid = output_grid_np.tolist()
    
    return output_grid