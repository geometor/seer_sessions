*   **Perception:** The task involves identifying three distinct elements in the input grid: a background color, a single contiguous "pattern" object of a unique color, and multiple single "marker" pixels of another unique color. The transformation uses the locations of the marker pixels as anchors to replicate the pattern object onto the output grid. The original pattern and marker pixels are effectively replaced by the stamped copies. The background color persists in the output where no pattern is stamped.

*   **YAML Facts:**
    
```yaml
    task_type: pattern_stamping
    background_color: most_frequent_color_in_input
    elements:
      - role: pattern
        description: A single contiguous object of a unique color (not background, not marker).
        properties:
          - color: unique_color_1
          - shape: specific_shape_per_example (e.g., T, L, custom shape)
          - size: small (typically 3x3 bounding box in examples)
          - count: 1
        actions:
          - identified
          - center_determined
          - used_as_stamp
      - role: markers
        description: Multiple single pixels of another unique color.
        properties:
          - color: unique_color_2
          - shape: 1x1 pixel
          - count: multiple
          - distribution: scattered
        actions:
          - identified
          - locations_recorded
          - used_as_anchor_points_for_stamping
      - role: output_grid
        description: Result of the transformation.
        properties:
          - dimensions: same_as_input
          - background_color: same_as_input
          - content: background_color + stamped_pattern_copies
    relationships:
      - type: stamping
        origin: pattern_object
        target: output_grid
        anchor: marker_locations
        details: The pattern object is copied onto the output grid, centered at each marker location. The pattern pixels overwrite existing pixels (background or original markers) at those locations.
      - type: identification
        based_on: color_frequency_and_contiguity
        elements_identified: background, pattern, markers
    ```


*   **Natural Language Program:**
    1.  Determine the background color by finding the most frequent color in the input grid.
    2.  Identify all unique colors present in the input grid, excluding the background color.
    3.  Group the non-background pixels by color.
    4.  Identify the "marker" color: This is the color associated with pixels that appear as isolated single points (no adjacent pixels of the same color). Record the coordinates of each marker pixel.
    5.  Identify the "pattern" color: This is the remaining non-background, non-marker color.
    6.  Isolate the contiguous object formed by the pattern color pixels. This is the "pattern object".
    7.  Determine the center coordinates of the pattern object (e.g., the central pixel within its bounding box).
    8.  Calculate the relative coordinates of each pixel within the pattern object with respect to its center pixel. Store these relative coordinates along with their corresponding pattern color.
    9.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color.
    10. For each recorded marker coordinate (anchor point):
        a.  For each relative coordinate and color pair derived from the pattern object:
            i.  Calculate the absolute target coordinate in the output grid by adding the marker coordinate (anchor point) to the relative coordinate.
            ii. If the target coordinate is within the bounds of the output grid, set the pixel at the target coordinate to the pattern pixel's color, overwriting the existing background color.
    11. The resulting grid is the final output.