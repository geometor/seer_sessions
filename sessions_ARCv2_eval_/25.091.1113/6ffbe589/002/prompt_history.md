
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 3 3 8 8 0 8 8 8 0 8 0 3 0 0
0 0 0 0 0 0 0 3 8 0 8 8 0 8 8 8 8 3 0 0
0 0 0 0 0 0 0 3 0 8 0 0 6 0 0 8 0 3 0 0
0 0 0 0 0 0 0 3 8 8 6 6 6 6 0 8 8 3 3 0
0 0 0 0 0 0 0 3 8 0 0 6 0 6 0 0 8 3 0 0
0 0 0 0 0 0 0 3 8 8 0 6 6 6 6 8 8 3 3 0
0 0 0 0 0 0 0 3 0 8 0 0 6 0 0 8 0 3 0 0
0 0 0 0 0 0 3 3 8 8 8 8 0 8 8 8 8 3 0 0
0 0 0 0 0 0 0 3 0 8 0 8 8 8 0 8 0 3 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0 3 0 0
0 3 3 3 3 3 3 3 3 3 3 3 0
0 3 0 8 0 8 8 8 0 8 0 3 3
0 3 8 8 8 8 0 8 8 8 8 3 0
0 3 0 8 0 0 6 0 0 8 0 3 3
3 3 8 8 6 6 6 6 0 8 8 3 0
3 3 8 0 0 6 0 6 0 0 8 3 0
0 3 8 8 0 6 6 6 6 8 8 3 0
0 3 0 8 0 0 6 0 0 8 0 3 0
0 3 8 8 8 8 0 8 8 0 8 3 0
0 3 0 8 0 8 8 8 0 8 8 3 0
0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 3 0 3 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 0 5 5 5 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 3 3 3 3 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3 3 0 4 0 0 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 3 0 4 4 0 3 3 0 0 0 0 0
0 0 0 0 0 0 5 0 3 0 4 4 4 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 3 0 0 0 0 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 0 3 3 3 3 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 5 0 5 5 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 5 0 5 5 5 5 0 5
0 0 0 0 0 0 3 0 0 0
5 0 0 3 3 3 3 0 0 5
0 0 3 0 0 0 0 3 3 5
5 3 3 0 4 4 4 3 0 0
5 0 3 0 4 4 0 3 0 5
5 0 3 0 4 0 0 3 0 5
5 0 0 3 3 3 3 0 0 5
0 0 0 0 0 3 0 0 0 0
5 0 5 5 0 5 5 5 0 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 1 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 1 0 0 1 1 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 1 2 2 0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 4 1 0 2 2 1 0 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 1 1 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 1 1 0 0 0 4 0 0 0 0 0 0 0 0 0
0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0
0 4 0 1 1 0 0 0 0 4
4 0 0 1 0 1 0 0 4 0
0 4 1 0 2 2 0 1 0 4
4 0 0 0 2 2 1 1 4 0
0 4 0 1 1 0 1 0 0 4
4 0 0 0 0 1 0 0 4 0
0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0
```

Okay, let's break down the task based on the provided examples.

## Perception

1.  **Input Grid Structure:** The input grids are relatively large (20x20) and mostly composed of the background color, white (0).
2.  **Objects:** Within the white background, there are distinct shapes or patterns formed by non-white pixels (colors 1 through 9). These appear to be the primary focus.
3.  **Multiple Objects:** In some inputs, there might be several disconnected groups of non-white pixels. For example, in `train_1`, besides the main central pattern, there are isolated azure pixels and a green/magenta pair near the bottom.
4.  **Output Grid Structure:** The output grids are smaller than the input grids and contain only one main object, seemingly extracted from the input. The output grid's size corresponds exactly to the dimensions of this extracted object.
5.  **Transformation:** The core transformation appears to be identifying the "most significant" object in the input grid and cropping the grid to the minimal bounding box containing just that object.
6.  **Significance Criteria:** Comparing the central objects with the smaller, isolated groups of pixels, the central objects are significantly larger in terms of the number of pixels they contain. This suggests the "most significant" object is the one with the largest area (pixel count).
7.  **Connectivity:** The pixels forming the main object are connected, often including diagonal connections (8-way connectivity).
8.  **Color Preservation:** The colors of the pixels within the extracted object remain unchanged in the output.

## Facts


```yaml
task_type: extraction, cropping, object_identification

components:
  - role: input_grid
    type: 2D array of integers (colors)
    properties:
      - contains a background color (white, 0)
      - contains one or more objects made of non-white pixels
  - role: output_grid
    type: 2D array of integers (colors)
    properties:
      - smaller dimensions than the input_grid
      - contains a single object extracted from the input_grid
      - dimensions match the bounding box of the extracted object

objects:
  - type: pixel_group
    definition: A contiguous group of non-white pixels.
    connectivity: 8-way (von Neumann + diagonal neighbors)
    properties:
      - color: composed of various non-white colors (1-9)
      - size: number of pixels in the group
      - location: defined by pixel coordinates
      - bounding_box: minimum rectangle enclosing all pixels of the group

relationships:
  - type: spatial
    description: Objects are located within the input grid, potentially separated by white pixels.
  - type: size_comparison
    description: Objects can be compared based on their size (pixel count).

actions:
  - name: identify_objects
    description: Find all distinct connected components of non-white pixels in the input grid.
    inputs: input_grid
    outputs: list of objects (pixel_groups)
  - name: find_largest_object
    description: Determine which identified object has the maximum number of pixels.
    inputs: list of objects
    outputs: the single largest object
    assumption: There is a unique largest object in the examples provided.
  - name: calculate_bounding_box
    description: Find the minimum and maximum row and column indices for the pixels belonging to the largest object.
    inputs: largest_object
    outputs: bounding_box (min_row, max_row, min_col, max_col)
  - name: crop_grid
    description: Extract the subgrid defined by the bounding box from the input grid.
    inputs: input_grid, bounding_box
    outputs: output_grid

goal: Extract the largest connected component of non-white pixels from the input grid and return it within its minimal bounding box.
```


## Natural Language Program

1.  Identify all groups of connected non-white pixels in the input grid. Consider pixels connected if they touch horizontally, vertically, or diagonally (8-way connectivity).
2.  For each identified group (object), count the number of pixels it contains.
3.  Select the object that has the largest pixel count.
4.  Determine the minimum row index, maximum row index, minimum column index, and maximum column index occupied by the pixels of this largest object. These four values define the bounding box.
5.  Create a new output grid with height equal to `(max_row - min_row + 1)` and width equal to `(max_col - min_col + 1)`.
6.  Copy the pixels from the input grid located within the calculated bounding box (from `min_row` to `max_row` and `min_col` to `max_col`) into the new output grid, preserving their relative positions.
```python
import numpy as np
from collections import deque

"""
Identify all groups of connected non-white pixels (8-way connectivity).
Find the group with the largest number of pixels.
Determine the bounding box of this largest group.
Crop the input grid to this bounding box and return the result.
"""

def _find_connected_objects(grid):
    """
    Finds all connected components of non-background pixels using BFS.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is a list of (row, col) tuples
              representing the coordinates of pixels in a connected object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            # If it's a non-background pixel and not yet visited
            if grid[r, c] != background_color and not visited[r, c]:
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col))

                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            # Skip the center pixel itself
                            if dr == 0 and dc == 0:
                                continue

                            nr, nc = row + dr, col + dc

                            # Check bounds
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if neighbor is non-background and not visited
                                if grid[nr, nc] != background_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))

                if current_object_pixels:
                    objects.append(current_object_pixels)

    return objects

def _calculate_bounding_box(pixels):
    """
    Calculates the minimum bounding box for a list of pixel coordinates.

    Args:
        pixels (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if no pixels.
    """
    if not pixels:
        return None

    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]

    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)

    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Identifies the largest connected object of non-background pixels
    and crops the grid to its bounding box.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the cropped output grid.
                 Returns an empty array if no non-background objects are found.
    """
    # Convert input list of lists to numpy array if necessary
    grid = np.array(input_grid)

    # 1. Identify all connected non-background objects
    objects = _find_connected_objects(grid)

    # Handle case where there are no objects
    if not objects:
        return np.array([[]], dtype=int) # Or handle as appropriate, maybe empty grid of correct shape?

    # 2. Find the object with the largest pixel count
    largest_object = max(objects, key=len)

    # 3. Determine the bounding box of the largest object
    bounding_box = _calculate_bounding_box(largest_object)
    if bounding_box is None:
         return np.array([[]], dtype=int) # Should not happen if objects is not empty

    min_row, max_row, min_col, max_col = bounding_box

    # 4. Create the output grid by cropping the input grid
    # Note: Slicing in numpy is exclusive of the end index, so add 1
    output_grid = grid[min_row : max_row + 1, min_col : max_col + 1]

    return output_grid.tolist() # Convert back to list of lists if required by framework
```
