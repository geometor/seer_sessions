
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transforms an input grid based on pixel adjacency and propagation rules.

Rule: 
1. Identify all green pixels (3) that are orthogonally adjacent (up, down, left, right) 
   to at least one red pixel (2) in the input grid.
2. These identified green pixels, and any other green pixels (3) that are connected 
   to them through an orthogonal path consisting only of green pixels (3), 
   change to blue (1) in the output grid.
3. All other pixels (white (0), red (2), and green (3) pixels not part of the 
   propagated blue regions) retain their original colors from the input grid.
"""

def transform(input_grid):
    """
    Applies the adjacency and propagation transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input grid. 
    # Pixels will be changed in this grid as the rules are applied.
    output_grid = np.copy(input_np)

    # Queue for Breadth-First Search (BFS) to handle the propagation (flood fill).
    # It will store coordinates (row, column) of pixels to process.
    queue = deque()

    # --- Step 1: Identify Initial Blue Pixels ---
    # Iterate through each pixel of the input grid.
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is green (3).
            if input_np[r, c] == 3:
                is_adjacent_to_red = False
                # Define orthogonal neighbor offsets.
                neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
                
                # Check each orthogonal neighbor.
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    
                    # Ensure the neighbor is within the grid boundaries.
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is red (2) in the input grid.
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break  # Found a red neighbor, no need to check others for this green pixel.
                
                # If this green pixel is adjacent to a red one:
                if is_adjacent_to_red:
                    # Check if it hasn't already been marked blue (important if multiple red neighbors)
                    if output_grid[r, c] == 3: 
                        # Change this pixel to blue (1) in the output grid.
                        output_grid[r, c] = 1
                        # Add its coordinates to the queue to start the propagation from here.
                        queue.append((r, c))

    # --- Step 2: Propagate Blue Color (Flood Fill) ---
    # While there are pixels in the queue to process:
    while queue:
        # Get the coordinates of the next pixel from the front of the queue.
        r, c = queue.popleft()

        # Define orthogonal neighbor offsets again.
        neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Check each orthogonal neighbor for potential propagation.
        for dr, dc in neighbor_offsets:
            nr, nc = r + dr, c + dc

            # Ensure the neighbor is within the grid boundaries.
            if 0 <= nr < height and 0 <= nc < width:
                # Check two conditions for propagation:
                # 1. Was the neighbor originally green (3) in the input grid?
                # 2. Is the neighbor still marked as green (3) in the output grid? 
                #    (This implicitly checks if it hasn't been visited/changed to blue yet).
                if input_np[nr, nc] == 3 and output_grid[nr, nc] == 3:
                    # If both conditions are true, change the neighbor to blue (1) in the output grid.
                    output_grid[nr, nc] = 1
                    # Add the neighbor's coordinates to the queue to process its neighbors later.
                    queue.append((nr, nc))

    # --- Step 3: Finalize Output ---
    # Pixels that were not green, or were green but not connected to a red-adjacent 
    # green pixel, retain their original values because we started with a copy.
    # Convert the final numpy array back to a list of lists as required.
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 2 3 3 3 0 0 0 0 3 3 3 3 3
0 0 2 3 3 3 3 3 3 2 3 0 0 0 2 3 3 2 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 2 3 3 3 0 2 0 0 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 2
0 0 3 2 3 3 3 3 3 3 3 0 0 0 0 3 3 3 3 3
0 0 3 3 3 3 3 2 3 3 3 0 0 2 0 2 3 3 3 3
0 0 2 3 3 3 3 3 3 3 3 0 2 0 0 3 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 2 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 2 3 3 3 0 2 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 2 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 2 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 2 3 3 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3 3
0 0 3 3 3 3 1 1 1 3 3 0 0 0 0 3 3 3 3 3
0 1 1 1 3 3 1 2 1 1 1 0 0 0 0 3 1 1 1 3
0 1 2 1 3 3 1 1 1 2 1 0 0 0 2 3 1 2 1 3
0 1 1 1 3 3 1 1 1 1 1 0 0 0 0 3 1 1 1 3
0 0 3 3 3 3 1 2 1 3 3 0 2 0 0 3 3 3 3 3
0 0 3 3 3 3 1 1 1 3 3 0 0 0 0 3 3 3 1 1
0 0 1 1 1 3 3 3 3 3 3 0 0 0 0 3 3 3 1 2
0 0 1 2 1 3 1 1 1 3 3 0 0 0 1 1 1 3 1 1
0 1 1 1 1 3 1 2 1 3 3 0 0 2 1 2 1 3 3 3
0 1 2 1 3 3 1 1 1 3 3 0 2 0 1 1 1 3 3 3
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 3 3 3 3 3
0 2 0 3 3 3 3 3 1 1 1 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 1 2 1 1 1 0 2 0 0 0 0 0
0 0 0 3 3 3 1 1 1 1 1 2 1 0 0 0 0 0 0 0
0 0 0 3 3 3 1 2 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 3 3 3 1 1 1 1 2 1 3 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 1 1 1 1 1
0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1
0 0 1 1 1 1 1 2 1 1 1 0 0 0 0 1 1 1 1 1
0 0 2 1 1 1 1 1 1 2 1 0 0 0 2 1 1 2 1 1
0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1
0 0 1 1 1 1 1 2 1 1 1 0 2 0 0 1 1 1 1 1
0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1
0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 2
0 0 1 2 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1
0 0 1 1 1 1 1 2 1 1 1 0 0 2 0 2 1 1 1 1
0 0 2 1 1 1 1 1 1 1 1 0 2 0 0 1 1 1 1 1
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1
0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1
0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1
0 2 0 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 2 1 1 1 0 2 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 2 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 2 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 2 1 1 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 142
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 71.0

## Example 2:
Input:
```
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 2 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 2 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0
2 0 2 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 2 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 2 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 3 3 3 3 3 3 3 3 2 0 0 0
0 0 0 0 0 0 0 0 3 3 2 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 3 3 3 2 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 3 2 3 3 3 3 3 3 3 2 0 0
```
Expected Output:
```
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 1 1 1 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 3 1 2 1 3 3 1 1 1 3 3 3 0 0 0 0 0
0 0 0 3 1 1 1 3 3 1 2 1 3 1 1 1 0 0 0 0
0 0 0 3 3 3 3 3 3 1 1 1 3 1 2 1 0 0 0 0
2 0 2 1 1 1 3 3 3 3 3 3 3 1 1 1 0 0 0 0
0 0 0 1 2 1 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 1 1 1 3 3 3 3 3 3 3 3 3 0 2 0 0 0
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 1 2 1 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 2 0 1 1 1 3 3 3 3 3 1 1 1 0 0
0 0 0 0 0 0 2 0 3 1 1 1 3 3 3 1 2 1 0 0
0 0 0 0 0 0 0 0 3 1 2 1 1 3 3 1 1 1 0 0
0 0 0 0 0 0 0 0 3 1 1 2 1 3 3 3 3 0 0 0
0 0 0 0 0 2 0 0 1 1 1 1 1 3 3 3 3 0 0 0
0 0 0 0 0 0 2 0 1 2 1 3 3 3 3 3 3 2 0 0
```
Transformed Output:
```
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 1 1 2 1 1 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 2 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 1 1 2 0 0 0 0 0
2 0 2 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 1 2 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 2 0 0 0
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 1 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 2 0 0 1 1 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 2 0 1 1 1 1 1 1 1 1 2 0 0 0
0 0 0 0 0 0 0 0 1 1 2 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 1 1 1 2 1 1 1 1 1 0 0 0
0 0 0 0 0 2 0 0 1 1 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 2 0 1 2 1 1 1 1 1 1 1 2 0 0
```
Match: False
Pixels Off: 108
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 54.0

## Example 3:
Input:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 2 0 0 0 0 3 3 3 3 3 2 0 0
0 3 3 3 3 0 0 0 0 3 3 3 3 3 3 0 0
0 3 3 3 3 0 0 0 0 3 2 2 3 3 3 0 0
0 2 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 3 3 1 1 1 0 0 0 0 0 0 0 1 1 1 0
0 3 3 1 2 1 0 0 0 3 3 3 3 1 2 1 0
0 3 3 1 1 1 0 0 0 1 1 1 1 1 1 1 0
0 3 3 3 3 0 0 0 0 1 2 2 1 3 3 0 0
0 2 0 0 0 0 0 0 0 1 1 1 1 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 2 0 0 0 0 1 1 1 1 1 2 0 0
0 1 1 1 1 0 0 0 0 1 1 1 1 1 1 0 0
0 1 1 1 1 0 0 0 0 1 2 2 1 1 1 0 0
0 2 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.64705882352942
