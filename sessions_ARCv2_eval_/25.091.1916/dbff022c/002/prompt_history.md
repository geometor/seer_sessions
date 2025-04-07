
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

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are grids of colored pixels. The output grid largely mirrors the input grid, with specific modifications.
2.  **Objects:** The grids contain distinct shapes (objects) formed by contiguous pixels of the same non-white color. Some shapes are single-colored (like the yellow 'U', green 'H', orange 'C' in example 1), while others are multi-colored conglomerates.
3.  **Key Feature:** The core transformation involves filling enclosed white (0) areas within single-colored shapes. Multi-colored shapes seem unaffected by this filling process.
4.  **Enclosed Areas:** These are regions of white pixels completely surrounded by pixels of a single non-white color or other enclosed white pixels. They do not touch the grid boundary or larger background white areas.
5.  **Fill Color Logic:** The color used to fill these enclosed white areas seems determined by a rule involving the color of the enclosing shape and potentially the colors of adjacent shapes.
    *   In some cases (e.g., the green 'H' and orange 'C' in example 1), the fill color matches the color of the enclosing shape itself.
    *   In other cases (e.g., the yellow 'U' in example 1 fills with magenta; the azure 'H' in example 2 fills with blue), the fill color is *different* from the enclosing shape.
    *   Observing the cases where the fill color differs, it appears to be influenced by the color of pixels from *other* shapes that are directly adjacent (orthogonally) to the enclosed white region. If such "foreign" colored pixels touch the white hole, the most frequent *foreign* color seems to be chosen. If there's a tie in frequency, the lowest color index among the tied foreign colors seems to be selected (e.g., Example 1, Yellow U: Magenta(6) and Orange(7) both touch the hole once, Magenta(6) is chosen). If no foreign colors touch the hole, the shape's own color is used.

**YAML Facts:**


```yaml
task_description: Fill enclosed white regions within single-colored shapes based on adjacent colors.

elements:
  - element: grid
    description: A 2D array of pixels with integer values 0-9 representing colors.
  - element: pixel
    description: A single cell in the grid with a color value. White (0) is the background. Non-zero values represent colors.
  - element: shape
    description: A contiguous region of pixels of the same non-white color.
    properties:
      - color: The single color of the shape's pixels.
      - boundary: Pixels of the shape adjacent to white pixels or pixels of a different color.
      - interior: Pixels of the shape not on the boundary.
  - element: enclosed_region
    description: A contiguous region of white (0) pixels that cannot reach the grid boundary by moving only through white pixels.
    properties:
      - size: Number of pixels in the region.
      - location: Coordinates of the pixels.
      - adjacent_shape_color: The color of the shape immediately surrounding the region.
      - adjacent_foreign_colors: List of colors (and their counts) from pixels of *other* shapes that are orthogonally adjacent to any pixel in the enclosed region.

actions:
  - action: identify_enclosed_regions
    description: Find all connected components of white pixels that are not reachable from the grid boundary via other white pixels.
    using: Flood fill from boundary white pixels.
  - action: determine_fill_color
    description: For each enclosed region, determine the color to fill it with.
    logic: >
      1. Identify the primary color (C_primary) of the surrounding shape.
      2. Find all orthogonal neighboring pixels to the region that are non-white AND not C_primary.
      3. If no such neighbors exist, the fill color is C_primary.
      4. If such neighbors exist, count the frequency of each color among them.
      5. The fill color is the color with the highest frequency. If there's a tie for the highest frequency, choose the color with the lowest index among the tied colors.
  - action: fill_region
    description: Change the color of all pixels within an enclosed region to the determined fill color.

relationships:
  - relationship: adjacency
    description: Pixels are adjacent if they share an edge (orthogonal adjacency). Used for defining shapes, regions, and determining fill colors.
  - relationship: enclosure
    description: A white region is enclosed by a shape if all paths from the region to the grid boundary must pass through non-white pixels.
  - relationship: influence
    description: The colors of shapes adjacent to an enclosed white region can influence the color used to fill that region.

input_output_relationship:
  - The output grid is identical to the input grid, except that identified enclosed white regions within single-colored shapes are filled with a color determined by the adjacency rules. Multi-colored shapes and shapes without enclosed regions remain unchanged.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all white pixels (color 0) in the input grid that are "enclosed". An enclosed white pixel is one that cannot reach any boundary pixel of the grid by traveling only through adjacent (up, down, left, right) white pixels. This can be found by performing a flood fill starting from all white pixels on the grid's border; any white pixel not reached by this flood fill is enclosed.
3.  Group the identified enclosed white pixels into connected regions (where connectivity is defined by orthogonal adjacency).
4.  For each distinct enclosed white region:
    a.  Determine the single primary color (`C_primary`) of the shape that immediately surrounds this region (i.e., the color of the non-white pixels orthogonally adjacent to the region's pixels).
    b.  Examine all non-white pixels that are orthogonally adjacent to *any* pixel within the current enclosed white region.
    c.  Create a list of colors from these adjacent non-white pixels, excluding any pixels that have the color `C_primary`. Let this list be `Foreign_Colors`.
    d.  If the `Foreign_Colors` list is empty, set the `Fill_Color` for this region to `C_primary`.
    e.  If the `Foreign_Colors` list is not empty:
        i.  Count the occurrences of each distinct color in the `Foreign_Colors` list.
        ii. Find the maximum occurrence count.
        iii. Identify all colors that have this maximum count.
        iv. Select the color with the *lowest* numerical index value among these most frequent colors. Set this as the `Fill_Color`.
    f.  Change the color of all pixels in the output grid corresponding to the current enclosed white region to the determined `Fill_Color`.
5.  Return the modified output grid.
```python
import numpy as np
from collections import deque, Counter

"""
Identifies enclosed regions of white pixels (0) within single-colored shapes in the input grid. 
Determines a fill color for each enclosed region based on the colors of adjacent pixels from other shapes. 
If no other shapes are adjacent to the enclosed region, it's filled with the color of the surrounding shape. 
If other shapes are adjacent, the fill color is the most frequent adjacent color from those other shapes (ties broken by lowest color index).
The output grid is the input grid with these enclosed regions filled.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_enclosed_regions(grid):
    """
    Finds all connected regions of white pixels (0) that are not reachable 
    from the grid boundary via other white pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of regions, where each region is a list of (row, col) tuples.
    """
    height, width = grid.shape
    visited_background = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Start BFS from all boundary white pixels
    for r in range(height):
        if grid[r, 0] == 0 and not visited_background[r, 0]:
            q.append((r, 0))
            visited_background[r, 0] = True
        if grid[r, width - 1] == 0 and not visited_background[r, width - 1]:
            q.append((r, width - 1))
            visited_background[r, width - 1] = True
    for c in range(width):
        if grid[0, c] == 0 and not visited_background[0, c]:
            q.append((0, c))
            visited_background[0, c] = True
        if grid[height - 1, c] == 0 and not visited_background[height - 1, c]:
            q.append((height - 1, c))
            visited_background[height - 1, c] = True

    while q:
        r, c = q.popleft()
        for nr, nc in get_neighbors(r, c, height, width):
            if grid[nr, nc] == 0 and not visited_background[nr, nc]:
                visited_background[nr, nc] = True
                q.append((nr, nc))

    # Identify enclosed white pixels (those not visited)
    enclosed_coords = set()
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited_background[r, c]:
                enclosed_coords.add((r, c))

    # Group enclosed pixels into connected regions using BFS
    regions = []
    processed_enclosed = set()

    for r_start, c_start in enclosed_coords:
        if (r_start, c_start) in processed_enclosed:
            continue

        current_region = []
        region_q = deque([(r_start, c_start)])
        processed_enclosed.add((r_start, c_start))
        
        while region_q:
            r, c = region_q.popleft()
            current_region.append((r, c))

            for nr, nc in get_neighbors(r, c, height, width):
                coord = (nr, nc)
                # Check if the neighbor is an enclosed white pixel AND not yet processed for this region
                if coord in enclosed_coords and coord not in processed_enclosed:
                    processed_enclosed.add(coord)
                    region_q.append(coord)
        
        if current_region:
            regions.append(current_region)
            
    return regions


def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions within 
    single-colored shapes based on adjacent colors.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Find all enclosed white regions
    enclosed_regions = find_enclosed_regions(grid)

    # Process each enclosed region
    for region_coords in enclosed_regions:
        if not region_coords:
            continue

        primary_colors = set()
        foreign_colors = []
        
        # Determine the primary surrounding color and collect foreign adjacent colors
        for r, c in region_coords:
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = grid[nr, nc]
                if neighbor_color != 0: # If neighbor is not white
                    # If neighbor is not part of the current region (should always be true for non-white neighbors)
                    if (nr, nc) not in region_coords: 
                        primary_colors.add(neighbor_color)
        
        # If the region is bordered by more than one color, it doesn't fit the pattern
        # (Based on examples, enclosed regions are surrounded by a single color)
        # If primary_colors is empty, something is wrong (a white hole with no colored neighbors?)
        if len(primary_colors) != 1:
            # print(f"Warning: Region at {region_coords[0]} has {len(primary_colors)} primary colors: {primary_colors}. Skipping.")
            continue # Skip this region if it's not enclosed by a single color
            
        c_primary = list(primary_colors)[0]

        # Now collect foreign colors adjacent to the region
        for r, c in region_coords:
             for nr, nc in get_neighbors(r, c, height, width):
                 neighbor_color = grid[nr, nc]
                 if neighbor_color != 0 and neighbor_color != c_primary:
                     foreign_colors.append(neighbor_color)

        # Determine the fill color
        fill_color = c_primary # Default to primary color
        if foreign_colors:
            color_counts = Counter(foreign_colors)
            max_freq = 0
            # Find the maximum frequency
            for color in color_counts:
                 if color_counts[color] > max_freq:
                     max_freq = color_counts[color]
            
            # Find all colors with the maximum frequency
            most_frequent_colors = []
            for color in color_counts:
                if color_counts[color] == max_freq:
                    most_frequent_colors.append(color)
            
            # Choose the one with the lowest index (value)
            fill_color = min(most_frequent_colors)

        # Fill the region in the output grid
        for r, c in region_coords:
            output_grid[r, c] = fill_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
