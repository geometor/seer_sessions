"""
Identify all distinct, connected groups (objects) of azure pixels (color 8) in the input grid using 8-way connectivity (including diagonals).
For each identified azure object:
1. Calculate its width based on the horizontal span of its bounding box (max_col - min_col + 1).
2. Determine the horizontal shift amount as `shift = width + 1`.
3. Create an output grid initialized with the background color (white, 0).
4. For every pixel belonging to the object at input position (row, column), calculate its new position (row, column + shift) and place the azure color (8) at this new position in the output grid, ensuring the new position is within the grid boundaries.
Return the final output grid.
"""

import numpy as np
import collections

def _find_objects(grid, target_color):
    """
    Finds all connected components of a specific color in a grid using 8-way connectivity (BFS).

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (list of (r, c) tuples), 'bounding_box'
              (min_r, min_c, max_r, max_c), and 'width'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find an unvisited pixel of the target color
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_pixels = []
                q = collections.deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform BFS
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))
                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip the current cell itself
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds and if the neighbor is a valid part of the object
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Calculate properties after finding all pixels of the object
                width = max_c - min_c + 1
                bounding_box = (min_r, min_c, max_r, max_c)
                objects.append({
                    "pixels": current_object_pixels,
                    "bounding_box": bounding_box,
                    "width": width
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by shifting azure objects horizontally based on their width.

    Args:
        input_grid (list[list[int]]): The 2D input grid.

    Returns:
        list[list[int]]: The transformed 2D output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output grid with background color 0 (white)
    output_grid = np.zeros_like(input_np)
    
    object_color = 8 # Azure
    background_color = 0 # White

    # Find all azure objects in the input grid
    azure_objects = _find_objects(input_np, object_color)

    # Process each found object
    for obj in azure_objects:
        # Calculate the width of the object's bounding box
        width = obj["width"]
        
        # Calculate the horizontal shift amount
        shift = width + 1
        
        # Move each pixel of the current object
        for r, c in obj["pixels"]:
            # Calculate the new column index
            new_c = c + shift
            
            # Place the object's color in the output grid at the new position,
            # ensuring it's within the grid bounds.
            if 0 <= r < rows and 0 <= new_c < cols:
                 output_grid[r, new_c] = object_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()