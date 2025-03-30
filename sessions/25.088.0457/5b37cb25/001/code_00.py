import numpy as np
from collections import deque, Counter

"""
Propagates colors from the four sides of a 1-pixel border inwards into an enclosed area.
The propagation starts from the pixels immediately inside the border.
Propagation moves one step orthogonally inwards per iteration (like a breadth-first search).
If a propagation wave encounters a pixel of a pre-identified 'obstacle' color, it colors that obstacle pixel but does not propagate further past it along that path.
If propagation waves from different borders reach the same pixel in the same step, the pixel takes the color of the wave that originated from the border corresponding to the processing order (Top, Right, Bottom, Left). In practice, the first wave to claim a pixel prevents others from claiming it.
Pixels that are not reached by any propagation wave (e.g., behind obstacles) retain their original color.
The border itself remains unchanged.
"""

def find_obstacle_color(grid, border_colors):
    """Identifies the obstacle color within the inner area."""
    h, w = grid.shape
    if h <= 2 or w <= 2: # No inner area
        return None
        
    inner_grid = grid[1:h-1, 1:w-1]
    unique_colors, counts = np.unique(inner_grid, return_counts=True)
    
    if len(unique_colors) == 0:
        return None # Empty inner grid

    # Exclude border colors from potential obstacle colors
    border_colors_set = set(border_colors)
    
    # Find the most frequent color, assume it's background
    # Handle cases where inner grid might be uniform (no obstacles)
    if len(unique_colors) == 1:
         return None # Only one color inside, no obstacles
         
    # Find potential background color (most frequent)
    # Need to ignore colors that might be border colors spilling in initial state if they match background
    possible_bg_candidates = {}
    for color, count in zip(unique_colors, counts):
         possible_bg_candidates[color] = count

    # Remove border colors from candidates *if they exist*
    for bc in border_colors_set:
        if bc in possible_bg_candidates:
             # Don't assume a border color IS the background if it's infrequent
             # Heuristic: If a border color is the most frequent, it's likely background
             # If not, it's unlikely background. Let's refine this.
             pass # Keep border colors for now, let frequency decide background

    if not possible_bg_candidates:
        # This happens if the inner grid only contained border colors
        return None 

    background_color = max(possible_bg_candidates, key=possible_bg_candidates.get)

    # Obstacle is a color in the inner grid that is NOT the background and NOT a border color
    obstacle_color = None
    for color in unique_colors:
        if color != background_color: #and color not in border_colors_set:
             # Let's rethink: the obstacle color is defined *before* propagation.
             # It's simply the non-background color present initially.
             # What if multiple non-background colors exist? The examples only show one.
             # Assume only one type of obstacle color exists besides background.
             obstacle_color = color
             break # Found the first non-background color, assume it's the obstacle

    # Check if the found 'obstacle' color is actually one of the border colors
    # This can happen if the example shows a border color already present inside
    # In train_1, obstacle is 6, borders are 3, 2, 4, 8. Bg=1. OK.
    # In train_2, obstacle is 2, borders are 1, 8, 6, 3. Bg=4. OK.
    # If the identified non-background color IS a border color, then there are no obstacles
    # of a distinct color.
    if obstacle_color in border_colors_set:
        return None # No distinct obstacle color found

    return obstacle_color


def transform(input_grid):
    """
    Applies the border color propagation transformation.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    h, w = grid.shape

    # Handle grids too small to have an inner area
    if h <= 2 or w <= 2:
        return output_grid.tolist()

    # 1. Identify border colors (assuming 1-pixel border)
    # Added checks for grid size > 1 in that dimension
    top_color = grid[0, 1] if w > 1 else grid[0,0]
    right_color = grid[1, w - 1] if h > 1 else grid[0, w-1]
    bottom_color = grid[h - 1, 1] if w > 1 else grid[h-1, 0]
    left_color = grid[1, 0] if h > 1 else grid[0, 0]
    border_colors = [top_color, right_color, bottom_color, left_color] # Order matters: T, R, B, L

    # 2. Identify the obstacle color
    obstacle_color = find_obstacle_color(grid, border_colors)
    # print(f"Obstacle color identified as: {obstacle_color}") # Debug

    # 3. Initialize BFS structures
    # source_grid stores the index of the border color (0=T, 1=R, 2=B, 3=L) that claimed the pixel
    source_grid = np.full_like(grid, -1, dtype=int)
    
    q_top = deque()
    q_right = deque()
    q_bottom = deque()
    q_left = deque()
    queues = [q_top, q_right, q_bottom, q_left]

    # 4. Initialize queues with pixels just inside each border
    # Top border initialization
    for c in range(1, w - 1):
        r = 1
        if source_grid[r, c] == -1:
            source_grid[r, c] = 0 # 0 for Top
            q_top.append((r, c))
            
    # Right border initialization
    for r in range(1, h - 1):
        c = w - 2
        if source_grid[r, c] == -1:
             source_grid[r, c] = 1 # 1 for Right
             q_right.append((r, c))

    # Bottom border initialization
    for c in range(1, w - 1):
        r = h - 2
        if source_grid[r, c] == -1:
             source_grid[r, c] = 2 # 2 for Bottom
             q_bottom.append((r, c))

    # Left border initialization
    for r in range(1, h - 1):
        c = 1
        if source_grid[r, c] == -1:
             source_grid[r, c] = 3 # 3 for Left
             q_left.append((r, c))

    # 5. Perform simultaneous BFS, layer by layer
    while any(queues):
        next_q_top = deque()
        next_q_right = deque()
        next_q_bottom = deque()
        next_q_left = deque()
        next_queues = [next_q_top, next_q_right, next_q_bottom, next_q_left]

        # Process Top queue expansion (downwards)
        while q_top:
            r, c = q_top.popleft()
            nr, nc = r + 1, c
            # Check bounds and if already claimed
            if 1 <= nr < h - 1 and 1 <= nc < w - 1 and source_grid[nr, nc] == -1:
                source_grid[nr, nc] = 0 # Claimed by Top
                # Check if the target pixel is NOT an obstacle before adding to next queue
                if grid[nr, nc] != obstacle_color:
                    next_q_top.append((nr, nc))

        # Process Right queue expansion (leftwards)
        while q_right:
            r, c = q_right.popleft()
            nr, nc = r, c - 1
            if 1 <= nr < h - 1 and 1 <= nc < w - 1 and source_grid[nr, nc] == -1:
                source_grid[nr, nc] = 1 # Claimed by Right
                if grid[nr, nc] != obstacle_color:
                     next_q_right.append((nr, nc))

        # Process Bottom queue expansion (upwards)
        while q_bottom:
            r, c = q_bottom.popleft()
            nr, nc = r - 1, c
            if 1 <= nr < h - 1 and 1 <= nc < w - 1 and source_grid[nr, nc] == -1:
                 source_grid[nr, nc] = 2 # Claimed by Bottom
                 if grid[nr, nc] != obstacle_color:
                     next_q_bottom.append((nr, nc))

        # Process Left queue expansion (rightwards)
        while q_left:
            r, c = q_left.popleft()
            nr, nc = r, c + 1
            if 1 <= nr < h - 1 and 1 <= nc < w - 1 and source_grid[nr, nc] == -1:
                source_grid[nr, nc] = 3 # Claimed by Left
                if grid[nr, nc] != obstacle_color:
                     next_q_left.append((nr, nc))

        # Update queues for the next layer
        queues = next_queues
        q_top, q_right, q_bottom, q_left = queues

    # 6. Apply the colors based on the source grid
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            source_index = source_grid[r, c]
            if source_index != -1: # If the pixel was claimed
                output_grid[r, c] = border_colors[source_index]

    return output_grid.tolist()