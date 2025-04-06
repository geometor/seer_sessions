"""
This module transforms an input 13x13 grid containing four distinct 3-cell L-shapes
into a 4x4 output grid. It identifies each L-shape, determines its 2x2 bounding
box pattern and its orientation (based on the position of the single zero cell
within the 2x2 box). It then places each 2x2 pattern into a specific quadrant
of the 4x4 output grid according to the shape's orientation:
- Top-Left shape (zero at bottom-right) goes to output top-left quadrant.
- Top-Right shape (zero at bottom-left) goes to output top-right quadrant.
- Bottom-Left shape (zero at top-right) goes to output bottom-left quadrant.
- Bottom-Right shape (zero at top-left) goes to output bottom-right quadrant.
"""

import numpy as np
from collections import deque

def _find_shapes(grid: np.ndarray) -> list[dict]:
    """
    Finds all connected components (shapes) of non-zero cells in the grid.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A list of dictionaries, where each dictionary represents a shape
        and contains 'color' (int) and 'coords' (list of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    coords.append((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if coords: # Should always be true if we start with a non-zero cell
                    shapes.append({'color': color, 'coords': coords})
                    
    return shapes

def _get_2x2_pattern(grid: np.ndarray, coords: list[tuple[int, int]]) -> np.ndarray:
    """
    Extracts the 2x2 bounding box pattern for a shape.

    Args:
        grid: The input grid as a NumPy array.
        coords: List of (row, col) coordinates for the shape.

    Returns:
        A 2x2 NumPy array representing the shape's pattern.
    """
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    # Since it's an L-shape of 3 cells, the bounding box will be 2x2
    # The top-left corner of this 2x2 box is (min_r, min_c)
    pattern = grid[min_r : min_r + 2, min_c : min_c + 2]
    return pattern

def _get_orientation(pattern_2x2: np.ndarray) -> str:
    """
    Determines the orientation of the L-shape based on the zero's position
    in its 2x2 pattern.

    Args:
        pattern_2x2: The 2x2 NumPy array pattern.

    Returns:
        A string representing the orientation: 'TL', 'TR', 'BL', 'BR'.
        Corresponds to the location where the shape *block* is placed
        in the output (e.g. 'TL' means the main L is in the top left
        of its 2x2 square, meaning the zero is at the bottom right).
    """
    zero_pos = np.where(pattern_2x2 == 0)
    zero_r, zero_c = zero_pos[0][0], zero_pos[1][0]

    if zero_r == 1 and zero_c == 1: # Zero at bottom-right -> Shape at Top-Left
        return 'TL'
    elif zero_r == 1 and zero_c == 0: # Zero at bottom-left -> Shape at Top-Right
        return 'TR'
    elif zero_r == 0 and zero_c == 1: # Zero at top-right -> Shape at Bottom-Left
        return 'BL'
    elif zero_r == 0 and zero_c == 0: # Zero at top-left -> Shape at Bottom-Right
        return 'BR'
    else:
        # Should not happen for valid L-shapes
        raise ValueError("Invalid L-shape pattern encountered.")


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input 13x13 grid containing four distinct 3-cell L-shapes
    into a 4x4 output grid by identifying each L-shape, determining its 2x2
    pattern and orientation, and placing the pattern into the corresponding
    quadrant of the output grid based on orientation.
    """
    # Convert input to numpy array for easier slicing and processing
    grid_np = np.array(input_grid, dtype=int)

    # Initialize output_grid (4x4) with zeros
    output_grid_np = np.zeros((4, 4), dtype=int)

    # Find all distinct non-zero shapes in the input grid
    shapes = _find_shapes(grid_np)

    # Process each shape found
    for shape in shapes:
        # Get the 2x2 pattern for the current shape
        pattern = _get_2x2_pattern(grid_np, shape['coords'])

        # Determine the orientation of the shape based on the pattern
        orientation = _get_orientation(pattern)

        # Place the 2x2 pattern into the correct quadrant of the output grid
        if orientation == 'TL':
            output_grid_np[0:2, 0:2] = pattern
        elif orientation == 'TR':
            output_grid_np[0:2, 2:4] = pattern
        elif orientation == 'BL':
            output_grid_np[2:4, 0:2] = pattern
        elif orientation == 'BR':
            output_grid_np[2:4, 2:4] = pattern

    # Convert the numpy output grid back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid