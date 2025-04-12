import collections

"""
This transformation filters objects in a grid based on their shape and the relative counts of different shape types.

1. Identify all distinct objects (connected groups of non-white pixels) in the input grid.
2. For each object, determine if it forms a 'solid rectangle'. An object is a solid rectangle if its pixels perfectly fill its bounding box.
3. Classify objects into two categories: 'solid_rectangle' and 'non_solid_rectangle'.
4. Count the number of objects in each category.
5. If the counts are equal, keep only the 'solid_rectangle' objects in the output grid.
6. If the counts are unequal, keep only the 'non_solid_rectangle' objects in the output grid.
7. Removed objects are replaced with the background color (white, 0).
"""

def find_objects(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Identifies all distinct objects in the grid.
    An object is a connected group of pixels of the same non-white color.
    Uses Breadth-First Search (BFS) for connectivity (orthogonal adjacency).

    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        A list where each element represents an object. Each object is represented
        as a tuple containing its color and a list of its pixel coordinates (row, col).
        e.g., [(color1, [(r1, c1), (r2, c2), ...]), (color2, [(r3, c3), ...]), ...]
    """
    height = len(grid)
    width = len(grid[0])
    visited = [[False for _ in range(width)] for _ in range(height)]
    objects = []

    for r in range(height):
        for c in range(width):
            # Check if the pixel is part of an object and not yet visited
            if grid[r][c] != 0 and not visited[r][c]:
                color = grid[r][c]
                object_pixels = []
                q = collections.deque([(r, c)])
                visited[r][c] = True

                while q:
                    row, col = q.popleft()
                    object_pixels.append((row, col))

                    # Explore neighbors (orthogonal)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr][nc] == color and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                
                if object_pixels: # Should always be true if we entered the loop
                    objects.append((color, object_pixels))

    return objects

def get_bounding_box(pixels: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return 0, 0, 0, 0 # Should not happen for valid objects
    
    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)
    return min_row, max_row, min_col, max_col

def is_solid_rectangle(pixels: list[tuple[int, int]]) -> bool:
    """Checks if an object represented by its pixels forms a solid rectangle."""
    if not pixels:
        return False # Empty object cannot be solid
        
    pixel_count = len(pixels)
    min_row, max_row, min_col, max_col = get_bounding_box(pixels)
    
    bbox_height = max_row - min_row + 1
    bbox_width = max_col - min_col + 1
    bbox_area = bbox_height * bbox_width
    
    return pixel_count == bbox_area

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Filters objects in the input grid based on whether they are solid rectangles
    and the relative counts of solid vs. non-solid objects.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid with white (0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 1. Find all objects in the input grid
    all_objects = find_objects(input_grid)

    # 2. Classify objects and store them
    solid_objects = []
    non_solid_objects = []
    for color, pixels in all_objects:
        if is_solid_rectangle(pixels):
            solid_objects.append((color, pixels))
        else:
            non_solid_objects.append((color, pixels))

    # 3. Determine which category of objects to keep
    count_solid = len(solid_objects)
    count_non_solid = len(non_solid_objects)
    
    objects_to_keep = []
    if count_solid == count_non_solid:
        # Keep solid rectangles
        objects_to_keep = solid_objects
    else:
        # Keep non-solid rectangles
        objects_to_keep = non_solid_objects

    # 4. Draw the kept objects onto the output grid
    for color, pixels in objects_to_keep:
        for r, c in pixels:
            # Ensure coordinates are valid (should be, but good practice)
            if 0 <= r < height and 0 <= c < width:
                output_grid[r][c] = color

    return output_grid