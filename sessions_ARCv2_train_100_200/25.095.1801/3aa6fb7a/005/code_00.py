import copy

"""
Transforms an input grid based on the following rules:
1. Create a new grid (output grid) identical in dimensions to the input grid.
2. Iterate through each cell (identified by `row` and `col`) of the input grid.
3. Get the value of the current cell (`input_value = input_grid[row][col]`).
4. **Rule 1: Handle '8's:** If `input_value` is 8, set the corresponding cell in the output grid to 8 (`output_grid[row][col] = 8`).
5. **Rule 2: Handle '0's:** If `input_value` is 0:
   a. Find the coordinates of all neighboring cells (up to 8) that have a value of 8 in the input grid.
   b. Count the number of these '8' neighbors (`count_8`).
   c. **Check Condition 1:** Is `count_8` exactly equal to 3?
   d. **Check Condition 2 (if Condition 1 is true):** Are the three '8' neighbors mutually adjacent? (Check if neighbor1 is adjacent to neighbor2 AND neighbor1 is adjacent to neighbor3 AND neighbor2 is adjacent to neighbor3).
   e. **Apply Transformation:** If both Condition 1 (count is 3) and Condition 2 (mutual adjacency) are true, set the corresponding cell in the output grid to 1 (`output_grid[row][col] = 1`).
   f. **Default for '0's:** Otherwise (if `input_value` is 0 but either condition is false), set the corresponding cell in the output grid to 0 (`output_grid[row][col] = 0`).
6. After iterating through all cells, return the completed output grid.
"""

def is_adjacent(coord1: tuple[int, int], coord2: tuple[int, int]) -> bool:
    """Checks if two coordinates are adjacent (horizontally, vertically, or diagonally)."""
    r1, c1 = coord1
    r2, c2 = coord2
    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

def check_mutual_adjacency(coords: list[tuple[int, int]]) -> bool:
    """Checks if three coordinates are all mutually adjacent."""
    if len(coords) != 3:
        # This function assumes exactly 3 coordinates
        return False 
        
    c1, c2, c3 = coords
    
    # Check adjacency between all pairs
    adj12 = is_adjacent(c1, c2)
    adj13 = is_adjacent(c1, c3)
    adj23 = is_adjacent(c2, c3)
    
    return adj12 and adj13 and adj23

def get_neighbors_with_value(grid: list[list[int]], r: int, c: int, target_value: int) -> list[tuple[int, int]]:
    """Finds coordinates of neighbors of cell (r, c) with the target_value."""
    rows = len(grid)
    cols = len(grid[0])
    neighbor_coords = []
    # Iterate through the 8 possible neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == target_value:
                    neighbor_coords.append((nr, nc))
    return neighbor_coords

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of the input grid.
    # This handles Rule 1 (8s stay 8s) and the default case for 0s (0s stay 0s).
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Get the value of the current cell in the *input* grid
            input_value = input_grid[r][c]

            # Check if the input cell's value is 0 (Rule 2)
            if input_value == 0:
                # Find neighbors with value 8 in the input grid
                neighbors_8_coords = get_neighbors_with_value(input_grid, r, c, 8)
                
                # Check Condition 1: Count is exactly 3
                if len(neighbors_8_coords) == 3:
                    # Check Condition 2: Mutual adjacency of the three neighbors
                    if check_mutual_adjacency(neighbors_8_coords):
                        # Apply Transformation: Change cell to 1 in the output grid
                        output_grid[r][c] = 1
            # If input_value is 8, output_grid[r][c] is already 8 from the deepcopy.
            # If input_value is 0 and conditions are not met, output_grid[r][c] is already 0 from the deepcopy.

    # Return the completed output grid
    return output_grid