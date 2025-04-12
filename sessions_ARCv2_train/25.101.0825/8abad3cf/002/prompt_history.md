
## train_1

**input:**
```
4 4 4 4 4 7 7
4 7 7 7 4 7 5
4 7 1 7 4 7 5
4 7 7 7 4 7 7
4 4 4 4 4 7 5
7 7 7 7 7 7 5
5 5 5 5 5 7 7
```


**output:**
```
7 7 7 7 7 7 4 4 4 4
7 7 5 5 5 7 4 4 4 4
7 7 5 5 5 7 4 4 4 4
1 7 5 5 5 7 4 4 4 4
```


## train_2

**input:**
```
9 9 9 9
7 7 9 7
9 9 9 9
7 7 7 7
7 6 7 6
7 6 7 6
7 7 7 7
```


**output:**
```
7 7 7 9 9 9
6 6 7 9 9 9
6 6 7 9 9 9
```

**Perception of Elements:**

The task involves transforming an input grid of colored pixels into a smaller or differently shaped output grid. The transformation seems to rearrange pixels based on their color, count, and potentially their original spatial properties, creating rectangular blocks in the output.

1.  **Color Analysis:** The input grid contains multiple colors. The frequency (count) of each color appears important.
2.  **Dominant Color:** In both examples, one color is significantly more frequent than others (Orange). This color acts as a background or filler in the output.
3.  **Special Colors:**
    *   Some colors appear only once (Blue in train_1). This 'pixel color' seems to have a special role.
    *   Other non-dominant colors ('block colors') have counts greater than 1.
4.  **Output Structure:** The output consists of solid rectangular blocks, potentially with a single pixel placed, arranged horizontally, and separated by columns filled with the dominant color.
5.  **Block Dimensions:** The dimensions of the output blocks seem related to the input counts of the corresponding colors. Specifically, the width of a block for a color `C` with `N` pixels appears to be `floor(sqrt(N))`. The height of all blocks is uniform and depends on the number of non-dominant colors.
6.  **Arrangement Logic:** The horizontal arrangement (order) of the blocks and the pixel color seems to depend on the color indices and whether a single pixel color exists in the input. Gaps filled with the dominant color are inserted between these elements.

**YAML Facts:**


```yaml
task_description: Rearrange pixels from the input grid into a new grid composed of solid rectangular blocks representing non-dominant colors, potentially including a single pixel element, arranged horizontally with gaps filled by the dominant color.

definitions:
  - &dominant_color The color with the highest pixel count in the input grid.
  - &pixel_color The color with a pixel count of exactly 1 in the input grid (if present).
  - &block_colors All colors in the input grid that are neither the dominant color nor the pixel color.
  - &output_height Calculated as the number of block colors + (1 if pixel_color exists else 0) + 1.
  - &block_width For a block color C with N pixels, its width W is floor(sqrt(N)).
  - &output_elements The pixel_color (if present) and the block_colors.

transformation_steps:
  - Identify unique colors and counts in the input grid.
  - Determine the dominant_color, pixel_color (if any), and block_colors.
  - Calculate the output_height H.
  - For each block_color, calculate its block_width W_i. Blocks are H x W_i.
  - Determine the horizontal placement order of output_elements:
    - If pixel_color exists: Sort block_colors by color index descending. Order = [pixel_color] + [sorted block_colors].
    - If no pixel_color: Sort block_colors by color index ascending. Order = [sorted block_colors].
  - Calculate the total output width W_total: Sum of widths (1 for pixel_color, W_i for block_colors) + (number of elements - 1) gaps.
  - Create an output grid of size H x W_total, filled with dominant_color.
  - Place the output_elements in the determined order, column by column:
    - Place pixel_color at (H-1, current_col). Advance current_col by 1.
    - Place block_color C_i (H x W_i) starting at (0, current_col). Advance current_col by W_i.
    - Between elements, leave a 1-column gap (already filled with dominant_color). Advance current_col by 1 after placing an element if it's not the last one.

example_1_specifics:
  dominant_color: 7 (Orange)
  pixel_color: 1 (Blue)
  block_colors: [4 (Yellow), 5 (Gray)]
  output_height: count(Yellow, Gray) + count(Blue) + 1 = 2 + 1 + 1 = 4
  block_widths: Yellow (W=4), Gray (W=3)
  order: [Blue, Gray, Yellow] (Blocks sorted desc: Gray, Yellow)
  output_width: W_Blue(1) + W_Gray(3) + W_Yellow(4) + 2 gaps = 1 + 3 + 4 + 2 = 10
  layout: Blue(pixel at 3,0) | Gap | Gray(4x3) | Gap | Yellow(4x4)

example_2_specifics:
  dominant_color: 7 (Orange)
  pixel_color: None
  block_colors: [6 (Magenta), 9 (Maroon)]
  output_height: count(Magenta, Maroon) + count(None) + 1 = 2 + 0 + 1 = 3
  block_widths: Magenta (W=2), Maroon (W=3)
  order: [Magenta, Maroon] (Blocks sorted asc: Magenta, Maroon)
  output_width: W_Magenta(2) + W_Maroon(3) + 1 gap = 2 + 3 + 1 = 6
  layout: Magenta(3x2) | Gap | Maroon(3x3)
```


**Natural Language Program:**

1.  Analyze the input grid to find all unique colors present and count the occurrences (pixels) of each color.
2.  Identify three types of colors:
    a.  The 'dominant color': the color that appears most frequently.
    b.  The 'pixel color': any color that appears exactly once (there will be at most one such color).
    c.  The 'block colors': all other colors (not dominant, count > 1).
3.  Calculate the height `H` for the output grid: `H` is the count of block colors, plus 1 if a pixel color exists, plus 1 more.
4.  For each block color, calculate its corresponding width `W` by taking the integer part of the square root of its pixel count in the input. These colors will form solid rectangular blocks of size `H x W` in the output.
5.  Determine the horizontal arrangement order of the pixel color (if present) and the block colors:
    a.  If a pixel color exists, sort the block colors by their color index number in *descending* order. The final arrangement order is: the pixel color first, followed by the sorted block colors.
    b.  If no pixel color exists, sort the block colors by their color index number in *ascending* order. This is the final arrangement order.
6.  Calculate the total width `W_total` for the output grid. This is the sum of the widths `W` for all block colors, plus 1 (for the pixel color's column if it exists), plus 1 for each gap needed between adjacent elements in the arrangement (i.e., number of elements minus 1).
7.  Create a new grid of size `H x W_total`, initially filled entirely with the dominant color.
8.  Place the elements (pixel color and block color rectangles) into the output grid according to the determined arrangement order, from left to right:
    a.  If the element is the pixel color, place its color at row `H-1` in the current column. Advance the current column position by 1.
    b.  If the element is a block color, fill the rectangle of size `H x W` starting at row 0 in the current column with its color. Advance the current column position by `W`.
    c.  After placing an element (unless it's the very last one), skip the next column (leave it filled with the dominant color) to create a gap. Advance the current column position by 1.
9.  The resulting grid is the final output.
```python
import math
import numpy as np
from collections import Counter

"""
Transforms an input grid based on color frequencies.

1. Counts the occurrences of each color in the input grid.
2. Identifies the 'dominant_color' (most frequent), 'pixel_color' (count=1, if any), 
   and 'block_colors' (all others with count > 1).
3. Calculates the output grid height 'H' based on the number of block colors and 
   the presence of a pixel color (H = num_block_colors + (1 if pixel_color else 0) + 1).
4. Calculates the width 'W' for each block_color by taking the floor of the square 
   root of its count.
5. Determines the horizontal arrangement order of elements (pixel_color and block_colors):
   - If pixel_color exists: Sort block_colors descending by color index. Order = [pixel_color] + sorted_blocks.
   - If no pixel_color: Sort block_colors ascending by color index. Order = sorted_blocks.
6. Calculates the total output width 'W_total' by summing the widths of blocks (1 for pixel_color), 
   plus 1 column for each gap between elements.
7. Creates the output grid of size H x W_total, filled with the dominant_color.
8. Places the elements (pixel or blocks) into the output grid according to the determined order, 
   leaving 1-column gaps filled with the dominant_color between them. The pixel_color, if present, 
   is placed in the bottom row (H-1) of its column. Blocks fill their H x W area.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the described rules.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Analyze Colors & Counts
    unique_colors, counts = np.unique(input_array, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    if not color_counts:
        return [] # Handle empty input

    # Handle single color input - return empty or based on specific rule if needed
    if len(color_counts) == 1:
         # Assuming simple pass-through or empty for single color based on task ambiguity
         # For this specific task, a single color seems unlikely given examples.
         # Let's assume it should return an empty grid or handle as dominant only.
         # Based on the logic, if there's only one color, it's dominant, no blocks, no pixel.
         # Output height would be 1, width 0. Resulting in an empty list of lists.
         return [[]]


    # 2. Identify Color Types
    dominant_color = max(color_counts, key=color_counts.get)
    
    pixel_color = None
    pixel_color_candidates = [color for color, count in color_counts.items() if count == 1]
    if pixel_color_candidates:
        # Assuming only one possible pixel color based on description
        pixel_color = pixel_color_candidates[0] 
        
    block_colors = {}
    for color, count in color_counts.items():
        if color != dominant_color and color != pixel_color and count > 1:
             block_colors[color] = count

    # 3. Calculate Output Height
    output_height = len(block_colors) + (1 if pixel_color is not None else 0) + 1

    # 4. Calculate Block Widths
    block_widths = {color: math.floor(math.sqrt(count)) for color, count in block_colors.items()}

    # 5. Determine Arrangement Order
    ordered_elements = []
    if pixel_color is not None:
        # Sort block colors descending by color index
        sorted_block_colors = sorted(block_colors.keys(), reverse=True)
        ordered_elements = [pixel_color] + sorted_block_colors
    else:
        # Sort block colors ascending by color index
        sorted_block_colors = sorted(block_colors.keys())
        ordered_elements = sorted_block_colors

    # 6. Calculate Output Width
    output_width = 0
    num_elements = len(ordered_elements)
    if num_elements > 0:
        for i, element_color in enumerate(ordered_elements):
            if element_color == pixel_color:
                output_width += 1 # Width of pixel color element is 1
            else: # It's a block color
                output_width += block_widths[element_color]
            
            if i < num_elements - 1: # Add gap width if not the last element
                output_width += 1

    # Handle case with no elements to place (only dominant color)
    if output_width == 0:
         # If only dominant color existed, H=1, W=0 -> [[]]
         # If dominant + pixel, H=2, W=1 -> Pixel placed? Let's assume min W=1 if H>0
         # If dominant + blocks, H=num_blocks+1, W=sum(W_blocks)+gaps
         # If dominant + pixel + blocks, H=num_blocks+1+1, W=1+sum(W_blocks)+gaps
         if output_height > 0:
             # This case implies only dominant color was present or dominant + pixel/blocks with sqrt(count) < 1
             # Returning an empty grid seems consistent with width 0.
              return [[]] # Or potentially a 1x1 grid of dominant color? The logic leads to 0 width.
         else: # Should not happen if input is not empty
             return []


    # 7. Create Output Grid
    output_grid = np.full((output_height, output_width), dominant_color, dtype=int)

    # 8. Place Elements
    current_col = 0
    for i, element_color in enumerate(ordered_elements):
        if element_color == pixel_color:
            # Place pixel color at the bottom row of the current column
            if output_height > 0: # Ensure height is valid
                 output_grid[output_height - 1, current_col] = pixel_color
            width = 1
        else: # It's a block color
            width = block_widths[element_color]
            # Place the block
            if output_height > 0 and width > 0: # Ensure dimensions are valid
                output_grid[0:output_height, current_col:current_col + width] = element_color
        
        # Advance column position by the width of the placed element
        current_col += width
        
        # Add gap if not the last element
        if i < num_elements - 1:
            current_col += 1 # Skip one column for the gap (already filled with dominant)

    # 9. Return Output
    return output_grid.tolist()
```
