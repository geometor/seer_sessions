**Perception**

1.  **Input/Output Structure:** Both examples show an input grid and a corresponding output grid of the same dimensions.
2.  **Key Feature:** A prominent feature in both inputs is the presence of lines made entirely of yellow (4) pixels. In Example 1, there's a horizontal yellow line. In Example 2, there's both a horizontal and a vertical yellow line intersecting at the center.
3.  **Transformation Pattern:** The output grids retain the yellow lines from the input. The key change involves mirroring or reflecting patterns across these yellow lines.
4.  **Example 1 Analysis:** The horizontal yellow line acts as a mirror. The pattern of colored pixels present above the yellow line in the input is copied and vertically reflected into the area below the yellow line in the output. The original pattern above the line remains unchanged.
5.  **Example 2 Analysis:** The horizontal and vertical yellow lines divide the grid into four quadrants. The pattern present in the top-left quadrant of the input is reflected horizontally into the top-right quadrant, vertically into the bottom-left quadrant, and both horizontally and vertically into the bottom-right quadrant in the output grid. The original pattern in the top-left quadrant remains unchanged.
6.  **General Observation:** The yellow lines function as axes of symmetry. The content from one region (the "source" region, which appears to be the top region in Example 1 and the top-left region in Example 2) is reflected across these axes to fill the other regions defined by the axes. The yellow lines themselves are preserved.

**Facts**


```yaml
Task: Reflect patterns across yellow lines.

Input_Grid:
  - Contains pixels of various colors (0-9).
  - Features one or more lines composed entirely of yellow (4) pixels.
    - These lines can be horizontal or vertical.
    - They act as separators or axes.

Output_Grid:
  - Same dimensions as the input grid.
  - Preserves the yellow lines from the input grid.
  - Fills regions separated by the yellow lines based on reflection.

Transformation:
  - Identify complete horizontal yellow lines.
  - Identify complete vertical yellow lines.
  - These lines define axes of reflection and divide the grid into regions (2 or 4).
  - Identify the "source" region:
    - If only a horizontal line exists, the source is the region above it.
    - If only a vertical line exists, the source is the region to the left of it.
    - If both exist, the source is the top-left region.
  - Copy the pattern from the source region (excluding the yellow lines themselves).
  - Reflect this pattern across the identified yellow line(s) into the other region(s).
    - Horizontal line: Reflect vertically.
    - Vertical line: Reflect horizontally.
    - Both lines: Reflect horizontally, vertically, and diagonally (or combination of horizontal and vertical reflections).
  - The original source pattern and the yellow lines remain in the output.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to find the row index (`hr`) of a horizontal line composed entirely of yellow (4) pixels, if one exists.
3.  Scan the input grid to find the column index (`vc`) of a vertical line composed entirely of yellow (4) pixels, if one exists.
4.  **If a horizontal yellow line exists at row `hr`:**
    a.  Define the source region as the area above the line (rows 0 to `hr-1`).
    b.  Define the target region as the area below the line (rows `hr+1` to the bottom).
    c.  For each pixel at `(r, c)` in the source region (where `0 <= r < hr`), copy its color to the corresponding reflected position `(hr + (hr - r), c)` in the output grid, provided this position is within the grid bounds.
5.  **If a vertical yellow line exists at column `vc`:**
    a.  Define the source region as the area to the left of the line (columns 0 to `vc-1`).
    b.  Define the target region as the area to the right of the line (columns `vc+1` to the right edge).
    c.  For each pixel at `(r, c)` in the source region (where `0 <= c < vc`), copy its color to the corresponding reflected position `(r, vc + (vc - c))` in the output grid, provided this position is within the grid bounds. *(Correction: Step 4c reflects across the horizontal line, Step 5c reflects across the vertical line. If both lines exist, these reflections populate the other quadrants based on the top-left source.)*
6.  **Refined approach for handling both lines:**
    a.  Find `hr` and `vc` as above.
    b.  If only `hr` exists: Perform vertical reflection as in step 4c.
    c.  If only `vc` exists: Perform horizontal reflection as in step 5c.
    d.  If both `hr` and `vc` exist:
        i.  Identify the top-left source region (rows `0` to `hr-1`, columns `0` to `vc-1`).
        ii. For each pixel `(r, c)` in the top-left source region:
            - Copy its color to the top-right reflected position `(r, vc + (vc - c))`.
            - Copy its color to the bottom-left reflected position `(hr + (hr - r), c)`.
            - Copy its color to the bottom-right reflected position `(hr + (hr - r), vc + (vc - c))`. Ensure all target coordinates are within the grid bounds.
7.  Return the modified output grid.