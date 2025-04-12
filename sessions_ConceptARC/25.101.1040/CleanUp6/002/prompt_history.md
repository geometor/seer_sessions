
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 3
3 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 0 0 0 0
0 1 0 0 3 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 1 0 0 3 0 0 0 0 3
0 0 0 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 1
3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 6 8 0 0 0 8 0 0 0 0 0 6 8 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 8 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 8 6 0 0 0 0 8 0 0 6 6 6 0 0
0 0 6 6 0 0 8 0 0 0 8 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 6 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 6 6 0 0 0 0 0 0 0 6 6 6 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task involves two training examples, each showing an input grid and a corresponding output grid.
    *   Each grid contains pixels of different colors, including a background color (white, 0).
    *   In both examples, the input grid has three colors (background + two others), while the output grid has only two colors (background + one other).
    *   One of the non-background colors from the input is completely removed in the output (Blue in train_1, Azure in train_2).
    *   The other non-background color (Green in train_1, Magenta in train_2) is mostly preserved, but some pixels of this color might also be removed (as seen with Green in train_1).
    *   In train_1, the removed Green pixels appear to be those that are isolated (have no other Green neighbors).
    *   In train_2, the Azure pixels are removed, and all Magenta pixels are kept. There are no isolated Magenta pixels in train_2's input.
    *   The color that is kept in the output appears to be the one that is more numerous or forms larger contiguous objects in the input compared to the color that is entirely removed.

*   **YAML Facts:**
    
```yaml
    task_context:
      problem_type: object_removal_and_filtering
      colors_present: more_than_two_non_background # Incorrect, only two non-bg colors per example
      color_mapping:
        0: white (background)
        1: blue
        3: green
        6: magenta
        8: azure
      grid_properties:
        size_constraints: input and output grids have the same dimensions
        content: pixels represented by integers 0-9

    example_1:
      input_colors: [0, 1, 3] # white, blue, green
      output_colors: [0, 3] # white, green
      primary_color: 3 # green (more frequent/larger objects)
      secondary_color: 1 # blue (less frequent/smaller objects)
      actions:
        - remove_color: 1 # remove all blue pixels
        - filter_color: 3 # remove green pixels based on a condition
      condition_for_filtering:
        - target_color: 3 # green
        - property: isolation # pixel has no neighbors of the same color (green)
        - result: remove_if_isolated

    example_2:
      input_colors: [0, 6, 8] # white, magenta, azure
      output_colors: [0, 6] # white, magenta
      primary_color: 6 # magenta (more frequent/larger objects)
      secondary_color: 8 # azure (less frequent/smaller objects)
      actions:
        - remove_color: 8 # remove all azure pixels
        - filter_color: 6 # remove magenta pixels based on a condition
      condition_for_filtering: # No magenta pixels satisfy this condition in this example
        - target_color: 6 # magenta
        - property: isolation # pixel has no neighbors of the same color (magenta)
        - result: remove_if_isolated

    derived_rule:
      - step: Identify the two non-background colors in the input.
      - step: Determine the primary color (P) as the one appearing most frequently, and the secondary color (S) as the other.
      - step: Remove all pixels of the secondary color (S).
      - step: Remove all pixels of the primary color (P) that do not have any adjacent (including diagonals) neighbors of the primary color (P) in the original input grid.
      - step: Keep all other pixels of the primary color (P).
      - step: Keep all background pixels (0).
    ```


*   **Natural Language Program:**
    1.  Analyze the input grid to identify the two non-background colors present.
    2.  Count the occurrences of each non-background color. Designate the color with the higher count as the 'primary color' (P) and the color with the lower count as the 'secondary color' (S).
    3.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
    4.  Iterate through each cell (pixel) of the input grid at row `r` and column `c`.
    5.  If the color of the input cell `(r, c)` is the primary color (P):
        a.  Examine its eight neighboring cells (including diagonals) in the input grid.
        b.  Check if at least one of these neighbors also contains the primary color (P).
        c.  If at least one neighbor is also color P (meaning the pixel at `(r, c)` is not isolated from other P-colored pixels), then set the corresponding cell `(r, c)` in the output grid to the primary color (P).
    6.  (Implicitly) If the input cell color is the secondary color (S) or the background color (0), or if it is an isolated primary color (P) pixel, the corresponding output cell remains the background color (0) as initialized in step 3.
    7.  The final output grid contains only the background color and the non-isolated pixels of the primary color.
```python
import collections

"""
1.  Analyze the input grid to identify the two non-background colors present (colors other than 0).
2.  Count the occurrences of each non-background color. Designate the color with the higher count as the 'primary color' (P) and the color with the lower count as the 'secondary color' (S).
3.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
4.  Iterate through each cell (pixel) of the input grid at row `r` and column `c`.
5.  If the color of the input cell `(r, c)` is the primary color (P):
    a.  Examine its eight neighboring cells (including diagonals) in the original input grid.
    b.  Check if at least one of these neighbors also contains the primary color (P).
    c.  If at least one neighbor is also color P (meaning the pixel at `(r, c)` is not isolated), then set the corresponding cell `(r, c)` in the output grid to the primary color (P).
6.  All other input cells (background, secondary color, or isolated primary color) result in the corresponding output cell remaining the background color (0).
7.  Return the final output grid.
"""

def get_neighbor_coords(r, c, height, width):
    """Yields valid coordinates of the 8 neighbors for a cell (r, c)."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                yield nr, nc

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by removing the less frequent non-background color
    and filtering out isolated pixels of the more frequent non-background color.
    """
    height = len(input_grid)
    width = len(input_grid[0])

    # 1. Analyze the input grid to identify non-background colors and their counts.
    color_counts = collections.Counter()
    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]
            if color != 0:
                color_counts[color] += 1

    # Check if there are exactly two non-background colors as expected
    if len(color_counts) != 2:
         # Handle unexpected cases if necessary, for now assume 2.
         # If only one non-bg color, maybe it's always the primary?
         # If zero non-bg colors, return the grid as is (all 0s).
         # If more than two, the rule is ambiguous.
         # Based on examples, we expect exactly two.
         pass # Or raise an error, or implement fallback logic


    # 2. Determine the primary (more frequent) and secondary (less frequent) colors.
    # Sort by count (descending), then by color value (ascending) as a tie-breaker
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
    
    primary_color = -1 # Initialize with invalid color
    secondary_color = -1 

    if len(sorted_colors) > 0:
        primary_color = sorted_colors[0][0]
    if len(sorted_colors) > 1:
        secondary_color = sorted_colors[1][0] # Only the secondary color is actually used for removal

    # 3. Create a new output grid filled with the background color (0).
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 4. Iterate through each cell of the input grid.
    for r in range(height):
        for c in range(width):
            cell_color = input_grid[r][c]

            # 5. If the cell color is the primary color:
            if cell_color == primary_color:
                is_isolated = True
                # a. Examine its eight neighbors in the input grid.
                for nr, nc in get_neighbor_coords(r, c, height, width):
                    # b. Check if at least one neighbor is also the primary color.
                    if input_grid[nr][nc] == primary_color:
                        is_isolated = False
                        break # Found a neighbor, no longer isolated

                # c. If not isolated, set the output cell to the primary color.
                if not is_isolated:
                    output_grid[r][c] = primary_color
            
            # 6. (Implicit) If the cell color is background (0), secondary color, 
            #    or an isolated primary color, the output cell remains 0.

    # 7. Return the final output grid.
    return output_grid
```
