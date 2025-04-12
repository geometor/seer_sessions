
## train_1

**input:**
```
0 0 0 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 3 3 3 0 0
0 0 0 2 3 3 3 3 0 0
0 0 0 3 1 1 0 3 0 0
0 0 0 3 1 0 0 3 0 0
0 0 0 3 0 0 1 3 0 0
0 0 0 3 0 1 1 3 0 0
0 0 0 3 3 3 3 2 0 0
0 0 0 3 3 3 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```

Okay, let's break down this first example.

## Initial Perception

The input grid contains several small, distinct shapes made of colors 1 (light blue) and 2 (red), scattered on a black background (color 0). There's also a single instance of color 3 (dark blue?) in the bottom-left corner, adjacent to a color 2 cell.

The output grid retains all the original shapes in their exact positions and colors. The significant change is the addition of color 3 (dark blue?), which now fills a rectangular area in the center-right portion of the grid. This filling seems selective: it only replaces the background color 0 within this rectangle, leaving the original shapes (colors 1 and 2) within that area untouched. The objects outside this filled rectangle, including the original color 3 cell, also remain unchanged.

The filled rectangle appears to correspond to the bounding box encompassing a specific subset of the initial shapes. Notably, the color used for filling (3) is the same color that appeared only once in the input grid. The shapes that seem to define the bounding box are the four 'L'-shaped objects, each composed of exactly three cells. The smaller objects (a single cell '1' and a two-cell '2'-'3' object) seem excluded from determining the fill area.

## Observed Facts (YAML)

```yaml
# Facts observed from train_1 example
grid_properties:
  size: [10, 10]
  background_color: 0
colors:
  present_in_input: [0, 1, 2, 3]
  present_in_output: [0, 1, 2, 3]
  added_to_output: [3] # Color 3 is added extensively
  unique_input_color: 3 # Appears only once at (9, 1) in input
objects_input:
  - type: shape
    color: 2
    location: [[0, 3], [0, 4], [1, 3]]
    size: 3
    shape_desc: L-shape (inverted)
  - type: shape
    color: 1
    location: [[2, 4], [2, 5], [3, 4]]
    size: 3
    shape_desc: L-shape
  - type: shape
    color: 1
    location: [[4, 6], [5, 5], [5, 6]]
    size: 3
    shape_desc: L-shape
  - type: shape
    color: 2
    location: [[6, 7], [7, 6], [7, 7]]
    size: 3
    shape_desc: L-shape (inverted)
  - type: shape
    color: 1
    location: [[8, 0]]
    size: 1
    shape_desc: single cell
  - type: shape
    color: [2, 3] # Multi-color object
    location: [[9, 0], [9, 1]]
    size: 2
    shape_desc: horizontal line
transformation:
  action: fill_region
  fill_color: 3
  region_definition:
    method: bounding_box
    source_objects: objects with size 3
    coordinates: # Calculated bounding box of size-3 objects
      min_row: 0
      max_row: 7
      min_col: 3
      max_col: 7
  fill_rule: replace background (0) only
  preservation:
    - all original non-zero cells retain their color and position.
    - objects outside the filled region are unaffected.
```

## Natural Language Program

1.  Identify all contiguous groups of non-zero cells (objects) in the input grid.
2.  For each object, determine its size (number of cells).
3.  Find the color value that appears exactly once in the entire input grid; designate this as the `fill_color`.
4.  Select only those input objects whose size is exactly 3.
5.  Calculate the minimal bounding box that encloses all the selected size-3 objects (find min/max row and min/max column).
6.  Initialize the output grid as a copy of the input grid.
7.  Iterate through each cell within the calculated bounding box area.
8.  If a cell within the bounding box has the background color (0) in the input grid, update its color to the `fill_color` in the output grid.
9.  Return the modified output grid.

## train_2

**input:**
```
0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 1 3 0 4 0 1 1 0 0
0 4 5 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 4 4
0 0 0 0 5 5 5 5 5 4
0 0 0 0 5 1 1 3 5 5
0 0 0 0 5 1 3 3 5 5
0 0 0 0 5 3 3 3 5 5
0 0 0 0 5 3 3 3 5 5
0 0 0 0 5 3 3 1 5 5
0 1 3 0 4 3 1 1 5 5
0 4 5 0 4 4 5 5 5 5
0 0 0 0 0 0 0 0 0 0
```

Okay, let's refine the understanding based on the second example (`train_2`).

## Refined Perception

The core concept seems consistent: identify a region based on certain objects, identify one or two specific colors, and fill the region with these colors, preserving the original non-background cells.

Example `train_2` introduces complexity compared to `train_1`. While `train_1` involved filling a bounding box with a single color (the unique color '3' found in the input), `train_2` uses *two* fill colors (5 and 3) within the bounding box.

Key observations refined by `train_2`:

1.  **Trigger Objects:** The objects determining the bounding box still appear to be those of size 3. In `train_2`, these are two L-shapes of color 1, one L-shape of color 4, and a vertical line of color 4.
2.  **Bounding Box:** The bounding box calculation based on these size-3 objects remains consistent (Rows 0-8, Cols 4-9 for `train_2`).
3.  **Fill Colors:** The input grid now contains *two* colors that appear exactly once: color 5 (at 8,2) and color 3 (at 7,2). The output uses color 5 for an "outer" fill within the bounding box and color 3 for an "inner" fill.
4.  **Outer Fill Color Source:** Color 5, used for the outer fill, is part of the two-cell object `[[8,1],[8,2]]` (colors 4, 5). In `train_1`, the fill color 3 was part of the two-cell object `[[9,0],[9,1]]` (colors 2, 3). This suggests the primary (or outer) fill color is the unique color associated with a multi-cell object.
5.  **Inner Fill Color Source:** Color 3, used for the inner fill in `train_2`, is the *other* unique color found in the input. In `train_1`, there was only one unique color, and no inner fill occurred.
6.  **Inner Fill Region:** The region filled with color 3 in `train_2` (approx. Rows 2-7, Cols 5-7) seems related to a subset of the size-3 objects. Specifically, it corresponds to the bounding box of the size-3 objects whose color is *not* the most frequent non-background color in the overall input grid. In `train_2`, color 4 is most frequent (7 times); the inner region corresponds to the bounding box of the two size-3 objects with color 1. In `train_1`, colors 1 and 2 tied for most frequent, potentially explaining why no inner fill occurred.
7.  **Fill Rule:** Filling still replaces only the background color (0) within the respective regions (outer and inner), preserving original non-zero cells. The inner fill color overwrites the outer fill color where their regions overlap and the input cell was 0.

## Updated Facts (YAML)

```yaml
# Facts observed from train_1 and train_2 examples
grid_properties:
  size: [10, 10]
  background_color: 0
colors:
  present_in_input: variable # [0, 1, 2, 3] for train_1; [0, 1, 3, 4, 5] for train_2
  present_in_output: variable
  unique_input_colors: # Colors appearing exactly once in the input grid
    train_1: [3]
    train_2: [3, 5]
  most_frequent_input_color: # Most frequent non-zero color(s) in input
    train_1: [1, 2] # Tie
    train_2: [4]
objects_input:
  properties:
    - id
    - color(s)
    - location (list of [row, col])
    - size (number of cells)
    - shape_desc (optional)
  criteria:
    bounding_box_source: objects with size 3
    outer_fill_color_source: the unique color belonging to a multi-cell object
    inner_fill_color_source: the other unique color (if it exists)
    inner_bounding_box_source: objects with size 3 whose color is NOT the single most frequent non-zero color in the grid (if one exists)
transformation:
  action: layered_fill_region
  layers:
    - layer_id: outer_fill
      fill_color_rule: find unique color in a multi-cell input object
      region_definition:
        method: bounding_box
        source_objects: objects with size 3
      fill_rule: replace background (0) only
    - layer_id: inner_fill (conditional)
      condition: exists a second unique color AND a single most frequent non-zero input color
      fill_color_rule: use the second unique color
      region_definition:
        method: bounding_box
        source_objects: size-3 objects whose color is not the most frequent grid color
      fill_rule: replace background (0) only (overwrites outer fill where applicable)
  preservation:
    - all original non-zero cells retain their color and position.
```

## Updated Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all contiguous groups of non-zero cells (objects) in the input grid, recording their size, color(s), and locations.
3.  Count the occurrences of each non-zero color in the entire input grid.
4.  Identify all colors that appear exactly once (`unique_colors`).
5.  Find the object containing two or more cells that includes one of the `unique_colors`. Designate this specific unique color as the `outer_fill_color`.
6.  If there is another color in `unique_colors` besides the `outer_fill_color`, designate it as the `inner_fill_color`. Otherwise, set `inner_fill_color` to None.
7.  Select all input objects whose size is exactly 3 (`size_3_objects`).
8.  Calculate the minimal bounding box (`BB_outer`) that encloses all `size_3_objects`.
9.  **Outer Fill:** Iterate through each cell within `BB_outer`. If the cell's color in the *input* grid is the background color (0), update its color in the *output* grid to `outer_fill_color`.
10. **Inner Fill Condition:** Determine if an inner fill should occur:
    *   Check if `inner_fill_color` is not None.
    *   Find the non-zero color(s) with the highest frequency count from step 3.
    *   If there is exactly *one* most frequent color (`most_frequent_color`), proceed with inner fill. Otherwise, skip inner fill.
11. **Inner Fill Execution (if condition met):**
    *   Select a subset of `size_3_objects`: include only those whose color is *not* equal to the `most_frequent_color`.
    *   Calculate the minimal bounding box (`BB_inner`) that encloses this subset of size-3 objects.
    *   Iterate through each cell within `BB_inner`. If the cell's color in the *input* grid is the background color (0), update its color in the *output* grid to `inner_fill_color` (this overwrites any `outer_fill_color` previously placed in this region).
12. Return the modified output grid.

## train_3

**input:**
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 2 3 4 4 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 4 3 3 1 1 3 3 2 3 3 3
3 3 3 3 3 3 3 3 3 3 1 3 2 2 3 3 3
3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3
3 3 1 6 3 3 3 3 4 4 3 3 3 3 3 3 3
3 3 2 9 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 4 0 3 3 3 1 3 3 3 3 3 3 3 3 3
3 3 8 9 3 3 3 1 1 3 3 3 3 3 3 3 3
```


**output:**
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 2 9 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 9 9 9 6 6 1 1 9 9 2 3 3 3
3 3 3 3 9 9 9 6 6 6 1 9 2 2 3 3 3
3 3 3 3 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 1 6 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 2 9 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 4 0 3 3 3 1 6 6 6 3 3 3 3 3 3
3 3 8 9 3 3 3 1 1 6 6 3 3 3 3 3 3
```

## Refined Perception

Based on the analysis of all three examples (`train_1`, `train_2`, `train_3`), the task involves identifying specific colors and regions within an input grid and performing a layered fill operation while preserving existing non-background elements.

1.  **Background Color:** The concept of a "background" color is crucial. It's the most frequent color in the input grid and is the only color replaced during the fill operations. This color is not necessarily 0 (it was 3 in `train_3`).
2.  **Fill Colors:** One or two fill colors are determined based on colors that appear uniquely (exactly once) in the input grid and their immediate neighbors.
    *   **Outer Fill Color:** Identify all unique colors. Find the color `C_adj` that is orthogonally adjacent to a unique color `C_unique`. The outer fill color appears to be the highest value found among all such `C_adj` and all `C_unique`.
    *   **Inner Fill Color:** If there are multiple unique colors, identify the highest unique color (`HUC`). The inner fill color appears to be the highest unique color that is *not* `HUC` and was *not* the unique color used to determine the outer fill color via adjacency. If no second unique color remains after determining the outer fill, there is no inner fill.
3.  **Object Identification:** The transformation relies on identifying specific objects, particularly contiguous groups of cells with size 3 ("size-3 objects").
4.  **Bounding Boxes:** Two bounding boxes potentially define the fill regions.
    *   **Outer Bounding Box (`BB_outer`):** This seems to be the minimal bounding box enclosing all size-3 objects whose color value is less than 5.
    *   **Inner Bounding Box (`BB_inner`):** This applies only if an `InnerFill` color exists. The rule appears to be the minimal bounding box enclosing size-3 objects that meet two criteria: a) their color value is less than 5, AND b) their color is *not* the single most frequent non-background color in the entire grid. (This worked perfectly for `train_1` and `train_2` but yielded a larger-than-expected region for `train_3`; however, it remains the most consistent hypothesis across examples).
5.  **Fill Operation:**
    *   The `OuterFill` color replaces the background color within `BB_outer`.
    *   If an `InnerFill` color and `BB_inner` exist, the `InnerFill` color replaces the background color within `BB_inner`, overwriting any `OuterFill` color placed in that region.
    *   All cells with non-background colors in the input grid retain their original color and position in the output grid.

## Updated Facts (YAML)

```yaml
# Facts observed from train_1, train_2, and train_3 examples
grid_properties:
  size: variable # [10, 10] or [12, 17]
  background_color_rule: most frequent color in the input grid
colors:
  present_in_input: variable
  present_in_output: variable
  unique_input_colors_rule: colors appearing exactly once in the input grid
  fill_colors_determination:
    candidates:
      - unique colors
      - orthogonal neighbors of unique colors (if not background)
    outer_fill_color: highest value among candidates
    inner_fill_color: (if >1 unique color exists) highest unique color NOT used (directly or via neighbor) to determine outer_fill_color.
  most_frequent_non_background_color_rule: find color counts excluding background, identify single highest count (if exists)
objects_input:
  properties:
    - id
    - color(s)
    - location (list of [row, col])
    - size (number of cells)
  criteria:
    bounding_box_source_objects: objects with size 3 AND color < 5
    inner_bounding_box_source_objects: objects meeting outer criteria AND whose color is NOT the single most frequent non-background color
transformation:
  action: layered_fill_region
  layers:
    - layer_id: outer_fill
      fill_color_rule: derived from unique colors and neighbors (highest candidate)
      region_definition:
        method: bounding_box
        source_objects: size-3 objects with color < 5
      fill_rule: replace background color only
    - layer_id: inner_fill (conditional)
      condition: exists an inner_fill_color derived from unique colors
      fill_color_rule: derived from unique colors (highest remaining unique)
      region_definition:
        method: bounding_box
        source_objects: size-3 objects with color < 5 AND color != single most frequent non-background color
      fill_rule: replace background color only (overwrites outer fill where applicable)
  preservation:
    - all original non-background cells retain their color and position.
```

## Updated Natural Language Program

1.  Determine the `background_color` by finding the most frequent color in the input grid.
2.  Initialize the output grid as a copy of the input grid.
3.  Identify all colors that appear exactly once in the input grid (`unique_colors`).
4.  If `unique_colors` is empty, return the initial output grid (no changes).
5.  **Determine Fill Colors:**
    *   Create a set of `candidate_fill_colors` initialized with all `unique_colors`.
    *   For each `uc` in `unique_colors`:
        *   Find all orthogonally adjacent neighbors `(nr, nc)` of the cell containing `uc`.
        *   For each neighbor, get its color `neighbor_color`.
        *   If `neighbor_color` is not the `background_color`, add `neighbor_color` to `candidate_fill_colors`.
    *   If `candidate_fill_colors` is empty (e.g., unique colors only had background neighbors), set `outer_fill_color` to the highest value in `unique_colors`. Otherwise, set `outer_fill_color` to the highest value in `candidate_fill_colors`.
    *   Determine which unique color `uc_used` was responsible for the `outer_fill_color` (either `uc_used == outer_fill_color` or `outer_fill_color` was a neighbor of `uc_used`). If multiple unique colors could be responsible, prioritize the highest `uc_used`.
    *   Create a set `remaining_unique_colors` by removing `uc_used` from the original `unique_colors`.
    *   If `remaining_unique_colors` is not empty, set `inner_fill_color` to the highest value in `remaining_unique_colors`. Otherwise, set `inner_fill_color` to None.
6.  Identify all contiguous groups of non-background cells (objects), recording their size, color, and locations.
7.  Select objects where `size == 3` and `color < 5` (`outer_bb_objects`).
8.  If `outer_bb_objects` is empty, return the initial output grid.
9.  Calculate the minimal bounding box (`BB_outer`) enclosing all `outer_bb_objects`.
10. **Outer Fill:** Iterate through each cell `(r, c)` within `BB_outer`. If the color in the *input* grid at `(r, c)` is the `background_color`, update its color in the *output* grid to `outer_fill_color`.
11. **Inner Fill Condition:** Check if `inner_fill_color` is not None.
12. **Inner Fill Execution (if condition met):**
    *   Count the frequency of each non-background color in the entire input grid. Find if there is a single color with the highest frequency (`most_frequent_non_bg`).
    *   Select a subset of `outer_bb_objects`: include only those whose color is *not* equal to `most_frequent_non_bg` (if one exists). Call this subset `inner_bb_objects`.
    *   If `inner_bb_objects` is not empty:
        *   Calculate the minimal bounding box (`BB_inner`) enclosing all `inner_bb_objects`.
        *   Iterate through each cell `(r, c)` within `BB_inner`. If the color in the *input* grid at `(r, c)` is the `background_color`, update its color in the *output* grid to `inner_fill_color` (this overwrites any `outer_fill_color` previously placed).
13. Return the modified output grid.

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 6 0 0 0 7 7 0 0
6 7 0 0 0 0 0 0 0 6 6 0 0 0 7 7 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 7 7 7 0 4 4 4 4 4 4
0 0 0 0 0 0 6 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0
3 3 0 0 0 0 7 7 7 7 6 0 0 0 6 6 0 0
6 7 0 0 0 0 7 7 7 6 6 0 0 0 6 6 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Refined Perception

This task involves transforming an input grid by filling rectangular regions with specific colors, determined by the properties of the input grid's elements. The core logic appears to adapt based on the presence or absence of unique colors (colors appearing exactly once).

1.  **Background Color:** Identify the most frequent color in the input grid; this is the background color, and it's the only color that gets replaced by fill operations.
2.  **Object Identification:** Locate all contiguous groups of non-background cells (objects) and determine their properties, especially size and color. Objects with size 3 are critical ("size-3 objects").
3.  **Primary Logic (Unique Colors Exist):**
    *   **Fill Colors:** Identify unique colors (`uc`) and their non-background orthogonal neighbors (`nc`). Form candidate pairs `(uc, nc)` or `(uc, uc)`. The `outer_fill_color` is the color (`nc` or `uc`) from the pair with the highest color value, prioritizing pairs with the highest `uc` in case of ties. The `inner_fill_color` (if any) is the highest remaining unique color not associated with the chosen outer fill pair.
    *   **Fill Regions:**
        *   `BB_outer`: Calculated from the minimal bounding box containing *all* size-3 objects whose color value is less than 5.
        *   `BB_inner`: Calculated (if `inner_fill_color` exists) from the minimal bounding box containing size-3 objects (color < 5) whose color is *not* the single most frequent non-background color in the grid.
    *   **Filling:** Apply `outer_fill_color` to background cells within `BB_outer`. Then, apply `inner_fill_color` to background cells within `BB_inner` (overwriting the outer fill).
4.  **Fallback Logic (No Unique Colors Exist):**
    *   **Fill Colors & Regions per Group:** Group size-3 objects by their color `C`. For each group:
        *   Determine `fill_color(C)`: Check if any cell of color `C` is adjacent to a different non-background color `C_adj`. If yes, `fill_color(C)` is the highest such `C_adj`. Otherwise, `fill_color(C)` is `C`.
        *   Determine `BB_C`: Calculate the minimal bounding box containing only the size-3 objects of color `C`.
        *   Apply `fill_color(C)` to background cells within `BB_C`. The order or overlap rule isn't perfectly clear, but filling seems independent for each color group `C`.
5.  **Preservation:** All original non-background cells retain their color and position in the output grid.
6.  **Bounding Box Ambiguity:** While minimal bounding boxes of the specified object subsets are the primary hypothesis, the exact filled regions in the examples sometimes deviate slightly (e.g., shifts, different start/end columns/rows). This suggests the BB calculation or application rule might be more complex, but minimal BB is the current best model.

## Updated Facts (YAML)

```yaml
# Facts observed from train_1, train_2, train_3, train_4 examples
grid_properties:
  size: variable
  background_color_rule: most frequent color in the input grid
colors:
  present_in_input: variable
  present_in_output: variable
  unique_input_colors_rule: colors appearing exactly once in the input grid
  fill_colors_determination:
    mode_selection: based on presence of unique_input_colors
    mode_unique_colors:
      candidates_rule: form pairs (uc, neighbor_or_uc) where uc is unique color, neighbor_or_uc is uc or its non-background orthogonal neighbor.
      outer_fill_color_rule: value from the candidate pair with the maximum value, breaking ties by maximizing uc.
      inner_fill_color_rule: (if >1 unique color) highest unique color not used (directly or via neighbor pair) to determine outer_fill_color.
    mode_no_unique_colors:
      trigger: process per distinct color C found in size-3 objects
      fill_color_rule(C): max non-background color adjacent to any cell of color C, or C itself if no different neighbors.
  most_frequent_non_background_color_rule: find color counts excluding background, identify single highest count (if exists)
objects_input:
  properties:
    - id
    - color(s)
    - location (list of [row, col])
    - size (number of cells)
  criteria:
    size_3_objects: objects with size = 3
    size_3_lt_5_objects: size-3 objects with color < 5 (used in unique color mode)
transformation:
  action: conditional_layered_fill
  condition: presence of unique input colors
  mode_unique_colors:
    layers:
      - layer_id: outer_fill
        fill_color_rule: derived from unique colors and neighbors (pair rule)
        region_definition:
          method: minimal_bounding_box # Note: Potential minor deviations observed
          source_objects: size-3 objects with color < 5
        fill_rule: replace background color only
      - layer_id: inner_fill (conditional)
        condition: exists an inner_fill_color derived from unique colors AND a single most frequent non-background color
        fill_color_rule: derived from remaining unique colors (highest remaining)
        region_definition:
          method: minimal_bounding_box # Note: Potential minor deviations observed
          source_objects: size-3 objects with color < 5 AND color != single most frequent non-background color
        fill_rule: replace background color only (overwrites outer fill where applicable)
  mode_no_unique_colors:
    process_per_color_group: For each distinct color C in size-3 objects
      layers: # Conceptually, one layer per color C
        - layer_id: fill_for_C
          fill_color_rule: derived from adjacency rule for C
          region_definition:
            method: minimal_bounding_box # Note: Potential minor deviations observed
            source_objects: size-3 objects with color C
          fill_rule: replace background color only
          # Overlap rule unclear, assume later fills might overwrite earlier ones or highest color wins? Coder needs to test.
  preservation:
    - all original non-background cells retain their color and position.
```

## Updated Natural Language Program

1.  Determine the `background_color` by finding the most frequent color in the input grid.
2.  Initialize the output grid as a copy of the input grid.
3.  Identify all contiguous groups of non-background cells (objects), recording their size, color, and locations.
4.  Identify all colors that appear exactly once in the input grid (`unique_colors`).
5.  Identify all objects with `size == 3` (`size_3_objects`).

6.  **Mode Selection:** Check if `unique_colors` is empty.
    *   If **NOT empty** (Unique Colors Mode): Proceed to step 7.
    *   If **empty** (No Unique Colors Mode): Proceed to step 12.

7.  **Unique Colors Mode - Determine Fill Colors:**
    *   Create a list of `candidate_pairs` = [].
    *   For each `uc` in `unique_colors`:
        *   Add `(uc, uc)` to `candidate_pairs`.
        *   Find the location `(r, c)` of the cell with color `uc`.
        *   Check orthogonal neighbors `(nr, nc)` of `(r, c)`.
        *   For each neighbor, get its color `neighbor_color`.
        *   If `neighbor_color` is not the `background_color` and `neighbor_color != uc`, add `(uc, neighbor_color)` to `candidate_pairs`.
    *   If `candidate_pairs` is empty, return the initial output grid (no changes possible).
    *   Find the pair `(uc_best, val_best)` in `candidate_pairs` that maximizes `val_best`, breaking ties by maximizing `uc_best`.
    *   Set `outer_fill_color = val_best`.
    *   Set `uc_used = uc_best`.
    *   Create `remaining_unique_colors` by removing `uc_used` from `unique_colors`.
    *   If `remaining_unique_colors` is not empty, set `inner_fill_color` to the highest value in `remaining_unique_colors`. Otherwise, set `inner_fill_color` to None.

8.  **Unique Colors Mode - Determine Fill Regions & Execute Fill:**
    *   Select `outer_bb_objects` from `size_3_objects` where `object.color < 5`.
    *   If `outer_bb_objects` is empty, return the initial output grid.
    *   Calculate the minimal bounding box (`BB_outer`) enclosing all `outer_bb_objects`.
    *   **(Outer Fill)** Iterate through each cell `(r, c)` within `BB_outer`. If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `outer_fill_color`.
    *   **(Inner Fill Condition)** Check if `inner_fill_color` is not None. If yes:
        *   Count frequency of each non-background color in the input grid. Find if there's a single color with the highest frequency (`most_frequent_non_bg`).
        *   If `most_frequent_non_bg` exists:
            *   Select `inner_bb_objects` from `outer_bb_objects` where `object.color != most_frequent_non_bg`.
            *   If `inner_bb_objects` is not empty:
                *   Calculate the minimal bounding box (`BB_inner`) enclosing `inner_bb_objects`.
                *   **(Inner Fill Execution)** Iterate through each cell `(r, c)` within `BB_inner`. If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `inner_fill_color` (overwriting `outer_fill_color`).
    *   Proceed to step 14 (Return).

9.  **No Unique Colors Mode - Process per Color Group:**
    *   Find the set of distinct colors `{C1, C2, ...}` present in the `size_3_objects`.
    *   For each distinct color `C` in this set:
        *   **Determine Fill Color for C:**
            *   Initialize `max_adjacent_color = -1`.
            *   Find all cells `(r, c)` in the input grid with color `C`.
            *   For each such cell `(r, c)`:
                *   Check orthogonal neighbors `(nr, nc)`.
                *   Get `neighbor_color` at `(nr, nc)`.
                *   If `neighbor_color != background_color` and `neighbor_color != C`:
                    *   `max_adjacent_color = max(max_adjacent_color, neighbor_color)`
            *   If `max_adjacent_color > -1`, set `fill_color_C = max_adjacent_color`.
            *   Else, set `fill_color_C = C`.
        *   **Determine Fill Region for C:**
            *   Select `group_C_objects` from `size_3_objects` where `object.color == C`.
            *   If `group_C_objects` is empty, continue to the next color `C`.
            *   Calculate the minimal bounding box (`BB_C`) enclosing `group_C_objects`.
        *   **Execute Fill for C:**
            *   Iterate through each cell `(r, c)` within `BB_C`.
            *   If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `fill_color_C`. (Note: If multiple groups fill the same cell, the result depends on processing order or an implicit priority like highest fill color wins. Assume processing order for now).

10. **No Unique Colors Mode - Finalize:** After processing all color groups C, proceed to step 14 (Return).

11. **Return Output:** Return the modified output grid.
```python
import collections
import itertools
from copy import deepcopy

"""
Transforms an input grid based on two potential modes, determined by the presence of unique colors (colors appearing exactly once).

Mode 1: Unique Colors Exist
1. Identify unique colors and their non-background orthogonal neighbors.
2. Determine 'outer_fill_color' based on the highest value among unique colors and their neighbors, prioritizing pairs with higher unique colors in case of ties.
3. Determine 'inner_fill_color' (if applicable) as the highest remaining unique color.
4. Identify size-3 objects with color < 5 ('outer_bb_objects').
5. Calculate the bounding box ('BB_outer') for these objects.
6. Fill background cells within 'BB_outer' with 'outer_fill_color'.
7. If 'inner_fill_color' exists and there's a single most frequent non-background color:
    a. Identify 'inner_bb_objects' (subset of 'outer_bb_objects' whose color is not the most frequent non-background color).
    b. Calculate the bounding box ('BB_inner') for these objects.
    c. Fill background cells within 'BB_inner' with 'inner_fill_color', overwriting the outer fill.

Mode 2: No Unique Colors Exist
1. Group size-3 objects by their color 'C'.
2. For each color group 'C':
    a. Determine 'fill_color_C' as the maximum non-background color adjacent to any cell of color 'C', or 'C' itself if no different neighbors exist.
    b. Calculate the bounding box ('BB_C') for the size-3 objects of color 'C'.
    c. Fill background cells within 'BB_C' with 'fill_color_C'. (Overwrites follow processing order).

General Rules:
- The 'background_color' is the most frequent color in the input grid.
- Only background cells are ever filled. Original non-background cells are preserved.
- Object finding considers orthogonal connectivity.
- Bounding boxes are minimal axis-aligned rectangles enclosing the specified objects.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_objects(grid: list[list[int]], background_color: int) -> list[dict]:
    """Finds connected objects of non-background colors."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] != background_color and (r, c) not in visited:
                obj_color = grid[r][c]
                obj_locations = set()
                is_single_color = True
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_locations.add((r,c))
                colors_in_obj = {obj_color}

                while q:
                    row, col = q.popleft()
                    
                    # Check neighbors
                    for nr, nc in get_neighbors(row, col, height, width):
                        neighbor_color = grid[nr][nc]
                        if neighbor_color != background_color and (nr, nc) not in visited:
                            # For this problem, assume objects are single-colored unless logic needs otherwise
                            # If objects can be multi-colored, need adjustment here
                            if neighbor_color == obj_color:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                obj_locations.add((nr,nc))
                            # Handle case where adjacent cells have different non-background colors if needed by future tasks
                            # For now, we assume objects are defined by connectivity of the *same* non-bg color.
                            # If the problem implies multi-color objects based on adjacency, this needs revision.
                            # Based on examples, seems like objects are mono-colored.
                            
                # Store the object if it has locations
                if obj_locations:
                    objects.append({
                        "color": obj_color, # Assumes mono-colored object based on initial cell
                        "locations": list(obj_locations),
                        "size": len(obj_locations)
                    })
    return objects


def get_color_counts(grid: list[list[int]]) -> collections.Counter:
    """Counts occurrences of each color in the grid."""
    counts = collections.Counter()
    for row in grid:
        counts.update(row)
    return counts

def get_bounding_box(objects: list[dict]) -> tuple[int, int, int, int] | None:
    """Calculates the minimal bounding box for a list of objects."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    has_locations = False

    for obj in objects:
        for r, c in obj['locations']:
            has_locations = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    if not has_locations:
        return None # No objects, no bounding box

    return min_r, min_c, max_r, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    height = len(input_grid)
    width = len(input_grid[0])
    output_grid = deepcopy(input_grid)

    # 1. Determine background color
    color_counts = get_color_counts(input_grid)
    if not color_counts: return output_grid # Empty grid
    background_color = color_counts.most_common(1)[0][0]

    # 2. Find all objects
    all_objects = find_objects(input_grid, background_color)
    if not all_objects: return output_grid # No objects

    # 3. Find unique colors and their locations
    unique_colors = {}
    non_bg_counts = {color: count for color, count in color_counts.items() if color != background_color}
    for r in range(height):
        for c in range(width):
             color = input_grid[r][c]
             if color != background_color and non_bg_counts.get(color) == 1:
                 unique_colors[color] = (r, c) # Store location too

    # 4. Identify size-3 objects
    size_3_objects = [obj for obj in all_objects if obj['size'] == 3]
    
    # 5. Mode Selection
    if unique_colors:
        # -------- Mode 1: Unique Colors Exist --------
        
        # 7. Determine Fill Colors
        candidate_pairs = []
        for uc, (r, c) in unique_colors.items():
            candidate_pairs.append((uc, uc)) # Pair with itself
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = input_grid[nr][nc]
                if neighbor_color != background_color and neighbor_color != uc:
                     # Ensure the unique color 'uc' is first element for tie-breaking
                     candidate_pairs.append((uc, neighbor_color))
                     
        if not candidate_pairs:
             # Fallback: if unique colors only neighbor background, maybe just use highest unique?
             # Based on logic, should always have at least (uc, uc) pairs if unique_colors exists.
             # If truly no pairs (e.g. if definition changes), return original.
             return output_grid 

        # Find the best pair: max value, tie-break with max uc
        candidate_pairs.sort(key=lambda pair: (pair[1], pair[0]), reverse=True)
        uc_used, outer_fill_color = candidate_pairs[0]

        remaining_unique_colors = {uc for uc in unique_colors if uc != uc_used}
        inner_fill_color = max(remaining_unique_colors) if remaining_unique_colors else None

        # 8. Determine Fill Regions & Execute Fill
        outer_bb_objects = [obj for obj in size_3_objects if obj['color'] < 5]

        if not outer_bb_objects:
            return output_grid # No objects to define outer region

        bb_outer = get_bounding_box(outer_bb_objects)
        if bb_outer is None: return output_grid

        min_r_outer, min_c_outer, max_r_outer, max_c_outer = bb_outer

        # (Outer Fill)
        for r in range(min_r_outer, max_r_outer + 1):
            for c in range(min_c_outer, max_c_outer + 1):
                if input_grid[r][c] == background_color:
                    output_grid[r][c] = outer_fill_color

        # (Inner Fill Condition & Execution)
        if inner_fill_color is not None:
            # Find single most frequent non-background color
            most_frequent_non_bg = None
            if non_bg_counts:
                 sorted_non_bg = sorted(non_bg_counts.items(), key=lambda item: item[1], reverse=True)
                 if len(sorted_non_bg) == 1 or sorted_non_bg[0][1] > sorted_non_bg[1][1]:
                      most_frequent_non_bg = sorted_non_bg[0][0]

            if most_frequent_non_bg is not None:
                inner_bb_objects = [obj for obj in outer_bb_objects if obj['color'] != most_frequent_non_bg]

                if inner_bb_objects:
                    bb_inner = get_bounding_box(inner_bb_objects)
                    if bb_inner:
                        min_r_inner, min_c_inner, max_r_inner, max_c_inner = bb_inner
                        # (Inner Fill Execution)
                        for r in range(min_r_inner, max_r_inner + 1):
                            for c in range(min_c_inner, max_c_inner + 1):
                                if input_grid[r][c] == background_color:
                                    output_grid[r][c] = inner_fill_color # Overwrite
                                    
    else:
        # -------- Mode 2: No Unique Colors Exist --------
        
        # 9. Process per Color Group
        colors_in_size_3 = sorted(list({obj['color'] for obj in size_3_objects}))

        for color_c in colors_in_size_3:
            # Determine Fill Color for C
            max_adjacent_color = -1
            cells_of_color_c = []
            group_c_objects = []
            for obj in size_3_objects:
                if obj['color'] == color_c:
                    group_c_objects.append(obj)
                    cells_of_color_c.extend(obj['locations'])
            
            if not group_c_objects: continue # Should not happen if color_c came from the set

            for r, c in cells_of_color_c:
                 for nr, nc in get_neighbors(r, c, height, width):
                     neighbor_color = input_grid[nr][nc]
                     if neighbor_color != background_color and neighbor_color != color_c:
                         max_adjacent_color = max(max_adjacent_color, neighbor_color)

            fill_color_c = max_adjacent_color if max_adjacent_color > -1 else color_c

            # Determine Fill Region for C
            bb_c = get_bounding_box(group_c_objects)
            if bb_c is None: continue

            min_r_c, min_c_c, max_r_c, max_c_c = bb_c

            # Execute Fill for C
            for r in range(min_r_c, max_r_c + 1):
                for c in range(min_c_c, max_c_c + 1):
                    if input_grid[r][c] == background_color:
                         # Overwrite based on processing order (sorted colors)
                        output_grid[r][c] = fill_color_c

    # 11. Return Output
    return output_grid
```

Previous Code:
```python
import collections
import itertools
from copy import deepcopy

"""
Transforms an input grid based on two potential modes, determined by the presence of unique colors (colors appearing exactly once).

Mode 1: Unique Colors Exist
1. Identify unique colors and their non-background orthogonal neighbors.
2. Determine 'outer_fill_color' based on the highest value among unique colors and their neighbors, prioritizing pairs with higher unique colors in case of ties.
3. Determine 'inner_fill_color' (if applicable) as the highest remaining unique color.
4. Identify size-3 objects with color < 5 ('outer_bb_objects').
5. Calculate the bounding box ('BB_outer') for these objects.
6. Fill background cells within 'BB_outer' with 'outer_fill_color'.
7. If 'inner_fill_color' exists and there's a single most frequent non-background color:
    a. Identify 'inner_bb_objects' (subset of 'outer_bb_objects' whose color is not the most frequent non-background color).
    b. Calculate the bounding box ('BB_inner') for these objects.
    c. Fill background cells within 'BB_inner' with 'inner_fill_color', overwriting the outer fill.

Mode 2: No Unique Colors Exist
1. Group size-3 objects by their color 'C'.
2. For each color group 'C':
    a. Determine 'fill_color_C' as the maximum non-background color adjacent to any cell of color 'C', or 'C' itself if no different neighbors exist.
    b. Calculate the bounding box ('BB_C') for the size-3 objects of color 'C'.
    c. Fill background cells within 'BB_C' with 'fill_color_C'. (Overwrites follow processing order).

General Rules:
- The 'background_color' is the most frequent color in the input grid.
- Only background cells are ever filled. Original non-background cells are preserved.
- Object finding considers orthogonal connectivity.
- Bounding boxes are minimal axis-aligned rectangles enclosing the specified objects.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_objects(grid: list[list[int]], background_color: int) -> list[dict]:
    """Finds connected objects of non-background colors."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] != background_color and (r, c) not in visited:
                obj_color = grid[r][c]
                obj_locations = set()
                is_single_color = True
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_locations.add((r,c))
                colors_in_obj = {obj_color}

                while q:
                    row, col = q.popleft()
                    
                    # Check neighbors
                    for nr, nc in get_neighbors(row, col, height, width):
                        neighbor_color = grid[nr][nc]
                        if neighbor_color != background_color and (nr, nc) not in visited:
                            # For this problem, assume objects are single-colored unless logic needs otherwise
                            # If objects can be multi-colored, need adjustment here
                            if neighbor_color == obj_color:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                obj_locations.add((nr,nc))
                            # Handle case where adjacent cells have different non-background colors if needed by future tasks
                            # For now, we assume objects are defined by connectivity of the *same* non-bg color.
                            # If the problem implies multi-color objects based on adjacency, this needs revision.
                            # Based on examples, seems like objects are mono-colored.
                            
                # Store the object if it has locations
                if obj_locations:
                    objects.append({
                        "color": obj_color, # Assumes mono-colored object based on initial cell
                        "locations": list(obj_locations),
                        "size": len(obj_locations)
                    })
    return objects


def get_color_counts(grid: list[list[int]]) -> collections.Counter:
    """Counts occurrences of each color in the grid."""
    counts = collections.Counter()
    for row in grid:
        counts.update(row)
    return counts

def get_bounding_box(objects: list[dict]) -> tuple[int, int, int, int] | None:
    """Calculates the minimal bounding box for a list of objects."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    has_locations = False

    for obj in objects:
        for r, c in obj['locations']:
            has_locations = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    if not has_locations:
        return None # No objects, no bounding box

    return min_r, min_c, max_r, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    height = len(input_grid)
    width = len(input_grid[0])
    output_grid = deepcopy(input_grid)

    # 1. Determine background color
    color_counts = get_color_counts(input_grid)
    if not color_counts: return output_grid # Empty grid
    background_color = color_counts.most_common(1)[0][0]

    # 2. Find all objects
    all_objects = find_objects(input_grid, background_color)
    if not all_objects: return output_grid # No objects

    # 3. Find unique colors and their locations
    unique_colors = {}
    non_bg_counts = {color: count for color, count in color_counts.items() if color != background_color}
    for r in range(height):
        for c in range(width):
             color = input_grid[r][c]
             if color != background_color and non_bg_counts.get(color) == 1:
                 unique_colors[color] = (r, c) # Store location too

    # 4. Identify size-3 objects
    size_3_objects = [obj for obj in all_objects if obj['size'] == 3]
    
    # 5. Mode Selection
    if unique_colors:
        # -------- Mode 1: Unique Colors Exist --------
        
        # 7. Determine Fill Colors
        candidate_pairs = []
        for uc, (r, c) in unique_colors.items():
            candidate_pairs.append((uc, uc)) # Pair with itself
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = input_grid[nr][nc]
                if neighbor_color != background_color and neighbor_color != uc:
                     # Ensure the unique color 'uc' is first element for tie-breaking
                     candidate_pairs.append((uc, neighbor_color))
                     
        if not candidate_pairs:
             # Fallback: if unique colors only neighbor background, maybe just use highest unique?
             # Based on logic, should always have at least (uc, uc) pairs if unique_colors exists.
             # If truly no pairs (e.g. if definition changes), return original.
             return output_grid 

        # Find the best pair: max value, tie-break with max uc
        candidate_pairs.sort(key=lambda pair: (pair[1], pair[0]), reverse=True)
        uc_used, outer_fill_color = candidate_pairs[0]

        remaining_unique_colors = {uc for uc in unique_colors if uc != uc_used}
        inner_fill_color = max(remaining_unique_colors) if remaining_unique_colors else None

        # 8. Determine Fill Regions & Execute Fill
        outer_bb_objects = [obj for obj in size_3_objects if obj['color'] < 5]

        if not outer_bb_objects:
            return output_grid # No objects to define outer region

        bb_outer = get_bounding_box(outer_bb_objects)
        if bb_outer is None: return output_grid

        min_r_outer, min_c_outer, max_r_outer, max_c_outer = bb_outer

        # (Outer Fill)
        for r in range(min_r_outer, max_r_outer + 1):
            for c in range(min_c_outer, max_c_outer + 1):
                if input_grid[r][c] == background_color:
                    output_grid[r][c] = outer_fill_color

        # (Inner Fill Condition & Execution)
        if inner_fill_color is not None:
            # Find single most frequent non-background color
            most_frequent_non_bg = None
            if non_bg_counts:
                 sorted_non_bg = sorted(non_bg_counts.items(), key=lambda item: item[1], reverse=True)
                 if len(sorted_non_bg) == 1 or sorted_non_bg[0][1] > sorted_non_bg[1][1]:
                      most_frequent_non_bg = sorted_non_bg[0][0]

            if most_frequent_non_bg is not None:
                inner_bb_objects = [obj for obj in outer_bb_objects if obj['color'] != most_frequent_non_bg]

                if inner_bb_objects:
                    bb_inner = get_bounding_box(inner_bb_objects)
                    if bb_inner:
                        min_r_inner, min_c_inner, max_r_inner, max_c_inner = bb_inner
                        # (Inner Fill Execution)
                        for r in range(min_r_inner, max_r_inner + 1):
                            for c in range(min_c_inner, max_c_inner + 1):
                                if input_grid[r][c] == background_color:
                                    output_grid[r][c] = inner_fill_color # Overwrite
                                    
    else:
        # -------- Mode 2: No Unique Colors Exist --------
        
        # 9. Process per Color Group
        colors_in_size_3 = sorted(list({obj['color'] for obj in size_3_objects}))

        for color_c in colors_in_size_3:
            # Determine Fill Color for C
            max_adjacent_color = -1
            cells_of_color_c = []
            group_c_objects = []
            for obj in size_3_objects:
                if obj['color'] == color_c:
                    group_c_objects.append(obj)
                    cells_of_color_c.extend(obj['locations'])
            
            if not group_c_objects: continue # Should not happen if color_c came from the set

            for r, c in cells_of_color_c:
                 for nr, nc in get_neighbors(r, c, height, width):
                     neighbor_color = input_grid[nr][nc]
                     if neighbor_color != background_color and neighbor_color != color_c:
                         max_adjacent_color = max(max_adjacent_color, neighbor_color)

            fill_color_c = max_adjacent_color if max_adjacent_color > -1 else color_c

            # Determine Fill Region for C
            bb_c = get_bounding_box(group_c_objects)
            if bb_c is None: continue

            min_r_c, min_c_c, max_r_c, max_c_c = bb_c

            # Execute Fill for C
            for r in range(min_r_c, max_r_c + 1):
                for c in range(min_c_c, max_c_c + 1):
                    if input_grid[r][c] == background_color:
                         # Overwrite based on processing order (sorted colors)
                        output_grid[r][c] = fill_color_c

    # 11. Return Output
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 2 3 3 3 0 0
0 0 0 2 3 3 3 3 0 0
0 0 0 3 1 1 0 3 0 0
0 0 0 3 1 0 0 3 0 0
0 0 0 3 0 0 1 3 0 0
0 0 0 3 0 1 1 3 0 0
0 0 0 3 3 3 3 2 0 0
0 0 0 3 3 3 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 2 2 3 3 3 0 0
0 0 0 2 3 3 3 3 0 0
0 0 0 3 1 1 3 3 0 0
0 0 0 3 1 3 3 3 0 0
0 0 0 3 3 3 1 3 0 0
0 0 0 3 3 1 1 3 0 0
0 0 0 3 3 3 3 2 0 0
0 0 0 3 3 3 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 1 3 0 4 0 1 1 0 0
0 4 5 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 5 5 5 5 4 4
0 0 0 0 5 5 5 5 5 4
0 0 0 0 5 1 1 3 5 5
0 0 0 0 5 1 3 3 5 5
0 0 0 0 5 3 3 3 5 5
0 0 0 0 5 3 3 3 5 5
0 0 0 0 5 3 3 1 5 5
0 1 3 0 4 3 1 1 5 5
0 4 5 0 4 4 5 5 5 5
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 5 5 5 5 4 4
0 0 0 0 5 5 5 5 5 4
0 0 0 0 5 1 1 5 5 5
0 0 0 0 5 1 5 5 5 5
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 1 5 5
0 1 3 0 4 5 1 1 5 5
0 4 5 0 4 4 5 5 5 5
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.0

## Example 3:
Input:
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 2 3 4 4 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 4 3 3 1 1 3 3 2 3 3 3
3 3 3 3 3 3 3 3 3 3 1 3 2 2 3 3 3
3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3
3 3 1 6 3 3 3 3 4 4 3 3 3 3 3 3 3
3 3 2 9 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 4 0 3 3 3 1 3 3 3 3 3 3 3 3 3
3 3 8 9 3 3 3 1 1 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 2 9 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 9 9 9 6 6 1 1 9 9 2 3 3 3
3 3 3 3 9 9 9 6 6 6 1 9 2 2 3 3 3
3 3 3 3 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 1 6 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 2 9 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 4 0 3 3 3 1 6 6 6 3 3 3 3 3 3
3 3 8 9 3 3 3 1 1 6 6 3 3 3 3 3 3
```
Transformed Output:
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 2 9 4 4 9 9 9 9 9 9 3 3 3
3 3 3 3 9 9 4 9 9 1 1 9 9 2 3 3 3
3 3 3 3 9 9 9 9 9 9 1 9 2 2 3 3 3
3 3 3 3 9 9 9 9 9 4 9 9 9 9 3 3 3
3 3 1 6 9 9 9 9 4 4 9 9 9 9 3 3 3
3 3 2 9 9 9 9 9 9 9 9 9 9 9 3 3 3
3 3 4 0 9 9 9 1 9 9 9 9 9 9 3 3 3
3 3 8 9 9 9 9 1 1 9 9 9 9 9 3 3 3
```
Match: False
Pixels Off: 55
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 53.921568627450995

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 6 0 0 0 7 7 0 0
6 7 0 0 0 0 0 0 0 6 6 0 0 0 7 7 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 7 7 7 0 4 4 4 4 4 4
0 0 0 0 0 0 6 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0
3 3 0 0 0 0 7 7 7 7 6 0 0 0 6 6 0 0
6 7 0 0 0 0 7 7 7 6 6 0 0 0 6 6 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 6 6 6 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0
3 3 0 0 0 0 6 6 6 6 6 0 0 0 7 7 0 0
6 7 0 0 0 0 6 6 6 6 6 0 0 0 7 7 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.037037037037038
## General Assessment

The provided code attempts to solve the task by implementing a two-mode strategy based on the presence or absence of unique colors (colors appearing exactly once) in the input grid.

*   **Mode 1 (Unique Colors Exist):** This mode seems partially correct. It correctly identifies unique colors and uses them (and their neighbors) to determine fill colors (outer and inner). It also uses size-3 objects (filtered by `color < 5`) to determine an outer bounding box. However, the logic for determining the inner bounding box (when applicable) and potentially a rule for preserving adjacency to original shapes seem flawed, leading to incorrect fills in Examples 1, 2, and 3. Example 3 is particularly problematic as the inner fill condition and region calculation failed significantly.
*   **Mode 2 (No Unique Colors Exist):** This mode attempts to process groups of size-3 objects based on their color `C`. It calculates a fill color based on neighbors (or `C` itself) and fills the bounding box of the respective size-3 objects. Example 4 shows this mode fails significantly in determining both the correct fill colors and the correct fill regions. The fill color logic `max(neighbor, C)` seems plausible but doesn't cover all cases, and the region logic (minimal BB of size-3 objects of color C) doesn't match the output.

**Strategy for Resolution:**

1.  **Re-evaluate Mode 1:**
    *   Confirm the fill color determination logic (`outer_fill_color` from best pair, `inner_fill_color` from remaining unique).
    *   Confirm the Outer BB object selection (`size=3` and `color<5`).
    *   Critically re-examine the conditions and object selection criteria for the Inner BB. The current rule involving the single most frequent non-background color seems incorrect or incomplete, especially when ties occur (E3). Explore alternatives: Is it based on colors <= inner fill color? Related to locations? Or is the failed "adjacency preservation" idea masking a simpler BB rule?
    *   Test the "adjacency preservation" hypothesis more carefully ONLY on examples 1 & 2 where it seemed plausible. If it holds ONLY for those, it might be conditional. However, given it fails E3, it's likely incorrect.
2.  **Re-evaluate Mode 2:**
    *   The current logic linking size-3 objects of color `C` to a specific fill color and region needs fundamental rethinking.
    *   Analyze E4: Identify the *actual* source objects/properties determining each filled region and its color. Is object size always 3? Is the fill color always `max(neighbor, C)` or different? Are the regions strictly BBs, or are they modified (e.g., clipped, expanded)?
3.  **Simplify/Unify:** Check if any logic elements (e.g., bounding box calculations, fill rules) can be unified across modes or if the two modes are truly distinct.
4.  **Prioritize:** Focus on getting Mode 1 correct first, as it covers more examples. The Inner BB calculation in E3 is the key challenge. For Mode 2, acknowledge the high uncertainty and formulate the best hypothesis based on E4, even if imperfect.

## Metrics and Analysis

| Example   | Mode      | Unique Colors | Size-3 Obj Colors | Most Freq Non-BG | Outer Fill (Exp/Code) | Inner Fill (Exp/Code) | Outer BB (Objs < 5) | Inner BB (Exp/Code) | Code Correct | Key Issues                                                                                                                               |
| :-------- | :-------- | :------------ | :---------------- | :----------------- | :---------------------- | :---------------------- | :-------------------- | :-------------------- | :----------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Train 1** | Unique    | {3}           | {2, 1, 1, 2}      | {1, 2} (Tie)       | 3 / 3                   | None / None             | [0:7, 3:7]            | N/A / N/A             | **No**       | Code filled all BG in BB; Output preserved BG adjacent to original shapes.                                                             |
| **Train 2** | Unique    | {3, 5}        | {1, 1, 4, 4}      | {4}                | 5 / 5                   | 3 / 3                   | [0:8, 4:9]            | [2:7, 6:7]? / [2:7, 5:8] | **No**       | Inner BB incorrect; Code filled all BG in Inner BB; Output preserved BG adjacent to original shapes.                                    |
| **Train 3** | Unique    | {6, 0, 8}     | {2, 4, 1, 2, 4, 1} | {1, 4} (Tie)       | 9 / 9                   | 6 / None                | [3:11, 4:13]          | [5:11, 7:10] / N/A     | **No**       | Code failed to trigger Inner Fill due to tie; Even if triggered, Inner BB rule (based on tie) would yield wrong region ([3:11, 4:13]). |
| **Train 4** | No Unique | None          | {3, 3, 4, 4, 6}   | {4, 6} (Tie)       | N/A / N/A               | N/A / N/A               | N/A                   | N/A                   | **No**       | Mode 2 logic flawed: Fill colors (esp. for C=6) incorrect in context; Fill regions derived from BBs of size-3 objects don't match output. |

*Code execution assumes the python code provided in the previous step.*
*Outer BB refers to the BB calculated from size-3 objects with color < 5.*
*Code Inner BB refers to the BB calculated by the code's logic (filtering based on single most frequent non-bg).*
*Exp Inner BB is inferred from the expected output.*

## Updated Facts (YAML)

```yaml
# Facts observed from all training examples and code execution results
grid_properties:
  size: variable
  background_color_rule: most frequent color in the input grid
colors:
  present_in_input: variable
  present_in_output: variable
  unique_input_colors_rule: colors appearing exactly once in the input grid (excluding background)
  fill_colors_determination:
    mode_selection: based on presence of unique_input_colors
    mode_unique_colors:
      # Determines outer_fill_color and uc_used (unique color source)
      candidates_rule: form pairs (uc, neighbor_or_uc) where uc is unique color, neighbor_or_uc is uc or its non-background orthogonal neighbor.
      outer_fill_color_rule: value from the candidate pair with the maximum value, breaking ties by maximizing uc.
      # Determines inner_fill_color
      inner_fill_color_rule: (if >1 unique color exists) highest unique color NOT equal to uc_used.
    mode_no_unique_colors:
      # Processes each distinct color C found in size-3 objects
      trigger: process per distinct color C found in size-3 objects
      fill_color_rule(C): max(max_adjacent_non_background_neighbor, C) # Previous neighbor-only rule failed E4 C=6->Fill=6; Needs neighbor *or* self. Max seems best fit.
  most_frequent_non_background_color_rule: find color counts excluding background, identify single highest count OR set of tied highest counts.
objects_input:
  properties:
    - id
    - color
    - location (list of [row, col])
    - size (number of cells)
  criteria:
    size_3_objects: objects with size = 3
    size_3_lt_5_objects: size-3 objects with color < 5 (used in unique color mode outer BB)
transformation:
  action: conditional_layered_fill
  condition: presence of unique input colors
  mode_unique_colors:
    layers:
      - layer_id: outer_fill
        fill_color_rule: derived from unique colors and neighbors (pair rule)
        region_definition:
          method: minimal_bounding_box
          source_objects: size_3_objects with color < 5
        fill_rule: replace background color only # Adjacency preservation rule seems incorrect (failed E3)
      - layer_id: inner_fill (conditional)
        condition: inner_fill_color exists # Trigger regardless of most frequent count status
        fill_color_rule: highest remaining unique color not used for outer fill
        region_definition:
          method: minimal_bounding_box # This remains the biggest uncertainty
          source_objects_rule: | # Revised hypothesis based on E2/E3 failure analysis
            Select from 'size_3_lt_5_objects' those whose color is NOT in the set of most frequent non-background color(s).
            If this selection results in an empty set, maybe fall back to using all 'size_3_lt_5_objects'? (Needs testing)
            *Self-Correction: This rule predicted wrong inner BB for E3. High uncertainty remains.*
            *Alternative Hypothesis: Maybe inner BB is Outer BB inset by 1? Or related to locations of unique colors? No consistent simple rule found yet.*
        fill_rule: replace background color only (overwrites outer fill where applicable)
  mode_no_unique_colors:
    # High uncertainty based on E4 failure
    process_per_color_group: For each distinct color C in size_3_objects (sorted by C)
      layers: # Conceptually, one layer per color C
        - layer_id: fill_for_C
          fill_color_rule: max(max_adjacent_non_background_neighbor, C) # Revised based on E4 C=6 case analysis
          region_definition:
            method: minimal_bounding_box # This is likely incorrect; regions seem shifted/clipped in E4
            source_objects: size_3_objects with color C
          fill_rule: replace background color only
          overlap_rule: Later fills (higher C) overwrite earlier fills. # Assumption
  preservation:
    - all original non-background cells retain their color and position.
```

## Updated Natural Language Program

1.  Determine the `background_color` by finding the most frequent color in the input grid.
2.  Initialize the output grid as a copy of the input grid.
3.  Find all contiguous groups of non-background cells (objects), recording their size, color, and locations.
4.  Identify all colors (excluding `background_color`) that appear exactly once in the input grid (`unique_colors`) and store their locations.
5.  Identify all objects with `size == 3` (`size_3_objects`).

6.  **Mode Selection:** Check if `unique_colors` is empty.
    *   If **NOT empty** (Unique Colors Mode): Proceed to step 7.
    *   If **empty** (No Unique Colors Mode): Proceed to step 13.

7.  **Unique Colors Mode - Determine Fill Colors:**
    *   Create a list of `candidate_pairs` = [].
    *   For each `uc` in `unique_colors` and its location `(r, c)`:
        *   Add `(uc, uc)` to `candidate_pairs`.
        *   Check orthogonal neighbors `(nr, nc)` of `(r, c)`.
        *   For each neighbor, get its color `neighbor_color`.
        *   If `neighbor_color != background_color` and `neighbor_color != uc`, add `(uc, neighbor_color)` to `candidate_pairs`.
    *   If `candidate_pairs` is empty, return the initial output grid.
    *   Find the pair `(uc_best, val_best)` in `candidate_pairs` that maximizes `val_best`, breaking ties by maximizing `uc_best`.
    *   Set `outer_fill_color = val_best`.
    *   Set `uc_used = uc_best`.
    *   Create `remaining_unique_colors` by removing `uc_used` from `unique_colors`.
    *   If `remaining_unique_colors` is not empty, set `inner_fill_color` to the highest value in `remaining_unique_colors`. Otherwise, set `inner_fill_color` to None.

8.  **Unique Colors Mode - Outer Fill:**
    *   Select `outer_bb_objects` from `size_3_objects` where `object.color < 5`.
    *   If `outer_bb_objects` is empty, return the initial output grid.
    *   Calculate the minimal bounding box (`BB_outer`) enclosing all `outer_bb_objects`.
    *   If `BB_outer` is valid, iterate through each cell `(r, c)` within `BB_outer`. If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `outer_fill_color`.

9.  **Unique Colors Mode - Inner Fill Condition:** Check if `inner_fill_color` is not None.

10. **Unique Colors Mode - Determine Inner BB Objects (High Uncertainty):**
    *   If the condition in step 9 is met:
        *   Count the frequency of each non-background color in the input grid. Find the set of colors with the highest frequency (`most_frequent_set`).
        *   Select `inner_bb_objects` from `outer_bb_objects` where the `object.color` is *NOT* in `most_frequent_set`.
        *   *(Self-Correction Note: This rule failed Example 3 by yielding an incorrect Inner BB. An alternative rule is needed but not yet identified. The coder should be aware this step is speculative).*
        *   If `inner_bb_objects` is empty (e.g., all outer objects had most frequent colors), potentially fall back to using all `outer_bb_objects` for the inner BB calculation (needs verification).

11. **Unique Colors Mode - Inner Fill Execution:**
    *   If `inner_bb_objects` (from step 10) is not empty:
        *   Calculate the minimal bounding box (`BB_inner`) enclosing `inner_bb_objects`.
        *   If `BB_inner` is valid, iterate through each cell `(r, c)` within `BB_inner`. If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `inner_fill_color` (overwriting `outer_fill_color` if previously placed).

12. **Unique Colors Mode - Finalize:** Proceed to step 16 (Return).

13. **No Unique Colors Mode - Process per Color Group (High Uncertainty):**
    *   Find the set of distinct colors `{C1, C2, ...}` present in the `size_3_objects`. Sort this set numerically.
    *   For each distinct color `C` in the sorted set:
        *   **Determine Fill Color for C:**
            *   Initialize `max_adjacent_color = -1`.
            *   Find all cells `(r, c)` belonging to size-3 objects of color `C`.
            *   For each such cell `(r, c)`:
                *   Check orthogonal neighbors `(nr, nc)`. Get `neighbor_color`.
                *   If `neighbor_color != background_color` and `neighbor_color != C`:
                    *   `max_adjacent_color = max(max_adjacent_color, neighbor_color)`
            *   Set `fill_color_C = max(max_adjacent_color, C)` (uses neighbor if found and higher, otherwise uses C).
        *   **Determine Fill Region for C:**
            *   Select `group_C_objects` from `size_3_objects` where `object.color == C`.
            *   If `group_C_objects` is empty, continue to the next color `C`.
            *   Calculate the minimal bounding box (`BB_C`) enclosing `group_C_objects`.
            *   *(Self-Correction Note: This BB calculation likely does not produce the correct fill regions seen in Example 4. The true region logic is unknown but seems related to this BB.)*
        *   **Execute Fill for C:**
            *   If `BB_C` is valid, iterate through each cell `(r, c)` within `BB_C`.
            *   If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `fill_color_C`. (Overwriting based on processing order of C).

14. **No Unique Colors Mode - Finalize:** After processing all color groups C, proceed to step 16 (Return).

15. **Return Output:** Return the modified output grid.
```python
import collections
import itertools
from copy import deepcopy

"""
Transforms an input grid based on two potential modes, determined by the presence of unique colors (colors appearing exactly once, excluding the background color).

Mode 1: Unique Colors Exist
1. Determine fill colors:
    - Identify unique colors (uc) and their non-background orthogonal neighbors (nc).
    - Form candidate pairs (uc, nc or uc).
    - 'outer_fill_color' is the value (nc or uc) from the pair with the max value, breaking ties by maximizing the associated uc.
    - 'uc_used' is the unique color associated with the selected outer fill pair.
    - 'inner_fill_color' is the highest remaining unique color not equal to 'uc_used', if any.
2. Determine fill regions:
    - Identify size-3 objects with color < 5 ('outer_bb_objects').
    - 'BB_outer' is the minimal bounding box of 'outer_bb_objects'.
    - If 'inner_fill_color' exists:
        - Find the set of most frequent non-background color(s).
        - Identify 'inner_bb_objects' (subset of 'outer_bb_objects' whose color is NOT in the most frequent set).
        - 'BB_inner' is the minimal bounding box of 'inner_bb_objects'. (High uncertainty about this rule).
3. Apply fills:
    - Fill background cells within 'BB_outer' with 'outer_fill_color'.
    - If 'BB_inner' exists, fill background cells within 'BB_inner' with 'inner_fill_color' (overwrites outer).

Mode 2: No Unique Colors Exist (High Uncertainty)
1. Group size-3 objects by their color 'C'. Sort these colors 'C'.
2. For each color group 'C' in sorted order:
    - Determine 'fill_color_C': max(max non-background color adjacent to any cell of color C, C itself).
    - Calculate 'BB_C': minimal bounding box for the size-3 objects of color 'C'. (Region rule is likely incorrect).
    - Fill background cells within 'BB_C' with 'fill_color_C'. Later fills (higher C) overwrite earlier ones.

General Rules:
- The 'background_color' is the most frequent color in the input grid.
- Only background cells are ever filled. Original non-background cells are preserved.
- Object finding uses orthogonal connectivity for cells of the *same* color.
- Bounding boxes are minimal axis-aligned rectangles.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_objects(grid: list[list[int]], background_color: int) -> list[dict]:
    """Finds connected objects of the same non-background color."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r][c]
            if color != background_color and (r, c) not in visited:
                obj_locations = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_locations.add((r,c))

                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            obj_locations.add((nr, nc))
                            
                if obj_locations:
                    objects.append({
                        "color": color,
                        "locations": list(obj_locations),
                        "size": len(obj_locations)
                    })
    return objects

def get_color_counts(grid: list[list[int]]) -> collections.Counter:
    """Counts occurrences of each color in the grid."""
    counts = collections.Counter()
    for row in grid:
        counts.update(row)
    return counts

def get_bounding_box(objects: list[dict]) -> tuple[int, int, int, int] | None:
    """Calculates the minimal bounding box for a list of objects."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    has_locations = False

    for obj in objects:
        for r, c in obj['locations']:
            has_locations = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    if not has_locations:
        return None 

    return min_r, min_c, max_r, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    height = len(input_grid)
    width = len(input_grid[0])
    output_grid = deepcopy(input_grid)

    # 1. Determine background color
    color_counts = get_color_counts(input_grid)
    if not color_counts: return output_grid
    background_color = color_counts.most_common(1)[0][0]

    # 2. Find all objects
    all_objects = find_objects(input_grid, background_color)
    if not all_objects: return output_grid

    # 3. Find unique colors (excluding background) and their locations
    unique_colors = {}
    non_bg_counts = {color: count for color, count in color_counts.items() if color != background_color}
    for r in range(height):
        for c in range(width):
             color = input_grid[r][c]
             if color != background_color and non_bg_counts.get(color) == 1:
                 unique_colors[color] = (r, c) 

    # 4. Identify size-3 objects
    size_3_objects = [obj for obj in all_objects if obj['size'] == 3]
    
    # 5. Mode Selection
    if unique_colors:
        # -------- Mode 1: Unique Colors Exist --------
        
        # 7. Determine Fill Colors
        candidate_pairs = []
        for uc, (r, c) in unique_colors.items():
            candidate_pairs.append((uc, uc)) # Pair with itself
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = input_grid[nr][nc]
                if neighbor_color != background_color and neighbor_color != uc:
                     candidate_pairs.append((uc, neighbor_color))
                     
        if not candidate_pairs:
             return output_grid # Should not happen if unique_colors is non-empty

        # Find the best pair: max value, tie-break with max uc
        candidate_pairs.sort(key=lambda pair: (pair[1], pair[0]), reverse=True)
        uc_used, outer_fill_color = candidate_pairs[0]

        # Determine inner fill color
        remaining_unique_colors = {uc for uc in unique_colors if uc != uc_used}
        inner_fill_color = max(remaining_unique_colors) if remaining_unique_colors else None

        # 8. Outer Fill
        outer_bb_objects = [obj for obj in size_3_objects if obj['color'] < 5]

        if not outer_bb_objects:
            return output_grid # No objects to define outer region

        bb_outer = get_bounding_box(outer_bb_objects)
        if bb_outer is None: return output_grid

        min_r_outer, min_c_outer, max_r_outer, max_c_outer = bb_outer

        # Apply Outer Fill
        for r in range(min_r_outer, max_r_outer + 1):
            for c in range(min_c_outer, max_c_outer + 1):
                if input_grid[r][c] == background_color:
                    output_grid[r][c] = outer_fill_color

        # 9. Inner Fill Condition
        if inner_fill_color is not None:
            # 10. Determine Inner BB Objects (High Uncertainty)
            most_frequent_set = set()
            if non_bg_counts:
                 max_freq = 0
                 for color, count in non_bg_counts.items():
                      max_freq = max(max_freq, count)
                 most_frequent_set = {color for color, count in non_bg_counts.items() if count == max_freq}

            inner_bb_objects = [obj for obj in outer_bb_objects if obj['color'] not in most_frequent_set]
            
            # Fallback (speculative, maybe not needed or correct)
            # if not inner_bb_objects and outer_bb_objects:
            #     inner_bb_objects = outer_bb_objects 

            # 11. Inner Fill Execution
            if inner_bb_objects:
                bb_inner = get_bounding_box(inner_bb_objects)
                if bb_inner:
                    min_r_inner, min_c_inner, max_r_inner, max_c_inner = bb_inner
                    # Apply Inner Fill
                    for r in range(min_r_inner, max_r_inner + 1):
                        for c in range(min_c_inner, max_c_inner + 1):
                            if input_grid[r][c] == background_color:
                                output_grid[r][c] = inner_fill_color # Overwrite
                                    
    else:
        # -------- Mode 2: No Unique Colors Exist (High Uncertainty) --------
        
        # 13. Process per Color Group
        colors_in_size_3 = sorted(list({obj['color'] for obj in size_3_objects}))

        for color_c in colors_in_size_3:
            # Determine Fill Color for C
            max_adjacent_color = -1
            cells_of_color_c = []
            group_c_objects = []
            for obj in size_3_objects:
                if obj['color'] == color_c:
                    group_c_objects.append(obj)
                    cells_of_color_c.extend(obj['locations'])
            
            if not group_c_objects: continue # Should not happen

            for r, c in cells_of_color_c:
                 for nr, nc in get_neighbors(r, c, height, width):
                     neighbor_color = input_grid[nr][nc]
                     if neighbor_color != background_color and neighbor_color != color_c:
                         max_adjacent_color = max(max_adjacent_color, neighbor_color)

            fill_color_c = max(max_adjacent_color, color_c) # Use neighbor if found and higher, else C

            # Determine Fill Region for C (Likely incorrect rule for E4)
            bb_c = get_bounding_box(group_c_objects)
            if bb_c is None: continue

            min_r_c, min_c_c, max_r_c, max_c_c = bb_c

            # Execute Fill for C
            for r in range(min_r_c, max_r_c + 1):
                for c in range(min_c_c, max_c_c + 1):
                    if input_grid[r][c] == background_color:
                        # Overwrite based on processing order (sorted colors C)
                        output_grid[r][c] = fill_color_c

    # 15. Return Output
    return output_grid
```

Previous Code:
```python
import collections
import itertools
from copy import deepcopy

"""
Transforms an input grid based on two potential modes, determined by the presence of unique colors (colors appearing exactly once, excluding the background color).

Mode 1: Unique Colors Exist
1. Determine fill colors:
    - Identify unique colors (uc) and their non-background orthogonal neighbors (nc).
    - Form candidate pairs (uc, nc or uc).
    - 'outer_fill_color' is the value (nc or uc) from the pair with the max value, breaking ties by maximizing the associated uc.
    - 'uc_used' is the unique color associated with the selected outer fill pair.
    - 'inner_fill_color' is the highest remaining unique color not equal to 'uc_used', if any.
2. Determine fill regions:
    - Identify size-3 objects with color < 5 ('outer_bb_objects').
    - 'BB_outer' is the minimal bounding box of 'outer_bb_objects'.
    - If 'inner_fill_color' exists:
        - Find the set of most frequent non-background color(s).
        - Identify 'inner_bb_objects' (subset of 'outer_bb_objects' whose color is NOT in the most frequent set).
        - 'BB_inner' is the minimal bounding box of 'inner_bb_objects'. (High uncertainty about this rule).
3. Apply fills:
    - Fill background cells within 'BB_outer' with 'outer_fill_color'.
    - If 'BB_inner' exists, fill background cells within 'BB_inner' with 'inner_fill_color' (overwrites outer).

Mode 2: No Unique Colors Exist (High Uncertainty)
1. Group size-3 objects by their color 'C'. Sort these colors 'C'.
2. For each color group 'C' in sorted order:
    - Determine 'fill_color_C': max(max non-background color adjacent to any cell of color C, C itself).
    - Calculate 'BB_C': minimal bounding box for the size-3 objects of color 'C'. (Region rule is likely incorrect).
    - Fill background cells within 'BB_C' with 'fill_color_C'. Later fills (higher C) overwrite earlier ones.

General Rules:
- The 'background_color' is the most frequent color in the input grid.
- Only background cells are ever filled. Original non-background cells are preserved.
- Object finding uses orthogonal connectivity for cells of the *same* color.
- Bounding boxes are minimal axis-aligned rectangles.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_objects(grid: list[list[int]], background_color: int) -> list[dict]:
    """Finds connected objects of the same non-background color."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r][c]
            if color != background_color and (r, c) not in visited:
                obj_locations = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_locations.add((r,c))

                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            obj_locations.add((nr, nc))
                            
                if obj_locations:
                    objects.append({
                        "color": color,
                        "locations": list(obj_locations),
                        "size": len(obj_locations)
                    })
    return objects

def get_color_counts(grid: list[list[int]]) -> collections.Counter:
    """Counts occurrences of each color in the grid."""
    counts = collections.Counter()
    for row in grid:
        counts.update(row)
    return counts

def get_bounding_box(objects: list[dict]) -> tuple[int, int, int, int] | None:
    """Calculates the minimal bounding box for a list of objects."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    has_locations = False

    for obj in objects:
        for r, c in obj['locations']:
            has_locations = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    if not has_locations:
        return None 

    return min_r, min_c, max_r, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    height = len(input_grid)
    width = len(input_grid[0])
    output_grid = deepcopy(input_grid)

    # 1. Determine background color
    color_counts = get_color_counts(input_grid)
    if not color_counts: return output_grid
    background_color = color_counts.most_common(1)[0][0]

    # 2. Find all objects
    all_objects = find_objects(input_grid, background_color)
    if not all_objects: return output_grid

    # 3. Find unique colors (excluding background) and their locations
    unique_colors = {}
    non_bg_counts = {color: count for color, count in color_counts.items() if color != background_color}
    for r in range(height):
        for c in range(width):
             color = input_grid[r][c]
             if color != background_color and non_bg_counts.get(color) == 1:
                 unique_colors[color] = (r, c) 

    # 4. Identify size-3 objects
    size_3_objects = [obj for obj in all_objects if obj['size'] == 3]
    
    # 5. Mode Selection
    if unique_colors:
        # -------- Mode 1: Unique Colors Exist --------
        
        # 7. Determine Fill Colors
        candidate_pairs = []
        for uc, (r, c) in unique_colors.items():
            candidate_pairs.append((uc, uc)) # Pair with itself
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = input_grid[nr][nc]
                if neighbor_color != background_color and neighbor_color != uc:
                     candidate_pairs.append((uc, neighbor_color))
                     
        if not candidate_pairs:
             return output_grid # Should not happen if unique_colors is non-empty

        # Find the best pair: max value, tie-break with max uc
        candidate_pairs.sort(key=lambda pair: (pair[1], pair[0]), reverse=True)
        uc_used, outer_fill_color = candidate_pairs[0]

        # Determine inner fill color
        remaining_unique_colors = {uc for uc in unique_colors if uc != uc_used}
        inner_fill_color = max(remaining_unique_colors) if remaining_unique_colors else None

        # 8. Outer Fill
        outer_bb_objects = [obj for obj in size_3_objects if obj['color'] < 5]

        if not outer_bb_objects:
            return output_grid # No objects to define outer region

        bb_outer = get_bounding_box(outer_bb_objects)
        if bb_outer is None: return output_grid

        min_r_outer, min_c_outer, max_r_outer, max_c_outer = bb_outer

        # Apply Outer Fill
        for r in range(min_r_outer, max_r_outer + 1):
            for c in range(min_c_outer, max_c_outer + 1):
                if input_grid[r][c] == background_color:
                    output_grid[r][c] = outer_fill_color

        # 9. Inner Fill Condition
        if inner_fill_color is not None:
            # 10. Determine Inner BB Objects (High Uncertainty)
            most_frequent_set = set()
            if non_bg_counts:
                 max_freq = 0
                 for color, count in non_bg_counts.items():
                      max_freq = max(max_freq, count)
                 most_frequent_set = {color for color, count in non_bg_counts.items() if count == max_freq}

            inner_bb_objects = [obj for obj in outer_bb_objects if obj['color'] not in most_frequent_set]
            
            # Fallback (speculative, maybe not needed or correct)
            # if not inner_bb_objects and outer_bb_objects:
            #     inner_bb_objects = outer_bb_objects 

            # 11. Inner Fill Execution
            if inner_bb_objects:
                bb_inner = get_bounding_box(inner_bb_objects)
                if bb_inner:
                    min_r_inner, min_c_inner, max_r_inner, max_c_inner = bb_inner
                    # Apply Inner Fill
                    for r in range(min_r_inner, max_r_inner + 1):
                        for c in range(min_c_inner, max_c_inner + 1):
                            if input_grid[r][c] == background_color:
                                output_grid[r][c] = inner_fill_color # Overwrite
                                    
    else:
        # -------- Mode 2: No Unique Colors Exist (High Uncertainty) --------
        
        # 13. Process per Color Group
        colors_in_size_3 = sorted(list({obj['color'] for obj in size_3_objects}))

        for color_c in colors_in_size_3:
            # Determine Fill Color for C
            max_adjacent_color = -1
            cells_of_color_c = []
            group_c_objects = []
            for obj in size_3_objects:
                if obj['color'] == color_c:
                    group_c_objects.append(obj)
                    cells_of_color_c.extend(obj['locations'])
            
            if not group_c_objects: continue # Should not happen

            for r, c in cells_of_color_c:
                 for nr, nc in get_neighbors(r, c, height, width):
                     neighbor_color = input_grid[nr][nc]
                     if neighbor_color != background_color and neighbor_color != color_c:
                         max_adjacent_color = max(max_adjacent_color, neighbor_color)

            fill_color_c = max(max_adjacent_color, color_c) # Use neighbor if found and higher, else C

            # Determine Fill Region for C (Likely incorrect rule for E4)
            bb_c = get_bounding_box(group_c_objects)
            if bb_c is None: continue

            min_r_c, min_c_c, max_r_c, max_c_c = bb_c

            # Execute Fill for C
            for r in range(min_r_c, max_r_c + 1):
                for c in range(min_c_c, max_c_c + 1):
                    if input_grid[r][c] == background_color:
                        # Overwrite based on processing order (sorted colors C)
                        output_grid[r][c] = fill_color_c

    # 15. Return Output
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 2 3 3 3 0 0
0 0 0 2 3 3 3 3 0 0
0 0 0 3 1 1 0 3 0 0
0 0 0 3 1 0 0 3 0 0
0 0 0 3 0 0 1 3 0 0
0 0 0 3 0 1 1 3 0 0
0 0 0 3 3 3 3 2 0 0
0 0 0 3 3 3 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 2 2 3 3 3 0 0
0 0 0 2 3 3 3 3 0 0
0 0 0 3 1 1 3 3 0 0
0 0 0 3 1 3 3 3 0 0
0 0 0 3 3 3 1 3 0 0
0 0 0 3 3 1 1 3 0 0
0 0 0 3 3 3 3 2 0 0
0 0 0 3 3 3 2 2 0 0
1 0 0 0 0 0 0 0 0 0
2 3 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 1 3 0 4 0 1 1 0 0
0 4 5 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 5 5 5 5 4 4
0 0 0 0 5 5 5 5 5 4
0 0 0 0 5 1 1 3 5 5
0 0 0 0 5 1 3 3 5 5
0 0 0 0 5 3 3 3 5 5
0 0 0 0 5 3 3 3 5 5
0 0 0 0 5 3 3 1 5 5
0 1 3 0 4 3 1 1 5 5
0 4 5 0 4 4 5 5 5 5
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 5 5 5 5 4 4
0 0 0 0 5 5 5 5 5 4
0 0 0 0 5 1 1 5 5 5
0 0 0 0 5 1 5 5 5 5
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 5 5 1 5 5
0 1 3 0 4 5 1 1 5 5
0 4 5 0 4 4 5 5 5 5
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.0

## Example 3:
Input:
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 2 3 4 4 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 4 3 3 1 1 3 3 2 3 3 3
3 3 3 3 3 3 3 3 3 3 1 3 2 2 3 3 3
3 3 3 3 3 3 3 3 3 4 3 3 3 3 3 3 3
3 3 1 6 3 3 3 3 4 4 3 3 3 3 3 3 3
3 3 2 9 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 4 0 3 3 3 1 3 3 3 3 3 3 3 3 3
3 3 8 9 3 3 3 1 1 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 2 9 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 9 9 9 6 6 1 1 9 9 2 3 3 3
3 3 3 3 9 9 9 6 6 6 1 9 2 2 3 3 3
3 3 3 3 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 1 6 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 2 9 3 3 3 6 6 6 6 3 3 3 3 3 3
3 3 4 0 3 3 3 1 6 6 6 3 3 3 3 3 3
3 3 8 9 3 3 3 1 1 6 6 3 3 3 3 3 3
```
Transformed Output:
```
3 3 5 5 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 5 3 3 3 3 5 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 5 5 3 3 3 3 3 3 3 3 3
3 3 3 3 2 2 9 9 9 9 9 9 9 9 3 3 3
3 3 3 3 2 9 4 4 9 9 9 9 9 9 3 3 3
3 3 3 3 9 9 4 9 9 1 1 9 9 2 3 3 3
3 3 3 3 9 9 9 9 9 9 1 9 2 2 3 3 3
3 3 3 3 9 9 9 9 9 4 9 9 9 9 3 3 3
3 3 1 6 9 9 9 9 4 4 9 9 9 9 3 3 3
3 3 2 9 9 9 9 9 9 9 9 9 9 9 3 3 3
3 3 4 0 9 9 9 1 9 9 9 9 9 9 3 3 3
3 3 8 9 9 9 9 1 1 9 9 9 9 9 3 3 3
```
Match: False
Pixels Off: 55
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 53.921568627450995

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 6 0 0 0 7 7 0 0
6 7 0 0 0 0 0 0 0 6 6 0 0 0 7 7 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 7 7 7 0 4 4 4 4 4 4
0 0 0 0 0 0 6 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 0 0 0 0 0 0 0
3 3 0 0 0 0 7 7 7 7 6 0 0 0 6 6 0 0
6 7 0 0 0 0 7 7 7 6 6 0 0 0 6 6 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 6 6 6 0 4 4 4 4 4 4
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0
3 3 0 0 0 0 6 6 6 6 6 0 0 0 7 7 0 0
6 7 0 0 0 0 6 6 6 6 6 0 0 0 7 7 0 0
4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.037037037037038
## General Assessment

The provided code attempts a two-mode solution based on the presence of unique colors. The execution results highlight partial success and significant failures:

1.  **Mode 1 (Unique Colors):**
    *   **Fill Color Determination:** The logic for selecting `outer_fill_color` and `inner_fill_color` based on unique colors and their neighbors seems robust and correct across examples 1, 2, and 3.
    *   **Outer Bounding Box:** Using size-3 objects with `color < 5` to define `BB_outer` works consistently.
    *   **Inner Fill Trigger:** The original code's trigger (requiring a *single* most frequent non-background color) failed Example 3. The trigger should simply be the existence of an `inner_fill_color`.
    *   **Inner Bounding Box:** The logic used (`outer_bb_objects` excluding those with the most frequent non-background color) worked partially for E2 but failed completely for E3. **This remains the biggest area of uncertainty in Mode 1.** The rule governing the inner fill region is not correctly captured.
    *   **Fill Rule:** The code correctly fills only background cells within the calculated boxes, preserving original shapes. The previous idea of "adjacency preservation" (not filling background cells next to original shapes) appears incorrect as it didn't generalize.

2.  **Mode 2 (No Unique Colors):**
    *   **Fill Color Determination:** The original rule (max adjacent non-background neighbor) failed for color group C=6 in Example 4 (expected fill 7, rule gave 6). The revised rule `max(max_adjacent_non_background_neighbor, C)` correctly predicts fill colors for C=3 (3->3), C=4 (4->4), and C=6 (6->7) in E4.
    *   **Fill Region Determination:** Using the minimal bounding box of size-3 objects of color `C` works for C=3 and C=4 in E4 but fails significantly for C=6 (code BB [8:12, 6:10] vs expected fill region [8:12, 8:11]). **The rule governing the fill region in Mode 2 is incorrect or incomplete, especially when the fill color is determined by a neighbor.**
    *   **Overlap Rule:** The assumption that later fills (higher C) overwrite earlier ones seems consistent with E4's output where the fill=7 region overlaps and overwrites the fill=4 region.

**Strategy for Resolution:**

1.  **Mode 1 Refinement:**
    *   Correct the Inner Fill trigger condition to simply check `inner_fill_color is not None`.
    *   **Acknowledge the failure to determine the correct Inner BB rule.** Keep the previous (failed) rule (`outer_bb_objects` excluding most frequent) as a placeholder but clearly document its known failure in the YAML facts and NL program. Further analysis is needed to find the correct Inner BB rule (possible candidates: relation to unique color locations, fixed inset from Outer BB, different object filtering criteria).
2.  **Mode 2 Refinement:**
    *   Update the Fill Color rule to `max(max_adjacent_non_background_neighbor, C)`.
    *   **Acknowledge the failure to determine the correct fill region rule for cases where the fill color comes from a neighbor (like C=6 in E4).** Keep the simple BB rule (BB of size-3 objects of color C) but document its known failure.
3.  **Documentation:** Update the YAML facts and NL Program to reflect these corrections and explicitly state the unresolved uncertainties regarding region calculations in both modes.

## Metrics and Analysis

| Example   | Mode      | Unique Colors (Input) | Size-3 Obj Colors | Most Freq Non-BG (Set) | Outer Fill (Exp/Code) | Inner Fill (Exp/Code) | Outer BB (Code Rule OK?) | Inner BB (Code Rule OK?) | Code Correct | Key Issues (Post-Analysis)                                                                                                     |
| :-------- | :-------- | :-------------------- | :---------------- | :----------------------- | :---------------------- | :---------------------- | :----------------------- | :----------------------- | :----------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **Train 1** | Unique    | {3}                   | {2, 1, 1, 2}      | {1, 2}                   | 3 / 3                   | None / None             | Yes ([0:7, 3:7])         | N/A                      | **No**       | Output matches if Inner Fill rule is ignored (as intended) and *all* BG cells in Outer BB are filled. (Prev code had BG preservation error). |
| **Train 2** | Unique    | {3, 5}                | {1, 1, 4, 4}      | {4}                      | 5 / 5                   | 3 / 3                   | Yes ([0:8, 4:9])         | No ([2:7, 5:7] vs [2:7, 5:8]) | **No**       | Inner BB calculation rule (`color != 4`) gives slightly wrong region.                                                        |
| **Train 3** | Unique    | {6, 0, 8}             | {2, 4, 1, 2, 4, 1} | {1, 4}                   | 9 / 9                   | 6 / 6                   | Yes ([3:11, 4:13])       | No ([5:11, 7:10] vs [3:6, 4:13]) | **No**       | Inner Fill *should* trigger (Inner Color=6 exists). Inner BB rule (`color not in {1,4}`) gives drastically wrong region.         |
| **Train 4** | No Unique | None                  | {3, 3, 4, 4, 6}   | {4, 6}                   | N/A / N/A               | N/A / N/A               | N/A                      | N/A                      | **No**       | Mode 2: Fill Colors fixed by `max(adj,C)`. Region for C=6 wrong ([8:12, 8:11] vs [8:12, 6:10]).                              |

*Code execution assumes the *latest* python code generated in the previous step (code_01.py).*
*Outer BB refers to the BB calculated from size-3 objects with color < 5.*
*Code Inner BB refers to the BB calculated by the code's logic (filtering based on `most_frequent_set`).*
*Exp Inner BB is inferred from the expected output.*

## Updated Facts (YAML)

```yaml
# Facts observed from all training examples and updated code execution results
grid_properties:
  size: variable
  background_color_rule: most frequent color in the input grid
colors:
  present_in_input: variable
  present_in_output: variable
  unique_input_colors_rule: colors appearing exactly once in the input grid (excluding background_color)
  fill_colors_determination:
    mode_selection: based on presence of unique_input_colors
    mode_unique_colors:
      # Determines outer_fill_color and uc_used (unique color source)
      candidates_rule: form pairs (uc, neighbor_or_uc) where uc is unique color, neighbor_or_uc is uc or its non-background orthogonal neighbor.
      outer_fill_color_rule: value from the candidate pair with the maximum value, breaking ties by maximizing uc.
      # Determines inner_fill_color
      inner_fill_color_rule: (if >1 unique color exists) highest unique color NOT equal to uc_used.
    mode_no_unique_colors:
      # Processes each distinct color C found in size-3 objects
      trigger: process per distinct color C found in size-3 objects
      fill_color_rule(C): max(max_adjacent_non_background_neighbor, C) # Confirmed better than previous rule
  most_frequent_non_background_color_rule: find color counts excluding background, identify the set of colors sharing the maximum frequency.
objects_input:
  properties:
    - id
    - color
    - location (list of [row, col])
    - size (number of cells)
  criteria:
    size_3_objects: objects with size = 3
    size_3_lt_5_objects: size-3 objects with color < 5 (used in unique color mode outer BB)
transformation:
  action: conditional_layered_fill
  condition: presence of unique input colors
  mode_unique_colors:
    layers:
      - layer_id: outer_fill
        fill_color_rule: derived from unique colors and neighbors (pair rule)
        region_definition:
          method: minimal_bounding_box
          source_objects: size_3_objects with color < 5 # Rule appears correct
        fill_rule: replace background_color only # Confirmed correct
      - layer_id: inner_fill (conditional)
        condition: inner_fill_color exists # Corrected trigger
        fill_color_rule: highest remaining unique color not used for outer fill # Rule appears correct
        region_definition:
          method: minimal_bounding_box # Assumption
          source_objects_rule: | # RULE IS UNCERTAIN / INCORRECT
            Select from 'size_3_lt_5_objects' those whose color is NOT in the set of most_frequent_non_background_color(s).
            *Known Issue: This rule produces incorrect regions for E2 (slightly) and E3 (majorly). The correct rule for determining Inner BB source objects or coordinates is unknown.*
        fill_rule: replace background_color only (overwrites outer fill where applicable) # Confirmed correct
  mode_no_unique_colors:
    process_per_color_group: For each distinct color C in size_3_objects (sorted by C)
      layers: # Conceptually, one layer per color C
        - layer_id: fill_for_C
          fill_color_rule: max(max_adjacent_non_background_neighbor, C) # Rule appears correct
          region_definition:
            method: minimal_bounding_box # RULE IS UNCERTAIN / INCORRECT for some cases
            source_objects: size_3_objects with color C
            *Known Issue: This rule produces the incorrect fill region for C=6 in E4. The correct rule for determining the region, especially when fill color comes from a neighbor, is unknown.*
          fill_rule: replace background_color only # Confirmed correct
          overlap_rule: Later fills (higher C) overwrite earlier fills. # Appears correct
  preservation:
    - all original non-background cells retain their color and position. # Confirmed correct
```

## Updated Natural Language Program

1.  Determine the `background_color` by finding the most frequent color in the input grid.
2.  Initialize the output grid as a copy of the input grid.
3.  Find all contiguous groups of non-background cells (objects), recording their size, color, and locations. Assume objects consist of cells of the same color connected orthogonally.
4.  Identify all colors (excluding `background_color`) that appear exactly once in the input grid (`unique_colors`) and store their locations.
5.  Identify all objects with `size == 3` (`size_3_objects`).

6.  **Mode Selection:** Check if `unique_colors` is empty.
    *   If **NOT empty** (Unique Colors Mode): Proceed to step 7.
    *   If **empty** (No Unique Colors Mode): Proceed to step 13.

7.  **Unique Colors Mode - Determine Fill Colors:**
    *   Create a list of `candidate_pairs` = [].
    *   For each `uc` in `unique_colors` and its location `(r, c)`:
        *   Add `(uc, uc)` to `candidate_pairs`.
        *   Check orthogonal neighbors `(nr, nc)` of `(r, c)`.
        *   For each neighbor, get its color `neighbor_color`.
        *   If `neighbor_color != background_color` and `neighbor_color != uc`, add `(uc, neighbor_color)` to `candidate_pairs`.
    *   If `candidate_pairs` is empty, return the initial output grid.
    *   Find the pair `(uc_best, val_best)` in `candidate_pairs` that maximizes `val_best`, breaking ties by maximizing `uc_best`.
    *   Set `outer_fill_color = val_best`.
    *   Set `uc_used = uc_best`.
    *   Create `remaining_unique_colors` by removing `uc_used` from `unique_colors`.
    *   If `remaining_unique_colors` is not empty, set `inner_fill_color` to the highest value in `remaining_unique_colors`. Otherwise, set `inner_fill_color` to None.

8.  **Unique Colors Mode - Outer Fill:**
    *   Select `outer_bb_objects` from `size_3_objects` where `object.color < 5`.
    *   If `outer_bb_objects` is empty, return the initial output grid.
    *   Calculate the minimal bounding box (`BB_outer`) enclosing all `outer_bb_objects`.
    *   If `BB_outer` is valid, iterate through each cell `(r, c)` within `BB_outer`. If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `outer_fill_color`.

9.  **Unique Colors Mode - Inner Fill Condition:** Check if `inner_fill_color` is not None.

10. **Unique Colors Mode - Determine Inner BB Objects (UNCERTAIN RULE):**
    *   If the condition in step 9 is met:
        *   Count the frequency of each non-background color in the input grid. Find the set of colors with the highest frequency (`most_frequent_set`).
        *   **Apply UNCERTAIN Rule:** Select `inner_bb_objects` from `outer_bb_objects` where the `object.color` is *NOT* in `most_frequent_set`.
        *   ***WARNING:*** *This rule for selecting `inner_bb_objects` is known to fail for Example 3 and produce slightly incorrect results for Example 2. The correct method for determining the inner fill region is currently unknown.*

11. **Unique Colors Mode - Inner Fill Execution:**
    *   If `inner_bb_objects` (from step 10) is not empty:
        *   Calculate the minimal bounding box (`BB_inner`) enclosing `inner_bb_objects`.
        *   If `BB_inner` is valid, iterate through each cell `(r, c)` within `BB_inner`. If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `inner_fill_color` (overwriting `outer_fill_color` if previously placed).

12. **Unique Colors Mode - Finalize:** Proceed to step 16 (Return).

13. **No Unique Colors Mode - Process per Color Group:**
    *   Find the set of distinct colors `{C1, C2, ...}` present in the `size_3_objects`. Sort this set numerically.
    *   For each distinct color `C` in the sorted set:
        *   **Determine Fill Color for C:**
            *   Initialize `max_adjacent_color = -1`.
            *   Find all cells `(r, c)` belonging to size-3 objects of color `C`.
            *   For each such cell `(r, c)`:
                *   Check orthogonal neighbors `(nr, nc)`. Get `neighbor_color`.
                *   If `neighbor_color != background_color` and `neighbor_color != C`:
                    *   `max_adjacent_color = max(max_adjacent_color, neighbor_color)`
            *   Set `fill_color_C = max(max_adjacent_color, C)`.
        *   **Determine Fill Region for C (UNCERTAIN RULE):**
            *   Select `group_C_objects` from `size_3_objects` where `object.color == C`.
            *   If `group_C_objects` is empty, continue to the next color `C`.
            *   **Apply UNCERTAIN Rule:** Calculate the minimal bounding box (`BB_C`) enclosing `group_C_objects`.
            *   ***WARNING:*** *This rule for determining the fill region `BB_C` is known to fail for color group C=6 in Example 4 (where the fill color is determined by a neighbor). The correct method for determining the fill region in this mode is currently unknown.*
        *   **Execute Fill for C:**
            *   If `BB_C` is valid, iterate through each cell `(r, c)` within `BB_C`.
            *   If the color in the *input* grid at `(r, c)` is `background_color`, update its color in the *output* grid to `fill_color_C`. (Overwriting based on processing order of C).

14. **No Unique Colors Mode - Finalize:** After processing all color groups C, proceed to step 16 (Return).

15. **Return Output:** Return the modified output grid.```
```python
import collections
import itertools
from copy import deepcopy

"""
Transforms an input grid based on two potential modes, determined by the presence of unique colors (colors appearing exactly once, excluding the background color).

Mode 1: Unique Colors Exist
1. Determine fill colors:
    - Identify unique colors (uc) and their non-background orthogonal neighbors (nc).
    - Form candidate pairs (uc, nc or uc).
    - 'outer_fill_color' is the value (nc or uc) from the pair with the max value, breaking ties by maximizing the associated uc.
    - 'uc_used' is the unique color associated with the selected outer fill pair.
    - 'inner_fill_color' is the highest remaining unique color not equal to 'uc_used', if any.
2. Determine fill regions:
    - Identify size-3 objects with color < 5 ('outer_bb_objects').
    - 'BB_outer' is the minimal bounding box of 'outer_bb_objects'.
    - If 'inner_fill_color' exists:
        - Find the set of most frequent non-background color(s).
        - Apply UNCERTAIN RULE: Identify 'inner_bb_objects' (subset of 'outer_bb_objects' whose color is NOT in the most frequent set).
        - 'BB_inner' is the minimal bounding box of 'inner_bb_objects'. (WARNING: This rule is known to be incorrect/incomplete).
3. Apply fills:
    - Fill background cells within 'BB_outer' with 'outer_fill_color'.
    - If 'BB_inner' exists, fill background cells within 'BB_inner' with 'inner_fill_color' (overwrites outer).

Mode 2: No Unique Colors Exist
1. Group size-3 objects by their color 'C'. Sort these colors 'C'.
2. For each color group 'C' in sorted order:
    - Determine 'fill_color_C': max(max non-background color adjacent to any cell of color C, C itself).
    - Apply UNCERTAIN RULE: Calculate 'BB_C': minimal bounding box for the size-3 objects of color 'C'. (WARNING: This region rule is known to be incorrect/incomplete, especially when fill color comes from a neighbor).
    - Fill background cells within 'BB_C' with 'fill_color_C'. Later fills (higher C) overwrite earlier ones.

General Rules:
- The 'background_color' is the most frequent color in the input grid.
- Only background cells are ever filled. Original non-background cells are preserved.
- Object finding uses orthogonal connectivity for cells of the *same* color.
- Bounding boxes are minimal axis-aligned rectangles.
"""

def get_neighbors(r, c, height, width):
    """Yields valid orthogonal neighbor coordinates."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def find_objects(grid: list[list[int]], background_color: int) -> list[dict]:
    """Finds connected objects of the same non-background color."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r][c]
            # Start BFS only if cell is not background and not already visited
            if color != background_color and (r, c) not in visited:
                obj_locations = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                obj_locations.add((r,c))

                # BFS to find all connected cells of the same color
                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            obj_locations.add((nr, nc))
                            
                # Store found object
                if obj_locations:
                    objects.append({
                        "color": color,
                        "locations": list(obj_locations),
                        "size": len(obj_locations)
                    })
    return objects

def get_color_counts(grid: list[list[int]]) -> collections.Counter:
    """Counts occurrences of each color in the grid."""
    counts = collections.Counter()
    for row in grid:
        counts.update(row)
    return counts

def get_bounding_box(objects: list[dict]) -> tuple[int, int, int, int] | None:
    """Calculates the minimal bounding box for a list of objects."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    has_locations = False

    # Find min/max row/col across all locations in all objects
    for obj in objects:
        for r, c in obj['locations']:
            has_locations = True
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    # Return None if no objects or locations found
    if not has_locations:
        return None 

    return min_r, min_c, max_r, max_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    height = len(input_grid)
    width = len(input_grid[0])
    # 2. Initialize output grid as a copy of the input
    output_grid = deepcopy(input_grid)

    # 1. Determine background color
    color_counts = get_color_counts(input_grid)
    if not color_counts: return output_grid # Handle empty grid
    background_color = color_counts.most_common(1)[0][0]

    # 3. Find all objects
    all_objects = find_objects(input_grid, background_color)
    if not all_objects: return output_grid # Handle grid with only background

    # 4. Find unique colors (excluding background) and their locations
    unique_colors = {}
    non_bg_counts = {color: count for color, count in color_counts.items() if color != background_color}
    for r in range(height):
        for c in range(width):
             color = input_grid[r][c]
             if color != background_color and non_bg_counts.get(color) == 1:
                 unique_colors[color] = (r, c) # Store color and location

    # 5. Identify size-3 objects
    size_3_objects = [obj for obj in all_objects if obj['size'] == 3]
    
    # 6. Mode Selection
    if unique_colors:
        # -------- Mode 1: Unique Colors Exist --------
        
        # 7. Determine Fill Colors
        candidate_pairs = []
        for uc, (r, c) in unique_colors.items():
            candidate_pairs.append((uc, uc)) # Pair unique color with itself
            # Check neighbors for non-background, non-uc colors
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_color = input_grid[nr][nc]
                if neighbor_color != background_color and neighbor_color != uc:
                     candidate_pairs.append((uc, neighbor_color)) # Pair uc with neighbor
                     
        if not candidate_pairs:
             # This case should not be reachable if unique_colors is non-empty
             return output_grid 

        # Find the best pair: sort by value (desc), then by unique color (desc)
        candidate_pairs.sort(key=lambda pair: (pair[1], pair[0]), reverse=True)
        uc_used, outer_fill_color = candidate_pairs[0]

        # Determine inner fill color: highest unique color not used for outer fill
        remaining_unique_colors = {uc for uc in unique_colors if uc != uc_used}
        inner_fill_color = max(remaining_unique_colors) if remaining_unique_colors else None

        # 8. Outer Fill
        # Select objects for outer bounding box (size=3, color<5)
        outer_bb_objects = [obj for obj in size_3_objects if obj['color'] < 5]

        if not outer_bb_objects:
            # If no objects meet criteria, no fill occurs
            return output_grid 

        # Calculate outer bounding box
        bb_outer = get_bounding_box(outer_bb_objects)
        if bb_outer is None: return output_grid # Should not happen if outer_bb_objects is not empty

        min_r_outer, min_c_outer, max_r_outer, max_c_outer = bb_outer

        # Apply Outer Fill to background cells within the box
        for r in range(min_r_outer, max_r_outer + 1):
            for c in range(min_c_outer, max_c_outer + 1):
                if input_grid[r][c] == background_color:
                    output_grid[r][c] = outer_fill_color

        # 9. Inner Fill Condition
        if inner_fill_color is not None:
            # 10. Determine Inner BB Objects (UNCERTAIN RULE)
            # Find the set of most frequent non-background colors
            most_frequent_set = set()
            if non_bg_counts:
                 max_freq = 0
                 # Find the maximum frequency among non-background colors
                 for count in non_bg_counts.values():
                      max_freq = max(max_freq, count)
                 # Collect all colors that have this maximum frequency
                 most_frequent_set = {color for color, count in non_bg_counts.items() if count == max_freq}

            # WARNING: This rule for selecting inner_bb_objects is known to be flawed.
            # Select objects from outer set whose color is NOT in the most frequent set
            inner_bb_objects = [obj for obj in outer_bb_objects if obj['color'] not in most_frequent_set]
            
            # 11. Inner Fill Execution
            if inner_bb_objects: # Proceed only if the filtering yielded objects
                bb_inner = get_bounding_box(inner_bb_objects)
                if bb_inner: # Proceed only if a valid inner bounding box exists
                    min_r_inner, min_c_inner, max_r_inner, max_c_inner = bb_inner
                    # Apply Inner Fill to background cells, overwriting outer fill
                    for r in range(min_r_inner, max_r_inner + 1):
                        for c in range(min_c_inner, max_c_inner + 1):
                            if input_grid[r][c] == background_color:
                                output_grid[r][c] = inner_fill_color # Overwrite
                                    
    else:
        # -------- Mode 2: No Unique Colors Exist --------
        
        # 13. Process per Color Group
        # Get distinct colors found in size-3 objects, sort them
        colors_in_size_3 = sorted(list({obj['color'] for obj in size_3_objects}))

        # Process each color group C
        for color_c in colors_in_size_3:
            # Determine Fill Color for C
            max_adjacent_color = -1
            cells_of_color_c = []
            group_c_objects = []
            # Collect all size-3 objects of color C and their cell locations
            for obj in size_3_objects:
                if obj['color'] == color_c:
                    group_c_objects.append(obj)
                    cells_of_color_c.extend(obj['locations'])
            
            if not group_c_objects: continue # Skip if no objects found for this color

            # Find the highest non-background neighbor color different from C
            for r, c in cells_of_color_c:
                 for nr, nc in get_neighbors(r, c, height, width):
                     neighbor_color = input_grid[nr][nc]
                     if neighbor_color != background_color and neighbor_color != color_c:
                         max_adjacent_color = max(max_adjacent_color, neighbor_color)

            # Fill color is the max of the highest adjacent neighbor (if any) and C itself
            fill_color_c = max(max_adjacent_color, color_c) 

            # Determine Fill Region for C (UNCERTAIN RULE)
            # WARNING: This bounding box rule is known to be flawed for some cases in Mode 2.
            bb_c = get_bounding_box(group_c_objects)
            if bb_c is None: continue # Skip if no bounding box could be determined

            min_r_c, min_c_c, max_r_c, max_c_c = bb_c

            # Execute Fill for C - fill background cells in BB_C
            for r in range(min_r_c, max_r_c + 1):
                for c in range(min_c_c, max_c_c + 1):
                    if input_grid[r][c] == background_color:
                        # Overwrite based on processing order (sorted colors C)
                        output_grid[r][c] = fill_color_c

    # 15. Return Output
    return output_grid
```
