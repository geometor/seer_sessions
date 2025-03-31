```python
import numpy as np
from collections import deque, Counter

"""
Identifies regions fully enclosed by a single connected component of a uniform non-white color.
For each such enclosed region:
1. Finds all "seed" pixels within the region. Seeds are pixels whose color is not white (0) and not the color of the enclosing boundary component.
2. Counts the number of seed pixels (N_seeds).
3. If N_seeds > 1:
    a. Determines the most frequent color among the seeds (C_fill). Ties in frequency are broken by choosing the color with the smallest numerical index.
    b. Changes the color of all pixels within the enclosed region (both original seeds and white pixels) to C_fill in the output grid. Marks the boundary and interior pixels as processed.
4. If N_seeds == 1:
    a. Changes the color of the single seed pixel to white (0) in the output grid. Marks the boundary and the seed pixel's location as processed.
5. If N_seeds == 0:
    a. Leaves the region unchanged in the output grid. Marks only the boundary pixels as processed.
Boundary component pixels themselves remain unchanged unless overwritten by a fill in a *different* region's processing step (unlikely but possible in complex overlaps).
After processing all components, any pixel that was initially non-white and has not been marked as processed (either as part of a boundary or a transformed region) is changed to white (0).
"""

# Imports are implicitly handled by the environment

def get_neighbors(r, c, height, width):
    """Gets 4-directionally adjacent valid neighbor coordinates."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def find_connected_components(grid_np):
    """
    Finds all connected components of non-white pixels.

    Args:
        grid_np: Numpy array representing the grid.

    Returns:
        A list of tuples, where each tuple is (component_pixels_set, component_color).
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    components = []
    
    for r in range(height):
        for c in range(width):
            color = grid_np[r, c]
            # Start BFS if non-white and not visited
            if color != 0 and not visited[r, c]:
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        # Check if neighbor has same color and not visited
                        if grid_np[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            component_pixels.add((nr, nc))
                            q.append((nr, nc))
                            
                if component_pixels:
                    components.append((component_pixels, color))
                    
    return components

def find_interior_region(grid_np, component_pixels):
    """
    Identifies the interior region enclosed by a given component.
    Uses flood fill from edges, treating the component pixels as walls.

    Args:
        grid_np: Numpy array representing the grid.
        component_pixels: A set of (r, c) tuples for the boundary component.

    Returns:
        A set of (r, c) tuples representing the interior pixels, 
        or an empty set if no fully enclosed interior exists.
    """
    height, width = grid_np.shape
    
    # Mark component pixels as walls (visited)
    exterior_visited = np.zeros_like(grid_np, dtype=bool)
    for r, c in component_pixels:
        exterior_visited[r, c] = True
        
    q = deque()
    
    # Add edge pixels to queue if they are not walls (part of the component)
    # Crucially, only add if the pixel is actually within grid bounds
    for r in range(height):
        if 0 <= r < height and 0 <= 0 < width and not exterior_visited[r, 0]: 
            q.append((r, 0)); exterior_visited[r, 0] = True
        if 0 <= r < height and 0 <= width - 1 < width and not exterior_visited[r, width - 1]: 
            q.append((r, width-1)); exterior_visited[r, width-1] = True
    for c in range(width): # Handle top/bottom edges, avoid double-counting corners
        if 0 <= 0 < height and 0 <= c < width and not exterior_visited[0, c]: 
            q.append((0, c)); exterior_visited[0, c] = True
        if 0 <= height - 1 < height and 0 <= c < width and not exterior_visited[height-1, c]: 
            q.append((height-1, c)); exterior_visited[height-1, c] = True
        
    # Flood fill from edges to find all exterior pixels
    while q:
        r, c = q.popleft()
        for nr, nc in get_neighbors(r, c, height, width):
            if not exterior_visited[nr, nc]: # If neighbor is not wall and not visited
                 exterior_visited[nr, nc] = True
                 q.append((nr, nc))

    # Identify interior pixels (those not visited by exterior flood and not walls)
    interior_pixels_coords = set()
    for r in range(height):
        for c in range(width):
            # A pixel is interior if it's not a wall AND not reached by exterior flood
            if not exterior_visited[r, c]: 
                interior_pixels_coords.add((r, c))
                
    return interior_pixels_coords


def transform(input_grid):
    """
    Applies the transformation logic based on enclosed regions and seed pixels,
    followed by a cleanup of unprocessed non-white pixels.
    """
    # Convert input list-of-lists to a NumPy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input, modifications happen here
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Keep track of pixels that are part of a boundary or transformed region
    processed_pixels = set()

    # --- Step 1: Find all connected components of non-white pixels (potential boundaries) ---
    boundary_components = find_connected_components(input_grid_np)

    # --- Step 2: Process each potential boundary component ---
    for component_pixels, boundary_color in boundary_components:
        
        # --- Step 3: Identify the interior region enclosed by this component ---
        interior_region_pixels = find_interior_region(input_grid_np, component_pixels)

        # --- Step 4: If a non-empty interior region is found ---
        if interior_region_pixels:
            
            # --- Step 5: Identify seed pixels within this interior region ---
            seed_pixels_info = [] # Store dicts {'color': c, 'pos': (r, c)}
            for r_int, c_int in interior_region_pixels:
                pixel_color = input_grid_np[r_int, c_int]
                # Seed definition: non-white (0) and not the boundary color
                if pixel_color != 0 and pixel_color != boundary_color:
                    seed_pixels_info.append({'color': pixel_color, 'pos': (r_int, c_int)})

            # --- Step 6: Count the seeds ---
            num_seeds = len(seed_pixels_info)

            # --- Step 7: Apply transformation rules based on seed count ---
            if num_seeds > 1:
                # Mark boundary as processed
                processed_pixels.update(component_pixels)
                
                # Find the most frequent seed color (tie-break with lowest index)
                seed_colors = [s['color'] for s in seed_pixels_info]
                color_counts = Counter(seed_colors)
                # Find max frequency, default to 0 if no seeds (shouldn't happen here)
                max_freq = max(color_counts.values()) if color_counts else 0
                # Get colors with max frequency, sort by color index for tie-breaking
                most_frequent_colors = sorted([color for color, count in color_counts.items() if count == max_freq])
                
                fill_color = most_frequent_colors[0] if most_frequent_colors else 0 # Use 0 as fallback

                # Flood fill the interior region in the output grid and mark as processed
                for r_fill, c_fill in interior_region_pixels:
                    output_grid[r_fill, c_fill] = fill_color
                    processed_pixels.add((r_fill, c_fill)) # Mark interior pixels as processed

            elif num_seeds == 1:
                # Mark boundary as processed
                processed_pixels.update(component_pixels)
                
                # Change the single seed pixel to white (0) in the output grid
                seed_pos = seed_pixels_info[0]['pos']
                output_grid[seed_pos[0], seed_pos[1]] = 0
                # Mark the seed pixel's original location as processed
                processed_pixels.add(seed_pos) 
                
            else: # num_seeds == 0
                # Mark boundary as processed
                processed_pixels.update(component_pixels)
                # Interior region remains unchanged, and its pixels are NOT marked processed yet.
                # If any were initially non-white, they'll be handled by cleanup.

    # --- Step 8: Final Cleanup ---
    # Iterate through the original grid. If a pixel was non-white initially
    # and wasn't marked as processed (boundary or transformed region), set it to white.
    for r in range(height):
        for c in range(width):
            # Check original color and if pixel was processed
            if input_grid_np[r, c] != 0 and (r, c) not in processed_pixels:
                output_grid[r, c] = 0 # Set to white in the output

    # Convert the final NumPy array back to a standard list of lists
    return output_grid.tolist()
```