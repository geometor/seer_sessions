import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify all distinct hollow rectangular frames made of azure (8) pixels in the input grid.
2. For each identified azure frame:
    a. Determine the bounding box of the azure frame.
    b. Define the inner area as the region strictly inside the bounding box (excluding the frame pixels themselves).
    c. Find all red (2) pixels located within this inner area in the original input grid.
    d. If no red pixels are found within the frame's inner area, do nothing for this frame.
    e. If red pixels are found, determine the minimum bounding box that encloses *only these red pixels*.
    f. Iterate through all pixel coordinates within the red pixels' bounding box.
    g. For each pixel within this red bounding box, check if its location is also within the inner area of the current azure frame.
    h. If the location is within the frame's inner area and its current color in the grid is white (0), change its color to red (2).
3. Keep all other pixels (including the azure frames) unchanged.
4. Return the modified grid.
"""

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates.

    Args:
        coords: A set or list of (row, col) tuples.

    Returns:
        A tuple (min_row, min_col, max_row, max_col), or None if coords is empty.
    """
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)

def find_connected_components(grid, color):
    """Finds all connected components of a given color in the grid using BFS.

    Args:
        grid: The 2D numpy array representing the grid.
        color: The color value to find components of.

    Returns:
        A list of sets, where each set contains the (row, col) tuples
        of a single connected component. Uses 4-way connectivity.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the component
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if neighbor is within bounds, is the correct color, and hasn't been visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))

                # Add the found component to the list
                components.append(component_coords)

    return components

def transform(input_grid):
    """
    Applies the transformation rule to the input grid. Finds azure frames,
    identifies red pixels inside, calculates their bounding box, and fills
    white pixels within that bounding box inside the frame with red.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    azure_color = 8
    red_color = 2
    white_color = 0

    # Find all connected components of azure pixels
    azure_components = find_connected_components(input_grid, azure_color)

    # Process each azure component (assumed to be a frame)
    for component_coords in azure_components:
        if not component_coords:
            continue

        # Determine the bounding box of the azure frame
        frame_bbox = get_bounding_box(component_coords)
        if frame_bbox is None:
            continue
        frame_min_r, frame_min_c, frame_max_r, frame_max_c = frame_bbox

        # Find all red pixels strictly within the inner area of the frame
        # The inner area is defined by coordinates > min and < max of the frame bbox
        red_pixels_inside = []
        # Iterate through the potential inner area of the frame
        for r in range(frame_min_r + 1, frame_max_r):
            for c in range(frame_min_c + 1, frame_max_c):
                # Check bounds just in case, although range should handle it
                if 0 <= r < rows and 0 <= c < cols:
                    # Check the *original* input grid for red pixels
                    if input_grid[r, c] == red_color:
                        red_pixels_inside.append((r, c))

        # If red pixels were found inside this frame
        if red_pixels_inside:
            # Calculate the bounding box of *these red pixels*
            red_bbox = get_bounding_box(red_pixels_inside)
            if red_bbox is None: # Should not happen if red_pixels_inside is not empty
                continue
            red_min_r, red_min_c, red_max_r, red_max_c = red_bbox

            # Fill the area defined by the red pixels' bounding box
            # but only paint white pixels that are also within the frame's inner area
            for r in range(red_min_r, red_max_r + 1):
                for c in range(red_min_c, red_max_c + 1):
                    # Check 1: Is the coordinate (r, c) strictly inside the azure frame's bounds?
                    is_inside_frame = (frame_min_r < r < frame_max_r and
                                       frame_min_c < c < frame_max_c)

                    # Check 2: Is the pixel currently white in the output grid?
                    if is_inside_frame and output_grid[r, c] == white_color:
                        # If both conditions are true, change the pixel to red
                        output_grid[r, c] = red_color

    # Return the modified grid
    return output_grid