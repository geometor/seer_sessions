
Previous Code:
```python
import numpy as np

"""
Transforms an input grid based on patterns and a color key.

1.  Identifies a 3x2 color key map in the top-left corner (rows 0-2, cols 0-1).
    This maps pattern colors (col 0) to border colors (col 1).
2.  Finds unique non-white pattern colors and their locations outside the key map area.
3.  For each pattern color:
    a. Determines the corresponding border color using the key map.
    b. Calculates the minimal bounding box enclosing its locations.
4.  Sorts the patterns based on the leftmost column of their bounding boxes.
5.  Initializes an output grid of the same size as the input, filled with white (0).
6.  Iterates through the sorted patterns and draws rectangles onto the output grid:
    a. The border of the rectangle is filled with the border color.
    b. The interior cells corresponding to the original pattern color keep that color.
    c. Other interior cells (originally white) are filled with the border color.
"""

def find_bounding_box(coords):
    """Calculates the minimal bounding box for a list of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Applies the described transformation to the input grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    rows, cols = input_grid.shape

    # 1. Initialize Output
    output_grid = np.zeros_like(input_grid)

    # 2. Identify Key Map
    key_map = {}
    for r in range(min(3, rows)):
        if cols >= 2:
            pattern_color = input_grid[r, 0]
            border_color = input_grid[r, 1]
            if pattern_color != 0: # Only map non-white pattern colors
                 key_map[pattern_color] = border_color

    # Create a temporary grid to easily find patterns outside the key map
    temp_grid = np.copy(input_grid)
    if rows >= 3 and cols >= 2:
        temp_grid[0:3, 0:2] = 0 # Blank out key map area

    # 3. Identify Pattern Objects and their locations
    pattern_coords = {}
    unique_colors = np.unique(temp_grid[temp_grid != 0])

    for color in unique_colors:
        coords = list(zip(*np.where(temp_grid == color)))
        if coords:
            pattern_coords[color] = coords

    # 4. Prepare Pattern Data (Color, Border Color, Bounding Box)
    pattern_data = []
    for pc, coords in pattern_coords.items():
        if pc in key_map:
            bc = key_map[pc]
            bbox = find_bounding_box(coords)
            if bbox:
                min_r, min_c, max_r, max_c = bbox
                pattern_data.append({
                    'pc': pc,
                    'bc': bc,
                    'min_r': min_r,
                    'min_c': min_c,
                    'max_r': max_r,
                    'max_c': max_c
                })
        # else: # Optional: Handle case where pattern color is not in key map
        #     print(f"Warning: Pattern color {pc} not found in key map.")
        #     continue

    # 5. Determine Processing Order (Sort by min_c)
    pattern_data.sort(key=lambda x: x['min_c'])

    # 6. Draw Rectangles
    for pattern in pattern_data:
        pc = pattern['pc']
        bc = pattern['bc']
        min_r, min_c, max_r, max_c = pattern['min_r'], pattern['min_c'], pattern['max_r'], pattern['max_c']

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Check if on border
                is_border = (r == min_r or r == max_r or c == min_c or c == max_c)

                if is_border:
                    output_grid[r, c] = bc
                else:
                    # Check original input color for interior cells
                    if input_grid[r, c] == pc:
                        output_grid[r, c] = pc
                    elif input_grid[r, c] == 0: # Fill white interior with border color
                        output_grid[r, c] = bc
                    else:
                        # If the interior pixel belonged to a *different* pattern
                        # that was already processed, keep its original color?
                        # Based on example 1, overlapping areas seem to take the border color
                        # of the *current* pattern being drawn if the original pixel was 0.
                        # If the original pixel was another pattern color, it seems to be overwritten
                        # by the border color if it's not the *current* pattern's color.
                        # Let's stick to the simpler logic first: if input was 0, fill BC, else fill PC.
                        # Re-evaluating train_1 output: cell (10, 8) is 5 (gray) in input, becomes 6 (magenta) border in output.
                        # cell (10, 9) is 0 (white) in input, becomes 6 (magenta) border in output.
                        # cell (10,10) is 5 (gray) in input, becomes 5 (gray) in output.
                        # cell (10,11) is 0 (white) in input, becomes 6 (magenta) border in output.
                        # So the logic seems correct: Input PC -> Output PC, Input 0 -> Output BC.
                        # What about Input OTHER_PC? Example 1 doesn't have overlap of non-zero pixels.
                        # The logic implemented (check input == PC or input == 0) covers the examples.
                         if input_grid[r, c] == 0: # Redundant check, already covered, keep for clarity
                            output_grid[r, c] = bc
                         # If input_grid[r,c] was a different non-zero color, it gets overwritten by BC
                         # if it's not the current PC. This might need adjustment if complex overlaps exist.
                         # But let's assume the current logic derived from examples is sufficient.


    # 7. Final Output
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
5 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 8 0 0 4 0 4 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 5 0 5 0 5 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 5 0 5 0 5 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 5 0 5 0 5 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 5 0 5 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 8 7 8 7 8 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 8 7 8 7 8 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 3 3 3 3 3 3 3 3 3 0
0 0 0 7 8 7 8 7 8 7 3 4 3 4 3 4 3 4 3 0
0 0 0 7 7 7 7 6 6 6 6 6 6 6 3 3 3 3 3 0
0 0 0 7 8 7 8 6 5 6 5 6 5 6 3 4 3 4 3 0
0 0 0 7 7 7 7 6 6 6 6 6 6 6 3 3 3 3 3 0
0 0 0 7 8 7 8 6 5 6 5 6 5 6 3 4 3 4 3 0
0 0 0 7 7 7 7 6 6 6 6 6 6 6 3 3 3 3 3 0
0 0 0 7 8 7 8 6 5 6 5 6 5 6 3 4 3 4 3 0
0 0 0 7 7 7 7 6 6 6 6 6 6 6 3 3 3 3 3 0
0 0 0 7 8 7 8 6 5 6 5 6 5 6 0 0 0 0 0 0
0 0 0 7 7 7 7 6 6 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 8 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 8 7 7 0 0 3 3 3 3 3 3 3 0 0
0 0 0 0 7 7 7 7 7 0 0 3 3 3 3 3 3 3 0 0
0 0 0 0 7 7 8 7 6 6 6 3 6 3 3 4 3 3 0 0
0 0 0 0 7 7 7 7 6 6 6 3 3 3 3 3 3 3 0 0
0 0 0 0 7 7 8 7 6 6 5 3 6 3 3 4 3 3 0 0
0 0 0 0 7 7 7 7 6 6 6 3 3 3 3 3 3 3 0 0
0 0 0 0 7 7 8 7 6 6 5 3 3 3 3 3 3 3 0 0
0 0 0 0 7 7 7 7 6 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 6 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 116
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 58.0

## Example 2:
Input:
```
4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 7 8 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 7 8 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 7 8 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 1 1 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 1 4 1 4 1 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 1 1 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 1 4 1 4 1 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 1 1 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 1 4 1 4 1 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 1 1 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 1 4 1 4 1 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 1 1 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 7 8 7 8 7 8 7 8 7 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 8 7 8 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 8 7 8 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 8 7 8 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 8 7 8 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 8 7 8 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 1 1 1 7 7 8 7 8 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 87
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 43.5

## Example 3:
Input:
```
1 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 1 0 0 7 0 7 0 7 0 7 0 7 0 0 0 0 0 0 0
7 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 0 0 8 7 8 7 8 7 8 7 8 7 8 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0
0 0 0 8 7 1 1 1 1 1 1 1 7 8 0 0 0 0 0 0
0 0 0 8 8 1 8 1 8 1 8 1 8 8 0 0 0 0 0 0
0 0 0 8 7 1 1 1 1 1 1 1 7 8 0 0 0 0 0 0
0 0 0 8 8 1 8 1 8 1 8 1 8 8 0 0 0 0 0 0
0 0 0 8 7 1 1 1 1 1 1 1 7 8 0 0 0 0 0 0
0 0 0 8 8 1 8 1 8 1 8 1 8 8 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 1 8 1 8 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 1 8 1 8 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 1 3 1 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 1 3 1 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 1 1 1 1 1 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 1 1 1 1 1 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 1 1 8 1 1 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 1 1 1 1 1 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 8 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 8 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 104
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 52.0
