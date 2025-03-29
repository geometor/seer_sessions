## General Assessment

The previous code correctly identified shapes composed of a primary color and containing exactly one pixel of a different "marker" color. However, it failed to accurately implement the transformation rule observed in the examples. The primary issues were:

1.  **Incorrect Coloring:** The code colored almost the entire shape with the marker color, instead of just the pixels forming the diamond pattern.
2.  **Border Preservation:** The original border pixels of the shape were incorrectly modified, whereas the expected output shows they should retain their original primary color.
3.  **Interior Clearing:** The logic for clearing the interior pixels (those not part of the border and not part of the diamond pattern) was flawed, leading to incorrect pixels being set to white (0) or not being cleared when they should have been. The marker pixel itself also needs to be cleared.
4.  **Diamond Expansion Termination:** The condition for stopping the diamond expansion might have been incorrect, potentially expanding too far or stopping too early. The expansion should likely continue as long as the pattern intersects with the shape's original area and stop when it goes beyond or completely fills the available space within the border.

The strategy to resolve these errors involves:
1.  Explicitly identifying the border pixels of the shape.
2.  Refining the diamond pattern generation: color only the pixels on the diamond path that fall within the original shape's primary color area.
3.  Implementing the correct clearing logic: After drawing the diamond pattern, iterate through the shape's original primary-colored pixels. If a pixel is *not* on the border and *not* colored by the diamond pattern, set it to white (0). Also, set the original marker position to white (0).
4.  Ensuring the border pixels retain their original primary color throughout the process.

## Metrics and Analysis

Let's analyze the first example to illustrate the discrepancies and the required logic.

**Example 1 Input:**

```
. . . . . . . . . . . . . .
. . G G G G G G G G G . . .
. . G G G G G G G M G . . .  (M=Magenta=6 at (2,9), G=Green=3)
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
```


**Shape:** A green (3) rectangle from (1,2) to (10,10), containing a magenta (6) marker at (2,9).
**Primary Color:** Green (3)
**Marker Color:** Magenta (6)
**Marker Position:** (2, 9)

**Border Pixels:** These are the green pixels adjacent (N, S, E, W) to a non-green, non-magenta pixel (in this case, white=0 or outside the grid). This forms the outer perimeter of the green rectangle.

``` python
import numpy as np

grid_str = """
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 6 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
"""
grid = np.array([list(map(int, row.split())) for row in grid_str.strip().split('\n')])
height, width = grid.shape
shape_primary_coords = set()
marker_coord = None
primary_color = 3
marker_color = 6
for r in range(height):
    for c in range(width):
        if grid[r,c] == primary_color:
            shape_primary_coords.add((r,c))
        elif grid[r,c] == marker_color:
             marker_coord = (r,c)

border_coords = set()
for r, c in shape_primary_coords:
    is_border = False
    # Check 4 neighbors
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        # Check if neighbor is outside grid OR is not part of the shape's area (not primary color AND not the marker)
        if not (0 <= nr < height and 0 <= nc < width) or \
           (grid[nr, nc] != primary_color and (nr, nc) != marker_coord):
             is_border = True
             break
    if is_border:
        border_coords.add((r, c))

print(f"Example 1:")
print(f"Shape Primary Coords Count: {len(shape_primary_coords)}")
print(f"Border Coords Count: {len(border_coords)}")
print(f"Marker Coord: {marker_coord}")
print(f"Marker Color: {marker_color}")
print(f"Primary Color: {primary_color}")
```
```
Example 1:
Shape Primary Coords Count: 89
Border Coords Count: 34
Marker Coord: (2, 9)
Marker Color: 6
Primary Color: 3

```
**Diamond Pattern:** Expands from (2,9). Pixels at Manhattan distance `d` from (2,9) that were originally green (3) are colored magenta (6).
- d=1: (1,9), (3,9), (2,8), (2,10). All originally green.
- d=2: (0,9), (4,9), (1,8), (3,8), (1,10), (3,10), (2,7), (2,11). Check original color: (4,9)=3, (1,8)=3, (3,8)=3, (1,10)=3, (3,10)=3, (2,7)=3, (2,11)=3. (0,9) is 0.
- ...and so on. Expansion stops when the diamond layer has no intersection with the original green pixels.

**Expected Output Logic:**
1.  Start with the input grid.
2.  Identify the border pixels (34 green pixels). These remain green.
3.  Draw the magenta diamond pattern starting from (2,9). Only color pixels that were originally green. Keep track of pixels colored magenta.
4.  Iterate through the original 89 green pixels.
5.  If a green pixel is *not* a border pixel AND was *not* colored magenta by the diamond pattern, change it to white (0).
6.  Change the original marker pixel (2,9) to white (0).

**Comparison with Actual Output (Example 1):**
The actual output colored almost all original green pixels (and the marker location) magenta (6), indicating a failure in steps 3, 4, 5, and 6. It did not preserve the border and did not clear the correct interior pixels.

Similar analysis applies to Examples 2 and 3, showing the same pattern of failures: border not preserved, incorrect interior clearing, and over-coloring with the marker color.

## Fact Extraction


```yaml
Task: Draw a hollow diamond pattern inside marked shapes.

Input_Features:
  - Grids containing contiguous shapes of uniform color (primary_color), potentially embedded with pixels of other colors.
  - Background is white (0).
  - Shapes are defined by 4-directional connectivity of non-white pixels.

Output_Features:
  - Grids where specific shapes have been modified.
  - Shapes without a single, unique internal marker pixel remain unchanged.

Transformation_Objects:
  - Shape: A contiguous area of pixels sharing the same non-white color (primary_color).
  - Marker: A single pixel of a different color (marker_color) located within or adjacent to the primary_color pixels of a shape, such that the marker and the primary pixels form one connected component (including the marker).
  - Border: The subset of a shape's primary_color pixels that are adjacent (4-directionally) to pixels not belonging to that shape (background or another shape, excluding the marker pixel itself during adjacency check).
  - Interior: The subset of a shape's primary_color pixels that are not part of the Border.
  - Diamond_Pattern: A diamond shape (defined by Manhattan distance) centered at the Marker's position.

Actions:
  1. Identify: Find all connected components of non-white pixels.
  2. Analyze_Components: For each component, determine if it consists of a primary_color area and exactly one marker_color pixel.
  3. Identify_Border: For qualifying shapes, determine the Border pixels.
  4. Generate_Pattern: Create a Diamond_Pattern expanding outwards from the Marker position layer by layer (increasing Manhattan distance).
  5. Apply_Pattern: For each pixel generated by the Diamond_Pattern, if it falls within the shape's original primary_color area, change its color to the marker_color in the output grid. Keep track of pixels changed by the pattern.
  6. Preserve_Border: Ensure all identified Border pixels retain their original primary_color in the output grid.
  7. Clear_Interior: For all pixels originally belonging to the shape's primary_color area: if a pixel is not a Border pixel and was not colored by the Apply_Pattern step, change its color to white (0) in the output grid.
  8. Clear_Marker: Change the color of the original Marker pixel's location to white (0) in the output grid.
  9. No_Change: If a shape does not have exactly one marker, or if a component is just a single pixel or doesn't fit the criteria, leave it unchanged in the output grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected shapes in the input grid. A shape is a group of connected non-white pixels. Connectivity is 4-directional.
3.  For each shape found:
    a.  Count the occurrences of each color within the shape's pixels.
    b.  Determine the most frequent color; this is the `primary_color`.
    c.  Identify all pixels within the shape that do *not* have the `primary_color`. These are potential `marker` pixels.
    d.  Check if there is exactly one `marker` pixel within the shape.
    e.  If there is exactly one `marker` pixel (with `marker_color` at `marker_coord`):
        i.  Identify the set of pixels belonging to the shape that have the `primary_color` (`primary_pixels`).
        ii. Identify the `border_pixels`: the subset of `primary_pixels` where at least one 4-directionally adjacent neighbor is either outside the grid boundaries or has a color different from `primary_color` and is not the `marker_coord`.
        iii. Initialize an empty set `pattern_pixels` to store coordinates colored by the diamond pattern.
        iv. Expand a diamond pattern outwards from `marker_coord`, layer by layer based on Manhattan distance `d` (starting with `d=1`).
        v.  For each distance `d`:
            1.  Generate all coordinates `(r, c)` that are exactly Manhattan distance `d` away from `marker_coord`.
            2.  Track if any pixels are colored in this layer (`colored_this_layer = false`).
            3.  For each generated coordinate `(r, c)`:
                a.  Check if `(r, c)` is within the grid boundaries.
                b.  Check if `(r, c)` is in the set `primary_pixels`.
                c.  If both conditions are true, change the color of `(r, c)` in the output grid to `marker_color`, add `(r, c)` to `pattern_pixels`, and set `colored_this_layer = true`.
            4.  If `colored_this_layer` is false after checking all coordinates at distance `d`, stop the diamond expansion. Otherwise, increment `d` and continue to the next layer.
        vi. Iterate through all coordinates `(r, c)` in the original `primary_pixels` set.
        vii. If `(r, c)` is *not* in `border_pixels` AND `(r, c)` is *not* in `pattern_pixels`, change the color of `(r, c)` in the output grid to white (0).
        viii. Change the color of the original `marker_coord` in the output grid to white (0).
    f.  If the shape does not have exactly one marker, leave it unchanged in the output grid.
4.  Return the modified output grid.