import numpy as np
from collections import defaultdict
import collections

"""
Transformation Rule:
1. Initialize: Create a copy of the input grid to serve as the output grid.
2. Identify Color Priority Legend:
    a. Scan the input grid row by row, starting from the bottom and moving upwards.
    b. Identify the first row encountered that matches the pattern: starts with azure (8), then alternates between a non-azure color pixel (C1, C2, ...) and azure (8), potentially ending with trailing azure (8) pixels (`8, C1, 8, C2, 8,...`). The pattern `8, C1...` must start at column 0.
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
            2. The color with the higher priority (lower numerical value in the map) is designated as the 'fill color' for this gap. If priorities are equal (including the case where neither is in the legend), use the interior color of Box A as the fill color (due to the <= implementation comparison order).
            3. Record the coordinates of all the azure pixels within this identified gap and the determined fill color.
5. Fill Gaps:
    a. Iterate through all the recorded gaps and their associated fill colors.
    b. For each gap, change the color of the pixels at the recorded azure coordinates in the output grid copy to the determined fill color. Only change pixels that are currently azure.
6. Output: Return the modified output grid.
"""

def _find_legend_priority(grid):
    """
    Finds the legend row and returns a dictionary mapping color to priority (lower is better).
    Scans from bottom-up for a row starting with 8, then alternating non-8 color and 8.
    Example: 8 C1 8 C2 8 C3 8 8 ...
    """
    height, width = grid.shape
    priority_list = []

    # Scan rows from bottom up
    for r in range(height - 1, -1, -1):
        row = grid[r]
        current_legend = []
        valid_pattern = False
        found_color = False

        # Check if pattern starts correctly (must start with 8 at column 0)
        if width == 0 or row[0] != 8:
             continue # Does not start with 8, cannot be the legend row

        # Check the rest of the pattern 8, C, 8, C...
        for c in range(width):
            pixel = row[c]
            is_even_idx = (c % 2 == 0)

            if is_even_idx: # Expect 8
                if pixel != 8:
                    # We expect an 8 here. If it's not 8, the pattern is broken.
                    # Unless this is the very start (c=0), which we already checked.
                    # If we previously found colors, this breaks the pattern mid-way (e.g., 8 C1 8 X)
                    current_legend = [] # Reset, this row is invalid
                    valid_pattern = False
                    break # Invalid pattern continuation
            else: # Expect non-8 Color
                if pixel == 8:
                     # If we see an 8 where a color should be:
                     # Check if it's potentially the start of trailing 8s
                     is_trailing = True
                     for k in range(c + 1, width):
                         if row[k] != 8:
                             is_trailing = False
                             break
                     if is_trailing and found_color: # Must have found colors before trailing 8s start
                         valid_pattern = True # Pattern ended correctly here
                         break # Exit column loop for this row
                     else: # It's an 8 misplaced within the pattern, or before any color found.
                         current_legend = [] # Reset
                         valid_pattern = False
                         break # Invalid row
                else: # Found a non-8 color where expected
                    # Ensure color is not azure (8) or blue (1) - based on box rules, maybe legend allows blue? Assume non-azure for now.
                    # The description just says "non-azure color pixel".
                    if pixel == 8: # Double check, should not happen based on outer if
                         current_legend = []
                         valid_pattern = False
                         break
                    current_legend.append(pixel)
                    found_color = True
                    valid_pattern = True # Mark as potentially valid, might break later

        # After checking all columns, if loop finished or broke due to valid end
        if valid_pattern and found_color:
             priority_list = current_legend
             # print(f"Found legend on row {r}: {priority_list}") # Debug
             break # Found the legend row, stop scanning rows

    # Create priority map (lower index = higher priority)
    temp_priority = {}
    for i, color in enumerate(priority_list):
        if color not in temp_priority: # Only take the first occurrence for priority
            temp_priority[color] = i

    # Use defaultdict for convenient lookup later, defaulting to infinity
    legend_priority = defaultdict(lambda: float('inf'), temp_priority)
    # print(f"Priority map: {dict(legend_priority)}") # Debug

    return legend_priority


def _find_boxes(grid):
    """Finds all blue-bordered boxes with solid non-blue, non-azure inner colors."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    boxes = []

    for r_start in range(height):
        for c_start in range(width):
            # Look for a potential top-left corner of the blue border (must be blue and unvisited)
            if grid[r_start, c_start] == 1 and not visited[r_start, c_start]:
                
                q = collections.deque([(r_start, c_start)])
                visited[r_start, c_start] = True
                border_pixels = set([(r_start, c_start)])
                component_pixels = set([(r_start, c_start)]) # Keep track of all blue pixels in this component

                # BFS to find all connected blue pixels in this component
                while q:
                    r, c = q.popleft()
                    
                    # Check 4 neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == 1 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            component_pixels.add((nr, nc))
                            q.append((nr, nc))

                # Determine bounding box of the blue component
                if not component_pixels: continue # Should not happen if we start with a blue pixel
                
                min_r = min(r for r, c in component_pixels)
                max_r = max(r for r, c in component_pixels)
                min_c = min(c for r, c in component_pixels)
                max_c = max(c for r, c in component_pixels)
                
                box_h = max_r - min_r + 1
                box_w = max_c - min_c + 1

                # Basic size check
                if box_h < 3 or box_w < 3: continue # Must be at least 3x3 including border

                # Verify if it forms a single-pixel thick rectangular border
                is_valid_border = True
                
                # 1. Check if all pixels on the perimeter of the bounding box are blue and part of the component
                # 2. Check if all pixels *inside* the perimeter are NOT part of the blue component
                # 3. Check if the count matches the expected border size
                
                expected_border_size = 2 * box_h + 2 * box_w - 4
                if len(component_pixels) != expected_border_size:
                    is_valid_border = False
                else:
                    for r in range(min_r, max_r + 1):
                        for c in range(min_c, max_c + 1):
                            is_on_perimeter = (r == min_r or r == max_r or c == min_c or c == max_c)
                            if is_on_perimeter:
                                if (r, c) not in component_pixels: # Should be blue and found by BFS
                                    is_valid_border = False
                                    break
                            # No need to check inside here, interior check comes next
                        if not is_valid_border: break
                
                if not is_valid_border: continue

                # Check inner region for solid, allowed color
                inner_r_start, inner_r_end = min_r + 1, max_r
                inner_c_start, inner_c_end = min_c + 1, max_c

                inner_color = grid[inner_r_start, inner_c_start]
                # Inner color cannot be blue (1) or azure (8)
                if inner_color == 1 or inner_color == 8: continue

                is_solid_and_valid = True
                for ir in range(inner_r_start, inner_r_end):
                    for ic in range(inner_c_start, inner_c_end):
                        if grid[ir, ic] != inner_color:
                            is_solid_and_valid = False
                            break
                        # Also check if any inner pixel was part of the blue component (means border not single pixel)
                        if (ir,ic) in component_pixels:
                             is_solid_and_valid = False
                             break
                    if not is_solid_and_valid: break

                if is_solid_and_valid:
                    # Successfully found a valid box
                    boxes.append({
                        'inner_color': inner_color,
                        'bounds': (min_r, max_r, min_c, max_c), # Inclusive bounds of border
                        # 'border_pixels': component_pixels # Optional: for debugging
                    })
                    # print(f"Found box: color={inner_color}, bounds=({min_r},{max_r},{min_c},{max_c})") # Debug
                # BFS already marked visited pixels, so we won't re-process this component

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
    processed_gaps = set() # Keep track of filled gap coords to avoid double filling if logic overlaps

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
            priority_a = legend_priority[color_a]
            priority_b = legend_priority[color_b]
            fill_color = color_a if priority_a <= priority_b else color_b
            # print(f"Comparing Box {i} ({color_a}, Prio {priority_a}) and Box {j} ({color_b}, Prio {priority_b}) -> Fill: {fill_color}") # Debug

            gap_coords = []
            is_gap_found = False

            # Check Horizontal Adjacency (A left of B, separated by 1 azure col)
            if ac2 + 2 == bc1: # A's right border col + 1 gap col + 1 B's left border col == B's left border col index
                gap_c = ac2 + 1 # Column index of the potential gap
                overlap_r_start = max(ar1, br1)
                overlap_r_end = min(ar2, br2)
                if overlap_r_start <= overlap_r_end: # Rows overlap
                    is_azure_gap = True
                    current_gap_segment = []
                    for r in range(overlap_r_start, overlap_r_end + 1):
                        if not (0 <= r < height and 0 <= gap_c < width) or input_grid[r, gap_c] != 8:
                            is_azure_gap = False
                            break
                        else:
                            current_gap_segment.append((r, gap_c))
                    if is_azure_gap and current_gap_segment:
                        gap_coords.extend(current_gap_segment)
                        is_gap_found = True
                        # print(f" Found H-Gap (A left B) between {i} and {j} at col {gap_c} rows {overlap_r_start}-{overlap_r_end}") # Debug

            # Check Horizontal Adjacency (B left of A, separated by 1 azure col)
            elif bc2 + 2 == ac1: # B's right border col + 1 gap col + 1 A's left border col == A's left border col index
                gap_c = bc2 + 1 # Column index of the potential gap
                overlap_r_start = max(ar1, br1)
                overlap_r_end = min(ar2, br2)
                if overlap_r_start <= overlap_r_end:
                    is_azure_gap = True
                    current_gap_segment = []
                    for r in range(overlap_r_start, overlap_r_end + 1):
                        if not (0 <= r < height and 0 <= gap_c < width) or input_grid[r, gap_c] != 8:
                            is_azure_gap = False
                            break
                        else:
                            current_gap_segment.append((r, gap_c))
                    if is_azure_gap and current_gap_segment:
                        gap_coords.extend(current_gap_segment)
                        is_gap_found = True
                        # print(f" Found H-Gap (B left A) between {i} and {j} at col {gap_c} rows {overlap_r_start}-{overlap_r_end}") # Debug

            # Check Vertical Adjacency (A above B, separated by 1 azure row)
            elif ar2 + 2 == br1: # A's bottom border row + 1 gap row + 1 B's top border row == B's top border row index
                gap_r = ar2 + 1 # Row index of the potential gap
                overlap_c_start = max(ac1, bc1)
                overlap_c_end = min(ac2, bc2)
                if overlap_c_start <= overlap_c_end: # Columns overlap
                    is_azure_gap = True
                    current_gap_segment = []
                    for c in range(overlap_c_start, overlap_c_end + 1):
                         if not (0 <= gap_r < height and 0 <= c < width) or input_grid[gap_r, c] != 8:
                            is_azure_gap = False
                            break
                         else:
                            current_gap_segment.append((gap_r, c))
                    if is_azure_gap and current_gap_segment:
                        gap_coords.extend(current_gap_segment)
                        is_gap_found = True
                        # print(f" Found V-Gap (A above B) between {i} and {j} at row {gap_r} cols {overlap_c_start}-{overlap_c_end}") # Debug

            # Check Vertical Adjacency (B above A, separated by 1 azure row)
            elif br2 + 2 == ar1: # B's bottom border row + 1 gap row + 1 A's top border row == A's top border row index
                gap_r = br2 + 1 # Row index of the potential gap
                overlap_c_start = max(ac1, bc1)
                overlap_c_end = min(ac2, bc2)
                if overlap_c_start <= overlap_c_end:
                    is_azure_gap = True
                    current_gap_segment = []
                    for c in range(overlap_c_start, overlap_c_end + 1):
                        if not (0 <= gap_r < height and 0 <= c < width) or input_grid[gap_r, c] != 8:
                            is_azure_gap = False
                            break
                        else:
                            current_gap_segment.append((gap_r, c))
                    if is_azure_gap and current_gap_segment:
                        gap_coords.extend(current_gap_segment)
                        is_gap_found = True
                        # print(f" Found V-Gap (B above A) between {i} and {j} at row {gap_r} cols {overlap_c_start}-{overlap_c_end}") # Debug


            # If a valid gap was found between this pair, store coords to fill
            if gap_coords: # Check if list is non-empty
                 # Filter out coordinates that might have been processed if multiple pairs share a gap pixel
                 unique_coords_for_this_pair = []
                 for coord in gap_coords:
                     if coord not in processed_gaps:
                         unique_coords_for_this_pair.append(coord)
                         processed_gaps.add(coord)

                 if unique_coords_for_this_pair:
                     gaps_to_fill.append({'coords': unique_coords_for_this_pair, 'fill_color': fill_color})


    # 5. Fill the identified gaps in the output grid
    # print(f"Gaps to fill: {gaps_to_fill}") # Debug
    for gap_info in gaps_to_fill:
        fill_color = gap_info['fill_color']
        for r, c in gap_info['coords']:
            # Final check: Ensure coordinates are within bounds and the pixel is currently azure
             if 0 <= r < height and 0 <= c < width and output_grid[r, c] == 8:
                 output_grid[r, c] = fill_color
             # else: # Debugging unusual cases
             #     if not (0 <= r < height and 0 <= c < width):
             #         print(f"Warning: Gap coord ({r},{c}) out of bounds ({height},{width})")
             #     elif output_grid[r, c] != 8:
             #          print(f"Warning: Gap coord ({r},{c}) is not azure ({output_grid[r,c]}), not filling with {fill_color}")


    # 6. Return the modified grid
    return output_grid