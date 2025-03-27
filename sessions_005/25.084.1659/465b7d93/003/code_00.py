import numpy as np
from collections import deque

def transform(input_grid_list):
    """
    Identifies a boundary object (color 6) and a fill source object (another non-background color).
    Removes the fill source object by changing its pixels to the background color (most frequent color).
    Determines the interior region: background-colored pixels enclosed by the boundary.
    If the fill source color's value is less than the boundary color's value (6), fills the entire interior region with the fill source color.
    If the fill source color's value is greater than the boundary color's value (6), fills only the pixels in the interior region that lie on the leftmost column or bottommost row of the interior region's bounding box (forming an L-shape) with the fill source color.
    """

    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Background, Boundary (6), and Fill Source colors
    colors, counts = np.unique(input_grid, return_counts=True)
    
    # Check for expected number of colors
    if len(colors) < 2: 
        # Not enough colors to perform the task, return copy of input
        return output_grid.tolist() 
        
    background_color = colors[np.argmax(counts)]
    boundary_color = 6  # Fixed based on examples

    # Find fill source color (the color that is not background and not boundary)
    fill_source_color = -1
    fill_source_coords = []
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_grid[r, c]
            if pixel_color != background_color and pixel_color != boundary_color:
                if fill_source_color == -1:
                    fill_source_color = pixel_color
                # Ensure consistency if multiple source pixels exist
                if pixel_color == fill_source_color:
                    fill_source_coords.append((r, c))
                else:
                     # Found more than one non-background, non-boundary color - ambiguity
                     # Based on current understanding, this shouldn't happen. Return input copy.
                     return output_grid.tolist()

    # Handle case where only background and boundary are present, or boundary is missing
    if fill_source_color == -1:
        # No fill source identified (e.g., only bg and boundary, or boundary is missing and mistaken for fill)
        # Or boundary color 6 is not present among non-background colors
        if 6 not in colors[colors != background_color]:
             return output_grid.tolist() # Boundary missing
        # else: Only BG and Boundary present, no action needed.

    # 2. Remove Fill Source object from the output grid
    for r, c in fill_source_coords:
        output_grid[r, c] = background_color

    # 3. Identify Interior region using Breadth-First Search (BFS) from edges
    visited = set() # Set of exterior background pixels
    queue = deque()

    # Add all background pixels on the edges to the queue and visited set
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_grid[r, c] == background_color and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
             if input_grid[r, c] == background_color and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))

    # Perform BFS to find all reachable background pixels from the outside
    while queue:
        r, c = queue.popleft()

        # Check neighbors (4-directional: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is background and not visited and not part of the boundary
                if (input_grid[nr, nc] == background_color and
                        (nr, nc) not in visited):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    # 4. Collect Interior background pixels and calculate their bounding box
    interior_pixels = []
    min_r, min_c = rows, cols
    max_r, max_c = -1, -1
    for r in range(rows):
        for c in range(cols):
            # If a pixel was originally background AND was not reached by BFS from the outside
            if input_grid[r, c] == background_color and (r, c) not in visited:
                interior_pixels.append((r,c))
                min_r = min(min_r, r)
                min_c = min(min_c, c)
                max_r = max(max_r, r)
                max_c = max(max_c, c)

    # 5. Apply Conditional Fill Logic
    if not interior_pixels: # No interior region found
        return output_grid.tolist()

    # Check if fill source was identified (could be missing if only bg and boundary)
    if fill_source_color == -1:
         return output_grid.tolist()

    # Case 1: Fill Color < Boundary Color (6) -> Fill completely
    if fill_source_color < boundary_color:
        for r, c in interior_pixels:
            output_grid[r, c] = fill_source_color
    # Case 2: Fill Color > Boundary Color (6) -> Fill L-shape
    elif fill_source_color > boundary_color:
        for r, c in interior_pixels:
            # Check if the pixel is on the left edge (min_c) or bottom edge (max_r) of the bbox
            if c == min_c or r == max_r:
                output_grid[r, c] = fill_source_color
    # Case 3: Fill Color == Boundary Color (unlikely based on examples, but default to no fill)
    # else:
    #    pass # No fill action if fill color equals boundary color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()