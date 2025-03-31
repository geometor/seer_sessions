import numpy as np
from collections import Counter, deque

"""
This module transforms input grids according to specific rules based on object shape and color.

Transformation Rules:
1. Identify the background color (most frequent color).
2. Find all distinct, contiguous objects of non-background colors.
3. Analyze each object based on its size (pixel count) and color:
    a. Objects with 13 pixels ('diamond' shape) are removed (replaced by the background color).
    b. Objects with 9 pixels ('plus_sign' shape) are processed as follows:
        i. If the color is maroon(9), magenta(6), or green(3), change the object's color to gray(5).
        ii. If the color is orange(7), remove the object (replace with background color).
        iii. If the color is white(0) AND the background color is magenta(6), remove the object.
        iv. Otherwise (blue(1), yellow(4), azure(8), red(2), or white(0) with non-magenta background), the object remains unchanged.
4. The background and any objects not matching the above criteria remain unchanged.
"""

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color of the grid.

    Returns:
        list: A list of tuples, where each tuple represents an object
              and contains (color, list_of_pixel_coordinates).
              Example: [(3, [(1,1), (1,2), (2,1)]) , ...]
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If pixel is not background and not visited, start a search (BFS)
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    # Only add pixels that actually belong to this object
                    if grid[row, col] == color:
                         obj_pixels.append((row, col))
                         # Explore neighbors (up, down, left, right)
                         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = row + dr, col + dc
                            # Check boundaries, if neighbor has the same color, and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                            grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                    # else: # This pixel belongs to a different object or background, but was visited because it was adjacent to a previous queue item. Ignore it for this object.
                    #    pass
                
                # Check if any pixels were actually added (handles edge cases where initial pixel doesn't match color?)
                if obj_pixels:
                     objects.append((color, obj_pixels))
            
            # Mark background pixels as visited to avoid starting searches from them
            elif grid[r,c] == background_color:
                 visited[r,c] = True


    return objects


def transform(input_grid):
    """
    Applies transformations to objects in the input grid based on their shape (pixel count) and color.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Identify the background color
    # Flatten the grid, count occurrences, find the most common
    colors, counts = np.unique(grid, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Find all distinct objects
    objects = find_objects(grid, background_color)

    # 3. Iterate through objects and apply rules
    for color, pixels in objects:
        size = len(pixels)
        
        # Rule 3a: Remove 13-pixel objects (diamonds)
        if size == 13:
            for r, c in pixels:
                output_grid[r, c] = background_color
        
        # Rule 3b: Process 9-pixel objects (plus signs)
        elif size == 9:
            # Rule 3b.i: Recolor maroon(9), magenta(6), green(3) to gray(5)
            if color in [9, 6, 3]:
                for r, c in pixels:
                    output_grid[r, c] = 5 # Gray
            # Rule 3b.ii: Remove orange(7)
            elif color == 7:
                for r, c in pixels:
                    output_grid[r, c] = background_color
            # Rule 3b.iii: Remove white(0) if background is magenta(6)
            elif color == 0 and background_color == 6:
                 for r, c in pixels:
                    output_grid[r, c] = background_color
            # Rule 3b.iv: Otherwise (blue(1), yellow(4), azure(8), red(2), or white(0) with non-magenta bg), leave unchanged.
            # No action needed here as output_grid is a copy initially.

    # Convert back to list of lists for the required output format
    return output_grid.tolist()