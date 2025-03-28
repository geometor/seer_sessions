## Perception

1.  **Input Grid Structure:** The input grids vary in size but consistently contain scattered pixels of red (2) and yellow (4) on a white (0) background. There is always a single horizontal line composed entirely of gray (5) pixels.
2.  **Output Grid Structure:** The output grids are consistently 2x2 in size.
3.  **Color Transformation:** The output grid is always filled with a single uniform color, which is either red (2) or yellow (4).
4.  **Core Logic:** The color chosen for the output grid appears to depend on the relative frequency of red (2) and yellow (4) pixels in the input grid.
5.  **Counting:** By counting the occurrences of red and yellow pixels in each input example:
    *   `train_1`: Red=2, Yellow=6. Output is Yellow. (Yellow > Red)
    *   `train_2`: Red=5, Yellow=4. Output is Red. (Red > Yellow)
    *   `train_3`: Red=5, Yellow=5. Output is Red. (Red == Yellow)
    *   `train_4`: Red=5, Yellow=3. Output is Red. (Red > Yellow)
6.  **Rule Inference:** The output color is determined by which color, red or yellow, appears more often in the input. In case of a tie, red is chosen. The gray line and white background pixels seem irrelevant to determining the output color.

## Facts


```yaml
task_elements:
  - name: input_grid
    description: A 2D grid of pixels with varying dimensions.
    contains:
      - object: red_pixels
        color: 2 (red)
        count: Variable across examples.
      - object: yellow_pixels
        color: 4 (yellow)
        count: Variable across examples.
      - object: gray_line
        color: 5 (gray)
        structure: A single complete horizontal line.
        relevance: Appears irrelevant to the output color determination.
      - object: background_pixels
        color: 0 (white)
        relevance: Appears irrelevant.
  - name: output_grid
    description: A 2D grid of pixels, always 2x2 in size.
    properties:
      - size: 2x2
      - content: Filled entirely with a single color (either red or yellow).

transformation:
  - action: count_pixels
    input: input_grid
    parameters:
      - color_to_count: 2 (red)
      - color_to_count: 4 (yellow)
    output:
      - name: red_count
      - name: yellow_count
  - action: compare_counts
    input:
      - red_count
      - yellow_count
    logic: Determine which count is greater or if they are equal.
    output:
      - name: dominant_color
        value: |
          if red_count >= yellow_count, dominant_color is 2 (red).
          if yellow_count > red_count, dominant_color is 4 (yellow).
  - action: construct_output
    input: dominant_color
    result: Create a 2x2 grid filled entirely with the dominant_color.

```


## Natural Language Program

1.  Examine the input grid and count the total number of red (2) pixels.
2.  Examine the input grid and count the total number of yellow (4) pixels.
3.  Compare the count of red pixels to the count of yellow pixels.
4.  If the count of red pixels is greater than or equal to the count of yellow pixels, determine the output color to be red (2).
5.  Otherwise (if the count of yellow pixels is strictly greater than the count of red pixels), determine the output color to be yellow (4).
6.  Construct the output grid as a 2x2 grid where every pixel has the determined output color.