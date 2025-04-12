**Refined Perception:**

Based on the third example, the transformation logic is more complex and context-dependent than initially hypothesized. The core concepts of an "Anchor Column" (preserved), "Static Objects" (preserved), and a "Mover Object" (transformed) seem valid, but the transformation rules for the Mover depend significantly on its position relative to the Anchor and potentially the presence and position of Static objects.

1.  **Anchor Identification:** The column containing specific, often vertically aligned, non-background values (like '2' or '2' and '8') remains the anchor (`anc_c`), and its contents are copied directly to the output.
2.  **Static Object Identification:** Other non-background, non-anchor objects that do not change position significantly (like the '4's in train_2, '9's in train_3) are identified as Static. They are also copied directly to the output.
3.  **Mover Object Identification:** The remaining non-background color is the Mover (`M`). Its transformation rule appears to depend on whether its input locations are primarily to the LEFT or RIGHT of the anchor column.
4.  **Left-Side Mover Transformation (Train 1 & 2):**
    *   Movers in column `anc_c - 1` are potentially shifted vertically based on the mover color `M` (e.g., `M=4` shift 0, `M=3` shift -1) and placed in the output if the target is background.
    *   Movers in column `anc_c - 2` are potentially shifted vertically (e.g., `M=4` shift -2, `M=3` shift -1) and horizontally (`+1` column) and placed in the output if the target is background.
    *   Collisions are resolved by prioritizing existing output values (Anchor, Static, `anc_c - 1` moves).
    *   A conditional generation rule might apply (e.g., placing a '4' at `(0, anc_c)` if `M=4` and a successful move from `anc_c - 2` occurred).
    *   Movers further left are removed.
5.  **Right-Side Mover Transformation (Train 3):**
    *   Input movers seem largely ignored *except* for one specific case: A mover cell at `(r, anc_c + 1)` that is horizontally aligned with an anchor cell `(r, anc_c)` might be preserved in the output.
    *   A *new shape* is generated using the Mover color `M`. This shape's position and form appear determined by the location of the Static object (`S`) and potentially the single preserved mover cell adjacent to the anchor. In Train 3, this generated shape is a 'V' adjacent to the right side of the Static '9's column.
6.  **General Principles:** The background color and grid dimensions are variable. The specific values used for Anchor, Mover, and Static roles change between examples.

**Updated YAML Facts:**

```yaml
task_type: grid_transformation
grid_properties:
  variable_dimensions: true # Examples: 7x7, 12x12, 17x17
  variable_background: true # Examples: 0, 7, 1
  value_set: [0, 1, 2, 3, 4, 7, 8, 9] # Combined from examples
object_roles:
  - role: anchor
    values_observed: [[2, 8], [2], [2]] # Per example
    behavior: Located in a single column (anc_c). Preserved in place in the output.
  - role: mover
    values_observed: [4, 3, 7] # Per example
    behavior: Transformation depends on relative position to anchor (left/right) and potentially static objects.
    left_rules: # Apply if mover coords are mostly < anc_c
      - relative_column: -1
        action: Vertical shift (value-dependent), horizontal shift 0. Place if target is background.
      - relative_column: -2
        action: Vertical shift (value-dependent), horizontal shift +1. Place if target is background. Track success.
      - relative_column: <-2
        action: Remove.
      - conditional_generation: If mover=4 and successful move from rel_col -2, place 4 at (0, anc_c).
    right_rules: # Apply if mover coords are mostly > anc_c
      - preservation_rule: Preserve mover at (r, anc_c + 1) if input(r, anc_c) is anchor. Store location (pr, pc).
      - removal_rule: Remove other input mover locations.
      - generation_rule: Generate a new shape using mover color, positioned relative to static object(s) and potentially (pr, pc). (e.g., Train 3 'V' shape relative to static '9's column and (6,7)).
  - role: static
    values_observed: [null, [4], [9]] # Per example
    behavior: Preserved in place in the output. May act as reference points for mover generation.
collision_resolution:
  priority:
    - Anchor column preservation
    - Static value preservation
    - Mover transformations (left: col -1 > col -2; right: preserved > generated?) - Needs refinement.
  mechanism: If a target cell for a lower-priority action is already occupied, the action is cancelled or overwritten based on exact rules.
```

**Updated Natural Language Program (v3):**

1.  Determine the grid dimensions (`H`, `W`) and the background color (`B`) from the input grid.
2.  Create an output grid (`out`) of dimensions `H`x`W`, initialized with `B`.
3.  Identify the Anchor object(s) and their column `anc_c`. Copy the column `input[:, anc_c]` to `out[:, anc_c]`.
4.  Identify the Mover color (`M`) and any Static color(s) (`S`) by analyzing non-anchor, non-background values and their change between input and output.
5.  Identify locations of Static objects (`static_S_coords`) in the input. Copy these values to the same locations in `out`. Determine primary column (`static_c`), min/max rows (`min_r_S`, `max_r_S`) if applicable (e.g., for Train 3 '9's).
6.  Find all locations of the Mover color `M` in the input: `input_M_coords`.
7.  Determine if `input_M_coords` are primarily located LEFT (`< anc_c`) or RIGHT (`> anc_c`) of the anchor column.

8.  **IF Mover location is primarily LEFT:**
    a.  Initialize lists `potential_moves_minus_1`, `potential_moves_minus_2`.
    b.  Initialize flag `made_move_from_minus_2 = false`.
    c.  For each `(r, c)` in `input_M_coords`:
        i.  If `c == anc_c - 1`: Calculate target `(tr, tc)` based on `M`'s vertical shift rule for col -1 (e.g., `M=4` -> `(r, c)`, `M=3` -> `(r-1, c)`). Add `(tr, tc)` to `potential_moves_minus_1`.
        ii. If `c == anc_c - 2`: Calculate target `(tr, tc)` based on `M`'s vertical shift rule for col -2 (e.g., `M=4` -> `(r-2, c+1)`, `M=3` -> `(r-1, c+1)`). Add `(tr, tc)` to `potential_moves_minus_2`.
    d.  Process `potential_moves_minus_1`: For each target `(tr, tc)`, if `tr >= 0` and `out[tr, tc] == B`, set `out[tr, tc] = M`.
    e.  Process `potential_moves_minus_2`: For each target `(tr, tc)`, if `tr >= 0` and `out[tr, tc] == B`, set `out[tr, tc] = M` and set `made_move_from_minus_2 = true`.
    f.  Conditional Generation: If `M == 4` and `made_move_from_minus_2`, set `out[0, anc_c] = 4` (overwriting if necessary).

9.  **ELSE IF Mover location is primarily RIGHT:**
    a.  Initialize `preserved_mover_coord = None`.
    b.  For each `(r, c)` in `input_M_coords`:
        i.  If `c == anc_c + 1` and `input[r, anc_c]` is an anchor color: Set `out[r, c] = M`. Store `preserved_mover_coord = (r, c)`. Break loop if only one such preservation expected. (Refinement: Assumes only one is preserved based on Train 3).
    c.  Generate the new Mover shape based on `preserved_mover_coord = (pr, pc)` and Static object properties (`static_c`, `min_r_S`, `max_r_S`):
        i.  **(Segment 1 - Approach):** Define points `(pr+i, pc+i)` for `i` from 1 up to `min_r_S - pr -1`.
        ii. **(Segment 2 - Alongside):** Define points `(min_r_S + i, static_c + 1)` for `i` from 0 up to `max_r_S - min_r_S`.
        iii. **(Segment 3 - Depart):** Define points `(max_r_S + 1 + i, static_c - i)` for `i` from 0 up to `(max_r_S + 1 + i == pr + (pc-(static_c-i)))?`. Simpler: Define points mirroring Segment 1's relative `(dr, dc)`: `(+1, -1)`. Start at `(max_r_S + 1, static_c)`. Generate `(max_r_S + 1 + i, static_c - i)` until the column reaches `pc`.
        iv. For each generated point `(gr, gc)` from segments 1, 2, 3: If `gr, gc` are within bounds and `out[gr, gc] == B`, set `out[gr, gc] = M`.

10. **ELSE (Mover position unclear / mixed / No specific rule matched):**
    a. Copy input `M` locations to output? Or leave as background? (Requires more examples for this case). Assume for now leave as background if no rule applies.

11. Return the final `out` grid.