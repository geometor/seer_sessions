```python
import numpy as np

"""
Transforms input grids by finding azure rectangular blocks and replacing
them with a specific multi-colored pattern based on internal coordinates.
The pattern has a 2-pixel border with colors determined by quadrants
(top-left: magenta(6), top-right: blue(1), bottom-left: red(2), bottom-right: green(3))
and a yellow(4) center.
"""

def find_azure_rectangles(grid):
    """
    Finds all contiguous rectangular blocks of azure (8) pixels.

    Assumes blocks are solid rectangles, as seen in the examples.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple represents a block's
        bounding box: (r_min, c_min, height, width).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []
    azure_color = 8

    for r in range(rows):
        for c in range(cols):
            # Check if it's an azure pixel and hasn't been visited yet
            if grid[r, c] == azure_color and not visited[r, c]:
                # Found the top-left corner of a potential new block
                q = [(r, c)]
                visited[r, c] = True
                block_coords = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Use Breadth-First Search (BFS) to find all connected azure pixels
                # belonging to this block and determine its bounds.
                head = 0
                while head < len(q):
                    curr_r, curr_c = q[head]
                    head += 1

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check neighbors (4-directional connectivity is sufficient)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == azure_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            block_coords.add((nr, nc))

                # Calculate height and width from min/max coords
                height = max_r - min_r + 1
                width = max_c - min_c + 1

                # Check if the number of found pixels matches the bounding box area
                # This confirms it's a solid rectangle (as per examples)
                if len(block_coords) == height * width:
                    rectangles.append((min_r, min_c, height, width))
                # else: handle non-rectangular shapes if necessary, but not needed for this task

    return rectangles


def transform_block(grid, r0, c0, H, W):
    """
    Applies the color pattern transformation to a specific block within the grid.
    Modifies the grid in place.

    Args:
        grid: The numpy array grid to modify.
        r0: Top row index of the block.
        c0: Left column index of the block.
        H: Height of the block.
        W: Width of the block.
    """
    # Define colors and border thickness
    MAGENTA = 6
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    BORDER_THICKNESS = 2

    # Calculate midpoints using integer division
    mid_h = H // 2 # Midpoint row index (relative to block)
    mid_w = W // 2 # Midpoint col index (relative to block)

    # Iterate through each pixel within the block's bounding box
    for r_local in range(H): # Local row index within the block (0 to H-1)
        for c_local in range(W): # Local col index within the block (0 to W-1)
            # Calculate global grid coordinates
            row = r0 + r_local
            col = c0 + c_local
            
            color_to_set = -1 # Default/error color

            # Determine the output color based on local coordinates (r_local, c_local)
            # The order of these checks is important.
            if r_local < BORDER_THICKNESS:
                # Pixel is in the Top border rows (first T rows)
                color_to_set = MAGENTA if c_local < mid_w else BLUE
            elif r_local >= H - BORDER_THICKNESS:
                # Pixel is in the Bottom border rows (last T rows)
                color_to_set = RED if c_local < mid_w else GREEN
            elif c_local < BORDER_THICKNESS:
                # Pixel is in the Left border columns (first T columns)
                # Excludes pixels already colored by Top/Bottom border checks
                color_to_set = MAGENTA if r_local < mid_h else RED
            elif c_local >= W - BORDER_THICKNESS:
                # Pixel is in the Right border columns (last T columns)
                # Excludes pixels already colored by Top/Bottom/Left border checks
                color_to_set = BLUE if r_local < mid_h else GREEN
            else:
                # Pixel is in the Central region
                color_to_set = YELLOW

            # Update the grid pixel with the determined color
            grid[row, col] = color_to_set


def transform(input_grid_list):
    """
    Transforms input grids by finding azure rectangular blocks and replacing
    them with a specific multi-colored pattern based on internal coordinates.
    The pattern has a 2-pixel border with colors determined by quadrants
    (top-left: magenta(6), top-right: blue(1), bottom-left: red(2), bottom-right: green(3))
    and a yellow(4) center.
    """
    # Convert list of lists to numpy array for efficient manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Initialize output_grid as a copy of the input grid. We will modify this copy.
    output_grid = np.copy(input_grid)
    
    # 1. Find all distinct, contiguous rectangular blocks of azure pixels in the input.
    azure_blocks = find_azure_rectangles(input_grid)

    # 2. For each identified azure block:
    for r0, c0, H, W in azure_blocks:
        # 3. Apply the pattern transformation to this block's area in the output grid.
        #    The transform_block function modifies output_grid directly.
        transform_block(output_grid, r0, c0, H, W)

    # 4. Return the modified output grid, converted back to a list of lists.
    return output_grid.tolist()
```