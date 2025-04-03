*   **Perception:** The input and output grids are the same size (16x16). The dominant color is orange (7), which acts as a background. Both input and output grids contain various small, scattered objects composed of different colors. The key difference between input and output is that many of these objects present in the input are removed (replaced by the orange background color) in the output. There is a consistent feature across all inputs: a horizontal line of four green (3) pixels located at row 3, columns 0 through 3. This green line object remains unchanged in all outputs. Observing the objects that remain versus those that are removed reveals a pattern related to proximity to this green line. Objects that are adjacent (sharing a side or a corner) with any part of the green line object are preserved in the output. All other objects, regardless of their color or shape, that are not adjacent to the green line are removed and replaced with the orange background color.

*   **Facts:**
    
```yaml
    task_context:
      grid_size: Fixed 16x16 for these examples.
      background_color: 7 (orange)
      objects: Contiguous blocks of non-background colors.
      anchor_object:
        shape: Horizontal line
        size: 1x4 pixels
        color: 3 (green)
        location: Fixed at row 3, columns 0-3 in all examples.
        persistence: Always present in input and output.
      relationships:
        adjacency: Objects touching the anchor object (sharing a side or corner).
      transformation:
        action: Selective removal of objects.
        rule: Objects not adjacent to the anchor object are removed.
        replacement_color: Background color 7 (orange).
    ```


*   **Natural Language Program:**
    1.  Identify the background color, which is orange (7).
    2.  Locate the specific "anchor" object: a 1x4 horizontal line of green (3) pixels. (In the examples, this is always at row 3, columns 0-3).
    3.  Identify all distinct objects in the input grid that are not the anchor object and are not the background color.
    4.  For each identified object, determine if any of its constituent pixels are adjacent (sharing a side or a corner) to any of the pixels belonging to the anchor object.
    5.  Create the output grid, initially identical to the input grid.
    6.  Iterate through all pixels of the objects identified in step 3. If an object was determined *not* to be adjacent to the anchor object (in step 4), change the color of all its constituent pixels in the output grid to the background color orange (7).
    7.  Keep the anchor object and all objects determined to be adjacent to it unchanged from the input grid.