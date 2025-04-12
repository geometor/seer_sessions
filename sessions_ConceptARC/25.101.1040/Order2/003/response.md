```python
"""
Transforms an input grid by rearranging its single non-background color pixels into a specific shape in the bottom-left corner of the output grid, based on whether the count of these pixels is a triangular number.

1.  Analyze Input: Find the non-background color 'C' and its count 'N'. Get grid dimensions.
2.  Prepare Output: Create a new grid of the same size, filled with background color 0.
3.  Check Condition: Determine if 'N' is a triangular number.
4.  Generate Output Shape:
    a. If 'N' is triangular: Construct a specific right-angled triangle shape in the bottom-left corner using 'N' pixels of color 'C'.
    b. If 'N' is not triangular: Fill pixels with color 'C' starting from the bottom row, left-to-right, then the next row up, left-to-right, continuing until 'N' pixels are placed in the bottom-left area.
5.  Finalize: Return the generated grid.
"""

import numpy as np
import math

def is_perfect_square(n: int) -> bool:
    """Checks if a non-negative integer is a perfect square."""
    if n < 0:
        return False
    if n == 0:
        return True
    x = int(math.isqrt(n))
    return x * x == n

def is_triangular(n: int) -> bool:
    """Checks if a non-negative integer is a triangular number."""
    if n < 0:
        return False
    # N is triangular if and only if 8*N + 1 is a perfect square.
    val = 8 * n + 1
    return is_perfect_square(val)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    H_grid, W_grid = input_np.shape
    background_color = 0

    # 1. Analyze Input
    non_background_pixels = input_np[input_np != background_color]

    if non_background_pixels.size == 0:
        # Handle empty input case: return grid of zeros
        return np.zeros_like(input_np).tolist()

    color_C = non_background_pixels[0] # Assume only one non-background color
    count_N = non_background_pixels.size

    # 2. Prepare Output
    output_np = np.full_like(input_np, background_color)

    # 3. Check Triangular Condition
    is_n_triangular = is_triangular(count_N)

    # 4. Generate Output Shape
    if is_n_triangular:
        # Case a: N is a triangular number (form right triangle)
        # Calculate triangle height H_tri (base width is also H_tri)
        # N = H_tri * (H_tri + 1) / 2  => 8N + 1 = (2*H_tri + 1)^2
        sqrt_val = math.isqrt(8 * count_N + 1)
        H_tri = (sqrt_val - 1) // 2 # Integer division is exact here

        # Iterate through potential pixel locations for the triangle in the bottom-left
        for r in range(H_grid):
            for c in range(W_grid):
                # Check if the pixel (r, c) belongs to the triangle shape
                # Condition 1: Row is within the bottom H_tri rows (r >= H_grid - H_tri)
                # Condition 2: Column is within the left H_tri columns (c <= H_tri - 1)
                # Condition 3: Pixel is on or below the hypotenuse (r + c >= H_grid - 1)
                if r >= H_grid - H_tri and c <= H_tri - 1 and r + c >= H_grid - 1:
                    output_np[r, c] = color_C
    else:
        # Case b: N is not a triangular number (fill bottom-up, left-to-right)
        placed_pixels = 0
        # Iterate rows bottom to top
        for r in range(H_grid - 1, -1, -1):
            # Iterate columns left to right
            for c in range(W_grid):
                if placed_pixels < count_N:
                    output_np[r, c] = color_C
                    placed_pixels += 1
                else:
                    # Exit inner loop (columns) if N pixels are placed
                    break
            # Exit outer loop (rows) if N pixels are placed
            if placed_pixels >= count_N:
                break

    # 5. Finalize
    return output_np.tolist()
```