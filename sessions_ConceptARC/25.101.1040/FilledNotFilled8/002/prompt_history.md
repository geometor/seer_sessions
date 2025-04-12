
## train_1

**input:**
```
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 6 6 6 6 6 6 6 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception**

1.  **Input/Output Grids:** Both input and output are 2D grids of pixels, primarily white (0) with a single contiguous shape made of another color (magenta/6 in train_1, green/3 in train_2).
2.  **Object Identification:** In each example, there's one main non-white object. The background is white.
3.  **Transformation in train_1:** The input shows a sparse collection of magenta pixels that seem to outline a region. The output fills this region with magenta pixels, effectively creating a solid shape bounded by the original pixels (and potentially extending slightly). The original magenta pixels remain.
4.  **Transformation in train_2:** The input shows a solid green shape. The output removes the interior of this shape, leaving only the pixels that were on the boundary (adjacent to white pixels in the input).
5.  **Core Logic:** The two examples demonstrate inverse operations. One goes from an outline-like structure to a filled shape, the other goes from a filled shape to an outline. The key seems to be determining whether the input shape is "hollow" (like an outline) or "solid" (filled) and then applying the corresponding transformation (fill or outline).
6.  **Determining Solid/Hollow:** A shape can be considered "solid" if it contains at least one pixel whose neighbours (including diagonals) are *all* the same color as the pixel itself. If all pixels of the shape have at least one neighbour that is white (background), the shape can be considered "hollow" or an outline.
7.  **Fill Mechanism (train_1):** The fill seems to happen for white pixels that lie "between" pixels of the shape's color, both horizontally and vertically. A white pixel is filled if there's a shape pixel to its left and right on the same row, OR if there's a shape pixel above and below it in the same column.
8.  **Outline Mechanism (train_2):** The outline keeps only those shape pixels from the input that were adjacent (including diagonals) to a white background pixel. Interior pixels are removed (turned white).

**Facts**


```yaml
Task: Toggle between filled shape and outline shape representation.

Input_Characteristics:
  - Grid contains a white background (0).
  - Grid contains a single contiguous object of a non-white color (C).

Object_Properties:
  - Color: The specific non-white color (C) of the object (e.g., magenta/6, green/3).
  - Solidity: Determined by the presence or absence of "interior" pixels.
    - Interior_Pixel: A pixel of color C where all 8 neighbours are also color C.
    - Solid_Object: Contains at least one Interior_Pixel.
    - Hollow_Object: Contains no Interior_Pixels (all object pixels are adjacent to the background).

Transformation_Rule:
  - Condition: Check if the input object is Solid or Hollow.
  - Action_If_Solid:
    - Goal: Produce the outline of the object.
    - Method: Keep only object pixels (C) that are adjacent (8 directions) to at least one background pixel (0) in the input. Change all other pixels (including interior object pixels) to background (0).
  - Action_If_Hollow:
    - Goal: Produce a filled version of the shape defined by the hollow object.
    - Method:
      - Start with a copy of the input grid.
      - Identify all background pixels (0).
      - For each background pixel (r, c):
        - Check_Horizontal: Are there pixels of color C at (r, c1) and (r, c2) where c1 < c < c2?
        - Check_Vertical: Are there pixels of color C at (r1, c) and (r2, c) where r1 < r < r2?
        - If Check_Horizontal is TRUE OR Check_Vertical is TRUE, change the pixel at (r, c) to color C.

Output_Characteristics:
  - Grid contains a white background (0).
  - Grid contains a single contiguous object of color C.
  - If the input object was Solid, the output object is Hollow (an outline).
  - If the input object was Hollow, the output object is Solid (filled).
```


**Natural Language Program**

1.  Identify the primary non-white color (C) and the single contiguous object made of this color within the input grid. The rest of the grid is background (white, 0).
2.  Determine if the object is "solid" or "hollow":
    *   Scan the object's pixels. If any pixel of color C has all 8 of its neighbours also being color C, classify the object as "solid".
    *   If no such pixel exists (i.e., every pixel of color C is adjacent to at least one background pixel), classify the object as "hollow".
3.  If the object is "solid":
    *   Create a new grid of the same dimensions, filled with the background color (0).
    *   Iterate through each pixel `(r, c)` of the input grid.
    *   If the input pixel `(r, c)` has color C AND it is adjacent (horizontally, vertically, or diagonally) to at least one background pixel (0) in the input grid, set the corresponding pixel `(r, c)` in the new grid to color C.
    *   The new grid is the output.
4.  If the object is "hollow":
    *   Create a new grid by copying the input grid.
    *   Iterate through each pixel `(r, c)` of the input grid that has the background color (0).
    *   Check for horizontal containment: Search leftwards from `(r, c)` on the same row `r` until the edge or a pixel of color C is found. Search rightwards from `(r, c)` on the same row `r` until the edge or a pixel of color C is found. If color C was found in *both* directions, the horizontal condition is met.
    *   Check for vertical containment: Search upwards from `(r, c)` in the same column `c` until the edge or a pixel of color C is found. Search downwards from `(r, c)` in the same column `c` until the edge or a pixel of color C is found. If color C was found in *both* directions, the vertical condition is met.
    *   If the horizontal condition OR the vertical condition is met for the background pixel `(r, c)`, change the color of pixel `(r, c)` in the new grid to C.
    *   The modified new grid is the output.
```python
"""
Transformation rule:
1. Identify the primary non-white color (C) and the single contiguous object made of this color in the input grid.
2. Determine if the object is "solid" or "hollow".
    - An object is "solid" if at least one pixel of color C has all 8 of its neighbors also being color C.
    - Otherwise, the object is "hollow".
3. If the object is "solid", create an "outline" of the object.
    - The outline consists of only those pixels of color C from the input that were adjacent (8 directions) to at least one background pixel (0). All other pixels become background (0).
4. If the object is "hollow", create a "filled" version of the shape.
    - Start with the input grid.
    - Change any background pixel (0) to color C if it has pixels of color C both to its left and right on the same row, OR if it has pixels of color C both above and below it in the same column.
"""

import numpy as np
from typing import List, Tuple, Set

def _get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Get valid 8-directional neighbor coordinates."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def _find_object_pixels(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]]]:
    """Find the non-background color and the set of coordinates for the object."""
    object_color = -1
    object_pixels = set()
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                if object_color == -1:
                    object_color = grid[r, c]
                elif grid[r, c] != object_color:
                    # Assuming only one object color besides background
                    # This case shouldn't happen based on examples, but good practice
                    pass # Or raise an error
                
                if grid[r, c] == object_color:
                     object_pixels.add((r, c))

    if object_color == -1: # Handle case of all background
        object_color = 0 # Default to background if no object found

    return object_color, object_pixels

def _is_solid(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> bool:
    """Check if any object pixel has all 8 neighbors of the same object color."""
    height, width = grid.shape
    for r, c in object_pixels:
        neighbors = _get_neighbors(r, c, height, width)
        if len(neighbors) < 8: # Pixel on the edge cannot be fully surrounded
             continue
        
        all_neighbors_are_object_color = True
        for nr, nc in neighbors:
            if grid[nr, nc] != object_color:
                all_neighbors_are_object_color = False
                break
        
        if all_neighbors_are_object_color:
            return True # Found an interior pixel, so it's solid
            
    return False # No interior pixel found

def _create_outline(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> np.ndarray:
    """Keep only object pixels adjacent to background."""
    height, width = grid.shape
    output_grid = np.zeros_like(grid) # Start with all background

    for r, c in object_pixels:
        is_boundary = False
        neighbors = _get_neighbors(r, c, height, width)
        for nr, nc in neighbors:
            if grid[nr, nc] == 0: # Check if adjacent to background
                is_boundary = True
                break
        
        if is_boundary:
            output_grid[r, c] = object_color
            
    return output_grid

def _fill_shape(grid: np.ndarray, object_color: int) -> np.ndarray:
    """Fill the shape defined by the hollow object."""
    height, width = grid.shape
    output_grid = grid.copy() # Start with the input grid

    for r in range(height):
        for c in range(width):
            if output_grid[r, c] == 0: # Only consider filling background pixels
                # Check horizontal containment
                found_left = any(output_grid[r, j] == object_color for j in range(c))
                found_right = any(output_grid[r, j] == object_color for j in range(c + 1, width))
                horizontal_contained = found_left and found_right

                # Check vertical containment
                found_up = any(output_grid[i, c] == object_color for i in range(r))
                found_down = any(output_grid[i, c] == object_color for i in range(r + 1, height))
                vertical_contained = found_up and found_down

                # Fill if horizontally OR vertically contained
                if horizontal_contained or vertical_contained:
                    output_grid[r, c] = object_color
                    
    return output_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by either filling a hollow shape or creating an outline 
    of a solid shape.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Find the object's color and pixel coordinates
    object_color, object_pixels = _find_object_pixels(grid_np)

    # Handle edge case: no object found or empty grid
    if object_color == 0 or not object_pixels:
        return input_grid # Return original grid if no object pixels

    # Determine if the object is solid or hollow
    solid = _is_solid(grid_np, object_pixels, object_color)

    # Apply the corresponding transformation
    if solid:
        # If solid, create the outline
        output_grid_np = _create_outline(grid_np, object_pixels, object_color)
    else:
        # If hollow, fill the shape
        # Note: The fill logic needs the original pixel locations, 
        # so we pass the original grid_np, not just object_pixels
        output_grid_np = _fill_shape(grid_np, object_color)

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid

```
