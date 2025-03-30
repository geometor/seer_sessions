import numpy as np
from collections import deque

"""
Identifies contiguous shapes made of blue (1) pixels in the input grid.
For each blue shape, it checks if it contains exactly one non-blue, non-white pixel (a marker) within its structure.
If a unique marker is found for a shape, the 'interior' blue pixels of that shape are changed to the marker's color in the output grid.
An 'interior' blue pixel is defined as a blue pixel that is not cardinally adjacent (up, down, left, right) to any white (0) pixel.
Shapes without a unique marker, boundary blue pixels of marked shapes, and pixels not part of any blue shape remain unchanged.
"""

def find_connected_component(grid, start_r, start_c, target_color, visited):
    """
    Finds all connected pixels of a target color starting from a given point using BFS.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        target_color (int): The color of the component to find.
        visited (np.array): A boolean grid tracking visited pixels.

    Returns:
        list: A list of (row, col) tuples representing the coordinates of the component.
              Returns an empty list if the start pixel is not the target color or already visited.
    """
    if visited[start_r, start_c] or grid[start_r, start_c] != target_color:
        return []

    height, width = grid.shape
    component_coords = []
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True

    while q:
        r, c = q.popleft()
        component_coords.append((r, c))

        # Check cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, target color, and visited status
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == target_color and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    return component_coords

def is_interior(grid, r, c):
    """
    Checks if a pixel at (r, c) is 'interior'.
    An interior pixel is not cardinally adjacent to any white (0) pixel.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.

    Returns:
        bool: True if the pixel is interior, False otherwise.
    """
    height, width = grid.shape
    # Check cardinal neighbors
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc

        # If neighbor is out of bounds, it's like a boundary, but the rule specifies adjacency to white (0).
        # If the neighbor is within bounds AND is white (0), it's a boundary pixel.
        if 0 <= nr < height and 0 <= nc < width:
            if grid[nr, nc] == 0:
                return False
        # else: # Treat out of bounds as a boundary condition - if a pixel is at edge, it's adjacent to 'outside' which is like white conceptually
              # Based on examples, pixels at the edge of the grid are still filled if not adjacent to 0.
              # So, only check in-bounds neighbours for 0.
              # pass

    # If no white neighbors were found
    return True

def find_marker_for_shape(grid, shape_coords):
    """
    Finds the unique marker color associated with a given shape.
    A marker is a non-blue(1), non-white(0) pixel adjacent to the shape.

    Args:
        grid (np.array): The input grid.
        shape_coords (list): List of (r, c) tuples for the blue shape.

    Returns:
        int: The color of the unique marker, or -1 if no unique marker is found.
    """
    height, width = grid.shape
    marker_color = -1
    marker_count = 0
    potential_markers = {} # Store potential marker locations to avoid recounting same marker

    shape_coords_set = set(shape_coords) # Faster lookups

    # Check adjacent cells for all pixels in the shape
    for r, c in shape_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1,-1)]: # Check all 8 neighbours
            nr, nc = r + dr, c + dc

            if 0 <= nr < height and 0 <= nc < width:
                pixel_color = grid[nr, nc]
                # Check if the neighbor is a potential marker and NOT part of the shape itself
                if pixel_color > 1 and (nr, nc) not in shape_coords_set:
                   # Check if this specific marker location has already been considered
                   if (nr, nc) not in potential_markers:
                        potential_markers[(nr, nc)] = pixel_color # Record this marker location and its color
                        # Now check if this is the first marker found for this shape
                        if marker_count == 0:
                            marker_color = pixel_color
                            marker_count = 1
                        # If it's not the first, check if it's the *same* color as the first
                        elif marker_color != pixel_color:
                            # Found a second, *different* colored marker associated with this shape
                            return -1 # Not a unique marker color
                        # If it's the same color, we just note we found another instance of it,
                        # but marker_count refers to *distinct colors*.
                        # The logic requires exactly *one* marker pixel *in total* though.

    # Let's refine the marker finding based on the examples and NL description.
    # The marker seems to *replace* a blue pixel or be located where a blue pixel could be.
    # Let's search the grid for non-blue, non-white pixels and see which shape they belong to.

    found_marker_color = -1
    found_marker_coords = None
    count = 0

    # Iterate over the grid to find potential markers first
    potential_marker_pixels = []
    for r_idx in range(height):
        for c_idx in range(width):
            if grid[r_idx, c_idx] > 1:
                potential_marker_pixels.append(((r_idx, c_idx), grid[r_idx, c_idx]))

    # Now check which shape each potential marker belongs to
    # A marker belongs to a shape if it's inside or directly adjacent.
    # Let's define 'inside' based on the examples: the marker pixel is found at coordinates (mr, mc)
    # such that changing grid[mr, mc] to 1 would make it part of the shape's connected component.
    # A simpler check: is the marker pixel adjacent to *any* pixel of the shape?

    for (mr, mc), m_color in potential_marker_pixels:
        is_adjacent_to_shape = False
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Check cardinal adjacency
             nr, nc = mr + dr, mc + dc
             if (nr, nc) in shape_coords_set:
                 is_adjacent_to_shape = True
                 break
        if is_adjacent_to_shape:
            if count == 0:
                found_marker_color = m_color
                found_marker_coords = (mr, mc) # Added tracking coords for clarity
                count = 1
            # Check if this newly found adjacent marker is the *same* marker pixel as before
            elif (mr, mc) != found_marker_coords:
                 # Found a second distinct marker pixel adjacent to the shape
                 return -1 # Not unique

    if count == 1:
        return found_marker_color
    else:
        return -1


def transform(input_grid):
    """
    Transforms the input grid by finding blue shapes, checking for unique markers,
    and filling the interior of marked shapes with the marker color.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    visited = np.zeros_like(input_np, dtype=bool)

    # Iterate through each cell to find starting points of blue shapes
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 1 and not visited[r, c]:
                # Found the start of a potential blue shape
                shape_coords = find_connected_component(input_np, r, c, 1, visited)

                if not shape_coords: # Should not happen if initial check passes, but good practice
                    continue

                # Check if this shape has a unique marker adjacent to it
                marker_color = find_marker_for_shape(input_np, shape_coords)

                # If a unique marker color is found for this shape
                if marker_color != -1:
                    # Iterate through all blue pixels identified as part of this shape
                    for br, bc in shape_coords:
                        # Check if the blue pixel is an interior pixel
                        if is_interior(input_np, br, bc):
                            # Change the color of this interior pixel in the output grid
                            output_np[br, bc] = marker_color

    return output_np.tolist()