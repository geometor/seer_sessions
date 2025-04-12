
## train_1

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 0 0 0 0 3 3
3 3 3 3 3 3 0 3 3 0 3 3
3 3 3 3 3 3 0 3 3 0 3 3
3 3 3 3 3 3 0 0 0 0 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
3 3
3 3
```


## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4
4 4 0 4 4 4 4 4 4 4 4
4 0 4 0 4 4 4 4 4 4 4
0 4 4 4 0 4 4 4 4 4 4
4 0 4 0 4 4 0 0 0 0 4
4 4 0 4 4 4 0 4 4 0 4
4 4 4 4 4 4 0 4 4 0 4
4 4 4 4 4 4 0 4 4 0 4
4 4 4 4 4 4 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
0 4 0 4 4
4 4 4 4 4
0 4 0 4 4
```

*   **Perception:**
    1.  The input grids contain a background color filling most of the area.
    2.  There is a distinct hollow rectangular frame object within the input grid, composed of a single color different from the background. The frame appears to be one pixel thick.
    3.  The area enclosed by the frame is filled with the same color as the background.
    4.  The output grid's content and structure seem derived from the frame and the content it encloses.
    5.  There appears to be a conditional transformation rule based on the shape (square vs. rectangle) of the area enclosed by the frame.

*   **YAML Facts:**


```yaml
Task: Extract content within a frame and potentially transform it based on shape.

Input_Features:
  - Grid: 2D array of pixels (colors 0-9).
  - Background: The most frequent pixel color in the grid.
  - Frame:
      Object_Type: Hollow rectangle.
      Property: Composed of a single color (F) different from the Background color.
      Property: Thickness of 1 pixel.
      Property: Dimensions (FrameHeight, FrameWidth).
      Relationship: Must exist uniquely in the input grid.
  - InnerContent:
      Object_Type: Solid rectangle.
      Relationship: Enclosed by the Frame.
      Property: Composed of a single color (C), same as the Background color.
      Property: Dimensions (ContentHeight = FrameHeight - 2, ContentWidth = FrameWidth - 2).
      Property: Shape (Square if ContentHeight == ContentWidth, Rectangle otherwise).
      Data: The grid of pixels forming the InnerContent (InnerGrid).

Output_Features:
  - Grid: A 2D array of pixels, derived from Frame and InnerContent.
  - Derivation_Rule: Conditional based on InnerContent shape.

Transformation_Logic:
  - Find: Identify the Background color, the Frame color (F), Frame dimensions (FH, FW), InnerContent color (C), and InnerContent grid (InnerGrid) with dimensions (CH, CW).
  - Condition: Check if InnerGrid is square (CH == CW).
  - Case_Square:
      Action: Output is the InnerGrid directly.
  - Case_Rectangle:
      Action: Construct a new output grid.
      Output_Dimensions: CH x FH (ContentHeight x FrameHeight).
      Define_Columns:
        - ContentColumn (ColC): The first column of InnerGrid.
        - ModifiedColumn (ColM): Copy of ContentColumn with the top (row 0) and bottom (row CH-1) pixels replaced by the FrameColor (F).
      Assemble_Output:
        - Create a sequence S of columns by repeating [ColM, ColC] CW times.
        - Append ColC to S until S has length FH.
        - Truncate S to length FH if it exceeds it (shouldn't happen with the previous step).
        - Combine columns in S to form the output grid.
```


*   **Natural Language Program:**

1.  Determine the background color, which is the most frequent color in the input grid.
2.  Identify the unique, hollow, single-color, 1-pixel-thick rectangular frame object in the input grid whose color is different from the background color. Record the frame's color (F), height (FH), and width (FW).
3.  Extract the rectangular block of pixels (InnerGrid) enclosed by the frame. Record its height (CH), width (CW), and assume it contains a uniform color (C, which should match the background color).
4.  Check if the shape of the `InnerGrid` is a square (i.e., CH equals CW).
5.  **If** the `InnerGrid` is square: The output grid is identical to the `InnerGrid`.
6.  **Else** (if the `InnerGrid` is rectangular):
    a.  Create a new output grid with dimensions CH (InnerGrid height) by FH (Frame height).
    b.  Define a "Content Column" (`ColC`) as the first column vector of the `InnerGrid`.
    c.  Define a "Modified Column" (`ColM`) by taking `ColC` and replacing its first and last pixel values with the frame's color (F).
    d.  Construct the columns of the output grid by creating a sequence: start with an empty sequence, then append `ColM` followed by `ColC`, repeating this pair `CW` (InnerGrid width) times. Then, continue appending `ColC` to the sequence until the total number of columns in the sequence equals `FH` (Frame height).
    e.  Assemble the final output grid using the generated sequence of columns.
