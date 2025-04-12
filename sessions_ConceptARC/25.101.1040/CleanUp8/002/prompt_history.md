
## train_1

**input:**
```
2 2 0 0 0 0 0 0 0 0
6 2 0 0 3 0 0 1 0 0
0 0 1 6 0 0 0 0 0 0
0 0 1 1 0 0 6 0 0 6
0 0 0 0 3 3 0 0 0 0
0 3 0 0 3 3 0 1 0 0
0 0 0 0 0 3 4 4 0 0
0 1 0 0 7 0 4 6 0 0
7 0 0 0 0 0 0 0 5 5
0 0 0 0 3 0 0 0 7 5
```


**output:**
```
2 2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 5 5
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 4 3
0 6 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 4 0 0 6 7 0 0
4 0 0 0 6 6 0 0 0 0
0 1 0 0 6 8 0 0 0 0
0 0 5 5 0 0 0 0 6 0
0 0 1 5 0 0 6 0 0 0
9 9 0 0 0 0 0 0 0 1
8 9 0 0 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0
```

**Perception**

The task involves processing a 2D grid containing various colored pixels. The input grid features multiple small "objects," defined as contiguous blocks of non-white pixels. The output grid retains only a subset of these objects, and the retained objects are always 2x2 squares, filled entirely with the color of the original object. Objects in the input that do not have a bounding box of exactly 2x2 are removed (their pixels are turned white) in the output. The core transformation identifies objects based on their spatial extent (specifically, a 2x2 bounding box) and standardizes their shape to a filled 2x2 square while preserving their color.

**Facts**


```yaml
task_context: Grid transformation focusing on object properties.
components:
  - item: Grid
    attributes:
      - 2D array of integers (0-9) representing colors.
      - Contains background (white, 0) and foreground pixels (non-white).
  - item: Object
    description: A contiguous block of one or more pixels of the same non-white color.
    attributes:
      - color: The integer value (1-9) of the pixels comprising the object.
      - pixels: Set of coordinates (row, col) belonging to the object.
      - bounding_box: The minimal rectangle enclosing all pixels of the object.
        properties:
          - top_left_corner: (min_row, min_col)
          - bottom_right_corner: (max_row, max_col)
          - height: max_row - min_row + 1
          - width: max_col - min_col + 1
relationships:
  - type: Selection criteria
    based_on: Object bounding box dimensions.
    condition: Height must be 2 AND Width must be 2.
actions:
  - action: Identify Objects
    actor: System
    input: Input grid
    output: List of identified objects with their properties (color, pixels, bounding_box).
  - action: Filter Objects
    actor: System
    input: List of identified objects
    condition: Keep only objects where bounding_box height == 2 and bounding_box width == 2.
    output: List of filtered objects.
  - action: Generate Output Grid
    actor: System
    input: Filtered objects and input grid dimensions.
    process: Create a new grid of the same dimensions as the input, initialized to white (0). For each filtered object, fill the 2x2 area defined by its bounding box with the object's color.
    output: Output grid.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid, entirely filled with the background color (white, 0).
2.  Identify all distinct contiguous objects formed by non-white pixels in the input grid.
3.  For each identified object:
    a.  Determine the color of the object.
    b.  Calculate the bounding box of the object (the smallest rectangle containing all its pixels).
    c.  Measure the height and width of the bounding box.
    d.  Check if the height is exactly 2 pixels and the width is exactly 2 pixels.
4.  If an object's bounding box dimensions are 2x2:
    a.  Locate the top-left corner coordinates of its bounding box in the input grid.
    b.  Fill the corresponding 2x2 area in the output grid (starting from the identified top-left corner) with the color of that object.
5.  Leave all other pixels in the output grid as the background color (white, 0).
6.  Return the final output grid.
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
