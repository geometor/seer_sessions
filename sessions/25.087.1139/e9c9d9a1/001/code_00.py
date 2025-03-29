import numpy as np

"""
Identifies horizontal green lines (dividers) that separate the grid into vertical bands (Top, Middle, Bottom).
Finds all contiguous rectangular blocks of white pixels within these bands.
Determines the horizontal position (Leftmost, Intermediate, Rightmost) of each white block within its band.
Recolors the white blocks based on their vertical band and horizontal position:
- Top Band: Leftmost -> Red (2), Rightmost -> Yellow (4), Intermediate -> White (0)
- Middle Bands: All -> Orange (7)
- Bottom Band: Leftmost -> Blue (1), Rightmost -> Azure (8), Intermediate -> White (0)
Keeps the original green structure intact.
"""

def find_horizontal_dividers(grid):
    """Finds rows composed entirely of green (3) pixels."""
    dividers = []
    height, width = grid.shape
    for r in range(height):
        if np.all(grid[r, :] == 3):
            dividers.append(r)
    return dividers

def find_blocks(grid, target_color=0):
    """Finds all contiguous blocks of a target color using BFS."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new block
                q = [(r, c)]
                visited[r, c] = True
                coords = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            coords.add((nr, nc))
                
                # Check if the block is rectangular (simple check for this task)
                is_rectangular = True
                if len(coords) != (max_r - min_r + 1) * (max_c - min_c + 1):
                    # This simple check might fail for complex shapes, but seems sufficient here
                    # A more robust check would verify all cells within the bbox are part of coords
                    # For this task, assuming white blocks are always rectangular fills
                    pass # Let's assume rectangular for now based on examples

                if is_rectangular:
                     blocks.append({
                         'coords': coords,
                         'bbox': (min_r, max_r, min_c, max_c)
                     })
                     
    return blocks

def get_vertical_band(bbox, divider_indices, grid_height):
    """Determines the vertical band (Top, Middle, Bottom) of a block."""
    min_r, max_r, _, _ = bbox
    
    if not divider_indices: # No dividers, everything is in one band
        return "Middle" # Or could define as Top/Bottom if needed, Middle seems reasonable

    first_divider = divider_indices[0]
    last_divider = divider_indices[-1]

    if max_r < first_divider:
        return "Top"
    elif min_r > last_divider:
        return "Bottom"
    else: # Between or spanning dividers
        # Check if it's strictly between two dividers or the grid edge and a divider
        is_middle = False
        if min_r > first_divider and max_r < last_divider: # Strictly between first and last
             is_middle = True
        elif len(divider_indices) > 1: # Check between intermediate dividers
             for i in range(len(divider_indices) - 1):
                 if min_r > divider_indices[i] and max_r < divider_indices[i+1]:
                     is_middle = True
                     break
        # If not strictly between, check if it's between a divider and an edge
        # Note: The logic handles blocks strictly above the first divider (Top)
        # and strictly below the last divider (Bottom). Anything else is Middle.
        if not is_middle and not (max_r < first_divider or min_r > last_divider):
             is_middle = True

        if is_middle:
             return "Middle"
        else:
             # This case should ideally not happen if blocks don't cross dividers
             # If a block somehow spans a divider, classify it based on majority maybe?
             # For this task, assume blocks are fully within one band defined by dividers.
             # Defaulting to Middle if ambiguous.
             return "Middle"


def transform(input_grid):
    """
    Transforms the input grid by finding white blocks enclosed by green lines
    and coloring them based on their vertical band and horizontal position within the band.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # 1. Find Horizontal Dividers
    divider_indices = find_horizontal_dividers(grid)

    # 2. Find all white (0) blocks
    white_blocks = find_blocks(grid, target_color=0)

    if not white_blocks:
        return output_grid.tolist() # No white blocks to change

    # 3. Categorize blocks by vertical band
    categorized_blocks = []
    for block in white_blocks:
        bbox = block['bbox']
        band = get_vertical_band(bbox, divider_indices, height)
        categorized_blocks.append({
            'bbox': bbox,
            'coords': block['coords'],
            'band': band,
            'min_c': bbox[2], # Store min/max col for easier sorting/comparison
            'max_c': bbox[3]
        })

    # 4. Group blocks by band and determine horizontal position
    bands = {"Top": [], "Middle": [], "Bottom": []}
    for block in categorized_blocks:
        bands[block['band']].append(block)

    final_blocks_info = []
    for band_name, blocks_in_band in bands.items():
        if not blocks_in_band:
            continue

        # Find min/max columns within this band
        if len(blocks_in_band) == 1:
             min_col_in_band = blocks_in_band[0]['min_c']
             max_col_in_band = blocks_in_band[0]['max_c'] # For a single block min_c and max_c define its span
             leftmost_blocks = blocks_in_band
             rightmost_blocks = blocks_in_band
        else:
            min_col_in_band = min(b['min_c'] for b in blocks_in_band)
            max_col_in_band = max(b['max_c'] for b in blocks_in_band) # Use max_c for rightmost edge
            
            leftmost_blocks = [b for b in blocks_in_band if b['min_c'] == min_col_in_band]
            # Important: Rightmost should be based on the maximum extent (max_c)
            rightmost_blocks = [b for b in blocks_in_band if b['max_c'] == max_col_in_band]


        # Assign horizontal position
        for block in blocks_in_band:
            is_leftmost = block in leftmost_blocks
            is_rightmost = block in rightmost_blocks # Check if it's among those reaching the rightmost extent

            if is_leftmost and is_rightmost: # Single block or blocks spanning the full width available
                position = "Single" # Covers both leftmost and rightmost
            elif is_leftmost:
                position = "Leftmost"
            elif is_rightmost:
                position = "Rightmost"
            else:
                position = "Intermediate"
            
            block['position'] = position
            final_blocks_info.append(block)


    # 5. Apply fill colors based on rules
    for block in final_blocks_info:
        band = block['band']
        position = block['position']
        bbox = block['bbox']
        coords = block['coords']
        fill_color = 0 # Default to white

        if band == "Top":
            if position == "Leftmost" or position == "Single":
                fill_color = 2 # Red
            elif position == "Rightmost":
                fill_color = 4 # Yellow
            # Intermediate remains white (0)
        elif band == "Middle":
            fill_color = 7 # Orange
        elif band == "Bottom":
            if position == "Leftmost" or position == "Single":
                fill_color = 1 # Blue
            elif position == "Rightmost":
                fill_color = 8 # Azure
            # Intermediate remains white (0)

        # Fill the block in the output grid only if fill_color is not white
        if fill_color != 0:
            # Use coordinates for accuracy, especially if blocks aren't perfectly rectangular
            # Though bbox filling is faster if blocks are guaranteed rectangular
            min_r, max_r, min_c, max_c = bbox
            output_grid[min_r:max_r+1, min_c:max_c+1] = fill_color
            # Correct potential overfill if block wasn't truly rectangular
            # Iterate through the bbox area and only color the actual block coords
            # This is safer
            # temp_fill = output_grid[min_r:max_r+1, min_c:max_c+1].copy()
            # for r_idx in range(temp_fill.shape[0]):
            #      for c_idx in range(temp_fill.shape[1]):
            #           grid_r, grid_c = min_r + r_idx, min_c + c_idx
            #           if (grid_r, grid_c) in coords:
            #                output_grid[grid_r, grid_c] = fill_color
            #           else: # This part might be wrong if the original was not 0
            #                # Instead of resetting, just color the coords:
            #                pass # Let's stick to bbox filling assuming rectilinearity
            
            # Refined filling using coordinates:
            for r_coord, c_coord in coords:
                 output_grid[r_coord, c_coord] = fill_color


    return output_grid.tolist()