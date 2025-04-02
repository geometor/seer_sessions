
## train_1

**input:**
```
0 4 0 0 2 3
4 1 1 2 1 0
0 1 0 0 2 3
0 2 0 0 1 0
0 2 1 1 1 0
0 2 0 0 4 0
```


**output:**
```
0 0 0 0 0 0
0 1 1 1 1 0
0 1 0 0 1 0
0 1 0 0 1 0
0 1 1 1 1 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 6 5 6
0 5 0 0 0 6
0 3 0 0 0 5
0 3 0 3 0 5
0 5 5 5 5 5
6 6 0 5 0 3
```


**output:**
```
0 5 5 5 5 5
0 5 0 0 0 5
0 5 0 0 0 5
0 5 0 0 0 5
0 5 5 5 5 5
0 0 0 0 0 0
```

*   **Perception:** The task involves identifying a dominant color pattern within the input grid and using its spatial extent to create a solid rectangular shape in the output grid. The background color is preserved, while all other non-dominant colors are removed. Isolated single pixels of the dominant color are ignored when determining the bounds of the final rectangle.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        role: input
        attributes:
          - colors: multiple distinct colors present, including a background color (white/0).
          - patterns: scattered pixels of various colors.
      - object: grid
        role: output
        attributes:
          - colors: primarily the background color and one other 'target' color.
          - patterns: a single solid rectangle filled with the 'target' color against the background.
    transformations:
      - action: identify_background_color
        input: input grid
        output: most frequent color in the input grid
        description: Counts the occurrences of each color and selects the most frequent one as the background.
      - action: identify_target_color
        input: input grid, background_color
        output: most frequent non-background color
        description: Counts the occurrences of each non-background color and selects the most frequent one as the target color.
      - action: find_target_pixels
        input: input grid, target_color
        output: list of coordinates for target color pixels
      - action: find_connected_components
        input: list of target pixel coordinates
        output: list of components (each component is a list of coordinates)
        attributes:
          - connectivity: 8-way adjacency (horizontal, vertical, diagonal)
      - action: filter_components
        input: list of components
        output: list of components with size > 1
        description: Removes components that contain only a single pixel.
      - action: calculate_bounding_box
        input: list of filtered components
        output: coordinates of the bounding box (min_row, max_row, min_col, max_col)
        description: Finds the minimum bounding rectangle that encloses all pixels in the filtered components. If no components remain, this step might be skipped or return null.
      - action: create_output_grid
        input: input grid dimensions, background_color, target_color, bounding_box
        output: output grid
        description: Creates a new grid of the same size as the input, filled with the background color. If a bounding box exists, fills the area defined by the bounding box with the target color.
    relationships:
      - The target color in the output is determined by the most frequent non-background color in the input.
      - The position and size of the rectangle in the output are determined by the spatial extent (bounding box) of the significant connected components (size > 1) of the target color pixels in the input.
      - All other colors from the input (except the background and target colors) are replaced by the background color.
      - Single, isolated pixels of the target color in the input do not contribute to defining the bounding box for the output rectangle.
    ```


*   **Natural Language Program:**
    1.  Determine the background color by finding the most frequent color in the input grid.
    2.  Identify the 'target' color by finding the most frequent color *excluding* the background color.
    3.  Locate all pixels in the input grid that match the target color.
    4.  Group these target pixels into connected components using 8-way adjacency (pixels are connected if they touch horizontally, vertically, or diagonally).
    5.  Discard any components that consist of only a single pixel.
    6.  If no components remain after discarding single-pixel ones, create an output grid of the same dimensions as the input, filled entirely with the background color.
    7.  If components remain, calculate the overall bounding box (minimum row, maximum row, minimum column, maximum column) that encloses all pixels belonging to these remaining components.
    8.  Create an output grid of the same dimensions as the input, initially filled with the background color.
    9.  Fill the rectangular area defined by the calculated bounding box (from minimum row to maximum row, and minimum column to maximum column, inclusive) with the target color.
```python
import numpy as np
from collections import Counter
from scipy.ndimage import label, find_objects

"""
1. Determine the background color by finding the most frequent color in the input grid.
2. Identify the 'target' color by finding the most frequent color *excluding* the background color.
3. Locate all pixels in the input grid that match the target color.
4. Group these target pixels into connected components using 8-way adjacency.
5. Discard any components that consist of only a single pixel.
6. If no components remain after discarding single-pixel ones, create an output grid of the same dimensions as the input, filled entirely with the background color.
7. If components remain, calculate the overall bounding box that encloses all pixels belonging to these remaining components.
8. Create an output grid of the same dimensions as the input, initially filled with the background color.
9. Fill the rectangular area defined by the calculated bounding box with the target color.
"""

def find_most_frequent_color(grid_flat):
    """Finds the most frequent color in a flattened grid."""
    if not grid_flat:
        return 0 # Default to white if grid is empty
    counts = Counter(grid_flat)
    most_common = counts.most_common(1)
    return most_common[0][0] if most_common else 0

def find_target_color(grid_flat, background_color):
    """Finds the most frequent non-background color."""
    non_background_colors = [c for c in grid_flat if c != background_color]
    if not non_background_colors:
        return None # No target color found
    counts = Counter(non_background_colors)
    most_common = counts.most_common(1)
    return most_common[0][0] if most_common else None


def transform(input_grid):
    """
    Transforms the input grid based on finding the largest connected component
    (excluding single pixels) of the most frequent non-background color and drawing
    its bounding box.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    grid_flat = input_array.flatten().tolist()

    # 1. Determine the background color
    background_color = find_most_frequent_color(grid_flat)

    # 2. Identify the 'target' color
    target_color = find_target_color(grid_flat, background_color)

    # Initialize output grid with background color
    output_array = np.full((rows, cols), background_color, dtype=int)

    # If no target color exists, return the background grid
    if target_color is None:
        return output_array.tolist()

    # 3. Locate all pixels matching the target color
    target_mask = (input_array == target_color)

    # 4. Group target pixels into connected components (8-way adjacency)
    # Structure for 8-way connectivity
    structure = np.ones((3, 3), dtype=bool)
    labeled_array, num_features = label(target_mask, structure=structure)

    # 5. Discard single-pixel components and find coordinates of remaining pixels
    valid_target_pixels_coords = []
    for i in range(1, num_features + 1):
        component_coords = np.argwhere(labeled_array == i)
        if len(component_coords) > 1: # Filter components with size > 1
            valid_target_pixels_coords.extend(component_coords)

    # 6. If no components remain, return the background grid
    if not valid_target_pixels_coords:
        return output_array.tolist()

    # 7. Calculate the overall bounding box for the valid pixels
    valid_target_pixels_coords = np.array(valid_target_pixels_coords)
    min_row = np.min(valid_target_pixels_coords[:, 0])
    max_row = np.max(valid_target_pixels_coords[:, 0])
    min_col = np.min(valid_target_pixels_coords[:, 1])
    max_col = np.max(valid_target_pixels_coords[:, 1])

    # 8. Create the output grid (already initialized)

    # 9. Fill the bounding box area with the target color
    output_array[min_row:max_row+1, min_col:max_col+1] = target_color

    return output_array.tolist()

```
