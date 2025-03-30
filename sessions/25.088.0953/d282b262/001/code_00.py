import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all distinct connected objects (contiguous blocks of non-white pixels) in the input grid.
2. For each identified object:
    a. Determine its rightmost column index (object_max_col).
    b. Calculate the horizontal shift required to move the object so its rightmost edge aligns with the rightmost column of the grid: shift = grid_width - 1 - object_max_col.
    c. Record the coordinates and colors of all pixels belonging to the object and its calculated shift.
3. Initialize an output grid of the same dimensions as the input, filled with the background color (white, 0).
4. Place each object onto the output grid by applying its calculated horizontal shift to all of its pixels. If objects overlap after shifting, the pixel colors from objects processed later will overwrite earlier ones.
"""

def find_objects(input_grid_np):
    """
    Finds all connected objects of non-background pixels in the grid.

    Args:
        input_grid_np: A NumPy array representing the input grid.

    Returns:
        A list of objects. Each object is a dictionary containing:
        - 'pixels': A list of tuples (row, col, color) for each pixel in the object.
        - 'max_col': The maximum column index occupied by the object.
    """
    height, width = input_grid_np.shape
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            # Check if the pixel is part of an object and hasn't been visited yet
            if input_grid_np[r, c] != 0 and (r, c) not in visited:
                # Start a Breadth-First Search (BFS) to find the connected object
                current_object_pixels = []
                object_max_col = -1
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    color = input_grid_np[curr_r, curr_c]
                    current_object_pixels.append((curr_r, curr_c, color))
                    object_max_col = max(object_max_col, curr_c)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds, if it's part of an object (non-zero), and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               input_grid_np[nr, nc] != 0 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                
                # Store the found object's data
                objects.append({'pixels': current_object_pixels, 'max_col': object_max_col})
                
    return objects

def transform(input_grid):
    """
    Moves all non-background objects in the input grid to the right edge,
    preserving their shape and relative vertical positions.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize the output grid with the background color (0)
    output_grid_np = np.zeros_like(input_grid_np)

    # Find all distinct objects in the input grid
    objects_data = find_objects(input_grid_np)

    # Process each found object
    for obj in objects_data:
        # Calculate the necessary horizontal shift for this object
        # Shift = target_right_edge - object_right_edge
        # target_right_edge = width - 1
        # object_right_edge = obj['max_col']
        shift = (width - 1) - obj['max_col']

        # Move each pixel of the object to its new location in the output grid
        for r_pix, c_pix, color in obj['pixels']:
            new_c = c_pix + shift
            # Ensure the new column is within bounds (should be, by calculation)
            if 0 <= new_c < width:
                 output_grid_np[r_pix, new_c] = color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid