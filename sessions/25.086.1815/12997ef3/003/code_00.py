import numpy as np
from collections import deque

"""
1. Identify Template: Locate the single, contiguous object composed of blue (1) pixels in the input grid (using diagonal adjacency). Determine its shape relative to its top-left corner, fitting it within a 3x3 area. This is the `template_pattern`.
2. Identify Color Sources: Find all pixels in the input grid that are *not* white (0) and *not* blue (1), and which are 'single' pixels (meaning they have no neighbors, including diagonals, of the same color). Record the color and original (row, column) position of each such `color_source_pixel`.
3. Sort Sources: Sort the list of `color_source_pixel`s based first on their row index (ascending) and then on their column index (ascending).
4. Generate Shapes: For each `color_source_pixel` in the sorted list:
    a. Create a new 3x3 grid filled with white (0) pixels.
    b. Apply the `template_pattern` onto this 3x3 grid, using the color of the current `color_source_pixel`. This results in an `individual_output_shape`.
    c. Collect these `individual_output_shape`s in the order they were generated.
5. Arrange Shapes: Determine the arrangement based on the original positions of the sorted `color_source_pixel`s:
    a. Vertical Alignment: If all `color_source_pixel`s have the same column index, stack the generated `individual_output_shape`s vertically, top-to-bottom, in the order they were generated.
    b. Horizontal Alignment: If all `color_source_pixel`s have the same row index, place the generated `individual_output_shape`s horizontally adjacent to each other, left-to-right, in the order they were generated, with **no** separator columns between them.
    c. Other Alignments: Default to vertical stacking if sources are neither strictly vertical nor horizontal.
6. Construct Output: Combine the `individual_output_shape`s according to the determined arrangement to create the final output grid.
"""

def find_connected_component(grid, start_r, start_c, target_color):
    """Finds all connected pixels of target_color starting from (start_r, start_c) using BFS, considering diagonal adjacency."""
    rows, cols = grid.shape
    q = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    component = set([(start_r, start_c)])

    while q:
        r, c = q.popleft()
        # Check 8 neighbors (orthogonal and diagonal)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and \
                   grid[nr, nc] == target_color and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
                    component.add((nr, nc))
    return component

def get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixel coordinates."""
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    # Return top-left row, top-left col, bottom-right row, bottom-right col
    return min(rows), min(cols), max(rows), max(cols)

# is_single_pixel helper is not strictly needed as the logic is embedded in transform,
# but could be reinstated if desired for modularity.

def transform(input_grid):
    """
    Transforms the input grid by replicating a blue template shape with colors
    from isolated source pixels, arranging the results based on source alignment.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify the blue template shape (template_pattern)
    blue_pixels = set()
    template_shape_relative = set()
    min_r_blue, min_c_blue = -1, -1

    # Find the first blue pixel and get the whole component
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 1:
                blue_pixels = find_connected_component(input_np, r, c, 1)
                break
        if blue_pixels:
            break

    # Handle case where no blue object is found
    if not blue_pixels:
        # Returning an empty grid or the input might be options.
        # Based on ARC structure, likely need *some* output.
        # Let's return an empty list-of-lists for now.
        return [[]]

    # Determine the template's top-left corner for relative coordinates
    bbox_blue = get_bounding_box(blue_pixels)
    min_r_blue, min_c_blue, _, _ = bbox_blue

    # Calculate relative coordinates for the template shape (template_pattern)
    for r, c in blue_pixels:
        template_shape_relative.add((r - min_r_blue, c - min_c_blue))

    # 2. Identify color source pixels (single, non-blue, non-white)
    color_sources = []
    for r in range(rows):
        for c in range(cols):
            color = input_np[r, c]
            # Check if color is valid source color (not white 0, not blue 1)
            if color not in [0, 1]:
                 # Check if it's a single pixel (no neighbors, incl. diagonal, of same color)
                 is_isolated = True
                 for dr in range(-1, 2):
                     for dc in range(-1, 2):
                         if dr == 0 and dc == 0: continue
                         nr, nc = r + dr, c + dc
                         # Check bounds and color match
                         if 0 <= nr < rows and 0 <= nc < cols and input_np[nr, nc] == color:
                             is_isolated = False
                             break
                     if not is_isolated: break # Stop checking neighbors for this pixel

                 # If it remained isolated after checking all neighbors
                 if is_isolated:
                     color_sources.append({'color': color, 'r': r, 'c': c})

    # Handle case where no color sources are found
    if not color_sources:
        return [[]] # Return empty list-of-lists

    # 3. Sort color sources by row, then column
    color_sources.sort(key=lambda x: (x['r'], x['c']))

    # 4. Generate individual 3x3 output shapes
    individual_shapes = []
    for source in color_sources:
        # Initialize 3x3 grid with white (0)
        # Assuming template fits within 3x3 based on examples
        shape_grid = np.zeros((3, 3), dtype=int)
        for r_rel, c_rel in template_shape_relative:
            # Apply template pattern using source color, ensure it stays within 3x3
            if 0 <= r_rel < 3 and 0 <= c_rel < 3:
                 shape_grid[r_rel, c_rel] = source['color']
        individual_shapes.append(shape_grid)

    # 5. Determine arrangement and combine
    output_grid = None
    if len(individual_shapes) > 0:
        # Check for Vertical Alignment (all sources share the same column index)
        if len(set(s['c'] for s in color_sources)) == 1:
            output_grid = np.vstack(individual_shapes)
        # Check for Horizontal Alignment (all sources share the same row index)
        elif len(set(s['r'] for s in color_sources)) == 1:
            # Stack horizontally with NO separators
            output_grid = np.hstack(individual_shapes)
        else:
            # Default behavior for scattered sources (e.g., stack vertically)
            output_grid = np.vstack(individual_shapes)

    # Handle case where output_grid might still be None (e.g., if individual_shapes was empty)
    # This is covered by the earlier checks for blue_pixels and color_sources,
    # but added for robustness.
    if output_grid is None:
         return [[]] # Return empty list-of-lists

    # 6. Construct Output (Convert final numpy array to list of lists)
    return output_grid.tolist()