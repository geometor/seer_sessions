
## train_1

**input:**
```
2 3 3 3 2
3 3 5 3 3
3 5 5 5 3
3 3 5 3 3
2 3 3 3 2
```


**output:**
```
2 3 3 3 2 2 5 3 2 5
3 3 5 3 3 2 5 3 2 5
3 5 5 5 3 2 5 3 2 5
3 3 5 3 3 2 5 3 2 5
2 3 3 3 2 2 5 3 2 5
2 2 2 2 2 5 5 3 2 5
5 5 5 5 5 5 3 3 2 5
3 3 3 3 3 3 3 2 2 5
2 2 2 2 2 2 2 2 5 5
5 5 5 5 5 5 5 5 5 3
```


## train_2

**input:**
```
9 8 8 8 9
8 8 2 8 8
8 2 2 2 8
8 8 2 8 8
9 8 8 8 9
```


**output:**
```
9 8 8 8 9 9 2 8 9 2
8 8 2 8 8 9 2 8 9 2
8 2 2 2 8 9 2 8 9 2
8 8 2 8 8 9 2 8 9 2
9 8 8 8 9 9 2 8 9 2
9 9 9 9 9 2 2 8 9 2
2 2 2 2 2 2 8 8 9 2
8 8 8 8 8 8 8 9 9 2
9 9 9 9 9 9 9 9 2 2
2 2 2 2 2 2 2 2 2 8
```

*   **Perception:**
    *   The input is a square grid (5x5 in the examples).
    *   The output is a square grid with double the dimensions of the input (10x10 in the examples).
    *   The output grid is composed of four quadrants, each the size of the original input grid.
    *   The top-left and bottom-left quadrants of the output are identical copies of the input grid.
    *   The top-right and bottom-right quadrants of the output are modified versions of the input grid.
    *   The modification involves swapping two specific colors within the input grid pattern.
    *   To determine which colors are swapped, analyze the frequency of colors in the input grid. Identify the two colors that appear most frequently. These two colors are swapped in the modified quadrants. The color(s) with lower frequencies remain in their original positions in the modified quadrants.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      input_size: NxN (e.g., 5x5)
      output_size: 2Nx2N (e.g., 10x10)
    components:
      - input_grid: The original NxN grid.
      - output_grid: The resulting 2Nx2N grid.
      - output_quadrants: The output grid is divided into four NxN quadrants.
        - top_left_quadrant: (rows 0 to N-1, cols 0 to N-1)
        - top_right_quadrant: (rows 0 to N-1, cols N to 2N-1)
        - bottom_left_quadrant: (rows N to 2N-1, cols 0 to N-1)
        - bottom_right_quadrant: (rows N to 2N-1, cols N to 2N-1)
    transformation_rules:
      - rule_1:
          action: copy
          source: input_grid
          target: output_quadrants
          quadrants: [top_left_quadrant, bottom_left_quadrant]
          condition: none
      - rule_2:
          action: modify_and_copy
          source: input_grid
          target: output_quadrants
          quadrants: [top_right_quadrant, bottom_right_quadrant]
          modification:
            type: color_swap
            details:
              - step: count color frequencies in the input_grid.
              - step: identify the two colors with the highest frequencies (color_A, color_B).
              - step: create a modified grid by iterating through the input_grid. If a pixel is color_A, change it to color_B. If a pixel is color_B, change it to color_A. Keep all other colors the same.
              - result: Use this modified grid for the specified quadrants.
    relationships:
      - The output grid size is determined by doubling the input grid dimensions.
      - The content of the output quadrants depends on the input grid and a color frequency analysis.
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height H, width W) of the input grid.
    2.  Create a new output grid with dimensions 2H x 2W.
    3.  Copy the input grid directly into the top-left quadrant (rows 0 to H-1, columns 0 to W-1) of the output grid.
    4.  Copy the input grid directly into the bottom-left quadrant (rows H to 2H-1, columns 0 to W-1) of the output grid.
    5.  Analyze the input grid to count the occurrences of each color.
    6.  Identify the two colors with the highest frequencies. Let these be `color1` and `color2`.
    7.  Create a modified version of the input grid: Iterate through each pixel of the input grid. If the pixel's color is `color1`, set the corresponding pixel in the modified grid to `color2`. If the pixel's color is `color2`, set the corresponding pixel to `color1`. Otherwise, keep the original color.
    8.  Copy this modified grid into the top-right quadrant (rows 0 to H-1, columns W to 2W-1) of the output grid.
    9.  Copy this modified grid into the bottom-right quadrant (rows H to 2H-1, columns W to 2W-1) of the output grid.
    10. Return the completed output grid.
```python
import numpy as np
from collections import Counter

"""
1.  Determine the dimensions (height H, width W) of the input grid.
2.  Create a new output grid with dimensions 2H x 2W.
3.  Copy the input grid directly into the top-left quadrant (rows 0 to H-1, columns 0 to W-1) of the output grid.
4.  Copy the input grid directly into the bottom-left quadrant (rows H to 2H-1, columns 0 to W-1) of the output grid.
5.  Analyze the input grid to count the occurrences of each color.
6.  Identify the two colors with the highest frequencies. Let these be `color1` and `color2`. Handle cases where there are fewer than two distinct colors.
7.  Create a modified version of the input grid: Iterate through each pixel of the input grid. If the pixel's color is `color1`, set the corresponding pixel in the modified grid to `color2`. If the pixel's color is `color2`, set the corresponding pixel to `color1`. Otherwise, keep the original color. If fewer than two distinct colors were found, the modified grid is identical to the input grid.
8.  Copy this modified grid into the top-right quadrant (rows 0 to H-1, columns W to 2W-1) of the output grid.
9.  Copy this modified grid into the bottom-right quadrant (rows H to 2H-1, columns W to 2W-1) of the output grid.
10. Return the completed output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by creating a 2x2 tiled output grid.
    The top-left and bottom-left tiles are copies of the input.
    The top-right and bottom-right tiles are copies of the input
    with the two most frequent colors swapped.
    """
    # Convert input_grid to numpy array if it's not already
    input_grid = np.array(input_grid)
    
    # 1. Determine the dimensions (height H, width W) of the input grid.
    H, W = input_grid.shape

    # 2. Create a new output grid with dimensions 2H x 2W.
    output_grid = np.zeros((2 * H, 2 * W), dtype=input_grid.dtype)

    # 3. Copy the input grid directly into the top-left quadrant.
    output_grid[0:H, 0:W] = input_grid

    # 4. Copy the input grid directly into the bottom-left quadrant.
    output_grid[H:2*H, 0:W] = input_grid

    # 5. Analyze the input grid to count the occurrences of each color.
    color_counts = Counter(input_grid.flatten())
    
    # 6. Identify the two colors with the highest frequencies.
    most_common = color_counts.most_common()

    modified_grid = input_grid.copy()
    
    # Check if there are at least two distinct colors to swap
    if len(most_common) >= 2:
        color1 = most_common[0][0]
        color2 = most_common[1][0]
        
        # 7. Create a modified version of the input grid by swapping color1 and color2.
        # Create masks for pixels with color1 and color2
        mask1 = (input_grid == color1)
        mask2 = (input_grid == color2)
        
        # Apply the swap using the masks
        modified_grid[mask1] = color2
        modified_grid[mask2] = color1
    # else: if less than 2 colors, modified_grid remains a copy of input_grid

    # 8. Copy this modified grid into the top-right quadrant.
    output_grid[0:H, W:2*W] = modified_grid

    # 9. Copy this modified grid into the bottom-right quadrant.
    output_grid[H:2*H, W:2*W] = modified_grid

    # 10. Return the completed output grid.
    return output_grid
```
