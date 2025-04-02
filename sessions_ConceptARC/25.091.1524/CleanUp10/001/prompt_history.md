
## train_1

**input:**
```
2 2 0 2 0 0
0 0 2 2 2 0
2 2 2 2 2 2
2 2 0 2 0 2
2 0 0 2 2 0
0 0 0 2 0 0
```


**output:**
```
0 0 0 2 0 0
0 0 0 2 0 0
2 2 2 2 2 2
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


## train_2

**input:**
```
0 0 2 0 2 0
0 2 0 0 2 0
0 0 2 2 2 2
2 2 0 0 2 2
2 2 2 2 2 2
0 2 0 0 2 0
```


**output:**
```
0 0 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
2 2 2 2 2 2
0 0 0 0 2 0
```

Okay, analyzing the provided examples.

## Perception

1.  **Grid Structure**: Both input and output are 2D grids of the same dimensions (6x6 in these examples).
2.  **Colors**: Only two colors are present: white (0) and red (2). White appears to be the background color.
3.  **Input Features**: The input grids contain scattered red pixels, potentially forming larger shapes or lines. Notably, some inputs contain complete horizontal or vertical lines made entirely of red pixels, spanning the full width or height of the grid.
4.  **Output Features**: The output grids are much sparser than the inputs. They only contain red pixels where the input grid had a complete horizontal line of red pixels or a complete vertical line of red pixels. All other pixels are white.
5.  **Transformation**: The transformation identifies complete horizontal and vertical lines of red pixels in the input. These lines are preserved in their original positions in the output grid. All other red pixels from the input are changed to white in the output. The output is essentially the union of the complete horizontal and vertical red lines found in the input, overlaid on a white background.

## YAML Facts


```yaml
task_context:
  grid_properties:
    - dimensions: Input and output grids have the same height and width.
    - value_range: Pixels values are integers 0 (white) and 2 (red).
  background_color: White (0) seems to be the default or background color.
objects:
  - object_type: pixel
    properties:
      - color: white (0) or red (2)
  - object_type: line
    properties:
      - color: red (2)
      - orientation: horizontal or vertical
      - completeness: A line is 'complete' if it spans the entire width (horizontal) or height (vertical) of the grid without interruption (i.e., all pixels in the line are red).
relationships:
  - relationship_type: composition
    description: Lines are composed of contiguous red pixels.
actions:
  - action: identify
    target: complete horizontal red lines in the input grid.
  - action: identify
    target: complete vertical red lines in the input grid.
  - action: create
    target: output grid, initialized with all white pixels, matching input dimensions.
  - action: transfer
    source: identified complete horizontal red lines from input
    destination: corresponding rows in the output grid.
  - action: transfer
    source: identified complete vertical red lines from input
    destination: corresponding columns in the output grid.
  - action: ignore/remove
    target: any red pixel in the input that is not part of a complete horizontal or vertical line. These become white in the output.
transformation_goal: Preserve only the complete horizontal and vertical red lines from the input grid onto an otherwise white output grid of the same size.
```


## Natural Language Program

1.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with white pixels (0).
2.  Iterate through each row of the input grid.
3.  For each row, check if all pixels in that row are red (2).
4.  If a row consists entirely of red pixels, change all pixels in the corresponding row of the *output* grid to red (2).
5.  Iterate through each column of the input grid.
6.  For each column, check if all pixels in that column are red (2).
7.  If a column consists entirely of red pixels, change all pixels in the corresponding column of the *output* grid to red (2).
8.  The final output grid contains only the complete horizontal and vertical red lines identified from the input, overlaid on the white background.
