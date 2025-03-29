*   **Perception:**
    *   The input grids contain a prominent square object composed of gray pixels (color 5).
    *   Outside this gray square, there are typically four single pixels of different colors. These pixels seem to be positioned conceptually near the four corners relative to the gray square or the grid boundaries.
    *   The output grids replace the gray square with a composite structure made of four equally sized smaller squares.
    *   The colors of these four smaller squares in the output correspond to the colors of the four single pixels found in the input.
    *   The position of each colored smaller square within the replaced area corresponds to the relative position of the original single pixel (e.g., the top-left input pixel's color fills the top-left quadrant of the replaced area).
    *   The size of the gray square dictates the size of the output squares. If the gray square is N x N, each output square is (N/2) x (N/2).
    *   All original pixels (the gray square and the four corner pixels) disappear in the output, replaced by the new structure within the bounds of the original gray square. The rest of the grid remains white.

*   **Facts:**
    
```yaml
    Objects:
      - Type: Background
        Color: white (0)
      - Type: Container
        Color: gray (5)
        Shape: Square
        Properties:
          - Size (N x N, where N is even)
          - Position (Top-left corner coordinates)
      - Type: Corner_Pixels
        Color: Any non-white, non-gray color
        Shape: Single pixel (1x1)
        Quantity: 4
        Properties:
          - Color
          - Relative Position (conceptually top-left, top-right, bottom-left, bottom-right relative to each other or the container)
    Actions:
      - Identify: Locate the gray square (Container).
      - Identify: Locate the four single non-white, non-gray pixels (Corner_Pixels).
      - Determine: Find the dimensions (N x N) and position of the Container.
      - Determine: Find the colors of the four Corner_Pixels.
      - Determine: Map each Corner_Pixel to a quadrant (top-left, top-right, bottom-left, bottom-right) based on their relative positions.
      - Calculate: Determine the size of the output sub-squares (N/2 x N/2).
      - Create: Initialize an output grid of the same size as the input, filled with the background color.
      - Replace: Fill the area previously occupied by the gray Container with four sub-squares.
      - Fill: Assign the color of the top-left Corner_Pixel to the top-left sub-square.
      - Fill: Assign the color of the top-right Corner_Pixel to the top-right sub-square.
      - Fill: Assign the color of the bottom-left Corner_Pixel to the bottom-left sub-square.
      - Fill: Assign the color of the bottom-right Corner_Pixel to the bottom-right sub-square.
    Relationships:
      - The gray Container defines the location and total size of the output structure.
      - The size of the Container (N x N) determines the size of the four output sub-squares ((N/2) x (N/2)).
      - The colors of the four Corner_Pixels determine the colors of the four output sub-squares.
      - The relative spatial arrangement of the four Corner_Pixels determines which color goes into which quadrant of the output structure.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Identify the largest contiguous square object composed solely of gray pixels (color 5) in the input grid. Record its top-left corner coordinates (row `r`, column `c`) and its size (N x N).
    3.  Identify all single pixels in the input grid that are not white (0) and not gray (5). There should be exactly four such pixels.
    4.  Determine the relative positions of these four pixels: identify which one is conceptually top-left, top-right, bottom-left, and bottom-right relative to the others. (This can be done by finding their bounding box and assigning roles based on corner proximity). Record the color of each of these four 'corner' pixels.
    5.  Calculate the size of the sub-squares for the output: `sub_size = N / 2`.
    6.  Fill the top-left `sub_size` x `sub_size` area of the output grid, starting at position (`r`, `c`), with the color of the identified top-left corner pixel.
    7.  Fill the top-right `sub_size` x `sub_size` area of the output grid, starting at position (`r`, `c + sub_size`), with the color of the identified top-right corner pixel.
    8.  Fill the bottom-left `sub_size` x `sub_size` area of the output grid, starting at position (`r + sub_size`, `c`), with the color of the identified bottom-left corner pixel.
    9.  Fill the bottom-right `sub_size` x `sub_size` area of the output grid, starting at position (`r + sub_size`, `c + sub_size`), with the color of the identified bottom-right corner pixel.
    10. The final output grid is the result of these filling operations.