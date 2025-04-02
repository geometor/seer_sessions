
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0 0 4 4 4
0 0 0 4 4 4 4 0 0 4 4 4
0 0 0 4 4 4 4 0 0 4 4 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 6 6 6 0 0 0 6 6 6 6 0 6 6
0 0 0 6 6 6 0 0 0 6 6 6 6 0 6 6
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 6 6 6 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6 6 0 0
0 0 6 6 0 0 6 6 0 0 6 6 6 6 0 0
0 0 6 6 0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 6 0 0 6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 6 6 0 0 0 6 6 6 6 0 6 6
0 0 0 6 6 6 0 0 0 6 6 6 6 0 6 6
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 1 0 0 0 0 0 0 0 1 1 0 0
0 0 1 1 1 0 0 1 1 1 0 0 1 1 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
1 1 0 1 1 1 0 0 0 1 1 1 0 0 0 0
1 1 0 1 1 1 0 0 0 1 1 1 0 0 0 0
1 1 0 0 0 0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 1 1 1 0 0 0 0 0 0 0 1 1 0 0
0 0 1 1 1 0 0 1 1 1 0 0 1 1 0 0
0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of the Elements:**

1.  **Input Grid Structure:** Each input grid appears to be divided into three main sections: an upper area containing colored objects, a distinct horizontal line, and a lower area also containing colored objects. The background color is consistently white (0).
2.  **Dividing Line:** There's a unique horizontal line in each input grid that spans the entire width.
    *   In `train_1`, it's a solid red (2) line.
    *   In `train_2`, it's a solid green (3) line.
    *   In `train_3`, it's an alternating azure (8) and white (0) line.
    This line acts as a clear separator. The color or pattern of this line seems distinct within each grid, not appearing as the main color of the other objects.
3.  **Objects:** Above and below the dividing line, there are distinct objects composed of contiguous blocks of a single color (yellow, magenta, blue). These objects vary in shape, size, and position across examples.
4.  **Transformation:** The transformation preserves the upper section of the grid (including the objects within it) and the dividing line itself. However, the entire section *below* the dividing line is cleared, meaning all pixels in the rows below the dividing line are set to white (0).
5.  **Output Grid Structure:** The output grid retains the dimensions of the input grid. It consists of the original upper section, the original dividing line, and a lower section filled entirely with white (0).

**YAML Facts:**


```yaml
task_elements:
  - item: Grid
    properties:
      - Contains distinct regions: upper, dividing_line, lower.
      - Background color is white (0).
  - item: Objects
    properties:
      - Located in the upper and lower regions.
      - Composed of contiguous pixels of a single non-white color (e.g., yellow, magenta, blue).
      - Vary in shape, size, and position.
  - item: Dividing_Line
    properties:
      - A single horizontal row.
      - Spans the full width of the grid.
      - Composition is unique within the grid (either a solid non-white color or a repeating pattern like azure/white).
      - Color/pattern is distinct from the primary colors of the objects above and below it.
      - Separates the upper and lower regions.
    location:
      - Row index varies per example.
  - item: Transformation
    action:
      - Identify the row index of the Dividing_Line.
      - Preserve all rows from the top of the grid down to and including the Dividing_Line row.
      - Replace all pixels in the rows below the Dividing_Line row with white (0).
    relationship:
      - The Dividing_Line determines the boundary for the preservation/replacement action. Content above and including the line is kept; content below is erased.
```


**Natural Language Program:**

1.  Scan the input grid row by row to identify the unique horizontal dividing line. This line is characterized by spanning the full width of the grid and having a unique color composition (either a single solid color different from the object colors or a distinct repeating pattern like color A / color B) for that specific row.
2.  Determine the row index of this dividing line.
3.  Create a new grid with the same dimensions as the input grid.
4.  Copy all rows from the input grid, starting from the top row (index 0) down to and including the identified dividing line row, into the new grid.
5.  Fill all remaining rows in the new grid (those below the dividing line row) entirely with the white color (0).
6.  The resulting new grid is the output.
