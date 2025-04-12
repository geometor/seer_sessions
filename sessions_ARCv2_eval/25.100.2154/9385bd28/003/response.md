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