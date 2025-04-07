"""
Transformation Rule:
1. Identify Color Priority Legend: Scan the grid, starting from the bottom row upwards. Locate the first row that follows the pattern `azure, color1, azure, color2, azure, color3, ...` across its width (allowing for trailing azure pixels). Extract the sequence of non-azure colors (`color1, color2, color3, ...`). This sequence defines the color priority, where colors appearing earlier have higher priority. If no such legend is found, assume a default low priority for all colors.
2. Find Blue-Bordered Boxes: Search the grid for distinct rectangular objects. A valid object consists of a continuous, single-pixel-thick border of blue (1) pixels completely enclosing a rectangular area. The enclosed area must be filled entirely with a single color, which cannot be blue (1) or azure (8). Record the inner color and the bounding box coordinates (of the blue border) for each valid box found.
3. Identify Adjacent Boxes and Azure Gaps: Examine all pairs of identified boxes. If two boxes are adjacent either horizontally or vertically, and the space between their blue borders consists *only* of a single row or single column composed entirely of azure (8) pixels, identify this sequence of azure pixels as a 'gap'. The adjacency must be exact (separation distance of 1 pixel, filled with azure).
4. Determine Fill Color: For each identified gap, consider the inner colors of the two boxes adjacent to it. Compare their priorities based on the legend identified in step 1. The color with the higher priority (appearing earlier in the legend sequence) is the designated 'fill color' for this gap. If priorities are equal (e.g., same color or neither in legend), the color of the first box considered (e.g., Box A in an A-B pair) is used due to the `<=` check.
5. Fill Gaps: Create a copy of the input grid. For every identified gap, change the color of all azure (8) pixels within that gap to the fill color determined in step 4.
6. Output: Return the modified grid.
"""

import numpy as np
from collections import defaultdict

def _find_legend_priority(grid):
    """Finds the legend row and returns a dictionary mapping color to priority (lower is better)."""
    height, width = grid.shape
    legend_priority = {}
    priority_list = []

    # Scan rows from bottom up, looking for the pattern 8, C, 8, C...
    for r in range(height - 1, -1, -1):
        row = grid[r]
        is_legend = False
        current_legend = []
        if width < 2: continue # Need at least 8, C

        # Check pattern: alternates between 8 and non-8, starting with 8
        valid_pattern = True
        for c in range(width):
            if c % 2 == 0: # Should be 8
                if row[c] != 8:
                    valid_pattern = False
                    break
            else: # Should be non-8 color
                if row[c] == 8:
                     # Allow trailing 8s
                    if c+1 < width and np.any(row[c+1:] != 8):
                         valid_pattern = False
                         break
                     else: # Trailing 8s are okay, end of legend part
                         break
                current_legend.append(row[c])

        if valid_pattern and current_legend: # Found a potential legend row with colors
             priority_list = current_legend
             break # Assume first valid one from bottom is the legend

    # Create priority map (lower index = higher priority)
    for i, color in enumerate(priority_list):
        if color not in legend_priority: # Only take the first occurrence for priority
            legend_priority[color] = i # Corrected indentation here

    # Handle case where legend might not contain all colors present in boxes
    # Assign lowest priority (infinity) to colors not in the legend
    legend_priority = defaultdict(lambda: float('inf'), legend_priority)

    return legend_priority

def _find_boxes(grid):
    """Finds all blue-bordered boxes with solid inner colors."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    boxes = []

    for r in range(height):
        for c in range(width):
            # Look for a potential top-left corner of the blue border
            if grid[r, c] == 1 and not visited[r, c]:
                q = [(r, c)]
                visited[r, c] = True
                border_pixels = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                # BFS to find connected blue pixels
                head = 0
                while head < len(q):
                    curr_r, curr_c = q[head]
                    head += 1
                    min_r, max_r = min(min_r, curr_r), max(max_r, curr_r)
                    min_c, max_c = min(min_c, curr_c), max(max_c, curr_c)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == 1 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            border_pixels.add((nr, nc))
                            q.append((nr, nc))

                # Check if it forms a rectangle border
                is_rect_border = True
                if max_r - min_r < 2 or max_c - min_c < 2: # Must be at least 3x3 including border
                    is_rect_border = False
                else:
                    # Check if all pixels on the calculated boundary are in border_pixels
                    calculated_border_size = 2 * (max_r - min_r + 1) + 2 * (max_c - min_c + 1) - 4
                    if len(border_pixels) != calculated_border_size:
                         is_rect_border = False
                    else:
                         for br in range(min_r, max_r + 1):
                             for bc in range(min_c, max_c + 1):
                                 is_on_edge = (br == min_r or br == max_r or bc == min_c or bc == max_c)
                                 if is_on_edge:
                                     if (br, bc) not in border_pixels:
                                         is_rect_border = False
                                         break
                                 # No need to check inner pixels here, BFS already ensured connectivity
                             if not is_rect_border: break


                if not is_rect_border: continue

                # Check inner region
                inner_r_start, inner_r_end = min_r + 1, max_r # Adjusted end boundary check logic
                inner_c_start, inner_c_end = min_c + 1, max_c # Adjusted end boundary check logic

                # Ensure inner region exists
                if inner_r_start >= inner_r_end or inner_c_start >= inner_c_end:
                    continue

                inner_color = grid[inner_r_start, inner_c_start]
                if inner_color == 1 or inner_color == 8: continue # Inner can't be blue or azure

                is_solid = True
                for ir in range(inner_r_start, inner_r_end):
                    for ic in range(inner_c_start, inner_c_end):
                        if grid[ir, ic] != inner_color:
                            is_solid = False
                            break
                    if not is_solid: break

                if is_solid:
                    boxes.append({
                        'inner_color': inner_color,
                        'bounds': (min_r, max_r, min_c, max_c), # Inclusive bounds of border
                    })

    return boxes


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify Color Priority Legend
    legend_priority = _find_legend_priority(input_grid)
    # Note: If no legend found, defaultdict assigns inf priority

    # 2. Find Blue-Bordered Boxes
    boxes = _find_boxes(input_grid)

    # 3. & 4. Identify adjacent boxes, determine fill color, and store gaps to fill
    gaps_to_fill = []
    num_boxes = len(boxes)
    for i in range(num_boxes):
        for j in range(i + 1, num_boxes):
            box_a = boxes[i]
            box_b = boxes[j]
            ar1, ar2, ac1, ac2 = box_a['bounds']
            br1, br2, bc1, bc2 = box_b['bounds']
            color_a = box_a['inner_color']
            color_b = box_b['inner_color']

            # Determine fill color based on priority (lower number = higher priority)
            fill_color = color_a if legend_priority[color_a] <= legend_priority[color_b] else color_b

            gap_coords = []

            # Check Horizontal Adjacency (A left of B, separated by 1 azure col)
            # Check if box B starts exactly one column after box A ends
            if ac2 + 1 == bc1 -1 : # Need ac2 < gap_col < bc1
                gap_c = ac2 + 1
                # Check if the vertical spans of the boxes overlap
                overlap_r_start = max(ar1, br1)
                overlap_r_end = min(ar2, br2)
                if overlap_r_start <= overlap_r_end: # Rows overlap
                    # Check if the column between them is all azure within the overlap
                    is_azure_gap = True
                    for r in range(overlap_r_start, overlap_r_end + 1):
                        if input_grid[r, gap_c] != 8:
                            is_azure_gap = False
                            break
                    if is_azure_gap:
                        for r in range(overlap_r_start, overlap_r_end + 1):
                           gap_coords.append((r, gap_c))

            # Check Horizontal Adjacency (B left of A, separated by 1 azure col)
            # Check if box A starts exactly one column after box B ends
            elif bc2 + 1 == ac1 - 1: # Need bc2 < gap_col < ac1
                gap_c = bc2 + 1
                # Check if the vertical spans of the boxes overlap
                overlap_r_start = max(ar1, br1)
                overlap_r_end = min(ar2, br2)
                if overlap_r_start <= overlap_r_end: # Rows overlap
                     # Check if the column between them is all azure within the overlap
                    is_azure_gap = True
                    for r in range(overlap_r_start, overlap_r_end + 1):
                         if input_grid[r, gap_c] != 8:
                            is_azure_gap = False
                            break
                    if is_azure_gap:
                        for r in range(overlap_r_start, overlap_r_end + 1):
                            gap_coords.append((r, gap_c))

            # Check Vertical Adjacency (A above B, separated by 1 azure row)
            # Check if box B starts exactly one row after box A ends
            elif ar2 + 1 == br1 - 1: # Need ar2 < gap_row < br1
                gap_r = ar2 + 1
                # Check if the horizontal spans of the boxes overlap
                overlap_c_start = max(ac1, bc1)
                overlap_c_end = min(ac2, bc2)
                if overlap_c_start <= overlap_c_end: # Columns overlap
                    # Check if the row between them is all azure within the overlap
                    is_azure_gap = True
                    for c in range(overlap_c_start, overlap_c_end + 1):
                        if input_grid[gap_r, c] != 8:
                             is_azure_gap = False
                             break
                    if is_azure_gap:
                        for c in range(overlap_c_start, overlap_c_end + 1):
                           gap_coords.append((gap_r, c))

            # Check Vertical Adjacency (B above A, separated by 1 azure row)
            # Check if box A starts exactly one row after box B ends
            elif br2 + 1 == ar1 - 1: # Need br2 < gap_row < ar1
                gap_r = br2 + 1
                # Check if the horizontal spans of the boxes overlap
                overlap_c_start = max(ac1, bc1)
                overlap_c_end = min(ac2, bc2)
                if overlap_c_start <= overlap_c_end: # Columns overlap
                     # Check if the row between them is all azure within the overlap
                    is_azure_gap = True
                    for c in range(overlap_c_start, overlap_c_end + 1):
                         if input_grid[gap_r, c] != 8:
                             is_azure_gap = False
                             break
                    if is_azure_gap:
                        for c in range(overlap_c_start, overlap_c_end + 1):
                            gap_coords.append((gap_r, c))

            # If a valid gap was found between this pair, store it
            if gap_coords:
                 gaps_to_fill.append({'coords': gap_coords, 'fill_color': fill_color})


    # 5. Fill the identified gaps in the output grid
    for gap_info in gaps_to_fill:
        fill_color = gap_info['fill_color']
        for r, c in gap_info['coords']:
            # Ensure coordinates are within bounds (should be, but safety check)
             if 0 <= r < height and 0 <= c < width:
                 output_grid[r, c] = fill_color

    # 6. Return the modified grid
    return output_grid