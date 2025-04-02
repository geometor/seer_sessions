
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 3 3 3 3 3 3
0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 3 3 3 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 3
0 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```

Okay, let's break down this task.

### Perception

1.  **Input Grid Structure:** The input grids primarily consist of a white background (color 0). Embedded within this background is a single, contiguous diagonal line composed of pixels of a single non-white color (yellow/4 in the first example, green/3 in the second).
2.  **Diagonal Types:** The diagonal line can either descend from top-left to bottom-right (main diagonal) or from top-right to bottom-left (anti-diagonal).
3.  **Output Grid Structure:** The output grid retains the original diagonal line. Additionally, a region below and to the left of this line is filled with the same non-white color.
4.  **Transformation Effect:** The transformation effectively "fills" a triangular area. This area seems bounded by the original diagonal line (as the hypotenuse), the left edge of the grid, and the bottom edge of the grid. Regardless of whether the input line was a main diagonal or an anti-diagonal, the resulting filled shape appears in the bottom-left portion of the grid.
5.  **Color Preservation:** The non-white color used in the input diagonal is the *only* non-white color used in the output grid.
6.  **Rule Identification:** A pixel at position (row `r`, column `c`) in the output grid gets the non-white color if and only if there was a non-white pixel at position (row `ri`, column `ci`) in the input grid such that `r >= ri` and `c <= ci`. All other output pixels are white.

### Facts


```yaml
Input Grid:
  - BackgroundColor: white (0)
  - Objects:
      - Type: Line
      - Shape: Diagonal (either main or anti-diagonal)
      - Color: C (variable, e.g., yellow/4, green/3)
      - Pixels: Set D = {(r, c) | input[r, c] == C}

Output Grid:
  - BackgroundColor: white (0)
  - Objects:
      - Type: Filled Region
      - Shape: Right-angled Triangle (bottom-left corner)
      - Color: C (same as input line color)
      - Defining Feature: Bounded by the original diagonal line, the left grid edge, and the bottom grid edge.

Transformation Rule:
  - Rule: Fill based on input line coordinates.
  - Condition: A pixel at output coordinates (ro, co) gets color C if there exists an input pixel coordinates (ri, ci) in set D such that ro >= ri AND co <= ci.
  - Otherwise: The pixel at output coordinates (ro, co) gets color white (0).
  - Relationship: The output is determined by iterating through all potential output pixels and checking their spatial relationship (below and to the left of, or on) relative to *any* of the original colored input pixels.
```


### Natural Language Program

1.  Initialize the output grid as a copy of the input grid, or create a new grid of the same dimensions filled with white (0).
2.  Identify the single non-white color (let's call it `fill_color`) present in the input grid.
3.  Create a list (or set) containing the coordinates (`r_in`, `c_in`) of all pixels in the input grid that have the `fill_color`.
4.  Iterate through each pixel position (`r_out`, `c_out`) in the grid dimensions (from row 0 to height-1, and column 0 to width-1).
5.  For the current position (`r_out`, `c_out`), check if there exists *any* coordinate (`r_in`, `c_in`) in the list created in step 3 such that `r_out >= r_in` AND `c_out <= c_in`.
6.  If such a coordinate pair exists (the condition in step 5 is true for at least one input pixel), set the color of the pixel at (`r_out`, `c_out`) in the output grid to `fill_color`.
7.  If no such coordinate pair exists (the condition in step 5 is false for all input pixels), ensure the color of the pixel at (`r_out`, `c_out`) in the output grid is white (0). (This step is crucial if you started by copying the input grid, otherwise, if you started with a white grid, you only need to perform step 6).
8.  Return the completed output grid.
```python
"""
Transforms an input grid by identifying a diagonal line of a single non-white color and filling the area below and to the left of this line with the same color.

The transformation rule is as follows:
1. Identify the single non-white color (fill_color) present in the input grid.
2. Find all coordinates (r_in, c_in) where this fill_color appears in the input grid.
3. Create an output grid of the same dimensions, initially filled with white (0).
4. For each pixel position (r_out, c_out) in the output grid:
   Check if there exists at least one input coordinate (r_in, c_in) such that r_out >= r_in AND c_out <= c_in.
5. If the condition in step 4 is true, set the output pixel at (r_out, c_out) to the fill_color.
6. Otherwise, the output pixel remains white (0).
"""

import numpy as np

def find_fill_color_and_coords(grid):
    """
    Finds the single non-white color and its coordinates in the grid.
    Assumes there is exactly one non-white color present as a diagonal line.
    """
    fill_color = 0
    coords = []
    non_white_colors = np.unique(grid[grid != 0])

    if len(non_white_colors) == 0:
        # Handle case with no non-white colors (though unlikely based on examples)
        return 0, []
    elif len(non_white_colors) > 1:
        # Handle case with multiple non-white colors if necessary,
        # but based on examples, assume only one.
        # For now, just pick the first one found.
        print(f"Warning: Multiple non-white colors found: {non_white_colors}. Using {non_white_colors[0]}.")
        fill_color = non_white_colors[0]
    else:
        fill_color = non_white_colors[0]

    # Find coordinates efficiently using numpy
    coords = list(zip(*np.where(grid == fill_color))) # Returns list of (row, col) tuples
    return int(fill_color), coords

def transform(input_grid):
    """
    Applies the fill transformation based on the diagonal line in the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. & 2. Identify the fill color and the coordinates of the input line pixels
    fill_color, input_coords = find_fill_color_and_coords(input_np)

    # Handle edge case where there's no fill color (e.g., all white input)
    if fill_color == 0 or not input_coords:
        return input_np # Return input as is or an all-white grid

    # 3. Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # 4. Iterate through each pixel position in the potential output grid
    for r_out in range(height):
        for c_out in range(width):
            # 5. Check the condition against all input coordinates
            fill_pixel = False
            for r_in, c_in in input_coords:
                if r_out >= r_in and c_out <= c_in:
                    fill_pixel = True
                    break # Found a condition match, no need to check further for this output pixel

            # 6. If the condition was met, fill the output pixel
            if fill_pixel:
                output_grid[r_out, c_out] = fill_color
            # 7. Otherwise, it remains white (0) as initialized

    return output_grid.tolist() # Return as list of lists if required by ARC standard
```
