*   **Perception**: The task involves transforming grids containing white (0) and green (3) pixels into grids containing white (0), green (3), and azure (8) pixels. The transformation specifically targets some of the green pixels, changing their color to azure, while leaving white pixels and other green pixels unchanged. The core challenge is to identify the rule that determines which green pixels are transformed. By analyzing the examples, it appears the transformation is related to the concept of connected components of green pixels, where connectivity includes both orthogonal and diagonal neighbors. The green pixels belonging to the single largest connected component (by pixel count) are the ones that change color to azure.

*   **Facts**:
    
```yaml
    task_elements:
      - Input Grid: A 2D array of pixels with values 0 (white) or 3 (green).
      - Output Grid: A 2D array of pixels derived from the input, containing values 0 (white), 3 (green), or 8 (azure).
      - Target Pixels: Pixels with value 3 (green) in the input grid.
      - Background Pixels: Pixels with value 0 (white) in the input grid.

    objects:
      - type: Pixel
        properties:
          - color: White (0), Green (3), Azure (8)
          - position: (row, column) coordinates
      - type: Connected Component
        description: A group of green pixels where each pixel is connected to at least one other pixel in the group either orthogonally or diagonally.
        properties:
          - pixels: List of pixel coordinates belonging to the component.
          - size: The total number of pixels in the component.
          - color: Initially Green (3).

    relationships:
      - Connectivity: Green pixels can be connected orthogonally or diagonally to form components.
      - Size Comparison: Connected components can be compared based on their size (number of pixels).

    actions:
      - Identify Connected Components: Find all groups of connected green pixels in the input grid.
      - Calculate Component Sizes: Determine the number of pixels in each identified component.
      - Find Largest Component: Identify the connected component with the maximum number of pixels. (Assumption based on examples: there is a unique largest component).
      - Color Change: Change the color of all pixels belonging to the largest identified component from green (3) to azure (8).
      - Maintain Others: Keep the color of all white pixels and green pixels not belonging to the largest component unchanged.

    state_changes:
      - Green pixels (3) within the largest connected component become Azure pixels (8).
      - All other pixels retain their original color.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all connected components of green pixels (value 3) in the input grid. Consider pixels connected if they are adjacent horizontally, vertically, or diagonally.
    3.  Calculate the size (number of pixels) for each identified green component.
    4.  Determine the maximum size among all green components.
    5.  Identify the single green component that has this maximum size.
    6.  For every pixel coordinate belonging to this largest green component, change the color in the output grid at that coordinate from green (3) to azure (8).
    7.  Return the modified output grid.