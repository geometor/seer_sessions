## Perception

1.  **Input/Output Structure:** Both input and output are grids of pixels, primarily white (0), with some red (2) pixels. The output grids additionally contain blue (1) pixels.
2.  **Input Objects:** The input grids contain multiple instances of a specific shape made of red (2) pixels. This shape resembles a plus sign '+' or sometimes an 'H' where the central horizontal bar is missing. More accurately, it's a central red pixel with single red pixels directly above, below, left, and right of it. The background is white (0).
3.  **Transformation:** The transformation involves adding blue (1) pixels to the grid. These blue pixels form straight lines, either horizontal or vertical.
4.  **Relationship:** The blue lines appear *between* pairs of the red '+' shapes present in the input.
5.  **Conditions for Transformation:**
    *   A blue line is drawn between the *center* pixels of two red '+' shapes *only if* these center pixels lie on the same row (horizontal alignment) or the same column (vertical alignment).
    *   The blue line fills the white (0) pixels strictly *between* the two center pixels along that row or column. The center pixels themselves remain red.
    *   No other pixels are changed.

## Facts


```yaml
Objects:
  - type: Shape
    color: red (2)
    structure: 5-pixel plus sign (center pixel with N, S, E, W neighbors)
    alias: red_plus
  - type: Background
    color: white (0)
  - type: Line
    color: blue (1)
    location: Output grid only
    role: Connector

Relationships:
  - type: Alignment
    between: center pixels of red_plus shapes
    qualifier: Horizontal (same row) or Vertical (same column)
    required_for: Action

Actions:
  - name: IdentifyObjects
    target: red_plus shapes
    method: Locate the central pixel of each 5-pixel red plus shape.
  - name: FindAlignedPairs
    target: Pairs of red_plus shapes
    condition: Center pixels are horizontally or vertically aligned.
  - name: DrawLine
    color: blue (1)
    from: Center pixel of first red_plus in an aligned pair
    to: Center pixel of second red_plus in the aligned pair
    path: Straight line (horizontal or vertical) along the alignment axis.
    constraint: Fill only the white (0) background pixels strictly *between* the two center pixels. Do not overwrite the red pixels.

GridProperties:
  - Size: Variable (input and output have the same dimensions)
  - ColorsUsed: Input (white, red), Output (white, red, blue)
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all instances of the 'red plus' shape in the input grid. A 'red plus' shape consists of a central red (2) pixel and four adjacent red (2) pixels (up, down, left, right). Record the coordinates of the *center* pixel for each identified shape.
3.  Iterate through all unique pairs of the identified center pixels.
4.  For each pair of center pixels (P1 at (r1, c1) and P2 at (r2, c2)):
    a.  Check if they are horizontally aligned (r1 == r2) and have at least one white (0) pixel between them (abs(c1 - c2) > 1).
    b.  If horizontally aligned, fill all white (0) pixels in the output grid at row r1 between column c1 and column c2 (exclusive of c1 and c2) with blue (1).
    c.  Check if they are vertically aligned (c1 == c2) and have at least one white (0) pixel between them (abs(r1 - r2) > 1).
    d.  If vertically aligned, fill all white (0) pixels in the output grid at column c1 between row r1 and row r2 (exclusive of r1 and r2) with blue (1).
5.  Return the modified output grid.