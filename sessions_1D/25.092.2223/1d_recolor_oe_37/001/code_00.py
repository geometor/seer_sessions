import numpy as np
from collections import deque

"""
Identifies contiguous objects of maroon (9) pixels in the input grid.
Calculates the size (number of pixels) of each maroon object.
Replaces the maroon pixels in the output grid based on the parity of the object's size:
- If the size is even, the object's pixels are changed to red (2).
- If the size is odd, the object's pixels are changed to yellow (4).
Background white (0) pixels remain unchanged.
"""

def find_connected_object(grid, start_row, start_col, target_color, visited):
    """
    Finds a single connected object of target_color starting from (start_row, start_col) using BFS.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        target_color (int): The color of the object pixels to find.
        visited (np.array): A boolean grid indicating visited pixels.

    Returns:
        list: A list of (row, col) tuples representing the coordinates of the object pixels.
              Returns an empty list if the starting cell is not the target color or already visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] != target_color:
        return []

    object_coords = []
    queue = deque([(start_row, start_col)])
    visited[start_row, start_col] = True

    while queue:
        r, c = queue.popleft()
        object_coords.append((r, c))

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds and if the neighbor is the target color and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and \
               grid[nr, nc] == target_color:
                visited[nr, nc] = True
                queue.append((nr, nc))

    return object_coords


def transform(input_grid):
    """
    Transforms the input grid by finding maroon objects and recoloring them
    based on the parity of their size (even -> red(2), odd -> yellow(4)).
    
    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    np_input = np.array(input_grid, dtype=int)
    rows, cols = np_input.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(np_input)
    
    # Keep track of visited pixels to avoid processing objects multiple times
    visited = np.zeros_like(np_input, dtype=bool)
    
    maroon_color = 9
    red_color = 2
    yellow_color = 4

    # Iterate through each pixel of the grid
    for r in range(rows):
        for c in range(cols):
            # If we find a maroon pixel that hasn't been visited yet, start finding the object
            if np_input[r, c] == maroon_color and not visited[r, c]:
                # Find all connected pixels belonging to this object
                object_pixels = find_connected_object(np_input, r, c, maroon_color, visited)
                
                # Calculate the size of the object
                object_size = len(object_pixels)
                
                # Determine the replacement color based on size parity
                if object_size % 2 == 0:
                    replacement_color = red_color # Even size -> Red
                else:
                    replacement_color = yellow_color # Odd size -> Yellow
                    
                # Update the output grid with the replacement color for all pixels in the object
                for obj_r, obj_c in object_pixels:
                    output_grid[obj_r, obj_c] = replacement_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()