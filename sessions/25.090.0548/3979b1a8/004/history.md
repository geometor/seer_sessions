
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
```python
import numpy as np
from collections import Counter
import copy

"""
Transforms the input grid based on color frequency ranks.

1.  Determine the dimensions (H, W) of the input grid.
2.  Analyze the input grid to find all unique colors and rank them by frequency.
    Let R1 be the most frequent, R2 the second most frequent, and R3 the third most frequent.
    Handle cases where there are fewer than 3 distinct colors.
3.  Create four intermediate grids (G1, G2, G3, G4), each of size HxW.
4.  G1: A direct copy of the input grid.
5.  G2: A copy of the input grid where colors R1 and R2 are swapped. If R2 does not exist, G2 is identical to G1.
6.  G3: A direct copy of G2.
7.  G4: A copy of G2 where colors R2 and R3 are swapped. 
    - If R3 does not exist, G4 is identical to G2.
    - If R2 does not exist (meaning only R1 exists), G4 is identical to G2 (which is identical to G1).
8.  Create the final output grid with dimensions 2H x 2W.
9.  Place G1 in the top-left quadrant (TL).
10. Place G2 in the top-right quadrant (TR).
11. Place G3 in the bottom-left quadrant (BL).
12. Place G4 in the bottom-right quadrant (BR).
13. Return the output grid.
"""

def swap_colors(grid: np.ndarray, color_a, color_b) -> np.ndarray:
    """Creates a new grid with two specified colors swapped."""
    if color_a is None or color_b is None or color_a == color_b:
        return grid.copy() # No swap needed if colors are missing or the same
        
    new_grid = grid.copy()
    mask_a = (grid == color_a)
    mask_b = (grid == color_b)
    new_grid[mask_a] = color_b
    new_grid[mask_b] = color_a
    return new_grid

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by creating a 2x2 tiled output grid based on color frequency swaps.
    TL = Input
    TR = Input with (Most Freq <-> 2nd Most Freq) swap
    BL = TR
    BR = TR with (2nd Most Freq <-> 3rd Most Freq) swap
    """
    input_grid = np.array(input_grid)
    H, W = input_grid.shape

    # Analyze color frequencies and determine ranks R1, R2, R3
    color_counts = Counter(input_grid.flatten())
    ranked_colors = [item[0] for item in color_counts.most_common()]
    
    R1 = ranked_colors[0] if len(ranked_colors) > 0 else None
    R2 = ranked_colors[1] if len(ranked_colors) > 1 else None
    R3 = ranked_colors[2] if len(ranked_colors) > 2 else None

    # Create G1: Input grid
    G1 = input_grid.copy()

    # Create G2: Input with R1 <-> R2 swap
    G2 = swap_colors(input_grid, R1, R2)

    # Create G3: Copy of G2
    G3 = G2.copy() # Since G2 is already a modified copy

    # Create G4: G2 with R2 <-> R3 swap
    # Note: We apply the swap to G2 using the original R2 and R3 colors.
    G4 = swap_colors(G2, R2, R3)

    # Assemble the output grid
    output_grid = np.zeros((2 * H, 2 * W), dtype=input_grid.dtype)

    output_grid[0:H, 0:W] = G1       # Top-Left
    output_grid[0:H, W:2*W] = G2    # Top-Right
    output_grid[H:2*H, 0:W] = G3    # Bottom-Left
    output_grid[H:2*H, W:2*W] = G4 # Bottom-Right
    
    return output_grid
```
