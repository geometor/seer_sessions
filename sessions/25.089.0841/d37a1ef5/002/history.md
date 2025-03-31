
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 5 0 0 0 0 2 0 0
0 2 0 0 5 0 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 5 0 2 2 2 2 0 0
0 2 2 0 5 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 0 5 0 0 5 0 2 0 0
0 2 0 0 0 5 0 0 2 0 0
0 2 0 0 0 0 0 0 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 5 0 0 5 2 2 0 0
0 2 2 0 0 5 0 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 0 0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 2 0
0 2 0 0 5 0 0 0 0 0 2 0
0 2 0 0 0 0 5 0 0 0 2 0
0 2 0 0 5 0 0 5 0 0 2 0
0 2 0 0 0 0 0 0 0 0 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 5 0 0 0 2 2 2 0
0 2 2 2 0 0 5 0 2 2 2 0
0 2 2 2 5 0 0 5 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Background:** The predominant background color is white (0).
2.  **Frame:** Each input grid contains a rectangular frame made of red (2) pixels. This frame is always hollow.
3.  **Internal Pixels:** Inside the red frame, there are pixels that are either white (0) or gray (5).
4.  **Transformation:** The core transformation involves changing the color of some pixels *inside* the red frame. Specifically, the white (0) pixels within the boundaries of the red frame are changed to red (2) in the output.
5.  **Preservation:** The red frame itself, the gray (5) pixels inside the frame, and the white (0) background *outside* the frame remain unchanged in the output.

**YAML Facts:**


```yaml
Observations:
  - Grid Structure:
      - Input and output grids have the same dimensions.
      - The background color is consistently white (0).
  - Objects:
      - A primary object is a rectangular frame composed of red (2) pixels.
      - Inside this frame, there are other pixels:
          - Some are white (0).
          - Some are gray (5). These appear as distinct single pixels or small groups.
  - Transformation:
      - The transformation acts specifically on the area *enclosed* by the red frame.
      - Pixels within the enclosed area that were originally white (0) are changed to red (2).
  - Invariants:
      - The red (2) frame pixels remain unchanged.
      - The gray (5) pixels inside the frame remain unchanged.
      - The white (0) pixels outside the frame remain unchanged.
  - Relationships:
      - The transformation depends on identifying the boundary defined by the red frame.
      - The color change (white to red) uses the same color as the frame.
      - The transformation distinguishes between the background color (white) and other non-frame colors (gray) within the enclosed area.
```


**Natural Language Program:**

1.  Identify the boundary of the contiguous red (2) shape (the frame) in the input grid.
2.  Determine the region enclosed by this red frame.
3.  Iterate through each pixel within the enclosed region.
4.  If a pixel within the enclosed region is white (0), change its color to red (2).
5.  Leave all other pixels (the red frame itself, any gray (5) pixels inside the frame, and all pixels outside the frame) unchanged.
6.  The resulting grid is the output.
```python
import numpy as np
from collections import deque

"""
Identifies the region enclosed by a red (2) frame and fills any white (0) pixels 
within that enclosed region with red (2), leaving the frame, gray (5) pixels 
inside the frame, and the background outside the frame unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the filling rule.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = input_np.copy()
    height, width = input_np.shape

    # Create a boolean grid to keep track of visited cells during flood fill
    visited = np.zeros_like(input_np, dtype=bool)
    # Queue for Breadth-First Search (BFS)
    queue = deque()

    # --- Step 1: Identify externally connected white (0) pixels using BFS (Flood Fill) ---
    # Start BFS from all white pixels on the border of the grid.
    # These are guaranteed to be outside any enclosed frame.
    for r in range(height):
        for c in [0, width - 1]: # Check first and last columns
            if input_np[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                queue.append((r, c))
    for c in range(width):
        for r in [0, height - 1]: # Check first and last rows (avoid double-checking corners)
             if input_np[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                queue.append((r, c))

    # Perform BFS to find all reachable white pixels from the outside
    while queue:
        r, c = queue.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) and hasn't been visited
                if input_np[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # --- Step 2: Fill the internal white pixels ---
    # Iterate through every cell in the grid
    for r in range(height):
        for c in range(width):
            # If a cell is white (0) and was *not* visited by the flood fill,
            # it must be inside the enclosed region.
            if input_np[r, c] == 0 and not visited[r, c]:
                # Change its color to red (2) in the output grid
                output_grid[r, c] = 2

    return output_grid.tolist() # Convert back to list of lists if necessary for the environment
```
