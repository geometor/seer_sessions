## Perception

The input and output are 1-dimensional grids (or single rows).
The input grid contains segments of orange (7) pixels separated by white (0) pixels.
The output grid retains the white (0) pixels in their original positions.
The segments of orange (7) pixels in the input are transformed into segments of either gray (5) or green (3) pixels in the output.
The length and position of these transformed segments correspond exactly to the original orange segments.
By comparing the examples, it appears the color transformation depends on the *length* of the contiguous orange segment:
- If an orange segment has a length greater than 3, it becomes gray (5).
- If an orange segment has a length less than or equal to 3, it becomes green (3).

## Facts


```yaml
task_context:
  grid_type: 1D array (1xN)
  input_colors_present: [white (0), orange (7)]
  output_colors_present: [white (0), green (3), gray (5)]
  background_color: white (0)

objects:
  - object: orange_segment
    description: A contiguous sequence of one or more orange (7) pixels.
    properties:
      - length: The number of pixels in the segment.
      - position: The start and end indices of the segment in the grid.
    relationships:
      - separated_by: White (0) pixels.

actions:
  - action: recolor_segment
    description: Change the color of all pixels within an orange segment based on its properties.
    conditions:
      - property: length of orange_segment
        comparison: greater than 3
        result_color: gray (5)
      - property: length of orange_segment
        comparison: less than or equal to 3
        result_color: green (3)
    target: orange_segment
    preserves:
      - length of the segment
      - position of the segment

transformations:
  - description: Iterate through the input grid to identify contiguous segments of orange (7) pixels.
  - description: For each identified orange segment, determine its length.
  - description: If the length is greater than 3, replace all orange (7) pixels in that segment with gray (5) pixels in the output grid.
  - description: If the length is less than or equal to 3, replace all orange (7) pixels in that segment with green (3) pixels in the output grid.
  - description: Copy all white (0) pixels from the input to the output grid in their original positions.
```


## Natural Language Program

1.  Initialize an output grid of the same dimensions as the input grid, filled with the background color (white - 0).
2.  Iterate through the input grid from left to right.
3.  If an orange (7) pixel is encountered that hasn't been processed as part of a segment yet:
    a.  Identify the full contiguous segment of orange (7) pixels starting from this position.
    b.  Calculate the length of this orange segment.
    c.  Determine the target color based on the length:
        i.  If the length is greater than 3, the target color is gray (5).
        ii. If the length is less than or equal to 3, the target color is green (3).
    d.  Fill the corresponding positions in the output grid with the determined target color for the entire length of the segment.
    e.  Mark the processed pixels of the segment to avoid reprocessing.
4.  If a white (0) pixel is encountered, copy it directly to the corresponding position in the output grid (this is handled by the initialization and selective updating of orange segments).
5.  Return the completed output grid.