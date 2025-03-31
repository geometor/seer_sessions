**Perception of Task Elements:**

1.  **Input Structure:**
    *   The input grids contain distinct regions.
    *   The top-left corner (typically the first few rows and first two columns) features pairs of non-white pixels. These pairs appear unique in each example and seem to act as a legend or key.
    *   The rest of the grid often contains vertical columns characterized by a repeating pattern of a single color alternating with white (`C 0 C 0 ...`). These pattern columns are separated by columns of all white pixels. Different pattern colors can exist in the same input grid.

2.  **Output Structure:**
    *   The output grids consist of rectangular blocks filled with checkerboard patterns.
    *   Each checkerboard pattern uses two colors.
    *   The locations and colors of these checkerboard rectangles correspond to the locations and colors of the pattern columns in the input.

3.  **Transformation:**
    *   The key pairs in the input's top-left define the two colors used for the checkerboard fill in the output. If a key pair is `(C1, C2)`, it seems to relate to input pattern columns of color `C1`. The corresponding output rectangle uses `C1` and `C2` for its checkerboard.
    *   For each distinct pattern color `C1` found in the input columns:
        *   Locate the corresponding key pair `(C1, C2)` in the top-left.
        *   Identify all columns containing the pattern color `C1`.
        *   Determine the bounding box (minimum and maximum row and column) that encloses all instances of `C1` within its pattern columns.
        *   In the output grid, fill this bounding box area. Cells within the bounding box that corresponded to `C1` in the input are filled with `C1` (which is `F2` in the logic below). Cells that corresponded to white (`0`) in the input are filled with `C2` (which is `F1` in the logic below).

**YAML Fact Document:**


```yaml
task_description: Transform input grids based on key pairs and pattern columns into output grids with corresponding filled checkerboard rectangles.

elements:
  - object: key_pairs
    description: Pairs of non-white pixels located in the top-left area of the input grid.
    properties:
      - location: Typically rows 0-2, columns 0-1.
      - structure: Two adjacent non-white pixels, e.g., `(C1, C2)`.
    role: Define the color mapping for the transformation. A pair `(C1, C2)` indicates that input patterns of color `C1` should be transformed using colors `C1` and `C2`.

  - object: pattern_columns
    description: Vertical columns in the input grid containing a repeating sequence of a specific color `C` and white `0` (e.g., `C 0 C 0...`).
    properties:
      - structure: Alternating non-white color `C` and white `0`.
      - separation: Pattern columns are usually separated by columns containing only white pixels.
      - multiplicity: Multiple pattern columns with different colors can exist in one input.
    role: Define the areas to be transformed in the output grid.

  - object: output_rectangle
    description: A rectangular area in the output grid filled with a two-color checkerboard pattern.
    properties:
      - fill: Two colors, determined by a key pair from the input.
      - pattern: Checkerboard fill.
      - location: Corresponds to the bounding box of a specific pattern color `C1` from the input's pattern columns.
      - color_rule: Input cells with `C1` become `C1` in output; input cells with `0` become `C2` in output (where `(C1, C2)` is the key pair).

actions:
  - action: identify_key_pairs
    description: Scan the top-left region of the input grid to find all color pairs `(C1, C2)`.
    output: A mapping from `C1` to `C2`. (Implicitly, `C1` also maps to itself).

  - action: identify_pattern_areas
    description: For each unique pattern color `C1` found outside the key pair region:
      - Find all columns containing `C1`.
      - Calculate the bounding box (min_row, max_row, min_col, max_col) enclosing all `C1` pixels within these columns.
    output: A set of bounding boxes, one for each pattern color `C1`, associated with the colors `(C1, C2)` derived from the key pairs.

  - action: generate_output
    description: Create an output grid of the same dimensions as the input, initially filled with white (`0`).
    input: Bounding boxes and associated fill colors `(C1, C2)`.
    process: For each bounding box associated with `(C1, C2)`:
      - Iterate through each cell `(r, c)` within the bounding box.
      - If the corresponding input cell `input[r][c]` was `C1`, set `output[r][c]` to `C1`.
      - If the corresponding input cell `input[r][c]` was `0`, set `output[r][c]` to `C2`.

relationships:
  - relationship: key_pair_to_pattern
    description: The first color `C1` of a key pair `(C1, C2)` corresponds to the color `C1` found in pattern columns.
  - relationship: pattern_to_rectangle
    description: The bounding box of a pattern color `C1` in the input defines the location and extent of the corresponding output rectangle.
  - relationship: key_pair_to_fill
    description: The key pair `(C1, C2)` determines the two colors (`C1` and `C2`) used to fill the output rectangle corresponding to pattern `C1`.
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Scan the top-left corner of the input grid (e.g., first 3 rows, first 2 columns) to identify all pairs of adjacent non-white pixels `(C1, C2)`. Store these as a mapping where the first color `C1` maps to the second color `C2`. Let's call this the `key_map`.
3.  Identify all unique non-white colors present in the input grid *outside* the key pair region. These are the pattern colors.
4.  For each unique pattern color `P` identified in step 3:
    a.  Check if `P` exists as a first color (`C1`) in the `key_map`. If not, skip this pattern color. Let the corresponding second color from the map be `K` (so `K = key_map[P]`).
    b.  Find all cell coordinates `(r, c)` in the input grid where the pixel value is `P`.
    c.  Determine the minimum and maximum row indices (`min_r`, `max_r`) and minimum and maximum column indices (`min_c`, `max_c`) from the coordinates found in step 4b. This defines the bounding box for pattern `P`.
    d.  Iterate through all cells `(r, c)` within this bounding box (from `min_r` to `max_r`, and `min_c` to `max_c`).
    e.  For each cell `(r, c)` inside the bounding box:
        i.  If the input grid at `input[r][c]` has the color `P`, set the output grid at `output[r][c]` to `P`.
        ii. If the input grid at `input[r][c]` has the background color (white, 0), set the output grid at `output[r][c]` to `K` (the corresponding second color from the key pair).
5.  Return the completed output grid.