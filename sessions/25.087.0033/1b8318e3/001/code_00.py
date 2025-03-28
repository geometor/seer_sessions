import numpy as np
from typing import List, Tuple, Dict

"""
Identifies 2x2 gray squares and other colored pixels (non-white, non-gray) in the input grid.
Pixels adjacent (including diagonally) to any part of a gray square are removed (set to white).
Non-adjacent colored pixels are moved.
The movement rule is:
1. Find the "closest" 2x2 gray square to the colored pixel.
   - "Closest" is defined by the minimum Manhattan distance from the pixel's coordinates to any of the four cells forming the gray square.
   - Ties in distance are broken by choosing the gray square whose top-left corner has the highest row index, then the highest column index.
2. Find the target destination cell:
   - Identify all empty (white) cells adjacent (including diagonally) to the chosen gray square.
   - Calculate the Manhattan distance from the original colored pixel's position to each of these empty adjacent cells.
   - The destination cell is the one with the minimum Manhattan distance.
   - Ties are broken by choosing the cell with the lowest row index, then the lowest column index.
3. The colored pixel is moved from its original location to the determined destination cell. The original location becomes white.
The output grid reflects these removals and movements. Gray squares remain unchanged.
"""

def find_gray_squares(grid: np.ndarray) -> List[Tuple[int, int]]:
    """Finds the top-left coordinates of all 2x2 gray (5) squares."""
    gray_squares = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            if (grid[r, c] == 5 and
                grid[r + 1, c] == 5 and
                grid[r, c + 1] == 5 and
                grid[r + 1, c + 1] == 5):
                gray_squares.append((r, c))
    return gray_squares

def find_colored_pixels(grid: np.ndarray) -> List[Tuple[Tuple[int, int], int]]:
    """Finds all non-white (0) and non-gray (5) pixels."""
    colored_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != 5:
                colored_pixels.append(((r, c), color))
    return colored_pixels

def get_gray_square_cells(square_tl: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Returns the four cell coordinates of a gray square given its top-left."""
    r, c = square_tl
    return [(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)]

def is_adjacent_to_gray(r: int, c: int, gray_squares: List[Tuple[int, int]]) -> bool:
    """Checks if a pixel at (r, c) is adjacent (incl. diagonally) to any gray square cell."""
    for sq_tl in gray_squares:
        sq_cells = get_gray_square_cells(sq_tl)
        for sq_r, sq_c in sq_cells:
            if abs(r - sq_r) <= 1 and abs(c - sq_c) <= 1:
                # Check it's not the cell itself, but an adjacent one
                if not (r == sq_r and c == sq_c): 
                     # Now check if the adjacent cell is actually part of *any* gray square
                     for check_sq_tl in gray_squares:
                         check_sq_cells = get_gray_square_cells(check_sq_tl)
                         if (sq_r, sq_c) in check_sq_cells:
                              return True
    return False
    
def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_closest_gray_square(r: int, c: int, gray_squares: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Finds the closest gray square based on min distance and tie-breaking rules."""
    min_dist = float('inf')
    closest_squares = []

    for sq_tl in gray_squares:
        sq_cells = get_gray_square_cells(sq_tl)
        current_min_dist_to_square = float('inf')
        for sq_r, sq_c in sq_cells:
            dist = manhattan_distance((r, c), (sq_r, sq_c))
            current_min_dist_to_square = min(current_min_dist_to_square, dist)
        
        if current_min_dist_to_square < min_dist:
            min_dist = current_min_dist_to_square
            closest_squares = [sq_tl]
        elif current_min_dist_to_square == min_dist:
            closest_squares.append(sq_tl)

    # Tie-breaking: highest row, then highest column for top-left corner
    closest_squares.sort(key=lambda sq: (-sq[0], -sq[1]))
    return closest_squares[0]

def find_destination_cell(r: int, c: int, chosen_square_tl: Tuple[int, int], grid: np.ndarray) -> Tuple[int, int]:
    """Finds the best destination cell adjacent to the chosen gray square."""
    height, width = grid.shape
    sq_cells = get_gray_square_cells(chosen_square_tl)
    potential_destinations = []

    # Find all adjacent cells (including diagonals) to the gray square
    adjacent_cells = set()
    for sq_r, sq_c in sq_cells:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = sq_r + dr, sq_c + dc
                # Check bounds and ensure it's not part of the square itself
                if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in sq_cells:
                    adjacent_cells.add((nr, nc))

    # Filter for empty (white) cells and calculate distances
    min_dist = float('inf')
    valid_destinations = []
    for dest_r, dest_c in adjacent_cells:
        if grid[dest_r, dest_c] == 0: # Check if the cell is initially empty
            dist = manhattan_distance((r, c), (dest_r, dest_c))
            if dist < min_dist:
                min_dist = dist
                valid_destinations = [(dest_r, dest_c)]
            elif dist == min_dist:
                valid_destinations.append((dest_r, dest_c))

    # Tie-breaking: lowest row, then lowest column
    valid_destinations.sort(key=lambda pos: (pos[0], pos[1]))
    
    # It's possible no valid empty adjacent cell exists, though not seen in examples
    if not valid_destinations:
        # This case shouldn't happen based on examples, but handle defensively
        # Maybe return original position or raise error? Let's return original for now.
         print(f"Warning: No valid destination found for pixel at ({r},{c}) near square {chosen_square_tl}. Keeping original position.")
         return (r, c) 
         
    return valid_destinations[0]


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the rules:
    - Removes colored pixels adjacent to gray squares.
    - Moves non-adjacent colored pixels closer to their nearest gray square.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find static elements
    gray_squares = find_gray_squares(input_grid)
    
    # Find elements to process
    colored_pixels = find_colored_pixels(input_grid)

    # Store moves to apply later to avoid conflicts during iteration
    moves = {} # original_pos -> new_pos
    removals = [] # original_pos

    for (r, c), color in colored_pixels:
        # Check adjacency to any gray square
        is_adj = False
        for sq_tl in gray_squares:
             sq_cells = get_gray_square_cells(sq_tl)
             for sq_r, sq_c in sq_cells:
                 # Check 8 neighbours of the pixel (r,c)
                 for dr in [-1, 0, 1]:
                     for dc in [-1, 0, 1]:
                         if dr == 0 and dc == 0:
                             continue
                         nr, nc = r + dr, c + dc
                         if (nr, nc) == (sq_r, sq_c): # Is neighbour a gray cell?
                             is_adj = True
                             break
                     if is_adj: break
             if is_adj: break
        
        if is_adj:
            # Mark for removal (set to white)
            removals.append((r, c))
        else:
            # Pixel needs to be moved
            if not gray_squares: # Handle case with no gray squares
                 print(f"Warning: No gray squares found. Pixel at ({r},{c}) cannot be moved.")
                 continue # Pixel stays in place

            # 1. Find the closest gray square
            chosen_square_tl = find_closest_gray_square(r, c, gray_squares)

            # 2. Find the destination cell using the *original* grid state for emptiness check
            dest_r, dest_c = find_destination_cell(r, c, chosen_square_tl, input_grid)

            # Mark for movement
            if (r, c) != (dest_r, dest_c): # Only record if it actually moves
                moves[(r, c)] = (dest_r, dest_c, color)


    # Apply removals first
    for r, c in removals:
        output_grid[r, c] = 0

    # Apply moves - need to handle potential overwrites if multiple pixels target same destination
    # Since tie-breaking for destination exists, this implies a unique target per source pixel.
    # Let's clear original positions first, then place new ones.
    
    # Intermediate grid to handle potential move conflicts (A->B, C->A)
    temp_grid = np.copy(output_grid) 
    
    # Clear original positions of moved pixels
    for (r, c) in moves.keys():
         temp_grid[r,c] = 0 # Make original spot empty in temp grid
         
    # Place pixels in new positions
    final_output_grid = np.copy(temp_grid) # Start with cleared spots
    
    # Check for conflicts before placing
    target_cells = {} # dest_pos -> list of source_pos
    for source_pos, (dest_r, dest_c, color) in moves.items():
        dest_pos = (dest_r, dest_c)
        if dest_pos not in target_cells:
            target_cells[dest_pos] = []
        target_cells[dest_pos].append(source_pos)

    # Apply moves, handling conflicts (though examples don't show any)
    # If conflict, problem is underspecified. Let's assume no conflicts based on examples.
    for source_pos, (dest_r, dest_c, color) in moves.items():
        if len(target_cells.get((dest_r, dest_c), [])) > 1:
             print(f"Warning: Conflict detected! Multiple pixels moving to ({dest_r},{dest_c}). Sources: {target_cells[(dest_r, dest_c)]}. Behavior undefined.")
             # Apply one arbitrarily for now, maybe the one processed last in original loop?
             # Or maybe the one with lower original row/col? Let's stick to last-write wins for now.
        final_output_grid[dest_r, dest_c] = color


    return final_output_grid