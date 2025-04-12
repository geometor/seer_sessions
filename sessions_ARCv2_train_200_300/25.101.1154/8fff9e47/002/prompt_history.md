
## train_1

**input:**
```
1 3 9 4
5 5 2 8
9 8 3 1
4 0 1 4
2 3 6 5
3 9 8 0
```


**output:**
```
6 6 6 6 6 6 5 5 5 5 5 5
6 2 2 2 2 2 3 3 3 3 3 5
6 2 3 3 3 3 1 1 1 1 3 5
6 2 3 9 9 9 8 8 8 1 3 5
6 2 3 9 9 9 4 4 8 1 3 5
6 2 3 9 9 1 3 4 8 1 3 5
8 3 1 4 2 5 5 8 0 4 9 0
8 3 1 4 2 2 8 8 0 4 9 0
8 3 1 4 4 4 0 0 0 4 9 0
8 3 1 1 1 1 4 4 4 4 9 0
8 3 3 3 3 3 9 9 9 9 9 0
8 8 8 8 8 8 0 0 0 0 0 0
```


## train_2

**input:**
```
9 1 1 7 7 9
2 0 7 7 0 3
2 8 7 7 2 1
5 3 9 7 7 8
```


**output:**
```
2 2 2 2 2 2 1 1 1 1 1 1
2 7 7 7 7 7 7 7 7 7 7 1
2 7 2 2 2 2 8 8 8 8 7 1
2 7 2 7 7 7 9 9 9 8 7 1
2 7 2 7 1 1 7 7 9 8 7 1
2 7 2 7 1 9 1 7 9 8 7 1
7 9 5 0 7 2 0 7 3 3 7 8
7 9 5 0 7 7 7 7 3 3 7 8
7 9 5 0 0 0 3 3 3 3 7 8
7 9 5 5 5 5 3 3 3 3 7 8
7 9 9 9 9 9 7 7 7 7 7 8
7 7 7 7 7 7 8 8 8 8 8 8
```

*   **Perception:**
    *   The task transforms a small input grid into a larger, fixed-size output grid (12x12).
    *   The transformation appears to involve scaling the input grid to fit the 12x12 output dimensions.
    *   The scaling factors are determined by the input grid's dimensions: `scale_h = 12 / H_in`, `scale_w = 12 / W_in`. Note that these factors can be different for height and width and vary between examples (2x3 for train_1, 3x2 for train_2).
    *   Each pixel in the input grid is expanded into a rectangular block of size `scale_h` x `scale_w` in the output grid.
    *   The color of each pixel within an output block is not simply the color of the original input pixel. Instead, it seems to be determined by sampling the color of one of the pixels in the 3x3 neighborhood (including the center pixel itself) of the corresponding input pixel.
    *   The specific neighbor chosen for sampling appears to depend on the relative position of the output pixel within its `scale_h` x `scale_w` block.
    *   There seems to be a fixed mapping rule that connects the relative coordinates within a block to a specific neighbor direction (e.g., North, South-West, Center, etc.).
    *   Pixels outside the original input grid boundaries, when queried as neighbors, likely return a default color value (potentially black/0, or perhaps derived from the input). The exact mapping and default value are not immediately obvious from the single example provided.

*   **YAML Facts:**
    
```yaml
    task_type: scaling_and_patterning
    input_object:
      type: grid
      description: A grid of pixels with varying dimensions (H_in x W_in).
    output_object:
      type: grid
      description: A grid of pixels with fixed dimensions (12x12).
    transformation:
      operation: scale_and_sample
      scaling_factors:
        height: 12 / H_in
        width: 12 / W_in
      block_size: [scale_h, scale_w]
      sampling:
        source: 3x3 neighborhood of the corresponding input pixel.
        method: Each pixel in the output block (size scale_h x scale_w) samples the color from one neighbor (including center) of the source input pixel.
        mapping: The choice of neighbor depends on the relative position within the block. (The exact mapping rule needs further examples to confirm).
        boundary_handling: Neighbors outside the input grid return a default color (e.g., black/0, but needs confirmation).
    relationships:
      - Each input pixel Input[i, j] corresponds to an output block starting at Output[i * scale_h, j * scale_w] of size scale_h x scale_w.
      - Each output pixel Output[r, c] is determined by the input pixel Input[floor(r / scale_h), floor(c / scale_w)] and its neighbors, based on the relative position (r % scale_h, c % scale_w).
    ```


*   **Natural Language Program:**
    1.  Determine the height (`H_in`) and width (`W_in`) of the input grid.
    2.  Calculate the integer scaling factors: `scale_h = 12 / H_in` and `scale_w = 12 / W_in`.
    3.  Create a new output grid of size 12x12, initially empty or filled with a default color (e.g., black/0).
    4.  Iterate through each pixel of the output grid using its row `r` (from 0 to 11) and column `c` (from 0 to 11).
    5.  For each output pixel `(r, c)`, identify the corresponding source input pixel coordinates: `i = floor(r / scale_h)` and `j = floor(c / scale_w)`.
    6.  Determine the relative position of the output pixel within its conceptual block: `rel_r = r % scale_h` and `rel_c = c % scale_w`.
    7.  Based on the relative position `(rel_r, rel_c)`, select a specific neighbor direction relative to the source input pixel `(i, j)`. This selection follows a predefined mapping rule associated with the block shape (`scale_h` x `scale_w`). (For example, if the block is 2x3, the mapping might associate `(rel_r=0, rel_c=0)` with the North-West neighbor, `(rel_r=1, rel_c=2)` with the East neighbor, etc. This specific mapping needs to be fully determined).
    8.  Get the coordinates `(ni, nj)` of the selected neighbor relative to `(i, j)`.
    9.  Check if the neighbor coordinates `(ni, nj)` are within the bounds of the input grid.
    10. If the neighbor is within bounds, retrieve its color value `Input[ni, nj]`.
    11. If the neighbor is out of bounds, use a default color value (e.g., black/0).
    12. Assign the retrieved or default color value to the output grid pixel `Output[r, c]`.
    13. After iterating through all output pixels, return the completed 12x12 output grid.
```python
import numpy as np
import math

"""
The transformation scales an input grid of size H_in x W_in to a fixed output grid of size 12x12.
The scaling factors are determined by integer division: scale_h = 12 / H_in and scale_w = 12 / W_in.
Each pixel Input[i, j] in the input grid corresponds to a block of size scale_h x scale_w in the output grid, starting at Output[i * scale_h, j * scale_w].
The color of each pixel Output[r, c] within this block is determined by sampling the color of one of the pixels in the 3x3 neighborhood (including the center pixel itself) of the corresponding input pixel Input[i, j].
The specific neighbor (offset dr, dc relative to (i, j)) is chosen based on the relative position (rel_r, rel_c) of the output pixel within its scale_h x scale_w block.
The mapping from (rel_r, rel_c) to (dr, dc) is determined by mapping the relative coordinates normalized to the 0-1 range onto a 3x3 grid representing the neighbor offsets (-1, 0, 1).
Neighbors outside the input grid boundaries are treated as having a default color of 0 (black).

Specifically, the neighbor offset (dr, dc) for an output pixel Output[r, c] is calculated as follows:
1. Find the corresponding input pixel: i = floor(r / scale_h), j = floor(c / scale_w).
2. Find the relative position within the block: rel_r = r % scale_h, rel_c = c % scale_w.
3. Calculate the normalized position within the 3x3 neighborhood grid:
   dr = floor((rel_r + 0.5) / scale_h * 3) - 1
   dc = floor((rel_c + 0.5) / scale_w * 3) - 1
4. Retrieve the color from the input grid at Input[i + dr, j + dc], handling boundary conditions by returning 0 if the coordinates are out of bounds.
"""

def get_neighbor(grid: np.ndarray, r: int, c: int, dr: int, dc: int, default_color: int = 0) -> int:
    """
    Safely retrieves the color of a neighbor pixel from the grid.

    Args:
        grid: The input numpy array.
        r: The row index of the center pixel.
        c: The column index of the center pixel.
        dr: The row offset of the neighbor (-1, 0, or 1).
        dc: The column offset of the neighbor (-1, 0, or 1).
        default_color: The color to return if the neighbor is out of bounds.

    Returns:
        The color of the neighbor pixel or the default color.
    """
    nr, nc = r + dr, c + dc
    H, W = grid.shape
    if 0 <= nr < H and 0 <= nc < W:
        return grid[nr, nc]
    else:
        return default_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by scaling and sampling neighbors based on relative position.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed 12x12 grid as a list of lists.
    """
    input_np = np.array(input_grid, dtype=int)
    H_in, W_in = input_np.shape
    H_out, W_out = 12, 12

    # Calculate integer scaling factors
    # Note: Use integer division H_out // H_in and W_out // W_in
    # This matches the observed block sizes in the examples:
    # Ex 1: 12 // 6 = 2, 12 // 4 = 3 -> scale_h=2, scale_w=3
    # Ex 2: 12 // 4 = 3, 12 // 6 = 2 -> scale_h=3, scale_w=2
    if H_in == 0 or W_in == 0:
        # Handle empty input grid case if necessary, maybe return empty or black grid?
        return [[0 for _ in range(W_out)] for _ in range(H_out)]
        
    scale_h = H_out // H_in
    scale_w = W_out // W_in

    # Initialize the output grid (12x12) with black/0
    output_np = np.zeros((H_out, W_out), dtype=int)

    # Iterate through each pixel of the output grid
    for r in range(H_out):
        for c in range(W_out):
            # Identify the corresponding source input pixel coordinates
            # Ensure division by zero is avoided if scale factors are 0 (though H_in/W_in > 0 implies scale > 0)
            i = math.floor(r / scale_h) if scale_h > 0 else 0
            j = math.floor(c / scale_w) if scale_w > 0 else 0
            
            # Handle potential out-of-bounds access for i, j if input dimensions are larger than output/scale
            # This shouldn't happen if H_out=12, W_out=12 and scale factors are calculated correctly
            i = min(i, H_in - 1)
            j = min(j, W_in - 1)

            # Determine the relative position within the conceptual block
            rel_r = r % scale_h if scale_h > 0 else 0
            rel_c = c % scale_w if scale_w > 0 else 0

            # Determine the neighbor offset (dr, dc) based on relative position
            # using the formula: dr = floor((rel_r + 0.5) / scale_h * 3) - 1
            # Handle division by zero for scale factors
            dr = math.floor((rel_r + 0.5) / scale_h * 3) - 1 if scale_h > 0 else 0
            dc = math.floor((rel_c + 0.5) / scale_w * 3) - 1 if scale_w > 0 else 0

            # Get the color from the calculated neighbor
            color = get_neighbor(input_np, i, j, dr, dc, default_color=0)

            # Assign the color to the output grid pixel
            output_np[r, c] = color

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
```
