
Previous Code:
```python
import copy
import collections

# Define color constants for clarity
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3

def transform(input_grid):
    """
    Performs a constrained flood fill. Finds the region containing the initial 
    red pixel (2) that is enclosed by blue (1), green (3), or grid boundaries. 
    Fills all white (0) pixels within this enclosed region with red (2). 
    Other pixels (blue, green, original red) remain unchanged.

    The process involves:
    1. Identifying all white pixels reachable from the grid border (external region).
    2. Identifying all white pixels *not* reachable from the border (internal region).
    3. Changing the color of the internal white pixels to red in the output grid.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Set to keep track of visited coordinates during the external flood fill
    # These are the white pixels reachable from the outside border.
    external_visited = set()
    
    # Queue for Breadth-First Search (BFS) starting from border white pixels
    queue = collections.deque()
    
    # Initialize the queue with all white pixels on the border
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on the border
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                # Check if the border pixel is white and not already visited
                if input_grid[r][c] == WHITE and (r, c) not in external_visited:
                    external_visited.add((r, c))
                    queue.append((r, c))

    # Define orthogonal directions (right, left, down, up)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform BFS to find all white pixels reachable from the border
    while queue:
        current_row, current_col = queue.popleft()
        
        # Explore neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = current_row + dr, current_col + dc
            neighbor_coord = (neighbor_row, neighbor_col)
            
            # Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
                # Check if the neighbor is white in the input grid and hasn't been visited yet
                if input_grid[neighbor_row][neighbor_col] == WHITE and neighbor_coord not in external_visited:
                    # Mark neighbor as visited (part of the external white region)
                    external_visited.add(neighbor_coord)
                    # Add neighbor to the queue to explore from it
                    queue.append(neighbor_coord)

    # Iterate through the grid to fill the internal white pixels
    for r in range(height):
        for c in range(width):
            # Check if the pixel in the input grid is white
            if input_grid[r][c] == WHITE:
                # Check if this white pixel was *not* reached by the external fill
                if (r, c) not in external_visited:
                    # This is an internal white pixel, change it to red in the output grid
                    output_grid[r][c] = RED
                    
    # The original red pixel, blue pixels, and green pixels are preserved 
    # because they were either not white (so skipped in the final loop) 
    # or part of the initial copy. The original red pixel will naturally be 
    # part of the "internal" area if enclosed, and since it's not white, 
    # the final loop won't attempt to change it.

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 1 1 1 2 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0
0 0 1 1 1 0 1 1 1 2 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 3 3 3 0 3 3 3 2 3 3 3
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 2 2 0 0 0
0 0 3 3 3 0 2 3 3 3 0 0
0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 1 1 1 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 2 3 3 3 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0
0 0 0 2 3 3 3 0 3 3 3 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 3 3 3 0 0 0 0 3 3
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 38
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.787878787878782

## Example 2:
Input:
```
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 3 3 3 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
1 1 1 2 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 1 1 1 2 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
1 1 0 0 1 1 1 2 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 2 2 2 2 0 0 0 0
0 0 0 0 2 3 3 3 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 2 3 3 3 0 3 3 3 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 1 1 1 2 0 1 1 1 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 36
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 27.27272727272728

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
2 0 0 3 0 0 1 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 1 0 0 3 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 2 2 2 2 3 0 0 0 0 0 0 0 0 0
2 2 2 3 0 2 1 0 2 3 0 0 0 0 0 0 0 0 0
0 0 2 3 0 2 1 0 2 3 0 0 3 0 0 0 0 0 0
0 0 2 2 2 2 1 0 2 2 2 2 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
2 0 0 3 0 0 1 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 1 0 0 3 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 28
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 22.672064777327932

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 1 0
2 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 0 1 0 0 0 3 0 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 2 1 0
2 2 2 2 2 2 3 0 2 2 2 2 2 3 0 0 2 2 2 2 1 0
0 0 0 0 0 2 3 0 2 1 0 0 2 3 0 0 2 1 0 0 1 0
0 0 0 0 0 2 2 2 2 1 0 0 2 2 2 2 2 1 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 1 0
2 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 1 0
0 0 0 0 0 0 3 0 0 1 0 0 0 3 0 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 31
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 23.4848484848485
**General Assessment & Strategy**

The previous code failed because it did not correctly identify the pixels to be filled. It used an "outside-in" approach (finding white pixels reachable from the border) rather than an "inside-out" approach (spreading from the initial red pixel). The metrics confirm that in all examples, the input contains exactly one red pixel, and the output contains significantly more red pixels, while the counts of blue and green pixels remain unchanged. The number of white pixels decreases by the same amount that the red pixels increase, confirming that only white pixels are being filled with red. The transformed output from the previous code is identical to the input in terms of pixel values, indicating the filling condition was never met.

The strategy is to implement a flood fill algorithm that starts specifically from the initial red pixel(s) found in the input grid. This fill should propagate through adjacent white pixels (orthogonally) and stop at grid boundaries or any non-white pixels (specifically blue or green, though stopping at any non-white pixel is sufficient and simpler).

**Metrics Analysis**

-   **Grid Shapes:** Input and output shapes are consistent for each example. The failed code also preserved the shape.
-   **Color Counts:**
    -   Inputs consistently have 1 red pixel (color 2).
    -   Outputs have many more red pixels (39, 37, 29, 32).
    -   The number of white pixels (color 0) decreases in the output by exactly the increase in red pixels (`pixels_filled = output_red_count - input_red_count`; `output_white_count = input_white_count - pixels_filled`).
    -   The counts of blue (1) and green (3) pixels are identical between input and output.
    -   The failed transformed output has identical color counts to the input.
-   **Initial Red Location:** Each input has a single starting red pixel.
-   **Pixels Off:** The number of pixels off in the failed transformation corresponds exactly to the number of white pixels that *should* have been filled red (`pixels_off = output_red_count - input_red_count`).

**Facts (YAML)**


```yaml
Task: Constrained Flood Fill from Red Pixel

Priors:
  - Objectness: Pixels of the same color form contiguous regions. White (0) areas are distinct from Red (2), Blue (1), and Green (3) areas.
  - Geometry & Topology: The transformation involves connectivity (adjacency) and containment (being blocked by barriers). Grid boundaries also act as barriers.

Input Grid:
  - Contains pixels of colors White (0), Blue (1), Red (2), and Green (3).
  - Contains exactly one Red (2) pixel which acts as the seed/origin for the transformation.
  - Contains Blue (1) and Green (3) pixels which form barriers.
  - Contains White (0) pixels which are the target for filling.

Output Grid:
  - Same dimensions as the input grid.
  - Preserves the location and color of the original Red (2), Blue (1), and Green (3) pixels from the input.
  - Some White (0) pixels from the input are changed to Red (2).

Transformation Rule (Action):
  - Identify the location of the initial Red (2) pixel(s).
  - Perform a flood fill starting from these initial Red pixel(s).
  - The fill spreads orthogonally (up, down, left, right) to adjacent pixels.
  - The fill propagates *only* through White (0) pixels.
  - The fill is blocked by Blue (1) pixels, Green (3) pixels, and the grid boundaries.
  - All White (0) pixels reachable by this flood fill are changed to Red (2) in the output grid.
  - Pixels that are not White (0) or are White (0) but not reachable from the initial Red pixel via other White pixels are unchanged.
```


**Natural Language Program**

1.  Create a copy of the input grid to serve as the output grid.
2.  Find the coordinates (row, column) of all Red (2) pixels in the input grid. These are the starting points for the fill.
3.  Initialize a queue for a Breadth-First Search (BFS) or stack for Depth-First Search (DFS) with the coordinates of the initial Red pixel(s).
4.  Initialize a set or boolean grid to keep track of visited coordinates to avoid cycles and redundant processing. Add the initial Red pixel coordinates to the visited set.
5.  While the queue/stack is not empty:
    a.  Dequeue/Pop a coordinate `(r, c)`.
    b.  Examine its four orthogonal neighbors (up, down, left, right): `(nr, nc)`.
    c.  For each neighbor:
        i.  Check if `(nr, nc)` is within the grid boundaries.
        ii. Check if `(nr, nc)` has already been visited.
        iii. Check if the pixel at `(nr, nc)` in the *input* grid is White (0).
        iv. If the neighbor is within bounds, not visited, and is White (0) in the input:
            1.  Change the color of the pixel at `(nr, nc)` in the *output* grid to Red (2).
            2.  Mark `(nr, nc)` as visited.
            3.  Enqueue/Push `(nr, nc)` to continue the fill from this neighbor.
6.  Return the modified output grid.**General Assessment & Strategy**

The previous code failed because its core logic was incorrect for the task. It attempted to find enclosed white areas by identifying white pixels connected to the border and then filling the *rest* of the white pixels. However, the task requires a direct flood fill *originating* from the specific red pixel(s) present in the input. The fill should spread only through white pixels and be stopped by blue, green, or boundary pixels.

The metrics gathered confirm this:
1.  Each input has exactly one red pixel.
2.  The output shows the red color spreading from this initial pixel.
3.  The spread fills only white pixels.
4.  Blue and green pixels act as barriers and remain unchanged.
5.  The number of incorrect pixels in the failed output exactly matches the number of white pixels that should have been turned red.

The strategy is to implement a standard flood fill (like BFS or DFS) starting from the initial red pixel(s). The fill algorithm will explore adjacent white pixels, changing them to red in the output grid, and stop exploring paths blocked by non-white pixels or grid boundaries.

**Metrics Analysis**

*   **Grid Shapes:** Consistently maintained between input and output.
*   **Color Counts:**
    *   Input Red (2): Always 1.
    *   Output Red (2): Significantly increased (39, 37, 29, 32).
    *   Input White (0): High count.
    *   Output White (0): Decreased count, matching the increase in red pixels.
    *   Input/Output Blue (1) & Green (3): Counts remain identical.
*   **Initial Red Location:** Confirmed a single starting point in each input.
*   **Pixels Off (Previous Code):** The difference between the failed output and the expected output corresponds precisely to the white pixels that needed filling (`output_red_count - input_red_count`).

**Facts (YAML)**


```yaml
Task: Flood Fill from Red Seed

Input_Objects:
  - Type: Grid
    Properties:
      - Contains pixels of colors: White (0), Blue (1), Red (2), Green (3).
  - Type: Seed Pixel
    Properties:
      - Color: Red (2)
      - Count: Exactly 1 per input grid.
      - Role: Origin point for the fill action.
  - Type: Barrier Pixels
    Properties:
      - Color: Blue (1) or Green (3)
      - Role: Block the spread of the fill action.
  - Type: Fillable Pixels
    Properties:
      - Color: White (0)
      - Role: Can be changed to Red (2) by the fill action if reachable.
  - Type: Boundary
    Properties:
      - Location: Edges of the grid.
      - Role: Block the spread of the fill action.

Output_Objects:
  - Type: Grid
    Properties:
      - Same dimensions as the input grid.
      - Contains the original Barrier Pixels (Blue, Green) and the original Seed Pixel (Red) in their initial locations.
      - Contains some former Fillable Pixels (White) that are now Red (2).
      - Contains remaining Fillable Pixels (White) that were not reached by the fill.

Action:
  - Name: Constrained Flood Fill
  - Start Condition: Begins at the location(s) of the Seed Pixel(s) (Red).
  - Propagation: Spreads orthogonally (up, down, left, right) to adjacent pixels.
  - Constraint - Medium: Can only spread *through* Fillable Pixels (White).
  - Constraint - Blocking: Spread stops upon encountering Barrier Pixels (Blue, Green), already filled pixels, or the Grid Boundary.
  - Effect: Changes the color of all reachable Fillable Pixels (White) to the Seed Pixel color (Red).
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the coordinates `(r, c)` of all Red (2) pixels in the input grid.
3.  Create a queue data structure and add all initial Red pixel coordinates to it.
4.  Create a set or 2D array to keep track of visited coordinates, initially marking the starting Red pixel(s) as visited.
5.  While the queue is not empty:
    a.  Dequeue a coordinate `(row, col)`.
    b.  For each of its four orthogonal neighbors `(next_row, next_col)`:
        i.  Check if `(next_row, next_col)` is within the grid boundaries.
        ii. Check if `(next_row, next_col)` has already been visited.
        iii. Check if the pixel at `(next_row, next_col)` in the *input* grid is White (0).
        iv. If the neighbor is valid (within bounds, not visited, and is White):
            1.  Set the pixel at `(next_row, next_col)` in the *output* grid to Red (2).
            2.  Mark `(next_row, next_col)` as visited.
            3.  Enqueue `(next_row, next_col)`.
6.  Return the final output grid.
