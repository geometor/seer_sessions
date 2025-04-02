*   **Perception:**
    *   The task involves identifying specific "marker" pixels and larger "source" objects of the same color within the input grid.
    *   The transformation copies the largest source object of a given color and places it onto the grid, centered at the location of the corresponding single marker pixel of the same color.
    *   Multiple colors can be processed independently within the same grid.
    *   Objects that are neither markers nor the largest source object for a marker remain unchanged.
    *   The original source objects also remain unchanged.

*   **YAML Facts:**
    
```yaml
    elements:
      - role: grid
        description: A 2D array of pixels with integer values 0-9 representing colors.
      - role: object
        description: A contiguous block of pixels of the same non-white color.
        properties:
          - color: The color value (1-9) of the pixels in the object.
          - size: The number of pixels comprising the object.
          - shape: The spatial arrangement of the pixels.
          - position: The coordinates (row, col) of the pixels.
          - bounding_box: The smallest rectangle enclosing the object.
          - center: The calculated center coordinate of the bounding box.
      - role: marker_pixel
        description: An object with a size of exactly one pixel.
        relationship: Corresponds to a source object of the same color.
      - role: source_object
        description: The largest object (by pixel count) of a specific color, excluding any marker pixels of that color.
        relationship: Is copied and centered onto the location of a marker pixel of the same color.

    actions:
      - name: identify_objects
        description: Find all distinct contiguous objects of non-white colors in the input grid.
      - name: classify_objects
        description: For each color present, categorize objects into single-pixel markers and potential source objects (size > 1).
      - name: find_largest_source
        description: For each color with exactly one marker pixel, identify the largest object (by pixel count) among the potential source objects of that same color.
      - name: calculate_center
        description: Determine the center coordinates for the bounding box of the largest source object and the coordinates of the marker pixel.
      - name: copy_and_place
        description: Create a copy of the largest source object's pixels. Calculate the offset required to align the center of the source object's copy with the marker pixel's location. Place the copied pixels onto the output grid at the calculated offset positions, overwriting existing pixels including the marker.
      - name: preserve_others
        description: Ensure all original pixels/objects not involved in the copy/place operation (i.e., not markers that were replaced, and not the pixels newly placed) are present in the output grid in their original positions.

    flow:
      - Input grid is analyzed to identify all colored objects.
      - For each color, objects are checked. If a color has exactly one single-pixel object (marker) and one or more larger objects, proceed.
      - The largest object of that color (the source object) is identified.
      - The source object is copied.
      - The copy is positioned on the grid such that its center aligns with the location of the marker pixel, overwriting the marker.
      - This process is repeated for all colors meeting the criteria.
      - The final grid state forms the output.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct contiguous objects (groups of same-colored, adjacent pixels) for each non-white color in the input grid.
    3.  For each color present in the grid:
        a.  Count how many objects of this color consist of exactly one pixel (these are "marker pixels").
        b.  Count how many objects of this color consist of more than one pixel (these are potential "source objects").
        c.  If there is exactly one marker pixel and at least one potential source object of this color:
            i.  Identify the source object with the largest number of pixels (the "largest source object").
            ii. Find the coordinates of the single marker pixel.
            iii. Determine the bounding box of the largest source object.
            iv. Calculate the relative coordinates of each pixel within the largest source object relative to its top-left corner of the bounding box.
            v. Calculate the center position of the largest source object's bounding box.
            vi. Calculate the top-left coordinate where the copied object should be placed so that its calculated center aligns with the marker pixel's coordinates. Handle fractional centers by rounding or truncation consistently (e.g., floor).
            vii. For each pixel in the largest source object, calculate its target position in the output grid by adding its relative coordinates (from step iv) to the calculated top-left placement coordinate (from step vi).
            viii. Place the color of the source object at these target coordinates in the *output* grid, overwriting any existing pixels at those locations (including the original marker pixel).
    4.  Return the modified output grid.