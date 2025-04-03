
## train_1

**input:**
```
0 0 6 6 6 6 6 0 0 0 6 6 0 6 6 0 0 0 6 6 6 6 0 6 6 6 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 0 0 0 9 9 0 9 9 0 0 0 9 9 9 9 0 3 3 3 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 6 6 0 6 0 0 6 6 6 0 0 0 6 6 6 6 6 0 0 0 6 6 6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 0 3 0 0 3 3 3 0 0 0 3 3 3 3 3 0 0 0 9 9 9 9 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 6 6 0 0 0 6 6 6 0 0 6 6 6 0 6 6 6 0 0 6 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 0 0 0 3 3 3 0 0 3 3 3 0 3 3 3 0 0 3 0 0 0 0 0 0 0 0 0 0 0
```

**Perception**

1.  **Input/Output Structure:** Both input and output are grids of the same dimensions.
2.  **Background:** The background color is white (0) and remains unchanged in the output.
3.  **Objects:** The input grid contains distinct, contiguous objects composed solely of magenta (6) pixels. These objects vary in shape and size across the examples.
4.  **Transformation:** The magenta (6) pixels in the input are transformed into either green (3) or maroon (9) pixels in the output. The spatial arrangement and shape of the original magenta objects are preserved in the output, but their color changes.
5.  **Color Change Logic:** The determining factor for the output color (green or maroon) appears to be the size (number of pixels) of the original magenta object. Objects with an odd number of pixels become green (3), while objects with an even number of pixels become maroon (9).

**Facts**


```yaml
Input Grid:
  - Contains a background color: white (0)
  - Contains foreground objects composed of a single color: magenta (6)

Objects:
  - Type: Contiguous clusters of magenta (6) pixels.
  - Properties:
    - Color: magenta (6)
    - Size: Variable number of pixels per object.
    - Shape: Variable shapes.
  - Identification: Defined by adjacency (side-by-side or diagonal) of magenta pixels.

Transformation:
  - Target: Pixels within magenta (6) objects.
  - Action: Recolor magenta (6) pixels based on a property of the object they belong to.
  - Rule:
    - Determine the size (pixel count) of each distinct magenta object.
    - If the object's size is odd: change all its pixels to green (3).
    - If the object's size is even: change all its pixels to maroon (9).
  - Non-Target Pixels: White (0) background pixels remain unchanged.

Output Grid:
  - Retains the same dimensions as the input.
  - Background remains white (0).
  - Original magenta objects are replaced by objects of the same shape but colored either green (3) or maroon (9) based on the size rule.
```


**Natural Language Program**

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all distinct, contiguous objects composed of magenta (6) pixels in the input grid. Use 8-way connectivity (including diagonals) to define contiguity.
3.  For each identified magenta object:
    a.  Calculate its size by counting the number of magenta pixels it contains.
    b.  Determine if the size is odd or even.
    c.  If the size is odd, change the color of all pixels belonging to this object in the output grid to green (3).
    d.  If the size is even, change the color of all pixels belonging to this object in the output grid to maroon (9).
4.  Leave all non-magenta pixels (white, 0) unchanged in the output grid.
5.  Return the modified output grid.
```python
import collections
import copy

"""
Identifies distinct, contiguous objects composed of magenta (6) pixels in the input grid using 8-way connectivity.
For each identified magenta object, it calculates its size (number of pixels).
If the object's size is odd, all its pixels in the output grid are changed to green (3).
If the object's size is even, all its pixels in the output grid are changed to maroon (9).
All non-magenta pixels (e.g., white/0 background) remain unchanged.
"""

def find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in a grid.

    Args:
        grid (list[list[int]]): The input grid.
        target_color (int): The color of the components to find.

    Returns:
        list[list[tuple[int, int]]]: A list where each element is a list
                                     of (row, col) tuples representing a
                                     single connected component.
    """
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    components = []

    # Define 8 directions for connectivity (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for r in range(rows):
        for c in range(cols):
            # If the cell is the target color and hasn't been visited yet,
            # start a Breadth-First Search (BFS) to find its component
            if grid[r][c] == target_color and not visited[r][c]:
                component_pixels = []
                queue = collections.deque([(r, c)])
                visited[r][c] = True

                while queue:
                    curr_r, curr_c = queue.popleft()
                    component_pixels.append((curr_r, curr_c))

                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor is the target color and not visited
                            if grid[nr][nc] == target_color and not visited[nr][nc]:
                                visited[nr][nc] = True
                                queue.append((nr, nc))

                if component_pixels:
                    components.append(component_pixels)

    return components

def transform(input_grid):
    """
    Transforms the input grid based on the size of magenta (6) objects.
    Odd-sized magenta objects become green (3).
    Even-sized magenta objects become maroon (9).
    Other pixels remain unchanged.

    Args:
        input_grid (list[list[int]]): The input grid represented as a 2D list of integers.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input to preserve background
    output_grid = copy.deepcopy(input_grid)
    magenta_color = 6
    green_color = 3
    maroon_color = 9

    # Find all connected components (objects) of magenta pixels
    magenta_objects = find_connected_components(input_grid, magenta_color)

    # Process each magenta object
    for obj_pixels in magenta_objects:
        # Calculate the size of the object
        object_size = len(obj_pixels)

        # Determine the output color based on whether the size is odd or even
        if object_size % 2 != 0:  # Odd size
            output_color = green_color
        else:  # Even size
            output_color = maroon_color

        # Change the color of all pixels belonging to this object in the output grid
        for r, c in obj_pixels:
            output_grid[r][c] = output_color

    return output_grid
```
