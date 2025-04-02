
## train_1

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 3 1 1 1 1 1 3 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0
0 0 3 0 3 0 0
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 3 0 0 0 3 0
0 0 3 0 3 0 0
0 0 0 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 0 9 9 9 9 9 0 0 0 0 0 0 0 0
4 0 4 9 4 0 4 9 4 0 4 0 4 0 4 0
0 4 0 9 0 4 0 9 0 4 0 4 0 4 0 4
0 0 0 9 0 0 0 9 0 0 0 0 0 0 0 0
6 0 6 9 9 9 9 9 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0
0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 9 9 9 9
9 0 0 0 9
9 0 0 0 9
9 0 0 0 9
9 9 9 9 9
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 4 0 0
0 4 0 4 0 4 0 4 0 4 0
0 0 4 0 0 0 4 0 0 0 4
4 0 0 6 6 6 0 0 4 0 0
0 4 0 4 0 6 0 4 0 4 0
0 0 4 0 0 6 4 0 0 0 4
4 0 0 6 6 6 0 0 0 0 0
0 4 0 4 0 4 0 0 0 4 0
0 0 4 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 4 0 0 0
```


**output:**
```
6 6 6
0 0 6
0 0 6
6 6 6
```

Okay, I will analyze the provided examples to understand the transformation task.

**Perception of Elements:**

1.  **Input/Output Structure:** Each example consists of an input grid and an output grid. The output grid is generally smaller than the input grid. Both grids contain pixels represented by integers (colors).
2.  **Colors:** The grids use various colors. White (0) often acts as a background. Other colors (Blue, Red, Green, Yellow, Gray, Magenta, Orange, Azure, Maroon) form patterns or shapes.
3.  **Patterns in Input:**
    *   Example 1: Alternating horizontal Blue and White lines, with a sparse pattern of Green pixels mostly on the White lines.
    *   Example 2: Various checkerboard/alternating patterns using Red, Yellow, Magenta, Azure, and Gray. A distinct rectangular shape made of Maroon pixels exists separately from these patterns.
    *   Example 3: Alternating Yellow pixel patterns. A distinct 'T' shape made of Magenta pixels exists.
4.  **Content of Output:**
    *   Example 1: Contains only Green pixels and White pixels, arranged in the same relative configuration as the Green pixels in the input, cropped to their bounding box.
    *   Example 2: Contains only Maroon pixels and White pixels, forming the same hollow rectangle shape as in the input, cropped to its bounding box.
    *   Example 3: Contains only Magenta pixels and White pixels, forming the 'T' shape from the input, cropped to its bounding box.
5.  **Key Observation:** In each case, the output seems to isolate a specific "figure" or "object" from the input grid, discarding the "background" patterns. This figure is defined by a single non-white color. The output grid represents the smallest bounding box around this figure in the input, but only contains pixels of the figure's color (preserving their relative positions) and White pixels for everything else within that box.
6.  **Identifying the Target Object/Color:** The crucial step is identifying which color's shape to extract.
    *   In Ex 1, Green (3) is extracted. Blue (1) forms two distinct lines. Green forms one connected shape.
    *   In Ex 2, Maroon (9) is extracted. All other non-white colors form multiple, small, repeating patterns/objects. Maroon forms one connected shape.
    *   In Ex 3, Magenta (6) is extracted. Yellow (4) forms multiple small patterns/objects. Magenta forms one connected shape.
    *   The rule appears to be: find the non-white color that forms exactly **one** contiguous object (using 8-way adjacency, including diagonals) in the input grid. This color becomes the "target color".

**Facts (YAML):**


```yaml
task_description: Extract a specific object based on its color and connectivity, crop it to its bounding box, and filter out other colors within that box.

definitions:
  - object: A contiguous group of pixels of the same non-white color. Connectivity is 8-way (includes diagonals).
  - background: Pixels of color white (0) or non-white pixels forming repeating patterns or multiple separate objects of the same color.
  - figure: The single non-white object that is targeted for extraction.
  - target_color: The color of the figure object.
  - bounding_box: The smallest rectangle enclosing all pixels of the target_color in the input grid.

transformation_steps:
  - step: Identify the target_color.
    criteria: The target_color is the unique non-white color C such that all pixels of color C in the input grid form exactly one connected object.
  - step: Determine the bounding_box of all pixels with the target_color in the input grid.
    outputs: min_row, max_row, min_col, max_col.
  - step: Create the output grid.
    properties:
      height: max_row - min_row + 1
      width: max_col - min_col + 1
  - step: Populate the output grid.
    logic: For each cell (r, c) in the input grid within the bounding_box (from min_r, min_col to max_r, max_col):
      - If input[r, c] equals the target_color:
          output[r - min_r, c - min_col] = target_color
      - Else:
          output[r - min_r, c - min_col] = white (0)

examples_analysis:
  - example: train_1
    target_color: Green (3) # Forms 1 object, Blue (1) forms 2 objects.
    bounding_box: rows 3-9, cols 3-9 (size 7x7)
    output_derivation: Extract input[3:10, 3:10], keep only Green(3), change others to White(0).
  - example: train_2
    target_color: Maroon (9) # Forms 1 object, other colors form multiple objects.
    bounding_box: rows 3-7, cols 3-7 (size 5x5)
    output_derivation: Extract input[3:8, 3:8], keep only Maroon(9), change others to White(0).
  - example: train_3
    target_color: Magenta (6) # Forms 1 object, Yellow (4) forms multiple objects.
    bounding_box: rows 4-7, cols 4-6 (size 4x3)
    output_derivation: Extract input[4:8, 4:7], keep only Magenta(6), change others to White(0).

```


**Natural Language Program:**

1.  Analyze the input grid to identify all unique non-white colors present.
2.  For each unique non-white color, determine how many separate contiguous objects (using 8-way adjacency) are formed by pixels of that color.
3.  Identify the single "target color" which forms exactly one contiguous object.
4.  Locate all pixels in the input grid that have this target color.
5.  Determine the minimum and maximum row and column indices occupied by these target color pixels to define their bounding box.
6.  Calculate the height and width of the bounding box.
7.  Create a new output grid with these dimensions.
8.  Iterate through each position (row `r`, column `c`) within the bounding box region of the original input grid.
9.  For the corresponding position (`r` minus `min_row`, `c` minus `min_col`) in the output grid: if the input grid pixel at (`r`, `c`) has the target color, copy the target color to the output grid; otherwise, set the output grid pixel to white (0).
10. Return the generated output grid.
```python
import numpy as np
from collections import deque

"""
Identify the unique non-white color C such that all pixels of color C in the input grid form exactly one connected object (using 8-way adjacency).
Determine the bounding box of this single object.
Create an output grid sized to this bounding box.
Populate the output grid: place the target color C at the relative positions corresponding to the object's pixels in the input, and fill the rest with white (0).
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in a grid using 8-way adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a single connected object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    # Define 8-way neighbors (including diagonals)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and not yet visited, start a search (BFS)
            if grid[r, c] == color and not visited[r, c]:
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object.add((curr_r, curr_c))

                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Add the found object to the list
                objects.append(current_object)

    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the described logic.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Find unique non-white colors
    unique_colors = np.unique(input_array)
    non_white_colors = unique_colors[unique_colors != 0]

    target_color = -1
    target_object_coords = None

    # Identify the target color (forms exactly one object)
    for color in non_white_colors:
        objects = find_objects(input_array, color)
        if len(objects) == 1:
            target_color = color
            target_object_coords = objects[0] # Get the set of coordinates
            break # Found the target color

    # Handle case where no suitable object is found (shouldn't happen based on examples)
    if target_color == -1 or not target_object_coords:
        # Return an empty grid or raise an error, depending on requirements
        # For now, return a 1x1 white grid as a placeholder
        return [[0]] 

    # Determine the bounding box of the target object
    min_row = rows
    max_row = -1
    min_col = cols
    max_col = -1
    for r, c in target_object_coords:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    # Calculate output grid dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Create the output grid, initialized with white (0)
    output_array = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid
    for r, c in target_object_coords:
        # Calculate relative coordinates within the bounding box
        relative_r = r - min_row
        relative_c = c - min_col
        # Place the target color in the output grid
        output_array[relative_r, relative_c] = target_color

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
