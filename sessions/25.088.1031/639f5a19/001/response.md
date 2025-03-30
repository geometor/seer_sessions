```python
import numpy as np
from collections import deque

"""
Transforms an input grid by finding all rectangular blocks of azure (8) pixels. 
Each azure block is replaced with a patterned block of the same dimensions. 
The pattern consists of a central yellow (4) rectangle (if the block is large enough) 
surrounded by a border region divided into four quadrants: top-left is magenta (6), 
top-right is blue (1), bottom-left is red (2), and bottom-right is green (3). 
The central yellow region starts at relative row/column index 2 and ends at relative 
row/column index H-3/W-3. The quadrants are divided based on the integer division 
midpoints of the block's height and width. Pixels outside the azure blocks remain unchanged.
"""

def find_azure_blocks(grid):
    """
    Finds all contiguous rectangular blocks of a specific color (azure=8).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block
              and contains 'r', 'c' (top-left coordinates), 'h' (height),
              and 'w' (width).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    target_color = 8 # Azure

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Found the start of a potential block
                q = deque([(r, c)])
                visited[r, c] = True
                block_pixels = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Use BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            block_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                # Check if the found region is a solid rectangle
                block_h = max_r - min_r + 1
                block_w = max_c - min_c + 1
                is_rectangle = True
                if len(block_pixels) != block_h * block_w:
                    is_rectangle = False
                else:
                    # Double check all pixels within the bounding box are the target color
                    for br in range(min_r, max_r + 1):
                        for bc in range(min_c, max_c + 1):
                            if grid[br, bc] != target_color:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break
                
                if is_rectangle:
                    blocks.append({'r': min_r, 'c': min_c, 'h': block_h, 'w': block_w})

    return blocks


def transform(input_grid):
    """
    Applies the patterned transformation to azure blocks in the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all azure rectangular blocks
    azure_blocks = find_azure_blocks(input_grid)

    # Define colors
    magenta = 6
    blue = 1
    red = 2
    green = 3
    yellow = 4

    # Process each block
    for block in azure_blocks:
        R, C = block['r'], block['c']
        H, W = block['h'], block['w']

        # Calculate relative midpoints for quadrant division
        mid_row_rel = H // 2 
        mid_col_rel = W // 2

        # Calculate relative boundaries for the central yellow region
        # Note: indices are 0-based
        r_start_yellow = 2
        r_end_yellow = H - 1 - 2  # Inclusive end index relative to block start
        c_start_yellow = 2
        c_end_yellow = W - 1 - 2  # Inclusive end index relative to block start

        # Iterate through each cell within the block's area
        for r_rel in range(H):
            for c_rel in range(W):
                # Absolute coordinates in the grid
                r_abs = R + r_rel
                c_abs = C + c_rel

                # Determine the color based on relative position
                color = 0 # Default color (should be overwritten)

                # Check if within the central yellow region
                if (r_start_yellow <= r_rel <= r_end_yellow) and \
                   (c_start_yellow <= c_rel <= c_end_yellow):
                    color = yellow
                else:
                    # Determine quadrant for border region
                    if r_rel < mid_row_rel: # Top half
                        if c_rel < mid_col_rel: # Left half
                            color = magenta
                        else: # Right half
                            color = blue
                    else: # Bottom half
                        if c_rel < mid_col_rel: # Left half
                            color = red
                        else: # Right half
                            color = green

                # Update the output grid
                output_grid[r_abs, c_abs] = color

    return output_grid
```