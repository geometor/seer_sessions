```python
import numpy as np
from collections import deque

"""
Identify distinct objects in the input grid. An object is defined as a 
contiguous group of non-background (non-zero) pixels, using 8-way adjacency 
(sides and diagonals). For each object found, determine the unique non-background 
colors present within it. If an object consists of exactly two distinct 
non-background colors (Color A and Color B), swap these colors within that 
object in the output grid: all pixels of Color A become Color B, and all pixels 
of Color B become Color A. Objects with fewer or more than two distinct 
non-background colors, as well as the background pixels (color 0), remain 
unchanged. The output grid has the same dimensions as the input grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by swapping the two constituent colors within each 
    distinct multi-colored object.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input. This ensures that
    # background pixels and objects not meeting the criteria remain unchanged.
    output_grid_np = np.copy(input_grid_np)
    # Get grid dimensions
    height, width = input_grid_np.shape
    # Keep track of visited cells to ensure each object is processed only once
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # Iterate through each cell of the grid to find starting points of objects
    for r in range(height):
        for c in range(width):
            # Check if the cell is non-background and hasn't been visited yet
            if input_grid_np[r, c] != 0 and not visited[r, c]:
                # Start of a new potential object, initiate Breadth-First Search (BFS)
                object_coords = []  # Store coordinates of pixels in the current object
                object_colors = set()  # Store unique non-background colors in the object
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True # Mark starting cell as visited

                # Perform BFS to find all connected non-background pixels
                while q:
                    curr_r, curr_c = q.popleft()

                    # Record the coordinate and color of the current cell
                    object_coords.append((curr_r, curr_c))
                    object_colors.add(input_grid_np[curr_r, curr_c])

                    # Explore 8 neighbors (horizontal, vertical, and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip the cell itself

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if the neighbor is within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is non-background and not visited
                                if input_grid_np[nr, nc] != 0 and not visited[nr, nc]:
                                    visited[nr, nc] = True # Mark neighbor as visited
                                    q.append((nr, nc)) # Add neighbor to the queue

                # --- Object Processing ---
                # After the BFS completes, analyze the identified object
                # Check if the object consists of exactly two distinct non-background colors
                if len(object_colors) == 2:
                    # Get the two colors found in the object
                    color1, color2 = list(object_colors)
                    
                    # Iterate through all coordinates belonging to this object
                    # and apply the color swap directly onto the output grid
                    for obj_r, obj_c in object_coords:
                        if input_grid_np[obj_r, obj_c] == color1:
                            output_grid_np[obj_r, obj_c] = color2
                        elif input_grid_np[obj_r, obj_c] == color2:
                            output_grid_np[obj_r, obj_c] = color1
                # Else (object has 1 color, or more than 2 colors): 
                # No action needed, as output_grid_np already holds the original colors.

    # Convert the final NumPy array back to a list of lists format
    return output_grid_np.tolist()
```