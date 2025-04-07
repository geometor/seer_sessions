**Perception:**

The input grids are relatively large and contain a dominant background color (green, blue, or azure across the examples). Scattered within this background are various small objects composed of different colors. A key feature in each input grid is a distinct rectangular region composed entirely of white (0) pixels. This white rectangle also contains some non-white pixels within its boundaries.

The output grids are significantly smaller than the input grids. Their background color is consistently white (0). The non-white pixels present in the output grids correspond exactly in color and relative position to the non-white pixels found within the white rectangular region of the input grid. The dimensions of the output grid precisely match the dimensions of the white rectangular region identified in the input.

The core transformation appears to be locating this unique white rectangular subgrid within the larger input grid and extracting it directly to form the output. The surrounding background color and any objects outside this white rectangle in the input are ignored.

**Facts:**


```yaml
task_description: Identify and extract the largest contiguous rectangular area composed of white pixels from the input grid.
grid_properties:
  - input_grid_size: Variable (e.g., 20x22, 23x23, 21x20)
  - output_grid_size: Variable, determined by the size of the identified white rectangle (e.g., 7x7, 7x12, 5x5)
  - dominant_input_background_color: Varies (green, blue, azure), appears irrelevant to the output.
  - output_background_color: Consistently white (0).
objects:
  - type: Contiguous Rectangular Area
    properties:
      - color: white (0)
      - role: Defines the boundaries of the output grid.
      - location: Varies within the input grid.
      - key_feature: Appears to be the largest such rectangle by area in each input.
  - type: Pixels
    properties:
      - color: Various non-white colors (e.g., red, yellow, azure, blue, green)
      - location: Some are scattered outside the white rectangle (ignored), others are located *inside* the white rectangle (preserved).
      - role: Pixels inside the white rectangle are copied to the output grid in their relative positions.
transformation:
  - action: Find all contiguous rectangular regions composed entirely of white (0) pixels in the input grid.
  - action: Select the rectangular region with the largest area (width * height).
  - action: Extract the subgrid defined by the boundaries of the selected white rectangle.
  - result: The extracted subgrid becomes the output grid.
relationships:
  - The output grid is a subgrid of the input grid.
  - The dimensions of the output grid are identical to the dimensions of the largest white (0) rectangular area found in the input.
  - The content of the output grid (including non-white pixels) is identical to the content within the boundaries of the largest white (0) rectangular area in the input.
```


**Natural Language Program:**

1.  Scan the input grid to locate all contiguous rectangular areas where every pixel within the rectangle's boundary is white (color 0).
2.  Calculate the area (width multiplied by height) for each identified white rectangle.
3.  Identify the white rectangle with the maximum area. (Assume there will be only one such rectangle with the maximum area based on the examples).
4.  Determine the top-left corner coordinates (row, column) and the dimensions (height, width) of this largest white rectangle.
5.  Create a new grid with the determined height and width.
6.  Copy the content (all pixel values, including any non-white ones) from the identified rectangular region of the input grid (starting at its top-left corner and spanning its height and width) into the newly created output grid.
7.  The resulting grid is the final output.