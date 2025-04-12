
## train_1

**input:**
```
0 0 0 4 1 0 0
0 7 0 4 0 1 1
0 0 0 4 0 1 0
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 3 0 4 0 1 0
0 0 0 4 1 1 1
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 8 0 4 0 1 1
0 0 0 4 1 0 1
```


**output:**
```
0 0 0 4 7 0 0
0 7 0 4 0 7 7
0 0 0 4 0 7 0
4 4 4 4 4 4 4
0 0 0 4 3 3 0
0 3 0 4 0 3 0
0 0 0 4 3 3 3
4 4 4 4 4 4 4
0 0 0 4 8 8 0
0 8 0 4 0 8 8
0 0 0 4 8 0 8
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
1 0 0 4 0 1 0 4 1 0 1
0 1 0 4 1 1 1 4 1 0 1
1 1 1 4 1 0 1 4 0 1 0
```


**output:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
3 0 0 4 0 2 0 4 6 0 6
0 3 0 4 2 2 2 4 6 0 6
3 3 3 4 2 0 2 4 0 6 0
```

*   **Perception**:
    *   The input and output grids have the same dimensions.
    *   Both examples feature prominent yellow (4) lines, acting as separators, dividing the grid into distinct regions.
    *   In `train_1`, horizontal yellow lines separate three row-based regions. In `train_2`, one horizontal and two vertical yellow lines separate six regions (3 upper, 3 lower).
    *   Within some regions, there is a single, unique non-white (0) and non-yellow (4) colored pixel (e.g., orange (7), green (3), azure (8) in `train_1`; green (3), red (2), magenta (6) in `train_2`). These act as "source" colors.
    *   In other regions, there are patterns of blue (1) pixels. These act as "target" pixels.
    *   The transformation involves replacing the blue (1) pixels in a target region with the source color found in a corresponding source region.
    *   The correspondence relationship seems tied to the layout defined by the yellow separators. In `train_1`, the source color is in the left part of a horizontal band, and the target blues are in the right part of the *same* band. In `train_2`, the source color is in an upper region, and the target blues are in the region directly *below* it, separated by the horizontal yellow line.
    *   All pixels that are not blue (1) in the input remain unchanged in the output.

*   **Facts**:
    
```yaml
    task_description: Replace specific pixels (blue) based on colors found in related regions defined by separators (yellow).
    
    grid_properties:
      - dimensions_preserved: Yes
      - background_color: white (0)
    
    elements:
      - type: separator
        color: yellow (4)
        description: Horizontal and/or vertical lines that partition the grid.
        persistence: Unchanged between input and output.
    
      - type: source_color_pixel
        color: Any non-white (0), non-yellow (4) color.
        occurrence: Typically one unique instance per 'source' region.
        location: Found within regions defined by separators.
        persistence: Unchanged between input and output.
        role: Provides the color value for replacement.
    
      - type: target_pixel
        color: blue (1)
        occurrence: Can be multiple pixels forming patterns within 'target' regions.
        location: Found within regions defined by separators.
        persistence: Replaced in the output.
        role: Placeholder pixels to be recolored.
    
    relationships:
      - type: partitioning
        element1: separator (yellow lines)
        element2: grid
        description: Separators divide the grid into distinct regions.
    
      - type: correspondence
        element1: source_region (contains source_color_pixel)
        element2: target_region (contains target_pixels)
        description: Each target region is linked to a specific source region based on spatial arrangement relative to separators (e.g., within the same horizontal band, vertically adjacent across a separator).
    
    actions:
      - action: identify_regions
        inputs: [grid, separators]
        outputs: [list_of_regions]
    
      - action: identify_source_color
        inputs: [region]
        outputs: [source_color or None]
        description: Find the unique non-white, non-yellow color within a region.
    
      - action: identify_target_pixels
        inputs: [region]
        outputs: [list_of_blue_pixel_coordinates or None]
        description: Find all blue (1) pixels within a region.
    
      - action: map_regions
        inputs: [list_of_regions, grid_layout]
        outputs: [dictionary_mapping_target_region_to_source_region]
    
      - action: replace_pixels
        inputs: [target_pixel_coordinates, source_color]
        outputs: [modified_grid]
        description: Change the color of target pixels to the corresponding source color.
    
    ```


*   **Natural Language Program**:
    1.  Identify all yellow (4) pixels which form horizontal and/or vertical lines partitioning the grid into distinct regions.
    2.  For each region:
        a.  Check if it contains blue (1) pixels. If yes, mark it as a "target region" and store the coordinates of the blue pixels.
        b.  Check if it contains exactly one pixel of a color other than white (0), yellow (4), or blue (1). If yes, mark it as a "source region" and store this unique color as the "source color".
    3.  Determine the correspondence between target regions and source regions based on their spatial relationship relative to the yellow separators (e.g., vertically adjacent across a horizontal separator, horizontally adjacent within the same band defined by horizontal separators).
    4.  Create a copy of the input grid to serve as the output grid.
    5.  For each target region:
        a.  Identify its corresponding source region using the determined mapping.
        b.  Retrieve the source color associated with that source region.
        c.  For every blue (1) pixel coordinate stored for the target region, change the color of the pixel at that coordinate in the output grid to the retrieved source color.
    6.  Return the modified output grid.
