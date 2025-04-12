**Refined Perception:**

The fourth example (`train_4`) reinforces the core concepts identified earlier: Anchor Column, Static Objects, and Mover Objects, but clarifies their interactions and specific transformation rules.

1.  **Anchor Column:** Confirmed. It's a column with specific, preserved non-background value(s) (`5` in `train_4`). Its position determines the relative positions for mover rules.
2.  **Static Objects:** Confirmed (`3` in `train_4`). These are non-anchor, non-mover values preserved in place initially.
3.  **Mover Objects:** Confirmed (`8` in `train_4`). Transformation depends on value (`M`) and relative position to the anchor column (`anc_c`).
    *   **Left-Side Movers (`c < anc_c`):** The specific vertical (`dr`) and horizontal (`dc`) shifts depend on *both* the relative column (`rel_c`) *and* the mover value (`M`).
        *   `M=4`: `rel_c=-1` -> (0, 0); `rel_c=-2` -> (-2, +1)
        *   `M=3`: `rel_c=-1` -> (-1, 0); `rel_c=-2` -> (-1, +1)
        *   `M=8`: `rel_c=-1` -> (-4, 0); `rel_c=-2` -> (-4, +1)
    *   **Right-Side Movers (`c > anc_c`):** Observed only for `M=7` (Train 3), involving preservation of one element adjacent to the anchor and generation of a new shape relative to static objects.
    *   **Movers far from anchor (`|c - anc_c| > 2`):** Removed.
4.  **Collision/Overwrite Priority:** Example `train_4` significantly clarifies this. The final state of a cell seems determined by the *last* action applied to it, with movers potentially overwriting static objects. A likely order is:
    1.  Initialize with background.
    2.  Place Static objects.
    3.  Place Anchor column values.
    4.  Place results of Mover transformations (potentially overwriting Static).
    5.  Place results of Conditional Generation (potentially overwriting previous steps).
5.  **Conditional Generation:** This appears specific to the Mover value and whether successful moves originated from `rel_c = -2` (for left-side movers).
    *   `M=4`: Place `M` at `(0, anc_c)`.
    *   `M=8`: Place `M` at `(0, anc_c - 1)`.
    *   `M=3, M=7`: No equivalent rule observed.

**Updated YAML Facts:**

```yaml
task_type: grid_transformation
grid_properties:
  variable_dimensions: true # Examples: 7x7, 12x12, 17x17, 10x10
  variable_background: true # Examples: 0, 7, 1, 0
  value_set: [0, 1, 2, 3, 4, 5, 7, 8, 9] # Combined from examples
object_roles:
  - role: anchor
    values_observed: [[2, 8], [2], [2], [5]] # Per example
    behavior: Located in a single column (anc_c). Preserved in place in the output, overwriting background/static if necessary.
  - role: static
    values_observed: [null, [4], [9], [3]] # Per example
    behavior: Preserved in place initially, but can be overwritten by mover or conditional generation steps. May act as reference points for right-side mover generation.
  - role: mover
    values_observed: [4, 3, 7, 8] # Per example
    behavior: Transformation depends on mover value (M), relative position to anchor (left/right), and potentially static objects. Resulting placements overwrite previous cell values.
    left_rules: # Apply if mover coords are mostly < anc_c
      - relative_column: -1
        action: Shift (dr, dc) depends on M. Place M at (r+dr, c+dc) if valid coords.
            # M=4: (0,0); M=3: (-1,0); M=8: (-4,0)
      - relative_column: -2
        action: Shift (dr, dc) depends on M. Place M at (r+dr, c+dc) if valid coords. Track success.
            # M=4: (-2,+1); M=3: (-1,+1); M=8: (-4,+1)
      - relative_column: other
        action: Remove.
      - conditional_generation: If successful move occurred from rel_col -2:
          # M=4: Place 4 at (0, anc_c).
          # M=8: Place 8 at (0, anc_c - 1).
          # Overwrites previous value.
    right_rules: # Apply if mover coords are mostly > anc_c (Observed for M=7)
      - preservation_rule: Preserve mover M at (r, anc_c + 1) if input(r, anc_c) is anchor. Store location (pr, pc). Overwrite previous value.
      - removal_rule: Remove other input mover locations (effectively overwritten by background or generated shape).
      - generation_rule: Generate a new shape ('V' for M=7) using mover color M, positioned relative to static object(s) and (pr, pc). Place M at shape coords, overwriting previous values.
overwrite_logic:
  priority: Appears sequential based on transformation steps. Later steps overwrite earlier ones.
  order:
    1. Background Initialization
    2. Static Placement
    3. Anchor Placement
    4. Mover Transformation Placement
    5. Conditional/Shape Generation Placement
```

**Updated Natural Language Program (v4):**

1.  Determine the grid dimensions (`H`, `W`) and the background color (`B`) from the input grid (`inp`).
2.  Create an output grid (`out`) of dimensions `H`x`W`, initialized with `B`.
3.  Identify the Anchor object value(s) (`A`) and their column index `anc_c`.
4.  Identify the Mover color (`M`) and any Static color(s) (`S`).
5.  Find all locations `(r, c)` where `inp[r, c]` is a Static color `S`. For each, set `out[r, c] = inp[r, c]`. Store Static object properties (like column `static_c`, `min_r_S`, `max_r_S` for Train 3 '9's) if needed for later steps.
6.  Copy the anchor column: For `r` from 0 to `H-1`, set `out[r, anc_c] = inp[r, anc_c]`.
7.  Find all locations `(r, c)` of the Mover color `M` in the input: `input_M_coords`.
8.  Determine if `input_M_coords` are primarily located LEFT (`< anc_c`) or RIGHT (`> anc_c`) of the anchor column.

9.  **IF Mover location is primarily LEFT:**
    a.  Initialize flag `made_move_from_minus_2 = false`.
    b.  Determine shifts based on `M`:
        *   If `M=4`: `(dr1, dc1)=(-0, 0)`, `(dr2, dc2)=(-2, +1)`
        *   If `M=3`: `(dr1, dc1)=(-1, 0)`, `(dr2, dc2)=(-1, +1)`
        *   If `M=8`: `(dr1, dc1)=(-4, 0)`, `(dr2, dc2)=(-4, +1)`
        *   Else: (Define default/error behavior if M is unknown left-mover)
    c.  Create a list `mover_placements` to store `(target_row, target_col)`.
    d.  For each `(r, c)` in `input_M_coords`:
        i.  If `c == anc_c - 1`: `tr, tc = r + dr1, c + dc1`. Add `(tr, tc)` to `mover_placements`.
        ii. If `c == anc_c - 2`: `tr, tc = r + dr2, c + dc2`. Add `(tr, tc)` to `mover_placements`. Mark that a potential move from col -2 exists.
    e.  Process `mover_placements`: For each `(tr, tc)`:
        i.  If `0 <= tr < H` and `0 <= tc < W`:
            *   Set `out[tr, tc] = M`.
            *   If the source column for this move was `anc_c - 2`, set `made_move_from_minus_2 = true`.
    f.  Apply Conditional Generation:
        *   If `M == 4` and `made_move_from_minus_2` and `0 <= anc_c < W`: Set `out[0, anc_c] = 4`.
        *   If `M == 8` and `made_move_from_minus_2` and `0 <= anc_c - 1 < W`: Set `out[0, anc_c - 1] = 8`.

10. **ELSE IF Mover location is primarily RIGHT (currently only M=7 logic):**
    a.  Initialize `preserved_mover_coord = None`.
    b.  Find the Static object properties (`static_c`, `min_r_S`, `max_r_S` for '9's in Train 3).
    c.  For each `(r, c)` in `input_M_coords`:
        i.  If `c == anc_c + 1` and `inp[r, anc_c]` is an anchor color:
            *   Set `out[r, c] = M`.
            *   Store `preserved_mover_coord = (r, c)`.
            *   (Assume only one such preserved point based on Train 3).
    d.  If `preserved_mover_coord = (pr, pc)` is found:
        i.  Generate the list of coordinates `shape_coords` for the 'V' shape relative to `(pr, pc)` and the static object properties (as detailed in thought block).
        ii. For each `(gr, gc)` in `shape_coords`:
            *   If `0 <= gr < H` and `0 <= gc < W`: Set `out[gr, gc] = M`.

11. **ELSE (Mover position unclear / mixed / No specific rule matched):**
    a.  (No examples yet, define behavior - perhaps default to no action for Mover).

12. Return the final `out` grid.