*   **Perception:**
    *   The input grids contain a single object composed of gray pixels (5) on a white background (0).
    *   The gray object generally forms a closed or partially open boundary, like a container or a 'U' shape.
    *   The output grids retain the gray object structure.
    *   The transformation involves filling certain areas of the white background with azure pixels (8).
    *   The filled area corresponds to the region enclosed or contained by the gray object.
    *   If the gray object forms an open shape (like a 'U'), the azure fill extends outwards from the opening towards the edge of the grid.

*   **Facts:**
    
```yaml
    task_description: Fill the region enclosed by a gray boundary with azure, extending the fill outwards if the boundary is open.
    
    elements:
      - element: background
        color: white (0)
      - element: boundary
        color: gray (5)
        shape: variable, forms a contiguous structure, often resembling a container or U-shape.
      - element: fill
        color: azure (8)
        location: Replaces white pixels enclosed by the gray boundary.
    
    relationships:
      - type: spatial
        description: The gray pixels form a boundary.
      - type: containment
        description: White pixels can be 'inside' or 'outside' the region defined by the gray boundary.
    
    actions:
      - action: identify_boundary
        input: input grid
        output: coordinates of gray (5) pixels.
      - action: identify_enclosed_area
        input: input grid, boundary coordinates
        description: Determine which white (0) pixels are enclosed by the gray boundary. A white pixel is considered enclosed if it cannot reach the grid border without crossing a gray pixel.
      - action: fill_area
        input: enclosed area coordinates
        output: output grid
        description: Change the color of the identified enclosed white pixels to azure (8). Keep all other pixels (gray boundary, outside white pixels) unchanged.
    
    properties:
      - property: color_invariance
        element: boundary
        description: The gray (5) boundary pixels remain unchanged in the output.
      - property: fill_extension
        description: If the gray boundary is open, the azure fill extends from the opening to the grid edge in the direction of the opening. This is implicitly handled by the 'reachability from border' definition of enclosed area.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the basis for the output grid.
    2.  Identify all white pixels (0) located on the border (top, bottom, left, right edges) of the input grid.
    3.  Perform a flood fill starting from these border white pixels. The fill should spread to adjacent (up, down, left, right) white pixels only. The fill cannot cross gray (5) pixels. Mark all reachable white pixels as 'outside'.
    4.  Iterate through all pixels in the input grid.
    5.  If a pixel is white (0) and was *not* marked as 'outside' during the flood fill, change its color to azure (8) in the output grid.
    6.  Leave all other pixels (gray pixels and 'outside' white pixels) unchanged in the output grid.
    7.  Return the modified grid as the final output.