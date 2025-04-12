import collections
import itertools
from copy import deepcopy

"""
Transforms an input grid based on two potential modes, determined by the presence of unique colors (colors appearing exactly once, excluding the background color).

Mode 1: Unique Colors Exist
1. Determine fill colors:
    - Identify unique colors (uc) and their non-background orthogonal neighbors (nc).
    - Form candidate pairs (uc, nc or uc).
    - 'outer_fill_color' is the value (nc or uc) from the pair with the max value, breaking ties by maximizing the associated uc.
    - 'uc_used' is the unique color associated with the selected outer fill pair.
    - 'inner_fill_color' is the highest remaining unique color not equal to 'uc_used', if any.
2. Determine fill regions:
    - Identify size-3 objects with color < 5 ('outer_bb_objects').
    - 'BB_outer' is the minimal bounding box of 'outer_bb_objects'.
    - If 'inner_fill_color' exists:
        - Find the set of most frequent non-background color(s).
        - Identify 'inner_bb_objects' (subset of 'outer_bb_objects' whose color is NOT in the most frequent set).
        - 'BB_inner' is the minimal bounding box of 'inner_bb_objects'. (High uncertainty about this rule).
3. Apply fills:
    - Fill background cells within 'BB_outer' with 'outer_fill_color'.
    - If 'BB_inner' exists, fill background cells within 'BB_inner' with 'inner_fill_color' (overwrites outer).

Mode 2: No Unique Colors Exist (High Uncertainty)
1. Group size-3 objects by their color 'C'. Sort these colors 'C'.
2. For each color group 'C' in sorted order:
    - Determine 'fill_color_C': max(max non-background color adjacent to any cell of color C, C itself).
    - Calculate 'BB_C': minimal bounding box for the size-3 objects of color 'C'. (Region rule is likely incorrect).
    - Fill background cells within 'BB_C' with 'fill_color_C'. Later fills (higher C) overwrite earlier ones.

General Rules:
- The 'background_color' is the most frequent color in the input grid.
- Only background cells are ever filled. Original non-background cells are preserved.
- Object finding uses orthogonal connectivity for cells of the *same* color.
- Bounding boxes are minimal axis-aligned rectangles.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_objects(grid: list[list[int]], background_color: int) -> list[dict]:
    """Finds connected objects of the same non-background color."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r][c]
            if color != background_color and (r, c) not in visited:
                obj_locations = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_locations.add((r,c))

                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            obj_locations.add((nr, nc))
                            
                if obj_locations:
                    objects.append({
                        "color": color,
                        "locations": list(obj_locations),
                        "size": len(obj_locations)
                    })
    return objects

def get_color_counts(grid: list[list[int]]) -> collections.Counter:
    """Counts occurrences of each color in the grid."""
    counts = collections.Counter()
    for row in grid:
        counts.update(row)
    return counts

def get_bounding_box(objects: list[dict]) -> tuple[int, int, int, int] | None:
    """Calculates the minimal bounding box for a list of objects."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    has_locations = False

    for obj in objects:
        for r, c in obj['locations']:
            has_locations = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    if not has_locations:
        return None 

    return min_r, min_c, max_r, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    height = len(input_grid)
    width = len(input_grid[0])
    output_grid = deepcopy(input_grid)

    # 1. Determine background color
    color_counts = get_color_counts(input_grid)
    if not color_counts: return output_grid
    background_color = color_counts.most_common(1)[0][0]

    # 2. Find all objects
    all_objects = find_objects(input_grid, background_color)
    if not all_objects: return output_grid

    # 3. Find unique colors (excluding background) and their locations
    unique_colors = {}
    non_bg_counts = {color: count for color, count in color_counts.items() if color != background_color}
    for r in range(height):
        for c in range(width):
             color = input_grid[r][c]
             if color != background_color and non_bg_counts.get(color) == 1:
                 unique_colors[color] = (r, c) 

    # 4. Identify size-3 objects
    size_3_objects = [obj for obj in all_objects if obj['size'] == 3]
    
    # 5. Mode Selection
    if unique_colors:
        # -------- Mode 1: Unique Colors Exist --------
        
        # 7. Determine Fill Colors
        candidate_pairs = []
        for uc, (r, c) in unique_colors.items():
            candidate_pairs.append((uc, uc)) # Pair with itself
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = input_grid[nr][nc]
                if neighbor_color != background_color and neighbor_color != uc:
                     candidate_pairs.append((uc, neighbor_color))
                     
        if not candidate_pairs:
             return output_grid # Should not happen if unique_colors is non-empty

        # Find the best pair: max value, tie-break with max uc
        candidate_pairs.sort(key=lambda pair: (pair[1], pair[0]), reverse=True)
        uc_used, outer_fill_color = candidate_pairs[0]

        # Determine inner fill color
        remaining_unique_colors = {uc for uc in unique_colors if uc != uc_used}
        inner_fill_color = max(remaining_unique_colors) if remaining_unique_colors else None

        # 8. Outer Fill
        outer_bb_objects = [obj for obj in size_3_objects if obj['color'] < 5]

        if not outer_bb_objects:
            return output_grid # No objects to define outer region

        bb_outer = get_bounding_box(outer_bb_objects)
        if bb_outer is None: return output_grid

        min_r_outer, min_c_outer, max_r_outer, max_c_outer = bb_outer

        # Apply Outer Fill
        for r in range(min_r_outer, max_r_outer + 1):
            for c in range(min_c_outer, max_c_outer + 1):
                if input_grid[r][c] == background_color:
                    output_grid[r][c] = outer_fill_color

        # 9. Inner Fill Condition
        if inner_fill_color is not None:
            # 10. Determine Inner BB Objects (High Uncertainty)
            most_frequent_set = set()
            if non_bg_counts:
                 max_freq = 0
                 for color, count in non_bg_counts.items():
                      max_freq = max(max_freq, count)
                 most_frequent_set = {color for color, count in non_bg_counts.items() if count == max_freq}

            inner_bb_objects = [obj for obj in outer_bb_objects if obj['color'] not in most_frequent_set]
            
            # Fallback (speculative, maybe not needed or correct)
            # if not inner_bb_objects and outer_bb_objects:
            #     inner_bb_objects = outer_bb_objects 

            # 11. Inner Fill Execution
            if inner_bb_objects:
                bb_inner = get_bounding_box(inner_bb_objects)
                if bb_inner:
                    min_r_inner, min_c_inner, max_r_inner, max_c_inner = bb_inner
                    # Apply Inner Fill
                    for r in range(min_r_inner, max_r_inner + 1):
                        for c in range(min_c_inner, max_c_inner + 1):
                            if input_grid[r][c] == background_color:
                                output_grid[r][c] = inner_fill_color # Overwrite
                                    
    else:
        # -------- Mode 2: No Unique Colors Exist (High Uncertainty) --------
        
        # 13. Process per Color Group
        colors_in_size_3 = sorted(list({obj['color'] for obj in size_3_objects}))

        for color_c in colors_in_size_3:
            # Determine Fill Color for C
            max_adjacent_color = -1
            cells_of_color_c = []
            group_c_objects = []
            for obj in size_3_objects:
                if obj['color'] == color_c:
                    group_c_objects.append(obj)
                    cells_of_color_c.extend(obj['locations'])
            
            if not group_c_objects: continue # Should not happen

            for r, c in cells_of_color_c:
                 for nr, nc in get_neighbors(r, c, height, width):
                     neighbor_color = input_grid[nr][nc]
                     if neighbor_color != background_color and neighbor_color != color_c:
                         max_adjacent_color = max(max_adjacent_color, neighbor_color)

            fill_color_c = max(max_adjacent_color, color_c) # Use neighbor if found and higher, else C

            # Determine Fill Region for C (Likely incorrect rule for E4)
            bb_c = get_bounding_box(group_c_objects)
            if bb_c is None: continue

            min_r_c, min_c_c, max_r_c, max_c_c = bb_c

            # Execute Fill for C
            for r in range(min_r_c, max_r_c + 1):
                for c in range(min_c_c, max_c_c + 1):
                    if input_grid[r][c] == background_color:
                        # Overwrite based on processing order (sorted colors C)
                        output_grid[r][c] = fill_color_c

    # 15. Return Output
    return output_grid