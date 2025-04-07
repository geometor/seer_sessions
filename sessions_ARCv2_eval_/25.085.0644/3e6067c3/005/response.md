```python
"""
Transformation Rule:
1. Initialize: Create a copy of the input grid to serve as the output grid.
2. Identify Color Priority Legend:
    a. Scan the input grid row by row, starting from the bottom and moving upwards.
    b. Identify the first row encountered that matches the pattern: azure pixel (8), non-azure color pixel, azure pixel (8), non-azure color pixel, and so on (`8, C1, 8, C2, 8,...`). The pattern must start with azure at the beginning of the row. Trailing azure pixels at the end of the row are permitted after the last non-azure color.
    c. If such a row is found, extract the sequence of non-azure colors (`C1, C2, C3,...`). This sequence defines the color priority: `C1` has the highest priority, `C2` the next highest, and so on.
    d. Create a priority mapping where lower numbers indicate higher priority (e.g., `C1: 0, C2: 1, ...`). Assign a very low priority (e.g., infinity) to any color not found in this legend sequence.
    e. If no such legend row is found, all colors effectively have the lowest priority.
3. Find Blue-Bordered Boxes:
    a. Search the input grid to locate all distinct rectangular objects that meet the following criteria:
        i. They have a continuous, single-pixel-thick border composed entirely of blue (1) pixels.
        ii. The area strictly inside the blue border is filled entirely with a single, solid color.
        iii. This interior fill color is *not* blue (1) and *not* azure (8).
    b. For each valid box found, record its interior color and the coordinates defining the bounding box of its blue border (minimum row, maximum row, minimum column, maximum column).
4. Identify Adjacent Boxes, Azure Gaps, and Determine Fill Color:
    a. Iterate through all unique pairs of boxes found in the previous step.
    b. For each pair (Box A, Box B):
        i. Check if they are adjacent horizontally (side-by-side) with exactly one column separating their blue borders. Verify that this separating column consists *only* of azure (8) pixels within the vertical range where the boxes overlap.
        ii. Check if they are adjacent vertically (one above the other) with exactly one row separating their blue borders. Verify that this separating row consists *only* of azure (8) pixels within the horizontal range where the boxes overlap.
        iii. If a valid azure gap (either horizontal or vertical) is found between Box A and Box B:
            1. Compare the priority of Box A's interior color and Box B's interior color using the legend priority map established in step 2.
            2. The color with the higher priority (lower numerical value in the map) is designated as the 'fill color' for this gap. If priorities are equal (including the case where neither is in the legend), use the interior color of Box A as the fill color (due to the <= implementation).
            3. Record the coordinates of all the azure pixels within this identified gap and the determined fill color.
5. Fill Gaps:
    a. Iterate through all the recorded gaps and their associated fill colors.
    b. For each gap, change the color of the pixels at the recorded azure coordinates in the output grid copy to the determined fill color.
6. Output: Return the modified output grid.
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
        current_legend = []
        valid_pattern = True
        if width < 2: continue # Need at least 8, C

        # Check pattern: alternates between 8 and non-8, starting with 8
        found_color = False
        for c in range(width):
            if c % 2 == 0: # Should be 8
                if row[c] != 8:
                    # Allow starting non-8 only if we haven't found the pattern yet
                    # This check might be too lenient depending on exact reqs,
                    # but tries to handle cases where the legend might not start exactly at col 0
                    # Update: Sticking to the 'must start with 8' rule from the description.
                    if c == 0 or found_color: # If pattern already started, must be 8
                       valid_pattern = False
                       break
                    # If c > 0 and not found_color, it means we have non-8s before the pattern starts. invalid.
                    if c > 0 and not found_color:
                        valid_pattern = False
                        break
                    # If c==0 and row[c]!=8, invalid start
                    if c==0:
                        valid_pattern = False
                        break


            else: # Should be non-8 color
                if row[c] == 8:
                     # Allow trailing 8s only if we've already seen colors
                    if c+1 < width and np.any(row[c+1:] != 8) and found_color:
                         # If there's a non-8 *after* this 8, it breaks the pattern
                         valid_pattern = False
                         break
                     elif found_color: # Trailing 8s after colors are okay, end of legend part
                         break
                     else: # 8 where color should be, and no colors seen yet. Invalid.
                         valid_pattern = False
                         break
                else:
                    # Found a non-8 color in the correct position
                    current_legend.append(row[c])
                    found_color = True

        # Only accept if the pattern was valid AND we actually found colors
        if valid_pattern and found_color:
             priority_list = current_legend
             break # Assume first valid one from bottom is the legend

    # Create priority map (lower index = higher priority)
    temp_priority = {}
    for i, color in enumerate(priority_list):
        if color not in temp_priority: # Only take the first occurrence for priority
            temp_priority[color] = i

    # Assign lowest priority (infinity) to colors not in the legend
    # Use defaultdict for convenient lookup later
    legend_priority = defaultdict(lambda: float('inf'), temp_priority)

    return legend_priority

def _find_boxes(grid):
    """Finds all blue-bordered boxes with solid non-blue, non-azure inner colors."""
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
                component_q = [(r,c)] # Keep track of component for later marking as visited

                # BFS to find connected blue pixels
                head = 0
                while head < len(component_q):
                    curr_r, curr_c = component_q[head]
                    head += 1
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check 4 neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == 1 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            border_pixels.add((nr, nc))
                            component_q.append((nr, nc))

                # Check if it forms a single-pixel thick rectangle border
                is_rect_border = True
                box_h = max_r - min_r + 1
                box_w = max_c - min_c + 1

                if box_h < 3 or box_w < 3: # Must be at least 3x3 including border
                    is_rect_border = False
                else:
                    calculated_border_size = 2 * box_h + 2 * box_w - 4
                    if len(border_pixels) != calculated_border_size:
                         is_rect_border = False
                    else:
                         # Verify all pixels on the perimeter are blue and in border_pixels
                         # And verify pixels just inside the perimeter are NOT blue
                         for br in range(min_r, max_r + 1):
                             for bc in range(min_c, max_c + 1):
                                 is_on_edge = (br == min_r or br == max_r or bc == min_c or bc == max_c)
                                 if is_on_edge:
                                     if (br, bc) not in border_pixels or grid[br,bc] != 1:
                                         is_rect_border = False
                                         break
                                 else: # Inner pixel relative to bounding box
                                      # Check if any immediate neighbor *within* the bbox is blue (indicates thick border)
                                      # Note: This check is implicitly handled by the size check and BFS finding *only* the border.
                                      # A simpler check: ensure all border pixels have neighbors outside the border OR neighbors inside that are not blue.
                                      # We will check the inner area explicitly later.
                                      pass
                             if not is_rect_border: break


                if not is_rect_border: continue

                # Check inner region
                inner_r_start, inner_r_end = min_r + 1, max_r
                inner_c_start, inner_c_end = min_c + 1, max_c

                # Ensure inner region exists (already covered by size check >= 3)
                # if inner_r_start >= inner_r_end or inner_c_start >= inner_c_end:
                #     continue

                inner_color = grid[inner_r_start, inner_c_start]
                # Inner color cannot be blue (border) or azure (gap/legend)
                if inner_color == 1 or inner_color == 8: continue

                is_solid = True
                for ir in range(inner_r_start, inner_r_end):
                    for ic in range(inner_c_start, inner_c_end):
                        if grid[ir, ic] != inner_color:
                            is_solid = False
                            break
                    if not is_solid: break

                if is_solid:
                    # Successfully found a valid box
                    boxes.append({
                        'inner_color': inner_color,
                        'bounds': (min_r, max_r, min_c, max_c), # Inclusive bounds of border
                    })
                    # Mark all border pixels as visited (redundant with BFS but safe)
                    # for br, bc in border_pixels:
                    #    visited[br, bc] = True # Already done in BFS
                #else: # If not solid or not valid border, ensure component is marked visited
                    # Pass, BFS already marked visited pixels

    return boxes

def transform(input_grid):
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify Color Priority Legend
    legend_priority = _find_legend_priority(input_grid)

    # 3. Find Blue-Bordered Boxes
    boxes = _find_boxes(input_grid)

    # 4. Identify adjacent boxes, determine fill color, and store gaps to fill
    gaps_to_fill = []
    num_boxes = len(boxes)
    for i in range(num_boxes):
        for j in range(i + 1, num_boxes):
            box_a = boxes[i]
            box_b = boxes[j]
            ar1, ar2, ac1, ac2 = box_a['bounds'] # min_r, max_r, min_c, max_c
            br1, br2, bc1, bc2 = box_b['bounds'] # min_r, max_r, min_c, max_c
            color_a = box_a['inner_color']
            color_b = box_b['inner_color']

            # Determine fill color based on priority (lower number = higher priority)
            # If equal or both infinite, color_a wins due to <=
            fill_color = color_a if legend_priority[color_a] <= legend_priority[color_b] else color_b

            gap_coords = []
            is_gap_found = False

            # Check Horizontal Adjacency (A left of B, separated by 1 azure col)
            # Check if B's left border is exactly 2 columns right of A's right border
            if ac2 + 2 == bc1:
                gap_c = ac1 + 1 # Column index of the potential gap
                # Ensure this is a valid column index (safety check)
                if 0 <= gap_c < width:
                    # Check if the vertical spans of the *borders* overlap
                    overlap_r_start = max(ar1, br1)
                    overlap_r_end = min(ar2, br2)
                    if overlap_r_start <= overlap_r_end: # Rows overlap
                        # Check if the column between them is all azure within the overlap
                        is_azure_gap = True
                        current_gap_segment = []
                        for r in range(overlap_r_start, overlap_r_end + 1):
                            if input_grid[r, gap_c] != 8:
                                is_azure_gap = False
                                break
                            else:
                                current_gap_segment.append((r, gap_c))
                        if is_azure_gap and current_gap_segment: # Ensure gap exists and is azure
                            gap_coords.extend(current_gap_segment)
                            is_gap_found = True

            # Check Horizontal Adjacency (B left of A, separated by 1 azure col)
            # Check if A's left border is exactly 2 columns right of B's right border
            elif bc2 + 2 == ac1 and not is_gap_found: # Prevent checking if already found
                gap_c = bc1 + 1 # Column index of the potential gap
                if 0 <= gap_c < width:
                    overlap_r_start = max(ar1, br1)
                    overlap_r_end = min(ar2, br2)
                    if overlap_r_start <= overlap_r_end:
                        is_azure_gap = True
                        current_gap_segment = []
                        for r in range(overlap_r_start, overlap_r_end + 1):
                            if input_grid[r, gap_c] != 8:
                                is_azure_gap = False
                                break
                            else:
                                current_gap_segment.append((r, gap_c))
                        if is_azure_gap and current_gap_segment:
                            gap_coords.extend(current_gap_segment)
                            is_gap_found = True

            # Check Vertical Adjacency (A above B, separated by 1 azure row)
            # Check if B's top border is exactly 2 rows below A's bottom border
            elif ar2 + 2 == br1 and not is_gap_found: # Prevent checking if already found
                gap_r = ar1 + 1 # Row index of the potential gap
                if 0 <= gap_r < height:
                    # Check if the horizontal spans of the *borders* overlap
                    overlap_c_start = max(ac1, bc1)
                    overlap_c_end = min(ac2, bc2)
                    if overlap_c_start <= overlap_c_end: # Columns overlap
                        is_azure_gap = True
                        current_gap_segment = []
                        for c in range(overlap_c_start, overlap_c_end + 1):
                            if input_grid[gap_r, c] != 8:
                                is_azure_gap = False
                                break
                            else:
                                current_gap_segment.append((gap_r, c))
                        if is_azure_gap and current_gap_segment:
                            gap_coords.extend(current_gap_segment)
                            is_gap_found = True

            # Check Vertical Adjacency (B above A, separated by 1 azure row)
            # Check if A's top border is exactly 2 rows below B's bottom border
            elif br2 + 2 == ar1 and not is_gap_found: # Prevent checking if already found
                gap_r = br1 + 1 # Row index of the potential gap
                if 0 <= gap_r < height:
                    overlap_c_start = max(ac1, bc1)
                    overlap_c_end = min(ac2, bc2)
                    if overlap_c_start <= overlap_c_end:
                        is_azure_gap = True
                        current_gap_segment = []
                        for c in range(overlap_c_start, overlap_c_end + 1):
                            if input_grid[gap_r, c] != 8:
                                is_azure_gap = False
                                break
                            else:
                                current_gap_segment.append((gap_r, c))
                        if is_azure_gap and current_gap_segment:
                            gap_coords.extend(current_gap_segment)
                            is_gap_found = True # Although redundant due to loop structure

            # If a valid gap was found between this pair, store it
            if gap_coords: # Check if list is non-empty
                 gaps_to_fill.append({'coords': gap_coords, 'fill_color': fill_color})


    # 5. Fill the identified gaps in the output grid
    for gap_info in gaps_to_fill:
        fill_color = gap_info['fill_color']
        for r, c in gap_info['coords']:
            # Ensure coordinates are within bounds (should be, but safety check)
             if 0 <= r < height and 0 <= c < width:
                 # Only fill if the pixel is currently azure (prevents overwriting unrelated things)
                 if output_grid[r, c] == 8:
                     output_grid[r, c] = fill_color

    # 6. Return the modified grid
    return output_grid
```