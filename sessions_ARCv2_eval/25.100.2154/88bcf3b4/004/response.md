Okay, analyzing the fifth example pair (`train_5`) in the context of the previous four.

**Refined Perception:**

This example strongly confirms the core model of **Anchor**, **Static**, and **Mover** objects interacting within a grid transformation.
-   **Anchor:** Column 5 contains '6's, which are preserved, identifying '6' as the anchor value and column 5 as `anc_c`.
-   **Static:** The '3's in column 3 are preserved, identifying '3' as the static value `S`.
-   **Mover:** The '9's are the mover value `M`. They are primarily located to the left of the anchor column, triggering the "Left-Side Mover" rules.

Key refinements and confirmations from `train_5`:

1.  **Mover Shift Rules Depend on `M`:** The specific `(dr, dc)` shift applied to a mover depends heavily on the mover value `M` and its relative column `rel_c`.
    *   `rel_c = -1`: `train_5` (M=9) shows `(dr, dc) = (0, 0)`. This adds to the pattern: M=4 -> (0,0), M=3 -> (-1,0), M=8 -> (-4,0), M=9 -> (0,0).
    *   `rel_c = -2`: `train_5` (M=9) shows `(dr, dc) = (-2, 0)`. This *breaks* the previous pattern of `dc=+1` for this relative column. The new pattern for `dc` seems to be: `dc = +1` if `M != 9`, else `dc = 0`. The `dr` pattern remains specific to M: M=4 -> -2, M=3 -> -1, M=8 -> -4, M=9 -> -2.
    *   `rel_c = -3`: `train_5` introduces a rule for `rel_c = -3` specifically when `M=9`, with `(dr, dc) = (-5, 0)`. For other M values, movers at `rel_c <= -3` are still removed.
2.  **Conditional Generation Depends on `M`:** The generation of new mover values at the top of the grid (or nearby columns) also depends on `M` and seems triggered by successful moves originating from `rel_c = -2`.
    *   `M=4`: Place `4` at `(0, anc_c)`.
    *   `M=8`: Place `8` at `(0, anc_c - 1)`.
    *   `M=9`: Place `9` at `(0, anc_c - 1)` *and* `(1, anc_c - 1)`.
3.  **Overwrite Logic Confirmed:** The sequential overwrite logic (Background -> Static -> Anchor -> Movers -> Conditional Generation) holds. Movers (`9`) overwrite the background, and the conditional generation (`9`s at `(0,4)` and `(1,4)`) also overwrites the background. Previous examples showed movers overwriting static values.
4.  **Right-Side Rule Unchanged:** This example doesn't involve right-side movers, so the rule derived from `train_3` (M=7) remains unchanged but specific to M=7 for now.

**Updated YAML Facts:**

```yaml
task_type: grid_transformation
grid_properties:
  variable_dimensions: true # Examples: 7x7, 12x12, 17x17, 10x10, 9x9
  variable_background: true # Examples: 0, 7, 1, 0, 0
  value_set: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # Combined from examples
object_roles:
  - role: anchor
    values_observed: [[2, 8], [2], [2], [5], [6]] # Per example
    behavior: Located in a single column (anc_c). Preserved in place in the output, overwriting background/static if necessary.
  - role: static
    values_observed: [null, [4], [9], [3], [3]] # Per example
    behavior: Preserved in place initially, but can be overwritten by mover or conditional generation steps. May act as reference points for right-side mover generation (M=7).
  - role: mover
    values_observed: [4, 3, 7, 8, 9] # Per example
    behavior: Transformation depends on mover value (M), relative position to anchor (left/right), and potentially static objects. Resulting placements overwrite previous cell values.
    left_rules: # Apply if mover coords are mostly < anc_c
      - relative_column: -1
        action: Shift (dr, dc) = (lookup_dr1(M), 0). Place M at (r+dr, c+dc) if valid coords.
            # lookup_dr1: M=4->0, M=3->-1, M=8->-4, M=9->0
      - relative_column: -2
        action: Shift (dr, dc) = (lookup_dr2(M), lookup_dc2(M)). Place M at (r+dr, c+dc) if valid coords. Track success flag_minus_2.
            # lookup_dr2: M=4->-2, M=3->-1, M=8->-4, M=9->-2
            # lookup_dc2: M=9->0, else +1
      - relative_column: -3
        action: If M=9, Shift (dr, dc) = (-5, 0). Place M at (r+dr, c+dc) if valid coords. Track success flag_minus_3. Else remove.
            # For M!=9, this rule does not apply (effectively remove).
      - relative_column: <-3
        action: Remove.
      - conditional_generation: If flag_minus_2 is true: # Check if M=9 trigger needs flag_minus_3? Train_5 suggests flag_minus_2 is sufficient.
          # M=4: Place 4 at (0, anc_c).
          # M=8: Place 8 at (0, anc_c - 1).
          # M=9: Place 9 at (0, anc_c - 1) AND (1, anc_c - 1).
          # Overwrites previous value.
    right_rules: # Apply if mover coords are mostly > anc_c (Observed only for M=7)
      - preservation_rule: Preserve M=7 at (r, anc_c + 1) if input(r, anc_c) is anchor. Store location (pr, pc). Overwrite previous value.
      - removal_rule: Remove other input M=7 locations.
      - generation_rule: Generate a 'V' shape using M=7, positioned relative to static object(s) (S=9) and (pr, pc). Place M=7 at shape coords, overwriting previous values.
overwrite_logic:
  priority: Sequential based on transformation steps. Later steps overwrite earlier ones.
  order:
    1. Background Initialization
    2. Static Placement
    3. Anchor Placement
    4. Mover Transformation Placement (from rel_c -1, -2, -3 based on rules)
    5. Conditional/Shape Generation Placement
```

**Updated Natural Language Program (v5):**

1.  Determine the grid dimensions (`H`, `W`) and the background color (`B`) from the input grid (`inp`).
2.  Create an output grid (`out`) of dimensions `H`x`W`, initialized with `B`.
3.  Identify the Anchor object value(s) (`A`) and their column index `anc_c`.
4.  Identify the Mover color (`M`) and any Static color(s) (`S`).
5.  **Static Placement:** Find all locations `(r, c)` where `inp[r, c]` is a Static color `S`. For each, set `out[r, c] = inp[r, c]`. Store Static object properties (like column `static_c`, `min_r_S`, `max_r_S` for `train_3` S=9) if needed for right-side mover generation.
6.  **Anchor Placement:** Copy the anchor column: For `r` from 0 to `H-1`, set `out[r, anc_c] = inp[r, anc_c]`.
7.  Find all locations `(r, c)` of the Mover color `M` in the input: `input_M_coords`.
8.  Determine if `input_M_coords` are primarily located LEFT (`< anc_c`) or RIGHT (`> anc_c`) of the anchor column.

9.  **IF Mover location is primarily LEFT:**
    a.  Initialize flags `flag_minus_2 = false`, `flag_minus_3 = false`.
    b.  Define M-dependent vertical shifts:
        *   `dr1_map = {4: 0, 3: -1, 8: -4, 9: 0}`
        *   `dr2_map = {4: -2, 3: -1, 8: -4, 9: -2}`
        *   `dr3 = -5` (only for M=9)
    c.  Define M-dependent horizontal shifts:
        *   `dc1 = 0`
        *   `dc2 = 0 if M == 9 else 1`
        *   `dc3 = 0` (only for M=9)
    d.  Create a list `mover_placements` to store target coordinates `(target_row, target_col, source_rel_col)`.
    e.  For each `(r, c)` in `input_M_coords`:
        i.   `rel_c = c - anc_c`
        ii.  If `rel_c == -1`:
            *   `dr, dc = dr1_map.get(M, 0), dc1` # Default dr=0 if M unknown
            *   `tr, tc = r + dr, c + dc`
            *   Add `(tr, tc, rel_c)` to `mover_placements`.
        iii. If `rel_c == -2`:
            *   `dr, dc = dr2_map.get(M, 0), dc2` # Default dr=0 if M unknown
            *   `tr, tc = r + dr, c + dc`
            *   Add `(tr, tc, rel_c)` to `mover_placements`.
        iv.  If `rel_c == -3` and `M == 9`:
            *   `dr, dc = dr3, dc3`
            *   `tr, tc = r + dr, c + dc`
            *   Add `(tr, tc, rel_c)` to `mover_placements`.
    f.  **Mover Placement:** Process `mover_placements`. For each `(tr, tc, src_rel_c)`:
        i.   If `0 <= tr < H` and `0 <= tc < W`:
            *   Set `out[tr, tc] = M`.
            *   If `src_rel_c == -2`: Set `flag_minus_2 = true`.
            *   If `src_rel_c == -3`: Set `flag_minus_3 = true`. # Tracked, but check if needed for Cond Gen
    g.  **Conditional Generation:** (Apply only if `flag_minus_2` is true, based on observation across examples)
        *   If `M == 4` and `flag_minus_2` and `0 <= anc_c < W`: Set `out[0, anc_c] = 4`.
        *   If `M == 8` and `flag_minus_2` and `0 <= anc_c - 1 < W`: Set `out[0, anc_c - 1] = 8`.
        *   If `M == 9` and `flag_minus_2`:
            *   If `0 <= anc_c - 1 < W`: Set `out[0, anc_c - 1] = 9`.
            *   If `1 < H` and `0 <= anc_c - 1 < W`: Set `out[1, anc_c - 1] = 9`.

10. **ELSE IF Mover location is primarily RIGHT (currently only M=7 logic):**
    a.  Initialize `preserved_mover_coord = None`.
    b.  Retrieve the Static object properties (`static_c`, `min_r_S`, `max_r_S` for '9's in Train 3).
    c.  **Preservation:** For each `(r, c)` in `input_M_coords`:
        i.   If `c == anc_c + 1` and `inp[r, anc_c]` is an anchor color:
            *   Set `out[r, c] = M` (which must be 7 for this rule).
            *   Store `preserved_mover_coord = (r, c)`.
            *   (Assume only one such preserved point based on Train 3).
    d.  **Shape Generation:** If `preserved_mover_coord = (pr, pc)` is found:
        i.   Generate the list of coordinates `shape_coords` for the 'V' shape relative to `(pr, pc)` and the static object properties (as detailed previously).
        ii.  For each `(gr, gc)` in `shape_coords`:
            *   If `0 <= gr < H` and `0 <= gc < W`: Set `out[gr, gc] = M` (which is 7).

11. **ELSE (Mover position unclear / mixed / No specific rule matched):**
    a.  Leave the output grid as is (only Background, Static, Anchor populated).

12. Return the final `out` grid.