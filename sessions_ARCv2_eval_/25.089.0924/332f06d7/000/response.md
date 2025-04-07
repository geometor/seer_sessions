Okay, let's analyze the task examples.

**Perception of the Elements:**

1.  **Colors:** The primary colors involved in the transformation are Red (2), White (0), and Blue (1). Green (3) acts as a background or neutral color, remaining unchanged in all examples.
2.  **Objects:** The transformation seems to focus on contiguous blocks (objects) of Red, White, and Blue pixels. These objects vary in size (1x1, 2x2, 3x3) across examples.
3.  **Transformation Type:** The core operation is a pixel-wise color change applied to Red, White, and/or Blue pixels. The specific changes depend on a condition related to the input grid's composition.
4.  **Conditional Logic:** There appear to be two distinct transformation rules. The rule applied depends on the number of distinct objects of each color (Red, White, Blue) present in the input.
    *   In examples 2 and 3, there is exactly one distinct object of Red, one of White, and one of Blue. In these cases, White pixels become Blue, and Blue pixels become White, while Red pixels remain unchanged.
    *   In examples 1 and 4, the condition of having exactly one object of each color (Red, White, Blue) is *not* met (specifically, there isn't one distinct Blue object separate from other blue structures). In these cases, Red pixels become White, White pixels become Blue, and Blue pixels remain unchanged.

**YAML Fact Documentation:**


```yaml
Task: Conditional Color Transformation

Input_Features:
  - Grid: 2D array of pixels (0-9).
  - Colors:
      - Active: Red (2), White (0), Blue (1)
      - Background: Green (3) (and potentially others, though only Green appears here)
  - Objects: Contiguous blocks of a single active color (Red, White, or Blue).
  - Object_Counts: The number of distinct, isolated objects found for each active color.

Output_Features:
  - Grid: Transformed 2D array of pixels.

Transformation:
  - Type: Pixel-wise color substitution based on a global condition.
  - Condition: Check if the number of distinct Red objects = 1 AND the number of distinct White objects = 1 AND the number of distinct Blue objects = 1.
  - Rules:
      - If Condition is True:
          - Red (2) -> Red (2)
          - White (0) -> Blue (1)
          - Blue (1) -> White (0)
          - Other_Colors -> Other_Colors (e.g., Green (3) -> Green (3))
      - If Condition is False:
          - Red (2) -> White (0)
          - White (0) -> Blue (1)
          - Blue (1) -> Blue (1)
          - Other_Colors -> Other_Colors (e.g., Green (3) -> Green (3))
  - Scope: Applies to all pixels in the grid.
```


**Natural Language Program:**

1.  Analyze the input grid to identify all distinct, contiguous objects composed solely of Red (2), White (0), or Blue (1) pixels. Consider Green (3) pixels as background or separators.
2.  Count the number of these distinct objects for each color: `num_red_objects`, `num_white_objects`, `num_blue_objects`.
3.  Evaluate the condition: `is_condition_met = (num_red_objects == 1) AND (num_white_objects == 1) AND (num_blue_objects == 1)`.
4.  Create a new output grid, initially identical to the input grid.
5.  Iterate through each pixel `(row, col)` of the input grid:
    a.  Get the `input_color` at `(row, col)`.
    b.  If `is_condition_met` is True:
        i.  If `input_color` is White (0), set the output grid pixel at `(row, col)` to Blue (1).
        ii. If `input_color` is Blue (1), set the output grid pixel at `(row, col)` to White (0).
        iii. If `input_color` is Red (2) or any other color, keep the color unchanged in the output grid.
    c.  If `is_condition_met` is False:
        i.  If `input_color` is Red (2), set the output grid pixel at `(row, col)` to White (0).
        ii. If `input_color` is White (0), set the output grid pixel at `(row, col)` to Blue (1).
        iii. If `input_color` is Blue (1) or any other color, keep the color unchanged in the output grid.
6.  Return the completed output grid.