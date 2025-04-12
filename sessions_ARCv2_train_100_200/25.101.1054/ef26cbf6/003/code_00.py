"""
Transforms an input grid based on region analysis and color replacement rules.

1.  The grid is partitioned into contiguous regions of non-yellow (4) pixels, using yellow pixels as boundaries.
2.  Regions are classified as either 'source' or 'target':
    - A 'source region' contains exactly one pixel of a unique color (not white 0, yellow 4, or blue 1) and no blue pixels. Its unique color is the 'source color'.
    - A 'target region' contains one or more blue (1) pixels and no other unique non-white/yellow colors.
3.  A correspondence is established between each target region and exactly one source region based on adjacency across a yellow separator:
    - Priority is implicitly given by the grid layout (either vertical or horizontal adjacency applies).
    - Vertical Adjacency: The source region is immediately above the target region, separated by a continuous horizontal segment of yellow pixels along their shared boundary.
    - Horizontal Adjacency: The source region is immediately to the left of the target region, separated by a continuous vertical segment of yellow pixels along their shared boundary.
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
                        if grid[nr, nc] != 4 and not visited[nr, nc]:
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
        # A region is a source only if it has exactly one unique 'other' color AND no blue pixels.
        if len(other_colors) == 1 and not blue_coords_list:
             source_color = list(other_colors)[0] # Get the single element

        bbox = _calculate_bounding_box(coords)

        region_data.append({
            'id': i, # Assign an ID for potential debugging
            'coords': coords,
            # Store list if blue found, else None
            'blue_coords': blue_coords_list if blue_coords_list else None,
            'source_color': source_color,
            'bbox': bbox
        })
    return region_data

def _is_horizontal_separator(grid: np.ndarray, r: int, c1: int, c2: int) -> bool:
    """ Checks if row r between columns c1 and c2 (inclusive) is entirely yellow(4) """
    height, width = grid.shape
    if r < 0 or r >= height: return False # Row out of bounds
    # Ensure column indices are valid and within grid bounds
    c_start = max(0, c1)
    c_end = min(width - 1, c2)
    if c_start > c_end: return False # No valid column range to check (e.g., if c1 > c2)

    # Check if all cells in the specified range within the row are yellow
    return np.all(grid[r, c_start : c_end + 1] == 4)

def _is_vertical_separator(grid: np.ndarray, c: int, r1: int, r2: int) -> bool:
    """ Checks if col c between rows r1 and r2 (inclusive) is entirely yellow(4) """
    height, width = grid.shape
    if c < 0 or c >= width: return False # Column out of bounds
    # Ensure row indices are valid and within grid bounds
    r_start = max(0, r1)
    r_end = min(height - 1, r2)
    if r_start > r_end: return False # No valid row range to check (e.g., if r1 > r2)

    # Check if all cells in the specified range within the column are yellow
    return np.all(grid[r_start : r_end + 1, c] == 4)

def _find_correspondence(source_regions: list[dict], target_regions: list[dict], grid: np.ndarray) -> dict:
    """
    Finds the mapping from each target region to its corresponding source color.
    Uses adjacency rules:
    1. Vertical: Source directly above Target, separated by horizontal yellow line segment.
    2. Horizontal: Source directly left of Target, separated by vertical yellow line segment.
    Returns a dictionary mapping frozenset(target_coords) -> source_color.
    """
    mapping = {}

    for target in target_regions:
        # Use frozenset of coordinates as a hashable key for the mapping
        target_coords_frozen = frozenset(target['coords'])
        # Should not happen with current analysis logic, but safeguard
        if not target['blue_coords']: continue

        matched_source_color = None
        t_min_r, t_min_c, t_max_r, t_max_c = target['bbox']

        # Iterate through potential source regions to find a match
        for source in source_regions:
            # Skip if this region doesn't have a source color defined
            if source['source_color'] is None: continue

            s_min_r, s_min_c, s_max_r, s_max_c = source['bbox']

            # --- Check Vertical Adjacency ---
            # Condition 1: Source's bottom edge is exactly one row above Target's top edge
            if s_max_r == t_min_r - 1:
                # Condition 2: Horizontal overlap exists between source and target bounding boxes
                overlap_min_c = max(s_min_c, t_min_c)
                overlap_max_c = min(s_max_c, t_max_c)
                if overlap_min_c <= overlap_max_c:
                    # Condition 3: The row between them (at row s_max_r = t_min_r - 1)
                    # must be a yellow separator *within the overlapping columns*
                    separator_row_idx = s_max_r
                    if _is_horizontal_separator(grid, separator_row_idx, overlap_min_c, overlap_max_c):
                         matched_source_color = source['source_color']
                         break # Found vertical match, stop searching sources for this target

            # --- Check Horizontal Adjacency (only if vertical didn't match) ---
            # Condition 1: Source's right edge is exactly one column left of Target's left edge
            if matched_source_color is None and s_max_c == t_min_c - 1:
                 # Condition 2: Vertical overlap exists between source and target bounding boxes
                overlap_min_r = max(s_min_r, t_min_r)
                overlap_max_r = min(s_max_r, t_max_r)
                if overlap_min_r <= overlap_max_r:
                    # Condition 3: The column between them (at col s_max_c = t_min_c - 1)
                    # must be a yellow separator *within the overlapping rows*
                    separator_col_idx = s_max_c
                    if _is_vertical_separator(grid, separator_col_idx, overlap_min_r, overlap_max_r):
                        matched_source_color = source['source_color']
                        break # Found horizontal match, stop searching sources for this target

        # If a match was found (either vertical or horizontal), add it to the mapping
        if matched_source_color is not None:
             mapping[target_coords_frozen] = matched_source_color

    return mapping

# --- Main Transform Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(grid)

    # 1. Find all distinct regions separated by yellow(4) lines
    regions_coords = _find_regions(grid)

    # 2. Analyze properties of each region (source color, blue pixels, bounding box)
    #    Classifies into potential sources and targets based on content.
    region_data = _analyze_regions(grid, regions_coords)

    # 3. Separate into actual source and target lists based on analysis
    source_regions = [r for r in region_data if r['source_color'] is not None]
    target_regions = [r for r in region_data if r['blue_coords'] is not None]

    # 4. Determine the correspondence between target regions and source regions
    #    Returns a map: { frozenset(target_coords) -> source_color }
    mapping = _find_correspondence(source_regions, target_regions, grid)

    # 5. Apply the transformations based on the mapping
    #    Iterate through all identified target regions
    for region in target_regions:
        target_coords_frozen = frozenset(region['coords'])
        # Check if a corresponding source was found for this target region in the mapping
        if target_coords_frozen in mapping:
            source_color = mapping[target_coords_frozen]
            # Replace all blue pixels (stored in 'blue_coords') in this target region
            # with the corresponding source color in the output grid.
            for r, c in region['blue_coords']:
                output_grid[r, c] = source_color

    # Convert the final numpy array back to a list of lists format for the expected output
    return output_grid.tolist()