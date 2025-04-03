**Perception**

The task operates on single-row grids (1xN). The input grid contains background pixels (white, 0) and colored objects. These objects appear either as single pixels of a specific color or as horizontal blocks of three identical colored pixels. The transformation rule modifies only the single-pixel objects. Existing 3-pixel blocks remain unchanged. Each single colored pixel in the input is expanded into a 3-pixel block of the same color in the output. This expansion effectively replaces the single pixel and the two pixels immediately to its right (which are background pixels in the examples) with the triplet of the single pixel's color. The relative order of objects and background segments is preserved, though the lengths change due to expansion.

**Facts**


```yaml
Grid:
  dimensionality: 1D (represented as 1xN 2D grid)
  background_color: 0 (white)

Objects:
  - type: Pixel Block
    properties:
      color: non-zero integer (1-9)
      size: 
        - 1 pixel (single pixel object)
        - 3 pixels (3-pixel block object)
      shape: horizontal line segment
      position: index within the row

Transformation:
  action: Conditional Expansion
  target: Single Pixel Objects (size=1, color != 0)
  condition: The object must be a single pixel (i.e., not immediately followed by two pixels of the same color).
  effect:
    - Replace the single pixel and the two subsequent pixels with a 3-pixel block of the original single pixel's color.
  unchanged:
    - Background pixels (0), unless overwritten by expansion.
    - 3-pixel block objects.

Relationships:
  - Spatial: Objects are positioned horizontally, separated by background pixels.
  - Transformation Dependency: The transformation applied depends on the size (1 or 3) of the non-background object encountered. Expansion occurs rightward.
```


**Natural Language Program**

1.  Initialize an empty list to store the output row.
2.  Initialize an index `i` to 0, pointing to the current position in the input row.
3.  While `i` is less than the width of the input row:
    a.  Get the color `C` of the pixel at `input[i]`.
    b.  If `C` is the background color (0):
        i.  Append `0` to the output list.
        ii. Increment `i` by 1.
    c.  If `C` is a non-background color:
        i.  Check if the pixels at `input[i+1]` and `input[i+2]` (within bounds) are also equal to `C`.
        ii. If yes (it's a 3-pixel block): Append `C`, `C`, `C` to the output list. Increment `i` by 3.
        iii.If no (it's treated as a single pixel to be expanded): Append `C`, `C`, `C` to the output list. Increment `i` by 1.
4.  Construct the final output grid using the generated output list (maintaining the 1xN shape).