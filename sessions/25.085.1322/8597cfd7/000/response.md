**Perception**

1.  **Input Grid Structure:** The input grids vary in size but always contain a single, solid horizontal line of gray pixels (color 5) that spans the entire width. The background is white (color 0).
2.  **Key Colors:** Red (color 2) and Yellow (color 4) pixels are present in the input grids, appearing both above and below the gray line. They often form small clusters or vertical line segments.
3.  **Output Grid Structure:** The output grid is consistently a 2x2 grid.
4.  **Output Color:** The output 2x2 grid is filled entirely with a single color, either Red (2) or Yellow (4).
5.  **Transformation Goal:** The task is to determine which color (Red or Yellow) should fill the output grid based on the arrangement and quantity of Red and Yellow pixels in the input grid.
6.  **Initial Hypothesis & Refinement:**
    *   Comparing total counts of Red vs. Yellow directly doesn't work (Ex 1, 2 fail).
    *   Comparing counts only above or only below the gray line doesn't work consistently.
    *   Comparing the sizes of the largest objects of each color doesn't work (Ex 1 fails).
    *   Comparing the number of rows containing each color below the gray line doesn't work (Ex 1 fails).
    *   The gray line seems potentially irrelevant to the core comparison logic, possibly acting as a visual separator or distractor.
7.  **Successful Hypothesis:** A rule comparing the total count of Yellow pixels to *twice* the total count of Red pixels successfully explains all examples: Yellow wins only if its count is at least double the Red count; otherwise, Red wins.

**Facts**


```yaml
elements:
  - item: input_grid
    properties:
      - type: 2D array of integers (0-9)
      - variable height and width (within 1x1 to 30x30)
      - contains pixels of white (0), red (2), yellow (4), gray (5)
      - always includes a single solid horizontal gray line
  - item: output_grid
    properties:
      - type: 2D array of integers (0-9)
      - fixed size: 2x2
      - contains pixels of a single color: either red (2) or yellow (4)
objects:
  - object: red_pixels
    properties:
      - color_value: 2
      - location: scattered in input_grid, both above and below the gray line
  - object: yellow_pixels
    properties:
      - color_value: 4
      - location: scattered in input_grid, both above and below the gray line
  - object: gray_line
    properties:
      - color_value: 5
      - shape: horizontal line spanning the width of the input_grid
      - location: separates the grid vertically
relationships:
  - relationship: count_comparison
    description: The core logic compares the total count of yellow pixels to twice the total count of red pixels.
actions:
  - action: count_pixels
    actor: system
    inputs:
      - input_grid
      - target_color (red=2 or yellow=4)
    outputs:
      - total count of the target color pixels
  - action: compare_counts
    actor: system
    inputs:
      - red_count
      - yellow_count
    outputs:
      - decision_color (red=2 or yellow=4)
    logic: If yellow_count >= 2 * red_count, decision_color is yellow, otherwise it is red.
  - action: generate_output
    actor: system
    inputs:
      - decision_color
    outputs:
      - output_grid (2x2 grid filled with decision_color)

```


**Natural Language Program**

1.  Scan the entire input grid and count the total number of red (2) pixels (`CountR`).
2.  Scan the entire input grid and count the total number of yellow (4) pixels (`CountY`).
3.  Compare `CountY` with `CountR * 2`.
4.  If `CountY` is greater than or equal to (`>=`) `CountR * 2`, then determine the output color is yellow (4).
5.  Otherwise (if `CountY` is less than `<` `CountR * 2`), determine the output color is red (2).
6.  Construct the output grid as a 2x2 grid filled entirely with the determined output color.