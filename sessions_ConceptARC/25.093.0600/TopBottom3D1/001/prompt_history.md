
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 4 4 4 4 3 0
0 3 4 4 4 4 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 3 3 3 3 3 0
0 3 3 3 3 3 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```


**output:**
```
0 0 0 6 0 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a 2D grid of numbers (representing colors). The core operation appears to be a "fill" or "paint bucket" like function, constrained by specific boundaries within the grid.

1.  **Grid Structure:** Both input and output are 2D grids of the same dimensions, containing single digits (0-9). '0' consistently represents the background color.
2.  **Colored Regions:** Non-zero numbers form distinct regions or shapes within the grid.
3.  **Boundary/Frame:** In each example, there's a specific non-zero color that acts as a frame or boundary (`C_frame`). This frame partially or fully encloses regions of other non-zero colors.
4.  **Enclosed Area:** The area inside the `C_frame` boundary contains other non-zero colors (`C_inner`).
5.  **External Area:** Areas outside the `C_frame` boundary, including the background (0) and potentially other non-zero colored regions not enclosed by `C_frame`, are considered external.
6.  **Transformation:** The transformation identifies the `C_frame` color and the region it encloses. All cells within this enclosed region that originally had a `C_inner` color are changed to the `C_frame` color in the output. The `C_frame` cells themselves, the background (0), and any non-zero cells in the external area remain unchanged.

## Facts


```yaml
---
task_elements:
  - name: Grid
    type: Container
    properties:
      - dimensions: [rows, columns] (constant between input/output)
      - elements: Cells

  - name: Cell
    type: Element
    properties:
      - position: [row, column]
      - color: integer (0-9)
      - state: (derived) external or internal relative to the frame

  - name: Background
    type: Region
    properties:
      - color: 0
      - state: external

  - name: Frame Region
    type: Region
    properties:
      - color: C_frame (specific non-zero integer, e.g., 1, 3, 7 in examples)
      - connectivity: Forms a boundary separating internal and external areas
      - state: external (in the sense that its color is preserved)

  - name: Enclosed Region
    type: Region
    properties:
      - color: C_inner (one or more non-zero integers different from C_frame)
      - location: Geometrically inside the Frame Region
      - state: internal

  - name: External Non-Frame Region
    type: Region
    properties:
      - color: Non-zero integer (potentially same as C_inner, but located outside)
      - location: Geometrically outside the Frame Region
      - state: external

relationships:
  - type: Adjacency
    between: [Cell, Cell]
    properties: [4-connectivity (up, down, left, right)]
  - type: Enclosure
    subject: Frame Region
    object: Enclosed Region
  - type: Reachability
    description: Cells reachable from the Background without crossing the Frame Region color are external.

actions:
  - name: Identify Frame Color (C_frame)
    input: Input Grid
    output: C_frame color value
    method: Find the unique non-zero color C such that treating C as a wall isolates other non-zero colors from the background during a flood fill starting from the background.
  - name: Determine Reachability (Flood Fill)
    input: [Input Grid, C_frame]
    output: Set of coordinates for "external" cells
    method: Perform a flood fill starting from all background (0) cells. The fill can propagate to adjacent cells unless the target cell has the C_frame color. Mark all reached cells as external.
  - name: Generate Output Grid
    input: [Input Grid, C_frame, External Cells Set]
    output: Output Grid
    method: Iterate through input grid cells. If a cell's color is C_frame, copy C_frame to output. If a cell is marked external, copy its input color to output. If a cell is not external and not C_frame, set its output color to C_frame.
---
```


## Natural Language Program

1.  **Identify** the unique non-zero color (`C_frame`) in the input grid that acts as a boundary, such that if cells of this color were treated as impassable walls, a flood fill starting from the background (color 0) would fail to reach at least one other non-zero colored cell.
2.  **Perform** a flood fill starting from all background cells (color 0) in the input grid. This fill can move to adjacent cells (up, down, left, right) but *cannot* enter cells whose color is `C_frame`.
3.  **Mark** all cells reached by this flood fill as "external". All other cells (including the `C_frame` cells themselves and any unreached non-zero cells) are considered "internal" in terms of reachability, though `C_frame` cells are treated specially.
4.  **Create** a new output grid with the same dimensions as the input grid.
5.  **Iterate** through each cell `(r, c)` of the input grid:
    a.  If the input cell `(r, c)` has the color `C_frame`, set the output cell `(r, c)` to `C_frame`.
    b.  Else if the input cell `(r, c)` is marked "external" (from step 3), copy the input cell's color to the output cell `(r, c)`.
    c.  Else (the cell is not `C_frame` and was not marked "external"), set the output cell `(r, c)` to the `C_frame` color.
6.  **Return** the completed output grid.
