Okay, let's break down this task.

## Perception

1.  **Input Grid Structure:** Each input grid appears segmented into distinct regions. There's typically an upper area with a background color (blue, azure, or yellow in the examples) containing several smaller, distinct objects composed of one or more colors. Below this, there are horizontal bands, each characterized by a fill color bordered on the left/right by a different border color. Sometimes there are separator lines (like full rows of blue or azure) between these regions or bands.
2.  **Output Grid Structure:** The output grid retains the overall structure, particularly the horizontal bands and separator lines. However, the objects originally present in the upper area of the input grid are removed (replaced by the upper background color). Crucially, modifications occur *within* the fill areas of the horizontal bands.
3.  **Transformation:** The core transformation involves transferring information from the upper objects ("patterns") to the lower horizontal bands ("targets"). Specifically, the *shape* of each pattern object from the top section is "stamped" or "drawn" onto the fill area of a corresponding target band below. The color used for stamping is the *border* color of the target band.
4.  **Pattern-Target Matching:** There's a one-to-one correspondence between the pattern objects in the top section and the target bands in the bottom section. The matching rule seems to be based on color: a pattern object is matched to a target band if one of the colors *within* the pattern object matches the *fill* color of the target band. In cases where multiple patterns could match a band based on the same color (Example 2, where two patterns contain red, and one band has a red fill), the pattern with the *most pixels* of the matching color is assigned to that band.
5.  **Stamping Process:** Once a pattern shape is matched to a target band, the shape (defined by the non-background pixels within the pattern object's bounding box) is drawn onto the target band's fill area using the target band's border color. The original fill color pixels within the shape's area are overwritten.
6.  **Cleanup:** The original pattern objects in the upper area are erased from the output grid, replaced by the background color of that upper area.

## Facts


```yaml
InputGrid:
  Properties:
    - segmentation: Contains distinct upper and lower regions.
    - upper_region:
        - contains: pattern_objects
        - background_color: dominant color in the upper area (e.g., blue, azure, yellow)
    - lower_region:
        - contains: horizontal_bands
        - contains: separator_lines (optional, single color rows)
  Elements:
    - pattern_object:
        - description: Connected component of non-background pixels in the upper_region.
        - properties:
            - shape: Relative coordinates of its non-background pixels.
            - colors: Set of colors present within the object.
            - color_counts: Count of pixels for each color within the object.
            - location: Bounding box or coordinates in the upper_region.
    - horizontal_band:
        - description: Rectangular area in the lower_region.
        - properties:
            - fill_color: Color of the main central part of the band.
            - border_color: Color of the pixels typically flanking the fill area on the left/right.
            - fill_area: Coordinates corresponding to the fill_color pixels.
            - location: Row indices defining the band.
    - background_pixel: Pixel belonging to the dominant background color of the upper_region.

OutputGrid:
  Properties:
    - derivation: Derived from InputGrid by applying transformations.
    - structure: Retains separator_lines and band structure from InputGrid.
    - upper_region: Contains only the background_color from the input's upper_region.
    - lower_region: Horizontal bands are potentially modified.

Transformation:
  Actions:
    - identify_elements:
        - Find background_color of the upper_region.
        - Find all pattern_objects in the upper_region. Extract shape, colors, and color_counts for each.
        - Find all horizontal_bands in the lower_region. Extract fill_color, border_color, and fill_area for each.
    - match_patterns_to_bands:
        - Establish a one-to-one mapping between pattern_objects and horizontal_bands.
        - rule: For a band B with fill_color C_fill:
            - Find all available patterns P containing C_fill.
            - If one pattern P is found, match P to B.
            - If multiple patterns P1, P2... are found, match the pattern P_max (which has the highest count of C_fill pixels) to B.
        - dependencies: Matches might need to be resolved iteratively if choices depend on prior matches.
    - stamp_shapes:
        - For each matched pair (pattern P, band B):
            - Get the shape S of pattern P.
            - Get the border_color C_border of band B.
            - Get the fill_area A of band B.
            - Modify the output grid: For each pixel location within shape S (relative to its origin), find the corresponding absolute coordinate within the fill_area A and set its color to C_border.
    - cleanup_upper_region:
        - Replace all pixels in the output grid corresponding to the original pattern_objects' locations with the upper_region's background_color.
```


## Natural Language Program

1.  **Initialization:** Create a copy of the input grid to serve as the initial output grid.
2.  **Identify Upper Background:** Determine the background color of the upper region of the input grid (e.g., the most frequent color in the top portion or the color at the corners).
3.  **Extract Patterns:** Locate all distinct connected objects in the upper region that are not the background color. For each object (pattern):
    *   Record its shape (the relative positions of all its constituent pixels).
    *   Record the set of colors it contains and the count of pixels for each color.
    *   Keep track of the original locations of these pattern objects.
4.  **Extract Bands:** Identify all horizontal bands in the lower region. For each band:
    *   Record its fill color.
    *   Record its border color (typically found in columns flanking the fill area within the band's rows).
    *   Record the coordinates defining its fill area.
5.  **Match Patterns and Bands:**
    *   Create lists of the extracted patterns and bands.
    *   Iteratively match patterns to bands:
        *   For each unmatched band `B` with fill color `C_fill`:
            *   Identify the set of unmatched patterns `P_candidates` where each pattern contains the color `C_fill`.
            *   If `P_candidates` is empty, continue to the next band.
            *   If `P_candidates` contains exactly one pattern `P`, match `P` to `B`. Mark both as matched.
            *   If `P_candidates` contains multiple patterns, find the pattern `P_best` within `P_candidates` that has the maximum count of pixels with the color `C_fill`. Match `P_best` to `B`. Mark both as matched.
    *   Repeat this process until all patterns and bands are matched.
6.  **Apply Stamping:**
    *   For each matched pair (Pattern `P`, Band `B`):
        *   Retrieve the shape `S` of pattern `P`.
        *   Retrieve the border color `C_border` of band `B`.
        *   Retrieve the fill area coordinates `A` of band `B`.
        *   For every pixel coordinate defined by shape `S` (relative to the pattern's origin), calculate its corresponding absolute coordinate within the band's fill area `A` in the output grid.
        *   Change the color of these pixels in the output grid to `C_border`.
7.  **Clean Up:** Go back to the original locations of the pattern objects identified in step 3. In the output grid, set all pixels at these locations to the upper background color identified in step 2.
8.  **Final Output:** The modified grid is the final output.