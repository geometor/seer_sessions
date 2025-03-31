## Perception

1.  **Grid Structure:** The input and output are grids of varying sizes filled with colors, primarily orange (7), gray (5), red (2), and azure (8).
2.  **Background:** The dominant color is orange (7), acting as the background, which remains static between input and output.
3.  **Key Objects:**
    *   A single red pixel (2).
    *   A single azure pixel (8).
    *   A solid rectangular block of gray pixels (5).
4.  **Transformation:** The core transformation involves changing the positions of the red and azure pixels. The gray block and the orange background remain unchanged.
5.  **Red Pixel Movement:** The red pixel moves from its original location in the input to the location previously occupied by the azure pixel in the input.
6.  **Azure Pixel Movement:** The azure pixel moves from its original location in the input to a new location determined by the position of the gray rectangle. Specifically, it moves to the cell located at the row index of the bottom edge of the gray rectangle and the column index immediately to the right of the right edge of the gray rectangle.
7.  **Interaction:** The movement of the red pixel depends on the initial position of the azure pixel. The final movement of the azure pixel depends on the position (specifically the bottom-right extent) of the gray rectangle.

## Facts


```yaml
task_elements:
  - background:
      color: orange (7)
      shape: grid_fill
      state: static
  - object_1:
      description: Single red pixel
      color: red (2)
      shape: 1x1 pixel
      initial_position: variable (r1_in, c1_in)
      final_position: location of object_2 in input (r2_in, c2_in)
      action: moves
  - object_2:
      description: Single azure pixel
      color: azure (8)
      shape: 1x1 pixel
      initial_position: variable (r2_in, c2_in)
      final_position: calculated based on object_3 (r3_bottom, c3_right + 1)
      action: moves
  - object_3:
      description: Gray rectangle
      color: gray (5)
      shape: rectangle (variable size)
      position: variable (defined by top-left (r3_top, c3_left) and bottom-right (r3_bottom, c3_right))
      state: static
relationships:
  - object_1's final position is determined by object_2's initial position.
  - object_2's final position is determined by object_3's bottom-right boundary.
```


## Natural Language Program

1.  Create the output grid by copying the input grid.
2.  Locate the coordinates of the single red pixel (color 2) in the input grid. Let this be `(red_row_in, red_col_in)`.
3.  Locate the coordinates of the single azure pixel (color 8) in the input grid. Let this be `(azure_row_in, azure_col_in)`.
4.  Identify the gray rectangular block (color 5). Find the maximum row index (`gray_row_bottom`) and maximum column index (`gray_col_right`) occupied by any gray pixel.
5.  Set the pixel at `(red_row_in, red_col_in)` in the output grid to the background color (orange 7).
6.  Set the pixel at `(azure_row_in, azure_col_in)` in the output grid to the color of the red pixel (red 2).
7.  Calculate the target position for the azure pixel: `(gray_row_bottom, gray_col_right + 1)`.
8.  Set the pixel at the calculated target position `(gray_row_bottom, gray_col_right + 1)` in the output grid to the color of the azure pixel (azure 8).
9.  Leave all other pixels (the gray rectangle and the remaining orange background) unchanged from their input values.