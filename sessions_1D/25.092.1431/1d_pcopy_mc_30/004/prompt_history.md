
## train_1

**input:**
```
0 0 5 5 5 0 0 0 2 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 0 2 2 2 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 7 7 7 0 0 0 9 0 0 0 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 0 9 9 9 0 8 8 8 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 6 6 6 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples for this task.

**Perception of Elements:**

1.  **Grid Size:** The input and output data are presented as 1D arrays of length 32. Observing the patterns, particularly the horizontal lines of length 3, suggests a 2D grid structure. A 4x8 grid (4 rows, 8 columns) fits the data and reveals the underlying patterns clearly.
2.  **Colors:** The grids use white (0) as the background and various other colors (Gray-5, Red-2, Orange-7, Maroon-9, Azure-8, Blue-1, Magenta-6) for foreground objects.
3.  **Objects:** There appear to be two types of significant objects in the input grids:
    *   Single, isolated pixels of a non-white color. A pixel is isolated if all its 8 neighbors (horizontal, vertical, and diagonal) are white (0).
    *   Horizontal lines of exactly 3 pixels, all having the same non-white color.
4.  **Transformation:** The core transformation seems to operate differently on these two types of objects:
    *   Existing horizontal lines of length 3 are preserved; they appear unchanged in the output grid at the same location.
    *   Single, isolated pixels are expanded into a horizontal line of length 3, using the original pixel's color. The original pixel becomes the center of the new line (if possible).
5.  **Wrapping Behavior:** The expansion of single pixels exhibits edge wrapping:
    *   If a single pixel is in the leftmost column (column 0), the leftmost pixel of its expanded line wraps to the last column (column 7) of the row *above*. The row index also wraps (row 0 wraps to row 3).
    *   If a single pixel is in the rightmost column (column 7), the rightmost pixel of its expanded line wraps to the first column (column 0) of the row *below*. The row index also wraps (row 3 wraps to row 0).
    *   For pixels not on the left or right edges, the expansion is simply `(r, c-1), (r, c), (r, c+1)`.
6.  **Output Construction:** The output grid seems to be constructed by taking the input grid, identifying the single pixels, and then drawing the corresponding expanded 3-pixel lines onto the grid, overwriting the original single pixel and potentially adjacent white pixels. The unchanged 3-pixel lines from the input are effectively carried over.

**Facts (YAML):**


```python
import numpy as np
from typing import List

"""
Transforms a 4x8 grid represented as a 1D list of 32 integers.

The transformation rule operates as follows:
1. Reshape the input 1D list into a 4x8 2D grid.
2. Create an output grid initialized as a copy of the input grid.
3. Iterate through each cell (pixel) of the input grid.
4. Identify "isolated" non-white pixels. An isolated pixel is a non-white pixel (value > 0) where all 8 of its neighbors (horizontally, vertically, and diagonally adjacent, with wrap-around for edges) are white (value 0).
5. For each isolated pixel found at position (r, c) with color 'C':
    a. Determine the coordinates for a 3-pixel horizontal line centered at (r, c), considering wrap-around for columns:
        - Center: (r, c)
        - Left: (r, (c - 1 + 8) % 8)
        - Right: (r, (c + 1 + 8) % 8)
    b. Apply special row wrap-around rules for pixels on the left or right edges:
        - If the isolated pixel is in the leftmost column (c == 0), the row index for the "left" pixel (which wraps to column 7) becomes (r - 1 + 4) % 4.
        - If the isolated pixel is in the rightmost column (c == 7), the row index for the "right" pixel (which wraps to column 0) becomes (r + 1 + 4) % 4.
    c. Set the pixels at the calculated left, center, and right coordinates in the output grid to the color 'C' of the original isolated pixel.
6. Pixels that were already part of a 3-pixel horizontal line in the input grid remain unchanged in the output grid because they are not "isolated" and the output grid starts as a copy.
7. Flatten the final 4x8 output grid back into a 1D list of 32 integers.
"""

def get_neighbors(grid, r, c):
    """Gets the values of the 8 neighbors of a cell (r, c) with wrap-around."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr = (r + dr + rows) % rows
            nc = (c + dc + cols) % cols
            neighbors.append(grid[nr, nc])
    return neighbors

def is_isolated(grid, r, c):
    """Checks if a non-white pixel at (r, c) is isolated."""
    if grid[r, c] == 0: # White pixels cannot be isolated points of interest
        return False
    neighbors = get_neighbors(grid, r, c)
    # Check if all neighbors are white (0)
    return all(neighbor == 0 for neighbor in neighbors)

def transform(input_grid_flat: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    Expands isolated single pixels into 3-pixel horizontal lines with wrapping.
    Preserves existing 3-pixel horizontal lines.
    """
    if len(input_grid_flat) != 32:
        raise ValueError("Input grid must have exactly 32 elements for a 4x8 grid.")

    # Reshape input list into a 4x8 numpy array
    input_grid = np.array(input_grid_flat).reshape(4, 8)
    rows, cols = input_grid.shape

    # Initialize output grid as a copy of the input
    output_grid = input_grid.copy()

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is an isolated non-white pixel
            if is_isolated(input_grid, r, c):
                color = input_grid[r, c]

                # Calculate coordinates for the 3-pixel line
                center_r, center_c = r, c
                left_r, left_c = r, (c - 1 + cols) % cols
                right_r, right_c = r, (c + 1 + cols) % cols

                # Apply special row wrapping for edge columns
                if c == 0: # Left edge column
                    left_r = (r - 1 + rows) % rows
                if c == cols - 1: # Right edge column (using cols-1 for generality)
                    right_r = (r + 1 + rows) % rows

                # Update the output grid with the expanded line
                output_grid[left_r, left_c] = color
                output_grid[center_r, center_c] = color # This pixel is already set, but good for clarity
                output_grid[right_r, right_c] = color

    # Flatten the output grid back to a 1D list
    return output_grid.flatten().tolist()

```
```python
import numpy as np
from typing import List

"""
Transforms a 4x8 grid represented as a 1D list of 32 integers.

The transformation rule operates as follows:
1. Reshape the input 1D list into a 4x8 2D grid.
2. Create an output grid initialized as a copy of the input grid.
3. Iterate through each cell (pixel) of the input grid.
4. Identify "source" pixels: A non-white pixel is a source if its horizontal neighbors (left and right, with column wrap-around) have different colors than the pixel itself.
5. For each source pixel found at position (r, c) with color 'C':
    a. Determine the target coordinates for a 3-pixel horizontal line centered conceptually at (r, c):
        - Center: (r, c)
        - Left column: (c - 1 + 8) % 8
        - Right column: (c + 1 + 8) % 8
    b. Apply special row wrap-around rules for the left/right pixels if the source pixel is on a column edge:
        - If the source pixel is in the leftmost column (c == 0), the row index for the "left" target pixel (which wraps to the last column) becomes (r - 1 + 4) % 4. Otherwise, it's 'r'.
        - If the source pixel is in the rightmost column (c == 7), the row index for the "right" target pixel (which wraps to the first column) becomes (r + 1 + 4) % 4. Otherwise, it's 'r'.
    c. Set the pixels at the calculated left, center, and right target coordinates in the *output* grid to the color 'C' of the source pixel.
6. Pixels that were part of an existing 3-pixel horizontal line in the input grid (and therefore not "source" pixels) remain unchanged in the output grid because the output grid starts as a copy and these pixels are not overwritten.
7. Flatten the final 4x8 output grid back into a 1D list of 32 integers.
"""

def is_source_pixel(grid: np.ndarray, r: int, c: int) -> bool:
    """
    Checks if a pixel at (r, c) is a source for expansion.
    A pixel is a source if it's non-white and its horizontal neighbors
    (with column wrap-around) are not the same color as the pixel.
    """
    rows, cols = grid.shape
    color = grid[r, c]

    # Must be non-white
    if color == 0:
        return False

    # Check horizontal neighbors
    left_c = (c - 1 + cols) % cols
    right_c = (c + 1 + cols) % cols
    left_neighbor_color = grid[r, left_c]
    right_neighbor_color = grid[r, right_c]

    return left_neighbor_color != color and right_neighbor_color != color

def calculate_target_coords(r: int, c: int, rows: int, cols: int) -> tuple:
    """
    Calculates the target coordinates (left, center, right) for expansion,
    applying row and column wrap-around rules.
    Returns: ((left_r, left_c), (center_r, center_c), (right_r, right_c))
    """
    # Calculate column indices with wrap-around
    left_c_target = (c - 1 + cols) % cols
    center_c_target = c
    right_c_target = (c + 1 + cols) % cols

    # Calculate row indices, initially same as source row
    left_r_target = r
    center_r_target = r
    right_r_target = r

    # Apply row wrap adjustment for edge columns
    if c == 0: # Source is in the first column
        left_r_target = (r - 1 + rows) % rows
    if c == cols - 1: # Source is in the last column
        right_r_target = (r + 1 + rows) % rows

    return ((left_r_target, left_c_target),
            (center_r_target, center_c_target),
            (right_r_target, right_c_target))


def transform(input_grid_flat: List[int]) -> List[int]:
    """
    Applies the expansion transformation to the input grid list.
    """
    # Assume 4x8 grid dimensions based on analysis
    rows, cols = 4, 8
    expected_length = rows * cols
    if len(input_grid_flat) != expected_length:
        raise ValueError(f"Input grid list must have exactly {expected_length} elements for a {rows}x{cols} grid.")

    # Reshape input list into a 2D numpy array
    input_grid = np.array(input_grid_flat).reshape(rows, cols)

    # Initialize output grid as a copy of the input
    output_grid = input_grid.copy()

    # Iterate through each cell of the input grid to find source pixels
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is a source for expansion
            if is_source_pixel(input_grid, r, c):
                color = input_grid[r, c]

                # Calculate the target coordinates for the 3-pixel line
                (left_coord, center_coord, right_coord) = calculate_target_coords(r, c, rows, cols)

                # Update the output grid with the expanded line
                output_grid[left_coord] = color
                output_grid[center_coord] = color # Overwrites original source pixel
                output_grid[right_coord] = color

    # Flatten the output grid back to a 1D list
    return output_grid.flatten().tolist()
```
