*   **Perception:**
    The input grids contain several distinct, contiguous blocks of non-white pixels, typically rectangular, vertically stacked upon a white background. These blocks vary in color, width, and height. The transformation rearranges these blocks vertically. Observing the examples, the relative vertical order of the blocks in the output seems determined by their width. Specifically, the blocks are re-stacked in ascending order of their width, from narrowest to widest. The original content (shape and color) and height of each block are preserved. The vertical stacking in the output starts at the row where the topmost block began in the input.

*   **Facts:**
    
```yaml
    task_description: Reorder vertically stacked non-background objects based on their width.
    
    definitions:
      - object: A contiguous block of non-white pixels.
      - background_color: white (0)
    
    input_features:
      - objects:
          - properties:
              - content: The 2D array of pixel values constituting the object.
              - width: The horizontal extent of the object.
              - height: The vertical extent of the object.
              - start_row: The row index of the top-most pixel of the object.
              - color: The single color value of the object's pixels.
          - relationship: Objects are typically stacked vertically, separated by background pixels or directly adjacent. All observed objects start at column 0.
      - grid_dimensions: height and width of the input grid.
      - background: The background pixels (usually white) remain in the output unless overwritten by a rearranged object.
    
    transformation:
      - step 1: Identify all distinct contiguous non-white objects in the input grid.
      - step 2: For each object, determine its width, height, content (pixel data), and original starting row.
      - step 3: Find the minimum starting row among all identified objects (`min_start_row`).
      - step 4: Create a list representing the objects, storing their width, height, and content.
      - step 5: Sort this list of objects based primarily on their width in ascending order. If widths are equal, maintain original relative order (though not explicitly needed based on examples, it's a safe tie-breaker).
      - step 6: Initialize the output grid with the same dimensions as the input, filled with the background color (white).
      - step 7: Initialize a `current_output_row` variable to `min_start_row`.
      - step 8: Iterate through the width-sorted list of objects.
      - step 9: For each object in the sorted list, take its content and height.
      - step 10: Place the object's content onto the output grid starting at `(current_output_row, 0)`.
      - step 11: Increment `current_output_row` by the height of the object just placed.
      - step 12: The final output grid contains the rearranged objects stacked according to width.
    
    output_features:
      - grid: Same dimensions as the input.
      - background: Same background color as the input.
      - objects: The same set of objects as the input, but potentially in a different vertical order.
      - object_order: Objects are stacked vertically, starting from `min_start_row`, in ascending order of their width.
      - object_properties: Each object retains its original content, color, width, and height.
    ```


*   **Natural Language Program:**
    1.  Identify all separate, contiguous blocks of non-white pixels in the input grid. These are the 'objects'.
    2.  For each object, record its pixel data (content), its width, its height, and the row number of its top edge (start row).
    3.  Determine the overall top-most starting row (`min_start_row`) across all identified objects.
    4.  Create a list of the objects, focusing on their width, height, and content.
    5.  Sort this list of objects based on their width, from smallest width to largest width.
    6.  Create a new empty grid of the same size as the input grid, filled with the background color (white).
    7.  Set a variable `current_row` to the `min_start_row`.
    8.  Go through the sorted list of objects (from step 5):
        a.  Take the next object from the sorted list.
        b.  Copy its content (pixel data) onto the new grid, starting at position (`current_row`, 0).
        c.  Add the height of this object to `current_row`.
    9.  The new grid, now populated with the re-stacked objects, is the output.