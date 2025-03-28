import collections
import copy

"""
Identifies distinct contiguous objects composed of non-background (non-zero) pixels 
using side-adjacency. For each object found, it determines the set of unique 
non-background colors present within it. If an object contains exactly two distinct 
non-background colors, it iterates through the pixels of that object in the output 
grid (initially a copy of the input) and swaps the two identified colors. Pixels 
that are part of objects not containing exactly two non-background colors, or 
background pixels (color 0), remain unchanged.
"""

def _find_objects(grid, height, width):
    """
    Finds all distinct contiguous objects of non-background pixels using BFS.
    
    Args:
        grid (list[list[int]]): The input grid.
        height (int): The height of the grid.
        width (int): The width of the grid.

    Returns:
        list[tuple[set[tuple[int, int]], set[int]]]: 
            A list of objects. Each object is represented as a tuple containing:
            - A set of (row, col) tuples representing the coordinates of the pixels in the object.
            - A set of integers representing the unique non-background colors present in the object.
    """
    visited = [[False for _ in range(width)] for _ in range(height)]
    objects = []

    for r in range(height):
        for c in range(width):
            # Start BFS if we find a non-background pixel (color != 0) that hasn't been visited
            if grid[r][c] != 0 and not visited[r][c]:
                object_pixels = set()
                object_colors = set()
                q = collections.deque([(r, c)])
                visited[r][c] = True

                # Perform BFS to find all connected non-background pixels
                while q:
                    curr_r, curr_c = q.popleft()
                    pixel_color = grid[curr_r][curr_c]

                    # Record pixel coordinate
                    object_pixels.add((curr_r, curr_c))
                    # Only add non-background colors to the object's color set
                    if pixel_color != 0:
                        object_colors.add(pixel_color)

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor is part of the same object (non-background) 
                            # and hasn't been visited yet
                            if grid[nr][nc] != 0 and not visited[nr][nc]:
                                visited[nr][nc] = True
                                q.append((nr, nc))

                # Once BFS for an object is complete, store its pixels and unique non-background colors
                # Ensure the object is not empty (shouldn't happen with the check `grid[r][c] != 0` but good practice)
                if object_pixels: 
                    objects.append((object_pixels, object_colors))

    return objects


def transform(input_grid):
    """
    Transforms the input grid by swapping colors within objects that contain exactly two 
    distinct non-background colors.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    """
    # Handle empty input grid scenario
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid.
    # This ensures that unchanged pixels and objects retain their original values.
    output_grid = copy.deepcopy(input_grid)

    # Find all distinct contiguous objects of non-background pixels in the input grid.
    # Each object contains its pixel coordinates and the set of unique non-background colors it holds.
    objects = _find_objects(input_grid, height, width)

    # Iterate through each identified object to apply the transformation rule.
    for object_pixels, object_colors in objects:
        
        # Check if the object contains exactly two distinct non-background colors.
        if len(object_colors) == 2:
            # Extract the two colors to be swapped. Convert set to tuple or list.
            color_a, color_b = tuple(object_colors)

            # Iterate through each pixel belonging to the current object.
            for r, c in object_pixels:
                # IMPORTANT: Check the color in the *original* input_grid to decide the swap.
                # Modify the corresponding pixel in the *output_grid*.
                if input_grid[r][c] == color_a:
                    output_grid[r][c] = color_b
                elif input_grid[r][c] == color_b:
                    output_grid[r][c] = color_a
                # Pixels within the object that might somehow not match color_a or color_b 
                # (e.g., if the object definition included background accidentally, which it shouldn't)
                # would remain unchanged in the output grid, matching the input grid.
        
        # Else (if the object has 1 or >2 unique non-background colors):
            # No action is needed. The pixels for this object in the output_grid 
            # already hold the correct values copied from the input_grid.

    # Background pixels (color 0) were never part of any object and remain unchanged 
    # because output_grid started as a copy of input_grid.

    # Return the modified output grid.
    return output_grid