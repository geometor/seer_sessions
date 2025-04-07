
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transforms an input grid based on a hierarchical set of rules:

1.  Vertical Red Line Rule: If a contiguous vertical line of Red (2) pixels exists spanning the grid's height at column 'c':
    - Copy the input grid to the output grid.
    - Change the pixels in the output grid at column 'c' to Blue (1).
    - Fill the area in the output grid to the left of the line (columns < c) with Red (2).
    - Pixels to the right (columns > c) remain as they were in the input grid.
    This rule takes precedence over all others.

2.  Azure Presence Rule: If no vertical Red line is found, check if Azure (8) is present in the input grid.
    - If Azure (8) is present:
        a. Count the frequency of all non-white (0) and non-azure (8) colors.
        b. If no such colors exist (only white and/or azure present): Create the output grid by copying the input grid and changing all Azure(8) pixels to white(0).
        c. If other colors exist, find the Most Frequent Color (MFC) among them. (Assume lowest color value wins ties, though none observed in examples).
        d. Apply transformation based on MFC:
            - If MFC is Blue (1):
                i. Find all contiguous Blue (1) objects using 8-way adjacency (including diagonals).
                ii. Identify the largest Blue object by pixel count.
                iii. Create a new output grid filled entirely with white (0).
                iv. Draw the shape of the largest Blue object onto the output grid using Red (2).
            - If MFC is Magenta (6):
                i. Create an intermediate grid, initially filled with white (0).
                ii. Populate the intermediate grid by applying these transformations based on the input grid: Magenta(6)->Orange(7), Orange(7)->Magenta(6), Red(2)->Yellow(4), Yellow(4)->Red(2). All other input colors (including Azure) result in white(0) in the intermediate grid.
                iii. Initialize the final output grid as a copy of this intermediate grid.
                iv. Iterate through the *original input* grid. If an input pixel at (r, c) is Magenta(6) and the pixel below it (r+1, c) is white(0) (and within bounds), set the *final output* grid pixel at (r+1, c) to Orange(7).
                v. Similarly, if an input pixel at (r, c) is Orange(7) and the pixel below it (r+1, c) is white(0) (and within bounds), set the *final output* grid pixel at (r+1, c) to Magenta(6).
            - If MFC is Yellow (4):
                i. Initialize the output grid filled entirely with white (0).
                ii. Iterate through the input grid. If an input pixel is Yellow(4), set the corresponding output pixel to Red(2). If an input pixel is Blue(1), set the corresponding output pixel to Orange(7). All other input pixel colors result in white(0) at the corresponding output location.
            - If MFC is any other color: (Fallback based on observed Azure removal) Create the output grid by copying the input grid and changing all Azure(8) pixels to white(0).

3.  Default Rule: If no vertical Red line is found AND Azure (8) is not present, return the input grid unchanged.
"""

def find_objects(grid, color, adjacency=4):
    """Finds all contiguous objects of a given color using specified adjacency."""
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    if adjacency == 8:
        neighbor_deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else: # Default to 4-way
        neighbor_deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    # Check neighbors
                    for dr, dc in neighbor_deltas:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def find_vertical_line_column(grid, color):
    """Checks for a vertical line of a specific color and returns its column index."""
    height, width = grid.shape
    for c in range(width):
        is_line = True
        if height == 0: continue # Handle empty grid case
        for r in range(height):
            if grid[r, c] != color:
                is_line = False
                break
        if is_line:
            return c
    return None

def get_color_counts(grid):
    """Counts the frequency of non-white (0) and non-azure (8) colors."""
    counts = Counter()
    if grid.size == 0: return counts # Handle empty grid
    grid_flat = grid.flatten()
    for color in grid_flat:
        if color != 0 and color != 8:
            counts[color] += 1
    return counts

def transform(input_grid):
    """
    Applies the transformation rule based on the presence of a vertical red line
    or the most frequent color alongside azure.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    if height == 0 or width == 0: # Handle empty input
        return []

    # 1. Check for Vertical Red Line
    red_line_col = find_vertical_line_column(input_grid_np, 2)
    if red_line_col is not None:
        output_grid = np.array(input_grid_np) # Start with a copy
        # a. Fill left side with Red (2)
        if red_line_col > 0:
            output_grid[:, :red_line_col] = 2
        # b. Change line itself to Blue (1)
        output_grid[:, red_line_col] = 1
        # c. Right side remains as copied from input
        return output_grid.tolist()

    # 2. Check for Azure (8)
    if 8 in input_grid_np:
        color_counts = get_color_counts(input_grid_np)

        # 2.b Handle cases where there are no non-white, non-azure colors
        if not color_counts:
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()

        # 2.c Find MFC (using min color value as tie-breaker if needed)
        mfc = max(color_counts, key=lambda k: (color_counts[k], -k)) # Higher count wins, then lower color value wins

        # 2.d Apply transformation based on MFC
        # MFC is Blue (1)
        if mfc == 1:
            # Find largest blue object using 8-way adjacency
            blue_objects = find_objects(input_grid_np, 1, adjacency=8)
            if not blue_objects:
                # Should not happen if blue is MFC, but as a safe fallback, treat as 'other MFC'
                 output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
                 return output_grid.tolist()

            largest_blue_object = max(blue_objects, key=len)
            output_grid = np.zeros_like(input_grid_np) # Start with white grid
            for r, c in largest_blue_object:
                output_grid[r, c] = 2 # Change to Red
            return output_grid.tolist()

        # MFC is Magenta (6)
        elif mfc == 6:
            # Create intermediate grid with initial swaps
            intermediate_grid = np.zeros_like(input_grid_np)
            for r in range(height):
                for c in range(width):
                    color = input_grid_np[r, c]
                    if color == 6: intermediate_grid[r, c] = 7 # Magenta -> Orange
                    elif color == 7: intermediate_grid[r, c] = 6 # Orange -> Magenta
                    elif color == 2: intermediate_grid[r, c] = 4 # Red -> Yellow
                    elif color == 4: intermediate_grid[r, c] = 2 # Yellow -> Red
                    # Other colors (0, 1, 3, 5, 8, 9) result in 0

            output_grid = np.array(intermediate_grid) # Copy intermediate to final output

            # Apply row duplication logic based on *original* input
            for r in range(height - 1): # Iterate up to second to last row
                for c in range(width):
                    input_color = input_grid_np[r, c]
                    below_input_color = input_grid_np[r + 1, c]

                    if input_color == 6 and below_input_color == 0: # Magenta above white in input
                        output_grid[r + 1, c] = 7 # Color below Orange in output
                    elif input_color == 7 and below_input_color == 0: # Orange above white in input
                        output_grid[r + 1, c] = 6 # Color below Magenta in output

            return output_grid.tolist()

        # MFC is Yellow (4)
        elif mfc == 4:
            output_grid = np.zeros_like(input_grid_np) # Start with white grid
            for r in range(height):
                for c in range(width):
                    color = input_grid_np[r, c]
                    if color == 4: # Yellow -> Red
                        output_grid[r, c] = 2
                    elif color == 1: # Blue -> Orange
                        output_grid[r, c] = 7
                    # Other colors remain white (0)
            return output_grid.tolist()

        # MFC is any other color (Fallback)
        else:
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()


    # 3. Default Case: No vertical red line and no Azure
    # Return the input grid unchanged
    return input_grid_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 2 8 8 8
0 0 0 0 1
0 0 0 1 0
0 0 0 1 0
0 0 0 0 1
```
Expected Output:
```
0 0 0 0 0
0 0 0 0 2
0 0 0 2 2
0 0 0 2 2
0 0 0 0 2
```
Transformed Output:
```
0 0 0 0 0
0 0 0 0 2
0 0 0 2 0
0 0 0 2 0
0 0 0 0 2
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 2 0 8 0 8 0 0 0 0 0 0 0 4 0
0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 8 0 0 6 0 0 8 0 0 0 0 0 0 0
8 0 4 2 0 4 2 0 8 0 0 0 0 0 0
0 8 0 0 7 0 0 8 0 0 0 0 0 2 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 7 0 8 0 8 0 7 0 7 0 7 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 7 0 7 0 7 0 7 0 7 0 7 0 7 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0 7
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0
6 0 6 0 0 0 6 0 6 0 6 0 6 0 0
0 6 0 0 0 0 0 6 0 6 0 6 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 2 4 7 2 4 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 4 0
0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 6 0 0 7 0 0 6 0 6 0 6 0 0 0
0 6 0 0 0 0 0 6 0 6 0 6 0 0 0
```
Match: False
Pixels Off: 71
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 63.111111111111114

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 8 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 8 0 0 0 8 0 0 0 4 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0
```
Expected Output:
```
0 2 0 2 0 2 0 0 0 0 0 2 0 2 0 2 0 2 0 2
0 0 2 0 2 0 0 0 0 0 2 0 0 0 2 0 2 0 0 0
0 2 0 2 0 2 0 0 0 0 0 2 0 2 0 2 0 2 0 2
2 0 2 0 0 0 2 0 0 0 0 0 2 0 2 0 2 0 2 0
0 2 0 0 0 2 0 0 0 0 0 0 0 2 0 0 0 2 0 0
0 0 2 0 2 0 0 0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 53
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.5

## Example 4:
Input:
```
1 1 1 1 1 2 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 2 1 8 0 2 0 0
0 0 0 0 0 2 0 0
0 0 8 0 0 2 0 0
0 0 2 0 0 2 0 0
0 0 1 0 0 2 0 0
```
Expected Output:
```
2 2 2 2 2 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
```
Transformed Output:
```
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
2 2 2 2 2 1 0 0
```
Match: False
Pixels Off: 35
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 109.375
