import numpy as np
from collections import deque

"""
Transforms the input grid based on the following rule:
1. Identify all connected components of white (0) pixels in the input grid. Connectivity is defined by orthogonal adjacency. Movement between white pixels is blocked by gray (5), azure (8), blue (1), and the grid boundaries.
2. Identify the locations of all initial blue (1) pixels in the input grid.
3. For each connected component of white pixels, check if any pixel within that component is orthogonally adjacent to any of the initial blue (1) pixels.
4. If a white component is adjacent to an initial blue pixel, change all pixels belonging to that component to blue (1) in the output grid.
5. Pixels that were initially blue (1), gray (5), or azure (8) remain unchanged in the output grid. White components not adjacent to any initial blue pixel also remain unchanged (white).
"""

def transform(input_grid):
    """
    Fills connected components of white pixels if they are adjacent to an initial blue pixel.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define colors
    white = 0
    blue = 1
    gray = 5
    azure = 8
    boundary_colors = {gray, azure, blue} # Blue is also a boundary for white components

    # Find initial blue pixel locations
    initial_blue_locations = set(tuple(coord) for coord in np.argwhere(input_np == blue))

    # Keep track of visited white pixels during component finding
    visited_white = np.zeros_like(input_np, dtype=bool)
    
    # List to store coordinates of pixels in components that should be filled blue
    pixels_to_fill = []

    # Iterate through each cell to find connected components of white pixels
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited yet, start BFS to find its component
            if input_np[r, c] == white and not visited_white[r, c]:
                component_pixels = set()
                is_adjacent_to_blue = False
                queue = deque([(r, c)])
                visited_white[r, c] = True
                component_pixels.add((r, c))

                while queue:
                    curr_r, curr_c = queue.popleft()

                    # Check adjacency to initial blue pixels for the current pixel
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width:
                            if (nr, nc) in initial_blue_locations:
                                is_adjacent_to_blue = True
                                # No need to break here, continue BFS to find the whole component

                    # Explore neighbors for BFS (only add unvisited white pixels)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is white and not visited
                            if input_np[nr, nc] == white and not visited_white[nr, nc]:
                                visited_white[nr, nc] = True
                                queue.append((nr, nc))
                                component_pixels.add((nr, nc))
                
                # After BFS for the component is complete, if it was adjacent to blue, mark its pixels for filling
                if is_adjacent_to_blue:
                    pixels_to_fill.extend(list(component_pixels))

    # Fill the marked pixels in the output grid
    for r_fill, c_fill in pixels_to_fill:
        output_np[r_fill, c_fill] = blue

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid