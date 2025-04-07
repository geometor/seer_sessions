
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 2 0 2 0 2 0 2 0 2
2 2 2 0 2 0 2 0 2 0 2 0 2
0 0 0 0 2 0 2 0 2 0 2 0 2
2 2 2 2 2 0 2 0 2 0 2 0 2
0 0 0 0 0 0 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 4 0 4
4 4 4 4 4 0 4 0 4 0 4 0 4
0 0 0 0 4 0 4 0 4 0 4 0 4
4 4 4 0 4 0 4 0 4 0 4 0 4
0 0 4 0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0 4 0 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 0 3 0 3 0 3 0 3 0 3
8 0 0 3 0 3 0 3 0 3 0 0
0 0 0 3 0 3 0 3 0 3 3 3
8 8 8 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 3 3 3 3
8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3
8 8 8 8 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 0 3 3 3
8 8 8 0 8 0 8 0 8 0 0 0
0 0 8 0 8 0 8 0 8 0 0 3
8 0 8 0 8 0 8 0 8 0 8 0
```


## train_3

**input:**
```
1 0 0 0 0 0 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
8 0 0 0 0 0 0
```


**output:**
```
1 0 1 0 2 0 2
0 0 1 0 2 0 0
1 1 1 0 2 2 2
0 0 0 0 0 0 0
8 8 8 0 0 2 2
0 0 8 0 8 0 0
8 0 8 0 8 0 0
```


## train_4

**input:**
```
1 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 1 0 1 2 0 2 0 2
0 0 1 0 1 2 0 2 0 0
1 1 1 0 1 2 0 2 2 2
0 0 0 0 1 2 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input/Output:** Both are 2D grids (matrices) filled with integers.
2.  **Content:** The grids primarily contain zeros (background color) and a few non-zero integers (representing distinct colors or sources).
3.  **Input Characteristics:** The non-zero numbers in the input are sparse, typically located near the edges or corners. These act as "seeds" or "sources".
4.  **Output Characteristics:** The output grids are significantly more filled than the inputs. The non-zero numbers from the input appear to have expanded or "painted" regions of the grid.
5.  **Transformation Pattern:** The painting seems related to proximity. Each cell in the output grid appears to take the color of the *nearest* source cell from the input grid, measured by Manhattan distance. However, there's an additional constraint: the painting process creates striped patterns. A cell `(r, c)` only gets painted by a source `(sr, sc)` if the column index `c` has the same parity (even or odd) as the source's column index `sc`.
6.  **Tie-breaking:** If a cell is equidistant from two or more source cells, it remains zero (background color).

**YAML Facts:**


```yaml
Grid:
  Type: 2D Matrix
  Cell Values: Integers (0 for background, non-zero for colors)
  Dimensions: Consistent between input and output pair

Source Cells:
  Identification: Non-zero cells in the input grid.
  Properties:
    - row_index (integer)
    - column_index (integer)
    - value (color, integer > 0)
    - column_parity (even/odd based on column_index)
  Role: Initiate painting/filling process.

Target Cells:
  Identification: All cells in the output grid.
  Properties:
    - row_index (integer)
    - column_index (integer)
    - value (color, integer >= 0)

Action:
  Name: Paint Grid
  Rule: Assign color to target cells based on proximity to source cells and column parity matching.
  Proximity Metric: Manhattan Distance (|row1 - row2| + |col1 - col2|)

Relationships:
  - Each target cell's value is determined by the nearest unique source cell in the input.
  - Tie-breaking: If a target cell is equidistant to multiple source cells, its value remains 0.
  - Parity Constraint: A target cell (tr, tc) can only receive color from a source cell (sr, sc) if tc % 2 == sc % 2. If the closest unique source does not satisfy this parity constraint, the target cell's value remains 0.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled with zeros.
2.  Identify all source cells in the input grid: find coordinates `(sr, sc)` and value `sv` for all cells where `sv > 0`. Store these sources along with their column parity (`sc % 2`).
3.  Iterate through each target cell `(tr, tc)` in the grid dimensions.
4.  For the current target cell `(tr, tc)`:
    a.  Calculate the Manhattan distance from `(tr, tc)` to every source cell `(sr, sc)`.
    b.  Find the minimum distance calculated.
    c.  Identify all source cells that are at this minimum distance.
    d.  If there is exactly one unique source cell `(sr_closest, sc_closest)` with value `sv_closest` at the minimum distance:
        i.  Check if the target column parity `(tc % 2)` matches the source column parity `(sc_closest % 2)`.
        ii. If the parities match, set the value of the output grid cell `(tr, tc)` to `sv_closest`.
        iii. If the parities do *not* match, the output grid cell `(tr, tc)` remains 0.
    e.  If there is zero or more than one source cell at the minimum distance (a tie), the output grid cell `(tr, tc)` remains 0.
5.  Return the completed output grid.
```python
"""
Transforms an input grid by "painting" cells based on the nearest non-zero source cell from the input, subject to a column parity constraint.

1. Identifies all non-zero "source" cells in the input grid, noting their value, coordinates, and column parity.
2. Initializes an output grid of the same dimensions as the input, filled with zeros.
3. For each cell in the grid:
   a. Calculates the Manhattan distance to all source cells.
   b. Finds the minimum distance.
   c. Identifies all source cells at that minimum distance.
   d. If exactly one source cell is closest:
      i. Checks if the current cell's column index has the same parity (even/odd) as the closest source cell's column index.
      ii. If the parities match, the output cell takes the value of the closest source cell.
   e. If there's a tie for the closest source cell, or if the single closest source doesn't match the column parity, the output cell remains zero.
4. Returns the painted output grid.
"""

import math

def manhattan_distance(r1: int, c1: int, r2: int, c2: int) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the nearest-source painting rule with column parity constraint.
    """
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find all source cells (non-zero values in input)
    # Store as (row, col, value, column_parity)
    sources = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] != 0:
                sources.append((r, c, input_grid[r][c], c % 2))

    # If there are no sources, return the zero grid
    if not sources:
        return output_grid

    # Iterate through each cell in the grid to determine its output value
    for tr in range(rows):
        for tc in range(cols):
            min_dist = float('inf')
            closest_sources = [] # Stores (value, source_col_parity) for tied sources

            # Calculate distance to each source
            for sr, sc, sv, sparity in sources:
                dist = manhattan_distance(tr, tc, sr, sc)

                # If this source is closer than the current minimum
                if dist < min_dist:
                    min_dist = dist
                    closest_sources = [(sv, sparity)] # Reset list with this source
                # If this source is equally close as the current minimum
                elif dist == min_dist:
                    closest_sources.append((sv, sparity)) # Add to list

            # Determine the output value based on closest sources and parity
            if len(closest_sources) == 1:
                source_value, source_col_parity = closest_sources[0]
                target_col_parity = tc % 2
                # Check if target column parity matches the unique closest source's column parity
                if target_col_parity == source_col_parity:
                    output_grid[tr][tc] = source_value
            # If there's a tie (len > 1) or no sources found (len == 0, though unlikely after initial check),
            # or if the unique closest source parity doesn't match, the cell remains 0 (already initialized).

    return output_grid
```
