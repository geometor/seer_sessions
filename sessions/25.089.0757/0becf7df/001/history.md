
## train_1

**input:**
```
4 2 0 0 0 0 0 0 0 0
3 7 0 0 0 0 4 0 0 0
0 0 0 0 0 3 4 4 0 0
0 0 0 0 0 3 2 4 0 0
0 0 0 7 7 3 2 4 0 0
0 0 0 7 3 3 2 0 0 0
0 0 0 7 0 0 2 2 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 2 0 0 0 0 0 0 0 0
3 7 0 0 0 0 2 0 0 0
0 0 0 0 0 7 2 2 0 0
0 0 0 0 0 7 4 2 0 0
0 0 0 3 3 7 4 2 0 0
0 0 0 3 7 7 4 0 0 0
0 0 0 3 0 0 4 4 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 3 0 0 0 0 0 0 0 0
2 8 0 0 0 0 1 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 3 3 3 3 1 8 0 0
0 0 3 3 2 0 8 8 0 0
0 0 0 0 2 0 8 8 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 3 0 0 0 0 0 0 0 0
2 8 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 0 0 0
0 0 0 0 3 3 3 0 0 0
0 0 1 1 1 1 3 2 0 0
0 0 1 1 8 0 2 2 0 0
0 0 0 0 8 0 2 2 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
9 4 0 0 0 0 0 0 0 0
7 6 0 0 0 9 9 0 0 0
0 0 0 0 0 7 9 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 7 4 0 0 0 0
0 0 0 6 6 7 0 0 0 0
0 0 0 7 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 4 0 0 0 0 0 0 0 0
7 6 0 0 0 4 4 0 0 0
0 0 0 0 0 6 4 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 6 9 0 0 0 0
0 0 0 7 7 6 0 0 0 0
0 0 0 6 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the transformation in these examples.

**Perception of Task Elements**

1.  **Input/Output Structure:** Both input and output are grids of the same dimensions (10x10 in these examples).
2.  **Key Area:** The top-left 2x2 area seems distinct and important. It contains four non-white pixels in all examples.
3.  **Main Grid Area:** The rest of the grid contains various shapes and patterns composed of different colors.
4.  **Transformation:** The transformation appears to be a color substitution applied to the main grid area, while the top-left 2x2 area remains unchanged. The specific colors involved in the substitution seem to be defined by the colors within that top-left 2x2 area.
5.  **Color Swapping:** By comparing input and output grids (excluding the top-left 2x2), specific colors in the input are consistently replaced by other specific colors in the output. For example, in `train_1`:
    *   Input yellow (4) becomes red (2).
    *   Input red (2) becomes yellow (4).
    *   Input green (3) becomes orange (7).
    *   Input orange (7) becomes green (3).
    *   These substitutions correspond exactly to the pairs of colors found horizontally in the top-left 2x2 area: (yellow, red) i.e., (4, 2) in the first row, and (green, orange) i.e., (3, 7) in the second row.
6.  **Consistency:** This pattern of defining color swaps using the top-left 2x2 pairs holds true for `train_2` ((blue, green) <-> (1, 3), (red, azure) <-> (2, 8)) and `train_3` ((maroon, yellow) <-> (9, 4), (orange, magenta) <-> (7, 6)).
7.  **Scope:** The color swapping rule applies only to the pixels *outside* the top-left 2x2 area. The pixels within the 2x2 area ((0,0), (0,1), (1,0), (1,1)) are preserved exactly as they were in the input. Other colors (like white/0) not involved in the defined swaps also remain unchanged.

**YAML Facts**


```yaml
Grid_Properties:
  - Dimensions: Consistent between input and output for each example.
  - Background: Predominantly white (0).

Objects:
  - Type: Control_Area
    Location: Top-left 2x2 corner (cells (0,0), (0,1), (1,0), (1,1)).
    Content: Contains four non-white pixels defining color pairs.
    Persistence: Unchanged between input and output.
  - Type: Main_Grid_Content
    Location: All cells outside the Control_Area.
    Content: Various shapes and patterns made of non-white pixels.
    Transformation: Undergoes color substitution based on rules from Control_Area.

Color_Pairs:
  - Source: Defined by the Control_Area.
  - Pair_1: Color at (0,0) and color at (0,1). Let's call them C1 and C2.
  - Pair_2: Color at (1,0) and color at (1,1). Let's call them C3 and C4.

Actions:
  - Identify: Determine the four colors (C1, C2, C3, C4) in the Control_Area of the input.
  - Map_Colors: Establish a swapping map: C1 <-> C2, C3 <-> C4.
  - Apply_Map: Iterate through all cells in the Main_Grid_Content of the input.
  - Substitute: For each cell in the Main_Grid_Content:
      - If color is C1, replace with C2 in the output.
      - If color is C2, replace with C1 in the output.
      - If color is C3, replace with C4 in the output.
      - If color is C4, replace with C3 in the output.
      - Otherwise, keep the original color.
  - Preserve: Copy the Control_Area from the input directly to the output.

Relationships:
  - The Control_Area defines the color transformation rules for the Main_Grid_Content.
  - The transformation affects only colors present in the Control_Area pairs.
  - The transformation preserves the spatial arrangement (shape and position) of pixels in the Main_Grid_Content, only altering their colors according to the defined swaps.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the four colors in the top-left 2x2 area of the input grid:
    *   `ColorA` = color at `(row=0, col=0)`
    *   `ColorB` = color at `(row=0, col=1)`
    *   `ColorC` = color at `(row=1, col=0)`
    *   `ColorD` = color at `(row=1, col=1)`
3.  Iterate through each cell `(r, c)` of the grid, starting from `r=0` up to `height-1` and `c=0` up to `width-1`.
4.  Check if the current cell `(r, c)` is *outside* the top-left 2x2 area (i.e., if `r >= 2` or `c >= 2`).
5.  If the cell is outside the top-left 2x2 area:
    *   Let `CurrentColor` be the color of the cell `(r, c)` in the input grid.
    *   If `CurrentColor` is `ColorA`, change the color of the cell `(r, c)` in the output grid to `ColorB`.
    *   Else if `CurrentColor` is `ColorB`, change the color of the cell `(r, c)` in the output grid to `ColorA`.
    *   Else if `CurrentColor` is `ColorC`, change the color of the cell `(r, c)` in the output grid to `ColorD`.
    *   Else if `CurrentColor` is `ColorD`, change the color of the cell `(r, c)` in the output grid to `ColorC`.
    *   (If `CurrentColor` is none of these, the output grid already has the correct, unchanged color from the initial copy).
6.  (If the cell is *inside* the top-left 2x2 area, do nothing, as the output grid already has the correct, unchanged color from the initial copy).
7.  After checking all cells, return the modified output grid.
