
## train_1

**input:**
```
0 8 0 0 8 0 0
8 8 0 0 8 8 0
0 8 8 0 8 8 0
0 8 8 0 8 8 0
0 0 8 8 0 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 4 0 0
2 2 0 0 4 4 0
0 1 1 0 1 1 0
0 1 1 0 1 1 0
0 0 3 3 0 0 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 8 0 0 0
8 8 8 8 8 0 0
0 8 8 0 8 8 0
0 8 8 8 8 0 0
0 0 0 8 8 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 1 1 0 0 0
3 3 1 1 4 0 0
0 3 2 0 4 4 0
0 2 2 1 1 0 0
0 0 0 1 1 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_3

**input:**
```
8 8 8 0 0 0 0
8 8 8 8 0 0 0
8 8 0 8 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
1 1 4 0 0 0 0
1 1 4 4 0 0 0
3 3 0 2 0 0 0
0 3 2 2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming an input grid containing white (0) and azure (8) pixels into an output grid of the same dimensions. The white pixels remain unchanged. The azure pixels are replaced by one of four colors: blue (1), red (2), green (3), or yellow (4). The core challenge lies in determining the rule that dictates which of the four colors replaces a specific azure pixel. The transformation appears to depend on the local neighborhood of each azure pixel, specifically the pattern of other azure pixels within a 2x2 square starting at the pixel's location.

*   **Facts:**
    
```yaml
    task_type: color_transformation
    grid_properties:
      - input_output_size_identical: true
      - background_color: 0 # white
    objects:
      - type: pixel_group
        color: 8 # azure
        input_representation: contiguous_blocks
        output_representation: same_pixels_recolored
    transformations:
      - type: recoloring
        input_color: 8 # azure
        output_colors: [1, 2, 3, 4] # blue, red, green, yellow
        rule_basis: local_pattern
        pattern_scope: 2x2_neighborhood
        details: Each azure pixel in the input is assigned an output color based on the configuration of azure pixels within the 2x2 square for which the input pixel is the top-left corner. White pixels remain white.
    color_mapping_rule (hypothesis):
      - pattern: '[[8,0],[0,0]]' -> color: 3 # green
      - pattern: '[[8,8],[0,0]]' -> color: 1 # blue
      - pattern: '[[8,0],[8,0]]' -> color: 2 # red
      - pattern: '[[8,0],[0,8]]' -> color: 3 # green
      - pattern: '[[8,8],[8,0]]' -> color: 3 # green
      - pattern: '[[8,8],[0,8]]' -> color: 2 # red
      - pattern: '[[8,0],[8,8]]' -> color: 4 # yellow
      - pattern: '[[8,8],[8,8]]' -> color: 1 # blue
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with white (0).
    2.  Iterate through each pixel `(r, c)` in the input grid, from top-to-bottom, left-to-right.
    3.  If the input pixel `input[r, c]` is white (0), skip to the next pixel.
    4.  If the input pixel `input[r, c]` is azure (8):
        a.  Examine the 2x2 neighborhood block starting at `(r, c)`. Consider pixels outside the grid boundaries as white (0). Let this block be `P = [[input[r,c], input[r,c+1]], [input[r+1,c], input[r+1,c+1]]]`.
        b.  Determine the output color `C` based on the pattern `P` according to the following rules:
            *   If `P` is `[[8,0],[0,0]]`, `C` is 3 (green).
            *   If `P` is `[[8,8],[0,0]]`, `C` is 1 (blue).
            *   If `P` is `[[8,0],[8,0]]`, `C` is 2 (red).
            *   If `P` is `[[8,0],[0,8]]`, `C` is 3 (green).
            *   If `P` is `[[8,8],[8,0]]`, `C` is 3 (green).
            *   If `P` is `[[8,8],[0,8]]`, `C` is 2 (red).
            *   If `P` is `[[8,0],[8,8]]`, `C` is 4 (yellow).
            *   If `P` is `[[8,8],[8,8]]`, `C` is 1 (blue).
            *   (Handle patterns not starting with 8 if necessary, though step 4 ensures `input[r,c]` is 8).
        c.  Set the corresponding pixel in the output grid `output[r, c]` to the determined color `C`.
    5.  Return the completed output grid.
