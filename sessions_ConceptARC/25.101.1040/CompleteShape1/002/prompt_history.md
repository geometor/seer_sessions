
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 0 0 2 0
```


**output:**
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 6 6 2 0
```

## Perception

The task involves modifying input grids by filling in specific rectangular areas composed entirely of white pixels (color 0). The color used to fill these white rectangles appears to be determined by the color of adjacent or aligned non-white shapes. The goal seems to be completing or bridging gaps in existing monochromatic (single-color) lines or shapes.

1.  **Example 1:** A 2x2 white rectangle near the top-center is filled with blue (1). This white rectangle is located directly above a vertical column of white space, which in turn is above a 2x2 blue rectangle near the bottom-center. The filling action appears to extend the lower blue rectangle upwards across the white gap.
2.  **Example 2:** A 1x2 white rectangle near the bottom-center is filled with magenta (6). This white rectangle is located immediately to the right of a 1x2 horizontal segment of magenta pixels. The filling action extends this magenta segment to the right.

The core operation is identifying these "fillable" white rectangles and determining the correct color based on context, specifically looking for monochromatic shapes that are aligned (horizontally or vertically) with the white rectangle and separated only by other white pixels, or directly adjacent.

## Facts


```yaml
Examples:
  - id: train_1
    Input:
      grid_size: [12, 10]
      objects:
        - type: background
          color: white
        - type: shape # Left top
          color: blue
          pixels: [[2,1],[2,2],[3,1],[3,2]]
        - type: shape # Left middle
          color: red
          pixels: [[4,1],[4,2],[7,1],[7,2]]
        - type: shape # Left bottom
          color: blue
          pixels: [[5,1],[5,2],[6,1],[6,2],[8,1],[8,2],[9,1],[9,2]]
        - type: shape # Right top
          color: red
          pixels: [[2,3],[3,3],[2,6],[3,6],[4,7],[4,8],[7,7],[7,8]]
        - type: shape # Right bottom
          color: blue
          pixels: [[5,7],[5,8],[6,7],[6,8],[8,7],[8,8],[9,7],[9,8]]
        - type: shape # Center vertical line (bottom part)
          color: blue
          pixels: [[8,4],[8,5],[9,4],[9,5]]
        - type: shape # Center vertical line (top part - target)
          color: white
          pixels: [[2,4],[2,5],[3,4],[3,5]]
        - type: shape # Center white space separator
          color: white
          pixels: [[4,4],[4,5],[5,4],[5,5],[6,4],[6,5],[7,4],[7,5]]
    Output:
      grid_size: [12, 10]
      objects: # Same as input, except:
        - type: shape # Center vertical line (top part - filled)
          color: blue
          pixels: [[2,4],[2,5],[3,4],[3,5]]
      action:
        - type: fill_rectangle
          target_rectangle: # Center vertical line (top part)
            color: white
            pixels: [[2,4],[2,5],[3,4],[3,5]]
          fill_color: blue
          reason: >
            Completes vertical alignment with the blue shape [[8,4],[8,5],[9,4],[9,5]]
            across the white separator [[4,4]..[7,5]].

  - id: train_2
    Input:
      grid_size: [6, 8]
      objects:
        - type: background
          color: white
        - type: shape # Frame parts
          color: red
          pixels: [[0,1],[0,6],[5,1],[5,6]]
        - type: shape # Frame parts
          color: magenta
          pixels: [[0,2],[0,3],[0,4],[0,5],[1,1],[1,6],[2,1],[2,6],[3,1],[3,6],[4,1],[4,6],[5,2],[5,3]]
        - type: shape # Horizontal line gap (target)
          color: white
          pixels: [[5,4],[5,5]]
    Output:
      grid_size: [6, 8]
      objects: # Same as input, except:
        - type: shape # Horizontal line gap (filled)
          color: magenta
          pixels: [[5,4],[5,5]]
      action:
        - type: fill_rectangle
          target_rectangle: # Horizontal line gap
            color: white
            pixels: [[5,4],[5,5]]
          fill_color: magenta
          reason: >
            Completes horizontal alignment by extending the adjacent magenta shape
            [[5,2],[5,3]] to the right.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through all possible rectangular subgrids within the input grid.
3.  Identify maximal contiguous rectangular subgrids composed entirely of white pixels (color 0). Let the current white rectangle be `W`.
4.  For each white rectangle `W`:
    a.  **Check for Vertical Completion Below:** Find the highest non-white, monochromatic rectangle `S` located entirely below `W`, such that `S` has the same width and occupies the same columns as `W`. Check if the rectangular region between the bottom edge of `W` and the top edge of `S` consists entirely of white pixels. If such an `S` exists and the separating region is white, fill the region corresponding to `W` in the output grid with the color of `S`. Stop checking for this `W` and proceed to the next white rectangle.
    b.  **Check for Horizontal Completion Left:** Find the rightmost non-white, monochromatic rectangle `S` located entirely to the left of `W`, such that `S` has the same height and occupies the same rows as `W`. Check if `S` is immediately adjacent to `W` (no gap between them). If such an `S` exists, fill the region corresponding to `W` in the output grid with the color of `S`. Stop checking for this `W` and proceed to the next white rectangle.
    c.  **(Implicit)** Similar checks can be defined for vertical completion above and horizontal completion right, if necessary based on other examples, potentially with a defined priority order (e.g., Below > Left > Above > Right).
5.  Return the modified output grid.
```python
"""
The transformation rule identifies maximal contiguous rectangular areas of white pixels (color 0) within the input grid.
For each such white rectangle, it attempts to determine a fill color based on adjacent or aligned non-white monochromatic shapes, following specific priority rules:

1.  **Vertical Completion Below:** It checks if there is a non-white monochromatic shape S located directly below the white rectangle W, perfectly aligned horizontally (sharing the same columns), and separated from W only by other white pixels. If such a shape S exists, the white rectangle W is filled with the color of S.
2.  **Horizontal Completion Left:** If the vertical check does not result in a fill, it checks if there is a non-white monochromatic shape S located immediately to the left of the white rectangle W, perfectly aligned vertically (sharing the same rows). If such a shape S exists, the white rectangle W is filled with the color of S.

If a fill occurs based on rule 1, rule 2 is not checked for that white rectangle. The process is repeated for all identified maximal white rectangles. The output grid reflects these fill operations.
"""

import numpy as np
from copy import deepcopy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to fill specific white rectangles.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Keep track of white pixels already part of a processed maximal rectangle
    visited = np.zeros((rows, cols), dtype=bool)
    rectangles_to_process = []

    # Find all maximal white rectangles (color 0)
    for r in range(rows):
        for c in range(cols):
            # Start search if pixel is white and not visited
            if grid[r, c] == 0 and not visited[r, c]:
                start_r, start_c = r, c
                
                # Find the maximum width of white pixels starting at (start_r, start_c)
                current_width = 0
                while start_c + current_width < cols and grid[start_r, start_c + current_width] == 0 and not visited[start_r, start_c + current_width]:
                    current_width += 1
                
                if current_width == 0: continue # Should not happen based on initial check, but safety

                # Find the maximum height for this width, ensuring all cells are white & unvisited
                current_height = 0
                possible_height = True
                while start_r + current_height < rows and possible_height:
                    # Check if the entire segment in this row is white and unvisited
                    for w_offset in range(current_width):
                        if grid[start_r + current_height, start_c + w_offset] != 0 or visited[start_r + current_height, start_c + w_offset]:
                            possible_height = False
                            break
                    if possible_height:
                        current_height += 1
                    else:
                        break # Height expansion stopped

                # If a valid rectangle is found, store it and mark visited
                if current_height > 0 and current_width > 0:
                    r1, c1 = start_r, start_c
                    r2, c2 = start_r + current_height - 1, start_c + current_width - 1
                    rectangles_to_process.append((r1, c1, r2, c2)) 

                    # Mark pixels within this maximal rectangle as visited
                    for i in range(r1, r2 + 1):
                        for j in range(c1, c2 + 1):
                            visited[i, j] = True

    # Process each found white rectangle according to the rules
    for r1, c1, r2, c2 in rectangles_to_process:
        filled = False # Flag to track if this rectangle has been filled

        # Rule 1: Check for Vertical Completion Below
        
        # Find the first row below the rectangle (r2 + 1)
        shape_start_r = r2 + 1
        
        # Check if this row is within grid bounds
        if shape_start_r < rows:
            # Check if the space between W and the potential shape S is purely white
            is_gap_white = True
            # Note: For this rule, the gap *must* start at r2+1. We check if the row shape_start_r
            # is the *first* non-white row below W aligned with its columns.
            # A more rigorous check would trace the gap row by row, but let's check shape_start_r first.
            
            # Check if the segment in shape_start_r aligned with W is monochromatic and non-white
            potential_color = grid[shape_start_r, c1]
            is_segment_mono = False
            if potential_color != 0: # Must be non-white
                 if np.all(grid[shape_start_r, c1 : c2 + 1] == potential_color):
                     is_segment_mono = True

            if is_segment_mono:
                 # Now verify the gap between W (ending at r2) and S (starting at shape_start_r) is white
                 gap_is_truly_white = True
                 for gap_r in range(r2 + 1, shape_start_r):
                      if not np.all(grid[gap_r, c1 : c2 + 1] == 0):
                           gap_is_truly_white = False
                           break
                 
                 if gap_is_truly_white:
                      # All conditions met for Rule 1
                      fill_color = potential_color
                      output_grid[r1:r2+1, c1:c2+1] = fill_color
                      filled = True


        # Rule 2: Check for Horizontal Completion Left (only if not filled by Rule 1)
        if not filled:
            # Check if column c1-1 exists (i.e., c1 > 0)
            if c1 > 0:
                # Check if the column segment adjacent left is monochromatic and non-white
                adj_col_segment = grid[r1:r2+1, c1-1]
                potential_color = adj_col_segment[0]

                if potential_color != 0: # Must be non-white
                    if np.all(adj_col_segment == potential_color):
                        # All conditions met for Rule 2 (adjacency is implicit)
                        fill_color = potential_color
                        output_grid[r1:r2+1, c1:c2+1] = fill_color
                        filled = True # Mark filled, though loop for this rect ends here

    # Convert the result back to a list of lists
    return output_grid.tolist()

```
