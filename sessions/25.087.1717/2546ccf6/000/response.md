*   **Perception:** The input and output grids are structured grids separated by lines of a single color (Red in example 1, Magenta in example 2). These lines divide the grid into a 3x3 arrangement of smaller, equally-sized subgrids. The background is white (0). Some subgrids contain patterns made of another single color (Green or Blue in example 1, Yellow in example 2), while others are empty (white). The transformation modifies the content of some subgrids based on the content of the subgrid below them and the content of the central subgrid.

*   **YAML Facts:**
    
```yaml
    grid_structure:
      type: partitioned
      rows: 3
      cols: 3
      separator_color: dynamically determined (e.g., Red=2, Magenta=6)
      separator_lines: horizontal and vertical
      subgrid_size: dynamically determined (e.g., 4x4, 4x4) # Note: example 1 subgrids are 4x4, example 2 are 4x4. Need to confirm dimensions carefully. Let's recheck. Ex1: 19x18. Separators rows 4, 9, 14. Separator cols 4, 9, 14. Subgrids: rows 0-3, 5-8, 10-13 (size 4). cols 0-3, 5-8, 10-13 (size 4). Yes, 4x4. Ex2: 17x19. Separators rows 4, 9, 14. Separator cols 4, 9, 14. Subgrids: rows 0-3, 5-8, 10-13 (size 4). cols 0-3, 5-8, 10-13 (size 4). Yes, 4x4.
      background_color: White (0)
    objects:
      - type: separator_lines
        color: Red(2) or Magenta(6)
      - type: subgrid_pattern
        color: Green(3), Blue(1), Yellow(4)
        location: within specific subgrids
      - type: central_subgrid_pattern
        location: subgrid at index (1, 1)
        properties: defines the 'replacement pattern' (C) and 'trigger color' (P)
    relationships:
      - type: vertical_adjacency
        description: Between subgrids (r, c) and (r+1, c)
    actions:
      - type: identification
        actor: self
        details: Identify separator color, background color, subgrid boundaries, central pattern (C), and trigger color (P).
      - type: conditional_replacement
        details: Replace content of subgrid (r, c) with central pattern C IF subgrid (r+1, c) contains the trigger color P.
        conditions:
          - Applies only to subgrids in rows 0 and 1 (r < 2).
          - Trigger condition: Subgrid below (r+1, c) must contain trigger color P.
    ```


*   **Natural Language Program:**
    1.  Parse the input grid to identify the separator color (the color forming the grid lines) and determine the boundaries and dimensions of the 9 subgrids arranged in a 3x3 layout. Identify the background color (usually white/0).
    2.  Extract the content (pattern) of the central subgrid (at row index 1, column index 1). Store this pattern as the 'replacement pattern' `C`.
    3.  Identify the primary non-background, non-separator color present within the central subgrid pattern `C`. Store this color as the 'trigger color' `P`. If no such color exists (e.g., the central subgrid is empty or only contains separators), make no changes to the grid and return the original input.
    4.  Create a copy of the input grid to serve as the output grid.
    5.  Iterate through the subgrids by their row (`r`) and column (`c`) indices in the 3x3 layout.
    6.  For subgrids where `r` is 0 or 1:
        a.  Examine the subgrid located directly below the current subgrid, at index (`r+1`, `c`).
        b.  Check if any pixel within this lower subgrid (`r+1`, `c`) has the 'trigger color' `P`.
        c.  If the trigger color `P` is found in the subgrid below, replace the content of the current subgrid (`r`, `c`) in the output grid with the 'replacement pattern' `C`.
        d.  If the trigger color `P` is *not* found, the content of the current subgrid (`r`, `c`) in the output grid remains unchanged from the input grid.
    7.  Subgrids in the last row (`r` = 2) are never modified.
    8.  Return the modified output grid.