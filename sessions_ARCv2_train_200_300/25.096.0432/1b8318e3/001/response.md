```python
import math

"""
Processes a 2D grid of integers based on the following rules:

1. Identifies 2x2 blocks of the digit '5' (FiveSquares). These FiveSquares remain 
   static and are copied directly from the input to the output grid.
2. Identifies all other non-zero digits (SingletonDigits) that are not part of 
   a FiveSquare.
3. Each SingletonDigit is relocated in the output grid. Its destination is determined 
   by finding the nearest FiveSquare (based on Manhattan distance from the 
   SingletonDigit's original position to the center of the FiveSquare, with 
   top-left tie-breaking).
4. The SingletonDigit is then placed in one of the 12 cells immediately 
   adjacent (orthogonally or diagonally) to the chosen nearest FiveSquare. 
   The specific adjacent cell chosen is the one closest (Manhattan distance) 
   to the SingletonDigit's *original* position (with top-left tie-breaking).
5. The original positions of the moved SingletonDigits become '0' in the output grid, 
   unless overwritten by the destination of another SingletonDigit. All other '0' 
   cells from the input remain '0' unless overwritten.
"""

def find_five_squares(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Finds all top-left coordinates of 2x2 squares of 5s."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    five_squares_coords = []
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r][c] == 5 and grid[r+1][c] == 5 and
                    grid[r][c+1] == 5 and grid[r+1][c+1] == 5):
                five_squares_coords.append((r, c))
    return five_squares_coords

def is_part_of_five_square(r: int, c: int, five_squares_coords: list[tuple[int, int]]) -> bool:
    """Checks if a cell (r, c) belongs to any identified FiveSquare."""
    for sq_r, sq_c in five_squares_coords:
        if sq_r <= r <= sq_r + 1 and sq_c <= c <= sq_c + 1:
            return True
    return False

def find_singleton_digits(grid: list[list[int]], five_squares_coords: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """Finds all non-zero digits not part of a FiveSquare, returning (value, r, c)."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    singletons = []
    for r in range(rows):
        for c in range(cols):
            value = grid[r][c]
            if value != 0 and not is_part_of_five_square(r, c, five_squares_coords):
                singletons.append((value, r, c))
    return singletons

def manhattan_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_adjacent_cells(sq_r: int, sq_c: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """Gets the 12 adjacent cells around a 2x2 square starting at (sq_r, sq_c)."""
    adjacent = []
    # Cells around the 2x2 square
    for r_offset in range(-1, 3): # Covers rows from sq_r-1 to sq_r+2
        for c_offset in range(-1, 3): # Covers cols from sq_c-1 to sq_c+2
            r, c = sq_r + r_offset, sq_c + c_offset
            # Check if it's within grid bounds
            if 0 <= r < rows and 0 <= c < cols:
                # Check if it's *not* part of the 2x2 square itself
                is_part_of_square = (0 <= r_offset <= 1 and 0 <= c_offset <= 1)
                if not is_part_of_square:
                    adjacent.append((r, c))
    return adjacent


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by relocating singleton digits towards the nearest
    2x2 '5' square.
    """
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 1. Find FiveSquares and copy them to the output
    five_squares_coords = find_five_squares(input_grid)
    for r_sq, c_sq in five_squares_coords:
        for r_offset in range(2):
            for c_offset in range(2):
                if 0 <= r_sq + r_offset < rows and 0 <= c_sq + c_offset < cols:
                     output_grid[r_sq + r_offset][c_sq + c_offset] = 5

    # 2. Find SingletonDigits
    singletons = find_singleton_digits(input_grid, five_squares_coords)

    # 3. Process each SingletonDigit
    processed_targets = set() # Keep track of occupied target cells to handle potential overwrites (first wins)

    for value, r_orig, c_orig in singletons:
        
        # 4a. Calculate distance to each FiveSquare center
        nearest_sq_coord = None
        min_dist_to_sq = float('inf')

        if not five_squares_coords: # Handle case with no five squares
             # If no FiveSquares, singleton stays put? Or disappears? 
             # Based on examples, they seem to disappear if no FiveSquare exists.
             # Let's assume they disappear (remain 0 in output).
             continue 

        for r_sq, c_sq in five_squares_coords:
            # Center of the FiveSquare (using top-left + 0.5 offset)
            center_sq = (r_sq + 0.5, c_sq + 0.5)
            dist = manhattan_distance((r_orig, c_orig), center_sq)

            # 4b. Determine nearest FiveSquare with tie-breaking
            if dist < min_dist_to_sq:
                min_dist_to_sq = dist
                nearest_sq_coord = (r_sq, c_sq)
            elif dist == min_dist_to_sq:
                # Tie-breaking: top-most (smaller r), then left-most (smaller c)
                if r_sq < nearest_sq_coord[0]:
                    nearest_sq_coord = (r_sq, c_sq)
                elif r_sq == nearest_sq_coord[0] and c_sq < nearest_sq_coord[1]:
                    nearest_sq_coord = (r_sq, c_sq)

        if nearest_sq_coord is None: 
             # Should not happen if five_squares_coords is not empty, but defensive check
             continue

        # 4c. Get adjacent cells for the nearest FiveSquare
        r_sq_nearest, c_sq_nearest = nearest_sq_coord
        adjacent_cells = get_adjacent_cells(r_sq_nearest, c_sq_nearest, rows, cols)

        # 4d. Find the closest adjacent cell to the singleton's *original* position
        closest_adj_cell = None
        min_dist_to_adj = float('inf')

        potential_targets = []
        for r_adj, c_adj in adjacent_cells:
            # Only consider cells that are currently 0 in the output grid (available)
             # Also check if it hasn't been claimed by another singleton already in this loop
            if output_grid[r_adj][c_adj] == 0 and (r_adj, c_adj) not in processed_targets:
                dist = manhattan_distance((r_orig, c_orig), (r_adj, c_adj))
                potential_targets.append(((r_adj, c_adj), dist))

        if not potential_targets:
            # No available adjacent cell found, the singleton might disappear
            # Or maybe there's another rule? Based on examples, it seems it lands somewhere.
            # Re-evaluate: Maybe it can overwrite 0s even if not adjacent? Let's stick to adjacent for now.
            # It's possible the adjacent cell calculation or the target availability check is slightly off.
            # Let's assume it must find *one* of the 12, even if occupied by 0.
            # Re-calculating distances for *all* 12 adjacent cells
            
            potential_targets = [] # Reset and recalculate without the output_grid[r_adj][c_adj] == 0 check initially
            for r_adj, c_adj in adjacent_cells:
                 dist = manhattan_distance((r_orig, c_orig), (r_adj, c_adj))
                 potential_targets.append(((r_adj, c_adj), dist))


        if not potential_targets: # Still no targets? Something is wrong.
             # For now, skip placing this singleton if no adjacent cells found
             # This might indicate an edge case or misunderstanding.
             print(f"Warning: No adjacent cells found for singleton {value} at ({r_orig}, {c_orig}) near square at {nearest_sq_coord}")
             continue


        # Sort potential targets: primary key distance, secondary key row, tertiary key column
        potential_targets.sort(key=lambda x: (x[1], x[0][0], x[0][1]))
        
        # 4e. Determine the best target cell based on sorted list (handles tie-breaking)
        # Find the first target that hasn't been claimed yet
        chosen_target = None
        for target_coord, dist in potential_targets:
            if target_coord not in processed_targets:
                 # Check if the target cell is part of another FiveSquare (shouldn't happen with get_adjacent_cells logic, but safety check)
                 is_target_part_of_sq = False
                 for sq_r_chk, sq_c_chk in five_squares_coords:
                     if sq_r_chk <= target_coord[0] <= sq_r_chk + 1 and sq_c_chk <= target_coord[1] <= sq_c_chk + 1:
                          is_target_part_of_sq = True
                          break
                 if not is_target_part_of_sq:
                    chosen_target = target_coord
                    break # Found the best available target

        # 4f. Place the SingletonDigit's value in the output grid if a target was found
        if chosen_target:
            r_target, c_target = chosen_target
            output_grid[r_target][c_target] = value
            processed_targets.add(chosen_target) # Mark this cell as claimed
        # else:
            # print(f"Warning: Could not place singleton {value} from ({r_orig}, {c_orig}) as all preferred adjacent cells were taken or invalid.")


    # 5. Return the completed output grid
    return output_grid

```