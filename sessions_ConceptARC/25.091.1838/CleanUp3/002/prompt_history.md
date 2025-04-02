
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 8 7 7 7 7 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0 0 4 4 8 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 8 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 6 6 6 6 6 0 0
8 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 8 0 0 6 8 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 0 3
0 0 3 3 3 3 3 3 3 3 0 0 3 3 0
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3
0 0 3 0 3 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 2 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 0 0
0 2 2 2 0 0 0 0 0 0 2 2 2 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 3 3 3 3 3 0 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
```

Okay, let's analyze the provided examples to understand the transformation.

*   **Note:** The prompt provided data for `train_2` but labeled the section `train_1`. It then provided data labeled `train_1`. I will assume these are two distinct examples, `example_1` (Azure removal) and `example_2` (3x3 fill), illustrating the task's logic.

## Perception

1.  **Example 1 (Azure Removal):**
    *   The input grid contains several distinct objects composed of Orange (7), Yellow (4), and Magenta (6) pixels, along with numerous scattered single pixels of Azure (8).
    *   The output grid is identical to the input grid, except all Azure (8) pixels have been replaced by white (0) pixels.
    *   The transformation appears to be a targeted removal of all pixels of a specific color (Azure).

2.  **Example 2 (3x3 Fill):**
    *   The input grid contains large shapes made of Green (3) and Red (2), along with some smaller, less dense groupings of these colors, interspersed with white (0). Notably, Azure (8) is absent.
    *   The output grid shows that the large shapes remain mostly unchanged. However, in two specific 3x3 regions, white pixels have been filled in.
        *   A 3x3 area in the top-right (rows 0-2, cols 12-14) originally contained 8 Green pixels and 1 white pixel. In the output, the white pixel is filled with Green.
        *   A 3x3 area in the middle-right (rows 4-6, cols 11-13) originally contained 7 Red pixels and 2 white pixels. In the output, the white pixels are filled with Red.
    *   The transformation identifies 3x3 areas that are densely populated by a single non-white color (at least 6 out of 9 pixels) and fills any white pixels within that 3x3 area with the dominant color.

3.  **Overall Logic:** The task seems to have two distinct modes of operation, determined by the presence of Azure (8) pixels in the input:
    *   If Azure (8) is present, remove all Azure pixels.
    *   If Azure (8) is *not* present, apply the 3x3 density fill rule.

## Facts


```yaml
task_type: conditional_transformation
condition_feature: presence_of_color_azure_8

# Rule 1: Activated if Azure (8) is present
rule_1:
  name: remove_azure_pixels
  trigger:
    property: color
    value: 8 # Azure
  action:
    type: replace_pixels
    source_color: 8 # Azure
    target_color: 0 # white

# Rule 2: Activated if Azure (8) is NOT present
rule_2:
  name: fill_dense_3x3_squares
  trigger:
    condition: color 8 (Azure) is absent in input
  target: 3x3 pixel squares within the grid
  condition_for_action:
    - structure: 3x3 square
    - property: color_density
    - check: unique_dominant_non_white_color
    - dominant_color_name: C
    - dominant_color_count_threshold: >= 6
  action:
    type: replace_pixels_in_subgrid
    subgrid: 3x3 square matching the condition
    source_color: 0 # white
    target_color: C # the unique dominant non-white color
    scope: apply changes to a copy of the grid, using original input for conditions

# General Observations
grid_properties:
  size: variable height and width
  colors: 0-9 used, representing different categories/objects
objects:
  - type: contiguous_shapes (e.g., Orange, Yellow, Magenta, Green, Red shapes)
  - type: scattered_pixels (e.g., Azure pixels in example 1, Green/Red pixels in example 2 before filling)
relationships:
  - adjacency: pixels within shapes, pixels within 3x3 squares
  - density: count of colors within a local area (3x3 square)
```


## Natural Language Program

1.  Examine the input grid to determine if any pixels have the color Azure (8).
2.  **If Azure (8) pixels are present:**
    a. Create a copy of the input grid to serve as the output grid.
    b. Iterate through every cell `(row, column)` in the grid.
    c. If the cell in the input grid at `(row, column)` contains Azure (8), set the corresponding cell in the output grid to white (0).
    d. All other cells retain their original color.
3.  **If Azure (8) pixels are *not* present:**
    a. Create a copy of the input grid to serve as the output grid.
    b. Iterate through all possible 3x3 squares within the input grid. Define a 3x3 square by its top-left corner `(r, c)`, where `r` ranges from 0 to `height-3` and `c` ranges from 0 to `width-3`.
    c. For each 3x3 square:
        i. Count the occurrences of each color (0-9) within this square in the *input* grid.
        ii. Find the non-white color `C` that occurs most frequently within the square.
        iii. Check if this color `C` is the *unique* most frequent non-white color (i.e., no other non-white color occurs with the same highest frequency).
        iv. Check if the count of color `C` is 6 or greater.
        v. If both conditions (unique dominant non-white color `C` AND count >= 6) are met:
            - Iterate through each cell `(rr, cc)` within this 3x3 square (from `(r, c)` to `(r+2, c+2)`).
            - If the cell `(rr, cc)` in the *input* grid is white (0), change the corresponding cell `(rr, cc)` in the *output* grid to color `C`.
4.  Return the final output grid.
```python
import numpy as np
from collections import Counter

"""
The transformation rule depends on the presence of the color Azure (8) in the input grid.

Rule 1: If Azure (8) is present in the input grid:
- Replace all pixels with the color Azure (8) with white (0).
- All other pixels remain unchanged.

Rule 2: If Azure (8) is NOT present in the input grid:
- Iterate through all possible 3x3 subgrids within the input grid.
- For each 3x3 subgrid:
    - Count the occurrences of each non-white color.
    - Find the non-white color 'C' that appears most frequently.
    - Check if this color 'C' is the unique most frequent non-white color (no ties for the highest frequency among non-white colors).
    - Check if the count of color 'C' is 6 or greater.
    - If both conditions (unique dominant color and count >= 6) are met:
        - In the corresponding 3x3 area of the output grid, replace any white (0) pixels with the dominant color 'C'. Note: Use the original input grid to identify the white pixels to change, but apply the change to the output grid.
- Pixels not part of such qualifying 3x3 squares, or non-white pixels within qualifying squares, remain unchanged.
"""

def transform(input_grid):
    """
    Applies the conditional transformation rule based on the presence of Azure (8).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Check if Azure (color 8) is present
    azure_present = np.any(input_grid_np == 8)

    if azure_present:
        # Rule 1: Remove Azure pixels
        # Find all locations where the input grid has color 8
        azure_locations = (input_grid_np == 8)
        # Set those locations to white (0) in the output grid
        output_grid_np[azure_locations] = 0
    else:
        # Rule 2: Fill dense 3x3 squares
        # Iterate through all possible top-left corners (r, c) of 3x3 squares
        for r in range(height - 2):
            for c in range(width - 2):
                # Extract the 3x3 subgrid from the input
                subgrid = input_grid_np[r:r+3, c:c+3]

                # Count non-white colors in the subgrid
                non_white_pixels = subgrid[subgrid != 0]
                if non_white_pixels.size == 0:
                    continue # Skip if the subgrid is all white

                colors, counts = np.unique(non_white_pixels, return_counts=True)

                # Find the maximum count among non-white colors
                max_count = np.max(counts)

                # Check if the count threshold is met (>= 6)
                if max_count >= 6:
                    # Check if the maximum count is unique (only one color has this max count)
                    if np.sum(counts == max_count) == 1:
                        # Find the unique dominant color
                        dominant_color = colors[np.argmax(counts)]

                        # Identify white pixels within this 3x3 subgrid in the input
                        white_mask_in_subgrid = (subgrid == 0)

                        # Apply the dominant color to the corresponding white pixels in the output grid's subgrid
                        output_subgrid = output_grid_np[r:r+3, c:c+3]
                        output_subgrid[white_mask_in_subgrid] = dominant_color

    # Convert the final NumPy array back to a list of lists
    return output_grid_np.tolist()

```
