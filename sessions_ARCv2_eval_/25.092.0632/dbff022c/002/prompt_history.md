
## train_1

**input:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 7 7 7 7 0
0 3 0 0 3 0 0 7 0 7 7 0
0 0 3 0 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 0 7 7 0
0 0 3 3 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 0 0 8 0 0
6 8 0 0 8 0 0 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```


**output:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 5 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 5 4
0 0 0 0 0 0 0 4 4 4
```


## train_3

**input:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 0 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 0 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```


**output:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```

**Perception:**

1.  **Input/Output Structure:** Both input and output are grids of colored pixels (represented by integers 0-9). The output grid generally resembles the input grid, with specific modifications.
2.  **Core Transformation:** The primary change involves filling regions of `white` (0) pixels within the input grid with a specific non-`white` color.
3.  **Identifying Regions to Fill:** The `white` regions that get filled appear to be "holes" – contiguous areas of `white` pixels that are completely surrounded (including diagonals) by pixels of a single, uniform non-`white` color.
4.  **Determining Fill Color:** The color used to fill a hole depends on the color (`C`) of the surrounding pixels. There's a specific mapping rule:
    *   If the surrounding color `C` is Green (3), the fill color `F` is Green (3).
    *   If `C` is Orange (7), `F` is Orange (7).
    *   If `C` is Red (2), `F` is Orange (7).
    *   If `C` is Gray (8), `F` is Blue (1).
    *   If `C` is Yellow (4), the rule is conditional:
        *   If the grid is square (height equals width), the fill color `F` is determined by the grid dimension (Height / 2 or Width / 2). For example, in a 12x12 grid, F=6 (Magenta); in a 10x10 grid, F=5 (Gray).
        *   If the grid is not square, holes surrounded by Yellow (4) are *not* filled (remain `white` (0)).
5.  **No Other Changes:** Pixels that are not part of these fillable `white` holes remain unchanged from input to output. Shapes and other colored pixels retain their original positions and colors.

**Facts (YAML):**


```yaml
task_description: Fill enclosed white regions based on surrounding color and grid properties.

elements:
  - element: grid
    description: A 2D array of pixels with integer values 0-9 representing colors.
  - element: pixel
    description: A single cell in the grid with a color value.
    properties:
      - color: Integer 0-9.
      - position: (row, column) coordinates.
  - element: region
    description: A contiguous area of pixels of the same color.
    properties:
      - color: The uniform color of the pixels in the region.
      - connectivity: Pixels are connected horizontally, vertically, or diagonally (8-way adjacency).
  - element: hole
    description: A contiguous region of white (0) pixels.
    properties:
      - boundary_pixels: The set of non-white pixels directly adjacent (8-way) to the hole region.
      - surrounding_color_uniformity: Whether all boundary pixels share the same single color C.
      - surrounding_color: The uniform color C of the boundary pixels, if uniformity holds.

actions:
  - action: identify_holes
    description: Find all contiguous regions of white (0) pixels.
  - action: analyze_boundary
    description: For each white region, determine the set of adjacent non-white pixels and check if they are all of a single color C.
  - action: determine_fill_color
    description: Based on the surrounding color C and grid properties (shape and size), determine the fill color F according to specific rules.
  - action: fill_hole
    description: Change the color of all pixels within an identified hole region to the determined fill color F (if F is non-white).

relationships:
  - relationship: enclosure
    description: A white region is enclosed if all its adjacent non-white pixels have the same color C.
  - relationship: color_mapping
    description: A mapping exists between the surrounding color C and the fill color F.
    details:
      - C=2 (Red) -> F=7 (Orange)
      - C=3 (Green) -> F=3 (Green)
      - C=7 (Orange) -> F=7 (Orange)
      - C=8 (Gray) -> F=1 (Blue)
      - C=4 (Yellow) -> depends on grid shape/size
  - relationship: grid_property_dependency
    description: The fill rule for holes surrounded by Yellow (4) depends on whether the grid is square and its dimensions.
    details:
      - If grid is square (H=W), F = H / 2.
      - If grid is not square, F = 0 (no fill).

```


**Natural Language Program:**

1.  Start with the input grid. Initialize the output grid as a copy of the input grid.
2.  Find all distinct contiguous regions of `white` (0) pixels in the input grid. Use 8-way adjacency (horizontal, vertical, and diagonal connections). Keep track of visited `white` pixels to process each region only once.
3.  For each `white` region found:
    a.  Identify all pixels that are adjacent (8-way) to any pixel within this `white` region.
    b.  From these adjacent pixels, collect only the ones that are *not* `white` (color > 0). Let this set be the `boundary_pixels`.
    c.  Check if the `boundary_pixels` set is non-empty and if all pixels in this set have the exact same color. Let this uniform color be `C`.
    d.  If such a uniform surrounding color `C` exists, determine the fill color `F` based on the following rules:
        i.  If `C` is Green (3), set `F` to Green (3).
        
```python
import numpy as np
from collections import deque

"""
Identify contiguous regions of white (0) pixels in the input grid using 8-way adjacency.
For each distinct white region found:
1. Identify all non-white pixels that are adjacent (8-way, including diagonals) to any pixel within the white region. These form the 'boundary pixels'.
2. Check if the set of boundary pixels is non-empty and if all boundary pixels share the exact same color, C.
3. If a uniform surrounding color C exists, determine the fill color F based on the following rules:
    - If C is Green (3), set F to Green (3).
    - If C is Orange (7), set F to Orange (7).
    - If C is Red (2), set F to Orange (7).
    - If C is Gray (8), set F to Blue (1).
    - If C is Yellow (4):
        - Check if the input grid is square (height equals width).
        - If the grid is square, set F to the color value equal to the grid's height (or width) divided by 2 using integer division (e.g., a 10x10 grid results in F=5).
        - If the grid is not square, set F to white (0), meaning the hole is not filled.
    - For any other uniform surrounding color C not listed above, set F to white (0) (no fill).
4. If a non-white fill color F (F > 0) is determined for the white region, change the color of all pixels belonging to that specific white region to F in the output grid.
5. Pixels that are not part of a fillable white region (either because they were not white initially, or the white region didn't meet the filling criteria) remain unchanged from the input grid.
Initialize the output grid as a copy of the input grid, and apply the modifications based on the rules above.
"""

def get_neighbors(r, c, height, width):
    """ 
    Get 8-way adjacent neighbor coordinates (including diagonals) 
    for a given cell (r, c) that are within the grid bounds.
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_white_region_and_boundary(grid, start_r, start_c, visited):
    """
    Performs a Breadth-First Search (BFS) starting from (start_r, start_c)
    to find a contiguous region of white (0) pixels using 8-way adjacency.
    It identifies the non-white pixels adjacent to this region (boundary).

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): A boolean grid marking visited pixels.

    Returns:
        tuple: A tuple containing:
            - region_coords (set): A set of (r, c) tuples for pixels in the white region.
            - boundary_pixels (set): A set of ((r, c), color) tuples for boundary pixels.
        Returns (None, None) if the starting pixel is invalid (already visited or not white).
    """
    height, width = grid.shape
    # Check if the starting point is valid
    if visited[start_r, start_c] or grid[start_r, start_c] != 0:
        return None, None

    region_coords = set()
    # Using a set for boundary_pixels automatically handles duplicates
    boundary_pixels = set() 
    queue = deque([(start_r, start_c)])
    # Mark the starting pixel as visited immediately
    visited[start_r, start_c] = True 
    
    while queue:
        r, c = queue.popleft()
        # Add the current pixel to the identified white region
        region_coords.add((r, c))

        # Explore neighbors
        for nr, nc in get_neighbors(r, c, height, width):
            neighbor_color = grid[nr, nc]
            if neighbor_color == 0: # Neighbor is white
                # If this white neighbor hasn't been visited, add to queue
                if not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))
            else: # Neighbor is non-white, potential boundary pixel
                # Add the boundary pixel's coordinate and color to the set
                boundary_pixels.add(((nr, nc), neighbor_color))
                
    return region_coords, boundary_pixels


def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions based 
    on the surrounding color and grid properties.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, leaving the original input unchanged
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    # Keep track of visited white pixels to process each region only once
    visited = np.zeros_like(input_np, dtype=bool)

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Check if it's a white pixel and hasn't been visited yet
            if input_np[r, c] == 0 and not visited[r, c]:
                # Found the start of a potential white region, explore it
                region_coords, boundary_pixels = find_white_region_and_boundary(input_np, r, c, visited)

                # If the region exploration was valid (started on a white pixel)
                if region_coords is not None:
                    # Check if the region has any boundary pixels
                    if not boundary_pixels:
                        # No boundary (e.g., touches grid edge or fully surrounded by white)
                        # Or an isolated white pixel with no non-white neighbours - skip.
                        continue 

                    # Extract the colors of all boundary pixels
                    boundary_colors = {color for _, color in boundary_pixels}
                    
                    # Check if all boundary pixels have the same single color
                    if len(boundary_colors) == 1:
                        surrounding_color_C = boundary_colors.pop()
                        fill_color_F = 0 # Default: no fill (keep white)

                        # Apply the color mapping rules
                        if surrounding_color_C == 3: # Green surround -> Green fill
                            fill_color_F = 3
                        elif surrounding_color_C == 7: # Orange surround -> Orange fill
                            fill_color_F = 7
                        elif surrounding_color_C == 2: # Red surround -> Orange fill
                            fill_color_F = 7 
                        elif surrounding_color_C == 8: # Gray surround -> Blue fill
                            fill_color_F = 1 
                        elif surrounding_color_C == 4: # Yellow surround - check grid shape
                            if height == width: # Grid is square
                                # Fill color is determined by grid dimension / 2
                                fill_color_F = height // 2
                                # Ensure calculated color is valid (0-9). Redundant for ARC constraints but safe.
                                if not (0 <= fill_color_F <= 9):
                                    fill_color_F = 0 # Revert to no fill if calculation is out of bounds
                            else: # Grid is not square
                                fill_color_F = 0 # No fill for yellow in non-square grids
                        
                        # If a valid non-white fill color was determined
                        if fill_color_F != 0:
                            # Iterate through all coordinates of the identified white region
                            for reg_r, reg_c in region_coords:
                                # Update the color in the output grid
                                output_grid[reg_r, reg_c] = fill_color_F

    # Convert the final numpy array back to a list of lists for the output
    return output_grid.tolist()
```
