
Previous Code:
```python
import numpy as np
from collections import deque, Counter

def find_inner_colors(grid):
    """
    Analyzes the inner area (excluding the 1-pixel border) of the grid 
    to find the background color (most frequent) and the obstacle color 
    (assumed to be the single other color present, if any).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (background_color, obstacle_color)
               Returns (None, None) if the inner area is empty or cannot be analyzed.
               Obstacle color is None if only one color is present in the inner area.
    """
    h, w = grid.shape
    # Ensure there's an inner area to analyze
    if h <= 2 or w <= 2:
        return None, None 
        
    inner_grid = grid[1:h-1, 1:w-1]
    
    # Check if inner grid is actually empty after slicing
    if inner_grid.size == 0:
        return None, None

    colors, counts = np.unique(inner_grid, return_counts=True)
    
    if len(colors) == 0: 
         return None, None # Should not happen if size > 0, but safety check
         
    if len(colors) == 1:
        # Only one color found, it's the background, no obstacles
        background_color = colors[0]
        obstacle_color = None
    else:
        # Multiple colors found, assume background is the most frequent
        count_map = dict(zip(colors, counts))
        background_color = max(count_map, key=count_map.get)
        # Assume the first color encountered that isn't background is the obstacle
        obstacle_color = None
        for color in colors:
             if color != background_color:
                 obstacle_color = color
                 break # Assuming only one type of obstacle color based on examples
                 
    return background_color, obstacle_color

def transform(input_grid_list):
    """
    Propagates colors from the four sides of a 1-pixel border inwards into an 
    enclosed area. The propagation starts from background pixels immediately 
    inside the border and moves orthogonally inwards, layer by layer (BFS). 
    
    Propagation Rules:
    1. Only overwrites pixels that initially had the 'background_color'.
    2. 'background_color' is the most frequent color in the initial inner area.
    3. 'obstacle_color' is any other color initially present in the inner area.
    4. Pixels with the 'obstacle_color' block propagation and remain unchanged.
    5. Pixels retain their original color if not reached by propagation (e.g., shielded 
       background pixels or original obstacle pixels).
    6. The 1-pixel border itself remains unchanged.
    7. If propagation waves from different directions reach the same pixel in the 
       same step (layer), the conflict is resolved by processing order: 
       Top -> Right -> Bottom -> Left. The first wave to claim the pixel colors it.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = input_grid.copy()
    h, w = input_grid.shape

    # --- 1. Handle edge case: grid too small for an inner area ---
    if h <= 2 or w <= 2:
        # No inner area to propagate into, return the original grid
        return output_grid.tolist()

    # --- 2. Identify Grid Elements ---
    # Get border colors, handling potential 1xN or Nx1 grids where some sides are just corners
    # Default to the corner color if a side doesn't exist (e.g., grid[0,1] in a Hx1 grid)
    top_color = input_grid[0, 1] if w > 1 else input_grid[0, 0]
    right_color = input_grid[1, w - 1] if h > 1 else input_grid[0, w-1]
    bottom_color = input_grid[h - 1, 1] if w > 1 else input_grid[h-1, 0]
    left_color = input_grid[1, 0] if h > 1 else input_grid[0, 0]
    # Store border colors in the processing order for collision resolution
    border_colors = [top_color, right_color, bottom_color, left_color] # Order: T, R, B, L

    # Find background and potential obstacle color in the inner area
    background_color, obstacle_color = find_inner_colors(input_grid)
    
    # If the inner area couldn't be analyzed (e.g., completely empty somehow)
    # or if there's no background color to propagate onto, return the original.
    if background_color is None: 
         return output_grid.tolist() 

    # --- 3. Setup Propagation Structures ---
    q_top = deque()
    q_right = deque()
    q_bottom = deque()
    q_left = deque()
    # Queues store tuples: (row, column)
    queues = [q_top, q_right, q_bottom, q_left] 
    
    # Create a mask to track which pixels have been colored by propagation.
    # Initialize all to True (cannot be colored).
    colored_mask = np.ones_like(input_grid, dtype=bool) 
    # Set the inner area to False (can potentially be colored).
    colored_mask[1:h-1, 1:w-1] = False 

    # --- 4. Seed Propagation from Inner Border ---
    # Iterate through pixels just inside each border. If a pixel is the 
    # background color and hasn't been colored yet (important for corners where
    # seeding waves might overlap), color it, mark it, and add to the queue.
    # Process in T, R, B, L order for deterministic seeding at corners.
    
    # Top seed (propagate downwards)
    r_seed_top = 1
    for c in range(1, w - 1):
        if input_grid[r_seed_top, c] == background_color and not colored_mask[r_seed_top, c]:
            output_grid[r_seed_top, c] = top_color
            colored_mask[r_seed_top, c] = True
            q_top.append((r_seed_top, c))

    # Right seed (propagate leftwards)
    c_seed_right = w - 2
    for r in range(1, h - 1):
         if input_grid[r, c_seed_right] == background_color and not colored_mask[r, c_seed_right]:
            output_grid[r, c_seed_right] = right_color
            colored_mask[r, c_seed_right] = True
            q_right.append((r, c_seed_right))
            
    # Bottom seed (propagate upwards)
    r_seed_bottom = h - 2
    for c in range(1, w - 1):
         if input_grid[r_seed_bottom, c] == background_color and not colored_mask[r_seed_bottom, c]:
            output_grid[r_seed_bottom, c] = bottom_color
            colored_mask[r_seed_bottom, c] = True
            q_bottom.append((r_seed_bottom, c))

    # Left seed (propagate rightwards)
    c_seed_left = 1
    for r in range(1, h - 1):
         if input_grid[r, c_seed_left] == background_color and not colored_mask[r, c_seed_left]:
            output_grid[r, c_seed_left] = left_color
            colored_mask[r, c_seed_left] = True
            q_left.append((r, c_seed_left))

    # --- 5. Iterative Propagation (Simultaneous BFS Layer by Layer) ---
    while any(queues): # Continue as long as any queue has nodes for the next layer
        # Prepare queues for the *next* layer of propagation
        next_q_top = deque()
        next_q_right = deque()
        next_q_bottom = deque()
        next_q_left = deque()
        next_queues = [next_q_top, next_q_right, next_q_bottom, next_q_left]

        # Process propagation for the current layer, in T, R, B, L order
        
        # Top queue expands downwards
        while q_top:
            r, c = q_top.popleft()
            nr, nc = r + 1, c # Neighbor coordinates
            # Check: neighbor within inner bounds? Is neighbor originally background? Not already colored?
            if 1 <= nr < h - 1 and input_grid[nr, nc] == background_color and not colored_mask[nr, nc]:
                output_grid[nr, nc] = top_color   # Color the neighbor
                colored_mask[nr, nc] = True       # Mark as colored
                next_q_top.append((nr, nc))       # Add to next layer's queue

        # Right queue expands leftwards
        while q_right:
            r, c = q_right.popleft()
            nr, nc = r, c - 1
            if 1 <= nc < w - 1 and input_grid[nr, nc] == background_color and not colored_mask[nr, nc]:
                 output_grid[nr, nc] = right_color
                 colored_mask[nr, nc] = True
                 next_q_right.append((nr, nc))

        # Bottom queue expands upwards
        while q_bottom:
            r, c = q_bottom.popleft()
            nr, nc = r - 1, c
            if 1 <= nr < h - 1 and input_grid[nr, nc] == background_color and not colored_mask[nr, nc]:
                 output_grid[nr, nc] = bottom_color
                 colored_mask[nr, nc] = True
                 next_q_bottom.append((nr, nc))

        # Left queue expands rightwards
        while q_left:
            r, c = q_left.popleft()
            nr, nc = r, c + 1
            if 1 <= nc < w - 1 and input_grid[nr, nc] == background_color and not colored_mask[nr, nc]:
                 output_grid[nr, nc] = left_color
                 colored_mask[nr, nc] = True
                 next_q_left.append((nr, nc))

        # Move to the next layer
        queues = next_queues
        q_top, q_right, q_bottom, q_left = queues

    # --- 6. Return the final grid ---
    # The output_grid now contains the original border, original obstacles, 
    # original background pixels that were shielded, and the newly colored pixels.
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 1 1 1 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 1 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 6 1 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 1 1 1 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 1 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 6 6 6 6 6 6 6 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 6 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 6 1 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 1 1 1 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
```
Expected Output:
```
0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 3 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 3 3 3 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 3 6 6 6 6 6 6 6 6 2 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 6 6 2 2 2 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 6 6 6 2 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 6 4 6 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 6 6 6 4 4 4 6 6 6 1 1 1 1 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1 1 2
8 1 8 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 8 8 8 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 8 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 2 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 2 2 2 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 8 6 6 6 6 6 6 6 2 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 8 8 8 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 6 6 6 6 6 6 6 6 1 1 1 1 1 8 6 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 6 4 6 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 6 6 6 4 4 4 6 6 6 6 6 1 1 1 1 1 6 6 6 6 6 6 6 6 6 1 1 2
8 1 1 1 1 1 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
```
Transformed Output:
```
0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0
8 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2
8 8 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 2
8 8 6 6 6 6 3 3 3 6 6 6 6 6 6 6 6 3 3 3 3 3 3 3 3 3 3 2 2 2
8 8 6 6 6 6 6 3 6 6 6 6 6 6 6 6 1 3 3 3 3 3 3 3 3 3 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 6 6 1 1 3 3 3 3 3 3 3 3 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 3 3 3 3 3 3 3 2 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 3 3 3 3 3 3 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 3 3 3 3 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 6 6 6 6 6 6 6 6 2 2 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 6 6 6 6 6 6 6 6 6 2 2 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 6 6 6 6 6 6 6 6 6 2 2 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 6 6 6 6 1 6 6 6 6 2 2 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 6 6 6 1 1 1 6 6 6 2 2 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 6 6 6 6 6 6 6 6 6 6 4 4 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 6 6 6 6 6 6 6 6 6 4 4 4 4 4 6 6 6 6 6 6 6 6 6 2 2 2
8 8 8 6 6 6 6 6 6 6 6 6 6 4 4 4 4 4 6 6 6 6 6 6 6 6 6 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 4 4 4 4 6 6 6 6 6 6 6 6 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 4 4 4 4 6 6 6 6 6 6 6 2 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 4 4 4 4 1 6 6 6 6 6 6 6 2 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 4 4 4 4 1 1 6 6 6 6 6 6 6 2 2 2
8 8 6 6 6 6 6 6 6 6 6 6 6 4 4 4 4 4 1 6 6 6 6 6 6 6 6 2 2 2
8 8 6 6 6 6 4 6 6 6 6 6 6 4 4 4 4 4 6 6 6 6 6 6 6 6 6 2 2 2
8 8 6 6 6 4 4 4 6 6 6 6 6 4 4 4 4 4 6 6 6 6 6 6 6 6 6 2 2 2
8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2
8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2
8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
```
Match: False
Pixels Off: 426
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 94.66666666666667

## Example 2:
Input:
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 2 2 2 2 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 4 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 4 4 4 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
```
Expected Output:
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
3 4 4 4 4 4 4 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 2 2 2 1 1 1 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 2 2 2 2 1 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 3 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 3 3 3 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 3 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 6 2 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 6 6 6 2 2 2 2 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
3 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
```
Transformed Output:
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
3 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8
3 3 1 2 2 2 1 1 1 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
3 3 3 2 2 2 2 1 2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 4 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 4 4 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 4 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 2 2 2 2 2 2 2 2 2 2 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 1 1 2 2 2 2 2 2 2 2 2 2 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 3 6 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 6 6 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 6 6 6 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 6 6 6 6 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 3 6 6 6 6 6 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 3 6 6 6 6 6 6 6 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
3 3 3 3 3 6 6 6 6 6 6 6 6 2 2 2 2 6 2 2 2 2 2 6 8 8 8 8 8 8
3 3 3 3 6 6 6 6 6 6 6 6 6 2 2 2 6 6 6 2 2 2 2 6 6 8 8 8 8 8
3 3 3 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 8 8 8 8
3 3 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 8 8 8
3 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 8 8
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
```
Match: False
Pixels Off: 486
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 108.0
