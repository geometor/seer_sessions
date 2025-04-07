*   **Perception of Task Elements:**
    *   The input and output are grids of numbers (colors), primarily 0 (black), 2 (blue), 3 (red), and 8 (orange).
    *   The transformation modifies the color '2' within distinct connected regions (shapes).
    *   The grid appears conceptually divided into four quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right), often separated by rows/columns of zeros.
    *   Shapes composed of the color '2' exist within these quadrants. Sometimes a quadrant may contain multiple disjoint shapes of color '2'.
    *   The final color of a shape (or shapes) in a quadrant depends on a comparison between shapes in diagonally opposite quadrants (TL vs BR, TR vs BL).
    *   The comparison involves both the spatial pattern of the '2's within the shapes and their size (number of '2' cells).

*   **YAML Fact Document:**
    
```yaml
    Objects:
      - Grid: A 2D array of integer values representing colors.
      - Cell: An individual element within the Grid, having a position (row, col) and a color value.
      - Shape: A connected component of Cells with color 2 in the input Grid.
      - Quadrant: Conceptual regions of the Grid (Top-Left, Top-Right, Bottom-Left, Bottom-Right), defined relative to the Grid's center or separating zero-lines.

    Properties:
      - Cell:
        - color: Integer value (0, 2, 3, 8).
        - position: (row, col).
      - Shape:
        - cells: List of Cell positions belonging to the shape.
        - pattern: The relative arrangement of '2's within the shape's bounding box (or a canonical representation).
        - size: The number of cells in the shape (count of '2's).
        - quadrant: The Quadrant the shape primarily belongs to (e.g., based on the center of its bounding box).
        - input_color: Always 2 for shapes considered.
        - output_color: The determined color (2, 3, or 8) for the shape in the output Grid.

    Actions:
      - Identify_Shapes: Find all connected components of color 2 in the input Grid.
      - Assign_Quadrants: Determine the Quadrant for each identified Shape. If multiple shapes are in one quadrant, treat them as a single entity for comparison (combine patterns, sum sizes).
      - Get_Shape_Properties: For each Quadrant (or combined entity), determine its pattern and size.
      - Compare_Diagonal_Patterns:
        - Compare the pattern of the TL shape(s) with the BR shape(s).
        - Compare the pattern of the TR shape(s) with the BL shape(s).
      - Compare_Diagonal_Sizes: (Used if patterns do not match)
        - Compare the size of the TL shape(s) with the BR shape(s).
        - Compare the size of the TR shape(s) with the BL shape(s).
      - Determine_Output_Color: Assign an output_color (2, 3, or 8) to the shape(s) in each Quadrant based on the results of the pattern and size comparisons.
      - Recolor_Grid: Create the output Grid by replacing the color of the cells belonging to the input shapes with their determined output_color. Cells not part of an initial color 2 shape remain unchanged.

    Relationships:
      - Shape belongs_to Quadrant.
      - Shapes are compared diagonally (TL <-> BR, TR <-> BL).
      - Output_color depends_on pattern_match (diagonal comparison).
      - If patterns do not match, Output_color depends_on size_comparison (diagonal comparison).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct connected shapes formed by cells with color 2 in the input grid.
    3.  For each shape, determine its primary quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) based on its position (e.g., center of bounding box relative to grid center).
    4.  Group the shapes by quadrant. If a quadrant contains multiple shapes, treat them as a single logical entity: calculate a combined pattern (representing all '2's in that quadrant relative to a common bounding box or origin) and a total size (sum of '2's in all shapes within that quadrant). If a quadrant has no shape of color 2, its pattern is empty and size is 0.
    5.  Define the shape entities for each quadrant: `TL_Shape`, `TR_Shape`, `BL_Shape`, `BR_Shape`, along with their respective patterns (`P_TL`, `P_TR`, `P_BL`, `P_BR`) and sizes (`S_TL`, `S_TR`, `S_BL`, `S_BR`).
    6.  Compare the Top-Left and Bottom-Right shapes:
        *   If `P_TL` is identical to `P_BR`: Assign output color 2 to `TL_Shape` and output color 3 to `BR_Shape`.
        *   If `P_TL` is different from `P_BR`:
            *   If `S_TL > S_BR`: Assign output color 3 to `TL_Shape` and output color 8 to `BR_Shape`.
            *   If `S_TL <= S_BR`: Assign output color 8 to `TL_Shape` and output color 3 to `BR_Shape`.
    7.  Compare the Top-Right and Bottom-Left shapes:
        *   If `P_TR` is identical to `P_BL`: Assign output color 8 to `TR_Shape` and output color 8 to `BL_Shape`.
        *   If `P_TR` is different from `P_BL`:
            *   If `S_TR > S_BL`: Assign output color 8 to `TR_Shape` and output color 2 to `BL_Shape`.
            *   If `S_TR <= S_BL`: Assign output color 2 to `TR_Shape` and output color 8 to `BL_Shape`.
    8.  For every original shape identified in step 2, find its assigned output color based on its quadrant (determined in step 6 or 7) and update the color of all its constituent cells in the output grid to this assigned color.
    9.  Return the modified output grid.