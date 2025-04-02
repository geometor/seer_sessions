*   **Perception:**
    *   The input grids contain multiple distinct objects, defined as contiguous blocks of non-white pixels.
    *   Objects vary in color and shape across examples.
    *   A key feature is whether an object fully "encloses" or "surrounds" a pixel of a different color. An enclosed pixel is one whose eight neighbors (including diagonals) are all part of the surrounding object.
    *   The transformation rule involves selectively removing *all* objects of a specific color based on a condition applied to the entire grid's set of objects.
    *   There appear to be two distinct conditions for removal:
        1.  If *any* object in the input grid encloses a pixel of a different color, the objects to be removed are those whose color is the *minimum* numerical value among all colors of enclosing objects.
        2.  If *no* object in the input grid encloses a pixel of a different color, the objects to be removed are those whose color appears most frequently (i.e., there are more distinct objects of that color than any other color).
    *   Removing an object means replacing all its pixels with the background color (white, 0).

*   **Facts:**
    
```yaml
    elements:
      - type: grid
        description: A 2D array of pixels with integer values 0-9 representing colors. White (0) is the background.
      - type: object
        description: A contiguous block of pixels of the same non-white color.
        properties:
          - color: The integer value (1-9) of the pixels forming the object.
          - pixels: The set of coordinates constituting the object.
          - encloses_other_color: A boolean property indicating if the object surrounds at least one pixel of a different color. A pixel is surrounded if all 8 of its neighbors belong to the object.
      - type: collection
        description: The set of all distinct objects present in the input grid.

    relationships:
      - type: comparison
        description: Comparing the colors of objects within the grid.
      - type: frequency
        description: Counting the number of distinct objects for each color.
      - type: enclosure_check
        description: Determining if any object in the grid satisfies the 'encloses_other_color' property.

    actions:
      - type: identify_objects
        description: Segment the input grid into distinct objects and determine their properties (color, pixels, encloses_other_color).
      - type: conditional_selection
        description: Select a target color for removal based on the 'enclosure_check'.
        conditions:
          - if: Any object 'encloses_other_color' is true.
            action: Find the minimum color value among all objects where 'encloses_other_color' is true. This is the target color.
          - else: (No object 'encloses_other_color' is true).
            action: Count the number of distinct objects for each color. Find the color(s) with the maximum count. This is the target color (or colors, if tied).
      - type: removal
        description: Modify the grid by changing the color of all pixels belonging to objects whose color matches the target color to white (0).
        output: The modified grid.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct objects (contiguous areas of non-white pixels) in the input grid.
    2.  For each object, check if it "encloses" any pixel of a different color. A pixel is considered enclosed if all 8 of its neighbors (horizontal, vertical, and diagonal) belong to the object. Keep track of which objects enclose other colors.
    3.  Determine if *any* object in the grid encloses another color.
    4.  **If yes (at least one object encloses another color):**
        a.  Collect the colors of all objects that enclose another color.
        b.  Find the minimum numerical value among these collected colors. This is the "target removal color".
    5.  **If no (no object encloses another color):**
        a.  Count the number of distinct objects for each non-white color present in the grid.
        b.  Find the color(s) that have the highest object count. This is the "target removal color" (or colors).
    6.  Create the output grid by copying the input grid.
    7.  Iterate through all the identified objects from step 1. If an object's color matches the "target removal color" (determined in step 4 or 5), change all pixels belonging to that object in the output grid to white (0).
    8.  Return the modified output grid.