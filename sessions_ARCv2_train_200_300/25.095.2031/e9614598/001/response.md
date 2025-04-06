```python
import copy

"""
Transforms the input grid by finding two marker points (value 1), calculating their integer midpoint, 
and drawing a plus sign (value 3) centered at that midpoint on the output grid. 
The original marker points are preserved.
"""

def find_markers(grid: list[list[int]], marker_value: int = 1) -> list[tuple[int, int]]:
    """Finds the coordinates of all cells with the specified marker value."""
    markers = []
    height = len(grid)
    if height == 0:
        return markers
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] == marker_value:
                markers.append((r, c))
    return markers

def draw_plus(grid: list[list[int]], center_r: int, center_c: int, draw_value: int = 3):
    """Draws a plus shape with the draw_value centered at (center_r, center_c)"""
    height = len(grid)
    width = len(grid[0])
    
    # Define the coordinates for the plus sign relative to the center
    plus_coords = [
        (center_r, center_c),      # Center
        (center_r - 1, center_c),  # Up
        (center_r + 1, center_c),  # Down
        (center_r, center_c - 1),  # Left
        (center_r, center_c + 1)   # Right
    ]
    
    # Draw the plus sign onto the grid
    for r, c in plus_coords:
        # Check if the coordinate is within the grid boundaries
        if 0 <= r < height and 0 <= c < width:
            grid[r][c] = draw_value

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation: finds two '1' markers, calculates their midpoint, 
    and draws a '3' plus sign centered there.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    height = len(output_grid)
    if height == 0:
        return output_grid
    width = len(output_grid[0])
    if width == 0:
        return output_grid

    # Find the coordinates of the two marker points (value 1)
    markers = find_markers(output_grid, 1)

    # Proceed only if exactly two markers are found (as per examples)
    if len(markers) == 2:
        (r1, c1), (r2, c2) = markers

        # Calculate the integer midpoint coordinates
        # Integer division // automatically handles the floor for midpoint calculation
        mr = (r1 + r2) // 2
        mc = (c1 + c2) // 2

        # Draw the plus sign (value 3) centered at the midpoint
        draw_plus(output_grid, mr, mc, 3)

    # Return the modified grid
    return output_grid
```