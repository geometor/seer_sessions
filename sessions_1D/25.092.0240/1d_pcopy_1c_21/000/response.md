*   **Perception:** The task involves transforming input grids containing white backgrounds and objects of a single non-white color (orange, magenta, or red in the examples). The transformation specifically targets certain types of objects. In the input grids, there are two observed object shapes: single pixels and 1x3 horizontal lines. In the output grids, the single pixels are replaced by 1x3 horizontal lines of the same color, centered horizontally at the original pixel's location. The pre-existing 1x3 horizontal lines remain unchanged. The background color (white) is also unchanged.

*   **YAML Facts:**
    
```yaml
    task_description: "Expand single non-white pixels into 1x3 horizontal lines, leaving other shapes unchanged."
    background_color: 0 # white
    objects:
      - type: pixel
        color: non-white (variable per example: 7, 6, 2)
        shape: 1x1
        action:
          condition: "Is a single pixel (1x1 object)."
          transform: "Replace with a 1x3 horizontal line of the same color, centered at the original pixel's position."
          new_shape: 1x3 horizontal line
      - type: line
        color: non-white (variable per example: 7, 6, 2)
        shape: 1x3 horizontal
        action:
          condition: "Is not a single pixel."
          transform: "Keep unchanged."
    grid_properties:
      - size: Variable, potentially up to 30x30 (based on ARC standard)
      - background: Remains unchanged.
    relationships:
      - The transformation depends on the shape of the non-white objects.
      - The color of the transformed object is the same as the original object.
      - The position of the transformed line is relative to the original single pixel (centered).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel of the input grid.
    3.  If a pixel is non-white:
        a.  Check if this pixel forms a 1x1 object (i.e., it has no adjacent non-white neighbors horizontally or vertically).
        b.  If it is a 1x1 object:
            i.  Determine the pixel's color, row (`r`), and column (`c`).
            ii. In the output grid, change the pixels at (`r`, `c-1`), (`r`, `c`), and (`r`, `c+1`) to the determined color (ensure coordinates are within grid bounds).
    4.  Return the modified output grid. (Note: Step 1 copies existing shapes. Step 3b modifies only the single pixels, effectively leaving other shapes as they were copied in step 1).