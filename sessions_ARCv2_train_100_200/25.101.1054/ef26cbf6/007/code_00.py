"""
Transforms an input grid based on region analysis and color replacement rules across yellow separators.

1.  The grid is partitioned into contiguous regions of non-yellow (4) pixels, using yellow pixels as boundaries.
2.  Regions are classified as either 'source' or 'target':
    - A 'source region' contains exactly one pixel of a unique color (not white 0, yellow 4, or blue 1) and no blue pixels. Its unique color is the 'source color'.
    - A 'target region' contains one or more blue (1) pixels and no other unique non-white/yellow colors.
3.  A correspondence is established between each target region and exactly one source region based on adjacency across a single row or column of yellow pixels:
    - Vertical Adjacency: The source region is above the target region such that `source_max_row + 1 == target_min_row - 1`, AND the intervening row (`source_max_row + 1`) is entirely yellow within their horizontally overlapping columns.
    - Horizontal Adjacency: The source region is to the left of the target region such that `source_max_col + 1 == target_min_col - 1`, AND the intervening column (`source_max_col + 1`) is entirely yellow within their vertically overlapping rows.
4.  All blue (1) pixels within each target region are replaced in the output grid by the source color of its corresponding source region.
5.  All other pixels (white, yellow, source colors) remain unchanged.
"""

import numpy as np
from collections import deque

# --- Helper Functions ---

def _get_neighbors(r: int, c: int, height: int, width: int) -> list[tuple[int, int]]:
    """ Get 4-directional neighbors within grid bounds """
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def _find_regions(grid: np.ndarray) -> list[set[tuple[int, int]]]:
    """
    Finds connected regions of non-yellow(4) cells using BFS.
    Yellow cells act as boundaries and are not part of any region.
    Returns a list of sets, where each set contains the (row, col) coordinates of a region.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            # Start BFS only if cell is not yellow and not visited
            if grid[r, c] != 4 and not visited[r, c]:
                region_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    region_coords.add((row, col))

                    # Explore neighbors
                    for nr, nc in _get_neighbors(row, col, height, width):
                        # Add neighbor to queue if valid, not yellow, and not visited
                        if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] != 4 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if region_coords:
                    regions.append(region_coords)
    return regions

def _calculate_bounding_box(coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """ Calculates min_row, min_col, max_row, max_col for a set of coordinates """
    if not coords:
        return -1, -1, -1, -1 # Indicate empty region
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)

def _analyze_regions(grid: np.ndarray, regions: list[set[tuple[int, int]]]) -> list[dict]:
    """
    Analyzes each region to find its properties:
    - coords: set of (row, col) tuples in the region.
    - blue_coords: list of coordinates containing blue (1) pixels, or None.
    - source_color: the unique non-white(0)/yellow(4)/blue(1) color, if one exists, or None.
    - bbox: bounding box tuple (min_r, min_c, max_r, max_c).
    """
    region_data = []
    for i, coords in enumerate(regions):
        blue_coords_list = []
        # Using a set to find unique non-white/yellow/blue colors easily
        other_colors = set()

        for r, c in coords:
            color = grid[r, c]
            if color == 1: # Blue
                blue_coords_list.append((r, c))
            # Check for potential source color (not white, yellow, or blue)
            elif color not in [0, 4]:
                other_colors.add(color)

        source_color = None
        is_target = bool(blue_coords_list)
        is_potential_source = len(other_colors) == 1

        # Define as source only if exactly one 'other' color AND no blue pixels.
        # Define as target only if blue pixels exist AND no 'other' colors.
        # This prevents a region being both.
        if is_potential_source and not is_target:
             source_color = list(other_colors)[0]
             region_type = 'source'
        elif is_target and not is_potential_source:
             region_type = 'target'
        else:
            region_type = 'other' # Neither source nor target based on strict definition


        bbox = _calculate_bounding_box(coords)

        region_data.append({
            'id': i, # Assign an ID for potential debugging
            'coords': coords,
            'blue_coords': blue_coords_list if region_type == 'target' else None,
            'source_color': source_color if region_type == 'source' else None,
            'bbox': bbox,
            'type': region_type
        })
    return region_data

def _is_horizontal_separator(grid: np.ndarray, r: int, c1: int, c2: int) -> bool:
    """ Checks if row r between columns c1 and c2 (inclusive) is entirely yellow(4) """
    height, width = grid.shape
    if r < 0 or r >= height: return False # Row out of bounds
    # Ensure column indices are valid and within grid bounds
    c_start = max(0, c1)
    c_end = min(width - 1, c2)
    if c_start > c_end: return False # No valid column range to check

    # Check if all cells in the specified range within the row are yellow
    return np.all(grid[r, c_start : c_end + 1] == 4)

def _is_vertical_separator(grid: np.ndarray, c: int, r1: int, r2: int) -> bool:
    """ Checks if col c between rows r1 and r2 (inclusive) is entirely yellow(4) """
    height, width = grid.shape
    if c < 0 or c >= width: return False # Column out of bounds
    # Ensure row indices are valid and within grid bounds
    r_start = max(0, r1)
    r_end = min(height - 1, r2)
    if r_start > r_end: return False # No valid row range to check

    # Check if all cells in the specified range within the column are yellow
    return np.all(grid[r_start : r_end + 1, c] == 4)

def _find_correspondence(source_regions: list[dict], target_regions: list[dict], grid: np.ndarray) -> dict:
    """
    Finds the mapping from each target region to its corresponding source color.
    Uses adjacency rules across a single yellow separator row/column:
    1. Vertical: Source above Target, separated by one horizontal yellow row.
    2. Horizontal: Source left of Target, separated by one vertical yellow column.
    Returns a dictionary mapping frozenset(target_coords) -> source_color.
    """
    mapping = {}

    for target in target_regions:
        # Use frozenset of coordinates as a hashable key for the mapping
        target_coords_frozen = frozenset(target['coords'])
        if not target['blue_coords']: continue # Should already be filtered, but safety check

        matched_source_color = None
        t_min_r, t_min_c, t_max_r, t_max_c = target['bbox']

        # Iterate through potential source regions to find a match
        for source in source_regions:
            if source['source_color'] is None: continue # Skip non-sources

            s_min_r, s_min_c, s_max_r, s_max_c = source['bbox']

            # --- Check Vertical Adjacency ---
            # Condition 1: Exactly one row separates them (source is above target)
            separator_row_idx = s_max_r + 1
            if separator_row_idx == t_min_r - 1: # Check if target starts 2 rows below source end
                # Condition 2: Horizontal overlap exists
                overlap_min_c = max(s_min_c, t_min_c)
                overlap_max_c = min(s_max_c, t_max_c)
                if overlap_min_c <= overlap_max_c:
                    # Condition 3: The separating row IS a horizontal yellow separator
                    # within the overlapping columns.
                    if _is_horizontal_separator(grid, separator_row_idx, overlap_min_c, overlap_max_c):
                         matched_source_color = source['source_color']
                         break # Found vertical match

            # --- Check Horizontal Adjacency (only if vertical didn't match) ---
             # Condition 1: Exactly one col separates them (source is left of target)
            separator_col_idx = s_max_c + 1
            if matched_source_color is None and separator_col_idx == t_min_c - 1: # Check if target starts 2 cols right of source end
                # Condition 2: Vertical overlap exists
                overlap_min_r = max(s_min_r, t_min_r)
                overlap_max_r = min(s_max_r, t_max_r)
                if overlap_min_r <= overlap_max_r:
                    # Condition 3: The separating col IS a vertical yellow separator
                    # within the overlapping rows.
                    if _is_vertical_separator(grid, separator_col_idx, overlap_min_r, overlap_max_r):
                        matched_source_color = source['source_color']
                        break # Found horizontal match

        # If a match was found, add it to the mapping
        if matched_source_color is not None:
             mapping[target_coords_frozen] = matched_source_color

    return mapping

# --- Main Transform Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic: identifies regions, finds source-target
    correspondence across yellow separators, and replaces blue pixels in target
    regions with the corresponding source color.
    """
    # Convert input list of lists to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy of the grid to modify, preserving the original input
    output_grid = np.copy(grid)

    # 1. Identify all contiguous regions of non-yellow (4) pixels
    regions_coords = _find_regions(grid)

    # 2. Analyze each region to classify it and extract properties
    region_data = _analyze_regions(grid, regions_coords)

    # 3. Separate classified regions into source and target lists based on 'type'
    source_regions = [r for r in region_data if r['type'] == 'source']
    target_regions = [r for r in region_data if r['type'] == 'target']

    # 4. Determine the correspondence: map each target region to its adjacent source color
    #    The mapping uses frozenset(target_coords) as keys and source_color as values
    mapping = _find_correspondence(source_regions, target_regions, grid)

    # 5. Apply the color replacements based on the determined mapping
    #    Iterate through the target regions identified earlier
    for region in target_regions:
        target_coords_frozen = frozenset(region['coords'])
        # Check if a corresponding source color was found for this target region
        if target_coords_frozen in mapping:
            source_color = mapping[target_coords_frozen]
            # Replace all blue pixels (stored in 'blue_coords') within this target region
            # in the output grid with the corresponding source color.
            for r, c in region['blue_coords']:
                output_grid[r, c] = source_color

    # Convert the final numpy array back to a list of lists format
    return output_grid.tolist()