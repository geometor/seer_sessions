```python
import numpy as np
from collections import deque

"""
Transformation Rule Description:

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected areas (components) of white (0) pixels using orthogonal adjacency.
3.  For each white area:
    a.  Determine if it is "enclosed" by red (2) pixels. An area is enclosed if none of its pixels are on the grid's outer border, AND a path of only white pixels cannot reach the border from any pixel within the area. (Effectively, check if any pixel in the area is on the border during the component finding process).
    b.  If the area is enclosed:
        i.  Check if *any* pixel within this enclosed white area has red (2) neighbors directly opposite each other (i.e., North and South neighbors are both red, OR East and West neighbors are both red).
        ii. If such a pixel exists, fill the entire enclosed white area in the output grid with azure (8).
        iii. Otherwise (if no pixel in the enclosed area has opposite red neighbors), fill the entire enclosed white area in the output grid with blue (1).
    c.  If the area is not enclosed (touches the grid border), leave it as white (0).
4.  Red (2) pixels remain unchanged.
5.  Return the modified output grid.
"""

def find_connected_components(grid):
    """Finds connected components of white pixels and checks enclosure."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = [] # List to store tuples: (area_coordinates, is_enclosed)

    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited[r, c]:
                component_coords = []
                is_enclosed_flag = True # Assume enclosed initially
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.append((curr_r, curr_c))

                    # Check if this pixel is on the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_enclosed_flag = False # Touched border, not enclosed

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found component and its enclosure status
                # The check during BFS/DFS is sufficient for enclosure. If it never hit the border, it's enclosed.
                components.append((component_coords, is_enclosed_flag))
                
    return components

def check_fill_color(area_coords, grid):
    """Determines the fill color (blue or azure) for an enclosed area."""
    height, width = grid.shape
    for r, c in area_coords:
        # Check for opposite red neighbours (North/South)
        has_north_red = (r > 0 and grid[r-1, c] == 2)
        has_south_red = (r < height - 1 and grid[r+1, c] == 2)
        if has_north_red and has_south_red:
            return 8 # Azure

        # Check for opposite red neighbours (West/East)
        has_west_red = (c > 0 and grid[r, c-1] == 2)
        has_east_red = (c < width - 1 and grid[r, c+1] == 2)
        if has_west_red and has_east_red:
            return 8 # Azure
            
    # If no pixel triggered the azure condition, fill with blue
    return 1 # Blue

def fill_area(output_grid, area_coords, fill_color):
    """Fills the specified area in the grid with the given color."""
    for r, c in area_coords:
        output_grid[r, c] = fill_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies enclosed white areas and fills them with blue (1) or azure (8)
    based on the configuration of the surrounding red (2) pixels.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all connected white areas and their enclosure status
    white_components = find_connected_components(input_grid)

    # Process each white component
    for area_coords, is_enclosed in white_components:
        if is_enclosed:
            # Determine the fill color for this enclosed area
            fill_color = check_fill_color(area_coords, input_grid)
            # Fill the area in the output grid
            fill_area(output_grid, area_coords, fill_color)
        # Else (not enclosed), do nothing, leave as white (0)

    return output_grid
```