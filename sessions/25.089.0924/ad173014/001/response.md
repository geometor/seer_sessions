```python
import numpy as np
from typing import List, Tuple, Dict, Optional

"""
This module transforms an input grid based on patterns found within red rectangular frames.

The core logic involves:
1. Identifying all distinct rectangular frames made of red (2) pixels.
2. For each frame, determining its size (height x width).
3. Identifying the single color of the pattern enclosed within the frame (ignoring the red frame pixels and white background pixels).
4. Applying a color transformation rule to the enclosed pattern. This rule depends on:
    a. The dimensions of the frame (specifically 5x5 or 7x7).
    b. The original color of the enclosed pattern.
    c. For 5x5 frames containing magenta (6) patterns, whether the frame is adjacent (including diagonals) to any blue (1) pixel (part of the L-shaped border).
5. Preserving all other pixels (background, blue border, red frames) in their original positions.

Color Transformation Rules:
- If frame is 5x5:
    - Green (3) -> Azure (8)
    - Azure (8) -> Magenta (6)
    - Orange (7) -> Green (3)
    - Magenta (6):
        - If adjacent to Blue (1) -> Orange (7)
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
                # Check if it's a real top-left corner (no red directly above or left, unless it's the edge)
                is_top = (r == 0 or grid[r-1, c] != RED)
                is_left = (c == 0 or grid[r, c-1] != RED)
                
                # Also check if the pixel below and right are red (start of frame sides)
                has_right = (c + 1 < cols and grid[r, c+1] == RED)
                has_down = (r + 1 < rows and grid[r+1, c] == RED)

                if is_top and is_left and has_right and has_down:
                    # Found a potential top-left corner, now determine width and height
                    
                    # Determine width
                    w = 1
                    while c + w < cols and grid[r, c + w] == RED:
                        # Check if this horizontal line is valid (no red above)
                        if r > 0 and grid[r-1, c+w] == RED:
                            w = 0 # Invalid frame start
                            break
                        w += 1
                    if w == 0: continue # Not a valid top edge start

                    # Determine height
                    h = 1
                    while r + h < rows and grid[r + h, c] == RED:
                         # Check if this vertical line is valid (no red to the left)
                        if c > 0 and grid[r+h, c-1] == RED:
                            h = 0 # Invalid frame start
                            break
                        h += 1
                    if h == 0: continue # Not a valid left edge start
                    
                    # Verify the frame is closed and rectangular
                    is_closed = True
                    # Check bottom edge
                    for i in range(w):
                        if r + h - 1 >= rows or c + i >= cols or grid[r + h - 1, c + i] != RED:
                            is_closed = False
                            break
                    if not is_closed: continue
                    # Check right edge
                    for i in range(h):
                         if r + i >= rows or c + w - 1 >= cols or grid[r + i, c + w - 1] != RED:
                            is_closed = False
                            break
                    if not is_closed: continue

                    # Verify interior is not red (except maybe the pattern itself)
                    # A simple check at the center might suffice for this problem's structure
                    inner_r, inner_c = r + h // 2, c + w // 2
                    if grid[inner_r, inner_c] == RED:
                         # Check if the whole inner area is red - if so, it's not a frame with a pattern
                         is_solid = True
                         for ir in range(r + 1, r + h - 1):
                             for ic in range(c + 1, c + w - 1):
                                 if grid[ir, ic] != RED:
                                     is_solid = False
                                     break
                             if not is_solid: break
                         if is_solid: continue # Skip solid red blocks

                    # Mark frame pixels as visited and add frame to list
                    frames.append((r, c, h, w))
                    for i in range(h):
                        visited[r + i, c] = True
                        visited[r + i, c + w - 1] = True
                    for j in range(w):
                        visited[r, c + j] = True
                        visited[r + h - 1, c + j] = True
                        
    return frames

def _get_inner_color(grid: np.ndarray, r: int, c: int, h: int, w: int) -> Optional[int]:
    """
    Finds the single dominant non-red, non-white color inside the frame boundaries.

    Args:
        grid: The input grid.
        r, c, h, w: Frame definition (top_row, left_col, height, width).

    Returns:
        The color code of the inner pattern, or None if no single pattern color found.
    """
    inner_color = None
    for ir in range(r + 1, r + h - 1):
        for ic in range(c + 1, c + w - 1):
            pixel = grid[ir, ic]
            if pixel != RED and pixel != WHITE:
                if inner_color is None:
                    inner_color = pixel
                elif inner_color != pixel:
                    return None # More than one color found, unexpected
    return inner_color

def _is_adjacent_to_blue(grid: np.ndarray, r: int, c: int, h: int, w: int) -> bool:
    """
    Checks if any red pixel of the frame border is adjacent (8-way) to a blue pixel.

    Args:
        grid: The input grid.
        r, c, h, w: Frame definition (top_row, left_col, height, width).

    Returns:
        True if adjacent to blue, False otherwise.
    """
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self

            # Check top/bottom border pixels
            for i in range(w):
                br_top, bc_top = r, c + i
                br_bot, bc_bot = r + h - 1, c + i
                
                # Check neighbours of top border pixel
                nr, nc = br_top + dr, bc_top + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == BLUE:
                    return True
                    
                # Check neighbours of bottom border pixel
                nr, nc = br_bot + dr, bc_bot + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == BLUE:
                    return True

            # Check left/right border pixels (excluding corners already checked)
            for i in range(1, h - 1):
                br_left, bc_left = r + i, c
                br_right, bc_right = r + i, c + w - 1

                # Check neighbours of left border pixel
                nr, nc = br_left + dr, bc_left + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == BLUE:
                    return True

                # Check neighbours of right border pixel
                nr, nc = br_right + dr, bc_right + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == BLUE:
                    return True
                    
    return False

def _apply_transformation(output_grid: np.ndarray, r: int, c: int, h: int, w: int, c_in: int, c_out: int):
    """
    Changes the color of the inner pattern within the frame boundaries.

    Args:
        output_grid: The grid to modify.
        r, c, h, w: Frame definition.
        c_in: The original color of the pattern.
        c_out: The target color for the pattern.
    """
    for ir in range(r + 1, r + h - 1):
        for ic in range(c + 1, c + w - 1):
            # Only change pixels matching the original inner color
            if output_grid[ir, ic] == c_in:
                output_grid[ir, ic] = c_out


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by identifying red frames and changing the color
    of the pattern inside based on frame size, pattern color, and adjacency to blue.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid_np = grid_np.copy()

    # Find all red frames
    frames = _find_red_frames(grid_np)

    # Process each frame
    for r, c, h, w in frames:
        # Identify the color inside the frame
        c_in = _get_inner_color(grid_np, r, c, h, w)
        
        if c_in is None or c_in == WHITE or c_in == RED:
            continue # Skip if no valid inner pattern color found

        c_out = None
        # Determine the target color based on frame size and inner color
        if h == 5 and w == 5:
            if c_in == MAGENTA:
                # Special case for Magenta in 5x5 frame
                if _is_adjacent_to_blue(grid_np, r, c, h, w):
                    c_out = ORANGE
                else:
                    c_out = GREEN
            elif c_in in TRANSFORM_5x5:
                c_out = TRANSFORM_5x5[c_in]
                
        elif h == 7 and w == 7:
            if c_in in TRANSFORM_7x7:
                c_out = TRANSFORM_7x7[c_in]

        # If a valid transformation rule was found, apply it
        if c_out is not None:
            _apply_transformation(output_grid_np, r, c, h, w, c_in, c_out)

    # Convert the result back to a list of lists
    return output_grid_np.tolist()
```