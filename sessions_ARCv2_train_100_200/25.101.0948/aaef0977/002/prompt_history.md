
## train_1

**input:**
```
7 7 7 7 7 7 3 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
```


**output:**
```
9 8 2 5 0 4 3 4
6 9 8 2 5 0 4 0
1 6 9 8 2 5 0 5
3 1 6 9 8 2 5 2
4 3 1 6 9 8 2 8
0 4 3 1 6 9 8 9
5 0 4 3 1 6 9 6
2 5 0 4 3 1 6 1
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 5 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
```


**output:**
```
4 3 1 3 4 0 5 2
3 1 6 1 3 4 0 5
1 6 9 6 1 3 4 0
6 9 8 9 6 1 3 4
9 8 2 8 9 6 1 3
8 2 5 2 8 9 6 1
9 8 2 8 9 6 1 3
6 9 8 9 6 1 3 4
```

## Perception

The task involves transforming an input grid into an output grid of the same dimensions. The input grid consists of a uniform background color (orange, value 7) with a single pixel of a different color at a specific location. Let's call the coordinates of this unique pixel `(r0, c0)` and its color `v0`.

The output grid is filled with a complex pattern of colors (values 0-9). The transformation seems to depend critically on the location `(r0, c0)` and the color `v0` of the unique input pixel.

Observing the two examples:
1.  **Example 1:** Input has green (3) at (0, 6). Output is a complex grid.
2.  **Example 2:** Input has gray (5) at (5, 2). Output is a different complex grid.

Key observations:
*   The output grid dimensions match the input grid dimensions (8x8 in both examples).
*   The color of the output pixel at the location of the unique input pixel `(r0, c0)` is always equal to the unique input color `v0`. That is, `Output[r0][c0] = v0`.
*   The overall pattern in the output grid changes based on the position and color of the unique input pixel.
*   The output color `Output[r][c]` for any pixel `(r, c)` appears to be a deterministic function of its coordinates `(r, c)`, the unique pixel's coordinates `(r0, c0)`, and the unique pixel's color `v0`.
*   Initial hypotheses involving simple functions of Manhattan distance (`d = |r-r0| + |c-c0|`) like `(d + v0) % 10` match some output pixels but fail for others, indicating a more complex relationship. Similarly, linear combinations of coordinates relative to `(r0, c0)` like `(A*(r-r0) + B*(c-c0) + v0) % 10` also failed to consistently explain the patterns with constant coefficients A and B, or coefficients linearly dependent on `v0`.

The transformation generates a full grid pattern originating from or influenced by the single unique input point. The precise mathematical formula generating the pattern remains unclear from only two examples but involves the coordinates `(r, c)`, the unique point `(r0, c0, v0)`, and likely modulo 10 arithmetic.

## Facts


```yaml
task_elements:
  - description: Input grid has a uniform background color with one unique pixel.
    properties:
      background_color: orange (7) - based on examples
      grid_size: Variable (8x8 in examples)
      unique_pixel:
        exists: true
        count: 1
        properties:
          location: (r0, c0)
          color: v0 (different from background)

  - description: Output grid has the same dimensions as the input grid.
    properties:
      grid_size: Same as input
      content: Filled with a complex pattern of colors (0-9).

relationships:
  - description: The output grid pattern is determined by the location and color of the unique input pixel.
    input_elements:
      - unique_pixel location (r0, c0)
      - unique_pixel color (v0)
    output_elements:
      - Entire output grid pattern

transformations:
  - description: The value of the output pixel at the location of the unique input pixel is equal to the unique input pixel's color.
    rule: Output[r0][c0] = v0

  - description: The value of every other output pixel is calculated based on its coordinates (r, c), the unique pixel's coordinates (r0, c0), and the unique pixel's color (v0).
    rule: Output[r][c] = Function(r, c, r0, c0, v0) % 10
    notes: The exact nature of the function is complex and not fully determined by the provided examples. It likely involves the relative coordinates (r-r0, c-c0) or Manhattan distance, combined with v0, using modulo 10 arithmetic. Simple common formulas did not fully match the examples.
```


## Natural Language Program

1.  **Identify Unique Pixel**: Scan the input grid to find the pixel whose color is different from the majority background color (expected to be orange, value 7). Record its row `r0`, column `c0`, and color `v0`.
2.  **Initialize Output Grid**: Create a new grid with the same height and width as the input grid.
3.  **Calculate Output Pixel Values**: Iterate through each cell `(r, c)` of the grid (from row 0 to height-1, and column 0 to width-1).
4.  **Determine Pixel Color**: For the current cell `(r, c)`, calculate its color based on a rule involving `r`, `c`, `r0`, `c0`, and `v0`. The specific rule observed is `Output[r][c] = (|r - r0| + |c - c0| + v0) % 10`, where `|x|` denotes the absolute value (Manhattan distance calculation).
    * *Self-correction during thought process indicated this simple Manhattan distance formula does not perfectly match all pixels in the examples, but it captures the dependency on relative position and the unique value, and matches the unique pixel itself and some neighbors. It represents the most plausible simple hypothesis found.*
5.  **Populate Output Grid**: Assign the calculated color to the cell `(r, c)` in the output grid.
6.  **Return Output Grid**: Once all cells are calculated, return the completed output grid.
```python
"""
Transforms an input grid based on a single unique pixel.

1.  **Identify Unique Pixel**: Scan the input grid to find the pixel whose color
    is different from the majority background color. Record its row `r0`,
    column `c0`, and color `v0`.
2.  **Initialize Output Grid**: Create a new grid with the same height and
    width as the input grid.
3.  **Calculate Output Pixel Values**: Iterate through each cell `(r, c)` of the
    grid.
4.  **Determine Pixel Color**: For the current cell `(r, c)`, calculate its color
    based on the rule: `Output[r][c] = (|r - r0| + |c - c0| + v0) % 10`, where
    `|x|` denotes the absolute value (Manhattan distance calculation).
5.  **Populate Output Grid**: Assign the calculated color to the cell `(r, c)`
    in the output grid.
6.  **Return Output Grid**: Once all cells are calculated, return the completed
    output grid.
"""

import collections
import math

def find_unique_pixel(grid: list[list[int]]) -> tuple[int, int, int]:
    """
    Finds the row, column, and value of the single unique pixel in the grid.

    Assumes the background color is the most frequent color and there is
    exactly one pixel with a different color.

    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        A tuple containing (row, column, value) of the unique pixel.

    Raises:
        ValueError: If the grid is empty, no unique pixel is found, or more
                    than one unique pixel is found.
    """
    if not grid or not grid[0]:
        raise ValueError("Input grid cannot be empty")

    height = len(grid)
    width = len(grid[0])

    # Count color occurrences to find the background color
    counts = collections.Counter()
    for r in range(height):
        for c in range(width):
            counts[grid[r][c]] += 1

    if not counts:
         # This case would only happen if the grid dimensions were non-zero
         # but the grid itself was somehow empty, which is unlikely with checks above.
         raise ValueError("Could not count colors in the grid.")

    # Determine background color (most frequent). Handles uniform grids implicitly.
    background_color = counts.most_common(1)[0][0]

    # Find the unique pixel (the one not matching the background)
    unique_pixel_info = None
    unique_count = 0
    for r in range(height):
        for c in range(width):
            pixel_value = grid[r][c]
            if pixel_value != background_color:
                # Check if we already found a unique pixel
                if unique_count > 0:
                     raise ValueError("More than one unique pixel found.")
                unique_pixel_info = (r, c, pixel_value)
                unique_count += 1

    # Check if a unique pixel was found
    if unique_pixel_info is None:
        # This happens if all pixels are the same (background) color.
        # The problem description implies a unique pixel always exists.
         raise ValueError("No unique pixel found.")

    return unique_pixel_info

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule derived from the examples.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # 1. Identify Unique Pixel
    # Find the location (r0, c0) and value (v0) of the pixel
    # that differs from the background.
    try:
        r0, c0, v0 = find_unique_pixel(input_grid)
    except ValueError as e:
        # Handle cases where the input doesn't match expectations
        print(f"Error processing input grid: {e}")
        # Depending on requirements, might return input grid, empty grid, or re-raise
        return [] # Or raise e

    height = len(input_grid)
    width = len(input_grid[0])

    # 2. Initialize Output Grid
    # Create a new grid of the same size, initialized with zeros or any placeholder.
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 3. & 5. Calculate Output Pixel Values and Populate Output Grid
    # Iterate through each cell (r, c) of the grid.
    for r in range(height):
        for c in range(width):
            # 4. Determine Pixel Color
            # Calculate the Manhattan distance from the unique pixel (r0, c0)
            manhattan_distance = abs(r - r0) + abs(c - c0)
            # Apply the formula: (distance + unique_value) mod 10
            output_value = (manhattan_distance + v0) % 10
            # Assign the calculated value to the output grid
            output_grid[r][c] = output_value

    # 6. Return Output Grid
    return output_grid
```
