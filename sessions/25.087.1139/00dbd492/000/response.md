*   **Perception:**
    *   The input grids contain a white background (0) and one or more objects made of red (2) pixels.
    *   These red objects appear as hollow rectangular or square-like shapes.
    *   Crucially, each hollow red shape encloses exactly one disconnected red pixel within its boundary.
    *   The output grids are identical to the input grids, except that the white space *inside* each hollow red shape is filled with a new color.
    *   The original red border and the single internal red pixel remain red in the output.
    *   The color used for filling the interior varies between shapes and examples. The fill colors observed are green (3), yellow (4), and azure (8).
    *   The specific fill color for a shape seems to depend on the vertical position of the single internal red pixel relative to the top edge of its enclosing shape.

*   **Facts YAML:**
    
```yaml
    Input_Grid:
      Properties:
        - Background: White (0)
        - Contains: Red_Objects
    Red_Objects:
      Properties:
        - Color: Red (2)
        - Type: May be multiple per grid
        - Structure: Hollow, roughly rectangular/square shapes
        - Contains:
            - Outer_Border: Contiguous red pixels forming the shape boundary.
            - Interior: White (0) pixels enclosed by the Outer_Border.
            - Internal_Pixel: A single Red (2) pixel located within the Interior, not connected to the Outer_Border.
      Relationships:
        - The Internal_Pixel's vertical position relative to the top of the Outer_Border's bounding box determines the Fill_Color.
    Transformation:
      Action: Fill Interior
      Target: White (0) pixels within the Interior of each Red_Object.
      Condition: Only applies to Red_Objects containing an Internal_Pixel.
      Parameters:
        - Fill_Color: Determined by the relative row index of the Internal_Pixel.
          - Relative Row Index 2: Azure (8)
          - Relative Row Index 3: Yellow (4)
          - Relative Row Index 4: Green (3)
      Output_Grid:
        - Preserves: White background, Red Outer_Borders, Red Internal_Pixels.
        - Modifies: Interior white pixels are changed to the determined Fill_Color.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct groups of connected red (2) pixels in the input grid.
    2.  For each red group, analyze its structure to determine if it represents a hollow shape (an "Outer Border") enclosing both white (0) pixels (the "Interior") and at least one disconnected red pixel (an "Internal Pixel"). Focus on shapes with exactly one Internal Pixel.
    3.  For each such identified hollow shape with a single Internal Pixel:
        a.  Determine the bounding box of the Outer Border (minimum and maximum row and column indices).
        b.  Find the coordinates (row, column) of the single Internal Pixel.
        c.  Calculate the relative row index of the Internal Pixel: `relative_row = Internal_Pixel_row - bounding_box_min_row`.
        d.  Select the fill color based on the `relative_row`:
            *   If `relative_row` is 2, the fill color is Azure (8).
            *   If `relative_row` is 3, the fill color is Yellow (4).
            *   If `relative_row` is 4, the fill color is Green (3).
        e.  Identify all white (0) pixels that are located within the Interior of this specific Outer Border.
        f.  In the output grid, change the color of these identified Interior white pixels to the selected fill color.
    4.  Copy all other pixels (the Outer Borders, the Internal Pixels, and any pixels not part of these structures) from the input grid to the output grid without modification.
    5.  Return the modified grid as the output.