import numpy as np
from collections import deque

"""
This function transforms an input grid based on the positions of two gray pixels.
1. Find the coordinates of the two gray (5) pixels.
2. Identify which gray pixel is the 'anchor' (part of a larger connected component of non-white pixels) and which is the 'target' (isolated or part of a smaller component, usually size 1). The connected component containing the anchor is the 'source object'. Connectivity is defined by adjacent non-white (0) pixels (including diagonals - 8-way connectivity).
3. Calculate the translation vector (row_offset, col_offset) required to move from the anchor point to the target point.
4. Create a copy of the input grid to serve as the output grid.
5. Iterate through each pixel belonging to the source object (identified in step 2).
6. For each pixel in the source object *except* the anchor gray pixel:
    a. Calculate its new destination coordinates by adding the translation vector to its original coordinates.
    b. If the destination coordinates are within the grid bounds, update the pixel at the destination coordinates in the output grid with the color of the current source object pixel. This overwrites any existing pixel at the destination.
7. Return the modified output grid.
"""

def find_pixels(grid, color):
    """Finds all pixels of a specific color in the grid."""
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                coords.append((r, c))
    return coords

def find_connected_component(grid, start_coord, background_color=0):
    """
    Finds the connected component of non-background pixels including start_coord using 8-way connectivity (BFS).
    Returns a set of (row, col) tuples belonging to the component.
    """
    if grid[start_coord] == background_color:
        return set()

    height, width = grid.shape
    component = set()
    queue = deque([start_coord])
    visited = set([start_coord])

    while queue:
        r, c = queue.popleft()
        if grid[r, c] != background_color:
            component.add((r, c))

            # Check 8 neighbors (Moore neighborhood)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue # Skip self

                    nr, nc = r + dr, c + dc

                    # Check bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        neighbor_coord = (nr, nc)
                        # Check if not visited and not background
                        if neighbor_coord not in visited and grid[nr, nc] != background_color:
                            visited.add(neighbor_coord)
                            queue.append(neighbor_coord)
                            
    # Ensure the starting coordinate itself (even if isolated and non-background) is included if found
    if grid[start_coord] != background_color:
         component.add(start_coord)
            
    return component


def transform(input_grid_list):
    """
    Transforms the input grid by copying a source object defined by an anchor gray pixel
    to a location defined by a target gray pixel.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    gray_color = 5
    background_color = 0

    # 1. Find the coordinates of the two gray pixels.
    gray_pixels = find_pixels(input_grid, gray_color)
    if len(gray_pixels) != 2:
        # Handle error or unexpected input: assume no transformation if not exactly 2 gray pixels
        # Or return input grid? Based on task structure, assume 2 gray pixels always exist.
        # For robustness, let's return the input copy if the assumption fails.
        print(f"Warning: Expected 2 gray pixels, found {len(gray_pixels)}. Returning input copy.")
        return output_grid.tolist()

    p1, p2 = gray_pixels[0], gray_pixels[1]

    # 2. Identify Anchor, Target, and Source Object
    comp1 = find_connected_component(input_grid, p1, background_color)
    comp2 = find_connected_component(input_grid, p2, background_color)

    anchor_point = None
    target_point = None
    source_object_coords = set()

    # The anchor is the gray pixel belonging to the larger component.
    # If components are same size (e.g., both isolated), the logic might need refinement,
    # but examples suggest one is clearly part of a larger shape.
    if len(comp1) > len(comp2):
        anchor_point = p1
        target_point = p2
        source_object_coords = comp1
    elif len(comp2) > len(comp1):
        anchor_point = p2
        target_point = p1
        source_object_coords = comp2
    else: # len(comp1) == len(comp2), e.g., both size 1
          # This case doesn't appear in training data. Assume the first found is anchor arbitrarily?
          # Or assume the one with lower row/col index? Let's default to p1 as anchor.
          # More robust would be needed if this case appears.
        anchor_point = p1
        target_point = p2
        source_object_coords = comp1 # component only contains the anchor itself in this case
        print(f"Warning: Ambiguous anchor/target (components size {len(comp1)}). Defaulting {p1} to anchor.")


    # 3. Calculate the translation vector
    dr = target_point[0] - anchor_point[0]
    dc = target_point[1] - anchor_point[1]

    # 4. Initialize Output Grid (already done with np.copy)

    # 5. & 6. Iterate through source object, translate, and draw (excluding anchor)
    for r, c in source_object_coords:
        # Skip the anchor point itself
        if (r, c) == anchor_point:
            continue

        source_color = input_grid[r, c]

        # 6a. Calculate destination coordinates
        dest_r, dest_c = r + dr, c + dc

        # 6b. Check bounds
        if 0 <= dest_r < height and 0 <= dest_c < width:
            # 6c. Update output grid
            output_grid[dest_r, dest_c] = source_color
            
    # Handle the case where the target marker might need explicit clearing if nothing lands on it.
    # The description said "Clear Target Marker", but overwriting seems to be the actual behaviour.
    # If the target point wasn't overwritten by the copied object, should it become white?
    # Let's test. In train_2 output, the target gray pixel position (8,7) becomes white (0).
    # It seems the intended logic might be: the target marker *location* is the destination for the anchor *location*,
    # but the marker itself disappears. Overwriting achieves this if part of the object lands there.
    # If not, it should perhaps be cleared. Let's re-add the clearing step *before* copying.
    
    # Re-evaluate: The target gray pixel is *part of the input*. The copy operation *overwrites* pixels
    # in the *output* grid (which starts as a copy of input). If nothing is copied onto the
    # original target marker location, it will retain its original gray color in the output.
    # Example 2 output shows the location (8,7) which was gray(5) becomes white(0).
    # This implies the target marker *is* removed/overwritten. If a non-anchor part of the
    # source object lands there, it gets that color. If the *anchor* point lands there (offset=0),
    # it should become white? No, anchor isn't copied. If *nothing* lands there, it should become white.
    # Let's try clearing the target point in the output *after* the copy loop IF it wasn't overwritten.

    # Simpler approach: Clear the target marker *before* copying.
    output_grid_cleared = np.copy(input_grid)
    output_grid_cleared[target_point[0], target_point[1]] = background_color # Clear the target marker

    for r, c in source_object_coords:
        if (r, c) == anchor_point:
            continue
        source_color = input_grid[r, c]
        dest_r, dest_c = r + dr, c + dc
        if 0 <= dest_r < height and 0 <= dest_c < width:
            # Draw onto the grid where the target marker was already cleared
            output_grid_cleared[dest_r, dest_c] = source_color

    # 7. Return the final grid
    return output_grid_cleared.tolist()
