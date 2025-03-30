
Previous Code:
```python
import numpy as np
from typing import List, Dict, Tuple, Any

"""
Identifies horizontally adjacent "framed square" objects in the input grid that share the same center color. 
For each such qualifying pair (Square1 on the left, Square2 on the right):
1. Fills the background pixels (color 0) between the two squares, on the same row(s) as their centers, with the shared center color.
2. Fills a rectangular block of background pixels below the center of Square1 with the shared center color. The height of this block is 3 if the horizontal gap between the squares is exactly 3 pixels wide, otherwise the height is 2. The width of the block matches the width of the square's center. The block starts 2 rows below the square's center row(s).
"""

def _find_framed_squares(grid: np.ndarray) -> List[Dict[str, Any]]:
    """
    Finds all framed square objects (3x3 or 4x4) in the grid.

    Returns:
        A list of dictionaries, each representing a square with its properties:
        'frame_color', 'center_color', 'center_rows', 'center_cols', 'bbox'.
    """
    squares = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                # Check for 3x3 square starting at (r, c)
                if r + 2 < height and c + 2 < width:
                    subgrid = grid[r:r+3, c:c+3]
                    frame_color = subgrid[0, 0]
                    center_color = subgrid[1, 1]
                    is_3x3 = True
                    if frame_color == 0 or center_color == 0 or frame_color == center_color:
                        is_3x3 = False
                    else:
                        # Check frame
                        for i in range(3):
                            if subgrid[0, i] != frame_color or subgrid[2, i] != frame_color or \
                               subgrid[i, 0] != frame_color or subgrid[i, 2] != frame_color:
                                is_3x3 = False
                                break
                    
                    if is_3x3:
                        squares.append({
                            'frame_color': frame_color,
                            'center_color': center_color,
                            'center_rows': [r + 1],
                            'center_cols': [c + 1],
                            'bbox': (r, c, r + 2, c + 2) # min_r, min_c, max_r, max_c (inclusive)
                        })
                        visited[r:r+3, c:c+3] = True
                        continue # Found 3x3, skip 4x4 check starting here

                # Check for 4x4 square starting at (r, c)
                if r + 3 < height and c + 3 < width:
                    subgrid = grid[r:r+4, c:c+4]
                    frame_color = subgrid[0, 0]
                    center_color = subgrid[1, 1]
                    is_4x4 = True
                    if frame_color == 0 or center_color == 0 or frame_color == center_color:
                        is_4x4 = False
                    else:
                         # Check frame
                        for i in range(4):
                            if subgrid[0, i] != frame_color or subgrid[3, i] != frame_color or \
                               subgrid[i, 0] != frame_color or subgrid[i, 3] != frame_color:
                                is_4x4 = False
                                break
                        # Check center 2x2
                        if is_4x4:
                            for i in range(1, 3):
                                for j in range(1, 3):
                                    if subgrid[i, j] != center_color:
                                        is_4x4 = False
                                        break
                                if not is_4x4: break
                                
                    if is_4x4:
                         squares.append({
                            'frame_color': frame_color,
                            'center_color': center_color,
                            'center_rows': list(range(r + 1, r + 3)),
                            'center_cols': list(range(c + 1, c + 3)),
                            'bbox': (r, c, r + 3, c + 3) # min_r, min_c, max_r, max_c (inclusive)
                        })
                         visited[r:r+4, c:c+4] = True
                         
    # Sort squares by top-left corner (row, then column) for consistent pairing
    squares.sort(key=lambda s: (s['bbox'][0], s['bbox'][1]))
    return squares

def _are_horizontally_adjacent(grid: np.ndarray, sq1: Dict[str, Any], sq2: Dict[str, Any]) -> bool:
    """Checks if two squares are horizontally adjacent with only background in between."""
    bbox1 = sq1['bbox']
    bbox2 = sq2['bbox']

    # Must be in the same row span
    if bbox1[0] != bbox2[0] or bbox1[2] != bbox2[2]:
        return False

    # sq1 must be strictly to the left of sq2
    if bbox1[3] >= bbox2[1]:
        return False

    # Check the gap between them
    min_r, max_r = bbox1[0], bbox1[2]
    start_c = bbox1[3] + 1
    end_c = bbox2[1] # Exclusive index for range

    if start_c >= end_c: # No gap or touching
        return False
        
    gap_slice = grid[min_r : max_r + 1, start_c : end_c]
    
    # Check if all cells in the gap are background (0)
    return np.all(gap_slice == 0)


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on adjacent, same-center-color squares.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Step 1: Find all framed squares
    squares = _find_framed_squares(grid)

    # Step 2: Iterate through pairs of squares
    num_squares = len(squares)
    for i in range(num_squares):
        for j in range(i + 1, num_squares): # Only consider pairs where sq2 is potentially to the right of sq1
            sq1 = squares[i]
            sq2 = squares[j]

            # Step 3: Check conditions: horizontally adjacent and same center color
            if sq1['center_color'] == sq2['center_color'] and \
               _are_horizontally_adjacent(grid, sq1, sq2):

                fill_color = sq1['center_color']
                bbox1 = sq1['bbox']
                bbox2 = sq2['bbox']
                center_rows = sq1['center_rows'] # Same as sq2's center rows due to adjacency check
                
                # Step 4a: Fill between the squares
                gap_start_col = bbox1[3] + 1
                gap_end_col = bbox2[1] # Exclusive
                for r in center_rows:
                    for c in range(gap_start_col, gap_end_col):
                         # Check bounds just in case, though adjacency check should cover this
                         if 0 <= r < height and 0 <= c < width and output_grid[r, c] == 0:
                            output_grid[r, c] = fill_color

                # Step 4b: Fill below the first square (sq1)
                gap_width = gap_end_col - gap_start_col
                fill_height = 3 if gap_width == 3 else 2
                
                S1_center_cols = sq1['center_cols']
                fill_start_row = max(center_rows) + 2 # Start 2 rows below the center

                for r_offset in range(fill_height):
                    target_r = fill_start_row + r_offset
                    if 0 <= target_r < height: # Check row bounds
                        for c in S1_center_cols:
                             if 0 <= c < width and output_grid[target_r, c] == 0: # Check column bounds and background
                                output_grid[target_r, c] = fill_color

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 0 0 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 0 0 2 4 2 0 0 2 4 2 0 0 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 0 0 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 0 0 2 4 2 0 0 2 4 2 0 0 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 3 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 1 2 4 2 1 1 2 4 2 1 1 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 1 0 0 0 0 3 0 0 0 0 3 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 3 0 0 0 0 3 0 0 0 0 1 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 3 2 3 3 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 1 1 2 4 2 1 1 2 4 2 1 1 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 4 4 2 4 2 0 0 2 3 2 3 3 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 4 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 0 0 2 4 2 4 4 2 4 2 0 0 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 4 4 2 4 2 0 0 2 3 2 3 3 2 3 2 0 0 2 4 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 4 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 1 2 0 0 2 4 2 4 4 2 4 2 0 0 2 1 2 0 0 2 4
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 2 2
0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4 2 0 0 2 4
```
Match: False
Pixels Off: 38
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.801242236024848

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0 0 0 0 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 8 8 0 0 0 4 4 0 0 0 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 2 2 3 0 3 2 2 3 0 3 2 2 3 0 3 8 8 3 8 3 2 2 3 8 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 4 3 2 2 3 4 3 2 2 3 4 3 4 4 3 0 3 2 2
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 2 3 2 2 3 2 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 2 3 2 2 3 2 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 2 2 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 2 3 2 2 3 2 3 2 2 3 2 3 2 2 3 2 3 2 2 3 0 3 2 2
0 3 2 2 3 2 3 2 2 3 2 3 2 2 3 2 3 2 2 3 2 3 2 2 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 2 2 0 0 0 2 2 0 0 0 2 2 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 2 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 2 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 2 3 2 2 3 2 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 2 2 3 2 3 2 2 3 2 3 2 2 3 0 3 8 8 3 0 3 2 2 3 0 3 8 8
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 0 2 2 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3 3 0 3 3 3
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
0 3 2 2 3 0 3 4 4 3 0 3 2 2 3 0 3 2 2 3 0 3 4 4 3 0 3 2 2
```
Match: False
Pixels Off: 70
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 20.11494252873561

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 3 3 3 1 2 1 3 3 3 1 2 1 3 3 3 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 3 3 3 1 2 1 3 3 3 1 2 1 3 3 3 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 2 2 2 1 2 1 2 2 2 1 2 1 2 2 2 1 2 1 2 2 2 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 0 0 0 1 2 1 2 2 2 1 2 1 0 0 0 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 2 1 2 2 2 1 2 1 2 2 2 1 2 1 2 2 2 1 2 1 2 2 2 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 1 3 1 0 0 0 1 2 1 2 2 2 1 2 1 0 0 0 1 3 1 0 0 0 1 2 1 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0
```
Match: False
Pixels Off: 78
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 20.68965517241378
