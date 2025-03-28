**Perception:**

The input grids contain multiple small, isolated 3x3 patterns scattered on a white background. Each pattern is characterized by a specific arrangement of a single color against a white background within its 3x3 area. Within a single input grid, all patterns share the *same* structural arrangement but differ in their primary color. The specific pattern structure (e.g., 'hollow cross', 'plus', 'X') can vary between different task examples.

The output grid is constructed by extracting these 3x3 patterns from the input and arranging them adjacent to each other, either vertically or horizontally.

The key steps appear to be:
1.  Identify the non-white objects in the input.
2.  Filter for objects that precisely occupy a 3x3 bounding box. These are the target patterns.
3.  Extract the 3x3 grid for each target pattern.
4.  Determine the overall spatial arrangement of these patterns in the input grid (predominantly vertical or horizontal spread).
5.  Sort the extracted 3x3 patterns based on their original position (top-to-bottom for vertical spread, left-to-right for horizontal spread).
6.  Concatenate the sorted patterns into the output grid (stack vertically or horizontally based on the determined spread).

**YAML Facts:**


```yaml
task_description: Extract all instances of a repeating 3x3 pattern from the input and arrange them vertically or horizontally in the output based on their spatial distribution in the input.

elements:
  - element: background
    color: white
    value: 0
  - element: pattern
    description: A 3x3 shape composed of a single non-white color and white pixels. The specific arrangement within the 3x3 grid is consistent for all patterns within a single input example but can vary between examples.
    properties:
      - size: 3x3
      - composition: single non-white color + white pixels
      - repetition: Multiple instances appear in the input, differing only by color.
  - element: input_grid
    contains:
      - background
      - multiple pattern instances
  - element: output_grid
    description: A grid formed by arranging the extracted pattern instances adjacently.
    properties:
      - composition: Contains only the extracted 3x3 patterns, no background spacing between them.
      - arrangement: Either vertical stacking or horizontal stacking of patterns.

relationships:
  - type: spatial_distribution
    description: The relative positions of the pattern instances in the input grid determine the output arrangement.
    properties:
      - Calculate bounding box enclosing all pattern instances' top-left corners.
      - If bounding_box_height > bounding_box_width, arrangement is vertical.
      - If bounding_box_height <= bounding_box_width, arrangement is horizontal.
  - type: ordering
    description: The order of patterns in the output depends on their input position and the arrangement type.
    properties:
      - If arrangement is vertical, sort patterns by their top-row coordinate (ascending).
      - If arrangement is horizontal, sort patterns by their left-column coordinate (ascending).
  - type: transformation
    action: identify
    source: input_grid
    target: pattern instances
    details: Find all connected components of non-white pixels with a 3x3 bounding box.
  - type: transformation
    action: extract
    source: pattern instances from input_grid
    target: list of 3x3 grids
    details: Record the 3x3 pixel data for each identified pattern instance.
  - type: transformation
    action: assemble
    source: list of 3x3 grids
    target: output_grid
    details: Concatenate the 3x3 grids based on the determined arrangement (vertical/horizontal) and order.

constants:
  - pattern_size: 3x3
```


**Natural Language Program:**

1.  Scan the input grid to identify all distinct connected components (objects) composed of non-white pixels.
2.  For each identified object, determine its bounding box.
3.  Filter these objects, keeping only those whose bounding box dimensions are exactly 3x3. These are the target patterns.
4.  Create a list to store the extracted patterns. For each target pattern, record its full 3x3 pixel grid and the row and column coordinates of its top-left corner in the input grid.
5.  If no target patterns are found, output an empty grid (or handle as per specific requirements, though examples suggest patterns are always present).
6.  Determine the overall spatial arrangement of the target patterns:
    a.  Find the minimum and maximum row indices among the top-left corners of all patterns. Calculate the height of the span: `height = max_row - min_row + 1`.
    b.  Find the minimum and maximum column indices among the top-left corners of all patterns. Calculate the width of the span: `width = max_col - min_col + 1`.
    c.  Compare height and width. If `height > width`, the arrangement is 'vertical'. Otherwise (if `height <= width`), the arrangement is 'horizontal'.
7.  Sort the list of recorded patterns:
    a.  If the arrangement is 'vertical', sort the patterns primarily based on their top-left row coordinate (ascending).
    b.  If the arrangement is 'horizontal', sort the patterns primarily based on their top-left column coordinate (ascending).
8.  Construct the output grid:
    a.  If the arrangement is 'vertical', concatenate the sorted 3x3 pattern grids vertically. The output grid width will be 3, and the height will be `3 * number_of_patterns`.
    b.  If the arrangement is 'horizontal', concatenate the sorted 3x3 pattern grids horizontally. The output grid height will be 3, and the width will be `3 * number_of_patterns`.
9.  Return the constructed output grid.