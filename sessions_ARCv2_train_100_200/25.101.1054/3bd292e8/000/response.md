## Perception of Task Elements

The input grids consist primarily of two colors: Red (2) and Orange (7). The Red pixels form distinct shapes or patterns, while the Orange pixels typically fill the remaining space, acting like a background or field.

The output grids retain the original Red (2) pixels in their exact positions. The Orange (7) pixels from the input are replaced by either Green (3) or Gray (5) pixels in the output.

The transformation logic appears to depend on the proximity of the Orange pixels to the Red pixels. Orange pixels that are adjacent (horizontally, vertically, or diagonally) to any Red pixel are changed to Gray (5). Orange pixels that are not adjacent to any Red pixel are changed to Green (3).

## YAML Facts


```yaml
Colors:
  Input:
    - Red: 2
    - Orange: 7
  Output:
    - Red: 2
    - Green: 3
    - Gray: 5
Objects:
  - Type: Pixel cluster
    Color: Red (2)
    Property: Static - position remains unchanged.
  - Type: Pixel
    Color: Orange (7)
    Property: Dynamic - color changes based on relationship to Red pixels.
Relationships:
  - Type: Adjacency
    Description: Checks if an Orange pixel is adjacent (including diagonals) to a Red pixel.
    Source: Orange Pixel (7)
    Target: Red Pixel (2)
Actions:
  - Action: Identify
    Target: All Red (2) pixels.
  - Action: Identify
    Target: All Orange (7) pixels.
  - Action: Conditional Recolor
    Target: Orange (7) pixels.
    Condition:
      - If adjacent (8 directions) to any Red (2) pixel:
          Change color to Gray (5).
      - Else (not adjacent to any Red (2) pixel):
          Change color to Green (3).
Grid:
  Property: The dimensions of the output grid are identical to the input grid.
```


## Natural Language Program

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each cell (pixel) of the input grid using its row and column index.
3.  Get the color of the current pixel in the input grid.
4.  If the input pixel color is Red (2), set the corresponding pixel in the new grid to Red (2).
5.  If the input pixel color is Orange (7):
    a.  Examine the 8 neighboring pixels (up, down, left, right, and the four diagonals) of the current pixel in the *input* grid.
    b.  Check if any of these neighbors have the color Red (2).
    c.  If at least one neighbor is Red (2), set the corresponding pixel in the new grid to Gray (5).
    d.  If none of the neighbors are Red (2), set the corresponding pixel in the new grid to Green (3).
6.  The final new grid is the output.