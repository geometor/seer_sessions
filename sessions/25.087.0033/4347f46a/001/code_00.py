import numpy as np
from collections import deque

"""
Identifies solid rectangular shapes of non-background colors (any color other than white/0) 
in the input grid. For each identified solid rectangle, it replaces the interior pixels 
(pixels not on the outermost border of the rectangle) with the background color (white/0), 
effectively "hollowing" out the rectangle while preserving its 1-pixel thick border. 
Pixels that are not part of any identified solid rectangle remain unchanged.
"""

def _find_solid_rectangles(grid):
    """
    Helper function to find all solid rectangular regions of non-background colors.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents a rectangle
              (min_r, min_c, max_r, max_c, color). Returns an empty list
              if no solid rectangles are found.
    """
    rows, cols = grid.shape
    visited = set()
    rectangles = []
    background_color = 0 # Define background color

    for r in range(rows):
        for c in range(cols):
            # Check if pixel is non-background and not yet visited (part of a found component)
            if grid[r, c] != background_color and (r, c) not in visited:
                target_color = grid[r, c]
                component_pixels = []
                # Use a queue for Breadth-First Search (BFS) to find the connected component
                q = deque([(r, c)])
                visited.add((r, c))
                # Keep track of the component's boundaries
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform BFS
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels.append((curr_r, curr_c))
                    # Update boundaries
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor has the same color and hasn't been visited
                            if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))

                # After finding the component, check if it forms a solid rectangle
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                is_solid_rectangle = True

                # Condition 1: The number of pixels in the component must equal the area of the bounding box
                if len(component_pixels) != height * width:
                    is_solid_rectangle = False
                else:
                    # Condition 2: Verify all pixels within the bounding box actually belong to the component
                    # (This ensures there are no holes or the shape isn't irregular within its bounds)
                    # Note: This check might be slightly redundant if BFS guarantees finding all connected
                    # pixels, but it adds robustness against potentially complex edge cases or assumptions.
                    for check_r in range(min_r, max_r + 1):
                        for check_c in range(min_c, max_c + 1):
                            if grid[check_r, check_c] != target_color:
                                # Found a pixel within the bounds that doesn't match the color
                                is_solid_rectangle = False
                                break
                        if not is_solid_rectangle:
                            break
                
                # If both conditions are met, it's a solid rectangle
                if is_solid_rectangle:
                    rectangles.append((min_r, min_c, max_r, max_c, target_color))

    return rectangles

def transform(input_grid):
    """
    Transforms the input grid by hollowing out solid rectangles.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(input_np)
    background_color = 0

    # Find all solid rectangular objects in the input grid
    solid_rectangles = _find_solid_rectangles(input_np)

    # Process each identified solid rectangle
    for min_r, min_c, max_r, max_c, color in solid_rectangles:
        # Iterate through the pixels *inside* the bounding box, excluding the border.
        # The inner rows range from min_r + 1 up to (but not including) max_r.
        # The inner columns range from min_c + 1 up to (but not including) max_c.
        # Note: If height or width is <= 2, the corresponding range will be empty,
        # correctly handling thin rectangles with no interior.
        for r in range(min_r + 1, max_r):
             for c in range(min_c + 1, max_c):
                # Set the interior pixel to the background color
                output_grid[r, c] = background_color

    # Convert the resulting numpy array back to a list of lists for the standard output format
    return output_grid.tolist()