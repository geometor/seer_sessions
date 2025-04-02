import numpy as np
from collections import deque

"""
Transforms the input grid by identifying a 'container' shape and an 'inner' shape based on specific rules, 
then filling the empty space (white pixels, value 0) enclosed within the container shape 
with the color of the inner shape using a conditional flood fill (BFS). 
The original container and inner shapes retain their colors and positions.

Role Identification Logic:
1. Assumes exactly two non-white colors exist in the grid.
2. Determines which color touches the grid boundary (edge).
3. If only one color touches the edge, it's the container, the other is the inner/fill color.
4. If neither touches the edge, the one with more pixels is the container, the other is the inner/fill color.
5. If both touch the edge or the number of non-white colors is not two, roles cannot be determined, and the original grid is returned.

Conditional Flood Fill:
1. Starts from a pixel of the inner shape.
2. Expands through adjacent pixels (up, down, left, right).
3. Fill propagation stops at pixels matching the container color.
4. Only pixels that were originally white (0) are changed to the fill color.
"""

def find_colors_and_roles(grid):
    """
    Identifies the container color, inner/fill color, and inner shape pixels based on edge-touching and pixel counts.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (container_color, fill_color, inner_shape_pixels, error_message)
               Returns None for colors/pixels and an error message if identification fails.
               inner_shape_pixels is a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    unique_colors = np.unique(grid[grid != 0]) # Find all non-white colors

    # Check if exactly two non-white colors are present
    if len(unique_colors) != 2:
        return None, None, None, f"Requires exactly two non-background colors, found {len(unique_colors)}."

    c1, c2 = unique_colors
    all_non_white_pixels = {c1: set(), c2: set()}
    colors_touching_edge = set()
    pixel_counts = {c1: 0, c2: 0}

    # Collect pixel coordinates, counts, and check edge touching
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color == c1 or color == c2:
                all_non_white_pixels[color].add((r, c))
                pixel_counts[color] += 1
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    colors_touching_edge.add(color)

    # Determine roles based on rules
    c1_touches_edge = c1 in colors_touching_edge
    c2_touches_edge = c2 in colors_touching_edge
    container_color = None
    fill_color = None

    if c1_touches_edge and not c2_touches_edge:
        container_color = c1
        fill_color = c2
    elif not c1_touches_edge and c2_touches_edge:
        container_color = c2
        fill_color = c1
    elif not c1_touches_edge and not c2_touches_edge:
        # Neither touches edge, use pixel count
        if pixel_counts[c1] > pixel_counts[c2]:
             container_color = c1
             fill_color = c2
        else: # Assume c2 > c1 or equal (arbitrarily pick c2 as container in case of tie or equal counts)
             container_color = c2
             fill_color = c1
    else: # Both touch edge or some other ambiguity
        return None, None, None, f"Ambiguous roles: Both colors ({c1}, {c2}) touch edge or other issue."

    if fill_color not in all_non_white_pixels or not all_non_white_pixels[fill_color]:
         return None, None, None, f"Identified inner color {fill_color} has no pixels."

    inner_shape_pixels = all_non_white_pixels[fill_color]
    return container_color, fill_color, inner_shape_pixels, None


def transform(input_grid):
    """
    Applies the conditional flood fill transformation.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid, or the original if roles cannot be determined.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # 1. Identify Container Color, Fill Color, and Inner Shape Pixels
    container_color, fill_color, inner_shape_pixels, error = find_colors_and_roles(grid)

    # If roles cannot be determined, return the original grid
    if error:
        # print(f"Debug: Role identification error: {error}") # Optional debug print
        return output_grid.tolist()
        
    if not inner_shape_pixels:
        # print("Debug: No inner shape pixels found.") # Optional debug print
        return output_grid.tolist()

    # 2. Perform Conditional Flood Fill (BFS)
    # Select an arbitrary starting pixel from the inner shape
    start_pixel = next(iter(inner_shape_pixels)) 
    # Initialize queue for BFS with the start pixel
    q = deque([start_pixel])
    # Initialize visited set, starting with all pixels of the inner shape
    # This prevents overwriting the original inner shape during the fill.
    visited = set(inner_shape_pixels) 

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor has already been visited
                if (nr, nc) not in visited:
                    # Get the neighbor's color from the *original* input grid
                    original_neighbor_color = grid[nr, nc]

                    # Check if the neighbor is NOT part of the container boundary
                    if original_neighbor_color != container_color:
                        # Mark neighbor as visited
                        visited.add((nr, nc)) 
                        
                        # If the neighbor was originally white (0), color it in the output grid
                        if original_neighbor_color == 0:
                            output_grid[nr, nc] = fill_color
                        
                        # Add neighbor to the queue to explore from it (regardless of its original color,
                        # as long as it's not the container color)
                        q.append((nr, nc))
                    # Else: Neighbor is the container color, so we stop filling in this direction
                    # We don't mark it as visited here, only when approached from non-container pixel.
                    
    # Convert the final numpy array back to list of lists
    return output_grid.tolist()