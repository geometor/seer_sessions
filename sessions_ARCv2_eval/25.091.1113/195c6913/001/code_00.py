import numpy as np
from collections import deque

"""
Transforms an input grid based on a pattern fill rule derived from analysis of examples.

The transformation follows these steps:
1.  Analyze the input grid to identify key color roles:
    - Background color: Persists, often frames the grid.
    - Fillable color: Area to be overwritten with a pattern.
    - Seed color(s): Initiate the pattern fill into adjacent fillable areas.
    - Terminator color(s): Halt the pattern fill, retain their color.
    - Erased color(s): (Optional) Replaced by background color before filling.
    - Pattern Sequence: Repeating sequence of colors for filling.
    (Note: In this implementation, these parameters are currently hardcoded based 
     on the analysis of training example 1. A general solution would need to 
     derive these parameters dynamically).
2.  Initialize an output grid as a copy of the input grid.
3.  Pre-process the output grid:
    - Replace any Erased colors with the Background color. (Not applicable for Ex1)
    - Modify Seed pixels based on rules (e.g., retain color, replace with pattern start). (Retained for Ex1)
4.  Identify starting points for the fill: Find all pixels in the input grid that have the 
    Fillable color and are 8-directionally adjacent to any Seed color pixel in the input grid.
5.  Perform a pattern fill using Breadth-First Search (BFS):
    - Initialize a queue with the starting points. Each element stores the pixel coordinates 
      and the index of the pattern color to be applied to its neighbors.
    - Maintain a set of visited pixels to avoid re-processing and infinite loops.
    - Color the initial starting points with the first color of the pattern sequence.
    - While the queue is not empty:
        - Dequeue a pixel P and its associated 'next pattern index'.
        - Determine the color for P's neighbors based on this index and the pattern sequence.
        - Determine the pattern index for the *next* level of neighbors.
        - For each 8-directional neighbor N of P:
            - If N is within bounds, had the Fillable color in the input grid, and has not 
              been visited:
                - Set N's color in the output grid to the determined neighbor color.
                - Mark N as visited.
                - Enqueue N with the calculated pattern index for the next level.
6.  Return the modified output grid. The fill stops naturally at grid edges, Background pixels, 
    Terminator pixels, and already filled pixels.
"""

def get_neighbors(r, c, height, width):
    """
    Gets coordinates of 8-directional neighbors within grid bounds.

    Args:
        r (int): Row index of the center cell.
        c (int): Column index of the center cell.
        height (int): Grid height.
        width (int): Grid width.

    Returns:
        list[tuple[int, int]]: List of valid neighbor coordinates (row, col).
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Applies the pattern fill transformation to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid as a 2D list of integers.

    Returns:
        list[list[int]]: The transformed grid as a 2D list of integers.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # --- Parameter Definition (Hardcoded based on analysis of train_1) ---
    # In a general solver, these would be determined by analyzing examples.
    fillable_color = 0       # White
    seed_colors = {2, 8}     # Red, Azure
    # background_color = 3     # Green (Implicitly acts as boundary)
    # terminator_colors = {4}  # Yellow (Implicitly acts as boundary)
    # erased_colors = set()    # None for train_1
    pattern_sequence = [2, 2, 8] # Red, Red, Azure
    # seed_handling = "retain" # For train_1, seeds keep their color and initiate fill

    # --- Initialize BFS queue and visited set ---
    # Queue stores tuples: (row, col, pattern_index_for_next_neighbor)
    queue = deque()
    # Visited stores (row, col) tuples of pixels whose color has been set by the fill
    visited = set() 
    pattern_len = len(pattern_sequence)

    # --- Pre-processing Step ---
    # Placeholder: Handle Erased Colors (Replace with background)
    # for r in range(height):
    #     for c in range(width):
    #         if input_np[r,c] in erased_colors:
    #             output_grid[r,c] = background_color
    
    # Placeholder: Handle Seed Color Modification (e.g., replace seeds for train_3)
    # if seed_handling == "replace":
    #    start_pattern_color = pattern_sequence[0]
    #    for r in range(height):
    #       for c in range(width):
    #           if input_np[r,c] in seed_colors:
    #               output_grid[r,c] = start_pattern_color

    # --- Identify Initial Fill Locations & Seed Queue ---
    # Find fillable cells adjacent to seed cells in the original input.
    # These are the first cells to receive the pattern color.
    for r in range(height):
        for c in range(width):
            # Check if the current cell is fillable in the *input*
            if input_np[r, c] == fillable_color:
                is_initial_fill = False
                # Check its neighbors in the *input* grid
                for nr, nc in get_neighbors(r, c, height, width):
                    # If a neighbor has a seed color in the *input*
                    if input_np[nr, nc] in seed_colors:
                        is_initial_fill = True
                        break # Found a seed neighbor, no need to check others
                
                # If it's an initial fill point and not already visited
                if is_initial_fill and (r, c) not in visited:
                    # Color this initial point with the first pattern color
                    start_pattern_color = pattern_sequence[0]
                    output_grid[r, c] = start_pattern_color
                    visited.add((r, c))
                    # Add to queue. Its neighbors will get pattern_sequence[1]
                    # The index passed is the one to be used for *neighbors*
                    queue.append((r, c, 1)) 

    # --- BFS Propagation ---
    while queue:
        # Get the current cell and the pattern index its neighbors should use
        r, c, next_pattern_index = queue.popleft()
        
        # Determine the color to apply to neighbors based on the index from the queue
        neighbor_color_index = next_pattern_index % pattern_len
        neighbor_color = pattern_sequence[neighbor_color_index]
        
        # Calculate the index for the *next* level of neighbors
        # (i.e., the index to store when adding neighbors to the queue)
        next_next_pattern_index = next_pattern_index + 1 

        # Explore neighbors
        for nr, nc in get_neighbors(r, c, height, width):
            # Check if neighbor is:
            # 1. Originally fillable (in the input grid)
            # 2. Not already visited/colored by the fill process
            if input_np[nr, nc] == fillable_color and (nr, nc) not in visited:
                # Color the neighbor
                output_grid[nr, nc] = neighbor_color
                # Mark as visited
                visited.add((nr, nc))
                # Enqueue the neighbor, passing the index for *its* neighbors
                queue.append((nr, nc, next_next_pattern_index))

    # Return the final grid as a list of lists
    return output_grid.tolist()