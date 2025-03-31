
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
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


**output:**
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


## train_3

**input:**
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


**output:**
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

Okay, let's break down this task.

**Perception of Elements:**

1.  **Grid Structure:** The input and output grids are the same size (10x10 in all examples).
2.  **Persistent Elements:** The gray (5) pixels form lines or borders within the grid. These gray pixels remain unchanged between the input and output grids. They appear to divide the grid into distinct regions or compartments.
3.  **Changing Elements:** The white (0) pixels in the input are the primary elements that change color in the output. They are replaced by either blue (1) or red (2).
4.  **Influencing Elements:** The blue (1) and red (2) pixels present in the input seem to determine the color that fills the white (0) areas within their respective regions. These blue and red pixels themselves remain unchanged in the output.
5.  **Regions:** The areas enclosed by gray (5) lines (and the grid boundaries) act as independent zones for the color transformation.
6.  **Transformation Logic:** Within each region defined by the gray borders:
    *   If the region contains at least one red (2) pixel in the input, all white (0) pixels within that region become red (2) in the output.
    *   If the region contains no red (2) pixels but does contain at least one blue (1) pixel, all white (0) pixels within that region become blue (1) in the output.
    *   If a region contains only white (0) pixels (and gray borders), the white pixels would likely remain white (though this specific scenario isn't explicitly shown in the examples).
7.  **Color Priority:** Red (2) has priority over blue (1) when determining the fill color for a region.

**YAML Facts:**


```yaml
grid_properties:
  size_preservation: Input and output grids have the same dimensions.
  immutable_color: Gray (5) pixels remain unchanged and act as boundaries.
  mutable_color: White (0) pixels are subject to change.
  influencer_colors: Blue (1) and Red (2) pixels influence the change but remain unchanged themselves.

regions:
  definition: Areas of contiguous non-Gray (5) pixels, bounded by Gray (5) pixels or the grid edges.
  independence: Each region's transformation is determined independently.

transformation_rule:
  target: White (0) pixels within a region.
  condition_priority_1:
    trigger: Presence of at least one Red (2) pixel within the region in the input.
    action: Change all White (0) pixels in that region to Red (2) in the output.
  condition_priority_2:
    trigger: No Red (2) pixels are present, but at least one Blue (1) pixel is present within the region in the input.
    action: Change all White (0) pixels in that region to Blue (1) in the output.
  condition_priority_3:
    trigger: No Red (2) or Blue (1) pixels are present within the region in the input.
    action: White (0) pixels remain White (0). (Inferred, not explicitly shown in examples).
  source_pixel_preservation: Original Blue (1) and Red (2) pixels within the region remain unchanged in the output.
```


**Natural Language Program:**

1.  Identify all distinct contiguous regions in the input grid that are not composed of gray (5) pixels. These regions are separated by gray (5) pixels or the grid boundaries.
2.  For each identified region:
    a.  Scan all pixels within that region in the input grid.
    b.  Check if any pixel within the region has the color red (2).
    c.  If red (2) is found, determine the fill color for this region to be red (2).
    d.  If no red (2) pixels are found, check if any pixel within the region has the color blue (1).
    e.  If blue (1) is found (and no red (2) was found), determine the fill color for this region to be blue (1).
    f.  If neither red (2) nor blue (1) is found, the fill color is effectively white (0) (meaning no change occurs for white pixels in this region).
3.  Create the output grid by copying the input grid.
4.  For each region identified in step 1:
    a.  Retrieve the determined fill color (red, blue, or white) for that region from step 2.
    b.  Iterate through all pixels within that region in the output grid.
    c.  If a pixel's original color in the input grid was white (0), change its color in the output grid to the determined fill color for that region. Otherwise, leave the pixel's color unchanged.
5.  The resulting grid is the final output.
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
