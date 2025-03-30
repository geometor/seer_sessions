*   **Perception:**
    *   The input grids consist of a dominant background color and several distinct contiguous objects composed of other colors.
    *   These objects have varying shapes, sizes (pixel count), and bounding box dimensions.
    *   The output grid is always a rectangular subgrid extracted directly from the input grid.
    *   The output grid corresponds to the minimal bounding box of one specific object present in the input grid.
    *   The colors within the output grid are preserved exactly as they were in the corresponding section of the input grid. This means the output contains the selected object's pixels and potentially some background pixels that fall within the object's bounding box.

*   **Facts:**
    
```yaml
    task_elements:
      - Input Grid: Contains pixels of various colors (0-9).
      - Background Color: The color that appears most frequently in the input grid.
      - Objects: Contiguous regions of non-background-colored pixels. Each object has properties:
          - color: The color of the object's pixels.
          - shape: The spatial arrangement of the object's pixels.
          - pixel_area: The total number of pixels belonging to the object.
          - bounding_box: The smallest rectangle enclosing the object.
          - bounding_box_area: The area of the bounding box (height * width).
      - Output Grid: A rectangular subgrid of the input grid.

    transformation_logic:
      - identification:
          - Determine the background color (most frequent color in the input).
          - Identify all distinct contiguous objects composed of non-background colors.
          - For each object, calculate its pixel_area and bounding_box_area.
      - selection:
          - Apply a priority-based rule to select one target object:
            1. Select the object with the unique smallest pixel_area.
            2. If no unique smallest area object exists, select the object with the unique largest pixel_area.
            3. If there is a tie for the largest pixel_area, select the object among the tied ones that has the smallest bounding_box_area.
      - extraction:
          - Determine the minimal bounding box coordinates (top_row, left_col, bottom_row, right_col) of the selected target object.
          - Extract the subgrid from the input grid defined by these bounding box coordinates.
      - output_generation:
          - The extracted subgrid is the final output grid.

    examples_verification:
      - Example 1: BG=Red(2). Objects: E(Area=11, BBox=15), +(Area=5, BBox=15), squares(Area=4, BBox=8). Unique smallest area = squares(4). Unique largest area = E(11). Rule selects largest area object (E). Output is E's bounding box. Matches.
      - Example 2: BG=Azure(8). Objects: +(Area=7, BBox=15), H(Area=11, BBox=15), L(Area=11, BBox=25). Smallest area = +(7). Largest area = H(11), L(11) (tie). Rule proceeds to tie-breaker for largest area: H BBox=15, L BBox=25. Select smallest BBox (H). Output is H's bounding box. Matches.
      - Example 3: BG=Blue(1). Objects: H(Area=12, BBox=20), squares(Area=14, BBox=18), Green3(Area=9, BBox=15). Unique smallest area = Green3(9). Rule selects smallest area object (Green3). Output is Green3's bounding box. Matches.
      - Example 4: BG=Blue(1). Objects: Green3(Area=15, BBox=15), Red5(Area=17, BBox=25), Checker(Area=16, BBox=32). Unique smallest area = Green3(15). Unique largest area = Red5(17). Rule selects largest area object (Red5). Output is Red5's bounding box. Matches.
    ```


*   **Natural Language Program:**
    1.  Identify the background color, which is the most common pixel color in the input grid.
    2.  Find all separate, contiguous objects in the input grid that are not the background color.
    3.  For each object found, calculate two properties: its total number of pixels (pixel area) and the area of its minimal bounding box (height times width).
    4.  Select the target object based on the following criteria, checked in order:
        a.  If there is exactly one object with the smallest pixel area compared to all other objects, select that object.
        b.  Otherwise, if there is exactly one object with the largest pixel area compared to all other objects, select that object.
        c.  Otherwise (meaning there is a tie for the largest pixel area), compare the objects that are tied for the largest pixel area. Select the object among these tied objects that has the smallest bounding box area.
    5.  Determine the coordinates (top row, bottom row, left column, right column) of the minimal bounding box surrounding the selected target object.
    6.  Extract the rectangular portion of the input grid defined by these bounding box coordinates.
    7.  This extracted subgrid is the output.