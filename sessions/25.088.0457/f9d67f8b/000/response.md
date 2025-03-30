## Perception

1.  **Input/Output Structure:** Both input and output grids are the same size (30x30 in all examples).
2.  **Color Palette:** Multiple colors (0-9) are used. White (0) is not present. Maroon (9) and Gray (5) seem particularly important.
3.  **Key Object:** In each input grid, there's a prominent, relatively large, contiguous block of maroon (9) pixels, roughly centered but varying in exact position and shape (rectangular).
4.  **Transformation Focus:** The changes between input and output grids occur exclusively in the pixels immediately surrounding this central maroon block.
5.  **Affected Pixels:** Only gray (5) pixels adjacent (orthogonally or diagonally) to the maroon block are modified.
6.  **Nature of Change:** The affected gray pixels change their color. The new color seems determined by reflecting the position of the gray pixel across the boundary of the maroon block and copying the color found at that reflected position in the input grid.
7.  **The "Mirror":** The maroon block acts like a mirror. Gray pixels next to it take on the color of the pixel "seen" in the reflection.
8.  **Stability:** The maroon block itself and all pixels *not* adjacent to it remain unchanged. Pixels adjacent to the maroon block but *not* colored gray also remain unchanged.

## Facts


```yaml
elements:
  - object: grid
    description: A 2D array of pixels with integer values 0-9 representing colors. Input and output grids have identical dimensions in each example (30x30).
  - object: mirror_block
    description: The largest contiguous block of maroon (9) pixels in the input grid. Its shape and position vary between examples but it's always a single, connected component. Acts as the center for the transformation.
    properties:
      - color: maroon (9)
      - connectivity: contiguous (8-way adjacency)
      - role: reflector
  - object: target_pixels
    description: Pixels in the input grid that are subject to change.
    properties:
      - color: gray (5)
      - location: Must be immediately adjacent (orthogonally or diagonally) to at least one pixel belonging to the mirror_block.
  - object: source_pixels
    description: Pixels in the input grid whose color is copied onto target_pixels.
    properties:
      - location: Position determined by reflecting a target_pixel's coordinates across the boundary of the mirror_block.
      - color: Any color present in the input grid.

relationships:
  - type: adjacency
    description: Target_pixels must be adjacent (neighboring in 8 directions) to the mirror_block.
  - type: reflection
    description: The position of a source_pixel is the reflection of a target_pixel's position across the nearest boundary point/segment of the mirror_block.
    details: If a target_pixel (r, c) is adjacent to a mirror_block pixel (mr, mc), the reflected source_pixel position (sr, sc) is calculated as sr = 2*mr - r, sc = 2*mc - c.

actions:
  - action: identify_mirror
    description: Find the largest contiguous block of maroon (9) pixels in the input grid.
  - action: identify_targets
    description: Find all gray (5) pixels adjacent to the identified mirror_block.
  - action: reflect_and_copy
    description: For each target_pixel, calculate its reflection point across the adjacent mirror_block boundary. Copy the color from the input grid at the reflection point to the target_pixel's location in the output grid.
    condition: The reflection point must be within the grid boundaries. If a target_pixel is adjacent to multiple mirror_block pixels, the reflection across any one of them determines the change (typically the first one encountered in a scan).
  - action: copy_unchanged
    description: All pixels that are not target_pixels (i.e., not gray and adjacent to the mirror, or part of the mirror, or not adjacent at all) retain their original color from the input grid in the output grid.
```


## Natural Language Program

1.  Initialize the output grid as an identical copy of the input grid.
2.  Identify the largest contiguous block (using 8-way adjacency) of maroon (9) pixels in the input grid. Let this be the "mirror block".
3.  Iterate through each pixel (r, c) of the input grid.
4.  If the color of the input pixel at (r, c) is gray (5):
    a. Check its 8 neighbors (nr, nc).
    b. If any neighbor (nr, nc) is within the grid bounds AND is part of the "mirror block":
        i. Calculate the reflection coordinates (refl_r, refl_c) using the formula: `refl_r = 2 * nr - r`, `refl_c = 2 * nc - c`.
        ii. Check if the calculated reflection coordinates (refl_r, refl_c) are within the bounds of the grid.
        iii. If the reflection coordinates are valid (within bounds):
            1.  Get the color `reflected_color` from the *input* grid at position (refl_r, refl_c).
            2.  Update the color of the pixel at position (r, c) in the *output* grid to `reflected_color`.
            3.  Stop checking neighbors for the current gray pixel (r, c) and proceed to the next pixel in the main grid iteration (Step 3). (This ensures only the first valid reflection found is applied).
5.  After iterating through all pixels, return the final output grid.