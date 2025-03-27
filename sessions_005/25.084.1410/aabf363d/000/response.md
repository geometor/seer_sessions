Okay, let's analyze the provided examples.

**Perception of Elements**

*   **Input Grids:** Both input grids contain a large, contiguous object of a single color (green in train_1, red in train_2) and a single pixel of a different color located in the bottom-left corner (magenta in train_1, yellow in train_2). The rest of the grid is composed of the background color (white, 0).
*   **Output Grids:** In both output grids, the large object has changed its color to match the color of the single pixel from the input grid. The original single pixel in the bottom-left corner has been replaced by the background color (white, 0).
*   **Transformation:** The core transformation appears to be a "recoloring" operation. The color of the large object is determined by the color of a single, isolated pixel elsewhere in the grid. This isolated pixel is then effectively removed or "used up" in the process, reverting to the background color.

**Facts**


```yaml
task_name: recolor_object_by_indicator_pixel
examples:
  - id: train_1
    input:
      grid_size: [7, 7]
      objects:
        - object_id: 1
          color: 3 # green
          pixels: [[1, 3], [2, 2], [2, 3], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [4, 1], [4, 2], [5, 2], [5, 3]]
          property: contiguous, largest_non_background
        - object_id: 2
          color: 6 # magenta
          pixels: [[6, 0]]
          property: single_pixel, indicator_color
      background_color: 0 # white
    output:
      grid_size: [7, 7]
      objects:
        - object_id: 1
          color: 6 # magenta
          pixels: [[1, 3], [2, 2], [2, 3], [2, 4], [3, 1], [3, 2], [3, 3], [3, 4], [4, 1], [4, 2], [5, 2], [5, 3]]
          property: contiguous, largest_non_background
      background_color: 0 # white
      changes:
        - action: recolor
          target: object_id 1
          from_color: 3 # green
          to_color: 6 # magenta (derived from input object_id 2)
        - action: change_color
          target_pixel: [6, 0]
          from_color: 6 # magenta
          to_color: 0 # white
  - id: train_2
    input:
      grid_size: [7, 7]
      objects:
        - object_id: 1
          color: 2 # red
          pixels: [[1, 1], [1, 2], [1, 3], [2, 2], [3, 1], [3, 2], [3, 3], [3, 4], [4, 2], [4, 3], [4, 4], [5, 3]]
          property: contiguous, largest_non_background
        - object_id: 2
          color: 4 # yellow
          pixels: [[6, 0]]
          property: single_pixel, indicator_color
      background_color: 0 # white
    output:
      grid_size: [7, 7]
      objects:
        - object_id: 1
          color: 4 # yellow
          pixels: [[1, 1], [1, 2], [1, 3], [2, 2], [3, 1], [3, 2], [3, 3], [3, 4], [4, 2], [4, 3], [4, 4], [5, 3]]
          property: contiguous, largest_non_background
      background_color: 0 # white
      changes:
        - action: recolor
          target: object_id 1
          from_color: 2 # red
          to_color: 4 # yellow (derived from input object_id 2)
        - action: change_color
          target_pixel: [6, 0]
          from_color: 4 # yellow
          to_color: 0 # white

general_observations:
  - The input grid contains one large contiguous object and one single 'indicator' pixel of a different color.
  - The output grid shows the large object recolored using the indicator pixel's color.
  - The indicator pixel's location becomes the background color in the output.
  - The background color remains unchanged otherwise.
  - The indicator pixel appears exactly once in the input grid.
```


**Natural Language Program**

1.  Identify the background color (typically white, 0).
2.  Identify all contiguous objects in the input grid that are not the background color.
3.  Determine the largest contiguous object. Let its color be `original_color`.
4.  Scan the input grid to find a pixel whose color appears exactly once in the entire grid. Let this color be `indicator_color` and its location be `indicator_location`.
5.  Create the output grid as a copy of the input grid.
6.  Iterate through each pixel of the output grid. If a pixel's color matches `original_color`, change its color to `indicator_color`.
7.  Set the pixel at `indicator_location` in the output grid to the background color.