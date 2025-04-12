**Perception**

The task involves identifying specific patterns or objects within a larger input grid and assembling them into a smaller output grid. The input grid consists of a dominant background color and several smaller, distinct shapes made of various colors. Certain pixels, distinguished by their color (maroon in the first example, potentially gray or azure in the second), seem to act as "markers." These markers appear to signal which patterns should be extracted and possibly how they should be processed or arranged.

The transformation appears to consist of the following steps:
1.  **Identification:** Locate the marker pixels within the input grid.
2.  **Region Definition:** For each marker (or group of connected markers), define a specific 5-row high rectangular region (a "slice") of the input grid. The definition of this slice (its starting column and width) seems to depend on the position of the marker(s) relative to the associated non-background pattern (e.g., is the marker adjacent to the left, or contained within?).
3.  **Extraction:** Extract these 5xN slices from the input grid.
4.  **Ordering:** Arrange the extracted slices horizontally. The ordering appears to be based on the vertical position (row index) of the corresponding markers in the input grid, specifically in descending order of the minimum row index of the marker(s).
5.  **Concatenation:** Combine the ordered slices horizontally to form the final output grid.

**Facts**


```yaml
task_type: object_assembly_by_marker
components:
  - role: background
    properties:
      - color: most frequent color in the input grid (e.g., azure 8 in train_1, yellow 4 in train_2)
      - significance: ignored during extraction, defines empty space
  - role: marker_pixels
    properties:
      - color: specific color indicating patterns to extract (e.g., maroon 9 in train_1; potentially context-dependent like gray 5 or azure 8 in train_2)
      - location: either adjacent to or part of the pattern to be extracted
      - significance: identify patterns, define extraction region, determine output order
  - role: pattern_regions
    properties:
      - shape: rectangular slices, always 5 rows high
      - content: subgrids extracted from the input based on marker locations
      - relationship_to_markers:
          - adjacent_marker: slice might start at marker row, but column offset from marker column (e.g., marker column + 1)
          - internal_marker: slice might encompass the marker and the associated pattern
      - extraction_rule: precise definition of the 5xN slice relative to the marker(s)
  - role: output_grid
    properties:
      - composition: horizontal concatenation of extracted pattern_regions
      - ordering: pattern_regions are arranged based on the descending minimum row index of their corresponding marker_pixels in the input grid
      - dimensions: height is always 5 rows; width is the sum of the widths of the extracted pattern_regions

actions:
  - identify_markers: find all pixels of the specific marker color(s)
  - group_markers: identify connected components of marker pixels
  - define_region: for each marker component, determine the associated 5xN rectangular region in the input grid based on relative position to pattern
  - extract_regions: copy the pixel data from the defined regions
  - order_regions: sort the extracted regions based on the descending minimum row index of their corresponding marker component
  - concatenate: join the ordered regions horizontally

relationships:
  - marker_to_pattern: each marker component corresponds to one pattern_region to be extracted
  - marker_position_to_extraction_rule: the location of the marker relative to the pattern dictates how the 5xN region is defined
  - marker_row_to_output_order: the minimum row index of the marker component determines the horizontal position of its pattern_region in the output grid (descending order)
```


**Natural Language Program**

1.  Identify the marker color (e.g., maroon). Find all pixels of this color in the input grid.
2.  Group adjacent (including diagonal) marker pixels into connected components.
3.  For each marker component:
    a.  Determine its minimum row index (`min_marker_row`).
    b.  Define the associated 5-row high rectangular pattern region to extract from the input grid. The exact rows are `min_marker_row` to `min_marker_row + 4`. The columns depend on the marker's position relative to the nearby non-background pattern:
        i.  If the marker is located just to the left of the pattern (like marker (6,6) relative to pattern starting at column 7 in train_1), the columns start one position to the right of the marker's column and extend to cover the width of the adjacent pattern.
        ii. If the marker(s) are part of or on the edge of the pattern (like markers at column 22 relative to pattern in columns 20-22 in train_1), the columns cover the horizontal extent of the pattern including the markers.
    c.  Extract this 5xN rectangular region.
4.  Collect all extracted regions.
5.  Sort the extracted regions based on their corresponding `min_marker_row` in descending order (highest row index first).
6.  Concatenate the sorted regions horizontally from left to right. The result is the output grid.