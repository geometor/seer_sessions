
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 4 4 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 6 0 0 6 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0
6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0
```

## Perception
The user has provided two training examples for an ARC task.
Each example consists of an input grid and an output grid.
The grids contain pixels represented by integers 0-9, where 0 (white) is the background color.

**Observations:**
1.  **Color Conservation:** In both examples, the output grid contains only one non-background color. This color is the same as the single non-background color present in the input grid. The total count of these non-background pixels remains the same between the input and the output.
2.  **Shape Transformation:** The scattered non-background pixels from the input are rearranged into a single connected shape in the output grid.
3.  **Output Location:** The generated shape is always located in the bottom-left corner of the grid.
4.  **Two Different Shapes:** The shape generated in the output differs between the two examples.
    *   Example 1 (Input N=10 yellow pixels): The output is a right-angled triangle, 4 pixels high and 4 pixels wide, containing exactly 10 pixels. The right angle is at the top-left of the shape's bounding box, (row 6, col 3) if we use the grid coords, but visually it's oriented with the hypotenuse from bottom-left to top-right. Specifically, pixels (r, c) are filled if `r >= 6`, `c <= 3`, and `r + c >= 9`.
    *   Example 2 (Input N=13 magenta pixels): The output shape is different. It appears to be constructed by filling pixels column by column from left to right, and within each column, filling from bottom to top, until N pixels are placed.
5.  **Condition for Shape:** The number of pixels N in Example 1 is 10, which is a triangular number (1+2+3+4 = 10). The number of pixels N in Example 2 is 13, which is not a triangular number. This suggests the transformation rule depends on whether the count N of the non-background pixels is a triangular number.

**Hypothesized Rule:**
1.  Find the single non-background color (C) and count its occurrences (N).
2.  Check if N is a triangular number (i.e., if 8*N + 1 is a perfect square).
3.  If N is triangular, construct a specific right-angled triangle shape (like in Example 1) using N pixels of color C in the bottom-left of the output grid. The height H of this triangle is determined by N = H*(H+1)/2. The pixels (r, c) satisfy `r >= max_r - H + 1`, `c <= H - 1`, and `r + c >= max_r`.
4.  If N is not triangular, construct the shape by filling pixels with color C column by column (left to right), bottom to top within each column, starting from the bottom-left of the grid, until exactly N pixels have been placed.

## Facts

```yaml
task_type: pixel_rearrangement
background_color: 0 # white
examples:
  train_1:
    input_grid_size: [10, 11]
    output_grid_size: [10, 11]
    objects:
      - type: scattered_pixels
        color: 4 # yellow
        count: 10
        is_triangular_count: true
        output_shape_type: triangle
        output_shape_details: Height H=4, pixels satisfy r>=6, c<=3, r+c>=9
        location: bottom-left
  train_2:
    input_grid_size: [9, 10]
    output_grid_size: [9, 10]
    objects:
      - type: scattered_pixels
        color: 6 # magenta
        count: 13
        is_triangular_count: false
        output_shape_type: column_fill
        output_shape_details: Pixels filled column-by-column (0 to max_c), bottom-up (max_r to 0) until count reaches 13.
        location: bottom-left

properties:
  - Pixel count is conserved between input and output.
  - Only one non-background color exists in the input and output.
  - The final shape is always placed in the bottom-left corner.
  - The final shape depends on whether the pixel count is a triangular number.
```


## Natural Language Program

1.  **Analyze Input:**
    a.  Identify the background color (assumed to be 0, white).
    b.  Find the single non-background color present in the input grid. Call this color `C`.
    c.  Count the total number of pixels `N` that have color `C`.
    d.  Get the dimensions of the input grid (height `H_grid`, width `W_grid`). Let `max_r = H_grid - 1` and `max_c = W_grid - 1`.

2.  **Prepare Output:** Create a new grid of size `H_grid` x `W_grid`, filled entirely with the background color (0).

3.  **Check Triangular Condition:** Determine if `N` is a triangular number. This can be done by checking if `8 * N + 1` is a perfect square.

4.  **Generate Output Shape:**
    a.  **If `N` is a triangular number:**
        i.  Calculate the triangle height `H_tri = (sqrt(8 * N + 1) - 1) / 2`.
        ii. Iterate through all pixels `(r, c)` in the output grid.
        iii. If a pixel's coordinates `(r, c)` satisfy all three conditions:
            1.  `r >= max_r - H_tri + 1`
            2.  `c <= H_tri - 1`
            3.  `r + c >= max_r`
            Then set the color of pixel `(r, c)` in the output grid to `C`.
    b.  **If `N` is not a triangular number:**
        i.  Initialize a counter `placed_pixels = 0`.
        ii. Iterate through columns `c` from 0 to `max_c`.
        iii. For each column `c`, iterate through rows `r` from `max_r` down to 0.
        iv. If `placed_pixels < N`:
            1. Set the color of pixel `(r, c)` in the output grid to `C`.
            2. Increment `placed_pixels`.
            3. If `placed_pixels` is now equal to `N`, stop placing pixels (exit both row and column loops).
        v. If `placed_pixels` was already equal to `N` when checking, stop iterating through rows for the current column and proceed to the next column (or finish if this was the last necessary column).

5.  **Finalize:** Return the generated output grid.
```python
"""
Transforms an input grid by rearranging its single non-background color pixels into a specific shape in the bottom-left corner of the output grid.

1.  Analyze Input:
    a. Identify the background color (0, white).
    b. Find the single non-background color 'C'.
    c. Count the total number of pixels 'N' with color 'C'.
    d. Get the grid dimensions (height 'H_grid', width 'W_grid').

2.  Prepare Output: Create a new grid of size 'H_grid' x 'W_grid', filled with the background color.

3.  Check Triangular Condition: Determine if 'N' is a triangular number (if 8*N + 1 is a perfect square).

4.  Generate Output Shape:
    a. If 'N' is triangular:
        i. Calculate the triangle height 'H_tri' = (sqrt(8*N + 1) - 1) / 2.
        ii. Fill pixels (r, c) in the output grid with color 'C' if they satisfy:
           - r >= H_grid - H_tri
           - c <= H_tri - 1
           - r + c >= H_grid - 1
    b. If 'N' is not triangular:
        i. Fill pixels with color 'C' column by column (left to right), bottom to top within each column, starting from the bottom-left, until 'N' pixels are placed.

5.  Finalize: Return the generated output grid.
"""

import numpy as np
import math

def is_perfect_square(n):
    """Checks if a non-negative number is a perfect square."""
    if n < 0:
        return False
    x = int(math.isqrt(n))
    return x * x == n

def is_triangular(n):
    """Checks if a number is a triangular number."""
    if n < 0:
        return False
    # N is triangular if 8*N + 1 is a perfect square
    val = 8 * n + 1
    return is_perfect_square(val)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    H_grid, W_grid = input_np.shape
    max_r = H_grid - 1
    max_c = W_grid - 1
    background_color = 0

    # 1. Analyze Input
    non_background_pixels = input_np[input_np != background_color]
    
    if non_background_pixels.size == 0:
        # Handle empty input case: return grid of zeros
        return np.zeros_like(input_np).tolist()
        
    color_C = non_background_pixels[0] # Assuming only one non-background color
    count_N = non_background_pixels.size

    # 2. Prepare Output
    output_np = np.full_like(input_np, background_color)

    # 3. Check Triangular Condition
    is_n_triangular = is_triangular(count_N)

    # 4. Generate Output Shape
    if is_n_triangular:
        # Case a: N is a triangular number
        # Calculate triangle height H_tri
        sqrt_val = math.isqrt(8 * count_N + 1)
        H_tri = (sqrt_val - 1) // 2 # Integer division should be exact here

        # Iterate through potential pixel locations for the triangle
        for r in range(H_grid):
            for c in range(W_grid):
                # Apply the three conditions derived from Example 1
                # condition 1: r >= max_r - H_tri + 1 (equivalent to r >= H_grid - H_tri)
                # condition 2: c <= H_tri - 1
                # condition 3: r + c >= max_r (equivalent to r + c >= H_grid - 1)
                if r >= H_grid - H_tri and c <= H_tri - 1 and r + c >= H_grid - 1:
                    output_np[r, c] = color_C
    else:
        # Case b: N is not a triangular number
        placed_pixels = 0
        # Iterate columns left to right
        for c in range(W_grid):
            # Iterate rows bottom to top
            for r in range(max_r, -1, -1):
                if placed_pixels < count_N:
                    output_np[r, c] = color_C
                    placed_pixels += 1
                else:
                    # Stop filling rows in this column once N is reached
                    break 
            # Stop filling columns once N is reached
            if placed_pixels >= count_N:
                break

    # 5. Finalize
    return output_np.tolist()

```
