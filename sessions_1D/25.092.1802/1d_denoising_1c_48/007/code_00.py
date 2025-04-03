import numpy as np
from collections import deque

"""
Transforms the input grid by identifying the single foreground color (C), finding the topmost row ('max_row_idx') with the maximum count of C, locating all connected components (objects) of color C using 4-way adjacency, selecting the object(s) that intersect 'max_row_idx', and copying only the pixels belonging to these selected object(s) to an otherwise background-filled output grid of the same dimensions.
"""

def find_foreground_color(grid):
    """
    Finds the first non-zero (non-background) color encountered in the grid.
    Assumes there is at most one non-background color per grid based on examples.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The foreground color value, or 0 if only background is present.
    """
    # Iterate through all pixels in the grid
    for pixel in grid.flat:
        # If a non-background pixel is found, return its color
        if pixel != 0:
            return pixel
    # If no non-background pixel is found, return the background color
    return 0

def find_max_row(grid, foreground_color):
    """
    Finds the index of the row containing the maximum number of foreground_color pixels.
    Ties are broken by choosing the lowest row index (topmost).

    Args:
        grid (np.array): The input grid.
        foreground_color (int): The color to count.

    Returns:
        int: The index of the row with the maximum count, or -1 if the color is not found or has zero count.
    """
    max_count = -1
    max_row_idx = -1
    height = grid.shape[0]

    # Cannot meaningfully find max row for background color in this context
    if foreground_color == 0:
        return -1

    # Iterate through each row
    for r in range(height):
        # Count occurrences of the foreground color in the current row
        current_count = np.count_nonzero(grid[r, :] == foreground_color)
        # If current count is strictly greater than max_count, update max_count and max_row_idx
        # This automatically handles the tie-breaking (choosing the first max row found)
        if current_count > max_count:
            max_count = current_count
            max_row_idx = r

    # If max_count is still 0 after checking all rows, the color wasn't present with a count > 0
    if max_count <= 0:
      return -1

    return max_row_idx

def find_connected_components(grid, foreground_color):
    """
    Finds all connected components (objects) of a given foreground color using BFS.
    Connectivity is 4-directional (cardinal: up, down, left, right).

    Args:
        grid (np.array): The input grid.
        foreground_color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of pixels in a connected component.
                   Returns an empty list if foreground_color is 0 or not found.
    """
    # Cannot find components of the background color meaningfully here
    if foreground_color == 0:
        return []

    height, width = grid.shape
    # Keep track of visited pixels to avoid redundant processing
    visited = np.zeros_like(grid, dtype=bool)
    objects = [] # List to store the sets of coordinates for each object found

    # Iterate through every pixel in the grid
    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited yet
            if grid[r, c] == foreground_color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the connected component (object)
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True # Mark the starting pixel as visited

                while q:
                    row, col = q.popleft() # Get the next pixel from the queue
                    current_object_coords.add((row, col)) # Add it to the current object

                    # Check its 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == foreground_color and not visited[nr, nc]:
                                visited[nr, nc] = True # Mark neighbor as visited
                                q.append((nr, nc)) # Add neighbor to the queue

                # Once the queue is empty, the full object has been found
                objects.append(current_object_coords)

    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_array.size == 0:
        return []

    height, width = input_array.shape

    # Initialize output grid with the same dimensions, filled with background color (0)
    output_array = np.zeros_like(input_array)

    # Step 1: Find the unique foreground color
    foreground_color = find_foreground_color(input_array)

    # If no foreground color exists, return the all-background grid
    if foreground_color == 0:
        return output_array.tolist()

    # Step 2: Find the topmost row with the maximum count of the foreground color
    max_row_idx = find_max_row(input_array, foreground_color)

    # If no row contains the foreground color (e.g., max_count was 0), return background grid
    if max_row_idx == -1:
         return output_array.tolist()

    # Step 3: Find all connected components (objects) of the foreground color
    all_objects = find_connected_components(input_array, foreground_color)

    # Step 4: Identify target objects - those intersecting the max_row_idx
    target_pixels = set() # Use a set to store all pixels of the target object(s)
    for obj_coords in all_objects:
        # Check if any pixel in this object lies on the max_row_idx
        intersects_max_row = any(r == max_row_idx for r, c in obj_coords)
        if intersects_max_row:
            # If it intersects, add all pixels of this object to the target set
            target_pixels.update(obj_coords)

    # Step 5: Populate the output grid with the pixels from the target objects
    for r, c in target_pixels:
        # Check bounds just in case (should be guaranteed by find_connected_components)
        if 0 <= r < height and 0 <= c < width:
             output_array[r, c] = foreground_color # Set the pixel in the output grid

    # Convert the resulting NumPy array back to a list of lists and return
    return output_array.tolist()