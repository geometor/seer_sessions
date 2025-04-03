import numpy as np
from collections import deque

"""
Identify the single foreground color (C) in the input grid.
Find all distinct connected objects composed of this foreground color C, using cardinal (4-way) adjacency.
Determine the row index ('max_row_idx') that contains the highest count of color C. If multiple rows share the highest count, select the topmost row (smallest index).
Identify the specific object(s) that have at least one pixel located within 'max_row_idx'.
Create an output grid of the same dimensions as the input, filled entirely with the background color (0).
Copy only the pixels belonging to the identified target object(s) from the input grid to the corresponding positions in the output grid.
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
    for pixel in grid.flat:
        if pixel != 0:
            return pixel
    return 0 # Return background color (0) if no foreground color is found

def find_max_row(grid, foreground_color):
    """
    Finds the index of the row containing the maximum number of foreground_color pixels.
    Ties are broken by choosing the lowest row index (topmost).

    Args:
        grid (np.array): The input grid.
        foreground_color (int): The color to count.

    Returns:
        int: The index of the row with the maximum count, or -1 if the color is not found.
    """
    max_count = -1
    max_row_idx = -1
    height = grid.shape[0]

    if foreground_color == 0: # Cannot find max row for background color meaningfully in this context
        return -1

    for r in range(height):
        current_count = np.count_nonzero(grid[r, :] == foreground_color)
        if current_count > max_count:
            max_count = current_count
            max_row_idx = r
            
    # If max_count is still 0 after checking all rows, the color wasn't present
    if max_count == 0:
      return -1
      
    return max_row_idx

def find_connected_components(grid, foreground_color):
    """
    Finds all connected components (objects) of a given foreground color using BFS.
    Connectivity is 4-directional (cardinal).

    Args:
        grid (np.array): The input grid.
        foreground_color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of pixels in a connected component.
                   Returns an empty list if foreground_color is 0 or not found.
    """
    if foreground_color == 0:
        return []
        
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == foreground_color and not visited[r, c]:
                # Start BFS for a new object
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if it's a valid, unvisited pixel of the object
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == foreground_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append(current_object_coords)
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on selecting the object(s) connected
    to the row with the most foreground pixels.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if input_array.size == 0:
        return []
        
    height, width = input_array.shape

    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Find the foreground color
    foreground_color = find_foreground_color(input_array)

    # If no foreground color, return the background grid
    if foreground_color == 0:
        return output_array.tolist()

    # Find the row with the maximum count of the foreground color
    max_row_idx = find_max_row(input_array, foreground_color)

    # If the foreground color wasn't actually found (e.g., max count was 0), return background
    if max_row_idx == -1:
         return output_array.tolist()

    # Find all connected components (objects) of the foreground color
    all_objects = find_connected_components(input_array, foreground_color)

    # Identify target objects: those intersecting the max_row_idx
    target_objects_pixels = set()
    for obj_coords in all_objects:
        # Check if any pixel in this object lies on the max_row_idx
        intersects_max_row = any(r == max_row_idx for r, c in obj_coords)
        if intersects_max_row:
            # Add all pixels of this object to the set of pixels to keep
            target_objects_pixels.update(obj_coords)

    # Populate the output grid with the pixels from the target objects
    for r, c in target_objects_pixels:
        # Ensure coordinates are valid just in case (should be by construction)
        if 0 <= r < height and 0 <= c < width:
             output_array[r, c] = foreground_color

    # Convert back to list of lists and return
    return output_array.tolist()