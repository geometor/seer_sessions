"""
This task requires identifying the largest hollow rectangular frame made of a single, non-background color within the input grid. 
The output is the content found strictly inside this frame.

The process involves:
1. Scan the input grid to identify all possible hollow rectangular frames. A frame is defined by its top-left (r1, c1) and bottom-right (r2, c2) corners.
2. A valid frame must meet these criteria:
    a. The boundary pixels (top row r1 from c1 to c2, bottom row r2 from c1 to c2, left column c1 from r1+1 to r2-1, right column c2 from r1+1 to r2-1) must all be of the same single non-background color (1-9).
    b. The frame must have an interior, meaning height (r2-r1+1) > 2 and width (c2-c1+1) > 2.
    c. The interior region (pixels from r1+1 to r2-1, c1+1 to c2-1) must contain at least one pixel whose color is different from the frame's boundary color.
3. Calculate the area (height * width) of the bounding box for each valid frame found.
4. Select the frame with the largest bounding box area. 
5. Apply tie-breaking rules if multiple frames share the largest area: choose the one whose top-left corner (r1, c1) has the smallest row index (r1), and then the smallest column index (c1).
6. Extract the subgrid corresponding to the interior region of the selected frame (rows r1+1 to r2-1, columns c1+1 to c2-1).
7. Return this extracted subgrid as the output.
"""

import numpy as np
from typing import List, Tuple, Optional

def _is_hollow_frame(grid: np.ndarray, r1: int, c1: int, r2: int, c2: int) -> Tuple[bool, Optional[int], Optional[int]]:
    """
    Checks if the rectangle defined by (r1, c1) and (r2, c2) forms a valid hollow frame.

    Args:
        grid: The input grid as a numpy array.
        r1, c1: Top-left corner coordinates.
        r2, c2: Bottom-right corner coordinates.

    Returns:
        A tuple: (is_frame, frame_color, area)
        is_frame (bool): True if it's a valid hollow frame, False otherwise.
        frame_color (Optional[int]): The color of the frame if valid, None otherwise.
        area (Optional[int]): The area of the frame's bounding box if valid, None otherwise.
    """
    height = r2 - r1 + 1
    width = c2 - c1 + 1

    # Frame must have dimensions at least 3x3 to have an interior
    if height < 3 or width < 3:
        return False, None, None

    # Check top-left corner for frame color
    frame_color = grid[r1, c1]
    if frame_color == 0:  # Frame color cannot be background
        return False, None, None

    # Check boundary pixels
    # Top row
    if not np.all(grid[r1, c1:c2+1] == frame_color):
        return False, None, None
    # Bottom row
    if not np.all(grid[r2, c1:c2+1] == frame_color):
        return False, None, None
    # Left column (excluding corners)
    if not np.all(grid[r1+1:r2, c1] == frame_color):
        return False, None, None
    # Right column (excluding corners)
    if not np.all(grid[r1+1:r2, c2] == frame_color):
        return False, None, None

    # Check interior condition: at least one pixel must differ from frame_color
    interior = grid[r1+1:r2, c1+1:c2]
    if np.all(interior == frame_color):
        return False, None, None
        
    # If all checks pass, it's a valid frame
    area = height * width
    return True, frame_color, area

def find_frames(grid: np.ndarray) -> List[dict]:
    """
    Finds all valid hollow rectangular frames in the grid.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of dictionaries, where each dictionary represents a frame
        with keys: 'r1', 'c1', 'r2', 'c2', 'color', 'area'.
    """
    rows, cols = grid.shape
    frames = []

    # Iterate through all possible top-left (r1, c1) corners
    for r1 in range(rows):
        for c1 in range(cols):
            # Iterate through all possible bottom-right (r2, c2) corners
            # such that r2 >= r1 and c2 >= c1
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    is_frame, frame_color, area = _is_hollow_frame(grid, r1, c1, r2, c2)
                    if is_frame:
                        frames.append({
                            'r1': r1, 'c1': c1,
                            'r2': r2, 'c2': c2,
                            'color': frame_color,
                            'area': area
                        })
    return frames

def select_largest_frame(frames: List[dict]) -> Optional[dict]:
    """
    Selects the largest frame based on area, with tie-breaking.

    Args:
        frames: A list of frame dictionaries.

    Returns:
        The dictionary of the selected frame, or None if no frames were found.
    """
    if not frames:
        return None

    # Sort frames:
    # 1. By area (descending)
    # 2. By top row (r1, ascending)
    # 3. By left column (c1, ascending)
    sorted_frames = sorted(frames, key=lambda f: (-f['area'], f['r1'], f['c1']))

    return sorted_frames[0]


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies the largest hollow rectangular frame of a single non-background color
    in the input grid and returns the content strictly inside that frame.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the extracted interior of the largest frame.
        Returns an empty list if no valid frame is found.
    """
    # Convert input to numpy array
    grid_np = np.array(input_grid, dtype=int)
    
    if grid_np.size == 0:
        return [] # Handle empty input

    # Find all valid hollow rectangular frames
    frames = find_frames(grid_np)

    # Select the largest frame based on area and tie-breaking rules
    largest_frame = select_largest_frame(frames)

    # If no frame is found, return an empty grid (or handle as appropriate)
    if largest_frame is None:
        # Based on examples, it seems a frame is always expected.
        # If this can happen, decide on behavior (e.g., return empty grid, input grid, error?)
        # For now, returning an empty list.
        return [] 

    # Extract the interior of the selected frame
    r1, c1 = largest_frame['r1'], largest_frame['c1']
    r2, c2 = largest_frame['r2'], largest_frame['c2']
    
    # Interior coordinates are (r1+1 : r2, c1+1 : c2)
    output_np = grid_np[r1+1:r2, c1+1:c2]

    # Convert output numpy array back to list of lists
    output_grid = output_np.tolist()

    return output_grid