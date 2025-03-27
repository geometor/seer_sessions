import numpy as np
from collections import deque

"""
Determine the transformation rule from input to output grids.

1. Identify the 'target' color: This is the unique color in the input grid that is neither white (0) nor blue (1).
2. Identify 'outside' target pixels: These are target color pixels reachable from the grid border without crossing any blue (1) pixels. This is found using a Breadth-First Search (BFS) starting from all non-blue border cells. Only 4-directional adjacency (up, down, left, right) is considered.
3. Count the total number of target pixels (`total_target`) in the input grid.
4. Count the number of 'outside' target pixels (`count_outside`) found in step 2.
5. Calculate the number of 'inside' target pixels: `count_inside = total_target - count_outside`.
6. Determine the number of target pixels (`num_output_pixels`) to place in the 3x3 output grid: `num_output_pixels = count_inside`.
7. Create a 3x3 output grid initialized with white (0).
8. Fill the first `num_output_pixels` cells of the output grid (reading row by row, left to right) with the target color. Ensure the number does not exceed 9 (the size of the output grid).
9. Return the 3x3 output grid.
"""


def find_outside_pixels(grid, target_color, wall_color=1, background_color=0):
    """
    Finds pixels of target_color reachable from the border without crossing wall_color.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the pixels to find.
        wall_color (int): The color that acts as a barrier.
        background_color (int): The background color (typically 0).

    Returns:
        set: A set of coordinates (row, col) of the outside target pixels.
    """
    rows, cols = grid.shape
    visited = set()
    outside_target_pixels = set()
    queue = deque()

    # Add all non-wall border cells to the queue and mark as visited
    # Also, immediately check if these border cells are the target color
    for r in range(rows):
        # Left border
        if grid[r, 0] != wall_color and (r, 0) not in visited:
            queue.append((r, 0))
            visited.add((r, 0))
            if grid[r, 0] == target_color:
                outside_target_pixels.add((r, 0))
        # Right border
        if grid[r, cols - 1] != wall_color and (r, cols - 1) not in visited:
            queue.append((r, cols - 1))
            visited.add((r, cols - 1))
            if grid[r, cols - 1] == target_color:
                outside_target_pixels.add((r, cols - 1))

    for c in range(cols): # Use range(cols) to include corners correctly
        # Top border
        if grid[0, c] != wall_color and (0, c) not in visited:
            queue.append((0, c))
            visited.add((0, c))
            if grid[0, c] == target_color:
                outside_target_pixels.add((0, c))
        # Bottom border
        if grid[rows - 1, c] != wall_color and (rows - 1, c) not in visited:
            queue.append((rows - 1, c))
            visited.add((rows - 1, c))
            if grid[rows - 1, c] == target_color:
                outside_target_pixels.add((rows - 1, c))

    # Perform BFS using 4-directional neighbors
    while queue:
        r, c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-directional
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if visited or is a wall
                if (nr, nc) not in visited and grid[nr, nc] != wall_color:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    # Check if the newly visited cell is a target pixel
                    if grid[nr, nc] == target_color:
                        outside_target_pixels.add((nr, nc))

    return outside_target_pixels

def count_pixels(grid, color):
    """Counts the total number of pixels of a specific color."""
    return np.sum(grid == color)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 0
    wall_color = 1

    # 1. Identify the target color
    unique_colors = np.unique(input_np)
    target_color = -1
    for color in unique_colors:
        if color != background_color and color != wall_color:
            target_color = color
            break

    # Handle case where no target color is found
    if target_color == -1:
        return np.zeros((3, 3), dtype=int).tolist() # Return default 3x3 white grid

    # 2. Find outside target pixels
    outside_pixels_set = find_outside_pixels(input_np, target_color, wall_color, background_color)

    # 3. Count total target pixels
    total_target = count_pixels(input_np, target_color)

    # 4. Count outside target pixels
    count_outside = len(outside_pixels_set)

    # 5. Calculate inside target pixels
    count_inside = total_target - count_outside

    # 6. Determine the number of output pixels
    num_output_pixels = count_inside

    # Ensure num_output_pixels doesn't exceed 9 (max for 3x3 grid)
    num_output_pixels = min(num_output_pixels, 9)

    # 7. Create a 3x3 output grid initialized with background color
    output_grid = np.full((3, 3), background_color, dtype=int)

    # 8. Fill the output grid row by row
    output_pixels_placed = 0
    for r in range(3):
        for c in range(3):
            if output_pixels_placed < num_output_pixels:
                output_grid[r, c] = target_color
                output_pixels_placed += 1
            else:
                break # Stop filling once required number is reached
        if output_pixels_placed >= num_output_pixels:
             break # Stop outer loop as well

    # 9. Return the output grid as a list of lists
    return output_grid.tolist()