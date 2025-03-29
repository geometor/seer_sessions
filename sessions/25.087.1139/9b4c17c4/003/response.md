```python
import numpy as np
from collections import deque

"""
Identifies contiguous red (2) objects. For each object, determines the color 
(blue=1 or gray=8) of the immediately surrounding background region. Finds the 
horizontal boundaries (min and max column) of that specific background region. 
Moves the red object horizontally:
- If the background is gray (8), the object moves so its leftmost pixel aligns 
  with the minimum column index of the gray background region.
- If the background is blue (1), the object moves so its rightmost pixel aligns 
  with the maximum column index of the blue background region.
The object's shape, size, and vertical position are preserved. The original 
location is filled with the background color. Other grid areas remain unchanged.
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

def get_background_info(grid, obj_pixels):
    """
    Determines the background color immediately surrounding a given object and
    finds one coordinate within that background region.

    Args:
        grid (np.array): The input grid.
        obj_pixels (list): List of coordinates [(r, c)] for the object pixels.

    Returns:
        tuple: (background_color, background_coord) where background_coord
               is a tuple (r, c) of a pixel adjacent to the object belonging
               to the background. Returns (-1, None) if no non-object neighbor
               is found or if the neighbor is the object color itself.
    """
    height, width = grid.shape
    object_color = 2 # Color of the object we are checking neighbors for
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
                     # We expect background colors 1 (blue) or 8 (gray)
                     if neighbor_color != object_color:
                         return neighbor_color, (nr, nc) # Return color and a coordinate

    # Fallback case: No valid background neighbor found
    print(f"Warning: No valid background neighbor found for object starting at {obj_pixels[0] if obj_pixels else 'N/A'}")
    return -1, None


def find_background_region_bounds(grid, start_coord, background_color):
    """
    Finds the minimum and maximum column indices of a contiguous region
    of a specific background color, starting from a given coordinate. Uses BFS.

    Args:
        grid (np.array): The input grid.
        start_coord (tuple): A coordinate (r, c) known to be in the region.
        background_color (int): The color of the background region to trace.

    Returns:
        tuple: (min_col, max_col) representing the horizontal bounds of the region.
               Returns (start_coord[1], start_coord[1]) if the region is just
               the start coordinate or if start_coord is invalid.
    """
    height, width = grid.shape
    if not (0 <= start_coord[0] < height and 0 <= start_coord[1] < width and grid[start_coord] == background_color):
        # Handle cases where the start coordinate is invalid
        print(f"Warning: Invalid start_coord {start_coord} or color mismatch for find_background_region_bounds.")
        # Attempt to return a minimal valid bound if possible, otherwise indicate error potential
        if 0 <= start_coord[1] < width:
           return (start_coord[1], start_coord[1])
        else:
           return (0, 0) # Or raise an error


    visited = np.zeros_like(grid, dtype=bool)
    q = deque([start_coord])
    visited[start_coord] = True
    min_c = start_coord[1]
    max_c = start_coord[1]

    while q:
        curr_r, curr_c = q.popleft()

        # Update horizontal bounds
        min_c = min(min_c, curr_c)
        max_c = max(max_c, curr_c)

        # Explore 4 adjacent neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if the neighbor is within grid bounds, has the background color, and hasn't been visited
            if (0 <= nr < height and 0 <= nc < width and
                    grid[nr, nc] == background_color and not visited[nr, nc]):
                visited[nr, nc] = True
                q.append((nr, nc))

    return min_c, max_c


def transform(input_grid):
    """
    Transforms the input grid by moving red objects horizontally within their
    respective background regions (blue or gray) to the region's edge.

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

        # Determine the background color and a starting coordinate within it
        background_color, bg_start_coord = get_background_info(input_grid_np, obj_pixels)

        # Check if valid background info was found
        if background_color == -1 or bg_start_coord is None:
            print(f"Warning: Could not determine valid background info for object at {obj_pixels[0]}. Skipping object.")
            continue # Skip processing this object

        # We only handle blue (1) and gray (8) backgrounds as per the examples
        if background_color not in [1, 8]:
            print(f"Warning: Unexpected background color {background_color} found for object at {obj_pixels[0]}. Skipping object.")
            continue

        # Find the horizontal boundaries of this specific background region
        min_bg_c, max_bg_c = find_background_region_bounds(input_grid_np, bg_start_coord, background_color)

        # Find the min/max column indices of the red object itself
        min_obj_c = min(c for r, c in obj_pixels)
        max_obj_c = max(c for r, c in obj_pixels)

        # Calculate the required horizontal shift (column offset)
        offset_c = 0
        if background_color == 8:  # Gray background: move object to left edge of region
            offset_c = min_bg_c - min_obj_c
        elif background_color == 1:  # Blue background: move object to right edge of region
            offset_c = max_bg_c - max_obj_c
            
        # --- Apply Transformation ---
        
        # 1. Erase the object from its original position in the output grid.
        # Fill the original object locations with their determined background color.
        for r, c in obj_pixels:
             # Check bounds just in case, though r,c should be valid from find_objects
             if 0 <= r < height and 0 <= c < width:
                 output_grid[r, c] = background_color

        # 2. Draw the object (color 2) at its new, shifted position in the output grid
        for r, c in obj_pixels:
            new_c = c + offset_c
            # Ensure the new column index is within the grid's width bounds
            if 0 <= new_c < width:
                 # Check bounds for row as well
                 if 0 <= r < height:
                     output_grid[r, new_c] = 2 # Draw the red pixel at the new location
            else:
                # This might happen if region detection or shift calculation is flawed
                 print(f"Warning: Pixel ({r},{c})'s new calculated column {new_c} is out of bounds [0, {width-1}] during draw")

    # Convert the final numpy array grid back to a list of lists for the required output format
    return output_grid.tolist()
```