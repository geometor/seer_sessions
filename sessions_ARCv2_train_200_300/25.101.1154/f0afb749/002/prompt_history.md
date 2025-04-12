
## train_1

**input:**
```
2 0
0 0
```


**output:**
```
2 2 0 0
2 2 0 0
0 0 1 0
0 0 0 1
```


## train_2

**input:**
```
0 0 0 5 0
0 5 0 0 0
0 0 0 0 0
0 5 0 0 0
0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 5 5 0 0
0 1 0 0 0 0 5 5 0 0
0 0 5 5 0 0 0 0 1 0
0 0 5 5 0 0 0 0 0 1
1 0 0 0 1 0 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 0 5 5 0 0 1 0 0 0
0 0 5 5 0 0 0 1 0 0
0 0 0 0 1 0 0 0 1 0
0 0 0 0 0 1 0 0 0 1
```


## train_3

**input:**
```
0 0 0 0 0 3
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3
1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0
```

**Perception:**

The core transformation involves scaling the input grid by a factor of two. Each pixel in the input grid corresponds to a 2x2 block in the output grid. The content of this 2x2 block is determined by the color of the original input pixel and its immediate orthogonal neighbours.

1.  **Scaling:** The output grid is twice the height and twice the width of the input grid.
2.  **Non-White Pixels:** If an input pixel has a color other than white (0), the corresponding 2x2 block in the output grid is filled entirely with that color.
3.  **White Pixels:** If an input pixel is white (0), the corresponding 2x2 output block's content depends on the input pixel's cardinal neighbours (up, down, left, right).
    *   If all existing cardinal neighbours of the white input pixel are also white, the output block becomes a diagonal pattern: blue (1) top-left, white (0) top-right, white (0) bottom-left, blue (1) bottom-right.
    *   If any existing cardinal neighbour of the white input pixel is non-white, the output block remains entirely white (0).

**Facts:**


```yaml
Input Grid:
  - object: grid
  - properties:
      - height: H
      - width: W
      - pixels: Located at (r, c), have a color C (0-9, 0 is white)

Output Grid:
  - object: grid
  - properties:
      - height: 2H
      - width: 2W
      - pixels: Colors derived from input grid

Transformation Rules:
  - rule: Scaling
    - relationship: Each input pixel (r, c) maps to a 2x2 output block starting at (2*r, 2*c).
  - rule: Pattern Replacement based on Input Color and Neighbourhood
    - input_pixel: color C at (r, c)
    - output_block: 2x2 block starting at (2*r, 2*c)
    - condition: If C is not white (C > 0)
      - action: Fill output_block with color C. -> [[C, C], [C, C]]
    - condition: If C is white (C == 0)
      - sub_condition: Check cardinal neighbours (up, down, left, right) of input pixel (r, c). Are all neighbours that exist within the grid bounds also white (0)?
        - if True: Set output_block to [[blue(1), white(0)], [white(0), blue(1)]].
        - if False: Set output_block to [[white(0), white(0)], [white(0), white(0)]].
```


**Natural Language Program:**

1.  Initialize an `output_grid` with dimensions `2 * input_height` by `2 * input_width`, filling it with the white color (0).
2.  Iterate through each cell `(r, c)` of the `input_grid`.
3.  Let `input_color` be the color of the cell `(r, c)`.
4.  Determine the top-left coordinates `(out_r, out_c)` of the corresponding 2x2 block in the `output_grid`, where `out_r = 2 * r` and `out_c = 2 * c`.
5.  If `input_color` is not white (`input_color > 0`):
    a.  Set the color of the four cells in the `output_grid` block starting at `(out_r, out_c)` (i.e., `(out_r, out_c)`, `(out_r+1, out_c)`, `(out_r, out_c+1)`, `(out_r+1, out_c+1)`) to `input_color`.
6.  If `input_color` is white (`input_color == 0`):
    a.  Assume initially that the condition for the special blue pattern is `True`.
    b.  Check the neighbor above: If `r > 0` and the color of `input_grid[r-1, c]` is not white, set the condition to `False`.
    c.  Check the neighbor below: If `r < input_height - 1` and the color of `input_grid[r+1, c]` is not white, set the condition to `False`.
    d.  Check the neighbor left: If `c > 0` and the color of `input_grid[r, c-1]` is not white, set the condition to `False`.
    e.  Check the neighbor right: If `c < input_width - 1` and the color of `input_grid[r, c+1]` is not white, set the condition to `False`.
    f.  If the condition remains `True` after checking all neighbours:
        i.  Set `output_grid[out_r, out_c]` to blue (1).
        ii. Set `output_grid[out_r+1, out_c+1]` to blue (1).
    g.  (Otherwise, if the condition became `False`, the block remains white (0) as initialized).
7.  Return the final `output_grid`.
```python
"""
Scales the input grid by 2x. 
Non-white input pixels are expanded into 2x2 blocks of the same color.
White input pixels are expanded based on their cardinal neighbours:
- If all existing cardinal neighbours are white, the 2x2 output block becomes a diagonal blue (1) pattern: [[1, 0], [0, 1]].
- If any existing cardinal neighbour is non-white, the 2x2 output block remains entirely white (0).
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described scaling and pattern replacement transformation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Initialize output grid with white (0)
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_np[r, c]
            
            # Determine the top-left coordinates of the corresponding 2x2 block in the output grid
            out_r = 2 * r
            out_c = 2 * c

            # If the input pixel is not white
            if input_color > 0:
                # Fill the 2x2 output block with the input color
                output_np[out_r:out_r+2, out_c:out_c+2] = input_color
            
            # If the input pixel is white
            else: # input_color == 0
                # Check cardinal neighbours in the input grid
                all_neighbours_white = True
                neighbours = []
                # Check up
                if r > 0:
                    neighbours.append(input_np[r-1, c])
                # Check down
                if r < input_height - 1:
                    neighbours.append(input_np[r+1, c])
                # Check left
                if c > 0:
                    neighbours.append(input_np[r, c-1])
                # Check right
                if c < input_width - 1:
                     neighbours.append(input_np[r, c+1])

                # See if any existing neighbour is non-white
                for neighbour_color in neighbours:
                    if neighbour_color > 0:
                        all_neighbours_white = False
                        break
                
                # If all existing neighbours were white (or there were no neighbours)
                if all_neighbours_white:
                    # Set the diagonal blue pattern
                    output_np[out_r, out_c] = 1  # Top-left blue
                    output_np[out_r + 1, out_c + 1] = 1 # Bottom-right blue
                # Else (if any neighbour was non-white), the block remains white (0) - already initialized

    # Convert the NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```
