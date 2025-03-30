import numpy as np
from collections import deque

"""
Identifies connected components in the input grid. A component consists of contiguous pixels that are not white (0), connected cardinally and diagonally. 
A component is considered "valid" if it contains exactly one pixel whose color is not blue (1) and not white (0). This unique non-blue, non-white pixel is the "marker".
For each valid component:
  - Identify the marker's color.
  - Identify all the blue (1) pixels belonging to this component.
  - For each blue pixel in the component, determine if it is "interior". A blue pixel is interior if none of its cardinal neighbors (up, down, left, right) are white (0) pixels OR fall outside the grid boundary.
  - Change the color of all interior blue pixels within the valid component to the marker's color in the output grid.
Pixels in invalid components (those with zero or more than one marker) and pixels not part of any component (white pixels) remain unchanged.
"""

def find_marker_component(grid, start_r, start_c, visited):
    """
    Finds a connected component starting from (start_r, start_c) using BFS.
    The component includes non-white (0) pixels, connected cardinally and diagonally.
    It also identifies if the component has exactly one non-blue(1), non-white(0) marker pixel.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): A boolean grid tracking visited pixels.

    Returns:
        tuple: (component_pixels, marker_color, is_valid)
            component_pixels (list): List of ((r, c), color) tuples for pixels in the component.
            marker_color (int): The color of the unique marker, or -1 if not unique/found.
            is_valid (bool): True if the component has exactly one marker pixel.
    """
    height, width = grid.shape
    start_color = grid[start_r, start_c]

    # Ignore white pixels or already visited pixels
    if start_color == 0 or visited[start_r, start_c]:
        return [], -1, False

    component_pixels = []
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True

    marker_color = -1
    marker_count = 0
    marker_coord = None # Store coord to ensure only one marker *pixel* exists

    while q:
        r, c = q.popleft()
        current_color = grid[r, c]
        component_pixels.append(((r, c), current_color))

        # Check if this pixel is a potential marker
        if current_color > 1: # Non-blue, non-white
            if marker_count == 0:
                marker_color = current_color
                marker_count = 1
                marker_coord = (r, c)
            # If we find another marker pixel (different location or different color)
            elif (r,c) != marker_coord: 
                 # Check if it's the *same* color but different location, or just different color
                 # Either way, more than one marker pixel means invalid.
                 marker_count = 2 # Mark as invalid (more than one marker pixel)


        # Explore neighbors (8 directions: cardinal + diagonal)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self

                nr, nc = r + dr, c + dc

                # Check bounds
                if 0 <= nr < height and 0 <= nc < width:
                    neighbor_color = grid[nr, nc]
                    # Check if neighbor is part of the component (not white) and not visited
                    if neighbor_color != 0 and not visited[nr, nc]:
                        visited[nr, nc] = True
                        q.append((nr, nc))

    is_valid = (marker_count == 1)
    if not is_valid:
        marker_color = -1 # Ensure marker_color is -1 if not valid

    return component_pixels, marker_color, is_valid

def is_interior(grid, r, c):
    """
    Checks if a pixel at (r, c) is 'interior'.
    An interior pixel is not cardinally adjacent to any white (0) pixel
    or the grid boundary.

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

        # If neighbor is out of bounds OR is white (0), it's a boundary pixel.
        if not (0 <= nr < height and 0 <= nc < width) or grid[nr, nc] == 0:
            return False

    # If no white or out-of-bounds neighbors were found
    return True

def transform(input_grid):
    """
    Transforms the input grid by finding valid components (connected non-white pixels
    with exactly one marker pixel), and filling the interior blue pixels of those
    components with the marker color.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    visited = np.zeros_like(input_np, dtype=bool)

    # Iterate through each cell to find starting points of components
    for r in range(height):
        for c in range(width):
            # If pixel is non-white and hasn't been visited as part of a component yet
            if input_np[r, c] != 0 and not visited[r, c]:
                # Find the connected component starting from here
                component_pixels, marker_color, is_valid = find_marker_component(input_np, r, c, visited)

                # If the component is valid (exactly one marker found)
                if is_valid:
                    # Iterate through all pixels identified as part of this valid component
                    for (br, bc), pixel_color in component_pixels:
                        # We only modify blue pixels
                        if pixel_color == 1:
                            # Check if the blue pixel is an interior pixel
                            if is_interior(input_np, br, bc):
                                # Change the color of this interior blue pixel in the output grid
                                output_np[br, bc] = marker_color
                # No action needed for invalid components, pixels are already marked visited

    return output_np.tolist()