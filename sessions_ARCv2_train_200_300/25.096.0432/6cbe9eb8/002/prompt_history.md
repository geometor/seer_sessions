
## train_1

**input:**
```
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
```


**output:**
```
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3
```

**Perception:**

The task involves extracting a specific rectangular subgrid from a larger input grid. The input grids contain repeating background patterns (like `0 1 2 3`, `0 1 2`, or `0 1`) and embedded rectangular structures. These structures are defined by a solid border of a single digit (e.g., `8` in train_1, `3` in train_2 and train_3), which is distinct from the immediate background pattern. The content inside the border can vary. The output grid corresponds exactly to the largest such bordered rectangle found within the input grid, including its border.

**YAML Facts:**


```yaml
task_elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - contains: background_pattern (repeating sequence)
      - contains: bordered_rectangle (one or more)
  - object: bordered_rectangle
    properties:
      - shape: rectangle
      - border: composed of a single, uniform digit (border_digit)
      - interior: can contain various digits
      - location: embedded within the input_grid
      - size: defined by width and height
    relationships:
      - distinct_from: background_pattern (the border_digit is not part of the immediate background sequence)
  - object: output_grid
    properties:
      - type: 2D array of integers
      - content: identical to the largest bordered_rectangle from the input_grid
    relationships:
      - derived_from: input_grid
      - corresponds_to: the bordered_rectangle with the maximum area

actions:
  - action: identify_rectangles
    description: Scan the input_grid to find all rectangular regions enclosed by a solid border of a single digit.
  - action: determine_largest
    description: Calculate the area (width * height) for each identified bordered_rectangle and select the one with the maximum area.
  - action: extract_subgrid
    description: Copy the portion of the input_grid corresponding to the selected largest bordered_rectangle (including its border).
  - action: output_result
    description: Return the extracted subgrid.
```


**Natural Language Program:**

1.  Iterate through each cell of the input grid.
2.  If a cell contains a digit that could potentially form the top-left corner of a rectangular border, attempt to identify a complete rectangular frame originating from this cell, where all border cells contain the same digit.
3.  Keep track of all valid bordered rectangles found. A valid rectangle must have a border composed entirely of the same single digit.
4.  For each valid bordered rectangle found, calculate its area (width multiplied by height).
5.  Identify the bordered rectangle with the largest area among all found rectangles.
6.  Extract the subgrid from the input grid that corresponds exactly to the bounding box of this largest bordered rectangle (including the border cells).
7.  Return this extracted subgrid as the output.
```python
import copy

"""
Identifies all rectangular regions within the input grid that are enclosed by a solid border of a single, uniform digit. 
Calculates the area of each identified rectangle. Selects the rectangle with the largest area. Extracts and returns 
the subgrid corresponding to this largest rectangle, including its border.
"""

def _is_valid(r, c, R, C):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < R and 0 <= c < C

def _check_border(input_grid, r1, c1, r2, c2, border_digit):
    """Check if the border of the rectangle defined by (r1, c1) and (r2, c2) is solid and matches border_digit."""
    R = len(input_grid)
    C = len(input_grid[0])

    # Check top border
    for c in range(c1, c2 + 1):
        if not _is_valid(r1, c, R, C) or input_grid[r1][c] != border_digit:
            return False
            
    # Check bottom border
    for c in range(c1, c2 + 1):
        if not _is_valid(r2, c, R, C) or input_grid[r2][c] != border_digit:
            return False
            
    # Check left border (excluding corners)
    for r in range(r1 + 1, r2):
        if not _is_valid(r, c1, R, C) or input_grid[r][c1] != border_digit:
            return False
            
    # Check right border (excluding corners)
    for r in range(r1 + 1, r2):
        if not _is_valid(r, c2, R, C) or input_grid[r][c2] != border_digit:
            return False
            
    return True

def _extract_subgrid(input_grid, r1, c1, r2, c2):
    """Extracts the subgrid defined by the rectangle corners."""
    subgrid = []
    for r in range(r1, r2 + 1):
        subgrid.append(input_grid[r][c1 : c2 + 1])
    return subgrid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Finds the largest rectangle defined by a solid border of a single digit
    within the input grid and returns that rectangle as a subgrid.
    """
    R = len(input_grid)
    if R == 0:
        return []
    C = len(input_grid[0])
    if C == 0:
        return []

    found_rectangles = []

    # 1. Iterate through each cell as a potential top-left corner (r1, c1).
    for r1 in range(R):
        for c1 in range(C):
            border_digit = input_grid[r1][c1]
            
            # 2. Iterate through each cell as a potential bottom-right corner (r2, c2).
            #    Start from r1, c1 to ensure width and height >= 1.
            for r2 in range(r1, R):
                for c2 in range(c1, C):
                    # Basic check: bottom-right corner must match border digit
                    if input_grid[r2][c2] != border_digit:
                        continue
                        
                    # 3. Check if the rectangle defined by (r1, c1) and (r2, c2) has a valid solid border.
                    if _check_border(input_grid, r1, c1, r2, c2, border_digit):
                        # 4. If valid, calculate area and store rectangle info.
                        height = r2 - r1 + 1
                        width = c2 - c1 + 1
                        area = height * width
                        found_rectangles.append({
                            "r1": r1, "c1": c1, 
                            "r2": r2, "c2": c2, 
                            "area": area
                        })

    # 5. Identify the rectangle with the largest area.
    if not found_rectangles:
        return [] # Or handle error appropriately if a rectangle is always expected

    largest_rectangle = max(found_rectangles, key=lambda x: x["area"])

    # 6. Extract the subgrid corresponding to the largest rectangle.
    output_grid = _extract_subgrid(
        input_grid,
        largest_rectangle["r1"], largest_rectangle["c1"],
        largest_rectangle["r2"], largest_rectangle["c2"]
    )

    # 7. Return the extracted subgrid.
    return output_grid
```
