```python
import numpy as np
from collections import deque

"""
Identifies hollow rectangular frames in the input grid and fills their interior.
For each frame found:
1. Determine the color of the frame.
2. Define the rectangular region strictly inside the frame.
3. For every pixel within this interior region:
    If the pixel's original color (from the input grid) is not white (0), 
    change its color in the output grid to the frame's color.
Pixels on the frame itself or outside any frame remain unchanged.
White pixels inside frames also remain unchanged.
"""

def _find_frames(grid):
    """
    Finds all hollow rectangular frames made of a single non-white color in the grid.

    A hollow rectangular frame is defined as:
    - A connected component of a single non-white color.
    - The component's pixels perfectly form the perimeter of its bounding box.
    - The bounding box must have height > 1 and width > 1.
    - The area strictly inside the bounding box must contain at least one pixel
      that is *not* the frame's color (ensuring hollowness).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents a frame:
              (frame_color, min_row, min_col, max_row, max_col)
    """
    frames = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool) # Keep track of pixels already assigned to a component

    for r in range(height):
        for c in range(width):
            # Start search if pixel is non-white and not part of a previously found component
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                component_pixels = set() # Store pixels belonging to this component
                q = deque([(r, c)])      # Queue for BFS
                visited[r, c] = True     # Mark starting pixel as visited
                min_r, min_c = r, c      # Initialize bounding box
                max_r, max_c = r, c

                # --- Step 1: Find the connected component using BFS ---
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels.add((curr_r, curr_c))
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, color match, and if visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True # Mark neighbor visited
                            q.append((nr, nc))     # Add to queue

                # --- Step 2: Validate if the component is a hollow rectangular frame ---
                
                # Basic dimension check: must be larger than a line
                if not ((max_r - min_r) > 0 and (max_c - min_c) > 0):
                    continue # Not a potential frame with an interior

                is_perfect_perimeter = True
                is_hollow = False
                
                # Check all pixels within the bounding box
                for i in range(min_r, max_r + 1):
                    for j in range(min_c, max_c + 1):
                        is_on_perimeter = (i == min_r or i == max_r or j == min_c or j == max_c)
                        
                        if is_on_perimeter:
                            # Check 1: All perimeter pixels must be part of the component
                            if (i, j) not in component_pixels:
                                is_perfect_perimeter = False
                                break
                        else: # Pixel is in the interior
                            # Check 2: Interior pixels must NOT be part of the component
                            if (i, j) in component_pixels:
                                is_perfect_perimeter = False
                                break
                            # Check 3: At least one interior pixel must differ from frame color for hollowness
                            if grid[i,j] != color:
                                is_hollow = True
                                
                    if not is_perfect_perimeter:
                        break # Exit outer loop if perfection check fails

                # If it forms a perfect perimeter and is hollow, it's a valid frame
                if is_perfect_perimeter and is_hollow:
                    frames.append((color, min_r, min_c, max_r, max_c))

    return frames


def transform(input_grid):
    """
    Identifies hollow rectangular frames in the input grid and fills their interior.
    For each frame found: determines the frame's color, defines the interior region,
    and changes any non-white pixel within that interior region to the frame's color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid_np = np.copy(input_grid_np)

    # Find all valid hollow rectangular frames in the input grid
    frames = _find_frames(input_grid_np)

    # Process each found frame
    for frame_color, r1, c1, r2, c2 in frames:
        # Iterate through the coordinates strictly *inside* the frame's perimeter
        # Interior rows: r1 + 1 to r2 (exclusive of r2)
        # Interior columns: c1 + 1 to c2 (exclusive of c2)
        for r in range(r1 + 1, r2):
            for c in range(c1 + 1, c2):
                # Check the color of the pixel in the *original* input grid
                original_color = input_grid_np[r, c]
                
                # If the original pixel was not white (0)
                if original_color != 0:
                    # Change the corresponding pixel in the output grid to the frame's color
                    output_grid_np[r, c] = frame_color

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
```