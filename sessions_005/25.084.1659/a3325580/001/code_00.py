"""
Identify all distinct objects (connected components of the same non-zero color) in the input grid.
Calculate the size (number of pixels) of each object.
Determine the maximum size found among all objects.
Identify all colors associated with objects that have this maximum size.
Sort these identified colors numerically in ascending order.
Construct an output grid where the height is the maximum size and the width is the count of identified colors.
Fill each column of the output grid entirely with one of the sorted colors, in order.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all connected components (objects) of non-zero colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'size', and 'pixels' (a list of coordinates).
    """
    height, width = grid.shape
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If already visited or background color, skip
            if (r, c) in visited or grid[r, c] == 0:
                continue

            # Start BFS for a new object
            current_color = grid[r, c]
            current_object_pixels = []
            q = deque([(r, c)])
            visited.add((r, c))

            while q:
                row, col = q.popleft()
                current_object_pixels.append((row, col))

                # Check neighbors (up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc

                    # Check boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if neighbor is part of the object and not visited
                        if grid[nr, nc] == current_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

            # Store the found object
            objects.append({
                'color': current_color,
                'size': len(current_object_pixels),
                'pixels': current_object_pixels
            })
            
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on finding the largest objects and their colors.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # 1. Scan the input grid to identify all distinct objects and their sizes.
    objects = find_objects(input_grid)

    # Handle case where there are no non-zero objects
    if not objects:
        # Returning a 1x1 grid with 0, although problem examples don't cover this.
        # Based on examples, a valid output is always generated.
        # An alternative might be an empty array, but let's assume 1x1 zero.
        # Re-evaluating: The output sizes depend on max_size and colors. If no objects, max_size is 0.
        # A 0-height array might be problematic. Let's return an empty array representation.
         return np.array([[]], dtype=int) # Or perhaps np.empty((0,0), dtype=int) ? Let's stick to this for now.


    # 2. Find the maximum size observed among them.
    max_size = 0
    if objects:
        max_size = max(obj['size'] for obj in objects)
        
    # Handle case where max_size is 0 (e.g., only background color)
    if max_size == 0:
         return np.array([[]], dtype=int) # Consistent with no objects case


    # 3. Create a list of all colors that have at least one object with size equal to max_size.
    max_size_colors_set = set()
    for obj in objects:
        if obj['size'] == max_size:
            max_size_colors_set.add(obj['color'])

    # 4. Sort this list of colors numerically in ascending order.
    output_colors = sorted(list(max_size_colors_set))
    
    # Handle case where no colors were found (shouldn't happen if max_size > 0)
    if not output_colors:
        return np.array([[]], dtype=int)


    # 5. Determine the dimensions of the output grid.
    output_height = max_size
    output_width = len(output_colors)

    # 6. Create and populate the output grid.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for j, color in enumerate(output_colors):
        output_grid[:, j] = color # Fill the entire column j with the color

    return output_grid