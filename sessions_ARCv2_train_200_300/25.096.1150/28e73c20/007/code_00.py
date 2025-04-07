import random
import numpy as np # Using numpy for convenience but stick to list-of-lists if required

"""
Generates a specific, deterministic perfect maze pattern within a grid for 
a given size N, represented by '0' for paths and '3' for walls.

The transformation follows these steps:
1.  Initialize an N x N output grid filled entirely with the wall character '3'.
2.  Seed the random number generator with a fixed value (e.g., 0) to ensure 
    deterministic maze generation.
3.  Apply a maze generation algorithm (Randomized Depth-First Search - DFS) 
    to the inner grid area (rows 1 to N-2, columns 1 to N-2).
    a. Start carving paths (changing '3' to '0') from cell (1, 1).
    b. Use a stack to manage the DFS traversal.
    c. Iteratively move to unvisited neighboring cells (2 steps away), carving 
       the wall between the current cell and the neighbor. The choice of 
       neighbor is determined by the seeded random number generator.
    d. Backtrack when a dead end is reached.
4.  Create an entrance at (1, 0) and an exit at (N-2, 0) by setting these 
    cells to the path character '0'.
5.  The final grid contains the specific maze structure determined by the 
    grid size N and the fixed seed.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Generates a deterministic maze structure within the input grid dimensions.

    Args:
        input_grid: An N x N list of lists containing only 0s.

    Returns:
        An N x N list of lists representing the specific maze for that N, 
        with 0s for paths and 3s for walls.
    """
    # --- Get grid dimensions ---
    n = len(input_grid)
    if n == 0:
        return []
    # Assuming square grid based on examples
    m = len(input_grid[0]) 
    if n != m:
         raise ValueError("Input grid must be square") 

    # --- Step 1: Initialize output_grid with walls (3) ---
    output_grid = [[3 for _ in range(n)] for _ in range(n)]

    # --- Handle edge cases: grids too small for standard maze structure ---
    # Examples start at N=6. Need N>=5 for a 1x1 inner carving area.
    if n < 5: 
        # Still create openings if possible based on the pattern N>=3
        if n >= 3: 
             if 1 < n: output_grid[1][0] = 0 # Entrance at (1,0)
             # Exit at (N-2,0), ensuring it's a valid index and different from entrance row
             if (n-2) >= 1 and (n-2) != 1 : output_grid[n-2][0] = 0 
        # Return the grid with just boundary walls and potential openings
        return output_grid 

    # --- Step 2: Maze Carving (Deterministic DFS) in the inner grid ---
    
    # CRUCIAL STEP: Seed the random number generator for deterministic results
    # Using seed=0 as a common starting point hypothesis
    random.seed(0) 
    
    # Define inner grid boundaries (inclusive) for carving
    inner_r_min, inner_r_max = 1, n - 2
    inner_c_min, inner_c_max = 1, n - 2

    # Stack for DFS: stores (row, col) tuples
    stack = []
    
    # Start DFS from a fixed point within the inner grid, e.g., (1, 1)
    start_r, start_c = 1, 1
    output_grid[start_r][start_c] = 0  # Mark starting cell as path
    stack.append((start_r, start_c))
    
    # The 'visited' status is implicitly tracked by checking if output_grid[nr][nc] is 0 or 3

    while stack:
        # Get the current cell from the top of the stack
        current_r, current_c = stack[-1] 

        # Find potential valid neighbors (2 steps away, within inner grid, still a wall)
        neighbors = []
        # Define possible moves (2 steps horizontally or vertically)
        possible_moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        # Shuffle moves using the seeded RNG to ensure deterministic order if multiple valid neighbors exist
        random.shuffle(possible_moves) 
        
        for dr, dc in possible_moves:
            nr, nc = current_r + dr, current_c + dc

            # Check if the potential neighbor (nr, nc) is:
            # 1. Within the inner grid bounds
            # 2. Still a wall (output_grid[nr][nc] == 3)
            if (inner_r_min <= nr <= inner_r_max and
                inner_c_min <= nc <= inner_c_max and
                output_grid[nr][nc] == 3):
                neighbors.append((nr, nc)) # Keep track of valid neighbors found in the shuffled order

        if neighbors:
            # If there are valid unvisited neighbors, choose the first one found
            # (due to the deterministic shuffle, this choice is now deterministic)
            next_r, next_c = neighbors[0] # Changed from random.choice to deterministic selection

            # Calculate the coordinates of the wall cell between current and neighbor
            wall_r, wall_c = (current_r + next_r) // 2, (current_c + next_c) // 2

            # Carve the path: set the wall cell and the neighbor cell to 0
            output_grid[wall_r][wall_c] = 0
            output_grid[next_r][next_c] = 0

            # Add the chosen neighbor to the stack to continue DFS from there
            stack.append((next_r, next_c))
        else:
            # If no unvisited neighbors (dead end), backtrack
            stack.pop()

    # --- Step 3: Create Entrance and Exit on the left boundary ---
    # Indices are valid because we checked n >= 5 earlier
    output_grid[1][0] = 0      # Set entrance at (1, 0)
    output_grid[n - 2][0] = 0  # Set exit at (n-2, 0)

    # --- Step 4: Final Output ---
    return output_grid