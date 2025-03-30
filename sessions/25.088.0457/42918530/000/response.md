Okay, let's analyze the task based on the provided examples.

**Perception**

1.  **Grid Structure:** The input and output grids are relatively large and structured. They contain multiple distinct shapes separated by white (0) background pixels.
2.  **Object Identification:** The primary objects appear to be 5x5 squares. Each square has a solid border of a specific color (not white) and an inner 3x3 area.
3.  **Object Properties:**
    *   Each 5x5 square is defined by its border color.
    *   The inner 3x3 area can either be entirely white (0) or contain a pattern made of the same color as the border.
4.  **Relationships:** Multiple squares can share the same border color. Their positions relative to each other vary across examples.
5.  **Transformation:** The core transformation seems to involve modifying the inner 3x3 area of *some* of the 5x5 squares. Specifically, squares with an all-white inner area appear to adopt the inner pattern from another square of the *same* border color, provided such a patterned square exists.
6.  **Consistency:** The outer 5x5 border of each square remains unchanged between input and output. Squares that already have an inner pattern also seem to remain unchanged. The white background separating the squares is also unchanged.

**Facts**


```yaml
elements:
  - type: grid
    description: A 2D array of pixels with values 0-9 representing colors. Contains background and distinct objects.
  - type: background
    color: white (0)
    description: Separates the main objects. Remains unchanged.
  - type: object
    shape: square
    size: 5x5
    components:
      - type: border
        thickness: 1 pixel
        color: non-white (1-9)
        description: Forms the outer frame of the 5x5 square.
      - type: inner_area
        shape: square
        size: 3x3
        location: center of the 5x5 square
        content:
          - type: pattern
            description: Can be either all white (0) pixels or contain a mix of white (0) and the border color pixels.
properties:
  - property: color_grouping
    description: Squares can be grouped based on their shared border color.
  - property: pattern_state
    description: The inner_area can be in one of two states - 'empty' (all white) or 'patterned' (contains non-white pixels).
actions:
  - action: identify_squares
    description: Locate all 5x5 squares based on their non-white borders.
  - action: group_by_color
    description: Group the identified squares by their border color.
  - action: find_source_pattern
    description: Within each color group, identify if there exists at least one square with a 'patterned' inner_area. If yes, designate its inner 3x3 pattern as the 'source pattern' for that color. Assume only one unique source pattern exists per color across all examples shown (or the first one found is sufficient).
  - action: find_target_squares
    description: Within each color group, identify all squares with an 'empty' inner_area. These are the 'target squares'.
  - action: copy_pattern
    description: If a 'source pattern' and 'target squares' exist for a color group, copy the 'source pattern' into the inner_area of all 'target squares' in that group.
relationships:
  - relationship: pattern_propagation
    description: An existing inner pattern within a color group propagates to other squares of the same color that lack a pattern (have an 'empty' inner_area).
    condition: Must have at least one 'patterned' source and at least one 'empty' target square within the same color group.
```


**Natural Language Program**

1.  Scan the input grid to locate all distinct 5x5 squares. A 5x5 square is identified by a 1-pixel thick border of a single non-white color surrounding a 3x3 inner area. These squares are separated by white pixels.
2.  Create groups of squares based on their border color.
3.  For each color group:
    a.  Initialize a variable `source_pattern` to `None`.
    b.  Iterate through the squares in the group. If a square's inner 3x3 area contains any non-white pixels (i.e., it's 'patterned'), store its 3x3 inner pattern in `source_pattern` and stop searching within this group (assuming only one source pattern matters per color or the first one found is the canonical one).
    c.  If a `source_pattern` was found for this color group:
        i.  Iterate through the squares in the group again.
        ii. If a square's inner 3x3 area is entirely composed of white pixels (i.e., it's 'empty'), replace its inner 3x3 area with the stored `source_pattern`.
4.  Ensure all squares that were originally 'patterned' or belonged to a color group with no 'source_pattern' remain unchanged.
5.  Output the modified grid.