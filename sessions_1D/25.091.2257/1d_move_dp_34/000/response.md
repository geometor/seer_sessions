**Perception**

1.  **Grid Structure**: The inputs and outputs are single-row grids (1D arrays).
2.  **Background**: The predominant color is white (0), acting as the background.
3.  **Objects**: Each input grid contains two distinct non-white elements:
    *   A contiguous block (or "object") of a single color (magenta 6, red 2, or azure 8). The length of this block varies across examples.
    *   A single green pixel (3).
4.  **Transformation**: The primary transformation is the horizontal movement (translation) of the colored block.
5.  **Movement Rule**: The colored block moves to the right.
6.  **Stopping Condition**: The movement stops when the rightmost pixel of the colored block is positioned immediately to the left of the single green pixel.
7.  **Invariance**: The green pixel's position remains unchanged. The size and color of the moving block remain unchanged. The overall size of the grid remains unchanged. The pixels previously occupied by the block become white (0).

**Facts**


```yaml
task_type: object_manipulation
grid_dimensionality: 1D
background_color: 0 # white
objects:
  - type: contiguous_block
    properties:
      color: any non-white, non-green color (e.g., 6, 2, 8)
      size: variable length (e.g., 4, 3, 5)
      role: mobile_object
  - type: single_pixel
    properties:
      color: 3 # green
      role: boundary_marker
relationship:
  - type: spatial_adjacency
    description: In the output, the rightmost pixel of the mobile_object is immediately to the left of the boundary_marker.
transformation:
  - type: translation
    target: mobile_object
    direction: right
    termination_condition: adjacency to boundary_marker
    properties:
      preserves_shape: True
      preserves_color: True
      overwrites_original_position: True (with background color)
invariants:
  - element: boundary_marker
    property: position
  - element: grid
    property: size
```


**Natural Language Program**

1.  Identify the background color (white, 0).
2.  Identify the single green pixel (3) and note its index; this is the `marker_index`.
3.  Identify the contiguous block of non-white, non-green pixels. Note its color, its starting index (`start_index`), and its ending index (`end_index`). Calculate its length (`length = end_index - start_index + 1`).
4.  Create a new output grid of the same size as the input grid, initially filled with the background color (white, 0).
5.  Place the green pixel (3) in the output grid at the `marker_index`.
6.  Calculate the target ending index for the block in the output grid: `target_end_index = marker_index - 1`.
7.  Calculate the target starting index for the block in the output grid: `target_start_index = target_end_index - length + 1`.
8.  Copy the identified block (using its original color and length) into the output grid starting at `target_start_index` and ending at `target_end_index`.