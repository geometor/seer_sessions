import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Convert all blue (1) pixels in the input grid to red (2) in the output grid. These red pixels, along with pre-existing red pixels, act as barriers.
3. Find the single green (3) pixel in the input grid, which serves as the seed for a flood fill.
4. Perform a flood fill starting from the seed location. The fill color is green (3).
5. The fill spreads horizontally and vertically (4-connectivity) into adjacent azure (8) pixels.
6. The fill stops when it hits a red (2) pixel (either original or converted from blue) or the grid boundaries.
7. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a flood fill transformation starting from a green seed, bounded by red barriers
    (original red or converted blue).

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = input_grid_np.copy()
    height, width = output_grid.shape
    
    # 2. Convert all blue (1) pixels to red (2) in the output grid.
    output_grid[output_grid == 1] = 2
    
    # 3. Find the single green (3) seed pixel.
    seed_coords = None
    seed_locations = np.where(input_grid_np == 3) # Use input_grid to find original seed
    if len(seed_locations[0]) > 0:
        # Assuming there's always exactly one seed as per examples
        seed_coords = (seed_locations[0][0], seed_locations[1][0])
    else:
        # Handle cases where no seed is found (though not expected based on examples)
        # Return the grid with only blue->red conversion if no seed
        return output_grid 

    # 4. Perform flood fill starting from the seed location.
    
    # Define the fill color (green) and target color (azure)
    fill_color = 3
    target_color = 8
    barrier_color = 2 # Red

    # Use a queue for Breadth-First Search (BFS) flood fill
    queue = deque([seed_coords])
    
    # Use a set to keep track of visited cells for the fill process
    # Important: Initialize visited with the seed to avoid reprocessing it,
    # but DO NOT change the seed's color in the output grid (it's already green).
    visited = {seed_coords} 

    # 5. & 6. Fill loop: Spread into azure, stop at red or boundaries
    while queue:
        r, c = queue.popleft()
        
        # Explore 4-directional neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            neighbor_coords = (nr, nc)

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor hasn't been visited yet
                if neighbor_coords not in visited:
                    # Check if the neighbor is the target color (azure) in the output grid
                    if output_grid[nr, nc] == target_color:
                        # Change the neighbor's color to the fill color (green)
                        output_grid[nr, nc] = fill_color
                        # Mark as visited
                        visited.add(neighbor_coords)
                        # Add to the queue to explore from this neighbor
                        queue.append(neighbor_coords)
                    # If the neighbor is not azure, add it to visited anyway 
                    # to prevent checking it again via another path. This includes barriers.
                    elif output_grid[nr, nc] != fill_color: # Don't add already filled cells
                         visited.add(neighbor_coords)
                         
    # 7. Return the final output grid.
    return output_grid.tolist() # Convert back to list of lists if required by framework
