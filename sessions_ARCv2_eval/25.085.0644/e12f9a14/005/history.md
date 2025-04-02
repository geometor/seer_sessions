
Previous Code:
```python
import numpy as np
import math

"""
Transforms an input grid by projecting colors from "source" pixels (those not azure 8 or green 3)
onto adjacent azure 8 background pixels. The projection extends outwards in the four cardinal directions
(up, down, left, right) from each source pixel. The projection stops if it hits a green 3 pixel,
another non-azure 8 pixel, or the grid boundary. Green 3 pixels and original source pixels remain unchanged.

If an azure 8 pixel can be reached by projections from multiple source pixels, the final color is determined
by the nearest source pixel. If there's a tie in distance between a vertical (up/down) projection and a
horizontal (left/right) projection, the vertical projection takes precedence. If there's a tie in distance
between two vertical projections (up vs down) or two horizontal projections (left vs right), the projection
originating from the source pixel with the smaller row index (for vertical ties) or smaller column index
(for horizontal ties) takes precedence. If row/column indices are also the same (which shouldn't happen
for distinct sources affecting the same pixel), the 'up' direction beats 'down', and 'left' beats 'right'.
Effectively, search order up, down, left, right determines the winner in case of equidistant sources.

The transformation logic involves:
1. Initializing the output grid as a copy of the input grid.
2. Iterating through each pixel of the grid.
3. If a pixel is azure (8), search outwards in the four cardinal directions to find the nearest source pixel(s).
4. The search stops upon encountering a green (3) boundary, another non-azure (8) pixel, or the grid edge.
5. Record the color and distance of the nearest source found in each direction.
6. Determine the final color for the azure pixel based on the minimum distance, prioritizing vertical sources in case of a tie.
7. Update the corresponding pixel in the output grid.
"""

def transform(input_grid):
    """
    Applies the color projection transformation with boundary constraints and conflict resolution.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    background_color = 8
    boundary_color = 3

    # Iterate through each pixel to potentially fill if it's background
    for r in range(height):
        for c in range(width):
            # Only modify background pixels
            if input_grid_np[r, c] == background_color:
                
                # Store potential source colors and their distances for this pixel
                # (color, distance, source_row, source_col, is_vertical)
                potential_sources = []

                # Search Up
                for row_idx in range(r - 1, -1, -1):
                    color = input_grid_np[row_idx, c]
                    if color != background_color and color != boundary_color:
                        potential_sources.append({'color': color, 'dist': r - row_idx, 'source_r': row_idx, 'source_c': c, 'is_vertical': True})
                        break # Found nearest source in this direction
                    elif color == boundary_color:
                        break # Hit boundary
                    # Continue if background_color
                
                # Search Down
                for row_idx in range(r + 1, height):
                    color = input_grid_np[row_idx, c]
                    if color != background_color and color != boundary_color:
                        potential_sources.append({'color': color, 'dist': row_idx - r, 'source_r': row_idx, 'source_c': c, 'is_vertical': True})
                        break 
                    elif color == boundary_color:
                        break
                        
                # Search Left
                for col_idx in range(c - 1, -1, -1):
                    color = input_grid_np[r, col_idx]
                    if color != background_color and color != boundary_color:
                        potential_sources.append({'color': color, 'dist': c - col_idx, 'source_r': r, 'source_c': col_idx, 'is_vertical': False})
                        break
                    elif color == boundary_color:
                        break
                        
                # Search Right
                for col_idx in range(c + 1, width):
                    color = input_grid_np[r, col_idx]
                    if color != background_color and color != boundary_color:
                        potential_sources.append({'color': color, 'dist': col_idx - c, 'source_r': r, 'source_c': col_idx, 'is_vertical': False})
                        break
                    elif color == boundary_color:
                        break

                # Determine the winning color based on rules
                if not potential_sources:
                    continue # No source found, pixel remains background

                min_dist = min(s['dist'] for s in potential_sources)
                
                # Filter sources with the minimum distance
                closest_sources = [s for s in potential_sources if s['dist'] == min_dist]

                # Prioritize vertical sources
                vertical_winners = [s for s in closest_sources if s['is_vertical']]
                horizontal_winners = [s for s in closest_sources if not s['is_vertical']]

                winner = None
                if vertical_winners:
                    # If multiple vertical winners, choose based on row index, then use original order (up first)
                    winner = min(vertical_winners, key=lambda s: s['source_r'])
                elif horizontal_winners:
                     # If multiple horizontal winners, choose based on col index, then use original order (left first)
                    winner = min(horizontal_winners, key=lambda s: s['source_c'])
                
                if winner:
                   output_grid[r, c] = winner['color']


    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 3 3 8 8 8 3 8 3 3 8 8 8
8 8 8 3 9 9 3 8 8 8 8 3 1 1 3 8 8 3 4 4 3 8 8 8
8 8 8 3 9 9 3 8 8 8 8 3 1 1 3 8 8 3 4 4 3 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 3 3 8 8 8 3 8 3 3 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 6 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 8 8 1 4 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 8 1 4 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 8 1 4 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 1 4 8 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 1 4 8 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 1 4 8 8 8 8 8
9 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 1 4 8 8 8 8 8
8 9 8 8 8 8 8 8 9 1 8 8 8 8 8 8 1 8 4 8 8 8 8 8
8 8 9 8 8 8 8 9 8 8 1 8 8 8 8 1 8 8 4 8 8 8 8 8
8 8 8 9 3 3 9 8 8 8 8 1 3 3 1 8 8 3 4 3 3 8 8 8
8 8 8 3 9 9 3 8 8 8 8 3 1 1 3 8 8 3 4 4 3 8 8 8
8 8 8 3 9 9 3 8 8 8 8 3 1 1 3 8 8 3 4 4 3 8 8 8
8 8 8 9 3 3 9 8 8 8 8 1 3 3 1 8 8 3 4 3 3 8 8 8
8 8 9 8 8 8 8 9 8 8 1 8 8 8 8 1 8 8 4 8 8 8 8 8
8 9 8 8 8 8 8 8 9 1 8 8 8 8 8 8 1 8 4 8 8 8 8 8
9 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 1 4 8 8 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 1 4 8 8 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 1 4 8 8 8 8
8 8 8 8 8 8 8 8 9 1 8 8 8 8 8 8 8 8 1 4 8 8 8 8
8 3 3 3 3 8 8 8 9 1 8 8 8 8 8 8 8 8 8 1 4 8 8 8
8 3 6 6 6 6 6 6 8 9 1 8 8 8 8 8 8 8 8 1 4 8 8 8
8 3 6 6 3 8 8 8 6 8 9 1 8 8 8 8 8 8 8 8 1 4 8 8
8 3 3 3 3 8 8 8 8 6 8 9 1 8 8 8 8 8 8 8 1 4 8 8
8 8 8 8 8 8 8 8 8 8 6 8 9 1 8 8 8 8 8 8 8 1 4 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 3 3 8 8 8 3 4 3 3 8 8 8
8 8 8 3 9 9 3 8 8 8 8 3 1 1 3 8 8 3 4 4 3 8 8 8
8 8 8 3 9 9 3 8 8 8 8 3 1 1 3 8 8 3 4 4 3 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 3 3 8 8 8 3 4 3 3 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 3 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 4 6 6 6 6 6
8 3 6 6 3 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
```
Match: False
Pixels Off: 108
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.5

## Example 2:
Input:
```
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
8 3 3 8 3 8 8 8
8 3 4 4 3 8 8 8
8 3 4 4 8 8 8 8
8 8 3 3 3 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 4 8 8 8 8
8 8 8 4 8 8 8 8
8 3 3 4 3 8 8 8
8 3 4 4 3 8 8 8
8 3 4 4 4 4 4 4
8 4 3 3 3 8 8 8
4 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 4 8 8 8 8
8 8 8 4 8 8 8 8
8 3 3 4 3 8 8 8
8 3 4 4 3 8 8 8
8 3 4 4 4 4 4 4
8 8 3 3 3 8 8 8
8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.25

## Example 3:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 3 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 3 8 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 4 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 4 4 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 7 7 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 7 7 3 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 4
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 4 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 4 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 4 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 2 8 4 8 8 8 8
8 8 8 3 2 2 2 2 2 2 2 2 2 8 4 8 8 8 8 8
2 2 2 2 2 2 3 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 3 4 3 8 8 8 8 8
4 4 4 4 4 4 4 4 4 4 4 4 4 4 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 4 4 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8
7 7 7 7 7 7 7 7 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 7 7 3 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 3 2 2 2 2 2 2 2 2 2 4 2 2 2 2 2 2
2 2 2 2 2 2 3 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 3 4 3 8 8 8 8 8
4 4 4 4 4 4 4 4 4 4 4 4 4 4 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 4 4 3 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8
7 7 7 7 7 7 7 7 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 7 7 3 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.5

## Example 4:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 3 8 3 8 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 6 8 8 8 6 8 8 8 8 8
8 8 6 8 8 6 8 8 8 8 8 8
8 3 6 3 6 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8
8 6 3 3 3 8 8 8 8 8 8 8
6 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 6 8 8 8 8 8 8 8 8 8
8 8 6 8 8 8 8 8 8 8 8 8
8 3 6 3 8 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8
8 3 6 6 3 8 8 8 8 8 8 8
8 8 3 3 3 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.944444444444429
