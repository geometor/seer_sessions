
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 4 4 4 4 8 8 8 8 8 8
8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 6 6 6 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
1
1
1
1
1
3
3
3
3
2
2
2
2
2
4
4
4
4
4
6
6
6
```


## train_2

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 2 2 2 2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 3 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 3 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 3 3 3 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 3 3 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
8
8
8
8
8
8
8
2
2
2
2
2
2
2
2
3
3
3
3
3
3
3
3
3
```

**Perception**

The input is a 2D grid of pixels with various colors. There appears to be a dominant background color, which is the color found at the top-left corner (0,0) of the input grid. Scattered across this background are several objects or collections of pixels of different colors.

The output is always a single column (Nx1 grid) containing a sequence of colors.

The transformation involves identifying the background color from the input grid's top-left pixel. Then, the input grid is scanned row by row, from top to bottom, and within each row, from left to right. Every pixel encountered that is *not* the background color is collected in the order it was scanned. Finally, these collected pixel colors are arranged sequentially into a single vertical column to form the output grid. The height of the output column corresponds exactly to the total count of non-background pixels in the input grid.

**Facts**

```yaml
task_description: Filter out background pixels and flatten the remaining pixels into a column vector based on scan order.
elements:
  - name: input_grid
    type: 2D array of integers (pixels)
    properties:
      - Contains a background color.
      - Contains foreground pixels (colors different from the background).
      - Size varies per example.
  - name: output_grid
    type: 2D array of integers (pixels)
    properties:
      - Always has a width of 1 (column vector).
      - Height equals the total count of foreground pixels in the input grid.
      - Contains only the foreground colors from the input grid.
  - name: background_color
    type: integer (pixel value)
    determination: The color of the pixel at the top-left corner (index [0][0]) of the input grid.
  - name: foreground_pixels
    type: list of integers (pixel values)
    determination: All pixels in the input grid whose color does not match the background_color.
relationships:
  - The sequence of pixels in the output_grid corresponds directly to the order in which foreground_pixels are encountered when scanning the input_grid row by row, left to right.
actions:
  - Identify the background_color from input_grid[0][0].
  - Scan the input_grid row by row (top to bottom), and within each row, column by column (left to right).
  - Filter out pixels matching the background_color.
  - Collect the remaining foreground_pixels in the scan order.
  - Reshape the collected list of foreground_pixels into a single column to form the output_grid.
```


**Natural Language Program**

1.  Determine the background color by taking the color value of the pixel at the top-left corner (row 0, column 0) of the input grid.
2.  Initialize an empty list to store the foreground pixel colors.
3.  Iterate through each row of the input grid, starting from the top row (row 0) and proceeding downwards.
4.  Within each row, iterate through each column, starting from the left column (column 0) and proceeding rightwards.
5.  For each pixel encountered during the iteration:
    a.  Compare the pixel's color value to the determined background color.
    b.  If the pixel's color is *different* from the background color, append its color value to the list of foreground pixel colors.
6.  After iterating through all pixels in the input grid, construct the output grid. The output grid will have 1 column and a number of rows equal to the total number of colors collected in the foreground pixel colors list.
7.  Populate the output grid column sequentially with the colors from the collected list, maintaining the order in which they were added.
