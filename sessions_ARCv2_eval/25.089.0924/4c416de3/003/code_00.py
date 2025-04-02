import numpy as np
from collections import Counter
import math
from scipy.ndimage import label

"""
Transformation Rule (v3.1):

1. Identify the background color (BGC) as the most frequent color.
2. Find all distinct contiguous regions of white (0) pixels.
3. For each white region:
    a. Determine its bounding box (r_min, c_min) to (r_max, c_max).
    b. Identify the four potential corner background pixels located diagonally outside the bounding box: 
       TL=(r_min-1, c_min-1), TR=(r_min-1, c_max+1), BL=(r_max+1, c_min-1), BR=(r_max+1, c_max+1). 
       Validate that these corners are within grid bounds and have the BGC.
    c. Find all 'color pixels' (non-BGC, non-white) associated with this region. A color pixel is associated if it's within the bounding box OR cardinally adjacent to any white pixel of this region.
    d. Assign a color to each valid corner pixel based on proximity: For each color pixel, calculate its Euclidean distance to each valid corner pixel. The color of the *closest* color pixel is assigned to the corner. Ties are implicitly broken by processing order (last closest pixel wins).
    e. For each corner that received a color assignment, paint a specific 2x2 block in the output grid with that color. The top-left coordinate of the 2x2 block depends on the corner type:
        - TL corner (cr, cc) -> paint block starting at (cr, cc+1)
        - TR corner (cr, cc) -> paint block starting at (cr, cc-1)
        - BL corner (cr, cc) -> paint block starting at (cr-1, cc+1)
        - BR corner (cr, cc) -> paint block starting at (cr-1, cc-1)
4. Pixels not part of these 2x2 blocks retain their original color.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid, ignoring white (0) if possible."""
    colors, counts = np.unique(grid, return_counts=True)
    non_white_indices = np.where(colors != 0)[0]
    
    if len(non_white_indices) > 0:
        # Find the most frequent non-white color
        max_count_idx_non_white = non_white_indices[np.argmax(counts[non_white_indices])]
        return colors[max_count_idx_non_white]
    else:
        # If only white exists, return white (or handle as error/edge case)
        # For robustness, return the most frequent overall if no non-white
        return colors[np.argmax(counts)]


def get_bounding_box(coords):
    """Calculates the bounding box for a list of (row, col) coordinates."""
    if not coords:
        return None
    rows, cols = zip(*coords)
    return min(rows), min(cols), max(rows), max(cols)

def euclidean_distance(p1, p2):
    """Calculates Euclidean distance between two points (r1, c1) and (r2, c2)."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_region_pixels(grid, region_coords_set):
    """Finds color pixels associated with a white region."""
    height, width = grid.shape
    bbox = get_bounding_box(list(region_coords_set))
    if bbox is None:
        return []
    
    r_min, c_min, r_max, c_max = bbox
    associated_pixels = []
    processed_coords = set() # Avoid duplicates if inside bbox AND adjacent

    # Check inside bounding box
    for r in range(r_min, r_max + 1):
        for c in range(c_min, c_max + 1):
             # Ensure coords are valid before checking grid value
            if 0 <= r < height and 0 <= c < width:
                color = grid[r, c]
                # Check if it's a color pixel (not white, not background - handled later)
                if color != 0:
                    coord = (r, c)
                    if coord not in processed_coords:
                         associated_pixels.append((coord, color))
                         processed_coords.add(coord)


    # Check adjacency to white pixels in the region
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # R, L, D, U
    for wr, wc in region_coords_set:
        for dr, dc in directions:
            nr, nc = wr + dr, wc + dc
            if 0 <= nr < height and 0 <= nc < width:
                color = grid[nr, nc]
                # Check if it's a color pixel
                if color != 0:
                    coord = (nr, nc)
                    if coord not in processed_coords:
                        associated_pixels.append((coord, color))
                        processed_coords.add(coord)
                        
    return associated_pixels


def transform(input_grid):
    """
    Applies the transformation rule based on white regions, corners, 
    and closest color pixels.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # 1. Identify background color
    bgc = find_background_color(input_array)

    # 2. Find white regions
    white_mask = (input_array == 0)
    labeled_array, num_labels = label(white_mask)

    # 3. Process each white region
    for i in range(1, num_labels + 1):
        region_coords = list(zip(*np.where(labeled_array == i)))
        if not region_coords:
            continue
            
        region_coords_set = set(region_coords)

        # a. Calculate bounding box
        bbox = get_bounding_box(region_coords)
        if bbox is None: continue
        r_min, c_min, r_max, c_max = bbox

        # b. Identify valid corner background pixels
        potential_corners = {
            "TL": (r_min - 1, c_min - 1),
            "TR": (r_min - 1, c_max + 1),
            "BL": (r_max + 1, c_min - 1),
            "BR": (r_max + 1, c_max + 1)
        }
        valid_corners = {}
        for name, (cr, cc) in potential_corners.items():
            if 0 <= cr < height and 0 <= cc < width and input_array[cr, cc] == bgc:
                valid_corners[name] = (cr, cc)

        if not valid_corners: # Skip region if no valid corners
             continue

        # c. Find associated color pixels (filtering out BGC here)
        all_associated = get_region_pixels(input_array, region_coords_set)
        color_pixels = [p for p in all_associated if p[1] != bgc]
        
        if not color_pixels: # Skip region if no associated color pixels
            continue

        # d. Assign colors to corners based on distance
        assignments = {name: {'dist': float('inf'), 'color': None} for name in valid_corners}
        for (pr, pc), color in color_pixels:
            pixel_coord = (pr, pc)
            for name, corner_coord in valid_corners.items():
                d = euclidean_distance(pixel_coord, corner_coord)
                if d < assignments[name]['dist']:
                    assignments[name]['dist'] = d
                    assignments[name]['color'] = color
                # Implicit tie-breaking: last pixel processed with equal min distance wins

        # e. Paint 2x2 blocks
        for name, corner_coord in valid_corners.items():
            assigned_color = assignments[name]['color']
            if assigned_color is not None:
                cr, cc = corner_coord
                start_r, start_c = -1, -1 # Initialize invalid start coords

                if name == "TL":
                    start_r, start_c = cr, cc + 1
                elif name == "TR":
                    start_r, start_c = cr, cc - 1
                elif name == "BL":
                    start_r, start_c = cr - 1, cc + 1
                elif name == "BR":
                    start_r, start_c = cr - 1, cc - 1

                # Paint the 2x2 block if start coords are valid
                if start_r != -1:
                    for r_offset in range(2):
                        for c_offset in range(2):
                            paint_r, paint_c = start_r + r_offset, start_c + c_offset
                            # Check bounds before painting
                            if 0 <= paint_r < height and 0 <= paint_c < width:
                                output_array[paint_r, paint_c] = assigned_color

    return output_array.tolist()