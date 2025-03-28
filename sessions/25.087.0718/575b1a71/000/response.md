**Perception:**

1.  **Input/Output Grids:** All examples consist of a 10x10 grid.
2.  **Background Color:** The predominant color in both input and output is gray (5). This color appears unchanged between input and output.
3.  **Target Pixels:** The input grids contain scattered white (0) pixels.
4.  **Transformation:** In the output grids, the white (0) pixels are replaced by other colors: blue (1), red (2), green (3), or yellow (4).
5.  **Positional Dependency:** The color assigned to replace a white pixel depends on the column it resides in. Specifically, it relates to the *order* of columns containing white pixels.
6.  **Columnar Coloring:** All white pixels within the same column are replaced by the same color.
7.  **Color Sequence:** The columns containing white pixels are identified. These columns, when sorted by their index (left-to-right), are assigned colors sequentially: the first column gets blue (1), the second gets red (2), the third gets green (3), and the fourth gets yellow (4). This pattern suggests a mapping based on the ordinal position of the column among those containing white pixels.

**Facts:**


```yaml
grid_dimensions:
  - input_height: 10
    input_width: 10
    output_height: 10
    output_width: 10
pixels:
  - background:
      color: gray (5)
      behavior: remains unchanged
  - target:
      color: white (0)
      behavior: replaced by a new color based on column position
  - replacement_colors:
      - blue (1)
      - red (2)
      - green (3)
      - yellow (4)
transformation:
  - type: pixel_replacement
  - scope: affects only white (0) pixels
  - logic: based on column index and order
relationships:
  - all white pixels in the same column receive the same replacement color.
  - the specific replacement color depends on the sorted order of columns containing white pixels.
rule_details:
  - identify all columns containing at least one white (0) pixel.
  - sort the indices of these columns in ascending order.
  - map the first sorted column index to blue (1).
  - map the second sorted column index to red (2).
  - map the third sorted column index to green (3).
  - map the fourth sorted column index to yellow (4).
  - replace each white (0) pixel with the color mapped to its column index.
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all unique column indices that contain at least one white (0) pixel in the input grid.
3.  Sort these unique column indices in ascending order.
4.  Define the sequence of replacement colors: blue (1), red (2), green (3), yellow (4).
5.  Create a mapping: associate the first column index from the sorted list with the first color (blue), the second column index with the second color (red), the third with green, and the fourth with yellow.
6.  Iterate through each cell (pixel) of the input grid.
7.  If a cell contains a white (0) pixel:
    a.  Determine its column index.
    b.  Find the replacement color associated with this column index using the mapping created in step 5.
    c.  Update the corresponding cell in the output grid with this replacement color.
8.  Return the modified output grid.