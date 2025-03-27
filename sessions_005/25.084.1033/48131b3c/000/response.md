## Perception
The input is a grid of pixels of varying dimensions. The output is always a grid with double the height and double the width of the input grid. The content of the output grid is formed by repeating the input grid in a 2x2 pattern. Essentially, the input grid is tiled twice horizontally and twice vertically to create the output.

## Facts


```yaml
task_description: Tile the input grid in a 2x2 arrangement to create the output grid.
grid_properties:
  - name: input_grid
    attributes:
      - height: H
      - width: W
  - name: output_grid
    attributes:
      - height: 2 * H
      - width: 2 * W
      - content: A 2x2 tiling of the input_grid.
transformation:
  - type: tiling
    source: input_grid
    target: output_grid
    repetition:
      - axis: horizontal
        count: 2
      - axis: vertical
        count: 2
relationship:
  - The output grid's dimensions are exactly double the input grid's dimensions.
  - The pattern in the input grid is repeated four times in the output grid, arranged in a 2x2 layout.
```


## Natural Language Program

1.  Determine the height (H) and width (W) of the input grid.
2.  Create a new output grid with height 2*H and width 2*W.
3.  Copy the input grid into the top-left quadrant of the output grid (rows 0 to H-1, columns 0 to W-1).
4.  Copy the input grid into the top-right quadrant of the output grid (rows 0 to H-1, columns W to 2*W-1).
5.  Copy the input grid into the bottom-left quadrant of the output grid (rows H to 2*H-1, columns 0 to W-1).
6.  Copy the input grid into the bottom-right quadrant of the output grid (rows H to 2*H-1, columns W to 2*W-1).
7.  Return the output grid.