
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 4 0 4 0 4 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 4 0 4 0 4 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves identifying different colored objects within a grid and moving some of them based on the position and shape of the largest object.

1.  **Object Identification**: In both examples, the input grid contains multiple non-background objects (pixels or groups of pixels). One object is significantly larger (in terms of pixel count) than the others.
2.  **Static vs. Mobile Objects**: The largest object remains stationary in the output grid (it acts as a "wall" or "anchor"). The smaller objects ("movers") change their positions.
3.  **Movement Pattern**: The movers shift horizontally towards a specific target column determined by the wall.
4.  **Wall Type & Target Column**:
    *   If the wall is a vertical line (like the green line in train_1), the target column is the column immediately to the left of the wall.
    *   If the wall is a horizontal line (like the red line in train_2), the target column is the horizontal midpoint (center column, rounded down) of the wall.
5.  **Mover Arrangement & Final Placement**:
    *   **Co-linear Movers (train_1)**: If all movers initially lie on the same row, they are treated as a single pattern. This pattern is shifted horizontally so that its rightmost pixel lands in the target column. The original row and relative horizontal spacing are maintained.
    *   **Scattered Movers (train_2)**: If movers are scattered across different rows and columns, they are moved individually to the target column. Their final vertical positions are determined by stacking them vertically within the target column, starting one row below the lowest extent of the wall. The original top-to-bottom order of the movers is preserved, and one empty row is left between each stacked mover.
6.  **Color Preservation**: Movers retain their original colors. The wall retains its original color and position. Background pixels remain background unless replaced by a moved object.

## Facts


```yaml
Input:
  - Grid: 2D array of integer colors (0-9)
  - Background: Color 0 (white)
  - Objects: Connected components of non-background pixels

Identify Components:
  - Find all connected components (pixels of the same non-zero color adjacent horizontally or vertically).
  - Count pixels in each component.

Identify Wall and Movers:
  - Wall: The component with the largest number of pixels. It remains static.
  - Movers: All other components. They change position.

Calculate Wall Properties:
  - Bounding Box: Min/Max row and column indices (Rmin, Rmax, Cmin, Cmax).
  - Width: Cmax - Cmin + 1
  - Height: Rmax - Rmin + 1

Determine Target Column (C_target):
  - If Wall is vertical (Width == 1): C_target = Cmin - 1
  - If Wall is horizontal (Height == 1): C_target = floor((Cmin + Cmax) / 2)
  # Note: Assumes wall is strictly vertical or horizontal based on examples.

Determine Movement Strategy based on Movers' initial positions:
  - Strategy 1 (Co-linear): If all movers share the same initial row index.
  - Strategy 2 (Scattered): If movers occupy different initial rows.

Apply Movement Strategy:
  - Strategy 1 (Co-linear):
    - Find the rightmost column (max_col) occupied by any mover pixel in the shared row.
    - Calculate shift distance: shift = C_target - max_col.
    - Move all mover pixels in that row horizontally by 'shift' columns.
  - Strategy 2 (Scattered):
    - Create a list of movers, storing their original color and top row index.
    - Sort the list by the original top row index (ascending).
    - Determine starting row for stacking: Start_Row = Rmax (of Wall) + 1.
    - Initialize current row: Current_Row = Start_Row.
    - For each mover in the sorted list:
      - Place the mover's pixels in the output grid, translated so their top-left corner (or reference point) is at (Current_Row, C_target). Adjust relative positions if mover is multi-pixel. (Simpler: For single-pixel movers, place at (Current_Row, C_target)).
      - Update current row for the next mover: Current_Row = Current_Row + 2 (to leave one empty row).

Construct Output Grid:
  - Start with a background grid of the same dimensions as the input.
  - Place the Wall pixels at their original positions.
  - Place the Mover pixels at their calculated final positions.

```


## Natural Language Program

1.  Create the output grid, initially filled with the background color (white, 0), having the same dimensions as the input grid.
2.  Find all distinct connected components of non-background colors in the input grid.
3.  Identify the component with the maximum number of pixels; this is the "Wall". Copy the Wall pixels to their original positions in the output grid.
4.  Identify all other components; these are the "Movers". Collect their original pixel coordinates and colors.
5.  Calculate the bounding box (minimum/maximum row and column) of the Wall.
6.  Determine the target column (`C_target`) for the Movers:
    *   If the Wall's width is 1 (vertical line), set `C_target` to the Wall's column minus 1.
    *   If the Wall's height is 1 (horizontal line), set `C_target` to the floor of the average of the Wall's minimum and maximum column indices (its horizontal center).
7.  Check if all Mover components lie entirely on the same row in the input grid.
8.  **If all Movers are on the same row**:
    *   Find the maximum column index occupied by any pixel of any Mover on that row.
    *   Calculate the horizontal shift required: `shift = C_target - maximum_column_index`.
    *   For each pixel belonging to any Mover, add the `shift` to its column index to get its new position. Copy the Mover pixel's color to this new position in the output grid.
9.  **If Movers are on different rows (Scattered)**:
    *   Create a list of Movers, recording the original color and minimum row index for each.
    *   Sort this list based on the minimum row index (top to bottom).
    *   Set the starting row for placement (`Current_Row`) to the Wall's maximum row index plus 1.
    *   Iterate through the sorted list of Movers:
        *   For the current Mover, determine its new top-left position (or single pixel position if it's a single pixel) as (`Current_Row`, `C_target`).
        *   Copy the Mover's pixels (with their original color), translated to this new position, onto the output grid.
        *   Increment `Current_Row` by 2 for the next Mover (placing one empty row between Movers).
10. Return the completed output grid.
