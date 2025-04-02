*   **Perception**:
    *   Each input grid is clearly divided into two main regions by a single row or column of white (0) pixels.
    *   Each region contains a larger shape, often acting as a background or container, and sometimes smaller shapes or patterns within it.
    *   The relationship and content of the inner patterns/shapes within the two main regions determine the output.
    *   Three distinct output types are observed:
        1.  A single white (0) pixel.
        2.  A pattern of pixels (e.g., blue in train_3) on a white (0) background.
        3.  A rectangular shape with a border of one color and a white (0) interior (train_1).

*   **Facts**:
    
```yaml
    task_structure:
      - item: input_grid
        description: Contains two primary zones separated by a line of white pixels.
        properties:
          separator_type: Can be a horizontal row or a vertical column.
          separator_color: Always white (0).
          zone_count: Always 2.
      - item: zone
        description: A region within the input grid, separated from the other zone by the white line.
        contains:
          - object: outer_shape
            properties:
              - shape: Typically rectangular or near-rectangular.
              - role: Acts as a container or background for the zone.
              - color: Varies (e.g., blue, red, orange, green, maroon, gray).
          - object: inner_content
            properties:
              - type: Can be a single geometric shape (e.g., rectangle) or scattered pixels.
              - color: Varies (e.g., yellow, azure, blue, red).
              - relationship_to_outer_shape: Fully contained within the outer_shape's boundary, distinct from the outer_shape's color.
              - role: The primary element for comparison between the two zones.
    comparison_logic:
      - rule: Comparison focuses on the 'inner_content' of the two zones.
      - criteria:
          - color_of_inner_content
          - shape_and_relative_position_of_inner_content
    output_determination:
      - condition: Inner contents are identical objects (same shape, color, relative position).
        action: Produce a 1x1 output grid with a single white (0) pixel.
        examples: [train_2, train_4]
      - condition: Inner content colors are the same, but the patterns/shapes differ.
        action: Extract the inner pattern from the first zone (top or left). Output this pattern using its original color on a white (0) background, cropped to its minimal bounding box.
        examples: [train_3]
      - condition: Inner content colors are different.
        action: Identify the fill area of the first zone (top or left). Determine its bounding box. Create an output grid of that size. Set the border pixels to the fill color of the first zone. Set the interior pixels to white (0).
        examples: [train_1]

    ```


*   **Natural Language Program**:
    1.  Identify the separator line (a single row or column composed entirely of white pixels) dividing the input grid into two zones (Zone A: top or left, Zone B: bottom or right).
    2.  For each zone, identify the main background/border color and locate the inner content (pixels within the main shape that are not the background/border color). Determine the color and pattern/shape of this inner content. Let `inner_colorA`, `inner_patternA` be for Zone A, and `inner_colorB`, `inner_patternB` for Zone B.
    3.  Compare the inner content of Zone A and Zone B:
        a.  **If** `inner_colorA` is the same as `inner_colorB` **AND** `inner_patternA` represents the exact same geometric shape and relative position as `inner_patternB`: Output a 1x1 grid containing only a white (0) pixel.
        b.  **Else if** `inner_colorA` is the same as `inner_colorB` (but the patterns/shapes differ): Extract the minimal bounding box containing `inner_patternA` from Zone A. Create a new grid of this size. For each pixel within this bounding box in the original Zone A, if it has `inner_colorA`, place `inner_colorA` in the corresponding position in the new grid; otherwise, place white (0). Output the new grid.
        c.  **Else** (`inner_colorA` is different from `inner_colorB`): Determine the fill color of Zone A (`fillA`, the color surrounding `inner_patternA` but inside the zone's border). Find the minimal bounding box of the area covered by `fillA` color. Create a new grid of this size. Fill the border pixels of this new grid with `fillA` color. Fill all interior pixels of the new grid with white (0). Output the new grid.