
## train_1

**input:**
```
3 2 0 2 2
3 3 0 2 2
0 0 0 0 0
3 2 0 3 2
3 3 0 3 3
```


**output:**
```
3 3 0 3 2
3 3 0 3 3
0 0 0 0 0
3 3 0 3 3
3 3 0 3 3
```


## train_2

**input:**
```
1 1 0 1 1
1 8 0 1 8
0 0 0 5 0
5 1 5 8 5
5 5 0 8 8
```


**output:**
```
1 1 0 1 1
1 1 0 1 1
0 0 0 0 0
1 1 0 1 1
1 1 0 1 8
```


## train_3

**input:**
```
3 3 4 0 3 3 4 0 4 4 4
3 3 4 0 3 3 4 0 4 4 4
4 3 3 0 4 3 3 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
3 3 4 0 3 3 4 0 4 4 4
3 3 4 0 3 3 4 5 4 4 4
4 3 3 0 5 3 3 0 4 4 4
0 0 0 0 5 5 0 0 0 0 0
4 4 4 5 5 5 4 0 3 3 4
4 5 5 5 3 3 4 0 3 3 4
4 4 5 0 4 3 3 0 4 3 3
```


**output:**
```
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 4 3 3
0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 4 3 3
0 0 0 0 0 0 0 0 0 0 0
3 3 4 0 3 3 3 0 3 3 3
3 3 4 0 3 3 3 0 3 3 3
4 3 3 0 3 3 3 0 3 3 3
```


## train_4

**input:**
```
4 4 2 0 4 4 2 0 2 2 2
2 4 2 0 2 4 2 0 2 2 2
4 4 4 0 4 4 4 5 2 2 5
0 0 0 0 0 0 0 0 0 0 5
2 2 2 0 4 4 2 5 2 2 2
2 2 2 0 2 5 2 5 5 2 2
2 2 5 0 4 5 5 0 2 5 2
0 0 5 0 0 0 0 0 0 0 0
4 5 5 5 4 4 2 5 4 4 2
5 5 5 0 2 5 2 0 2 4 2
4 5 4 0 4 4 4 0 4 4 4
```


**output:**
```
4 4 4 0 4 4 4 0 4 4 2
4 4 4 0 4 4 4 0 2 4 2
4 4 4 0 4 4 4 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
4 4 2 0 4 4 4 0 4 4 2
2 4 2 0 4 4 4 0 2 4 2
4 4 4 0 4 4 4 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 4 4 4 0 4 4 4
4 4 4 0 4 4 4 0 4 4 4
4 4 4 0 4 4 4 0 4 4 4
```

Okay, let's analyze the provided examples.

## Perception

1.  **Grid Structure:** The inputs and outputs are rectangular grids of varying sizes (5x5 and 11x11 in the examples).
2.  **Color Palette:** Multiple colors are used: green (3), red (2), white (0), blue (1), azure (8), gray (5), yellow (4). White (0) seems to act as a background or separator.
3.  **Invariant Pixels:** White (0) pixels remain unchanged in all examples.
4.  **Color Changes:** Other colors change based on their adjacency to a specific "dominant" color.
5.  **Dominant Color Identification:** In each example pair, one color seems to take precedence and "spread" to adjacent, non-white pixels.
    *   Example 1: Green (3) is dominant. Red (2) changes to green (3) if adjacent to green.
    *   Example 2: Blue (1) is dominant. Azure (8) and Gray (5) change to blue (1) if adjacent to blue.
    *   Example 3: Green (3) is dominant. Yellow (4) and Gray (5) change to green (3) if adjacent to green.
    *   Example 4: Yellow (4) is dominant. Red (2) and Gray (5) change to yellow (4) if adjacent to yellow.
6.  **Dominant Color Source:** The dominant color appears to be the color of the top-left pixel (0, 0) in the input grid in all provided examples.
7.  **Adjacency Rule:** The color change depends on non-diagonal adjacency (sharing an edge: up, down, left, or right). A pixel changes *if* at least one of its adjacent neighbors in the *input* grid has the dominant color.
8.  **Target Pixels:** Only pixels that are *not* white and *not* the dominant color are candidates for changing.
9.  **Transformation Logic:** The transformation identifies the dominant color from the top-left pixel. It then iterates through the grid. Any pixel that isn't white or the dominant color changes *to* the dominant color if it's adjacent to a dominant-colored pixel in the original input grid.

## Facts


```yaml
constants:
  - color_white: 0
  - adjacency_type: non-diagonal (up, down, left, right)

variables:
  - input_grid: 2D array of integers (colors)
  - output_grid: 2D array of integers (colors)
  - grid_dimensions: height and width of the input/output grids
  - dominant_color: The color identified as the primary agent of change.
  - target_pixel: A pixel whose color might change.
  - neighbor_pixel: A pixel adjacent to the target_pixel.

properties:
  - white pixels (color_white) are static and never change.
  - The dominant_color is determined by the color of the pixel at index (0, 0) in the input_grid.
  - Target_pixels are those whose color is neither color_white nor the dominant_color.

actions:
  - identify_dominant_color: Get the color from input_grid[0, 0].
  - iterate_pixels: Process each pixel (r, c) in the input_grid.
  - check_neighbors: For a target_pixel, examine its non-diagonal neighbors in the input_grid.
  - update_pixel: If a target_pixel has at least one neighbor with the dominant_color in the input_grid, change the target_pixel's color to the dominant_color in the output_grid. Otherwise, the pixel retains its original color.

relationships:
  - Adjacency: A target_pixel's potential change depends on the color of its adjacent neighbors in the input grid.
  - Dominance: The dominant_color replaces the color of adjacent target_pixels.
  - Invariance: White pixels and pixels already having the dominant_color are unaffected by the transformation.
```


## Natural Language Program

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Identify the `dominant_color` by reading the color value of the pixel at the top-left corner (row 0, column 0) of the `input_grid`.
3.  Iterate through each pixel `p` at coordinates `(row, col)` in the `input_grid`.
4.  Check the color of the current pixel `p`:
    *   If the color of `p` is the `dominant_color`, continue to the next pixel.
    *   If the color of `p` is white (0), continue to the next pixel.
5.  If the color of `p` is neither the `dominant_color` nor white:
    *   Examine the four non-diagonal neighbors (up, down, left, right) of `p` within the bounds of the `input_grid`.
    *   Check if any of these neighbors in the `input_grid` has the `dominant_color`.
    *   If at least one neighbor has the `dominant_color`, set the color of the corresponding pixel at `(row, col)` in the `output_grid` to the `dominant_color`.
6.  After iterating through all pixels, return the `output_grid`.
```python
import numpy as np

"""
Identify the dominant color from the top-left pixel (0,0) of the input grid.
Create an output grid initialized as a copy of the input grid.
Iterate through each pixel in the input grid.
If a pixel's color is neither white (0) nor the dominant color, check its non-diagonal neighbors (up, down, left, right) in the *input* grid.
If any of these neighbors has the dominant color, change the corresponding pixel's color in the *output* grid to the dominant color.
White pixels and pixels already having the dominant color remain unchanged.
Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the dominant color propagation rule.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Identify the dominant color from the top-left pixel
    dominant_color = input_np[0, 0]
    
    # Define white color constant
    color_white = 0
    
    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            current_color = input_np[r, c]
            
            # Skip processing if the pixel is white or already the dominant color
            if current_color == color_white or current_color == dominant_color:
                continue
                
            # Check non-diagonal neighbors
            found_dominant_neighbor = False
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Up, Down, Left, Right
                nr, nc = r + dr, c + dc
                
                # Check if neighbor coordinates are within grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if the neighbor in the *input* grid has the dominant color
                    if input_np[nr, nc] == dominant_color:
                        found_dominant_neighbor = True
                        break # No need to check other neighbors
            
            # If a dominant neighbor was found, update the pixel in the output grid
            if found_dominant_neighbor:
                output_grid[r, c] = dominant_color
                
    # Convert the result back to a list of lists
    return output_grid.tolist()

```
