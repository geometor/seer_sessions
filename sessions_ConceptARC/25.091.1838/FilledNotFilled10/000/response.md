*   **Perception of Task Elements:**
    The task involves grids containing primarily white (0), green (3), and yellow (4) pixels. Green pixels often form boundaries or shapes that enclose areas within the grid. Some enclosed areas contain only white pixels, while others contain a mix of white and yellow pixels, often in a checkerboard pattern. The transformation specifically targets white pixels based on their relationship with the enclosing green pixels.

*   **Facts:**
    
```yaml
    Objects:
      - Type: Boundary
        Color: green (3)
        Role: Encloses other pixels. Forms contiguous shapes or frames.
      - Type: Region
        Color: white (0)
        Role: Potential target for transformation. Exists both inside and outside green boundaries.
      - Type: Pixel
        Color: yellow (4)
        Role: Exists initially within some green boundaries, or is the result color for transformed white pixels.

    Properties:
      - Enclosure: A region is considered enclosed if it is completely surrounded by green (3) pixels, meaning any path from a pixel in the region to the grid edge must cross a green pixel.
      - Content: Enclosed regions can contain only white (0) pixels or a mix of white (0) and yellow (4) pixels.

    Actions:
      - Identify: Locate contiguous regions of white (0) pixels.
      - Check Enclosure: Determine if a white region is fully enclosed by green (3) pixels.
      - Check Content: Verify if an enclosed region contains *only* white (0) pixels.
      - Fill/Recolor: Change the color of pixels within a specific region.

    Relationships:
      - Spatial: Green pixels surround or bound white/yellow regions.
      - Conditional Transformation: The transformation (white -> yellow) only applies to white pixels if they belong to a region that is 1) entirely composed of white pixels and 2) fully enclosed by green pixels.
    ```


*   **Natural Language Program:**
    1.  Identify all contiguous regions composed exclusively of white (0) pixels.
    2.  For each identified white region, determine if it is completely enclosed by green (3) pixels. (A region is enclosed if every path from a pixel within the region to the edge of the grid passes through at least one green pixel).
    3.  If a white region is found to be completely enclosed by green pixels, change the color of all white (0) pixels within that specific enclosed region to yellow (4).
    4.  Leave all other pixels (green pixels, yellow pixels, and white pixels not part of a region fully enclosed by green) unchanged.
    5.  The output grid is the result of applying this conditional color change to the input grid.