*   **Perception:** The input grids contain various shapes composed of different colors. The output grids are always square and smaller than the input grids. The output grids exhibit a distinct pattern of concentric square frames of solid colors, surrounding a central pixel. The specific colors used in the output frames correspond to colors found adjacent to each other in a nested or layered manner within the input grid. The size of the output grid appears directly related to the number of distinct colors forming these nested layers.

*   **YAML Facts:**
    
```yaml
    task_description: Create a square grid representing the nested structure of colors found in the input.
    
    input_features:
      - grid: 2D array of pixels (colors 0-9).
      - objects: Contiguous blocks of non-background colors.
      - background_color: 0 (white).
      - relationships: Spatial adjacency and nesting/enclosure between different colored objects.
    
    output_features:
      - grid: Square 2D array.
      - structure: Concentric square frames of solid colors.
      - center: A single pixel of the innermost color.
      - size_determinant: Number of colors in the nested sequence found in the input.
    
    transformation_steps:
      - identify_nested_colors: Find the sequence of non-background colors (C1, C2, ..., CK) in the input that are spatially nested or layered, from outermost (C1) to innermost (CK).
      - count_layers: Determine the number of nested colors (N = K).
      - calculate_output_size: Output grid dimension is `Size = 2 * N - 1`.
      - create_output_grid: Initialize a `Size x Size` grid.
      - fill_grid_concentrically:
          - Set the center pixel `(floor(Size/2), floor(Size/2))` to color CK.
          - Fill the 1-pixel thick frame surrounding the center (forming a 3x3 area) with color C(K-1).
          - Fill the next frame outwards (forming a 5x5 area) with color C(K-2).
          - Continue until the outermost frame (border of the Size x Size grid) is filled with color C1.
    
    examples_analysis:
      - train_1:
          - nested_sequence: Gray(5) -> Red(2) -> Green(3) -> Blue(1) -> Orange(7)
          - N: 5
          - output_size: 9x9
          - center_color: Orange(7)
      - train_2:
          - nested_sequence: Azure(8) -> Blue(1) -> Yellow(4) -> Red(2) -> Green(3)
          - N: 5
          - output_size: 9x9
          - center_color: Green(3)
      - train_3:
          - nested_sequence: Red(2) -> Yellow(4) -> Green(3) -> Maroon(9) -> Orange(7) -> Gray(5)
          - N: 6
          - output_size: 11x11
          - center_color: Gray(5)
    ```


*   **Natural Language Program:**
    1.  Identify the sequence of non-background colors in the input grid that exhibit a nested spatial relationship, ordered from the outermost color layer (`C1`) to the innermost color layer (`CK`).
    2.  Count the number of colors (`N`) in this identified sequence.
    3.  Determine the size (`Size`) of the square output grid using the formula: `Size = (2 * N) - 1`.
    4.  Create a new square grid of dimensions `Size x Size`.
    5.  Fill the output grid by drawing concentric square frames, starting from the center and working outwards:
        a.  Set the color of the central pixel `(floor(Size/2), floor(Size/2))` to the innermost color `CK`.
        b.  For each layer `L` from 1 to `N-1`:
            i.  Determine the color for this layer: `Color = C(K-L)`.
            ii. Identify the square frame at distance `L` from the center (i.e., the pixels forming the border of a `(2*L + 1) x (2*L + 1)` square centered in the grid).
            iii. Fill all pixels within this frame with `Color`.