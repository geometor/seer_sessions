import numpy as np
from typing import List, Tuple, Dict, Optional, Set

"""
Transforms the input grid based on patterns found within red rectangular frames.

The core logic involves:
1. Identifying all distinct rectangular frames made of red (2) pixels.
2. For each frame, determining its size (height x width, specifically 5x5 or 7x7).
3. Identifying the single color of the pattern enclosed within the frame (ignoring the red frame pixels and white background pixels).
4. Dynamically detecting the main L-shaped blue (1) border.
5. Applying a color transformation rule to the enclosed pattern. This rule depends on:
    a. The dimensions of the frame (5x5 or 7x7).
    b. The original color of the enclosed pattern.
    c. For 5x5 frames containing magenta (6) patterns, whether the frame is adjacent (including diagonals) to any blue (1) pixel belonging to the detected main L-shaped border.
6. Preserving all other pixels (background, blue border, red frames) in their original positions.

Color Transformation Rules:
- If frame is 5x5:
    - Green (3) -> Azure (8)
    - Azure (8) -> Magenta (6)
    - Orange (7) -> Green (3)
    - Magenta (6):
        - If adjacent to main Blue (1) border -> Orange (7)
        - Else -> Green (3)
- If frame is 7x7:
    - Green (3) -> Azure (8)
    - Azure (8) -> Yellow (4)
    - Yellow (4) -> Green (3)
"""

# Define color constants for clarity
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
MAGENTA = 6
ORANGE = 7
AZURE = 8

# Define transformation maps based on frame size
TRANSFORM_5x5 = {
    GREEN: AZURE,
    AZURE: MAGENTA,
    ORANGE: GREEN,
    # Magenta is handled separately due to adjacency condition
}

TRANSFORM_7x7 = {
    GREEN: AZURE,
    AZURE: YELLOW,
    YELLOW: GREEN,
}

def _find_red_frames(grid: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Finds all distinct red rectangular frames in the grid.
    A frame is defined by red pixels forming a hollow rectangle.

    Args:
        grid: The input numpy array representing the grid.

    Returns:
        A list of tuples, where each tuple represents a frame:
        (top_row, left_col, height, width).
    """
    frames = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            # Check for potential top-left corner of a red frame that hasn't been visited
            if grid[r, c] == RED and not visited[r, c]:
                # Basic checks for top-left: no red directly above or left (unless edge)
                is_top = (r == 0 or grid[r-1, c] != RED)
                is_left = (c == 0 or grid[r, c-1] != RED)
                # Must have red neighbours down and right to start a frame
                has_right = (c + 1 < cols and grid[r, c+1] == RED)
                has_down = (r + 1 < rows and grid[r+1, c] == RED)

                if not (is_top and is_left and has_right and has_down):
                    continue

                # Determine width of the top edge
                w = 1
                while c + w < cols and grid[r, c + w] == RED:
                    # Ensure this top edge isn't connected vertically upwards mid-way
                    if r > 0 and grid[r-1, c+w] == RED:
                        w = 0 # Invalid frame start
                        break
                    w += 1
                if w <= 1: continue # Needs at least width 2

                # Determine height of the left edge
                h = 1
                while r + h < rows and grid[r + h, c] == RED:
                    # Ensure this left edge isn't connected horizontally leftwards mid-way
                    if c > 0 and grid[r+h, c-1] == RED:
                        h = 0 # Invalid frame start
                        break
                    h += 1
                if h <= 1: continue # Needs at least height 2

                # Verify the rectangle is closed and hollow
                is_complete_frame = True
                # Check bottom edge
                if r + h - 1 >= rows: is_complete_frame = False; continue
                for j in range(w):
                    if c + j >= cols or grid[r + h - 1, c + j] != RED:
                        is_complete_frame = False; break
                if not is_complete_frame: continue

                # Check right edge
                if c + w - 1 >= cols: is_complete_frame = False; continue
                for i in range(h):
                     if r + i >= rows or grid[r + i, c + w - 1] != RED:
                         is_complete_frame = False; break
                if not is_complete_frame: continue

                # Check if the inside is not red (must be hollow)
                # We only need to check one internal pixel for this problem's constraints
                if h > 2 and w > 2:
                    if grid[r + 1, c + 1] == RED:
                        # Check if the whole inside is red (solid block, not frame)
                        is_solid = True
                        for ir in range(r + 1, r + h - 1):
                             for ic in range(c + 1, c + w - 1):
                                 if ir>=rows or ic>=cols or grid[ir, ic] != RED:
                                     is_solid = False
                                     break
                             if not is_solid: break
                        if is_solid: continue # Skip solid red blocks

                # Mark frame pixels as visited and add frame
                # Use try-except for boundary checks, simpler than multiple ifs
                try:
                    frames.append((r, c, h, w))
                    for i in range(h):
                        visited[r + i, c] = True
                        visited[r + i, c + w - 1] = True
                    for j in range(w):
                        visited[r, c + j] = True
                        visited[r + h - 1, c + j] = True
                except IndexError:
                     # This case should ideally not happen with prior checks, but good safety
                     continue

    return frames


def _get_inner_color(grid: np.ndarray, r: int, c: int, h: int, w: int) -> Optional[int]:
    """
    Finds the single dominant non-red, non-white color inside the frame boundaries.
    Assumes frame height/width >= 3.

    Args:
        grid: The input grid.
        r, c, h, w: Frame definition (top_row, left_col, height, width).

    Returns:
        The color code of the inner pattern, or None if no single pattern color found
        or if inner area is empty/white/red.
    """
    inner_color = None
    # Iterate only within the inner area (excluding the frame border)
    for ir in range(r + 1, r + h - 1):
        for ic in range(c + 1, c + w - 1):
            # Ensure indices are within bounds (should be, but safety check)
            if ir >= grid.shape[0] or ic >= grid.shape[1]:
                continue
                
            pixel = grid[ir, ic]
            # Ignore background and frame color
            if pixel != RED and pixel != WHITE:
                if inner_color is None:
                    inner_color = pixel
                # If we find a different non-background/non-frame color, it's not a single pattern
                elif inner_color != pixel:
                    return None # More than one color found
                    
    return inner_color

def _detect_main_l_border(grid: np.ndarray) -> Set[Tuple[int, int]]:
    """
    Detects the coordinates of the main L-shaped blue border.
    Assumes the border is formed by the longest vertical blue segment
    at the minimum blue column index, and the longest horizontal blue
    segment at the maximum blue row index.

    Args:
        grid: The input grid.

    Returns:
        A set of (row, col) tuples representing the coordinates of the L-border.
    """
    rows, cols = grid.shape
    blue_coords = np.argwhere(grid == BLUE)
    
    if blue_coords.shape[0] == 0:
        return set() # No blue pixels

    main_border_coords = set()

    # --- Find Vertical Part ---
    min_c = np.min(blue_coords[:, 1])
    vertical_candidates = sorted([coord[0] for coord in blue_coords if coord[1] == min_c])
    
    if vertical_candidates:
        current_run_start = vertical_candidates[0]
        current_run_len = 1
        best_run_start = current_run_start
        best_run_len = 1

        for i in range(1, len(vertical_candidates)):
            if vertical_candidates[i] == vertical_candidates[i-1] + 1:
                current_run_len += 1
            else:
                if current_run_len > best_run_len:
                    best_run_len = current_run_len
                    best_run_start = current_run_start
                current_run_start = vertical_candidates[i]
                current_run_len = 1
        
        # Check the last run
        if current_run_len > best_run_len:
            best_run_len = current_run_len
            best_run_start = current_run_start

        # Add the longest contiguous vertical segment to the set
        for r_idx in range(best_run_start, best_run_start + best_run_len):
            main_border_coords.add((r_idx, min_c))

    # --- Find Horizontal Part ---
    max_r = np.max(blue_coords[:, 0])
    horizontal_candidates = sorted([coord[1] for coord in blue_coords if coord[0] == max_r])

    if horizontal_candidates:
        current_run_start = horizontal_candidates[0]
        current_run_len = 1
        best_run_start = current_run_start
        best_run_len = 1

        for i in range(1, len(horizontal_candidates)):
            if horizontal_candidates[i] == horizontal_candidates[i-1] + 1:
                current_run_len += 1
            else:
                if current_run_len > best_run_len:
                    best_run_len = current_run_len
                    best_run_start = current_run_start
                current_run_start = horizontal_candidates[i]
                current_run_len = 1
        
        # Check the last run
        if current_run_len > best_run_len:
            best_run_len = current_run_len
            best_run_start = current_run_start
            
        # Add the longest contiguous horizontal segment to the set
        for c_idx in range(best_run_start, best_run_start + best_run_len):
             main_border_coords.add((max_r, c_idx))

    return main_border_coords


def _is_adjacent_to_main_border(grid: np.ndarray, r: int, c: int, h: int, w: int, main_border_coords: Set[Tuple[int, int]]) -> bool:
    """
    Checks if any red pixel of the specified frame's border is adjacent
    (8-way connectivity) to a blue pixel belonging to the main L-border.

    Args:
        grid: The input grid.
        r, c, h, w: Frame definition (top_row, left_col, height, width).
        main_border_coords: A set of (row, col) tuples for the main border.

    Returns:
        True if the frame border is adjacent to the main blue border, False otherwise.
    """
    rows, cols = grid.shape
    
    # Iterate through all pixels forming the border of the frame
    border_pixels = []
    # Top and bottom rows
    for j in range(w):
        if r < rows and c + j < cols: border_pixels.append((r, c + j))
        if r + h - 1 < rows and c + j < cols: border_pixels.append((r + h - 1, c + j))
    # Left and right columns (excluding corners already added)
    for i in range(1, h - 1):
        if r + i < rows and c < cols: border_pixels.append((r + i, c))
        if r + i < rows and c + w - 1 < cols: border_pixels.append((r + i, c + w - 1))

    # Check 8 neighbours for each border pixel
    for br, bc in border_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self

                nr, nc = br + dr, bc + dc

                # Check if neighbour is within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if neighbour is blue AND part of the main L-border set
                    if grid[nr, nc] == BLUE and (nr, nc) in main_border_coords:
                        return True # Found adjacency to the main border

    return False # No adjacency found after checking all border pixels and neighbours


def _apply_transformation(output_grid: np.ndarray, r: int, c: int, h: int, w: int, c_in: int, c_out: int):
    """
    Changes the color of the inner pattern within the frame boundaries.
    Only pixels matching the original inner color (c_in) are changed.

    Args:
        output_grid: The grid to modify (numpy array).
        r, c, h, w: Frame definition.
        c_in: The original color of the pattern.
        c_out: The target color for the pattern.
    """
    rows, cols = output_grid.shape
    # Iterate through the inner area of the frame
    for ir in range(r + 1, r + h - 1):
        for ic in range(c + 1, c + w - 1):
            # Check bounds before accessing grid element
            if 0 <= ir < rows and 0 <= ic < cols:
                 # Only change pixels matching the original inner color
                 if output_grid[ir, ic] == c_in:
                    output_grid[ir, ic] = c_out


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Main function to transform the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid_np = grid_np.copy()

    # Detect the main L-shaped blue border coordinates once
    main_border_coords = _detect_main_l_border(grid_np)

    # Find all red frames
    frames = _find_red_frames(grid_np)

    # Process each identified frame
    for r, c, h, w in frames:
        # Identify the color inside the frame
        c_in = _get_inner_color(grid_np, r, c, h, w)

        # Skip if no valid single inner pattern color found
        if c_in is None or c_in == WHITE or c_in == RED:
            continue

        c_out = None # Target color initialization

        # Determine the target color based on frame size and inner color
        if h == 5 and w == 5:
            if c_in == MAGENTA:
                # Special case: Magenta in 5x5 frame depends on adjacency to main border
                if _is_adjacent_to_main_border(grid_np, r, c, h, w, main_border_coords):
                    c_out = ORANGE
                else:
                    c_out = GREEN
            elif c_in in TRANSFORM_5x5:
                # Standard 5x5 transformation
                c_out = TRANSFORM_5x5[c_in]

        elif h == 7 and w == 7:
            if c_in in TRANSFORM_7x7:
                # Standard 7x7 transformation
                c_out = TRANSFORM_7x7[c_in]

        # If a valid transformation rule resulted in a target color, apply it
        if c_out is not None:
            _apply_transformation(output_grid_np, r, c, h, w, c_in, c_out)

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()