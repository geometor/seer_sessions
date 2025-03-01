"""
1.  **Expand Input Grid:** The input grid is expanded to double its height and double *plus* double its width.
2. **Fill New Rows with background and secondary color:** all odd rows, starting at 1, is filled with `8`. Each element at an odd index is `8`.
3.  **Replicate Original Cells:** The original cells from the input grid are replicated in the output grid.
    *   Each original cell is copied into the output grid multiple times.
    *   The original cell located at (r, c) in the input appears at positions (2r, 2c) and (2r, 2c + 4) in the output.
4.  **Maintain Other cells:** Any empty cell `0` is maintained in the output at position (2r, 2c)
.

Essentially the output is structured as such:
- original input copied to maintain relative positions
- original input copied and x position + 4 added
- odd rows are filled with an alternating pattern

Example
