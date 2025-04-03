
## train_1

**input:**
```
0 0 0 4 4 4 7 4 4 4 4 4 4 8 4 4 2 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0
```


## train_2

**input:**
```
0 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 4 4 4 4 5 4 4 4 5 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids consist of a central region containing various non-white pixels, often surrounded by a border of white (0) pixels.
    *   Within the central region of the input, one non-white color usually appears more frequently than others.
    *   Other non-white colors ("interrupting colors") may be present within this central region.
    *   The output grid retains the white border pixels from the input.
    *   In the output grid, all non-white pixels within the central region are changed to the single, most frequent non-white color found in the input's central region. The interrupting colors are effectively replaced by the dominant color.

*   **Facts:**
    
```yaml
    elements:
      - type: grid
        properties:
          - contains pixels of various colors (0-9)
      - type: region
        identifier: central_region
        description: Contains all non-white (non-0) pixels in the grid.
        properties:
          - may contain multiple different non-white colors
      - type: color
        identifier: dominant_color
        description: The non-white color that appears most frequently within the central_region of the input grid.
      - type: color
        identifier: interrupting_colors
        description: Any non-white color within the central_region that is not the dominant_color.
      - type: color
        identifier: border_color
        description: The white (0) color, typically forming a border or background.

    actions:
      - action: identify
        target: central_region
        details: Select all pixels with color > 0.
      - action: count_frequency
        target: non-white colors
        scope: central_region
        details: Determine the count of each non-white color present.
      - action: determine
        target: dominant_color
        based_on: frequency counts
        details: Find the non-white color with the highest frequency.
      - action: replace
        target: interrupting_colors
        scope: central_region
        details: Change the color of all pixels identified as interrupting_colors to the dominant_color.
      - action: preserve
        target: border_color
        details: Pixels with the border_color (white/0) remain unchanged.

    relationships:
      - The dominant_color is derived from the pixel frequencies within the central_region.
      - Interrupting_colors are defined relative to the dominant_color within the central_region.
      - The transformation applies only to the non-white pixels; white pixels are unaffected.
    ```


*   **Natural Language Program:**
    1.  Examine the input grid and identify all pixels that are not white (color value is not 0).
    2.  Count the occurrences of each distinct non-white color found in step 1.
    3.  Determine the non-white color that has the highest count. This is the "dominant color".
    4.  Create a new grid, initially identical to the input grid.
    5.  Iterate through each pixel of the new grid.
    6.  If a pixel's color is non-white (not 0) *and* it is *not* the dominant color identified in step 3, change its color to the dominant color.
    7.  Leave all white pixels (color 0) and pixels already matching the dominant color unchanged.
    8.  The resulting grid is the output.
