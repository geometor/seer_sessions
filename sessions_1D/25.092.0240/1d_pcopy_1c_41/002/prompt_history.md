
## train_1

**input:**
```
0 0 5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 0 0 0 0 4 0 0 0 0 0 4 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 4 4 4 0 0 0 4 4 4 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 7 7 7 0 0 7 0 0 0 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 0 7 7 7 0 0 0 7 7 7 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are grids of pixels, likely 3 rows by 11 columns based on the data length (33) and visual grouping in the examples.
    *   The primary elements are the background (white pixels, value 0) and foreground objects.
    *   Foreground objects in the input consist of either single pixels of a specific color (gray, yellow, orange) or horizontal lines of three identical pixels of that same color.
    *   The transformation specifically targets the single-pixel objects.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_representation: 2D array of integers (0-9).
      grid_dimensions_analysis: Input/output data has 33 values; assuming 3x11 grid structure based on visual patterns.
      background_color: white (0).
      foreground_colors_observed: gray (5), yellow (4), orange (7).
    object_definitions:
      - object_type: background
        pixels: All cells with value 0.
        properties: Static unless overwritten.
      - object_type: colored_pixel_group
        pixels: Contiguous cells with the same non-zero color value.
        connectivity: Assumed horizontal adjacency primarily relevant.
    input_features:
      - feature: Single Pixels
        description: Isolated non-white pixels. Examples - gray at (0,9) in train_1; yellow at (0,9), (1,5), (1,9) in train_2; orange at (0,6), (1,1), (1,5) in train_3.
        properties: Color varies (gray, yellow, orange); Size is 1x1.
      - feature: Horizontal Triplet
        description: Horizontal line of 3 identical non-white pixels. Examples - gray `5 5 5` in train_1; yellow `4 4 4` in train_2; orange `7 7 7` in train_3.
        properties: Color varies; Size is 1x3.
    transformation_observations:
      - action: Expansion
        target: Single non-white pixels found in the input grid.
        result: The single pixel is expanded into a horizontal triplet (1x3 line) of the same color, starting at the original pixel's position and extending to the right.
        overwrite_behavior: Expansion overwrites any existing pixels (including white background) in the target locations.
      - action: Preservation
        target: Horizontal triplets (1x3 lines) already present in the input grid.
        result: These objects remain unchanged in the output grid.
      - relationship: The transformation depends on the shape/size of the non-white object in the input. Single pixels are expanded; existing 1x3 lines are kept.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each cell (pixel) of the input grid, checking its row `r` and column `c`.
    3.  If the pixel at `(r, c)` in the input grid is non-white (not 0):
        a.  Check if this pixel is part of a horizontal line of three identical pixels starting at `(r, c-2)`, `(r, c-1)`, or `(r, c)` in the *input* grid. Specifically, check if it satisfies the condition for being a single pixel object: it must be non-white AND it must NOT be the case that (`input[r, c] == input[r, c+1] == input[r, c+2]`) AND it must NOT be the case that (`input[r, c-1] == input[r, c] == input[r, c+1]`) AND it must NOT be the case that (`input[r, c-2] == input[r, c-1] == input[r, c]`).
        b.  A simpler way to identify the target pixels: Check if the pixel at `(r, c)` in the input grid is non-white AND it is *not* followed immediately to the right by two more pixels of the *same* color (i.e., `input[r, c+1]` or `input[r, c+2]` are either out of bounds, white, or a different color) AND it is *not* preceded immediately to the left by two pixels of the *same* color (similar check for `input[r, c-1]` and `input[r, c-2]`).
        c.  Alternative rule formulation (Object-based): Identify all connected components (objects) of non-white pixels in the input grid. If an object consists of exactly one pixel located at `(r, c)` with color `C`:
            i.  In the *output* grid, ensure the pixel at `(r, c)` retains color `C`.
            ii. If the column `c+1` is within the grid bounds, change the pixel at `(r, c+1)` in the *output* grid to color `C`.
            iii. If the column `c+2` is within the grid bounds, change the pixel at `(r, c+2)` in the *output* grid to color `C`.
    4.  Pixels belonging to input objects that are *not* single pixels (i.e., the existing 1x3 horizontal lines) remain unchanged in the output grid because they were copied initially and are not modified by step 3c.
    5.  Return the modified output grid.
```python
import numpy as np

"""
Transforms the input grid by identifying isolated, non-white pixels and expanding 
them into a horizontal line of three pixels of the same color, starting from 
the original pixel's position and extending to the right. Existing horizontal 
lines of three identical non-white pixels remain unchanged. The expansion 
overwrites any existing pixels in the target locations.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each cell (pixel) of the input grid at row `r` and column `c`.
3. If the pixel at `(r, c)` in the input grid is non-white (value > 0):
   a. Check if this pixel is isolated horizontally. A pixel is considered isolated 
      if its immediate left neighbor (if it exists) and its immediate right 
      neighbor (if it exists) are either the background color (0) or a 
      different color than the pixel itself.
   b. If the pixel at `(r, c)` is identified as isolated and non-white:
      i. Get the color `C` of the pixel `input_grid[r, c]`.
      ii. In the output grid, set the pixel at `(r, c)` to color `C`. 
         (This is already true from the initial copy, but confirms intent).
      iii. If the column `c + 1` is within the grid bounds, set the pixel 
          at `(r, c + 1)` in the output grid to color `C`.
      iv. If the column `c + 2` is within the grid bounds, set the pixel 
          at `(r, c + 2)` in the output grid to color `C`.
4. Pixels that were part of the original grid and were not identified as isolated, 
   non-white pixels remain unchanged in the output grid (due to the initial copy 
   and lack of modification).
5. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.
        
    Returns:
        np.ndarray: A 2D NumPy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_grid[r, c]

            # Check if the pixel is non-white
            if pixel_color > 0:
                # Check if the pixel is horizontally isolated
                is_isolated = True
                
                # Check left neighbor
                if c > 0 and input_grid[r, c - 1] == pixel_color:
                    is_isolated = False
                
                # Check right neighbor
                if c < width - 1 and input_grid[r, c + 1] == pixel_color:
                    is_isolated = False

                # If the pixel is isolated and non-white, expand it
                if is_isolated:
                    # The pixel itself keeps its color (already set by copy)
                    # output_grid[r, c] = pixel_color 

                    # Expand to the right, checking bounds
                    if c + 1 < width:
                        output_grid[r, c + 1] = pixel_color
                    if c + 2 < width:
                        output_grid[r, c + 2] = pixel_color

    return output_grid
```
