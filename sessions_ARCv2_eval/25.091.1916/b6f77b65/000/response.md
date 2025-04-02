**Perception:**
The task involves transforming an input grid into an output grid of the same dimensions (12x12 in all examples). The core mechanic is a translation (shift) of the grid's contents, excluding the background (white, 0) and a specific "control" pixel located at the top-left corner (0, 0). The direction and magnitude of the shift are determined solely by the color of this control pixel. The control pixel itself remains unchanged in the output grid at position (0, 0). Pixels shifted beyond the grid boundaries are removed, and the newly empty areas resulting from the shift are filled with the background color (white, 0). The specific shift vectors corresponding to the control colors observed in the training examples need to be deduced.

**Facts:**


```yaml
Grid Properties:
  - dimensions: 12x12 (consistent across examples)
  - background_color: white (0)

Control Element:
  - type: pixel
  - location: top-left corner (0, 0)
  - function: determines the transformation parameters (shift vector)
  - persistence: the control pixel at (0, 0) remains unchanged in the output.

Transformation:
  - type: translation (shift)
  - scope: applies to all pixels except the background (0) and the control pixel at (0, 0).
  - vector_determination: depends on the color value of the control pixel.
  - observed_mappings:
      - control_color: 9 (maroon) -> shift_vector: (0, 0)  # (delta_row, delta_col)
      - control_color: 4 (yellow) -> shift_vector: (3, 0)  # Down by 3 rows
      - control_color: 6 (magenta) -> shift_vector: (2, -3) # Down by 2 rows, Left by 3 columns
      - control_color: 7 (orange) -> shift_vector: (5, 2)  # Down by 5 rows, Right by 2 columns
  - boundary_handling: pixels shifted outside the grid dimensions are discarded.
  - vacated_area_fill: areas left empty by the shift are filled with the background_color (white, 0).

Objects:
  - The non-background pixels form distinct shapes/objects.
  - These objects are translated rigidly as part of the overall grid shift.
```


**Natural Language Program:**

1.  **Identify Control Parameters**: Examine the input grid at coordinates (0, 0) to find the control color `C`. Determine the corresponding shift vector `(delta_row, delta_col)` based on the value of `C` using the predefined mapping:
    *   If `C` is 9 (maroon), `(delta_row, delta_col) = (0, 0)`.
    *   If `C` is 4 (yellow), `(delta_row, delta_col) = (3, 0)`.
    *   If `C` is 6 (magenta), `(delta_row, delta_col) = (2, -3)`.
    *   If `C` is 7 (orange), `(delta_row, delta_col) = (5, 2)`.
2.  **Initialize Output**: Create a new grid (output grid) with the same dimensions as the input grid, filled entirely with the background color (white, 0).
3.  **Preserve Control Pixel**: Copy the control color `C` from the input grid's (0, 0) position to the output grid's (0, 0) position.
4.  **Translate Content**: Iterate through every cell `(row, col)` of the input grid, excluding the control cell (0, 0).
5.  **Calculate New Position**: For the current cell `(row, col)`, calculate its potential new position `(new_row, new_col)` in the output grid by applying the shift vector: `new_row = row + delta_row`, `new_col = col + delta_col`.
6.  **Apply Shift within Bounds**: Check if the calculated `(new_row, new_col)` falls within the valid row and column indices of the output grid.
7.  **Update Output Grid**: If the new position is within bounds, copy the color value from the input grid at `(row, col)` to the output grid at `(new_row, new_col)`. If the position is out of bounds, the pixel is effectively discarded.
8.  **Finalize**: The resulting output grid, containing the preserved control pixel and the shifted content, is the final result.