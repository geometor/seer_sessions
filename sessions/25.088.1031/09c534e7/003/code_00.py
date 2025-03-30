import numpy as np
from collections import deque

"""
Transformation Rule Description:

The transformation identifies non-background (white, 0) and non-primary shape (blue, 1) pixels, referred to as "seed" pixels. For each seed pixel, it identifies any adjacent blue pixels (4-way adjacency). For each such adjacent blue pixel that hasn't already been colored by a previous seed's operation, it performs a flood fill (BFS) starting from that blue pixel. This flood fill propagates only through contiguous blue pixels in the original input grid that have not yet been colored. All blue pixels reached by this specific flood fill operation are changed to the color of the originating seed in the output grid. Once a blue pixel is colored, it cannot be colored again by another seed's operation. Background pixels and the original seed pixels remain unchanged.
"""

def find_seeds(grid):
    """Finds seed pixels (non-white, non-blue) in the grid."""
    seeds = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Seeds are pixels that are not background (0) and not the primary shape color (1)
            if color != 0 and color != 1:
                seeds.append(((r, c), color))
    return seeds

def get_neighbors(coord, shape):
    """Gets 4-way adjacent neighbor coordinates within grid bounds."""
    r, c = coord
    height, width = shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid by flood-filling contiguous blue regions 
    adjacent to seed pixels with the seed's color.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Find all seed pixels
    seeds = find_seeds(input_grid)
    
    # Keep track of blue pixels that have already been colored by any seed's fill
    # This prevents a blue region adjacent to multiple seeds from being colored multiple times
    # and ensures the first seed encountered (in the seed iteration order) determines the color.
    globally_colored_blue_pixels = set()

    # Process each seed
    for seed_coord, seed_color in seeds:
        sr, sc = seed_coord
        
        # Find blue neighbors of the current seed
        seed_neighbors = get_neighbors(seed_coord, (height, width))
        
        for neighbor_r, neighbor_c in seed_neighbors:
            # Check if the neighbor is blue in the original grid
            # AND if it hasn't already been colored by a fill from another seed
            if input_grid[neighbor_r, neighbor_c] == 1 and (neighbor_r, neighbor_c) not in globally_colored_blue_pixels:
                
                # Start a flood fill (BFS) from this uncolored adjacent blue pixel
                # to find the entire contiguous blue component connected to it.
                q = deque([(neighbor_r, neighbor_c)])
                
                # Keep track of visited pixels *within this specific fill* to avoid cycles
                visited_in_this_fill = set([(neighbor_r, neighbor_c)]) 
                
                # Store all pixels belonging to the component found by this fill
                component_pixels = set([(neighbor_r, neighbor_c)])

                while q:
                    curr_r, curr_c = q.popleft()
                    
                    # Explore neighbors of the current pixel in the BFS
                    current_neighbors = get_neighbors((curr_r, curr_c), (height, width))
                    for nr, nc in current_neighbors:
                        # Check if the neighbor is blue in the original grid
                        # AND it hasn't been visited during *this* specific fill operation
                        # AND it hasn't been colored globally by *any* previous fill operation
                        if input_grid[nr, nc] == 1 and \
                           (nr, nc) not in visited_in_this_fill and \
                           (nr, nc) not in globally_colored_blue_pixels:
                            
                            # Mark as visited for this fill
                            visited_in_this_fill.add((nr, nc))
                            # Add to the component list
                            component_pixels.add((nr, nc))
                            # Add to the queue to explore its neighbors
                            q.append((nr, nc))
                            
                # After the BFS completes for this component, color all found pixels
                # in the output grid and mark them as globally colored.
                for comp_r, comp_c in component_pixels:
                    output_grid[comp_r, comp_c] = seed_color
                    globally_colored_blue_pixels.add((comp_r, comp_c))

    # Return the modified grid
    return output_grid