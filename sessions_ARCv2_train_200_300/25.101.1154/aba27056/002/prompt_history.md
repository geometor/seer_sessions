
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7
0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
0 0 0 0 7 0 0 0 7
0 0 0 0 7 7 7 7 7
```


**output:**
```
4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 4 0 7 7 7 7 7
0 0 0 4 7 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
4 4 4 4 4 4 4 4 7
0 0 0 4 7 4 4 4 7
0 0 4 0 7 7 7 7 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 6 6 0 6 6 0
0 6 0 0 0 6 0
0 6 6 6 6 6 0
```


**output:**
```
0 0 0 4 0 0 0
4 0 0 4 0 0 4
0 4 0 4 0 4 0
0 0 4 4 4 0 0
0 6 6 4 6 6 0
0 6 4 4 4 6 0
0 6 6 6 6 6 0
```


## train_3

**input:**
```
3 3 3 3 3 3
3 0 0 0 0 3
3 0 0 0 0 3
3 3 0 0 3 3
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3
3 4 4 4 4 3
3 4 4 4 4 3
3 3 4 4 3 3
0 4 4 4 4 0
4 0 4 4 0 4
```

**Perception:**

The task involves transforming an input grid containing a white background (0) and one or more shapes made of a single non-white color (foreground color) into an output grid. The foreground shapes from the input are preserved in the output. The transformation focuses on changing the color of some white pixels to yellow (4).

Observing the examples:
1.  **Train 1:** An orange (7) shape like '3'. The white area connected to the grid boundary, spreading around the '3', is filled with yellow (4). The white pixels technically "inside" the curves of the '3' are also filled yellow, suggesting they are reachable from the boundary fill.
2.  **Train 2:** A magenta (6) shape like an 'H'. The white area outside the 'H' connected to the boundary is filled yellow. The white area enclosed within the 'H' is also filled yellow. Both regions become connected via 4-connectivity through the gaps in the 'H'.
3.  **Train 3:** Green (3) shapes forming an outer frame and an inner rectangle. The white area between the frames and the white area in the bottom rows (connected to the boundary) appear to be targeted for filling. However, comparing the input white pixels and output yellow/white pixels shows a specific pattern: not all white pixels reachable from the boundary are filled yellow. Specifically, white pixels adjacent to the green frame at (4,0), (4,5) and white pixels on the boundary at (5,1), (5,4), plus internal white pixels (3,1), (3,4) remain white
, while others reachable from the boundary turn yellow.

The common logic appears to be a "flood fill" originating from the grid boundary. The fill color is yellow (4), and it spreads through connected white (0) pixels, stopping when it hits a non-white pixel. The discrepancy in Train 3 suggests either a subtlety in the rule or a potential ambiguity in interpreting the output image provided. Assuming the core logic is consistent, the most likely rule is a standard flood fill from boundary white pixels.

**YAML Facts:**


```yaml
task_type: flood_fill
grid_properties:
  size: variable, input and output grids have the same dimensions.
  background_color: white (0)
  fill_color: yellow (4)
objects:
  - id: foreground_shape
    description: Contiguous shape(s) made of a single non-white color present in the input. Acts as a barrier to the fill.
    color: variable (orange 7, magenta 6, green 3 in examples)
  - id: background_pixels
    description: Pixels with the background color (white 0). These are candidates for filling.
    color: white (0)
actions:
  - name: identify_boundary_pixels
    input: input grid
    output: coordinates of all white (0) pixels located on the grid edges (row 0, row H-1, col 0, col W-1).
  - name: flood_fill
    description: Starting from a set of source pixels, fill connected background pixels with the fill color, stopping at non-background pixels.
    parameters:
      source_pixels: result of identify_boundary_pixels
      fill_color: yellow (4)
      background_color: white (0)
      barrier_colors: all colors except white (0)
      connectivity: 4-way adjacency (up, down, left, right)
transformation:
  - step: Initialize the output grid as a copy of the input grid.
  - step: Identify the set of source pixels for the fill (white pixels on the boundary).
  - step: Perform a flood fill operation starting from the source pixels.
  - step: The flood fill propagates through white (0) pixels only.
  - step: When a white pixel is visited by the flood fill, change its color to yellow (4) in the output grid.
  - step: The flood fill is blocked by any non-white pixel in the input grid.
  - step: Pixels of the foreground shape remain unchanged. White pixels not reached by the flood fill remain white.
```


**Natural Language Program:**

1.  Create the output grid by copying the input grid.
2.  Identify all white pixels (color 0) that are located on the outermost border (top row, bottom row, leftmost column, rightmost column) of the input grid. These are the starting points for the fill.
3.  Initiate a flood fill process using the identified starting points.
4.  The fill color is yellow (color 4).
5.  The fill spreads from a filled pixel to its adjacent (up, down, left, right) neighbors only if the neighbor is within the grid boundaries and is currently white (color 0).
6.  When a white pixel is filled, change its color to yellow (4) in the output grid. Mark it as visited to avoid re-processing.
7.  The fill process stops spreading when it encounters a pixel that is not white (i.e., part of the original foreground shape) or reaches the grid boundaries.
8.  Continue the process until no more white pixels can be reached and filled from the initial boundary starting points.
9.  The resulting output grid reflects the original foreground shape(s) and the newly filled yellow areas.
```python
import copy
from collections import deque

"""
Transformation Rule:

1.  Identify all white (0) pixels located on the grid boundary (edges).
2.  Perform a flood fill operation starting from these boundary white pixels.
3.  The fill color is yellow (4).
4.  The fill spreads only to adjacent (up, down, left, right) white (0) pixels.
5.  Non-white pixels act as barriers, stopping the fill.
6.  The original non-white shapes remain unchanged. White pixels not reached by the fill also remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills the white areas (0) connected to the boundary with yellow (4),
    stopping at non-white pixels.
    """
    
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Define fill color and background color
    fill_color = 4
    background_color = 0

    # Initialize a queue for the flood fill (BFS)
    queue = deque()

    # Identify boundary white pixels and add them to the queue
    # Also, immediately color them in the output grid to mark as visited/source
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on the boundary
            is_boundary = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            
            # If it's a white pixel on the boundary, start fill from here
            if is_boundary and output_grid[r][c] == background_color:
                if output_grid[r][c] == background_color: # Check again to avoid duplicates if already processed
                    output_grid[r][c] = fill_color
                    queue.append((r, c))

    # Define 4-way adjacent neighbors (dx, dy)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform the flood fill using BFS
    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a background pixel (unvisited)
                if output_grid[nr][nc] == background_color:
                    # Change color to fill color
                    output_grid[nr][nc] = fill_color
                    # Add neighbor to the queue to process its neighbors
                    queue.append((nr, nc))

    # Return the modified grid
    return output_grid
```
