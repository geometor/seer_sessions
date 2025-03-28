
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 3 0 0 4 0 0 0 0 0
0 0 0 0 0 1 0 0 2 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 3 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 2 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 0 5 5 0 0 0 0
0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 1 0 0 2 0 0 0 0
0 0 3 0 0 4 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 4 0 0 0 0
0 0 0 1 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 4 0 1 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain one or more 2x2 squares composed of gray pixels (5). The rest of the grid is composed of white pixels (0).
    *   The output grids retain the original gray 2x2 squares from the input.
    *   Additionally, for each gray 2x2 square present in the input, four new colored pixels appear in the output grid.
    *   These new pixels are placed diagonally adjacent to the corners of the gray square:
        *   A blue pixel (1) is placed diagonally adjacent to the top-left corner of the gray square.
        *   A red pixel (2) is placed diagonally adjacent to the top-right corner of the gray square.
        *   A green pixel (3) is placed diagonally adjacent to the bottom-left corner of the gray square.
        *   A yellow pixel (4) is placed diagonally adjacent to the bottom-right corner of the gray square.
    *   The process is applied independently to every 2x2 gray square found in the input.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        description: A 2D array of pixels representing colors.
        properties:
          - background_color: white (0)
      - object: gray_square
        description: A contiguous 2x2 block of gray pixels (5).
        properties:
          - color: gray (5)
          - shape: square
          - size: 2x2
      - object: corner_pixels
        description: Four single pixels added around each gray_square.
        properties:
          - colors: [blue (1), red (2), green (3), yellow (4)]
          - placement: Diagonally adjacent to the corners of the associated gray_square.
            details:
              - color: blue (1) -> top-left diagonal
              - color: red (2) -> top-right diagonal
              - color: green (3) -> bottom-left diagonal
              - color: yellow (4) -> bottom-right diagonal
    actions:
      - identify: Locate all instances of 2x2 gray_squares in the input grid.
      - place: Add the corner_pixels to the output grid based on the location of each identified gray_square.
    relationships:
      - preservation: The original gray_squares from the input are preserved in the output grid.
      - creation: The corner_pixels are created in the output grid based on the locations of the gray_squares.
      - spatial: Each corner_pixel has a specific diagonal adjacency relationship to one corner of its associated gray_square.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each possible top-left corner position (row `r`, column `c`) in the input grid such that a 2x2 square can be formed within the grid boundaries (i.e., up to height-2 and width-2).
    3.  Check if the pixels at `(r, c)`, `(r+1, c)`, `(r, c+1)`, and `(r+1, c+1)` are all gray (5).
    4.  If a 2x2 gray square is found starting at `(r, c)`:
        a.  Place a blue pixel (1) at position `(r-1, c-1)` in the output grid, if this position is within the grid boundaries.
        b.  Place a red pixel (2) at position `(r-1, c+2)` in the output grid, if this position is within the grid boundaries.
        c.  Place a green pixel (3) at position `(r+2, c-1)` in the output grid, if this position is within the grid boundaries.
        d.  Place a yellow pixel (4) at position `(r+2, c+2)` in the output grid, if this position is within the grid boundaries.
    5.  Return the modified output grid.
