*   **Perception:**
    *   The input grid contains two main distinct non-white components against a white background.
    *   The first component is a large, contiguous shape made of a single color (e.g., green in train_1, blue in train_2, azure in train_3). This shape varies in form across examples but is always monochromatic.
    *   The second component is a smaller rectangular block composed of various different colors. This block also varies in size (3x3 in train_1/2, 4x4 in train_3).
    *   The output grid corresponds in size and content to the smaller multi-colored block from the input, but with some specific colors replaced by white (0).
    *   The transformation rule appears to involve using the color of the large shape to determine *which* colors within the smaller block should be replaced with white. The specific colors to be replaced depend on the color of the large shape.

*   **Facts:**
    
```yaml
    task_elements:
      - element: background
        color: white (0)
      - element: large_shape
        description: The largest contiguous block of non-white pixels.
        properties:
          - single_color: True
          - color_value: C (varies per example, e.g., 3, 1, 8)
          - shape: Variable, seems irrelevant to the transformation.
          - location: Variable, seems irrelevant to the transformation.
      - element: color_palette
        description: A relatively small rectangular block containing multiple different non-white colors. It is the smallest bounding box containing all non-white pixels *not* part of the large_shape.
        properties:
          - colors: Multiple, variable.
          - dimensions: Variable (e.g., 3x3, 4x4).
          - location: Variable.
      - element: output_grid
        description: The result of the transformation.
        properties:
          - dimensions: Same as the color_palette block.
          - content: Derived from the color_palette block.

    transformation:
      action: Color Filtering
      input_elements: [large_shape, color_palette]
      output_elements: [output_grid]
      rule:
        - Identify the single color C of the large_shape.
        - Identify the color_palette block B.
        - Determine a set of 'target colors' (T) based on the value of C. This mapping seems fixed but arbitrary based on the examples:
            - If C=3 (green), T={1 (blue), 8 (azure), 9 (maroon)}.
            - If C=1 (blue), T={1 (blue), 2 (red), 4 (yellow), 9 (maroon)}.
            - If C=8 (azure), T={1 (blue), 3 (green), 5 (gray), 7 (orange)}.
        - Create the output_grid O with the same dimensions as B.
        - For each pixel at position (row, col) in B:
            - If the color of B[row, col] is present in the target set T, set O[row, col] to white (0).
            - Otherwise, copy the color from B[row, col] to O[row, col].
    ```


*   **Natural Language Program:**
    1.  Find the largest contiguous object composed of a single non-white color in the input grid. Let its color be `FilterColor`.
    2.  Identify all other non-white pixels in the input grid. Find the smallest bounding box that encloses all these pixels. Let this be the `SourceBlock`.
    3.  Determine the set of `TargetColors` to be filtered out based on the `FilterColor`:
        *   If `FilterColor` is green (3), the `TargetColors` are {blue (1), azure (8), maroon (9)}.
        *   If `FilterColor` is blue (1), the `TargetColors` are {blue (1), red (2), yellow (4), maroon (9)}.
        *   If `FilterColor` is azure (8), the `TargetColors` are {blue (1), green (3), gray (5), orange (7)}.
        *   (Assume this mapping covers all potential `FilterColor` values encountered).
    4.  Create a new output grid with the same dimensions as the `SourceBlock`.
    5.  Iterate through each cell `(r, c)` of the `SourceBlock`:
        *   Get the color `CurrentColor` at `SourceBlock[r, c]`.
        *   Check if `CurrentColor` is present in the set of `TargetColors`.
        *   If it is present, set the corresponding cell in the output grid to white (0).
        *   If it is not present, set the corresponding cell in the output grid to `CurrentColor`.
    6.  Return the generated output grid.