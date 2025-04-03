*   **Perception**: The task involves transforming an input grid containing scattered, single-colored pixels (or small groups of pixels) on a white background into an output grid where these initial pixels have "expanded" outwards, filling the surrounding white space. The expansion seems to follow specific rules:
    *   Each non-white pixel in the input acts as a "seed".
    *   These seeds expand into adjacent (cardinal directions: up, down, left, right) white pixels.
    *   The expansion continues iteratively until no more white pixels can be filled.
    *   The expansion from one seed stops when it meets the boundary of the grid, an existing non-white pixel from the input, or the expansion area of another seed.
    *   Crucially, the color used for expansion (the "fill color") is usually the same as the seed color, *except* for magenta (6) seeds, which expand using orange (7). All other colors (blue, red, green, yellow, gray, orange, azure, maroon) expand using their own color.
    *   The process appears to be simultaneous for all seeds, meaning expansions happen in parallel, respecting each other's boundaries as they form.

*   **Facts**:
    
```yaml
    objects:
      - type: grid
        properties:
          height: variable (e.g., 20, 18, 15)
          width: variable (e.g., 20, 18, 15)
          pixels: represented by integers 0-9
      - type: pixel
        properties:
          color: integer 0-9 (white, blue, red, green, yellow, gray, magenta, orange, azure, maroon)
          location: (row, column) coordinates
      - type: seed_pixel
        description: A non-white (color 1-9) pixel in the input grid.
        properties:
          color: integer 1-9
          location: (row, column)
      - type: expansion_area
        description: The region filled by the expansion process originating from one or more seed pixels of the same effective fill color.
        properties:
          fill_color: integer 1-9 (determined by seed color)

    relationships:
      - type: adjacency
        description: Pixels can be adjacent cardinally (sharing an edge) or diagonally (sharing a corner). Cardinal adjacency is relevant for expansion.
      - type: boundary
        description: Expansion stops at grid edges or pixels belonging to a different expansion area or original non-white pixels.

    actions:
      - name: identify_seeds
        description: Find all pixels in the input grid with colors 1 through 9.
      - name: determine_fill_color
        description: Assign a fill color to each seed. Magenta (6) seeds get orange (7). All other seeds get their own color.
      - name: expand_simultaneously
        description: Iteratively fill adjacent white (0) pixels with the determined fill color.
        details:
          - Start with the seed pixels considered filled.
          - In each step, identify all white pixels cardinally adjacent to any currently filled pixel.
          - For each identified white pixel, check the fill colors of its adjacent filled neighbors.
          - If all adjacent filled neighbors belong to the *same* fill color group, color the white pixel with that fill color.
          - If adjacent filled neighbors belong to *different* fill color groups, the white pixel remains white (boundary).
          - Repeat until no more white pixels can be colored in a step.

    state_changes:
      - description: White (0) pixels in the input grid are changed to non-zero colors based on the expansion rules.
      - description: Original non-white pixels remain unchanged in color and location.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all non-white pixels (colors 1-9) in the input grid. These are the initial "seed" pixels.
    3.  Create a mapping of seed locations to their "fill color". If a seed pixel has color magenta (6), its fill color is orange (7). Otherwise, its fill color is its own color.
    4.  Create a set of "active" pixels, initially containing the locations of all seed pixels.
    5.  Start an iterative expansion process:
        a.  Initialize an empty set for `next_active_pixels` and a dictionary `potential_fills` mapping coordinates `(r, c)` to a set of fill colors proposing to fill that coordinate.
        b.  For each pixel location `(r, c)` in the `active` set:
            i.  Get the fill color `fill_c` associated with this active pixel (determined in step 3).
            ii. Check its four cardinal neighbors (up, down, left, right).
            iii. For each neighbor `(nr, nc)` that is within the grid boundaries and is currently white (0) in the output grid:
                *   Add `fill_c` to the set associated with `(nr, nc)` in the `potential_fills` dictionary. If the key `(nr, nc)` doesn't exist, create it with a new set containing `fill_c`.
        c.  Iterate through the `potential_fills` dictionary:
            i.  For each coordinate `(r, c)` and its associated set of proposed fill colors `colors_set`:
                *   If `colors_set` contains exactly one color `fill_c`:
                    *   Change the color of the pixel at `(r, c)` in the output grid to `fill_c`.
                    *   Add `(r, c)` to the `next_active_pixels` set.
        d.  If `next_active_pixels` is empty, the expansion is complete; break the loop.
        e.  Otherwise, update `active` to be `next_active_pixels` and continue to the next iteration (step 5a).
    6.  Return the final state of the output grid.