
## train_1

**input:**
```
0 0 0
0 2 3
0 3 3
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 3 3 3 3
```


## train_2

**input:**
```
3 3 0
3 2 0
0 0 0
```


**output:**
```
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
3 3 3 3 0 0 0 0 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0
```

*   **Perception**: The task involves transforming a small input grid into a larger output grid. The output grid's dimensions are exactly three times the input grid's dimensions in both height and width. This suggests a scaling operation where each pixel in the input grid corresponds to a 3x3 block of pixels in the output grid. Observing the color changes, most input pixel colors directly determine the color of their corresponding 3x3 block in the output. However, there's a specific exception: red (2) pixels in the input result in a 3x3 block of white (0) pixels in the output. All other colors seem to map directly (e.g., green input -> green block, white input -> white block).

*   **Facts**:
    
```yaml
    task_type: grid_transformation
    transformation: scaling_with_color_replacement
    input_grid:
      description: A small grid (e.g., 3x3).
      elements: Pixels with colors including white (0), red (2), green (3).
    output_grid:
      description: A larger grid, dimensions are 3 times the input grid dimensions.
      elements: Pixels with colors including white (0) and green (3). Red (2) is absent.
      derivation: Based on scaling the input grid.
    scaling_factor: 3
    pixel_mapping:
      rule: Each input pixel at (r, c) maps to a 3x3 block in the output grid starting at (r*3, c*3).
      color_rule:
        - condition: Input pixel color is red (2).
          action: Corresponding output 3x3 block is filled with white (0).
        - condition: Input pixel color is not red (2).
          action: Corresponding output 3x3 block is filled with the input pixel's color.
    objects:
      - type: pixel
        properties: color, grid_location
      - type: block (3x3)
        properties: color, grid_location (top-left corner)
        relationship: Derived from a single input pixel.
    ```


*   **Natural Language Program**:
    1.  Determine the height `H` and width `W` of the input grid.
    2.  Create a new output grid with height `3 * H` and width `3 * W`. Initialize all its pixels to white (0).
    3.  Iterate through each pixel of the input grid using its row index `r` (from 0 to `H-1`) and column index `c` (from 0 to `W-1`).
    4.  Let `input_color` be the color of the input pixel at `(r, c)`.
    5.  Define the target 3x3 block in the output grid: the pixels from row `r * 3` to `r * 3 + 2` and column `c * 3` to `c * 3 + 2`.
    6.  If `input_color` is red (2), leave the target 3x3 block in the output grid as white (0).
    7.  If `input_color` is *not* red (2), fill all pixels in the target 3x3 block in the output grid with `input_color`.
    8.  Return the completed output grid.
```python
import numpy as np

"""
Scales the input grid by a factor of 3. Each pixel in the input grid determines the 
color of a corresponding 3x3 block in the output grid. If the input pixel color 
is red (2), the corresponding 3x3 output block is filled with white (0). Otherwise, 
the 3x3 output block is filled with the input pixel's color.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid by scaling it 3x and applying a color replacement rule.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Calculate output dimensions
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize output grid with white (0)
    # Using white as the default handles the red (2) -> white (0) case automatically
    # if we only overwrite for non-red colors.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_np[r, c]

            # Determine the color for the output block
            # If input is red (2), output block remains white (0) as initialized.
            # Otherwise, output block takes the input color.
            if input_color != 2:
                output_color = input_color

                # Define the top-left corner of the 3x3 block in the output grid
                start_row = r * 3
                start_col = c * 3

                # Fill the 3x3 block in the output grid
                for i in range(3):
                    for j in range(3):
                        output_grid[start_row + i, start_col + j] = output_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
