```python
import numpy as np
from collections import deque
import math

"""
Transforms an input grid based on the following rules:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected components (objects) of red pixels (color 2) using 4-way adjacency (up, down, left, right).
3.  For each distinct red object found:
    a.  Calculate the total number of pixels (`num_pixels`) in the object.
    b.  Calculate the object's geometric center (`center_r`, `center_c`). This is done by finding the average row and column coordinates of all pixels in the object and taking the floor of each average coordinate independently.
    c.  Calculate a size parameter `K` = floor(`num_pixels` / 2).
    d.  Define a diamond shape centered at (`center_r`, `center_c`). A pixel (`r`, `c`) is part of the diamond if its Manhattan distance to the center (|`r` - `center_r`| + |`c` - `center_c`|) is less than or equal to `K`.
    e.  Iterate through all pixels (`r`, `c`) within the grid boundaries.
    f.  If a pixel (`r`, `c`) is part of the calculated diamond shape:
        i. Check the color of the pixel at `output_grid[r, c]`.
        ii. If the color is white (0), change the color of `output_grid[r, c]` to azure (8).
        iii. If the color is not white (including the original red object pixels), leave it unchanged.
4.  Return the final modified output grid.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a specified color in the grid using 4-way adjacency.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[list[tuple[int, int]]]: A list where each element is a list
                                     of (row, col) coordinates for one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a connected component
                component = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component.append((curr_r, curr_c))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds and if it's the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if component:
                    objects.append(component)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by finding red objects, calculating their center 
    (using floor of average coordinates) and a size parameter K (based on floor of half the pixel count),
    and drawing azure diamonds around them, modifying only white pixels.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid represented as a list of lists.
                         Returns the original grid if input is invalid or no red objects found.
    """
    # Validate input grid format
    if not isinstance(input_grid, list) or not input_grid or not all(isinstance(row, list) for row in input_grid):
        print("Invalid input grid format. Returning original grid.")
        return input_grid
        
    # Convert to numpy array for easier processing
    try:
        input_np = np.array(input_grid, dtype=int)
    except ValueError:
        print("Input grid contains non-uniform rows. Returning original grid.")
        return input_grid
        
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape
    
    # 2. Find all red objects (color 2)
    red_objects = find_objects(input_np, 2) 

    # If no red objects are found, return the original grid copy
    if not red_objects:
        return output_grid.tolist()

    # 3. Process each red object
    for obj_coords in red_objects:
        if not obj_coords:
            continue 

        # a. Calculate the total number of pixels
        num_pixels = len(obj_coords)
        
        # b. Calculate geometric center (centroid, using floor)
        sum_r = sum(r for r, c in obj_coords)
        sum_c = sum(c for r, c in obj_coords)
        
        # Use floor of average coordinates for center
        center_r = int(math.floor(sum_r / num_pixels))
        center_c = int(math.floor(sum_c / num_pixels))
        
        # c. Calculate size parameter K 
        # REVISED CALCULATION: floor(num_pixels / 2)
        radius_k = int(math.floor(num_pixels / 2)) 

        # d. & e. & f. Iterate through pixels potentially within the diamond shape and modify white pixels
        # Define the iteration bounds based on the diamond's maximum extent for efficiency
        min_check_r = max(0, center_r - radius_k)
        max_check_r = min(rows, center_r + radius_k + 1) # +1 for range upper bound
        min_check_c = max(0, center_c - radius_k)
        max_check_c = min(cols, center_c + radius_k + 1) # +1 for range upper bound

        for r in range(min_check_r, max_check_r):
            for c in range(min_check_c, max_check_c):
                # Calculate Manhattan distance to the center
                dist = abs(r - center_r) + abs(c - center_c)

                # Check if within diamond radius K
                if dist <= radius_k:
                    # Modify only if the pixel is currently white (0)
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 8 # 8 is azure

    # 4. Return the result as a list of lists
    return output_grid.tolist()
```