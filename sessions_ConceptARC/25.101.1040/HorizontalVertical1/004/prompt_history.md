
## train_1

**input:**
```
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 0 0 0 4 0 0
0 0 0 4 4 4 4 4 0 0
```


**output:**
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 2 2 2 2 2 2 2 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```

Okay, let's analyze the task based on the provided examples.

**Perception**

The input grids contain one or more distinct, closed shapes made of non-white pixels (Red, Yellow, Orange) on a white background. These shapes enclose regions of the white background pixels. The core transformation involves identifying these enclosed white regions and filling them with a new color. The specific color used for filling depends on the color of the shape that encloses the region. Crucially, the rule mapping the enclosing color to the fill color appears to change based on the *total number of distinct non-white colors* present in the shapes within the input grid.

In the first example, there are two distinct shape colors (Red, Yellow). Red shapes enclose areas filled with Green, and Yellow shapes enclose areas filled with Orange.

In the second example, there are three distinct shape colors (Red, Yellow, Orange). Here, Red shapes enclose areas filled with Orange, Yellow shapes enclose areas filled with Green, and Orange shapes enclose areas filled with Green.

This suggests two different color-filling rules, selected based on whether two or three (or more) distinct non-white colors form the shapes in the input grid.

**Facts**


```yaml
elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: background
    properties:
      - color: white (0)
  - type: shape
    description: A contiguous block of non-white pixels.
    properties:
      - color: [red (2), yellow (4), orange (7), ...]
      - connectivity: Assumed 8-way adjacency for shape pixels.
  - type: enclosed_region
    description: A contiguous region of white (0) pixels that does not touch the grid border and is entirely surrounded by pixels of a single shape/color.
    properties:
      - color: white (0)
      - connectivity: Assumed 8-way adjacency for region pixels.
      - status: enclosed (boolean)
      - enclosing_color: The color of the single shape surrounding the region.
      - border_touching: (boolean) True if any pixel is on the grid edge.

grid_properties:
  - name: distinct_shape_colors
    description: The set of unique non-white colors present in the shapes of the input grid.
  - name: num_distinct_shape_colors
    description: The count of unique non-white colors.

transformation:
  - action: identify_shapes
    description: Locate all contiguous non-white shapes.
  - action: count_distinct_colors
    description: Determine the number of unique colors used in the identified shapes.
  - action: identify_white_regions
    description: Locate all contiguous white (0) regions.
  - action: check_enclosure
    description: For each white region, determine if it is enclosed.
    criteria:
      - Must not touch the grid border.
      - All adjacent (8-way) non-white pixels must belong to a single shape and have the same color.
  - action: determine_enclosing_color
    description: Identify the color of the shape enclosing a white region.
  - action: apply_fill_rule
    description: Select a fill color based on the enclosing color and the total number of distinct shape colors in the grid.
    rules:
      - condition: num_distinct_shape_colors <= 2
        mapping:
          - input_color: red (2)
            output_color: green (3)
          - input_color: yellow (4)
            output_color: orange (7)
          # Add other colors if observed in more examples
      - condition: num_distinct_shape_colors >= 3
        mapping:
          - input_color: red (2)
            output_color: orange (7)
          - input_color: yellow (4)
            output_color: green (3)
          - input_color: orange (7)
            output_color: green (3)
          # Add other colors if observed in more examples
  - action: fill_region
    description: Change the color of the pixels within an enclosed white region to the determined fill color.

output_constraints:
  - The grid dimensions remain unchanged.
  - The original shapes remain unchanged in color and position.
  - Only the enclosed white regions are modified.
  - Background pixels not part of an enclosed region remain white.
```


**Natural Language Program**

1.  **Analyze Input Shapes:** Identify all contiguous shapes formed by non-white pixels in the input grid. Determine the set of unique colors present in these shapes and count how many distinct colors there are (`num_distinct_shape_colors`).
2.  **Identify Candidate Regions:** Find all contiguous regions of white (0) pixels in the input grid.
3.  **Check for Enclosure:** For each white region identified:
    a.  Verify that no pixel in the region lies on the border of the grid.
    b.  Examine all pixels directly adjacent (including diagonals) to the white region.
    c.  Confirm that all adjacent pixels that are *not* white share the exact same single color (`enclosing_color`).
    d.  If both conditions (a and c) are met, the white region is considered "enclosed".
4.  **Determine Fill Rule:** Based on the `num_distinct_shape_colors` calculated in step 1:
    a.  If `num_distinct_shape_colors` is 2 or less, use Rule Set A: Red(2) fills Green(3), Yellow(4) fills Orange(7).
    b.  If `num_distinct_shape_colors` is 3 or more, use Rule Set B: Red(2) fills Orange(7), Yellow(4) fills Green(3), Orange(7) fills Green(3).
5.  **Apply Filling:** Create a copy of the input grid to serve as the output. For every white region identified as "enclosed" in step 3:
    a.  Determine the appropriate `fill_color` using the selected Rule Set (A or B) and the `enclosing_color` found in step 3c.
    b.  Change the color of all pixels within that enclosed region to the determined `fill_color` in the output grid.
6.  **Finalize Output:** Return the modified grid. Pixels that were not part of an enclosed white region retain their original color from the input grid.
```python
import numpy as np
from collections import deque

"""
Identifies enclosed regions of white pixels (0) within the input grid and fills them based on the color of the enclosing shape.

The fill color depends on the number of distinct non-white colors present in the shapes across the entire grid:

1.  **Count Distinct Shape Colors:** Determine the number of unique non-white colors (1-9) present in the input grid.
2.  **Identify White Regions:** Find contiguous regions of white pixels (0).
3.  **Check for Enclosure:** A white region is considered "enclosed" if:
    a. It does not touch the border of the grid.
    b. All adjacent non-white pixels surrounding the region belong to a single shape and have the same color.
4.  **Apply Fill Rule:**
    *   **If 2 or fewer distinct shape colors exist:**
        *   Regions enclosed by Red (2) are filled with Green (3).
        *   Regions enclosed by Yellow (4) are filled with Orange (7).
        *   (Other color mappings might exist but are not shown in examples).
    *   **If 3 or more distinct shape colors exist:**
        *   Regions enclosed by Red (2) are filled with Orange (7).
        *   Regions enclosed by Yellow (4) are filled with Green (3).
        *   Regions enclosed by Orange (7) are filled with Green (3).
        *   (Other color mappings might exist but are not shown in examples).
5.  **Output:** Return the modified grid with enclosed regions filled according to the rules. Shapes and unenclosed areas remain unchanged.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling enclosed white regions based on
    the color of the enclosing shape and the total number of distinct
    shape colors in the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_grid = grid.copy()
    visited = np.zeros_like(grid, dtype=bool)

    # 1. Count Distinct Shape Colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # 4. Determine Fill Rule based on the count
    fill_map = {}
    if num_distinct_shape_colors <= 2:
        # Rule Set A (for 2 or fewer distinct colors)
        fill_map = {
            2: 3,  # Red -> Green
            4: 7,  # Yellow -> Orange
            # Add other rules if needed based on more examples
        }
    else:
        # Rule Set B (for 3 or more distinct colors)
        fill_map = {
            2: 7,  # Red -> Orange
            4: 3,  # Yellow -> Green
            7: 3,  # Orange -> Green
             # Add other rules if needed based on more examples
        }

    # 2. & 3. Identify White Regions and Check for Enclosure
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited[r, c]:
                # Start BFS for a potential white region
                region_pixels = set()
                adjacent_colors = set()
                is_border_touching = False
                queue = deque([(r, c)])
                visited[r, c] = True
                valid_region = True # Assume valid until proven otherwise

                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_pixels.add((curr_r, curr_c))

                    # Check if the current pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_border_touching = True

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if neighbor is within bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = grid[nr, nc]
                                if neighbor_color == 0: # Neighbor is white
                                    if not visited[nr, nc]:
                                        visited[nr, nc] = True
                                        queue.append((nr, nc))
                                else: # Neighbor is non-white (part of a shape)
                                    adjacent_colors.add(neighbor_color)
                            else:
                                # Neighbor is out of bounds - this shouldn't happen if border check works
                                # but good for robustness
                                pass

                # 3. Final check for enclosure after exploring the whole region
                is_enclosed = (not is_border_touching) and (len(adjacent_colors) == 1)

                # 5. Apply Filling if enclosed
                if is_enclosed:
                    enclosing_color = list(adjacent_colors)[0]
                    if enclosing_color in fill_map:
                        fill_color = fill_map[enclosing_color]
                        for pr, pc in region_pixels:
                            output_grid[pr, pc] = fill_color
                    # else: keep original color (white) if no mapping exists


    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies enclosed regions of white pixels (0) within the input grid and fills them based on the color of the enclosing shape.

The fill color depends on the number of distinct non-white colors present in the shapes across the entire grid:

1.  **Count Distinct Shape Colors:** Determine the number of unique non-white colors (1-9) present in the input grid.
2.  **Identify White Regions:** Find contiguous regions of white pixels (0).
3.  **Check for Enclosure:** A white region is considered "enclosed" if:
    a. It does not touch the border of the grid.
    b. All adjacent non-white pixels surrounding the region belong to a single shape and have the same color.
4.  **Apply Fill Rule:**
    *   **If 2 or fewer distinct shape colors exist:**
        *   Regions enclosed by Red (2) are filled with Green (3).
        *   Regions enclosed by Yellow (4) are filled with Orange (7).
        *   (Other color mappings might exist but are not shown in examples).
    *   **If 3 or more distinct shape colors exist:**
        *   Regions enclosed by Red (2) are filled with Orange (7).
        *   Regions enclosed by Yellow (4) are filled with Green (3).
        *   Regions enclosed by Orange (7) are filled with Green (3).
        *   (Other color mappings might exist but are not shown in examples).
5.  **Output:** Return the modified grid with enclosed regions filled according to the rules. Shapes and unenclosed areas remain unchanged.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling enclosed white regions based on
    the color of the enclosing shape and the total number of distinct
    shape colors in the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_grid = grid.copy()
    visited = np.zeros_like(grid, dtype=bool)

    # 1. Count Distinct Shape Colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # 4. Determine Fill Rule based on the count
    fill_map = {}
    if num_distinct_shape_colors <= 2:
        # Rule Set A (for 2 or fewer distinct colors)
        fill_map = {
            2: 3,  # Red -> Green
            4: 7,  # Yellow -> Orange
            # Add other rules if needed based on more examples
        }
    else:
        # Rule Set B (for 3 or more distinct colors)
        fill_map = {
            2: 7,  # Red -> Orange
            4: 3,  # Yellow -> Green
            7: 3,  # Orange -> Green
             # Add other rules if needed based on more examples
        }

    # 2. & 3. Identify White Regions and Check for Enclosure
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 0 and not visited[r, c]:
                # Start BFS for a potential white region
                region_pixels = set()
                adjacent_colors = set()
                is_border_touching = False
                queue = deque([(r, c)])
                visited[r, c] = True
                valid_region = True # Assume valid until proven otherwise

                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_pixels.add((curr_r, curr_c))

                    # Check if the current pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_border_touching = True

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if neighbor is within bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = grid[nr, nc]
                                if neighbor_color == 0: # Neighbor is white
                                    if not visited[nr, nc]:
                                        visited[nr, nc] = True
                                        queue.append((nr, nc))
                                else: # Neighbor is non-white (part of a shape)
                                    adjacent_colors.add(neighbor_color)
                            else:
                                # Neighbor is out of bounds - this shouldn't happen if border check works
                                # but good for robustness
                                pass

                # 3. Final check for enclosure after exploring the whole region
                is_enclosed = (not is_border_touching) and (len(adjacent_colors) == 1)

                # 5. Apply Filling if enclosed
                if is_enclosed:
                    enclosing_color = list(adjacent_colors)[0]
                    if enclosing_color in fill_map:
                        fill_color = fill_map[enclosing_color]
                        for pr, pc in region_pixels:
                            output_grid[pr, pc] = fill_color
                    # else: keep original color (white) if no mapping exists


    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 0 0 0 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Expected Output:
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Transformed Output:
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 2 2 2 2 2 2 2 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 3 3 3 3 3 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.102040816326536
**General Assessment**

The provided `transform` function correctly implements the logic described in the initial natural language program. It successfully identifies enclosed white regions, counts distinct shape colors, selects a fill rule based on that count, and applies the corresponding color transformations.

The code passed Example 1, where there were 2 distinct shape colors (Red, Yellow). The failure occurred in Example 2, which has 3 distinct shape colors (Red, Yellow, Orange). The code correctly identified the 3 colors and applied the corresponding fill rule ({Red: Orange, Yellow: Green, Orange: Green}). However, the *expected output* for Example 2 shows that the region enclosed by the Orange shape should *not* be filled, contradicting the observed pattern from Example 1 and the Red/Yellow shapes in Example 2.

The core algorithm for finding enclosed white regions (BFS, checking border proximity, ensuring a single enclosing color) appears sound and correctly identified all relevant regions in both examples. The discrepancy lies specifically in the fill rule applied when 3 distinct colors are present, particularly for regions enclosed by Orange (7).

**Strategy for Resolution:**

The most direct way to reconcile the code's behavior with the expected outputs is to adjust the fill rule for the case where 3 or more distinct colors are present. Specifically, the rule derived from Example 2 indicates that regions enclosed by Orange (7) should *not* be filled under this condition, while regions enclosed by Red (2) and Yellow (4) should be filled according to the mapping {Red: Orange, Yellow: Green}. The natural language program and facts will be updated to reflect this refined rule.

**Metrics**


*code_execution:*
```python
import numpy as np

def analyze_example(input_grid_list, expected_output_list, transformed_output_list):
    input_grid = np.array(input_grid_list)
    expected_output = np.array(expected_output_list)
    transformed_output = np.array(transformed_output_list)

    metrics = {}
    # Grid properties
    metrics['height'] = input_grid.shape[0]
    metrics['width'] = input_grid.shape[1]

    # Color analysis
    shape_colors = set(input_grid[input_grid > 0])
    metrics['distinct_shape_colors'] = sorted(list(shape_colors))
    metrics['num_distinct_shape_colors'] = len(shape_colors)

    # Comparison results
    match = np.array_equal(expected_output, transformed_output)
    metrics['match'] = match
    if not match:
        metrics['pixels_off'] = np.sum(expected_output != transformed_output)
        # Identify mismatch locations and values
        diff_indices = np.where(expected_output != transformed_output)
        mismatches = []
        for r, c in zip(*diff_indices):
            mismatches.append({
                'location': (int(r), int(c)),
                'expected': int(expected_output[r, c]),
                'transformed': int(transformed_output[r, c])
            })
        metrics['mismatches'] = mismatches
    else:
        metrics['pixels_off'] = 0
        metrics['mismatches'] = []

    return metrics

# Example 1 Data
grid1_in = [
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0]
]
grid1_out_expected = [
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 3, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 3, 2, 0, 0, 0, 0, 0, 0], [0, 2, 3, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
    [0, 0, 0, 4, 7, 7, 7, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0]
]
grid1_out_transformed = [
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 3, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 3, 2, 0, 0, 0, 0, 0, 0], [0, 2, 3, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
    [0, 0, 0, 4, 7, 7, 7, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0]
]

# Example 2 Data
grid2_in = [
    [0,0,0,0,0,0,0,0,0,0,0,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,0,4],
    [0,0,0,0,0,0,0,0,0,0,0,4,0,4],[0,2,2,2,2,2,2,2,2,0,0,4,0,4],
    [0,2,0,0,0,0,0,0,2,0,0,4,0,4],[0,2,0,0,0,0,0,0,2,0,0,4,4,4],
    [0,2,2,2,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,7,7,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,7],[0,0,7,7,7,7,7,7,7,0,0,7,0,7],
    [0,0,7,0,0,0,0,0,7,0,0,7,0,7],[0,0,7,7,7,7,7,7,7,0,0,7,0,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,7],[0,0,0,0,0,0,0,0,0,0,0,7,7,7]
]
grid2_out_expected = [
    [0,0,0,0,0,0,0,0,0,0,0,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,3,4],
    [0,0,0,0,0,0,0,0,0,0,0,4,3,4],[0,2,2,2,2,2,2,2,2,0,0,4,3,4],
    [0,2,7,7,7,7,7,7,2,0,0,4,3,4],[0,2,7,7,7,7,7,7,2,0,0,4,4,4],
    [0,2,2,2,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,7,7,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,3,7],[0,0,7,7,7,7,7,7,7,0,0,7,3,7],
    [0,0,7,0,0,0,0,0,7,0,0,7,3,7],[0,0,7,7,7,7,7,7,7,0,0,7,3,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,3,7],[0,0,0,0,0,0,0,0,0,0,0,7,7,7]
]
grid2_out_transformed = [
    [0,0,0,0,0,0,0,0,0,0,0,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,3,4],
    [0,0,0,0,0,0,0,0,0,0,0,4,3,4],[0,2,2,2,2,2,2,2,2,0,0,4,3,4],
    [0,2,7,7,7,7,7,7,2,0,0,4,3,4],[0,2,7,7,7,7,7,7,2,0,0,4,4,4],
    [0,2,2,2,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,7,7,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,3,7],[0,0,7,7,7,7,7,7,7,0,0,7,3,7],
    [0,0,7,3,3,3,3,3,7,0,0,7,3,7],[0,0,7,7,7,7,7,7,7,0,0,7,3,7], # Note: Row 10 transformed mismatch
    [0,0,0,0,0,0,0,0,0,0,0,7,3,7],[0,0,0,0,0,0,0,0,0,0,0,7,7,7]
]


metrics1 = analyze_example(grid1_in, grid1_out_expected, grid1_out_transformed)
metrics2 = analyze_example(grid2_in, grid2_out_expected, grid2_out_transformed)

print("--- Example 1 Metrics ---")
for key, value in metrics1.items():
    print(f"{key}: {value}")

print("\n--- Example 2 Metrics ---")
for key, value in metrics2.items():
    if key == 'mismatches':
        print(f"{key}:")
        for mismatch in value:
            print(f"  - {mismatch}")
    else:
        print(f"{key}: {value}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Metrics ---
height: 10
width: 10
distinct_shape_colors: [np.int64(2), np.int64(4)]
num_distinct_shape_colors: 2
match: True
pixels_off: 0
mismatches: []

--- Example 2 Metrics ---
height: 14
width: 14
distinct_shape_colors: [np.int64(2), np.int64(4), np.int64(7)]
num_distinct_shape_colors: 3
match: False
pixels_off: 5
mismatches:
  - {'location': (10, 3), 'expected': 0, 'transformed': 3}
  - {'location': (10, 4), 'expected': 0, 'transformed': 3}
  - {'location': (10, 5), 'expected': 0, 'transformed': 3}
  - {'location': (10, 6), 'expected': 0, 'transformed': 3}
  - {'location': (10, 7), 'expected': 0, 'transformed': 3}

```
**Facts**


```yaml
elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: background
    properties:
      - color: white (0)
  - type: shape
    description: A contiguous block of non-white pixels (using 8-way adjacency).
    properties:
      - color: [red (2), yellow (4), orange (7), ...]
  - type: enclosed_region
    description: A contiguous region of white (0) pixels (using 8-way adjacency) meeting specific criteria.
    properties:
      - color: white (0)
      - status: enclosed (boolean)
      - criteria_for_enclosed:
          - All pixels in the region must NOT be on the grid border (row 0, col 0, row max, col max).
          - All non-white pixels immediately adjacent (8-way) to any pixel in the region must have the exact same color (`enclosing_color`).
      - enclosing_color: The single non-white color surrounding the region.

grid_properties:
  - name: distinct_shape_colors
    description: The set of unique non-white colors present in the shapes of the input grid.
  - name: num_distinct_shape_colors
    description: The count of unique non-white colors (e.g., 2 in Example 1, 3 in Example 2).

transformation:
  - action: identify_shapes_and_colors
    description: Determine the set of unique non-white colors present (`distinct_shape_colors`) and their count (`num_distinct_shape_colors`).
  - action: identify_white_regions
    description: Locate all contiguous white (0) regions using 8-way adjacency.
  - action: check_enclosure_and_identify_enclosing_color
    description: For each white region, determine if it is enclosed based on the criteria (not touching border, surrounded by single non-white color). If enclosed, record the `enclosing_color`.
  - action: select_fill_rule
    description: Choose a specific color mapping rule based on `num_distinct_shape_colors`.
    rules:
      - condition: num_distinct_shape_colors <= 2
        description: Rule Set A
        mapping:
          - enclosing_color: red (2)
            fill_color: green (3)
          - enclosing_color: yellow (4)
            fill_color: orange (7)
          # Note: Add rules for other colors if observed in future examples.
      - condition: num_distinct_shape_colors >= 3
        description: Rule Set B
        mapping:
          - enclosing_color: red (2)
            fill_color: orange (7)
          - enclosing_color: yellow (4)
            fill_color: green (3)
          - enclosing_color: orange (7)
            fill_color: white (0) # Explicitly does not fill (or fills with background)
          # Note: Add rules for other colors if observed in future examples.
  - action: apply_fill
    description: Create a copy of the input grid. For each region identified as 'enclosed', find the corresponding `fill_color` from the selected rule set based on its `enclosing_color`. Change the color of all pixels within that region to the `fill_color` in the copied grid. If an enclosing color doesn't have a mapping in the rule set, the region remains white.

output_constraints:
  - Grid dimensions are preserved.
  - Original non-white shapes remain unchanged.
  - Only white regions meeting the 'enclosed' criteria are potentially modified.
  - White regions not meeting the criteria remain white.
```


**Natural Language Program**

1.  **Analyze Grid Colors:** Examine the input grid and identify all unique non-white pixel colors present. Count the number of these distinct colors (`num_distinct_shape_colors`).
2.  **Identify White Regions:** Find all contiguous areas composed solely of white (0) pixels using 8-way adjacency. Keep track of the pixels belonging to each distinct white region.
3.  **Determine Enclosure Status:** For each identified white region:
    a.  Check if any pixel within the region lies on the outermost border of the grid. If yes, the region is not enclosed.
    b.  Examine all pixels immediately adjacent (including diagonals) to the white region. Collect the colors of all *non-white* adjacent pixels.
    c.  If the region does not touch the border (passes 3a) AND all adjacent non-white pixels have the exact same single color (passes 3b), then the region is considered "enclosed". Record the single color of these adjacent non-white pixels as the `enclosing_color`.
4.  **Select Fill Mapping:** Choose the appropriate color transformation rule based on `num_distinct_shape_colors`:
    *   **If `num_distinct_shape_colors` is 2 or less:** Use Rule Set A: {Red(2) maps to Green(3), Yellow(4) maps to Orange(7)}.
    *   **If `num_distinct_shape_colors` is 3 or more:** Use Rule Set B: {Red(2) maps to Orange(7), Yellow(4) maps to Green(3), Orange(7) maps to White(0) (i.e., no change)}.
5.  **Apply Transformations:** Create a copy of the input grid. Iterate through all white regions identified as "enclosed" in Step 3. For each enclosed region:
    a.  Look up its `enclosing_color` in the selected fill mapping (Rule Set A or B).
    b.  If a mapping exists, change the color of all pixels within that region in the copied grid to the corresponding mapped `fill_color`.
    c.  If no mapping exists for the `enclosing_color` in the selected rule set (or if the mapped color is White(0)), leave the region's pixels as white (0).
6.  **Return Output:** The modified grid copy is the final output.
```python
"""
Transforms an input grid by identifying enclosed white regions (color 0) and filling them based on the color of the single surrounding shape. The specific fill color applied depends on the total number of distinct non-white colors present in the entire input grid.

1.  **Analyze Grid Colors:** Count the number of unique non-white colors (`num_distinct_shape_colors`) in the input grid.
2.  **Identify White Regions:** Find contiguous areas of white pixels (0) using 8-way adjacency.
3.  **Determine Enclosure Status:** A white region is "enclosed" if:
    a.  It does not touch the grid border.
    b.  All immediately adjacent non-white pixels belong to a single shape and have the same color (`enclosing_color`).
4.  **Select Fill Mapping:** Choose a fill rule based on `num_distinct_shape_colors`:
    *   If `num_distinct_shape_colors` is 2 or less: Red(2) fills Green(3), Yellow(4) fills Orange(7).
    *   If `num_distinct_shape_colors` is 3 or more: Red(2) fills Orange(7), Yellow(4) fills Green(3). Regions enclosed by Orange(7) are *not* filled (remain white).
5.  **Apply Transformations:** Create a copy of the input grid. For each "enclosed" white region, determine the fill color using the selected mapping and the region's `enclosing_color`. Update the pixels within the region in the copied grid.
6.  **Return Output:** Return the modified grid.
"""

import numpy as np
from collections import deque

def find_enclosed_regions(grid: np.ndarray) -> list[tuple[set[tuple[int, int]], set[int], bool]]:
    """
    Identifies contiguous white regions and checks their enclosure status.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list where each element represents a white region and contains:
        - A set of (row, col) tuples for pixels in the region.
        - A set of adjacent non-white colors.
        - A boolean indicating if the region touches the border.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions_data = []

    for r in range(height):
        for c in range(width):
            # Start BFS for a new white region if not visited
            if grid[r, c] == 0 and not visited[r, c]:
                region_pixels = set()
                adjacent_colors = set()
                is_border_touching = False
                queue = deque([(r, c)])
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_pixels.add((curr_r, curr_c))

                    # Check if the current pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_border_touching = True

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check if neighbor is within bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                neighbor_color = grid[nr, nc]
                                if neighbor_color == 0: # Neighbor is white
                                    if not visited[nr, nc]:
                                        visited[nr, nc] = True
                                        queue.append((nr, nc))
                                else: # Neighbor is non-white (part of a potential enclosing shape)
                                    adjacent_colors.add(neighbor_color)
                            # else: neighbor is out of bounds, implies border touching for the region pixel
                            # This is implicitly handled by the border check on curr_r, curr_c

                regions_data.append((region_pixels, adjacent_colors, is_border_touching))

    return regions_data


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling enclosed white regions based on
    the color of the enclosing shape and the total number of distinct
    shape colors in the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()

    # 1. Analyze Grid Colors: Count distinct non-white colors
    shape_colors = set(grid[grid > 0])
    num_distinct_shape_colors = len(shape_colors)

    # 4. Select Fill Mapping based on the count
    fill_map = {}
    if num_distinct_shape_colors <= 2:
        # Rule Set A (for 2 or fewer distinct colors)
        fill_map = {
            2: 3,  # Red -> Green
            4: 7,  # Yellow -> Orange
        }
    else:
        # Rule Set B (for 3 or more distinct colors)
        # Note: Orange(7) is intentionally left out based on Example 2 output
        fill_map = {
            2: 7,  # Red -> Orange
            4: 3,  # Yellow -> Green
            # 7: 3, # Removed based on failed test analysis
        }

    # 2. & 3. Identify White Regions and Determine Enclosure Status
    regions_data = find_enclosed_regions(grid)

    # 5. Apply Transformations
    for region_pixels, adjacent_colors, is_border_touching in regions_data:
        # Check enclosure criteria
        is_enclosed = (not is_border_touching) and (len(adjacent_colors) == 1)

        if is_enclosed:
            enclosing_color = list(adjacent_colors)[0]
            # Check if the enclosing color has a mapping in the selected rule set
            if enclosing_color in fill_map:
                fill_color = fill_map[enclosing_color]
                # Fill the region in the output grid
                for pr, pc in region_pixels:
                    output_grid[pr, pc] = fill_color
            # Else: If enclosing_color is not in the map (like Orange(7) in rule B),
            # the region remains white (0), no action needed as output_grid is a copy.

    # 6. Return Output
    return output_grid.tolist()
```
