import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify horizontal and vertical lines of azure (8) pixels that divide the grid.
2. Find all contiguous regions of white (0) pixels.
3. For each white region, determine if it is fully enclosed by the azure lines (i.e., it does not touch the grid boundaries).
4. If a white region is enclosed, determine its relative position within the central 3x3 area defined by the lines (top-center, middle-left, center, middle-right, bottom-center).
5. Fill the enclosed regions with specific colors based on their position:
    - top-center: red (2)
    - middle-left: yellow (4)
    - center: magenta (6)
    - middle-right: green (3)
    - bottom-center: blue (1)
6. Leave the azure lines and non-enclosed white regions unchanged.
"""

def find_regions(grid, color):
    """Finds all contiguous regions of a specified color."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                region_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    region_coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store region coords and bounding box
                regions.append({
                    'coords': region_coords,
                    'min_r': min_r, 'max_r': max_r,
                    'min_c': min_c, 'max_c': max_c
                })
    return regions

def find_lines(grid, color):
    """Finds the indices of horizontal and vertical lines of a specified color."""
    height, width = grid.shape
    h_lines = []
    v_lines = []

    # Find horizontal lines (rows full of the color)
    for r in range(height):
        if np.all(grid[r, :] == color):
            h_lines.append(r)

    # Find vertical lines (columns full of the color) - more complex if lines aren't full grid extent
    # Let's find columns that consist ONLY of the line color or background color,
    # and contain at least one line color pixel. A simpler approach for this specific problem
    # might be to find columns that contain the line color between the identified horizontal lines.
    # A robust way is finding columns with ONLY line color:
    for c in range(width):
         if np.all(grid[:, c] == color):
            v_lines.append(c)

    # Refined check for vertical lines based on examples: lines might not span the *entire* height
    # Find columns that contain the line color (8)
    potential_v_lines = [c for c in range(width) if color in grid[:, c]]
    
    # In the context of this problem, vertical lines are continuous segments of color 8.
    # Let's assume the vertical lines are simple and continuous columns of color 8.
    # We can refine this if needed, but the simple check seems to work for the examples.
    v_lines_strict = []
    for c in potential_v_lines:
        is_line = True
        for r in range(height):
             # A vertical line pixel should either be color 8, or be part of a horizontal line
             is_horizontal_line_pixel = False
             if r in h_lines and grid[r,c] == color:
                 is_horizontal_line_pixel = True
             
             if grid[r, c] != color and not is_horizontal_line_pixel: 
                 # Allow 0s only outside the horizontal bounds, if structure is always H-shape
                 # Check if this 0 is 'outside' the main structure defined by h_lines
                 if h_lines and (r < min(h_lines) or r > max(h_lines)):
                     pass # Allow 0s outside the horizontal lines
                 else:
                     # If it's not color 8 and not part of crossing horizontal line, it's not a pure vertical line
                     # However, the examples show 0s within the column span.
                     # Let's stick to the simpler definition first: columns containing only 8s or crossing horizontal 8s.
                     # The examples have columns that *are* pure 8s except at intersections.
                     pass # Revisit logic if needed

    # Simpler approach based on examples: Find columns containing only color 8 between the horizontal lines.
    v_lines = []
    if len(h_lines) >= 2:
       h_min, h_max = min(h_lines), max(h_lines)
       for c in range(width):
           segment = grid[h_min+1:h_max, c]
           # Check if this column has a continuous line of 8s between the horizontal lines
           # A simpler check might just be finding columns with 8s *somewhere*
           if color in grid[:, c]: 
               # Let's just find *all* columns that contain the color 8
               # The relative positioning logic will use the *innermost* ones implicitly.
               if c > 0 and c < width -1 : # Avoid grid edge columns if they happen to be 8
                    # Let's identify the main vertical dividers based on their position relative to each other
                    pass # This requires more complex line identification
    
    # Based on visual inspection of examples, let's find *any* column index containing color 8
    # and rely on sorting later.
    v_lines_indices = sorted(list(set(np.where(grid == color)[1])))
    h_lines_indices = sorted(list(set(np.where(grid == color)[0])))

    # Filter out lines that are just the border (if applicable, not in these examples)
    h_lines_indices = [r for r in h_lines_indices if 0 < r < height - 1 and np.all(grid[r, 1:-1] == color)] # check if it's a line internally
    v_lines_indices = [c for c in v_lines_indices if 0 < c < width - 1 and np.all(grid[1:-1, c] == color)] # check if it's a line internally
    
    # Assuming 2 horizontal and 2 vertical lines define the inner grid.
    h_lines_indices = sorted(list(set(np.where(grid == color)[0])))
    v_lines_indices = sorted(list(set(np.where(grid == color)[1])))

    # Filter based on actual lines (long segments) rather than individual pixels
    final_h_lines = []
    for r in h_lines_indices:
        if np.all(grid[r,:] == color): # Check for full horizontal line
             final_h_lines.append(r)
    
    final_v_lines = []
    for c in v_lines_indices:
         if np.all(grid[:,c] == color): # Check for full vertical line
             final_v_lines.append(c)
             
    # If full lines are not found, perhaps partial lines?
    # Let's refine based on the structure: Find rows/cols that are *mostly* color 8.
    final_h_lines = []
    for r in range(height):
        if np.count_nonzero(grid[r, :] == color) > width // 2 : # Heuristic: More than half the row is the line color
             # Check for continuity? Assume simple lines for now.
             is_line = True
             for c in range(width):
                 # If it's not line color, it must be an intersecting vertical line pixel
                 if grid[r, c] != color and grid[r, c] != 0: # Allow intersections if vertical lines exist
                     if not any(grid[:,c] == color): # Check if this column is a vertical line
                        # pass # This logic is getting complex, let's rethink
                        pass

             # Simpler: identify the row indices containing the horizontal segments of color 8
             if color in grid[r,:]:
                 is_solid_line = True
                 start_col, end_col = -1, -1
                 for c_idx in range(width):
                     if grid[r, c_idx] == color:
                         if start_col == -1: start_col = c_idx
                         end_col = c_idx
                     elif start_col != -1: # End of a segment
                         # Check if it's a significant segment?
                         break # Found a break, maybe not a main line
                 if start_col != -1 and end_col > start_col + 1: # Need at least 2 pixels
                     # Check if it spans most of the width or between vertical lines
                     # Let's assume the main horizontal lines span the whole width
                     if np.all(grid[r,:] == color):
                         final_h_lines.append(r)

    final_v_lines = []
    for c in range(width):
         # Assume main vertical lines span the whole height
         if np.all(grid[:,c] == color):
             final_v_lines.append(c)

    # Fallback / specific structure identification for this task:
    # Assume exactly two dominant horizontal and two dominant vertical lines.
    h_line_rows = sorted([r for r in range(height) if np.all(grid[r, :] == color)])
    v_line_cols = sorted([c for c in range(width) if np.all(grid[:, c] == color)])

    # If full lines aren't found, maybe they are interrupted?
    # Let's find rows/cols with *any* pixel of the line color (8)
    if not h_line_rows:
        h_line_rows = sorted(list(set(np.where(grid == color)[0])))
    if not v_line_cols:
        v_line_cols = sorted(list(set(np.where(grid == color)[1])))
        
    # Heuristic: Assume the lines are those rows/columns with the most color 8 pixels,
    # excluding borders if they are also color 8.
    h_counts = {r: np.count_nonzero(grid[r, :] == color) for r in range(height)}
    v_counts = {c: np.count_nonzero(grid[:, c] == color) for c in range(width)}

    # Sort by count descending, take top 2 (or more if counts are equal)
    sorted_h = sorted(h_counts.items(), key=lambda item: item[1], reverse=True)
    sorted_v = sorted(v_counts.items(), key=lambda item: item[1], reverse=True)

    # Filter out potential lines with low counts if there are clear dominant lines
    h_lines = []
    if sorted_h:
      max_h_count = sorted_h[0][1]
      # Take all rows with count >= max_count * 0.8 (heuristic threshold)
      h_lines = sorted([r for r, count in sorted_h if count >= max_h_count * 0.8])

    v_lines = []
    if sorted_v:
      max_v_count = sorted_v[0][1]
      v_lines = sorted([c for c, count in sorted_v if count >= max_v_count * 0.8])

    # In the specific examples, it seems the relevant lines *are* solid.
    final_h_lines = sorted([r for r in range(height) if np.all(grid[r, :] == color)])
    final_v_lines = sorted([c for c in range(width) if np.all(grid[:, c] == color)])


    # Final attempt: The examples seem to have exactly two solid lines each way.
    h_lines = [r for r in range(height) if np.all(grid[r, :] == color)]
    v_lines = [c for c in range(width) if np.all(grid[:, c] == color)]

    # It's possible the lines are not *fully* solid due to intersections.
    # Let's find rows and columns that are *predominantly* the line color.
    h_lines_final = []
    v_lines_final = []
    for r in range(height):
        # Check if row r is mostly line color, allowing for intersections with vertical lines
        count8 = 0
        for c in range(width):
             # Pixel is 8 OR it's a column identified as a potential vertical line
             is_potential_vline = np.any(grid[:,c] == color) # Does column c have *any* 8s?
             if grid[r,c] == color or (grid[r,c]!=color and is_potential_vline) :
                 count8 +=1
        # A less strict check: simply find rows containing 8s. The sorting will matter.
        if color in grid[r,:]:
             h_lines_final.append(r)


    for c in range(width):
        if color in grid[:,c]:
             v_lines_final.append(c)
             
    # Let's assume the examples *always* have exactly two clear horizontal and two clear vertical lines.
    h_lines = sorted([r for r in range(height) if np.count_nonzero(grid[r, :] == color) > 1])
    v_lines = sorted([c for c in range(width) if np.count_nonzero(grid[:, c] == color) > 1])

    # Identify the two most prominent lines based on count?
    h_counts = {r: np.count_nonzero(grid[r, :] == color) for r in h_lines}
    v_counts = {c: np.count_nonzero(grid[:, c] == color) for c in v_lines}
    
    # Sort by row/col index first, then maybe filter by count?
    # Let's assume the first and last lines found are the ones defining the outer boundary of the inner grid.
    if len(h_lines) >= 2:
        h_lines = [min(h_lines), max(h_lines)]
    if len(v_lines) >= 2:
        v_lines = [min(v_lines), max(v_lines)]
        
    # Use the visually correct lines from examples:
    h_lines_indices = sorted(list(set(np.where(grid == color)[0])))
    v_lines_indices = sorted(list(set(np.where(grid == color)[1])))
    
    # Assume the lines defining the structure are the min and max indices found.
    h_lines = []
    if h_lines_indices:
        h_lines = [min(h_lines_indices), max(h_lines_indices)]
        # Check if they are actual lines (mostly 8s)
        h_lines = [r for r in h_lines if np.count_nonzero(grid[r,:] == color) > width * 0.5]


    v_lines = []
    if v_lines_indices:
        v_lines = [min(v_lines_indices), max(v_lines_indices)]
        v_lines = [c for c in v_lines if np.count_nonzero(grid[:,c] == color) > height * 0.5]


    # Based on the problem structure: find the indices of the horizontal and vertical lines
    # These lines seem solid in the examples.
    h_lines = sorted([r for r in range(grid.shape[0]) if np.all(grid[r, :] == color)])
    v_lines = sorted([c for c in range(grid.shape[1]) if np.all(grid[:, c] == color)])

    # If lines are not solid (e.g., cross shape), adjust logic.
    # For now, assume solid lines based on train examples.

    return h_lines, v_lines


def transform(input_grid):
    """
    Transforms the input grid by finding enclosed white regions defined by azure lines
    and filling them with colors based on their relative position.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    azure_color = 8
    white_color = 0

    # 1. Find the dividing azure lines
    h_lines, v_lines = find_lines(input_grid, azure_color)

    # Expect exactly two horizontal and two vertical lines for the 3x3 inner structure
    if len(h_lines) != 2 or len(v_lines) != 2:
        # If line detection failed or structure is different, return copy
        # Or handle differently based on more examples
        print(f"Warning: Expected 2 horizontal and 2 vertical lines, found {len(h_lines)}h, {len(v_lines)}v. Using as is.")
        # return output_grid # Keep processing if possible

    # Ensure lines are sorted
    h_lines.sort()
    v_lines.sort()

    # 2. Find all white regions
    white_regions = find_regions(input_grid, white_color)

    # 3. Process each white region
    for region_info in white_regions:
        coords = region_info['coords']
        min_r, max_r = region_info['min_r'], region_info['max_r']
        min_c, max_c = region_info['min_c'], region_info['max_c']
        
        # Any point in the region can be used for position check, e.g., top-left
        rep_r, rep_c = min_r, min_c 

        # 4. Check if the region is enclosed (not touching borders)
        is_on_border = (min_r == 0 or max_r == height - 1 or
                        min_c == 0 or max_c == width - 1)

        if not is_on_border and len(h_lines) == 2 and len(v_lines) == 2:
            h1, h2 = h_lines
            v1, v2 = v_lines

            # 5. Determine relative position and assign color
            fill_color = -1 # Default/error color

            # Check position relative to the identified lines
            if rep_r < h1 and v1 < rep_c < v2: # Top-center
                fill_color = 2 # red
            elif h1 < rep_r < h2 and rep_c < v1: # Middle-left
                fill_color = 4 # yellow
            elif h1 < rep_r < h2 and v1 < rep_c < v2: # Center
                fill_color = 6 # magenta
            elif h1 < rep_r < h2 and rep_c > v2: # Middle-right
                fill_color = 3 # green
            elif rep_r > h2 and v1 < rep_c < v2: # Bottom-center
                fill_color = 1 # blue

            # 6. Fill the region in the output grid
            if fill_color != -1:
                for r, c in coords:
                    output_grid[r, c] = fill_color

    return output_grid
