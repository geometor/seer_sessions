import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify all distinct objects in the input grid. An object is defined as a contiguous group of non-white pixels (connected horizontally or vertically, 4-way adjacency).
3. If no objects are found (the grid is entirely white or empty), return the input grid unchanged.
4. For each identified object:
    a. Determine the maximum column index (`object_max_col`) occupied by any pixel belonging to this object.
    b. Calculate the required horizontal shift for this object: `shift = (grid_width - 1) - object_max_col`, where `grid_width` is the width of the input grid.
    c. Iterate through all pixels `(row, col)` with `color` belonging to this object.
    d. Calculate the new column for each pixel: `new_col = col + shift`.
    e. Place the `color` of the pixel at the new coordinates `(row, new_col)` in the output grid. Ensure the new column is within grid bounds (though the shift calculation should guarantee this if `object_max_col` is correct).
5. Return the completed output grid.
"""

def find_objects(grid_np):
    """
    Finds all distinct connected components (objects) of non-background pixels
    using Breadth-First Search (BFS).

    Args:
        grid_np: A NumPy array representing the input grid.

    Returns:
        A list of objects. Each object is represented as a dictionary containing:
        'pixels': A list of tuples, where each tuple is ((row, col), color).
        'max_c': The maximum column index occupied by any pixel in this object.
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If pixel is non-white and not yet visited, start BFS for a new object
            if grid_np[r, c] != 0 and not visited[r, c]:
                current_object_pixels = []
                object_max_c = -1
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    color = grid_np[row, col]
                    
                    # Add pixel to the current object list
                    current_object_pixels.append(((row, col), color))
                    # Update the maximum column for this object
                    object_max_c = max(object_max_c, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if neighbor is within bounds, is non-white, and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid_np[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object's pixels and its max column
                if current_object_pixels:
                     objects.append({
                         'pixels': current_object_pixels,
                         'max_c': object_max_c
                     })
                     
    return objects

def transform(input_grid):
    """
    Shifts each distinct non-background object horizontally so that its 
    rightmost edge aligns with the right edge of the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if input_grid_np.size == 0:
        return []
        
    height, width = input_grid_np.shape

    # Find all distinct objects in the input grid
    objects = find_objects(input_grid_np)

    # If there are no non-white pixels (no objects), return the original grid
    if not objects:
        return input_grid

    # Initialize the output grid with the background color (0)
    output_grid_np = np.zeros_like(input_grid_np)
    grid_width = width

    # Process each object independently
    for obj in objects:
        object_pixels = obj['pixels']
        object_max_col = obj['max_c']

        # Calculate the horizontal shift required for this specific object
        # shift = target_right_edge - current_object_right_edge
        shift = (grid_width - 1) - object_max_col

        # Apply the calculated shift to all pixels of this object
        for (r, c), color in object_pixels:
            new_c = c + shift
            # Place the pixel in the output grid at its new position
            # Bounds check added for safety, though shift calculation should prevent out-of-bounds
            if 0 <= new_c < grid_width: 
                output_grid_np[r, new_c] = color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid