Okay, let's analyze the provided ARC task examples.

## Perception

1.  **Grid Structure:** The input and output grids are consistently 30 rows by 24 columns.
2.  **Horizontal Bands:** The grids appear segmented into distinct horizontal bands. These bands are often characterized by a dominant background color and sometimes a frame or border of a different color around the inner area.
3.  **Source Band:** The topmost band containing patterns or shapes (i.e., colors different from its own background) seems to act as a "source" of information or patterns. In the output, this source band is typically cleared or reset to its background color.
4.  **Target Bands:** Bands located below the source band, particularly those with distinct frames, act as "target" areas. The transformation involves drawing shapes into these target bands.
5.  **Frames:** Target bands often have a frame (1-pixel border) of one color and a background (inner area) of another color. These frame and background colors are crucial for the transformation.
6.  **Objects/Patterns:** The source band contains various shapes or objects composed of contiguous pixels of the same color. Some objects might enclose other objects or pixels of different colors.
7.  **Transformation Logic:** The core logic seems to involve selecting specific shapes or pixels from the source band based on their color and transferring their *shape* or *location* into a corresponding target band. The color used for drawing in the target band is determined by the target band's *frame* color. The selection criteria appear to link the *color* of the source object/pixels to the *background color* of the target band.
8.  **Object Selection Refinements:**
    *   When multiple objects in the source band share the same color, and that color matches a target band's background, a selection rule (e.g., choosing the largest object) seems to apply (observed in train_2).
    *   Objects fully enclosed within another object in the source band seem to be ignored when selecting the primary object shape (observed in train_1).
    *   There appears to be a special case for yellow (color 4): when a target band's background is yellow, *all* yellow pixels from the source band (regardless of the object they formed) are copied, using the target's frame color (observed in train_2).

## Facts (YAML)


```yaml
task_context:
  grid_size: [30, 24] # rows, columns
  bands:
    type: horizontal
    source:
      location: top-most band containing multiple colors
      role: provides patterns/objects
      output_action: clear to source background color
    target:
      location: below source band
      structure: typically framed (border color different from background color)
      role: receives patterns from source
      properties:
        - background_color
        - frame_color
    separators: may exist as rows of uniform color between bands

objects:
  definition: contiguous block of same-colored pixels (non-background) in the source band
  properties:
    - color
    - shape (set of coordinates)
    - size (pixel count)
  relationships:
    - containment: one object can be fully enclosed within another
  filtering: enclosed objects are ignored for primary shape transfer

transformation:
  type: pattern transfer from source to target bands
  rules:
    - rule_1: # Standard Rule
        condition: target_band.background_color is NOT yellow (4)
        selection:
          - find source objects where object.color == target_band.background_color
          - filter_out_enclosed_source_objects: true
          - disambiguation (if multiple match): select the largest object by pixel count
        action:
          - if an object is selected:
              for each pixel_coord in selected_object.shape:
                output_grid[pixel_coord] = target_band.frame_color
    - rule_2: # Special Yellow Rule
        condition: target_band.background_color IS yellow (4)
        selection:
          - find all pixel_coords in source band where input_grid[pixel_coord] == yellow (4)
        action:
          - for each selected pixel_coord:
              output_grid[pixel_coord] = target_band.frame_color

output_generation:
  - start with a copy of the input grid
  - identify source and target bands, storing background and frame colors
  - identify primary source objects (non-enclosed, non-background)
  - clear the source band area in the output grid (fill with source background color)
  - for each target band:
      apply rule_1 or rule_2 based on target_band.background_color
```


## Natural Language Program

1.  **Initialize:** Create the output grid as a copy of the input grid.
2.  **Identify Bands:**
    *   Scan the grid from top to bottom to identify horizontal bands. A band boundary occurs where row composition changes significantly (e.g., uniform color row, change in framing).
    *   Designate the first band containing multiple colors as the "source band". Record its background color (`source_bg`).
    *   Identify subsequent bands that have a distinct frame color and background color as "target bands". For each target band, record its background color (`target_bg`) and frame color (`target_frame`). Store the row range for the source and each target band.
3.  **Analyze Source Band:**
    *   Within the row range of the source band, identify all contiguous objects formed by pixels that are not `source_bg`.
    *   Filter out any object that is completely enclosed within another identified object. Let the remaining objects be the "primary source objects". Record their color, shape (coordinates), and size (pixel count).
4.  **Clear Source in Output:** For all pixels `(r, c)` within the source band's row range in the output grid, set their color to `source_bg`.
5.  **Process Target Bands:** Iterate through each identified target band:
    *   **Check for Yellow Background:** If the current `target_bg` is yellow (4):
        *   Find all pixel coordinates `(r, c)` within the source band's row range where the *input* grid color is yellow (4).
        *   For each such coordinate `(r, c)`, set the color of the pixel at `(r, c)` in the *output* grid to the current `target_frame` color.
    *   **Standard Processing:** If the current `target_bg` is *not* yellow (4):
        *   Find all "primary source objects" whose color matches the current `target_bg`.
        *   If one or more matching objects are found:
            *   If exactly one object matches, select it.
            *   If multiple objects match, select the one with the largest size (pixel count).
            *   If an object is selected, for every coordinate `(r, c)` defining the shape of the selected object, set the color of the pixel at `(r, c)` in the *output* grid to the current `target_frame` color.
6.  **Finalize:** The modified output grid is the result.