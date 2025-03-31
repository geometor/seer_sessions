**Perception:**

The input grids contain multiple distinct "plus-sign" shapes, each made of a single non-white color against a white background. These shapes are always 3x3, with a white center and four adjacent pixels of the shape's color. The task involves identifying these plus-sign shapes, extracting them, and arranging them into a new grid. The arrangement in the output can be either a vertical stack or a horizontal row, preserving the relative order of the shapes from the input (top-to-bottom for vertical stacking, left-to-right for horizontal arrangement).

**Facts:**


```yaml
Input_Features:
  - Grid: 2D array of integers (0-9) representing colors.
  - Background: Primarily white (0).
  - Objects:
    - Multiple distinct objects present.
    - Each object is a connected component of non-white pixels.
    - Shape: All objects are 3x3 plus signs (white center, four adjacent pixels of the same color, white corners).
    - Colors: Objects can be green(3), blue(1), azure(8), red(2).
    - Separation: Objects are separated by white pixels.
    - Arrangement: Objects can be arranged vertically, horizontally, or scattered in the input grid.

Output_Features:
  - Grid: 2D array of integers (0-9).
  - Content: Composed solely of the 3x3 plus-sign shapes extracted from the input.
  - Background: White (0) pixels fill the space within each 3x3 shape's bounding box but not necessarily between shapes if they are directly adjacent in the output.
  - Arrangement:
    - The extracted 3x3 shapes are concatenated either vertically or horizontally.
    - Vertical Concatenation: Shapes are stacked one below the other. Output width is 3. Output height is 3 * number_of_shapes.
    - Horizontal Concatenation: Shapes are placed side-by-side. Output height is 3. Output width is 3 * number_of_shapes.
  - Order:
    - For vertical stacking: Shapes are ordered top-to-bottom based on their original top-most position in the input grid.
    - For horizontal arrangement: Shapes are ordered left-to-right based on their original left-most position in the input grid.

Transformation:
  - Action: Identify, Extract, Sort, Concatenate.
  - Identify: Locate all 3x3 plus-sign shapes in the input grid.
  - Extract: Crop each identified shape to its 3x3 bounding box.
  - Sort: Order the extracted 3x3 shapes based on their original position in the input grid. The sorting key (top row or left column) depends on the final output arrangement (vertical or horizontal).
  - Concatenate: Assemble the sorted 3x3 shapes into the final output grid, either stacking vertically or arranging horizontally.
```


**Natural Language Program:**

1.  Identify all distinct connected groups of non-white pixels in the input grid.
2.  For each group, determine its bounding box.
3.  Filter these groups to keep only those that perfectly match the 3x3 plus-sign pattern (a 3x3 area with a white center, four adjacent pixels of the *same* non-white color, and white corners). Record the 3x3 subgrid and the top-left coordinates of its bounding box in the original input.
4.  Collect all the valid 3x3 plus-sign subgrids found.
5.  Determine the intended output arrangement (vertical stack or horizontal row). *This might be inferred from the relative positions of the objects in the input or potentially from test output dimensions if available.*
6.  If the intended output is a vertical stack:
    a.  Sort the collected 3x3 subgrids based on the original top row coordinate (ascending).
    b.  Concatenate the sorted subgrids vertically to form the output grid.
7.  If the intended output is a horizontal row:
    a.  Sort the collected 3x3 subgrids based on the original left column coordinate (ascending).
    b.  Concatenate the sorted subgrids horizontally to form the output grid.