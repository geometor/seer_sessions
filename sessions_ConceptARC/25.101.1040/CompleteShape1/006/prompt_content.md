
Previous Code:
```python
import numpy as np
from copy import deepcopy

"""
The transformation rule identifies maximal contiguous rectangular areas of white pixels (color 0). 
For each such white rectangle 'W' that meets a size constraint (height <= 2 or width <= 2):
1. It checks for a 'Vertical Bridge Below': Is there a monochromatic, non-white horizontal segment 'S' below W (sharing the same columns)? Is the entire rectangular space between W and S composed only of white pixels? If yes, W is filled with the color of S.
2. If the vertical check doesn't apply, it checks for 'Horizontal Extension Left': Is there a monochromatic, non-white vertical segment 'SL' immediately to the left of W (sharing the same rows)? If yes, W is filled with the color of SL.
3. If neither of the above applies, it checks for 'Horizontal Extension Right': Is there a monochromatic, non-white vertical segment 'SR' immediately to the right of W (sharing the same rows)? If yes, W is filled with the color of SR.
The checks are performed in this order (Vertical Below > Horizontal Left > Horizontal Right). Only the first rule that applies results in a fill for a given white rectangle.
"""

def find_maximal_white_rectangles(grid: np.ndarray) -> list[tuple[int, int, int, int]]:
    """
    Finds all maximal contiguous rectangular areas of white pixels (0).

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of tuples, where each tuple represents a rectangle
        as (r1, c1, r2, c2) (top-left and bottom-right coordinates, inclusive).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                start_r, start_c = r, c
                
                # Find max width greedy
                max_width = 0
                while start_c + max_width < cols and grid[start_r, start_c + max_width] == 0 and not visited[start_r, start_c + max_width]:
                    max_width += 1
                
                if max_width == 0: continue # Should not happen

                # Find max height for this width greedy
                max_height = 0
                possible_height = True
                while start_r + max_height < rows and possible_height:
                    # Check if the entire row segment is white and unvisited
                    all_white_and_unvisited = True
                    for w_offset in range(max_width):
                        if grid[start_r + max_height, start_c + w_offset] != 0 or visited[start_r + max_height, start_c + w_offset]:
                            all_white_and_unvisited = False
                            break
                    
                    if all_white_and_unvisited:
                         # If row is valid, mark it as visited temporarily for width calculation
                         # for the *next* row, preventing overlapping starts from splitting rects
                         # Mark only if we extend height
                         if max_height > 0: 
                            for w_offset in range(max_width):
                                visited[start_r + max_height -1, start_c + w_offset] = True
                         max_height += 1
                    else:
                        possible_height = False # Stop extending height

                # Finalize rectangle coordinates and mark fully visited
                if max_height > 0 and max_width > 0:
                    r1, c1 = start_r, start_c
                    r2, c2 = start_r + max_height - 1, start_c + max_width - 1
                    rectangles.append((r1, c1, r2, c2))
                    # Ensure all pixels in the final maximal rectangle are marked visited
                    visited[r1:r2+1, c1:c2+1] = True
    return rectangles

def is_monochromatic_non_white(segment: np.ndarray) -> tuple[bool, int]:
    """Checks if a segment is monochromatic and not white (0)."""
    if segment.size == 0:
        return False, -1 # Not monochromatic if empty
    first_color = segment.flat[0]
    if first_color == 0:
        return False, 0 # White
    if np.all(segment == first_color):
        return True, int(first_color) # Use int() to ensure standard python int
    return False, -1 # Not monochromatic

def is_all_white(segment: np.ndarray) -> bool:
    """Checks if a segment contains only white pixels (0)."""
    if segment.size == 0: # An empty gap is considered "all white"
        return True
    return np.all(segment == 0)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to fill specific white rectangles
    based on vertical or horizontal bridging/extension patterns.
    """
    # Convert to numpy array for easier slicing and operations
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Find all maximal white rectangles
    white_rectangles = find_maximal_white_rectangles(grid)

    # Process each white rectangle
    for r1, c1, r2, c2 in white_rectangles:
        filled = False # Flag to track if this rectangle was filled
        
        # Calculate height and width
        rect_h = r2 - r1 + 1
        rect_w = c2 - c1 + 1

        # 4. Apply Size Constraint Check
        if rect_h > 2 and rect_w > 2:
            continue # Skip large rectangles

        # --- 5. Vertical Bridge Below Check ---
        # Find the first row below the rectangle that contains a non-white pixel in the rectangle's columns
        first_non_white_row_idx = -1
        for r_scan in range(r2 + 1, rows):
            segment_in_row = grid[r_scan, c1 : c2 + 1]
            if np.any(segment_in_row != 0):
                first_non_white_row_idx = r_scan
                break
        
        # If such a row was found within bounds
        if first_non_white_row_idx != -1:
            # Check if the segment in that row is monochromatic non-white
            segment_below = grid[first_non_white_row_idx, c1 : c2 + 1]
            is_mono, fill_color = is_monochromatic_non_white(segment_below)

            if is_mono:
                # Check if the gap between the rectangle and the segment is all white
                gap_segment = grid[r2 + 1 : first_non_white_row_idx, c1 : c2 + 1]
                if is_all_white(gap_segment):
                    # Conditions met: Fill the rectangle in the output grid
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    filled = True

        # --- 6. Horizontal Extension Left Check ---
        if not filled:
            # Check if there's a column to the left
            if c1 > 0:
                # Extract the segment immediately to the left
                segment_left = grid[r1 : r2 + 1, c1 - 1]
                # Check if it's monochromatic and non-white
                is_mono, fill_color = is_monochromatic_non_white(segment_left)
                
                if is_mono:
                    # Conditions met: Fill the rectangle
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    filled = True

        # --- 7. Horizontal Extension Right Check ---
        if not filled:
             # Check if there's a column to the right
             if c2 < cols - 1:
                # Extract the segment immediately to the right
                segment_right = grid[r1 : r2 + 1, c2 + 1]
                 # Check if it's monochromatic and non-white
                is_mono, fill_color = is_monochromatic_non_white(segment_right)

                if is_mono:
                    # Conditions met: Fill the rectangle
                    output_grid[r1 : r2 + 1, c1 : c2 + 1] = fill_color
                    filled = True # Not strictly needed as it's the last check, but good practice

    # Convert the result back to a list of lists for the final output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 0 0 2 1 1 0
0 1 1 2 0 0 2 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 2 2 2 1 1 2 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 2 2 2 1 1 2 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.666666666666657

## Example 2:
Input:
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 0 0 2 0
```
Expected Output:
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 6 6 2 0
```
Transformed Output:
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 6 6 2 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
