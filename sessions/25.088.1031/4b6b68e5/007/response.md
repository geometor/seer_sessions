```python
import numpy as np
from collections import deque, Counter

"""
Identifies non-black objects (contiguous regions of the same color 1-9).
For each object that does not touch the grid border, it determines the region enclosed by it.
An enclosed region consists of all pixels (white or non-boundary color) reachable from the white pixels immediately adjacent (4-directionally) to the object, without crossing the object's pixels and without reaching the grid border.
It collects all non-black pixels within this enclosed region that are *not* part of the boundary object itself ('internal markers').
If there is more than one unique color among these internal markers, the transformation proceeds.
It calculates the frequency of each internal marker color. The fill color is the color with the highest frequency. Ties are broken by choosing the color with the lowest numerical index (e.g., Red(2) wins over Green(3) if both appear the most times).
All originally white pixels within the identified enclosed region are then recolored to this fill color in the output grid.
If an object touches the border, or its enclosed region touches the border, or there are 1 or 0 unique internal marker colors, the enclosed white pixels remain unchanged. All other pixels (boundary object pixels, internal markers, pixels outside enclosures) also remain unchanged.
"""

def find_object(grid, start_pos, visited_objects):
    """
    Finds a connected component of a single non-black color using BFS.

    Args:
        grid (np.ndarray): The input grid.
        start_pos (tuple): The starting (row, col) for the BFS (must be non-black).
        visited_objects (np.ndarray): Boolean grid tracking pixels already part of a found object.

    Returns:
        tuple: (object_color, object_pixels, touches_border)
               object_color (int): The color index of the object found.
               object_pixels (set): Set of (row, col) tuples for the object.
               touches_border (bool): True if any pixel of the object is on the grid border.
    """
    H, W = grid.shape
    q = deque([start_pos])
    object_color = grid[start_pos]
    object_pixels = set()
    touches_border = False
    
    # Check if start_pos itself is on border
    r_start, c_start = start_pos
    if r_start == 0 or r_start == H - 1 or c_start == 0 or c_start == W - 1:
        touches_border = True

    visited_objects[start_pos] = True
    object_pixels.add(start_pos)

    while q:
        r, c = q.popleft()

        # Explore neighbors (4-directional for connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_pos = (nr, nc)
                # Check if neighbor is part of the same object and not visited yet
                if grid[neighbor_pos] == object_color and not visited_objects[neighbor_pos]:
                    visited_objects[neighbor_pos] = True
                    object_pixels.add(neighbor_pos)
                    q.append(neighbor_pos)
                    # Check if this neighbor touches the border
                    if nr == 0 or nr == H - 1 or nc == 0 or nc == W - 1:
                        touches_border = True
            # Out of bounds neighbors don't matter for object connectivity itself
            # but border touching is checked via pixel coordinates inside the loop.
            
    return object_color, object_pixels, touches_border

def find_adjacent_white(grid, object_pixels):
    """
    Finds all white pixels (color 0) 4-directionally adjacent to the object pixels.

    Args:
        grid (np.ndarray): The input grid.
        object_pixels (set): Set of (row, col) for the boundary object.

    Returns:
        set: Set of (row, col) tuples for adjacent white pixels.
    """
    H, W = grid.shape
    adjacent_white = set()
    for r, c in object_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_pos = (nr, nc)
                # Check if neighbor is white and not part of the object itself (shouldn't happen with non-black objects)
                if grid[neighbor_pos] == 0 and neighbor_pos not in object_pixels:
                     adjacent_white.add(neighbor_pos)
    return adjacent_white

def check_enclosure_and_find_markers(grid, start_pixels, boundary_color, boundary_pixels):
    """
    Performs a flood fill starting from start_pixels to check for enclosure
    and identify the enclosed region and internal markers.

    Args:
        grid (np.ndarray): The input grid.
        start_pixels (set): Set of (r,c) white pixels adjacent to the boundary to start fill from.
        boundary_color (int): The color of the boundary object (to avoid crossing).
        boundary_pixels (set): Set of (r,c) pixels of the boundary object.

    Returns:
        tuple: (is_enclosed, region_pixels, internal_markers)
               is_enclosed (bool): True if the region does not touch the border.
               region_pixels (set): Set of (r, c) tuples for all pixels in the enclosed region.
               internal_markers (list): List of color indices for non-black, non-boundary pixels found.
    """
    H, W = grid.shape
    q = deque(list(start_pixels))
    visited_region = set(start_pixels)
    internal_markers = []
    is_enclosed = True

    while q:
        r, c = q.popleft()

        # Check if current pixel touches the border
        if r == 0 or r == H - 1 or c == 0 or c == W - 1:
            is_enclosed = False
            # Continue flood fill to find all connected pixels, but mark as not enclosed.

        pixel_color = grid[r, c]
        # If it's a non-black, non-boundary pixel, add its color to markers
        if pixel_color != 0 and pixel_color != boundary_color:
            internal_markers.append(pixel_color)

        # Explore neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_pos = (nr, nc)

            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                # Check if neighbor is valid to explore:
                # 1. Not already visited in *this* flood fill.
                # 2. Not part of the boundary object.
                if neighbor_pos not in visited_region and neighbor_pos not in boundary_pixels:
                    visited_region.add(neighbor_pos)
                    q.append(neighbor_pos)
            # else: # Neighbor is out of bounds - this implicitly means the region touches the border
                 # Handled by the check at the start of the loop for (r,c). If a neighbor is out of bounds,
                 # the pixel (r,c) from which we are exploring must be on the border.
                 # is_enclosed = False # Redundant due to check at start of loop iteration

    return is_enclosed, visited_region, internal_markers


def determine_fill_color(marker_colors):
    """
    Determines the fill color based on frequency and tie-breaking rules.

    Args:
        marker_colors (list): List of color indices of internal markers.

    Returns:
        int: The determined fill color index, or -1 if no markers.
    """
    if not marker_colors:
        return -1 # Should not happen if called correctly, but safe check

    color_counts = Counter(marker_colors)
    unique_colors = list(color_counts.keys())

    if len(unique_colors) <= 1:
        return -1 # Condition for filling not met

    max_count = 0
    most_common_color = -1

    # Sort unique colors by index to ensure lowest index wins ties
    sorted_colors = sorted(unique_colors)

    for color in sorted_colors:
        count = color_counts[color]
        if count > max_count:
            max_count = count
            most_common_color = color
        # If count == max_count, the lower color index (already processed or current) remains the choice.

    return most_common_color


def transform(input_grid):
    """
    Transforms the input grid by finding boundary objects, checking for enclosed regions,
    analyzing internal markers, and filling based on frequency rules.
    """
    output_grid = np.copy(input_grid)
    H, W = input_grid.shape
    visited_objects = np.zeros_like(input_grid, dtype=bool) # Track pixels belonging to processed objects

    # Iterate through each pixel to find potential starting points for boundary objects
    for r in range(H):
        for c in range(W):
            pixel_color = input_grid[r, c]
            # If it's a non-black pixel and hasn't been visited as part of an object yet
            if pixel_color != 0 and not visited_objects[r, c]:

                # Find the connected non-black object and its properties
                boundary_color, boundary_pixels, touches_border = find_object(input_grid, (r, c), visited_objects)

                # Only proceed if the object itself does not touch the border
                if not touches_border:

                    # Find white pixels adjacent to this potential boundary
                    adjacent_white_pixels = find_adjacent_white(input_grid, boundary_pixels)

                    # If there are adjacent white pixels, check if they form an enclosed region
                    if adjacent_white_pixels:
                        # Perform flood fill from these white pixels to find the region, markers, and check enclosure
                        is_enclosed, region_pixels, internal_markers = check_enclosure_and_find_markers(
                            input_grid, adjacent_white_pixels, boundary_color, boundary_pixels
                        )

                        # Process only if the region is fully enclosed
                        if is_enclosed:
                            # Determine the fill color based on internal markers
                            # (handles the >1 unique color check and tie-breaking internally)
                            fill_color = determine_fill_color(internal_markers)

                            # If a valid fill color was determined (meaning >1 unique markers existed)
                            if fill_color != -1:
                                # Fill the *originally white* pixels within the identified enclosed region
                                for pr, pc in region_pixels:
                                    if input_grid[pr, pc] == 0: # Only change pixels that were originally white
                                        output_grid[pr, pc] = fill_color

    return output_grid
```