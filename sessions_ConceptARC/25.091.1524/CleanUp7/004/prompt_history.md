
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0
0 3 0 0 3 3 3 0 0
0 3 0 0 8 8 8 0 0
0 0 0 0 8 8 8 0 0
0 0 0 0 8 8 8 3 3
0 0 0 0 0 0 0 3 0
0 3 3 3 0 0 0 3 0
0 0 3 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0
0 3 0 0 3 3 3 0 0
0 3 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 3 0
0 3 3 3 0 0 0 3 0
0 0 3 0 0 0 0 0 0
```


## train_2

**input:**
```
4 0 4 0 0 0 0 0 0
4 4 4 0 4 0 4 0 0
4 0 4 0 4 4 4 0 0
0 0 0 0 8 8 8 8 8
0 0 0 0 8 8 8 8 8
4 0 4 0 8 8 8 8 8
4 4 4 0 0 0 4 4 4
4 0 4 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0
```


**output:**
```
4 0 4 0 0 0 0 0 0
4 4 4 0 4 0 4 0 0
4 0 4 0 4 4 4 0 0
0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 4 0 4
4 4 4 0 0 0 4 4 4
4 0 4 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 6 0 0 0 0 0 6 0
6 6 6 0 0 0 6 6 6
0 6 0 0 6 0 8 8 8
0 0 0 6 6 6 8 8 8
0 0 0 0 6 0 8 8 8
0 0 0 0 0 6 8 8 8
0 0 6 0 6 6 8 8 8
0 6 6 6 0 6 8 8 8
0 0 6 0 0 0 0 0 0
```


**output:**
```
0 6 0 0 0 0 0 6 0
6 6 6 0 0 0 6 6 6
0 6 0 0 6 0 0 6 0
0 0 0 6 6 6 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 6 0 6 6 6 0 0
0 6 6 6 0 6 0 0 0
0 0 6 0 0 0 0 0 0
```

## Perception

1.  **Grid Structure:** The input and output are both 2D grids of pixels with different colors. The size of the grid remains constant between input and output.
2.  **Color Palette:** The colors involved are white (0), green (3), yellow (4), magenta (6), and azure (8). White seems to be the background color.
3.  **Key Color:** The color azure (8) appears in all input examples but is completely absent in the corresponding output examples.
4.  **Affected Colors:** In each example, pixels of *another* color (green in ex 1, yellow in ex 2, magenta in ex 3) that are adjacent (including diagonals) to the azure pixels in the input are also removed (changed to white) in the output.
5.  **Unaffected Pixels:** Pixels that are not azure (8) and are not adjacent to any azure pixel retain their original color in the output. White (0) pixels also seem unaffected unless they replace a removed pixel.
6.  **Transformation:** The core transformation involves identifying all azure (8) pixels and all non-white pixels adjacent to them, and then replacing all these identified pixels with white (0).

## Facts


```yaml
task_description: "Identify and remove azure (8) pixels and any non-white pixels adjacent (including diagonals) to them, replacing them with white (0)."
grid_properties:
  - size_preservation: True # Grid dimensions do not change.
  - background_color: 0 # White is the default/background color.
objects:
  - type: primary_target
    color: 8 # azure
    description: "The main object/color to be removed."
  - type: secondary_target
    color: non-zero # Any color other than white (0) and azure (8).
    description: "Pixels of these colors are potentially affected if adjacent to the primary target."
relationships:
  - type: adjacency
    scope: 8-connectivity # Includes horizontal, vertical, and diagonal neighbors.
    condition: "A secondary target pixel is adjacent to a primary target pixel."
actions:
  - name: identify_primary
    target: pixels with color 8
    result: set of coordinates for all azure pixels.
  - name: identify_adjacent_secondary
    target: pixels with non-zero, non-8 color
    condition: adjacent (8-connectivity) to any pixel identified in 'identify_primary'
    result: set of coordinates for adjacent non-white, non-azure pixels.
  - name: remove_pixels
    target_coordinates: union of coordinates from 'identify_primary' and 'identify_adjacent_secondary'
    action: change pixel color to 0 (white).
  - name: preserve_pixels
    target_coordinates: all coordinates not in 'remove_pixels' target set.
    action: keep original pixel color.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Create two sets to store the coordinates of pixels to be changed to white: `azure_coords` and `adjacent_coords`.
3.  Iterate through each pixel (cell) of the input grid using its row and column index.
4.  If a pixel's color is azure (8), add its coordinates (row, col) to the `azure_coords` set.
5.  After identifying all azure pixels, iterate through each pixel of the input grid again.
6.  For each pixel that is *not* white (0) and *not* azure (8):
    a.  Check its 8 neighbors (horizontal, vertical, and diagonal).
    b.  If any neighbor's coordinates are present in the `azure_coords` set, add the current pixel's coordinates (row, col) to the `adjacent_coords` set.
7.  Combine the coordinates from `azure_coords` and `adjacent_coords` into a single set of `pixels_to_remove`.
8.  Iterate through all coordinates in the `pixels_to_remove` set. For each coordinate (row, col), set the color of the corresponding pixel in the output grid to white (0).
9.  Return the modified output grid.
```python
"""
Identify and remove azure (8) pixels and any non-white pixels adjacent (including diagonals) to them, replacing them with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing azure pixels (8) and any non-white, 
    non-azure pixels adjacent (8-connectivity) to them, replacing them with white (0).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to NumPy array for easier handling
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Set to store coordinates of azure pixels
    azure_coords = set()
    # Set to store coordinates of non-white, non-azure pixels adjacent to azure pixels
    adjacent_coords = set()

    # --- Step 1: Identify all azure pixels ---
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 8:
                azure_coords.add((r, c))

    # --- Step 2: Identify non-white, non-azure pixels adjacent to azure pixels ---
    # Define 8-connectivity neighbors (including diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]
            # Check if the pixel is non-white (0) and non-azure (8)
            if pixel_color != 0 and pixel_color != 8:
                is_adjacent_to_azure = False
                # Check all 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is an azure pixel
                        if (nr, nc) in azure_coords:
                            is_adjacent_to_azure = True
                            break # Found an azure neighbor, no need to check others
                
                # If adjacent to an azure pixel, mark this pixel for removal
                if is_adjacent_to_azure:
                    adjacent_coords.add((r, c))

    # --- Step 3: Combine coordinates and modify the output grid ---
    pixels_to_remove = azure_coords.union(adjacent_coords)

    for r, c in pixels_to_remove:
        output_grid[r, c] = 0 # Set to white

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
```python
"""
Replace all azure (8) pixels with white (0) pixels. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all azure (8) pixels with white (0).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to modify and return as the output
    output_grid = np.copy(grid)
    
    # Find the coordinates (rows and columns) of all pixels with the color azure (8)
    azure_coords = np.where(grid == 8)
    
    # Replace the pixels at the identified coordinates with white (0) in the output grid
    output_grid[azure_coords] = 0
    
    # Convert the modified NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()

```
