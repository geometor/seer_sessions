
## train_1

**input:**
```
0 8 0 0 8 0 0
8 8 0 0 8 8 0
0 8 8 0 8 8 0
0 8 8 0 8 8 0
0 0 8 8 0 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 4 0 0
2 2 0 0 4 4 0
0 1 1 0 1 1 0
0 1 1 0 1 1 0
0 0 3 3 0 0 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 8 0 0 0
8 8 8 8 8 0 0
0 8 8 0 8 8 0
0 8 8 8 8 0 0
0 0 0 8 8 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 1 1 0 0 0
3 3 1 1 4 0 0
0 3 2 0 4 4 0
0 2 2 1 1 0 0
0 0 0 1 1 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_3

**input:**
```
8 8 8 0 0 0 0
8 8 8 8 0 0 0
8 8 0 8 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
1 1 4 0 0 0 0
1 1 4 4 0 0 0
3 3 0 2 0 0 0
0 3 2 2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming an input grid containing white (0) and azure (8) pixels into an output grid of the same dimensions. The white pixels remain unchanged. The azure pixels are replaced by one of four colors: blue (1), red (2), green (3), or yellow (4). The core challenge lies in determining the rule that dictates which of the four colors replaces a specific azure pixel. The transformation appears to depend on the local neighborhood of each azure pixel, specifically the pattern of other azure pixels within a 2x2 square starting at the pixel's location.

*   **Facts:**
    
```yaml
    task_type: color_transformation
    grid_properties:
      - input_output_size_identical: true
      - background_color: 0 # white
    objects:
      - type: pixel_group
        color: 8 # azure
        input_representation: contiguous_blocks
        output_representation: same_pixels_recolored
    transformations:
      - type: recoloring
        input_color: 8 # azure
        output_colors: [1, 2, 3, 4] # blue, red, green, yellow
        rule_basis: local_pattern
        pattern_scope: 2x2_neighborhood
        details: Each azure pixel in the input is assigned an output color based on the configuration of azure pixels within the 2x2 square for which the input pixel is the top-left corner. White pixels remain white.
    color_mapping_rule (hypothesis):
      - pattern: '[[8,0],[0,0]]' -> color: 3 # green
      - pattern: '[[8,8],[0,0]]' -> color: 1 # blue
      - pattern: '[[8,0],[8,0]]' -> color: 2 # red
      - pattern: '[[8,0],[0,8]]' -> color: 3 # green
      - pattern: '[[8,8],[8,0]]' -> color: 3 # green
      - pattern: '[[8,8],[0,8]]' -> color: 2 # red
      - pattern: '[[8,0],[8,8]]' -> color: 4 # yellow
      - pattern: '[[8,8],[8,8]]' -> color: 1 # blue
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with white (0).
    2.  Iterate through each pixel `(r, c)` in the input grid, from top-to-bottom, left-to-right.
    3.  If the input pixel `input[r, c]` is white (0), skip to the next pixel.
    4.  If the input pixel `input[r, c]` is azure (8):
        a.  Examine the 2x2 neighborhood block starting at `(r, c)`. Consider pixels outside the grid boundaries as white (0). Let this block be `P = [[input[r,c], input[r,c+1]], [input[r+1,c], input[r+1,c+1]]]`.
        b.  Determine the output color `C` based on the pattern `P` according to the following rules:
            *   If `P` is `[[8,0],[0,0]]`, `C` is 3 (green).
            *   If `P` is `[[8,8],[0,0]]`, `C` is 1 (blue).
            *   If `P` is `[[8,0],[8,0]]`, `C` is 2 (red).
            *   If `P` is `[[8,0],[0,8]]`, `C` is 3 (green).
            *   If `P` is `[[8,8],[8,0]]`, `C` is 3 (green).
            *   If `P` is `[[8,8],[0,8]]`, `C` is 2 (red).
            *   If `P` is `[[8,0],[8,8]]`, `C` is 4 (yellow).
            *   If `P` is `[[8,8],[8,8]]`, `C` is 1 (blue).
            *   (Handle patterns not starting with 8 if necessary, though step 4 ensures `input[r,c]` is 8).
        c.  Set the corresponding pixel in the output grid `output[r, c]` to the determined color `C`.
    5.  Return the completed output grid.
```python
import numpy as np

"""
Transforms an input grid where azure (8) pixels are recolored based on the 
pattern of azure pixels in their 2x2 neighborhood (starting at the pixel).
White (0) pixels remain unchanged.

The specific mapping rules for the 2x2 neighborhood patterns (top-left, top-right, 
bottom-left, bottom-right) to the output color for the top-left pixel are:
- (8,0,0,0) -> 3 (green)
- (8,8,0,0) -> 1 (blue)
- (8,0,8,0) -> 2 (red)
- (8,0,0,8) -> 3 (green)
- (8,8,8,0) -> 3 (green)
- (8,8,0,8) -> 2 (red)
- (8,0,8,8) -> 4 (yellow)
- (8,8,8,8) -> 1 (blue)
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a 2x2 neighborhood pattern-based color transformation to azure pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Pad the input array with 0s (white) on the right and bottom edges 
    # to handle boundary conditions when extracting 2x2 neighborhoods.
    # We need 1 layer of padding at the bottom and right.
    padded_input = np.pad(input_array, ((0, 1), (0, 1)), mode='constant', constant_values=0)

    # Initialize the output grid with the same dimensions as the input, filled with 0s (white)
    output_array = np.zeros_like(input_array)

    # Define the mapping from 2x2 patterns (flattened tuple) to output colors
    # The pattern tuple represents (top-left, top-right, bottom-left, bottom-right)
    pattern_map = {
        (8, 0, 0, 0): 3,  # green
        (8, 8, 0, 0): 1,  # blue
        (8, 0, 8, 0): 2,  # red
        (8, 0, 0, 8): 3,  # green (Corrected based on train_1 example: pixel (4,3) -> 3)
        (8, 8, 8, 0): 3,  # green
        (8, 8, 0, 8): 2,  # red   (Corrected based on train_2 example: pixel (2,2) -> 2)
        (8, 0, 8, 8): 4,  # yellow
        (8, 8, 8, 8): 1,  # blue
    }

    # Iterate through each pixel of the original input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the original input is azure (8)
            if input_array[r, c] == 8:
                # Extract the 2x2 neighborhood from the padded input
                # The top-left of the neighborhood corresponds to (r, c) in the original grid
                neighborhood = padded_input[r:r+2, c:c+2]

                # Flatten the neighborhood into a tuple to use as a key for the map
                pattern = tuple(neighborhood.flatten())

                # Look up the corresponding output color from the pattern map
                # Default to 0 (white) if the pattern is somehow not found (though should not happen if input[r,c] is 8)
                output_color = pattern_map.get(pattern, 0) 

                # Assign the determined color to the output grid at the same position
                output_array[r, c] = output_color
            else:
                # If the input pixel is not azure (i.e., it's white), keep it white in the output
                output_array[r, c] = input_array[r, c] # which is 0

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
