```python
import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Identify connected components of green pixels (value 3) using 8-way adjacency.
    2. Determine if any pixel within a green component is adjacent (8-way) to any red pixel (value 2).
    3. If a green component is adjacent to a red pixel, change all pixels of that component to blue (value 1) in the output grid.
    4. Otherwise, the green component remains unchanged.
    5. All non-green pixels retain their original color.
    """
    
    # Convert input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to store the output; modifications will be made here
    output_np = np.copy(input_np)
    height, width = input_np.shape
    # Keep track of visited pixels to avoid processing components multiple times
    visited = np.zeros_like(input_np, dtype=bool)

    # Define relative coordinates for 8 neighbors (orthogonal and diagonal)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each pixel in the grid to find the start of green components
    for r in range(height):
        for c in range(width):
            # If we find a green pixel (3) that hasn't been visited yet, start exploring its component
            if input_np[r, c] == 3 and not visited[r, c]:
                
                # Initialize structures for the current component search (BFS)
                current_component_coords = [] # Stores coordinates of pixels in this component
                is_adjacent_to_red = False    # Flag to check if this component touches a red pixel
                queue = deque([(r, c)])       # Queue for BFS
                visited[r, c] = True          # Mark the starting pixel as visited
                
                # --- Breadth-First Search (BFS) ---
                # Explore the connected component of green pixels
                while queue:
                    curr_r, curr_c = queue.popleft()
                    # Add the current pixel to the list for this component
                    current_component_coords.append((curr_r, curr_c))
                    
                    # Check all 8 neighbors of the current pixel
                    for dr, dc in neighbor_offsets:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Ensure the neighbor is within the grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check neighbor's color in the original input grid
                            neighbor_color = input_np[nr, nc]
                            
                            # If the neighbor is red (2), set the flag for the component
                            if neighbor_color == 2:
                                is_adjacent_to_red = True 
                                # Note: We continue BFS to find all component pixels,
                                # even after finding a red neighbor.
                                
                            # If the neighbor is green (3) and hasn't been visited,
                            # mark it visited and add it to the queue to explore later.
                            elif neighbor_color == 3 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                # --- End of BFS for this component ---
                                
                # After exploring the entire component, check the flag
                if is_adjacent_to_red:
                    # If the component was adjacent to red, change all its pixels to blue (1) in the output grid
                    for comp_r, comp_c in current_component_coords:
                        output_np[comp_r, comp_c] = 1 

    # Convert the modified NumPy array back to a standard list of lists format
    output_grid = output_np.tolist()
    return output_grid

```