*   **Perception**: The task operates on single-row grids containing white pixels (0) and one other color (maroon, orange, or azure in the examples). The transformation involves modifying sequences of the non-white color. Specifically, isolated instances of the non-white color C are expanded horizontally into a sequence of three C's (C C C), centered on the original pixel's position. Sequences that are already three pixels long (C C C) remain unchanged. White pixels remain white unless overwritten by an expanding non-white pixel.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively 1xN grids
    objects:
      - type: pixel_sequence
        color: non-white (e.g., maroon, orange, azure)
        properties:
          - length: 1 (isolated)
          - length: 3 (triplet)
      - type: background
        color: white (0)
    actions:
      - name: expand_horizontally
        input_object: isolated non-white pixel (color C) at index i
        output_object: sequence C C C centered at index i (indices i-1, i, i+1)
        condition: The pixel at index i is non-white and is not already part of a C C C sequence.
      - name: preserve
        input_object: sequence C C C
        output_object: sequence C C C (no change)
      - name: preserve
        input_object: white pixel (0)
        output_object: white pixel (0)
        condition: Not overwritten by an expansion action.
    relationships:
      - type: adjacency
        description: The transformation depends on the immediate left and right neighbors of a non-white pixel to determine if it's isolated or part of a triplet.
      - type: position
        description: Expansion occurs symmetrically around the original position of the isolated pixel.
    invariants:
      - Grid dimensions remain the same.
      - The specific non-white color used in the input is preserved in the output.
      - White pixels remain white unless replaced by an expansion.
      - Existing C C C triplets remain unchanged.
    ```


*   **Natural Language Program**:
    1.  Initialize an output grid of the same dimensions as the input grid, filled with white (0).
    2.  Iterate through each pixel of the input grid row from left to right (index `i`).
    3.  Let the color of the current input pixel be `C`.
    4.  If `C` is white (0), continue to the next pixel.
    5.  If `C` is non-white:
        a.  Check if the pixel is part of a horizontal sequence of three identical non-white pixels (C C C). Specifically, check if the pixel at `i-1` (if `i > 0`) and the pixel at `i+1` (if `i < width-1`) are both equal to `C`.
        b.  If it *is* part of such a C C C sequence, copy the color `C` to the corresponding position `i` in the output grid.
        c.  If it *is not* part of such a sequence (meaning it's an isolated C, or at the end of a shorter sequence), then set the pixels at positions `i-1` (if `i > 0`), `i`, and `i+1` (if `i < width-1`) in the output grid to color `C`. *Correction*: This step needs refinement based on the observation that only isolated pixels expand. Let's rephrase:
    5.  If `C` is non-white:
        a. Define `left_is_C` as true if `i > 0` and `input[i-1] == C`, false otherwise.
        b. Define `right_is_C` as true if `i < width-1` and `input[i+1] == C`, false otherwise.
        c. **Condition 1 (Isolated):** If *not* `left_is_C` and *not* `right_is_C`, this is an isolated pixel. In the output grid, set pixels at `max(0, i-1)`, `i`, and `min(width-1, i+1)` to color `C`.
        d. **Condition 2 (Part of Triplet or Edge):** If `left_is_C` or `right_is_C` (meaning it's part of a sequence of 2 or 3 C's, or potentially longer, but the examples only show 1 or 3), copy the color `C` to the corresponding position `i` in the output grid. *Revisiting logic - the simplest is to handle the expansion first and then copy.*
    
    **Revised Natural Language Program**:
    1. Create a copy of the input grid to serve as the initial output grid.
    2. Iterate through each pixel of the input grid row from left to right (index `i`).
    3. Let the color of the current input pixel be `C`.
    4. If `C` is non-white:
        a. Check if the pixel at `i` is isolated horizontally. This means its left neighbor (if `i > 0`) is not `C`, and its right neighbor (if `i < width-1`) is not `C`. (Treat boundary conditions as neighbors that are not `C`).
        b. If the pixel at `i` *is* isolated, then modify the *output* grid by setting the color `C` at index `i`, and also at `i-1` (if `i > 0`) and `i+1` (if `i < width-1`).
    5. Pixels in the output grid that are not modified by step 4b retain their original color from the input grid copy.
    6. Return the modified output grid.