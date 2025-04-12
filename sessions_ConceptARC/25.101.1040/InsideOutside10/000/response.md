*   **Perception of the elements:**
    *   The grids contain a background color (white, 0) and two other primary colors.
    *   One color acts as a "Subject" (green(3) in example 1, blue(1) in example 2), often forming lines or shapes.
    *   Another color acts as a "Reactant" (red(2) in example 1, yellow(4) in example 2), sometimes forming frames or scattered points.
    *   The transformation modifies only the Subject color pixels based on their cardinal neighbors.
    *   The Subject color changes to the Reactant color if adjacent to a Reactant pixel.
    *   The Subject color changes to the Background color if adjacent to the Background color *unless* it's "protected" by being adjacent to another Subject pixel that isn't changing.

*   **YAML block documenting facts:**
    
```yaml
    task_context:
      grid_properties:
        size: Variable (e.g., 12x12)
        background_color: White (0)
      objects:
        - type: Subject_Shape
          color: Green (3) in ex1, Blue (1) in ex2
          properties: Forms lines or contiguous regions. Changes based on neighbors.
        - type: Reactant_Shape
          color: Red (2) in ex1, Yellow (4) in ex2
          properties: Does not change. Influences adjacent Subject_Shape pixels.
        - type: Background
          color: White (0)
          properties: Does not change. Influences adjacent Subject_Shape pixels.
      relationships:
        - type: Adjacency (Cardinal)
          description: Determines the interaction between pixels.
      actions:
        - name: Color_Change
          target: Subject_Shape pixels
          conditions:
            - rule: If a Subject pixel is cardinally adjacent to a Reactant pixel, it changes to the Reactant color.
            - rule: If a Subject pixel is cardinally adjacent to the Background color AND NOT cardinally adjacent to a "stable" Subject pixel (one that is not changing color due to Reactant adjacency), it changes to the Background color.
            - rule: Otherwise, the Subject pixel remains its original color.
          priority: Reactant adjacency takes priority over Background adjacency. Protection by stable Subject neighbors takes priority over changing to Background.
    ```


*   **Natural language program:**
    1.  Identify the three primary colors present in the input grid: the Background color (B, typically white/0), the Subject color (S, the one that changes), and the Reactant color (R, the one that causes S to change to R).
    2.  Initialize the output grid as a copy of the input grid.
    3.  Create a list/set of coordinates, `changes_to_R`, to store Subject pixels that will change to the Reactant color.
    4.  Iterate through each pixel `(r, c)` of the input grid. If the pixel `input[r][c]` has color S, check its 4 cardinal neighbors in the input grid. If any neighbor has color R, add the coordinate `(r, c)` to the `changes_to_R` list.
    5.  Create a list/set of coordinates, `changes_to_B`, to store Subject pixels that will change to the Background color.
    6.  Iterate again through each pixel `(r, c)` of the input grid. If `input[r][c]` has color S AND its coordinate `(r, c)` is NOT in `changes_to_R`:
        a.  Check its 4 cardinal neighbors in the input grid.
        b.  Determine if it has at least one neighbor with color B (`has_B_neighbor`).
        c.  Determine if it has at least one neighbor `(nr, nc)` that is color S AND the coordinate `(nr, nc)` is NOT in `changes_to_R` (`has_protecting_S_neighbor`).
        d.  If `has_B_neighbor` is true AND `has_protecting_S_neighbor` is false, add the coordinate `(r, c)` to the `changes_to_B` list.
    7.  Modify the output grid based on the collected changes:
        a.  For each coordinate `(r, c)` in `changes_to_R`, set `output[r][c]` to color R.
        b.  For each coordinate `(r, c)` in `changes_to_B`, set `output[r][c]` to color B.
    8.  Return the final output grid.