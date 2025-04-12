
## train_1

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 2 7 7 7
7 5 7 7 2 2 7 7
7 5 5 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7
7 7 7 7 2 2 7 7
```


**output:**
```
7 7 7 7 7 7 7 7
7 7 4 7 2 7 7 7
7 5 4 3 2 2 7 7
7 5 5 3 3 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7
7 7 7 7 2 2 3 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 5 7 7 7 5 5 7
7 5 5 7 7 7 5 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 2 2 7 7 2 7 7
7 7 2 7 7 2 2 7
7 7 7 7 7 7 7 7
```


**output:**
```
7 7 4 7 7 7 7 7
7 5 4 4 7 5 5 7
7 5 5 7 4 4 5 7
7 7 7 7 7 4 7 7
7 7 3 3 7 7 7 7
7 2 2 3 7 2 7 7
7 7 2 7 3 2 2 7
7 7 7 7 3 3 7 7
```

## Perception

The input and output are grids of pixels with different colors. The background color is orange (7). The task involves identifying specific shapes, 3-pixel L-shapes, composed of either gray (5) or red (2) pixels. Based on the color and properties (orientation, location) of these L-shapes, new pixels (yellow 4 and/or green 3) are added to the grid in specific patterns relative to the original L-shapes. The original L-shapes remain unchanged. The rules for adding pixels differ significantly depending on whether the L-shape is gray or red.

## Facts


```yaml
objects:
  - type: grid
    properties:
      background_color: 7 (orange)
  - type: shape
    identifier: L-shape
    properties:
      color: 5 (gray) or 2 (red)
      size: 3 pixels
      connectivity: L-configuration (one pixel connected to two others in the shape)
      corner_pixel: The pixel within the L-shape connected to the other two pixels.
      orientation: Defined by the relative positions of the 3 pixels (e.g., opens Top-Right, Bottom-Right, Bottom-Left, Top-Left).
      missing_pixel (MP): The unique background pixel adjacent to two pixels of the L-shape, which would complete a 2x2 square containing the L-shape.
actions:
  - name: identify_L_shapes
    input: input_grid
    output: list of L-shapes with properties (color, pixels, corner_pixel, orientation, missing_pixel)
  - name: process_gray_L_shape
    input: gray_L_shape (with properties)
    output: set of new pixels (coordinates and colors: Yellow 4, Green 3)
    condition: Based on L-shape orientation.
    details:
      - Fill the Missing Pixel (MP) with Yellow (4).
      - Add 3 more pixels (Yellow or Green) at specific relative positions to MP, determined by the L-shape's orientation.
        - Orientation "opens Top-Right": Add Y at MP+(-1,0), G at MP+(0,+1), G at MP+(+1,+1).
        - Orientation "opens Bottom-Right": Add Y at MP+(-1,-1), Y at MP+(0,-1), Y at MP+(+1,0).
  - name: process_red_L_shape
    input: red_L_shape (with properties)
    output: set of new pixels (coordinates and color: Green 3)
    condition: Based on the parity of the corner_pixel's coordinates (r, c).
    details:
      - If corner (r, c) is (even, even): Add nothing.
      - If corner (r, c) is (odd, odd): Add Green (3) at MP+(+1,+1).
      - If corner (r, c) is (even, odd): Add a Green (3) L-shape (3 pixels) opening Top-Right, with its corner at C+(+1,-1).
      - If corner (r, c) is (odd, even): Add a Green (3) L-shape (3 pixels) opening Bottom-Left, with its corner at C+(-1,+1).
  - name: apply_changes
    input: input_grid, list of new pixels to add
    output: output_grid
    details: Create a copy of the input grid. For each new pixel (coord, color), if the coordinate is within bounds and the current color at that coordinate in the copy is the background color (orange 7), update the color.
relationships:
  - The added pixels' locations and colors depend on the source L-shape's color, orientation, and corner pixel coordinates.
  - Added pixels only replace the background color.
```


## Natural Language Program

1.  **Initialize**: Create a copy of the input grid to serve as the output grid.
2.  **Identify L-Shapes**: Scan the input grid to find all 3-pixel L-shapes made of gray (5) or red (2). For each L-shape, record its color, the coordinates of its three pixels, the coordinate of its corner pixel (C), its orientation (e.g., opens Top-Right, Bottom-Right, etc.), and the coordinate of the background pixel (MP) that would complete its 2x2 bounding box.
3.  **Process Gray L-Shapes**: For each identified gray L-shape:
    a.  Determine its orientation and its Missing Pixel (MP).
    b.  Add Yellow (4) to the output grid at coordinate MP, if MP is currently background (orange 7).
    c.  Based on orientation, determine the coordinates for 3 additional pixels relative to MP:
        i.  If orientation is "opens Top-Right": Target coordinates are MP+(-1,0) [Y], MP+(0,+1) [G], MP+(+1,+1) [G].
        ii. If orientation is "opens Bottom-Right": Target coordinates are MP+(-1,-1) [Y], MP+(0,-1) [Y], MP+(+1,0) [Y].
        iii. (Define rules for other orientations if needed).
    d.  For each target coordinate and its associated color (Y or G) from step 3c, add the color to the output grid at that coordinate, provided it's within bounds and currently background (orange 7).
4.  **Process Red L-Shapes**: For each identified red L-shape:
    a.  Identify its corner pixel C=(r,c) and its Missing Pixel MP.
    b.  Check the parity of the corner pixel's coordinates (r, c).
    c.  Determine the target coordinates and color (Green 3) based on parity:
        i.  If r=even, c=even: No pixels are added.
        ii. If r=odd, c=odd: Target coordinate is MP+(+1,+1). Add Green (3).
        iii. If r=even, c=odd: Target coordinates form a Green (3) L-shape opening Top-Right, with its corner at C+(+1,-1). The three pixels are C+(0,-1), C+(+1,-1), C+(+1,0). Add Green (3) to each.
        iv. If r=odd, c=even: Target coordinates form a Green (3) L-shape opening Bottom-Left, with its corner at C+(-1,+1). The three pixels are C+(-1,0), C+(-1,+1), C+(0,+1). Add Green (3) to each.
    d.  For each target coordinate determined in step 4c, add Green (3) to the output grid at that coordinate, provided it's within bounds and currently background (orange 7).
5.  **Return Output**: The modified grid is the final output.
