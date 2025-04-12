
## train_1

**input:**
```
0 0 5 0 0 5 0 5 0 0 0 5 0
5 0 0 0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 0 0 5 0 5 0 0
```


**output:**
```
0 0 3 0 0 5 0 5 0 0 0 5 0
3 0 0 0 3 0 3 0 0 5 0 0 3
0 5 0 5 0 0 0 0 3 0 3 0 0
```


## train_2

**input:**
```
0 5 0 5 0 0 5 0 5 0 0 0
5 0 0 0 5 0 0 5 0 0 5 0
0 0 5 0 0 5 0 0 0 5 0 5
```


**output:**
```
0 3 0 3 0 0 5 0 5 0 0 0
5 0 0 0 5 0 0 3 0 0 5 0
0 0 5 0 0 3 0 0 0 3 0 3
```


## train_3

**input:**
```
0 0 5 0 0 5 0 5 0 5 0 5 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 5
0 5 0 5 0 0 5 0 0 0 0 0 5 0
```


**output:**
```
0 0 5 0 0 3 0 3 0 3 0 3 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 3
0 3 0 3 0 0 5 0 0 0 0 0 5 0
```


## train_4

**input:**
```
5 0 5 0 0 5 0 0 0 5
0 5 0 0 5 0 0 5 0 0
0 0 0 5 0 0 5 0 5 0
```


**output:**
```
5 0 5 0 0 3 0 0 0 3
0 3 0 0 5 0 0 3 0 0
0 0 0 3 0 0 5 0 5 0
```

**Perception of Task Elements:**

1.  **Grid Transformation:** The task involves transforming an input grid into an output grid of the same dimensions.
2.  **Colors Involved:**
    *   Input grids contain only white (0) and gray (5) pixels.
    *   Output grids contain white (0), gray (5), and green (3) pixels.
3.  **Constancy:** White pixels (0) remain unchanged in their positions.
4.  **Change:** Only gray pixels (5) can potentially change their color. They either remain gray (5) or change to green (3).
5.  **Local Rule:** The change appears to depend on the local neighborhood of each gray pixel, specifically the configuration of its gray neighbors.
6.  **Neighbor Analysis:** Examining the 8 neighbors (orthogonal and diagonal) of each gray pixel seems crucial.
7.  **Key Pattern:** Gray pixels that have *both* a gray neighbor to their South-West and a gray neighbor to their South-East tend to remain gray. Gray pixels not meeting this specific condition tend to change to green.

**Facts (YAML):**


```yaml
task_elements:
  - Input Grid:
      properties:
        colors: [white (0), gray (5)]
        dimensionality: 2D
  - Output Grid:
      properties:
        colors: [white (0), gray (5), green (3)]
        dimensionality: 2D
        size: same as input grid
  - Pixels:
      types:
        - white (0)
        - gray (5)
        - green (3)
  - Objects:
      - gray pixels (color 5) are the primary objects subject to transformation.
      - white pixels (color 0) form the background and remain static.
      - green pixels (color 3) are the result of transforming specific gray pixels.
Relationships:
  - Adjacency: The transformation rule depends on the 8-neighbor adjacency (orthogonal and diagonal) of gray pixels.
  - Spatial Configuration: The relative positions of gray neighbors, specifically South-West and South-East, are critical.
Transformation:
  - Rule Type: Local, conditional color change.
  - Condition: A gray pixel's transformation depends on whether it has gray neighbors simultaneously located at its South-West and South-East positions.
  - Input Color -> Output Color Mapping:
      - white (0) -> white (0)
      - gray (5) -> green (3) OR gray (5) (conditional)
```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid.
2.  Iterate through each cell (pixel) of the input grid at position (row, column).
3.  If the input pixel at (row, column) is white (0), copy its value (0) to the corresponding cell in the output grid.
4.  If the input pixel P at (row, column) is gray (5):
    a.  Check the pixel at position (row+1, column-1) (South-West neighbor). Is it within the grid boundaries and is it gray (5)?
    b.  Check the pixel at position (row+1, column+1) (South-East neighbor). Is it within the grid boundaries and is it gray (5)?
    c.  If **both** the South-West neighbor and the South-East neighbor exist and are gray (5), then set the output pixel at (row, column) to gray (5).
    d.  Otherwise (if at least one of the SW or SE neighbors is missing, out of bounds, or not gray), set the output pixel at (row, column) to green (3).
5.  Return the completed output grid.
```python
"""
Transforms an input grid based on the local neighborhood of gray (5) pixels.

1. White (0) pixels remain unchanged.
2. Gray (5) pixels are evaluated based on their South-West (SW) and South-East (SE) neighbors.
3. If a gray pixel has BOTH a gray SW neighbor AND a gray SE neighbor (both within grid bounds), it remains gray (5) in the output.
4. Otherwise, if a gray pixel does NOT meet the condition in step 3 (i.e., missing one or both SW/SE neighbors, or one or both are out of bounds, or one or both are not gray), it changes to green (3) in the output.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid.
    # This handles the white pixels remaining unchanged and sets the default
    # state for gray pixels before conditional checks.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell (pixel) of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is gray (5)
            if input_grid[r][c] == 5:
                # Initialize flags for neighbor conditions
                has_sw_gray = False
                has_se_gray = False

                # Define coordinates for South-West (SW) and South-East (SE) neighbors
                sw_r, sw_c = r + 1, c - 1
                se_r, se_c = r + 1, c + 1

                # Check South-West neighbor
                # Ensure SW coordinates are within grid boundaries
                if 0 <= sw_r < height and 0 <= sw_c < width:
                    # Check if the SW neighbor is gray (5)
                    if input_grid[sw_r][sw_c] == 5:
                        has_sw_gray = True

                # Check South-East neighbor
                # Ensure SE coordinates are within grid boundaries
                if 0 <= se_r < height and 0 <= se_c < width:
                    # Check if the SE neighbor is gray (5)
                    if input_grid[se_r][se_c] == 5:
                        has_se_gray = True

                # Apply the transformation rule:
                # If BOTH SW and SE neighbors are gray, the pixel remains gray (5).
                # Since the output_grid was initialized as a copy, we only need to act
                # if the condition is NOT met.
                if not (has_sw_gray and has_se_gray):
                    # If the condition is not met, change the pixel to green (3)
                    output_grid[r][c] = 3

    # Return the completed output grid
    return output_grid
```
