
## train_1

**input:**
```
0 0 0 0 0 0 8 0 0 0
0 2 2 2 0 8 8 8 0 0
0 2 2 2 0 0 8 8 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 5 5 5 0
0 0 1 1 1 0 0 5 5 0
0 0 1 1 1 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 4 4
0 0 0 0 0 0 4 4
0 0 4 0 0 0 4 4
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
7 7 0 0 0 2 0 0
7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 7 7 7 0
0 3 3 3 0 7 7 7 0
0 0 3 0 0 7 7 7 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input/Output:** Both are 2D grids (matrices) containing single-digit integers (0-9). The digit '0' consistently represents the background.
2.  **Objects:** The core objects are "regions" or "blobs" of connected cells sharing the same non-zero digit. Connectivity is defined by horizontal and vertical adjacency (not diagonal).
3.  **Properties:**
    *   Each region has a specific color (the digit value).
    *   Each region has a shape and size (number of cells).
    *   Each region has a position within the grid.
    *   A key property seems to be whether any part of the region touches the outer border/edge of the grid.
4.  **Transformation:** The transformation involves selectively removing entire regions based on a specific property. Regions that are removed are replaced by the background color '0'. Regions that are not removed remain unchanged in the output.
5.  **Underlying Rule:** Based on the examples, the rule appears to be: Identify all connected regions of non-zero colors. If *any* cell belonging to a region is located on the grid's outermost border (top row, bottom row, leftmost column, or rightmost column), then the *entire* region is removed (set to '0'). If a region is entirely contained within the grid and does not touch any border, it is preserved in the output.

**YAML Fact Documentation:**


```yaml
task_description: Remove connected regions of color if they touch the grid border.

elements:
  - element: grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (e.g., 10x10, 8x8, 9x9)
      - cell_values: integers 0-9
      - background_color: 0

  - element: region
    properties:
      - type: connected component of non-zero cells
      - connectivity: horizontal and vertical adjacency
      - color: the integer value (1-9) shared by cells in the region
      - location: set of coordinates (row, col) occupied by the region
      - border_touching: boolean (true if any cell in the region is in row 0, last row, col 0, or last col)

actions:
  - action: identify_regions
    input: input grid
    output: list of regions (each with color, coordinates, border_touching property)
    description: Finds all connected components of non-zero cells. For each component, determine its color, cell coordinates, and whether it touches the grid border.

  - action: filter_regions
    input: list of regions
    output: list of regions_to_keep
    description: Selects only those regions where the 'border_touching' property is false.

  - action: generate_output_grid
    input:
      - input grid dimensions
      - list of regions_to_keep
    output: output grid
    description: Creates a new grid filled with the background color ('0'). Then, for each region in 'regions_to_keep', place its color value at its corresponding coordinates in the new grid.

relationships:
  - relationship: border_determines_removal
    subject: region
    object: grid border
    description: A region's 'border_touching' status determines if it is kept or removed in the output grid. Removal applies to the entire region if any part touches the border.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color '0'.
2.  Find all distinct connected regions of cells in the input grid that have the same non-zero color. Use 4-way adjacency (up, down, left, right) to determine connectivity.
3.  For each identified region:
    a.  Check if any cell belonging to this region is located at row 0, the last row, column 0, or the last column of the input grid.
    b.  If *none* of the cells in the region touch any of the grid's borders, then copy all cells belonging to this region (with their original color) from the input grid to the corresponding positions in the output grid.
4.  Return the final output grid.
