```python
"""
Identifies three distinct colors in the input grid: a background color (most frequent), 
a seed color (unique occurrence), and a boundary color. Performs a flood fill starting 
from the seed pixel's location, replacing the background color with the seed color. 
The fill is bounded by pixels of the boundary color and the grid edges. Pixels with 
the boundary color and pixels outside the fill area remain unchanged.
"""

import numpy as np
from collections import Counter, deque

def transform(input_grid):
    """
    Applies a bounded flood fill transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Get grid dimensions
    height, width = input_grid.shape

    # --- Identify Colors ---
    
    # Count occurrences of each color
    color_counts = Counter(input_grid.flatten())
    
    # Find the background color (most frequent)
    background_color = color_counts.most_common(1)[0][0]
    
    # Find the seed color and location (appears only once)
    seed_color = -1
    seed_loc = None
    unique_colors = [color for color, count in color_counts.items() if count == 1]
    
    # There should be exactly one unique color which is the seed
    if len(unique_colors) == 1:
        seed_color = unique_colors[0]
        # Find its location
        seed_indices = np.where(input_grid == seed_color)
        if len(seed_indices[0]) == 1: # Should always be true if count is 1
             seed_loc = (seed_indices[0][0], seed_indices[1][0])
        else:
             # This case shouldn't happen based on the logic but added for robustness
             raise ValueError("Seed color found multiple times despite unique count.")
    else:
        # Handle cases where assumption of one unique color fails
        # Could try other heuristics, but based on examples, this holds.
        # For now, raise an error if the assumption doesn't fit.
        # A possible fallback: check if there's a color surrounded by background? 
        # Or check if exactly 3 colors exist and pick the one not most frequent?
        # Trying the 3-color heuristic:
        if len(color_counts) == 3:
            all_colors = set(color_counts.keys())
            possible_boundary = list(all_colors - {background_color})
            # Often the boundary color count > seed color count. 
            # Assuming seed is the least frequent non-background.
            counts_sorted = sorted([(count, color) for color, count in color_counts.items()])
            if counts_sorted[0][0] == 1: # If the least frequent has count 1, it's the seed.
                 seed_color = counts_sorted[0][1]
                 seed_indices = np.where(input_grid == seed_color)
                 seed_loc = (seed_indices[0][0], seed_indices[1][0])
            else:
                # If no unique color, maybe the single pixel is the same as boundary? Unlikely in ARC.
                # Or maybe the 'seed' point is actually the boundary color? Example 1 contradicts this.
                # Fallback needed or rethink assumptions if this path is hit.
                # For now, stick to the unique color assumption seems safest based on examples.
                raise ValueError("Could not definitively identify a unique seed color.")
        else:
             raise ValueError(f"Expected 3 distinct colors or 1 unique seed color, found {len(color_counts)}.")


    # Find the boundary color (the one that's not background or seed)
    boundary_color = -1
    for color in color_counts.keys():
        if color != background_color and color != seed_color:
            boundary_color = color
            break
            
    if boundary_color == -1:
        # This might happen if there are only 2 colors (e.g., background and seed, no boundary)
        # Or if the logic above failed. Handle or raise error.
        # Based on examples, 3 colors are present.
         raise ValueError("Could not identify a distinct boundary color.")

    # --- Perform Flood Fill ---
    
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Queue for BFS flood fill, starting with the seed location
    queue = deque([seed_loc])
    
    # Set to keep track of visited cells to avoid cycles and redundant work
    visited = set()
    visited.add(seed_loc) # Add seed location initially

    # Perform the fill
    while queue:
        r, c = queue.popleft()
        
        # The seed location itself should adopt the seed color (it already does, but conceptually important)
        # Change background pixels connected to the seed to the seed color
        if input_grid[r, c] == background_color or (r,c) == seed_loc:
             output_grid[r, c] = seed_color

        # Explore neighbors (cardinal directions: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_loc = (nr, nc)
                
                # Check if already visited
                if neighbor_loc in visited:
                    continue
                    
                # Check if neighbor is a boundary pixel (stop condition)
                if input_grid[nr, nc] == boundary_color:
                    continue # Don't add boundary pixels to queue, don't visit them
                    
                # If the neighbor is valid (within bounds, not boundary, not visited),
                # add it to visited set and the queue for processing.
                visited.add(neighbor_loc)
                queue.append(neighbor_loc)

    return output_grid
```