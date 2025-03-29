```python
import numpy as np
from collections import deque

"""
Identifies contiguous objects of red (2) pixels within the input grid.
Determines the background color (blue (1) or gray (8)) immediately surrounding each red object.
Moves each red object horizontally to an edge of the grid based on its background color:
- If the background is gray (8), the object moves to the left edge (column 0), aligning its leftmost pixel with column 0.
- If the background is blue (1), the object moves to the right edge (last column), aligning its rightmost pixel with the last column index.
The object's shape, size, and vertical position (row indices) are preserved during the move.
The original background layout (blue and gray areas) is maintained, except where objects are moved from or to.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects. Each object is represented as a list of
              pixel coordinates [(row1, col1), (row2, col2), ...]. Returns
              an empty list if no objects of the specified color are found.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            # Check if the current cell has the target color and hasn't been visited yet
            if grid[r, c] == color and not visited[r, c]:
                # Found the start of a new object, begin BFS
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))
                    # Explore 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                # Add the completed object's pixels to the list if it's not empty
                if current_object_pixels:
                    objects.append(current_object_pixels)
    return objects

def get_background_color(grid, obj_pixels):
    """
    Determines the background color immediately surrounding a given object.
    It checks the neighbors of the object's pixels.

    Args:
        grid (np.array): The input grid.
        obj_pixels (list): List of coordinates [(r, c)] for the object pixels.

    Returns:
        int: The background color (e.g., 1 for blue, 8 for gray).
             Returns -1 if no non-object neighbor is found (should not happen
             based on task constraints).
    """
    height, width = grid.shape
    object_color = 2 # We are looking for neighbors of red objects
    object_coords_set = set(obj_pixels) # Use a set for efficient neighbor checking

    # Iterate through each pixel belonging to the object
    for r, c in obj_pixels:
        # Check its 4 adjacent neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is NOT part of the object itself
                if (nr, nc) not in object_coords_set:
                     neighbor_color = grid[nr, nc]
                     # Return the color of the first valid non-object neighbor found
                     # Assumes the background is consistent around the object.
                     return neighbor_color
                     
    # Fallback case: Should not be reached if objects always have non-object neighbors
    print(f"Warning: No background neighbor found for object starting at {obj_pixels[0] if obj_pixels else 'N/A'}")
    return -1


def transform(input_grid):
    """
    Transforms the input grid by finding red objects, determining their
    surrounding background color, and moving them horizontally to the
    grid edge corresponding to that background color (left for gray,
    right for blue), preserving shape and vertical position.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Create the output grid, initially as a copy of the input
    output_grid = input_grid_np.copy()

    # Find all distinct red (color 2) objects in the input grid
    red_objects = find_objects(input_grid_np, 2)

    # Process each found red object
    for obj_pixels in red_objects:
        # Skip if the object finding somehow returned an empty list
        if not obj_pixels:
            continue

        # Determine the background color surrounding this object
        background_color = get_background_color(input_grid_np, obj_pixels)
        
        # If a valid background color wasn't found, skip this object (with a warning)
        if background_color == -1 or background_color == 2: # Should be 1 or 8
             print(f"Warning: Could not determine valid background (found {background_color}) for object at {obj_pixels[0]}")
             continue # Skip processing this object

        # Find the min/max column indices to know the object's horizontal span and reference points
        min_c = min(c for r, c in obj_pixels)
        max_c = max(c for r, c in obj_pixels)

        # Erase the object from its original position in the output grid.
        # Fill the original object locations with their determined background color.
        for r, c in obj_pixels:
            output_grid[r, c] = background_color

        # Calculate the required horizontal shift (column offset) based on the background color
        offset_c = 0
        if background_color == 8:  # Gray background: move object to left edge
            # Shift needed to align the object's leftmost pixel (min_c) with column 0
            offset_c = 0 - min_c
        elif background_color == 1:  # Blue background: move object to right edge
            # Shift needed to align the object's rightmost pixel (max_c) with the last column (width - 1)
            offset_c = (width - 1) - max_c
        # Note: No 'else' needed here due to the check after get_background_color

        # Draw the object (color 2) at its new, shifted position in the output grid
        for r, c in obj_pixels:
            new_c = c + offset_c
            # Ensure the new column index is within the grid's width bounds
            if 0 <= new_c < width:
                output_grid[r, new_c] = 2 # Draw the red pixel at the new location
            else:
                # This should ideally not happen if calculations are correct and objects fit
                 print(f"Warning: Pixel ({r},{c})'s new calculated column {new_c} is out of bounds [0, {width-1}]")

    # Convert the final numpy array grid back to a list of lists for the required output format
    return output_grid.tolist()
```