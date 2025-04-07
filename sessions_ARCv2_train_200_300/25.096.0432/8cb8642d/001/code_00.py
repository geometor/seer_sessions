import copy
from collections import deque

"""
Transforms an input grid based on identifying specific rectangular regions.

The transformation rule identifies rectangular regions within the input grid that meet the following criteria:
1. Bounded by a single, non-zero border color `B`.
2. The interior of the rectangle contains cells of color `B` and exactly one 'special' cell of a different non-zero color `S` at location `(r_s, c_s)`.

For each such identified region, the transformation modifies its interior in the output grid:
1. Cells `(r, c)` inside the region's border are updated.
2. If a cell `(r, c)` lies on a diagonal line passing through the special cell's location `(r_s, c_s)` (i.e., `abs(r - r_s) == abs(c - c_s)`), its value is set to the special cell's color `S`.
3. All other interior cells are set to 0.

Cells outside these identified regions (background and region borders) remain unchanged.
"""

def _find_regions(input_grid: list[list[int]]) -> list[dict]:
    """
    Finds all valid regions matching the specified criteria in the grid.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a valid region
        and contains keys: 'coords' (set of (r, c) tuples), 'bbox' (r1, c1, r2, c2),
        'border_color' (B), 'special_color' (S), 'special_pos' (r_s, c_s).
    """
    height = len(input_grid)
    width = len(input_grid[0])
    visited = set()
    regions = []

    for r in range(height):
        for c in range(width):
            if input_grid[r][c] != 0 and (r, c) not in visited:
                # Start BFS to find connected component of non-zero cells
                component_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                colors_in_component = {}
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))
                    color = input_grid[curr_r][curr_c]
                    colors_in_component[color] = colors_in_component.get(color, 0) + 1
                    
                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           input_grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                # Analyze the component
                non_zero_colors = {k: v for k, v in colors_in_component.items() if k != 0}
                
                if len(non_zero_colors) == 2:
                    color_list = list(non_zero_colors.keys())
                    count_list = list(non_zero_colors.values())
                    
                    special_color = -1
                    border_color = -1
                    special_pos = None

                    if count_list[0] == 1:
                        special_color = color_list[0]
                        border_color = color_list[1]
                    elif count_list[1] == 1:
                        special_color = color_list[1]
                        border_color = color_list[0]
                    else:
                        continue # Skip if neither color count is 1

                    # Find the special cell position
                    for cr, cc in component_coords:
                        if input_grid[cr][cc] == special_color:
                            special_pos = (cr, cc)
                            break
                    
                    if special_pos is None: continue # Should not happen if counts are correct

                    # Validate the region structure (border and interior)
                    is_valid = True
                    bbox = (min_r, min_c, max_r, max_c)
                    r1, c1, r2, c2 = bbox
                    
                    # Check if all component cells on the bbox perimeter are border_color
                    # Check if all interior cells are border_color or the special cell
                    for br, bc in component_coords:
                        is_on_perimeter = (br == r1 or br == r2 or bc == c1 or bc == c2)
                        is_interior = (r1 < br < r2 and c1 < bc < c2)
                        
                        cell_color = input_grid[br][bc]

                        if is_on_perimeter:
                             # Check if part of the rectangle defined by bbox.
                             # Cells on corners might be tricky, ensure they belong to this component's border.
                             # A simpler check: ensure all cells *within* the bbox that are *not* part of the component are 0.
                             pass # Defer comprehensive border check
                        
                        if is_interior:
                            if (br, bc) == special_pos:
                                if cell_color != special_color:
                                    is_valid = False
                                    break
                            elif cell_color != border_color:
                                is_valid = False
                                break
                        
                        # If a cell is neither on perimeter nor interior (e.g., concave shape), it might invalidate
                        # Let's assume rectangularity for now based on examples. A stricter check is needed for general cases.

                    # A more robust check: Iterate all cells within bbox
                    component_cell_count_in_bbox = 0
                    for ir in range(r1, r2 + 1):
                        for ic in range(c1, c2 + 1):
                             cell_color = input_grid[ir][ic]
                             is_on_border = (ir == r1 or ir == r2 or ic == c1 or ic == c2)

                             if (ir, ic) in component_coords:
                                 component_cell_count_in_bbox += 1
                                 # Check border cells have border_color
                                 if is_on_border and cell_color != border_color:
                                     is_valid = False; break
                                 # Check interior cells
                                 if not is_on_border:
                                     if (ir, ic) == special_pos:
                                         if cell_color != special_color: is_valid = False; break
                                     elif cell_color != border_color:
                                         is_valid = False; break
                             else:
                                 # Cells within bbox but not in component must be 0
                                 if cell_color != 0:
                                     is_valid = False; break
                        if not is_valid: break
                    
                    # Final check: ensure the component size matches the count within bbox
                    if len(component_coords) != component_cell_count_in_bbox:
                        is_valid = False

                    if is_valid:
                        regions.append({
                            'coords': component_coords,
                            'bbox': bbox,
                            'border_color': border_color,
                            'special_color': special_color,
                            'special_pos': special_pos
                        })

    return regions


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Find all valid regions in the input grid
    regions = _find_regions(input_grid)

    # Perform transformations for each identified region
    for region in regions:
        r1, c1, r2, c2 = region['bbox']
        r_s, c_s = region['special_pos']
        s_color = region['special_color']

        # Iterate through the interior cells of the region's bounding box
        for r in range(r1 + 1, r2):
            for c in range(c1 + 1, c2):
                # Check if the cell belongs to this specific region's interior 
                # (necessary if regions could overlap or be adjacent, though not seen in examples)
                # This check is implicitly handled by the region finding logic ensuring
                # components are distinct and structure is valid.

                # Calculate distance from the special cell
                dr = abs(r - r_s)
                dc = abs(c - c_s)

                # Apply the 'X' pattern rule
                if dr == dc:
                    output_grid[r][c] = s_color
                else:
                    output_grid[r][c] = 0  # Set other interior cells to background color

    return output_grid
