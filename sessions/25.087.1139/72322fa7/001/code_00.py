import numpy as np
from copy import deepcopy

"""
Transformation Rule:
1. Initialize the output grid as an identical copy of the input grid.
2. Identify all distinct "source patterns" present in the input grid. A source pattern is a small, recognizable motif like `X C X` (horizontal or vertical) or a plus shape centered on `C` with arms `X`, where `C` and `X` are non-white colors. Note the central color `C` and the structural/flanking color `X` for each source pattern. The known source patterns are:
    - Horizontal `4 8 4` (Yellow-Azure-Yellow): C=8, X=4
    - Vertical `1 3 1` (Blue-Green-Blue): C=3, X=1
    - Plus shape `8 6 8` (Azure-Magenta-Azure arms/center): C=6, X=8
    - Horizontal `8 2 8` (Azure-Red-Azure): C=2, X=8
3. Identify all "target markers" in the input grid. A target marker is either:
    a. An isolated single pixel of color `C`, where `C` matches the central color of at least one identified source pattern. A pixel is isolated if all 8 neighbors are white (0).
    b. A three-pixel sequence `X 0 X` (either horizontal `[X, 0, X]` or vertical `[[X], [0], [X]]`), where `X` matches the structural/flanking color of at least one identified source pattern. The center of this marker is the location of the white (0) pixel.
4. For each identified target marker:
    a. Determine the corresponding source pattern:
        i. If the marker is an isolated pixel `C`, select the source pattern whose central color is `C`.
        ii. If the marker is `X 0 X`, select the source pattern whose structural/flanking color is `X`. (Assume only one such source pattern exists for each relevant `C` or `X` in a given input).
    b. Determine the center location of the target marker (the position of the isolated pixel `C` or the central `0` in `X 0 X`).
    c. Copy the selected source pattern onto the output grid, centering the pattern at the determined target marker location. Overwrite any existing pixels at the destination.
5. Return the modified output grid.
"""

def is_valid(r, c, height, width):
    """Checks if coordinates (r, c) are within the grid bounds."""
    return 0 <= r < height and 0 <= c < width

def find_source_patterns(grid):
    """
    Identifies all predefined source patterns within the grid.

    Returns:
        tuple: (patterns_by_center, patterns_by_flank)
            patterns_by_center (dict): Maps central color C to pattern data.
            patterns_by_flank (dict): Maps flanking/structural color X to pattern data.
            pattern_data (dict): Contains 'pattern_rel' (list of (dr, dc, color)), 'C', 'X'.
    """
    height, width = grid.shape
    patterns_by_center = {}
    patterns_by_flank = {}
    
    # Define known pattern structures relative to center (0,0)
    # Format: (C, X, [(dr, dc, expected_color), ...])
    known_patterns_defs = [
        (8, 4, [(0, -1, 4), (0, 0, 8), (0, 1, 4)]),  # 4 8 4 horizontal
        (3, 1, [(-1, 0, 1), (0, 0, 3), (1, 0, 1)]),  # 1 3 1 vertical
        (6, 8, [(-1, 0, 8), (1, 0, 8), (0, -1, 8), (0, 1, 8), (0, 0, 6)]), # 8 6 8 plus
        (2, 8, [(0, -1, 8), (0, 0, 2), (0, 1, 8)]),  # 8 2 8 horizontal
    ]

    # Iterate through potential centers in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell could be the center of any known pattern
            for C, X, pattern_rel in known_patterns_defs:
                # The center pixel must match the pattern's center color
                center_pixel_def = next((p for p in pattern_rel if p[0] == 0 and p[1] == 0), None)
                if center_pixel_def is None or grid[r, c] != center_pixel_def[2]:
                    continue # Optimization: skip if center pixel doesn't match

                match = True
                actual_pixels_rel = []
                for dr, dc, expected_color in pattern_rel:
                    nr, nc = r + dr, c + dc
                    # Check if the relative position is valid and has the expected color
                    if not is_valid(nr, nc, height, width) or grid[nr, nc] != expected_color:
                        match = False
                        break
                    actual_pixels_rel.append((dr, dc, expected_color))
                
                # If all parts of the pattern matched
                if match:
                    pattern_data = {'pattern_rel': actual_pixels_rel, 'C': C, 'X': X}
                    # Store the found pattern data, indexed by C and X
                    # If multiple patterns share C or X, the last one found will overwrite previous ones.
                    # This seems acceptable based on the problem's examples.
                    if C is not None:
                        patterns_by_center[C] = pattern_data
                    if X is not None:
                        # Handle the case where X=8 maps to two patterns (plus and horiz).
                        # The problem seems deterministic; perhaps only one X=8 pattern exists per input,
                        # or the marker type implicitly disambiguates (though not stated).
                        # Let's assume the last found for a given X is sufficient or contextually correct.
                        patterns_by_flank[X] = pattern_data
                        
    return patterns_by_center, patterns_by_flank

def find_target_markers(grid):
    """
    Identifies target markers (isolated pixels or X 0 X patterns).

    Returns:
        list: A list of tuples: (marker_type, color, center_r, center_c)
              marker_type is 'isolated' or 'placeholder'.
              color is C for isolated, X for placeholder.
    """
    height, width = grid.shape
    markers = []
    
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            
            # Check for isolated non-white pixel
            if color != 0:
                is_isolated = True
                # Check all 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        # If a neighbor is within bounds and not white, it's not isolated
                        if is_valid(nr, nc, height, width) and grid[nr, nc] != 0:
                            is_isolated = False
                            break
                    if not is_isolated:
                        break
                # If all neighbors were checked and none were non-white
                if is_isolated:
                    markers.append(('isolated', color, r, c))
                    # If it's an isolated marker, don't check if it's also a placeholder center
                    continue 

            # Check for placeholder pattern X 0 X centered at (r, c) if current cell is white
            if color == 0:
                # Check Horizontal: X 0 X
                # Check if left and right neighbors are valid, non-white, and equal
                c_left, c_right = c - 1, c + 1
                if is_valid(r, c_left, height, width) and is_valid(r, c_right, height, width):
                    left_color = grid[r, c_left]
                    right_color = grid[r, c_right]
                    if left_color != 0 and left_color == right_color:
                        # Found horizontal placeholder
                        markers.append(('placeholder', left_color, r, c))
                        # Prioritize horizontal if both exist? Examples don't show overlap. Let's allow both potential matches.
                        # No 'continue' here allows checking vertical too, though unlikely relevant based on examples.

                # Check Vertical: X / 0 / X
                # Check if top and bottom neighbors are valid, non-white, and equal
                r_top, r_bottom = r - 1, r + 1
                if is_valid(r_top, c, height, width) and is_valid(r_bottom, c, height, width):
                    top_color = grid[r_top, c]
                    bottom_color = grid[r_bottom, c]
                    if top_color != 0 and top_color == bottom_color:
                        # Found vertical placeholder
                        markers.append(('placeholder', top_color, r, c))

    return markers

def stamp_pattern(grid, center_r, center_c, pattern_rel):
    """Stamps the pattern onto the grid centered at the given coordinates."""
    height, width = grid.shape
    for dr, dc, color in pattern_rel:
        r, c = center_r + dr, center_c + dc
        # Ensure the target pixel is within grid bounds before writing
        if is_valid(r, c, height, width):
            grid[r, c] = color

def transform(input_grid_list):
    """
    Applies the transformation rule: finds source patterns and target markers,
    then copies the corresponding patterns to the marker locations.
    """
    # Convert list of lists to numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    # Initialize output grid as a deep copy of the input
    output_grid = deepcopy(input_grid)
    height, width = input_grid.shape

    # 1. Find all unique source patterns present in the input grid
    patterns_by_center, patterns_by_flank = find_source_patterns(input_grid)

    # 2. Find all target markers (isolated pixels or placeholders)
    markers = find_target_markers(input_grid)

    # 3. For each marker, find the corresponding pattern and stamp it
    for marker_type, color, center_r, center_c in markers:
        pattern_data = None
        # Match marker to pattern based on type and color
        if marker_type == 'isolated':
            # Isolated marker color C should match pattern's central color C
            if color in patterns_by_center:
                pattern_data = patterns_by_center[color]
        elif marker_type == 'placeholder':
            # Placeholder marker color X should match pattern's flanking color X
            if color in patterns_by_flank:
                pattern_data = patterns_by_flank[color]

        # If a corresponding pattern was found for the marker
        if pattern_data:
            # Stamp the found pattern onto the output grid centered at the marker location
            stamp_pattern(output_grid, center_r, center_c, pattern_data['pattern_rel'])

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()