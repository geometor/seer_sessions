**Perception of Task Elements:**

1.  **Grid Structure:** The input and output grids are structured with prominent horizontal and vertical lines of a single color (green '3' in train_1, azure '8' in train_2 and train_3). These lines act as dividers, creating a grid of cells or "rooms".
2.  **Background:** The background color within these rooms is consistently white ('0').
3.  **Payload Objects:** Within some rooms, there are rectangular blocks of solid colors. These are the "payload" objects. In each example, there are exactly two distinct payload colors besides the divider and background colors.
    *   train_1: Yellow ('4') and Magenta ('6'). Divider: Green ('3').
    *   train_2: Green ('3') and Magenta ('6'). Divider: Azure ('8').
    *   train_3: Red ('2') and Yellow ('4'). Divider: Azure ('8').
4.  **Transformation:** The core transformation involves swapping the colors of the payload objects. All pixels that have the first payload color in the input grid are changed to the second payload color in the output grid. Conversely, all pixels that have the second payload color in the input are changed to the first payload color in the output.
5.  **Static Elements:** The divider lines and the white background pixels remain unchanged between the input and output grids.

**YAML Facts:**


```yaml
Grid:
  Structure: Delimited by lines of a single color (divider_color).
  Background: White (0).
Divider:
  Property: Forms horizontal and vertical lines.
  Role: Separates the grid into sections/rooms.
  Persistence: Remains unchanged in the output.
Payload_Colors:
  Quantity: Exactly two distinct colors per task, excluding white (0) and the divider_color.
  Identification:
    - Task 1: Yellow (4), Magenta (6)
    - Task 2: Green (3), Magenta (6)
    - Task 3: Red (2), Yellow (4)
  Role: Occupy specific pixel locations within the grid structure.
Transformation:
  Action: Swap pixel colors.
  Scope: Applies only to pixels matching one of the two payload_colors.
  Rule: All pixels of payload_color_1 become payload_color_2, and all pixels of payload_color_2 become payload_color_1.
  Invariance: Pixels matching the divider_color or the background_color (white 0) are not modified.
```


**Natural Language Program:**

1.  Identify the color used for the grid divider lines (this is the color that forms consistent horizontal and vertical lines across the grid).
2.  Identify the two distinct colors present in the input grid that are neither the background color (white '0') nor the divider color. Call these `payload_color_1` and `payload_color_2`.
3.  Create a new grid with the same dimensions as the input grid.
4.  Iterate through each pixel of the input grid:
    a.  If the pixel's color is `payload_color_1`, set the corresponding pixel in the new grid to `payload_color_2`.
    b.  If the pixel's color is `payload_color_2`, set the corresponding pixel in the new grid to `payload_color_1`.
    c.  Otherwise (if the pixel's color is the background color or the divider color), copy the pixel's color directly to the corresponding position in the new grid.
5.  The new grid is the output.