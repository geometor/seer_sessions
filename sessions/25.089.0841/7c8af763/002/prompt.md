
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions in the input grid separated by gray (5) pixels or grid boundaries.
For each region:
1. Checks if any red (2) pixels exist within the region. If yes, the fill color is red (2).
2. If no red pixels exist, checks if any blue (1) pixels exist. If yes, the fill color is blue (1).
3. If neither red nor blue pixels exist, the fill color is effectively white (0) (no change).
Creates an output grid by copying the input.
Then, for each region, fills all original white (0) pixels within that region with the determined fill color (red or blue).
Original non-white pixels (including gray borders and the influencer red/blue pixels) remain unchanged.
"""

def find_region(grid, start_row, start_col, visited):
    """
    Performs a Breadth-First Search (BFS) to find a contiguous region of non-gray pixels.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row for the BFS.
        start_col (int): The starting column for the BFS.
        visited (np.array): A boolean array marking visited cells.

    Returns:
        tuple: A tuple containing:
            - set: Coordinates ((row, col)) of all pixels in the found region.
            - set: Colors present in the found region.
    """
    rows, cols = grid.shape
    q = deque([(start_row, start_col)])
    region_coords = set()
    region_colors = set()
    gray_color = 5

    while q:
        r, c = q.popleft()

        # Check bounds and if already visited
        if r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c]:
            continue
        
        # Check if it's a boundary color (gray)
        if grid[r,c] == gray_color:
            continue

        # Process the pixel
        visited[r, c] = True
        region_coords.add((r, c))
        region_colors.add(grid[r, c])

        # Add neighbors to the queue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Add neighbor if it's within bounds and not visited (boundary check happens at dequeue)
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                 q.append((nr, nc))
                 
    return region_coords, region_colors


def transform(input_grid):
    """
    Transforms the input grid based on regional color filling rules.
    White (0) pixels within a region defined by gray (5) borders are filled
    with red (2) if the region contains any red pixels, otherwise with blue (1)
    if the region contains any blue pixels. Gray borders and original red/blue
    pixels remain unchanged.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape
    visited = np.zeros((rows, cols), dtype=bool)
    gray_color = 5
    white_color = 0
    blue_color = 1
    red_color = 2

    # Iterate through each cell to find starting points for regions
    for r in range(rows):
        for c in range(cols):
            # If the cell is not gray and hasn't been visited yet, start a region search
            if input_np[r, c] != gray_color and not visited[r, c]:
                # Find all connected non-gray pixels and the colors within that region
                region_coords, region_colors = find_region(input_np, r, c, visited)

                # Determine the fill color based on priority (Red > Blue)
                fill_color = 0 # Default to no change (for white pixels)
                if red_color in region_colors:
                    fill_color = red_color
                elif blue_color in region_colors:
                    fill_color = blue_color

                # If a fill color (Red or Blue) was determined, update the output grid
                if fill_color != 0:
                    for reg_r, reg_c in region_coords:
                        # Only change pixels that were originally white
                        if input_np[reg_r, reg_c] == white_color:
                            output_grid[reg_r, reg_c] = fill_color

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 5 1 5 5 2 5 5 5 1
0 0 0 5 0 0 0 5 0 0
0 0 0 5 0 0 0 2 0 0
0 0 0 5 0 0 0 5 0 0
5 2 5 5 5 5 5 5 2 5
0 0 0 5 0 0 0 5 0 0
0 0 0 1 0 0 0 5 0 0
0 0 0 5 0 0 0 5 0 0
0 0 0 5 0 0 0 5 0 0
5 2 5 5 5 5 1 5 5 2
```
Expected Output:
```
1 5 1 5 5 2 5 5 5 1
1 1 1 5 2 2 2 5 2 2
1 1 1 5 2 2 2 2 2 2
1 1 1 5 2 2 2 5 2 2
5 2 5 5 5 5 5 5 2 5
2 2 2 5 1 1 1 5 2 2
2 2 2 1 1 1 1 5 2 2
2 2 2 5 1 1 1 5 2 2
2 2 2 5 1 1 1 5 2 2
5 2 5 5 5 5 1 5 5 2
```
Transformed Output:
```
1 5 1 5 5 2 5 5 5 1
2 2 2 5 2 2 2 5 2 2
2 2 2 5 2 2 2 2 2 2
2 2 2 5 2 2 2 5 2 2
5 2 5 5 5 5 5 5 2 5
2 2 2 5 2 2 2 5 2 2
2 2 2 1 2 2 2 5 2 2
2 2 2 5 2 2 2 5 2 2
2 2 2 5 2 2 2 5 2 2
5 2 5 5 5 5 1 5 5 2
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 42.0

## Example 2:
Input:
```
2 5 5 5 1 5 5 5 5 2
0 0 5 0 0 0 0 5 0 0
0 0 1 0 0 0 0 1 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
5 1 5 5 5 2 5 5 5 1
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 2 0 0
0 0 5 0 0 0 0 5 0 0
1 5 5 5 2 5 5 5 5 1
```
Expected Output:
```
2 5 5 5 1 5 5 5 5 2
1 1 5 1 1 1 1 5 1 1
1 1 1 1 1 1 1 1 1 1
1 1 5 1 1 1 1 5 1 1
1 1 5 1 1 1 1 5 1 1
5 1 5 5 5 2 5 5 5 1
1 1 5 2 2 2 2 5 1 1
1 1 5 2 2 2 2 2 1 1
1 1 5 2 2 2 2 5 1 1
1 5 5 5 2 5 5 5 5 1
```
Transformed Output:
```
2 5 5 5 1 5 5 5 5 2
2 2 5 2 2 2 2 5 2 2
2 2 1 2 2 2 2 1 2 2
2 2 5 2 2 2 2 5 2 2
2 2 5 2 2 2 2 5 2 2
5 1 5 5 5 2 5 5 5 1
2 2 5 2 2 2 2 5 2 2
2 2 5 2 2 2 2 2 2 2
2 2 5 2 2 2 2 5 2 2
1 5 5 5 2 5 5 5 5 1
```
Match: False
Pixels Off: 44
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 87.99999999999999

## Example 3:
Input:
```
1 5 2 5 2 5 5 5 5 1
0 0 0 5 0 0 2 0 0 0
0 0 0 5 0 0 5 0 0 0
5 2 5 5 5 1 5 5 2 5
0 0 0 5 0 0 2 0 0 0
0 0 0 1 0 0 5 0 0 0
2 2 5 5 1 5 5 5 1 5
0 0 0 5 0 0 1 0 0 0
0 0 0 5 0 0 5 0 0 0
5 5 1 5 5 1 5 5 2 5
```
Expected Output:
```
1 5 2 5 2 5 5 5 5 1
2 2 2 5 2 2 2 2 2 2
2 2 2 5 2 2 5 2 2 2
5 2 5 5 5 1 5 5 2 5
2 2 2 5 1 1 2 2 2 2
2 2 2 1 1 1 5 2 2 2
2 2 5 5 1 5 5 5 1 5
2 2 2 5 1 1 1 1 1 1
2 2 2 5 1 1 5 1 1 1
5 5 1 5 5 1 5 5 2 5
```
Transformed Output:
```
1 5 2 5 2 5 5 5 5 1
2 2 2 5 2 2 2 2 2 2
2 2 2 5 2 2 5 2 2 2
5 2 5 5 5 1 5 5 2 5
2 2 2 5 2 2 2 2 2 2
2 2 2 1 2 2 5 2 2 2
2 2 5 5 1 5 5 5 1 5
2 2 2 5 2 2 1 2 2 2
2 2 2 5 2 2 5 2 2 2
5 5 1 5 5 1 5 5 2 5
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.0
