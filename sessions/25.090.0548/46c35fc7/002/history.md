
## train_1

**input:**
```
9 6 5 7 7 7 7
8 7 1 7 7 7 7
0 8 9 7 7 7 7
7 7 7 7 7 7 7
7 7 7 1 8 4 7
7 7 7 4 7 6 7
7 7 7 6 2 4 7
```


**output:**
```
5 8 9 7 7 7 7
8 7 6 7 7 7 7
9 1 0 7 7 7 7
7 7 7 7 7 7 7
7 7 7 4 4 4 7
7 7 7 2 7 8 7
7 7 7 1 6 6 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 5 2 8 7 7
7 7 1 7 9 7 7
7 7 4 3 0 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 8 1 0 7 7
7 7 3 7 2 7 7
7 7 5 9 4 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7
7 7 7 6 5 5 7
7 7 7 5 7 6 7
7 7 7 1 5 1 7
8 8 8 7 7 7 7
9 7 9 7 7 7 7
0 0 0 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 5 5 1 7
7 7 7 5 7 5 7
7 7 7 6 6 1 7
8 9 0 7 7 7 7
0 7 8 7 7 7 7
8 9 0 7 7 7 7
```

Okay, let's break down this task.

**Perception**

1.  **Grid Size:** The grid dimensions vary across examples but are consistent between the input and output of a single example (e.g., 7x7 in all provided examples).
2.  **Background Color:** The color orange (7) appears frequently and seems to act as a background or neutral color, often remaining unchanged.
3.  **Transformation Areas:** The changes between input and output occur within distinct, localized 3x3 square regions.
4.  **Transformation Type:** Within these 3x3 regions, the pattern of pixels is altered. Comparing the input and output 3x3 blocks reveals a consistent 90-degree counter-clockwise rotation.
5.  **Identifying Regions:** The key challenge is determining *which* 3x3 regions are selected for rotation.
    *   In `train_1`, two regions are rotated: one at the top-left corner (0,0) and one near the bottom-right (4,3).
    *   In `train_2`, one region in the center (2,2) is rotated.
    *   In `train_3`, two regions are rotated: one near the top-right (1,3) and one at the bottom-left (4,0).
6.  **Selection Criteria:** Let's examine the properties of the rotated 3x3 blocks versus non-rotated ones. The background color orange (7) seems crucial. Observing the *corners* of the 3x3 blocks:
    *   Rotated blocks (Examples 1, 2, 3): *None* of their four corner cells are orange (7).
    *   Consider non-rotated 3x3 blocks: They invariably have at least one orange (7) pixel in a corner position. For instance, in `train_1`, the 3x3 block starting at (0,1) has orange corners at (0,3) and (2,3). The block starting at (1,1) has orange corners at (1,1), (1,3), (3,1), and (3,3).
7.  **Conclusion:** The rule appears to be: identify all 3x3 subgrids whose four corner cells are *not* orange (7). Rotate each of these identified 3x3 subgrids 90 degrees counter-clockwise in place. Pixels outside these rotated blocks, or within blocks that don't meet the corner criteria, remain unchanged. The examples do not show overlapping selected regions, suggesting the transformation is applied independently to each qualifying region.

**Facts**


```yaml
Input_Grid:
  type: 2D array of integers (pixels)
  properties:
    - variable dimensions (height, width)
    - contains pixels with values 0-9 (colors)
    - has a predominant background color: orange (7)

Output_Grid:
  type: 2D array of integers (pixels)
  properties:
    - same dimensions as the corresponding input grid
    - derived from the input grid via transformation

Objects:
  - type: Subgrid
    identifier: 3x3 blocks of pixels
    properties:
      - location (top-left coordinate)
      - pixels (9 integer values)
      - corner_pixels (pixels at relative coordinates (0,0), (0,2), (2,0), (2,2))
  - type: Pixel
    properties:
      - color (integer 0-9)
      - location (row, column)

Relationships:
  - Input_Grid contains multiple potential 3x3 Subgrids.
  - Output_Grid is a transformation of Input_Grid.
  - The transformation depends on the corner_pixels of specific 3x3 Subgrids within the Input_Grid.

Actions:
  - Identify: Find all 3x3 Subgrids within the Input_Grid.
  - Filter: Select only those 3x3 Subgrids where none of the four corner_pixels have the background color (orange, 7).
  - Transform: For each selected 3x3 Subgrid, rotate its pixels 90 degrees counter-clockwise.
  - Compose: Construct the Output_Grid by applying the rotations to the selected Subgrids in their original locations and copying all other pixels directly from the Input_Grid.

Constants:
  - Background Color: orange (7)
  - Subgrid Size: 3x3
  - Rotation Angle: 90 degrees counter-clockwise
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through all possible top-left corner positions (row `r`, column `c`) for a 3x3 subgrid within the input grid (i.e., `r` from 0 to height-3, `c` from 0 to width-3).
3.  For each potential 3x3 subgrid:
    a.  Examine its four corner pixels: at input grid coordinates (`r`, `c`), (`r`, `c+2`), (`r+2`, `c`), and (`r+2`, `c+2`).
    b.  Check if *none* of these four corner pixels have the background color (orange, 7).
    c.  If the condition in step 3b is met (all four corners are non-orange):
        i.  Extract the 3x3 block of pixels from the input grid starting at (`r`, `c`).
        ii. Perform a 90-degree counter-clockwise rotation on this extracted 3x3 block.
        iii. Place the rotated 3x3 block into the output grid, starting at the same top-left corner position (`r`, `c`), overwriting the initially copied values.
4.  Return the modified output grid.
```python
"""
Identify all 3x3 subgrids within the input grid whose four corner cells (top-left, top-right, bottom-left, bottom-right) are not the background color orange (7). Rotate each of these identified 3x3 subgrids 90 degrees counter-clockwise in place. Pixels outside these rotated blocks remain unchanged.
"""

import numpy as np

def rotate_subgrid_counter_clockwise(subgrid):
  """
  Rotates a 3x3 numpy array 90 degrees counter-clockwise.
  """
  # np.rot90 rotates counter-clockwise by default
  return np.rot90(subgrid, k=1)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    height, width = input_np.shape
    background_color = 7
    subgrid_size = 3

    # Iterate through all possible top-left corners (r, c) for a 3x3 subgrid
    # The range ensures that the 3x3 subgrid fits entirely within the grid boundaries
    for r in range(height - subgrid_size + 1):
        for c in range(width - subgrid_size + 1):
            
            # Define the coordinates of the four corners of the current 3x3 subgrid
            top_left = (r, c)
            top_right = (r, c + subgrid_size - 1)
            bottom_left = (r + subgrid_size - 1, c)
            bottom_right = (r + subgrid_size - 1, c + subgrid_size - 1)

            # Check if none of the four corner pixels have the background color (7)
            if (input_np[top_left] != background_color and
                input_np[top_right] != background_color and
                input_np[bottom_left] != background_color and
                input_np[bottom_right] != background_color):

                # Extract the 3x3 subgrid from the input grid
                subgrid_to_rotate = input_np[r:r + subgrid_size, c:c + subgrid_size]
                
                # Perform a 90-degree counter-clockwise rotation
                rotated_subgrid = rotate_subgrid_counter_clockwise(subgrid_to_rotate)
                
                # Place the rotated 3x3 block into the output grid at the same position
                output_grid[r:r + subgrid_size, c:c + subgrid_size] = rotated_subgrid

    # Return the modified output grid
    return output_grid.tolist() # Return as list of lists if required by caller context

```
