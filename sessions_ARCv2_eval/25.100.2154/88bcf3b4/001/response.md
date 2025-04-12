**Refined Perception:**

The task involves transforming an input grid into an output grid of the same dimensions. The transformation rules appear centered around a specific "anchor" column, identifiable by a consistent set of non-background values ('2' and '8' in the first example, '2' in the second). The background color itself varies between examples ('0' vs '7').

Other numbers in the grid behave differently based on their value and their column's position relative to the anchor column:

1.  **Anchor Column:** Values in this column are preserved in the output.
2.  **Static Values:** Some numbers (like '4' in the second example) might exist independently and remain unchanged, regardless of the anchor column or other transformations.
3.  **Mover Values:** Other numbers (like '4' in the first example, '3' in the second) change position based on rules dependent on *both* their specific value *and* their column's distance from the anchor column.
    *   Movers in the column immediately left (relative position -1) of the anchor column either stay put (if value is '4') or move up one row (if value is '3').
    *   Movers in the column two positions left (relative position -2) of the anchor column move right one column and up a number of rows dependent on their value (up 2 if '4', up 1 if '3').
    *   Movers in any other column are removed.
4.  **Collision Handling:** When a move targets a cell already occupied (e.g., by a preserved value from column -1), the move is cancelled. Moves from column -1 seem to have priority over moves from column -2 targeting the same cell.
5.  **Conditional Generation:** A specific condition (mover value '4' combined with successful moves originating from column -2) triggers the placement of a '4' at the top of the anchor column in the output.

The grid dimensions also vary between examples (7x7 vs 12x12), indicating the rules must be independent of a fixed size.

**Updated YAML Facts:**

```yaml
task_type: grid_transformation
grid_properties:
  variable_dimensions: true # Example 1: 7x7, Example 2: 12x12
  variable_background: true # Example 1: 0, Example 2: 7
  value_set: [0, 2, 3, 4, 7, 8] # Combined from examples
anchor_column_behavior:
  identification: Contains a consistent set of non-background values (e.g., [2, 8] or [2]).
  action: Preserve all values in this column in the output.
value_specific_behaviors:
  - value: 4 # Based on train_1 (as mover) and train_2 (as static)
    roles: [mover, static]
    static_behavior: # Observed in train_2
      condition: If not acting as a mover relative to an anchor column.
      action: Preserve original position.
    mover_behavior: # Observed in train_1
      condition: If identified as the primary mover value relative to the anchor column.
      rules:
        - relative_column: -1 # One column left of anchor
          action: Preserve position (move up 0, right 0).
        - relative_column: -2 # Two columns left of anchor
          action: Move up 2 rows, right 1 column.
        - relative_column: other
          action: Remove.
      generation_trigger: # Observed in train_1
        condition: At least one successful move occurred from relative_column -2.
        action: Place '4' at row 0 of the anchor column.
  - value: 3 # Based on train_2 (as mover)
    roles: [mover]
    mover_behavior:
      condition: If identified as the primary mover value relative to the anchor column.
      rules:
        - relative_column: -1 # One column left of anchor
          action: Move up 1 row, right 0 columns.
        - relative_column: -2 # Two columns left of anchor
          action: Move up 1 row, right 1 column.
        - relative_column: other
          action: Remove.
  - value: [2, 8] # Based on train_1 and train_2 (as anchor components)
    roles: [anchor]
    anchor_behavior:
      action: Define the anchor column; preserve position within that column.
collision_resolution:
  priority:
    - Anchor column preservation
    - Static value preservation
    - Mover transformations from relative_column -1
    - Mover transformations from relative_column -2
  mechanism: If a target cell for a lower-priority move is already occupied, the move is cancelled.
```

**Updated Natural Language Program (v2):**

1.  Determine the grid dimensions (height `H`, width `W`) and the background color from the input grid.
2.  Create an output grid of dimensions `H`x`W`, initialized with the background color.
3.  Identify the "anchor column" (`anc_c`) by finding the column containing a consistent pattern of specific non-background values (e.g., '2's, or '2's and '8's).
4.  Identify the "mover" value (`M`) for this task (e.g., '4' in example 1, '3' in example 2). Assume only one mover value per task instance.
5.  Identify any "static" values (`S`) that are preserved in place independently (e.g., '4' in example 2, when '3' is the mover).
6.  Copy the identified anchor column (`anc_c`) entirely from the input to the output grid.
7.  Copy all instances of static values (`S`) from their input positions to the same positions in the output grid.
8.  Create two lists to store potential moves for the mover value `M`: `moves_col_minus_1` and `moves_col_minus_2`.
9.  Initialize a flag `made_move_from_minus_2 = false`.
10. Iterate through each cell `(r, c)` of the input grid:
    a.  If the value `input[r, c]` is the mover value `M`:
        i.  Calculate the relative column `rel_c = c - anc_c`.
        ii. If `rel_c == -1`:
            *   Determine target position `(tr, tc)` based on `M`:
                *   If `M == 4`, target is `(r, c)`.
                *   If `M == 3`, target is `(r - 1, c)`.
            *   Add `(tr, tc)` to `moves_col_minus_1`.
        iii. If `rel_c == -2`:
            *   Determine target position `(tr, tc)` based on `M`:
                *   If `M == 4`, target is `(r - 2, c + 1)`.
                *   If `M == 3`, target is `(r - 1, c + 1)`.
            *   Add `(tr, tc)` to `moves_col_minus_2`.
11. Process moves from `moves_col_minus_1`:
    a.  For each target position `(tr, tc)` in `moves_col_minus_1`:
        i.  If `tr` is within grid bounds (>= 0) and the cell `output[tr, tc]` currently holds the background color, place the mover value `M` at `output[tr, tc]`.
12. Process moves from `moves_col_minus_2`:
    a.  For each target position `(tr, tc)` in `moves_col_minus_2`:
        i.  If `tr` is within grid bounds (>= 0) and the cell `output[tr, tc]` currently holds the background color:
            *   Place the mover value `M` at `output[tr, tc]`.
            *   Set `made_move_from_minus_2 = true`.
13. Apply conditional generation rule:
    a.  If the mover value `M` is '4' *and* `made_move_from_minus_2` is `true`:
        i.  Place '4' at `output[0, anc_c]`, overwriting any existing value.
14. The final `output` grid is the result.