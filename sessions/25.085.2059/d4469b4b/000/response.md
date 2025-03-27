*   **Perception**:
    *   Input grids are 5x5.
    *   Output grids are 3x3.
    *   Input grids contain a background color (white - 0) and exactly one other foreground color (blue - 1, red - 2, or green - 3).
    *   The specific arrangement of the foreground color pixels within the input grid varies but does not seem to influence the output pattern directly, only the *identity* of the foreground color matters.
    *   Output grids contain a background color (white - 0) and a foreground color (gray - 5).
    *   The pattern formed by the gray pixels in the output grid is determined solely by which foreground color was present in the input grid. There's a fixed mapping between the input foreground color and the output 3x3 pattern.

*   **Facts**:
    
```yaml
    task_context:
      grid_size_input: [5, 5]
      grid_size_output: [3, 3]
      input_colors:
        - background: white (0)
        - foreground: [blue (1), red (2), green (3)] # Exactly one present per input
      output_colors:
        - background: white (0)
        - foreground: gray (5)

    transformation:
      rule_type: color_mapping_to_pattern
      input_feature: Unique non-white color in the input grid.
      output_generation: Generate a fixed 3x3 pattern based on the identified input color.

    color_to_pattern_mapping:
      blue (1):
        pattern_name: plus_sign
        grid:
          - [0, 5, 0]
          - [5, 5, 5]
          - [0, 5, 0]
      red (2):
        pattern_name: T_shape
        grid:
          - [5, 5, 5]
          - [0, 5, 0]
          - [0, 5, 0]
      green (3):
        pattern_name: L_shape
        grid:
          - [0, 0, 5]
          - [0, 0, 5]
          - [5, 5, 5]
    ```


*   **Natural Language Program**:
    1.  Identify the unique non-white color present in the 5x5 input grid.
    2.  If the identified color is blue (1), create a 3x3 output grid representing a plus sign shape using gray (5) pixels on a white (0) background: `[[0, 5, 0], [5, 5, 5], [0, 5, 0]]`.
    3.  If the identified color is red (2), create a 3x3 output grid representing a 'T' shape using gray (5) pixels on a white (0) background: `[[5, 5, 5], [0, 5, 0], [0, 5, 0]]`.
    4.  If the identified color is green (3), create a 3x3 output grid representing an 'L' shape using gray (5) pixels on a white (0) background: `[[0, 0, 5], [0, 0, 5], [5, 5, 5]]`.
    5.  Return the generated 3x3 grid.