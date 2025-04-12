```python
import collections

def find_objects(grid: list[list[int]]) -> list[tuple[int, set[tuple[int, int]]]]:
    """
    Identifies all distinct contiguous objects of non-white pixels in the grid.

    Args:
        grid: The input 2D list representing the grid.

    Returns:
        A list of tuples, where each tuple contains:
        - The color (int) of the object.
        - A set of (row, col) tuples representing the pixels of the object.
    """
    if not grid:
        return []
    
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                obj_pixels = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append((color, obj_pixels))
                    
    return objects

def calculate_bounding_box(pixels: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the bounding box of a set of pixels.

    Args:
        pixels: A set of (row, col) tuples.

    Returns:
        A tuple containing (min_row, min_col, height, width).
        Returns (0, 0, 0, 0) if pixels is empty.
    """
    if not pixels:
        return 0, 0, 0, 0
        
    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    return min_row, min_col, height, width

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by performing the following steps:
    1. Finds all contiguous objects of non-white pixels.
    2. Calculates the bounding box for each object.
    3. Filters objects whose bounding box dimensions are exactly 2x2.
    4. Creates an output grid initialized to white (0).
    5. For each filtered object, fills the 2x2 area corresponding to its 
       bounding box in the output grid with the object's color.
    """
    if not input_grid:
        return []
        
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid with background color (white, 0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # 1. Identify all distinct contiguous objects
    objects = find_objects(input_grid)
    
    # Iterate through each identified object
    for color, pixels in objects:
        # 2. Calculate the bounding box
        min_row, min_col, bb_height, bb_width = calculate_bounding_box(pixels)
        
        # 3. Check if the bounding box is exactly 2x2
        if bb_height == 2 and bb_width == 2:
            # 4. & 5. Fill the corresponding 2x2 area in the output grid
            # Ensure coordinates are within bounds (although should be correct)
            for r in range(min_row, min_row + 2):
                for c in range(min_col, min_col + 2):
                    if 0 <= r < height and 0 <= c < width:
                        output_grid[r][c] = color

    return output_grid
```