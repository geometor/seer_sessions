## Perception
The input grids are always 6x6 and contain a white background (color 0) and a single pixel of yellow (color 4). The output grid is also 6x6. The transformation involves extending the single yellow pixel either horizontally across its entire row or vertically down its entire column.

Observing the examples:
- In `train_1`, the yellow pixel is at (row 2, col 0). The output fills row 2 with yellow.
- In `train_2`, the yellow pixel is at (row 5, col 4). The output fills column 4 with yellow.
- In `train_3`, the yellow pixel is at (row 0, col 2). The output fills column 2 with yellow.
- In `train_4`, the yellow pixel is at (row 4, col 0). The output fills row 4 with yellow.

The pattern seems to be: if the single yellow pixel is located in the first column (column index 0), then the entire row containing that pixel is filled with yellow. Otherwise (if the yellow pixel is in any column other than the first), the entire column containing that pixel is filled with yellow.

## Facts


```yaml
task_context:
  grid_size: Fixed 6x6 for all examples.
  background_color: white (0)
  input_objects:
    - object_type: single_pixel
      color: yellow (4)
      quantity: 1
      location: Variable, one per input grid.
  output_objects:
    - object_type: line
      color: yellow (4)
      orientation: horizontal (row) or vertical (column)
      location: Determined by the input pixel's location.
transformation_rule:
  trigger_condition: Location of the single yellow pixel in the input grid.
  action_based_on_condition:
    - condition: The yellow pixel is in column 0.
      action: Fill the entire row containing the yellow pixel with yellow.
    - condition: The yellow pixel is NOT in column 0.
      action: Fill the entire column containing the yellow pixel with yellow.
  output_grid_preservation:
    - The grid dimensions remain the same (6x6).
    - Pixels not part of the filled line remain white (0).
```


## Natural Language Program

1.  Locate the single non-white (yellow, color 4) pixel in the input grid. Let its coordinates be (row `R`, column `C`).
2.  Check the column index `C` of this pixel.
3.  If `C` is equal to 0, then change the color of all pixels in row `R` of the input grid to yellow (4).
4.  If `C` is not equal to 0, then change the color of all pixels in column `C` of the input grid to yellow (4).
5.  Return the modified grid as the output.