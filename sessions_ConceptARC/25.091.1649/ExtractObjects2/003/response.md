```python
import numpy as np
from collections import deque

"""
Identify the unique non-white color C such that all pixels of color C in the input grid form exactly one connected object (using 8-way adjacency), AND this single object does not touch the grid boundary (outermost rows/columns).
Determine the bounding box of this single object.
Create an output grid sized to this bounding box.
Populate the output grid: place the target color C at the relative positions corresponding to the object's pixels in the input, and fill the rest with white (0).
"""

def find_objects_and_check_boundary(grid, color):
    """
    Finds all connected objects of a specific color and checks if they touch the boundary.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[dict]: A list where each element is a dictionary containing:
                    'coords': set of (row, col) tuples for the object's pixels.
                    'touches_boundary': boolean indicating if the object touches the grid edge.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects_data = []
    # Define 8-way neighbors (including diagonals)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and not yet visited, start a search (BFS)
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                touches_boundary = False # Flag for this specific object

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.add((curr_r, curr_c))

                    # Check if the current pixel touches the boundary
                    if curr_r == 0 or curr_r == rows - 1 or curr_c == 0 or curr_c == cols - 1:
                        touches_boundary = True

                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store data for the found object
                objects_data.append({
                    'coords': current_object_coords,
                    'touches_boundary': touches_boundary
                })

    return objects_data

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Find unique non-white colors
    unique_colors = np.unique(input_array)
    non_white_colors = unique_colors[unique_colors != 0]

    target_color = -1
    target_object_coords = None

    # Identify the target color and object
    # Loop through each non-white color found in the grid
    for color in non_white_colors:
        # Find all objects of this color and check their boundary contact
        objects_data = find_objects_and_check_boundary(input_array, color)
        
        # Check if this color meets the criteria: exactly one object AND it does not touch the boundary
        if len(objects_data) == 1 and not objects_data[0]['touches_boundary']:
            target_color = color
            target_object_coords = objects_data[0]['coords'] # Get the set of coordinates
            break # Found the unique target color, no need to check others

    # Handle case where no suitable object is found
    if target_color == -1 or not target_object_coords:
        # Return an empty or default grid if no target object is identified
        # Based on ARC tasks, this usually means the logic is incomplete,
        # but for robustness, return a small default grid.
        return [[0]] 

    # Determine the bounding box of the target object
    min_row = rows
    max_row = -1
    min_col = cols
    max_col = -1
    for r, c in target_object_coords:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    # Calculate output grid dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Create the output grid, initialized with white (0)
    output_array = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid with the target object's pixels
    for r, c in target_object_coords:
        # Calculate relative coordinates within the bounding box
        relative_r = r - min_row
        relative_c = c - min_col
        # Place the target color in the output grid at the relative position
        output_array[relative_r, relative_c] = target_color

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```