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
