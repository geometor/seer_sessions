```python
import numpy as np

"""
Transformation Rule Description:

The transformation identifies non-background (white, 0) and non-primary shape (blue, 1) pixels, referred to as "seed" pixels. For each seed pixel, it examines its 4-way adjacent neighbors in the input grid. If an adjacent neighbor pixel is blue (1), its color in the output grid is changed to the color of the seed pixel. All other pixels (background, seeds themselves, and blue pixels not adjacent to any seed) retain their original color from the input grid. If a blue pixel is adjacent to multiple seeds, its final color in the output grid will be determined by the last seed processed that has it as a neighbor during the iteration.
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
    Transforms the input grid by changing the color of blue pixels 
    adjacent to seed pixels to the seed's color.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Find all seed pixels
    seeds = find_seeds(input_grid)

    # Process each seed
    for seed_coord, seed_color in seeds:
        # Find 4-way neighbors of the current seed
        seed_neighbors = get_neighbors(seed_coord, (height, width))
        
        # Check each neighbor
        for neighbor_r, neighbor_c in seed_neighbors:
            # If the neighbor in the original input grid is blue (1)
            if input_grid[neighbor_r, neighbor_c] == 1:
                # Change the color of that neighbor position in the output grid
                # to the color of the current seed.
                output_grid[neighbor_r, neighbor_c] = seed_color
                
    # Return the modified grid
    return output_grid
```