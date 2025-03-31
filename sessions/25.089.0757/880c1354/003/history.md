
Previous Code:
```python
import numpy as np
from collections import deque

def find_connected_component(grid, start_row, start_col):
    """
    Finds all coordinates of the connected component of the same color
    starting from (start_row, start_col) using Breadth-First Search (BFS).
    Considers only 4-directional neighbors (up, down, left, right).

    Args:
        grid (np.array): The 2D grid of colors.
        start_row (int): The starting row index.
        start_col (int): The starting column index.

    Returns:
        set: A set of (row, col) tuples representing the coordinates
             of the connected component. Returns an empty set if the
             start coordinate is out of bounds.
    """
    height, width = grid.shape
    
    # Check if start coordinates are valid
    if not (0 <= start_row < height and 0 <= start_col < width):
        return set()

    target_color = grid[start_row, start_col]
    
    q = deque([(start_row, start_col)])
    visited = set([(start_row, start_col)])
    component_coords = set()

    while q:
        r, c = q.popleft()
        
        # Add the current coordinate to the component set
        component_coords.add((r, c))

        # Explore neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check neighbor validity: within bounds, not visited, and matches target color
            if 0 <= nr < height and 0 <= nc < width and \
               (nr, nc) not in visited and grid[nr, nc] == target_color:
                visited.add((nr, nc))
                q.append((nr, nc))
                
    return component_coords


def transform(input_grid):
    """
    Identifies the connected color blobs originating from the four corners
    of the input grid and swaps them diagonally. Specifically, the blob
    originating from the top-left corner is swapped with the blob
    originating from the bottom-right corner, and the blob originating
    from the top-right corner is swapped with the blob originating from
    the bottom-left corner. The pixels that do not belong to any of these
    four corner blobs remain unchanged. The swap involves changing the
    color of the pixels within each blob to the color of the diagonally
    opposite corner's starting pixel.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid_np)

    # Identify the colors at the four corner pixels
    # These colors determine the target color for the respective swaps
    c_tl = input_grid_np[0, 0]
    c_tr = input_grid_np[0, width - 1]
    c_bl = input_grid_np[height - 1, 0]
    c_br = input_grid_np[height - 1, width - 1]

    # Find the coordinates of the pixels belonging to each corner blob
    # using the connected component finding helper function.
    coords_tl = find_connected_component(input_grid_np, 0, 0)
    coords_tr = find_connected_component(input_grid_np, 0, width - 1)
    coords_bl = find_connected_component(input_grid_np, height - 1, 0)
    coords_br = find_connected_component(input_grid_np, height - 1, width - 1)

    # Create a map to track which corner blob each pixel belongs to.
    # Initialize with -1 (meaning not part of any tracked corner blob).
    # Indices: 0=TL, 1=TR, 2=BL, 3=BR
    corner_map = np.full((height, width), -1, dtype=int) 

    # Populate the corner_map. Assign pixels to the first corner blob that finds them.
    # This implicitly handles cases where blobs might touch or overlap,
    # though the examples suggest distinct corner blobs.
    for r, c in coords_tl:
        corner_map[r, c] = 0 # Mark as belonging to Top-Left blob
    for r, c in coords_tr:
        if corner_map[r, c] == -1: # Only mark if not already assigned
             corner_map[r, c] = 1 # Mark as belonging to Top-Right blob
    for r, c in coords_bl:
        if corner_map[r, c] == -1:
             corner_map[r, c] = 2 # Mark as belonging to Bottom-Left blob
    for r, c in coords_br:
        if corner_map[r, c] == -1:
             corner_map[r, c] = 3 # Mark as belonging to Bottom-Right blob

    # Apply the color swaps to the output grid based on the corner_map.
    for r in range(height):
        for c in range(width):
            origin_corner_index = corner_map[r, c]
            # If the pixel belonged to the original Top-Left blob...
            if origin_corner_index == 0: 
                output_grid[r, c] = c_br # ...change its color to the Bottom-Right corner's color.
            # If the pixel belonged to the original Top-Right blob...
            elif origin_corner_index == 1: 
                output_grid[r, c] = c_bl # ...change its color to the Bottom-Left corner's color.
            # If the pixel belonged to the original Bottom-Left blob...
            elif origin_corner_index == 2: 
                output_grid[r, c] = c_tr # ...change its color to the Top-Right corner's color.
            # If the pixel belonged to the original Bottom-Right blob...
            elif origin_corner_index == 3: 
                output_grid[r, c] = c_tl # ...change its color to the Top-Left corner's color.
            # Else: The pixel wasn't part of any corner blob, so its color remains unchanged
            # (already handled by initializing output_grid as a copy).

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
6 6 7 4 4 7 2 2
6 7 4 4 4 4 7 2
7 4 4 4 4 4 4 7
4 4 4 4 4 4 4 7
7 4 4 4 7 7 7 3
1 7 4 4 7 3 3 3
1 1 7 4 7 3 3 3
1 1 1 7 7 3 3 3
```
Expected Output:
```
1 1 7 4 4 7 6 6
1 7 4 4 4 4 7 6
7 4 4 4 4 4 4 7
4 4 4 4 4 4 4 7
7 4 4 4 7 7 7 2
3 7 4 4 7 2 2 2
3 3 7 4 7 2 2 2
3 3 3 7 7 2 2 2
```
Transformed Output:
```
3 3 7 4 4 7 1 1
3 7 4 4 4 4 7 1
7 4 4 4 4 4 4 7
4 4 4 4 4 4 4 7
7 4 4 4 7 7 7 6
2 7 4 4 7 6 6 6
2 2 7 4 7 6 6 6
2 2 2 7 7 6 6 6
```
Match: False
Pixels Off: 22
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 68.75

## Example 2:
Input:
```
1 1 7 4 4 7 6 6
1 7 4 4 4 7 6 6
7 4 4 4 4 7 6 6
9 7 4 4 4 7 6 6
9 9 7 4 4 7 6 6
9 9 9 7 4 7 6 6
9 9 9 9 7 7 6 6
9 9 9 9 9 7 6 6
```
Expected Output:
```
9 9 7 4 4 7 1 1
9 7 4 4 4 7 1 1
7 4 4 4 4 7 1 1
6 7 4 4 4 7 1 1
6 6 7 4 4 7 1 1
6 6 6 7 4 7 1 1
6 6 6 6 7 7 1 1
6 6 6 6 6 7 1 1
```
Transformed Output:
```
6 6 7 4 4 7 9 9
6 7 4 4 4 7 9 9
7 4 4 4 4 7 9 9
6 7 4 4 4 7 9 9
6 6 7 4 4 7 9 9
6 6 6 7 4 7 9 9
6 6 6 6 7 7 9 9
6 6 6 6 6 7 9 9
```
Match: False
Pixels Off: 19
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 59.375

## Example 3:
Input:
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
7 7 7 7 7 7 7 6
7 4 4 4 4 4 4 7
7 4 4 4 4 7 7 7
7 4 7 7 7 5 5 5
7 7 5 5 5 5 5 5
7 5 5 5 5 5 5 5
```
Expected Output:
```
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
7 7 7 7 7 7 7 5
7 4 4 4 4 4 4 7
7 4 4 4 4 7 7 7
7 4 7 7 7 6 6 6
7 7 6 6 6 6 6 6
7 6 6 6 6 6 6 6
```
Transformed Output:
```
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
6 6 6 6 6 6 6 5
6 4 4 4 4 4 4 7
6 4 4 4 4 7 7 7
6 4 7 7 7 6 6 6
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 40.625
## General Assessment

The previous code attempted to solve the task by identifying the connected components (blobs) originating from the four corners and swapping them diagonally (TL<->BR, TR<->BL), changing the color of the swapped blob to match the original color of the corner it was swapped *from*.

The execution results show this assumption was incorrect. The transformed outputs do not match the expected outputs, indicating the swap logic or the color assignment rule is wrong.

Specifically:
1.  **Incorrect Swap Pattern:** The examples suggest the movement or color assignment isn't a simple diagonal swap. The destination location for a color or blob seems to follow a different pattern, potentially conditional.
2.  **Incorrect Color Assignment:** The color assigned to a corner blob's location in the output does not consistently match the color of the diagonally opposite corner's original blob.

**Strategy for Resolution:**

1.  **Re-analyze Mappings:** Carefully examine the relationship between the input corner colors/blobs and the output corner colors/blobs across all three examples. Identify the source color for each corner location in the output.
2.  **Identify Controlling Factors:** Determine what factors influence the mapping (e.g., corner color values, equality between corner colors, shape properties).
3.  **Formulate Conditional Rule:** Develop a precise rule, potentially with conditions, that explains how the color of the blob at each corner location is determined in the output based on the input corner colors and shapes.
4.  **Refine Natural Language Program:** Update the program to reflect this new, more accurate rule.

## Metrics and Analysis

Let's analyze the corner colors and shapes for each example. We need the `find_connected_component` function.


