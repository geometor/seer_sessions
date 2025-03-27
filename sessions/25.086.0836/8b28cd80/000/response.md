Okay, let's analyze the provided task examples.

**Perception**

1.  **Input Grid:** The input is always a 3x3 grid.
2.  **Output Grid:** The output is always a 9x9 grid.
3.  **Color Usage:** Each input grid contains exactly one non-white pixel (colors observed: gray-5, azure-8, orange-7, green-3, yellow-4). The remaining pixels are white (0). The corresponding output grid uses only white (0) and the specific non-white color from the input grid.
4.  **Pattern Correlation:** The 9x9 output grid appears to be a fixed pattern determined solely by the *position* of the single non-white pixel within the 3x3 input grid.
5.  **Color Application:** The *color* of the non-white pixel in the input determines the color used for the non-white parts of the output pattern. White pixels in the input do not seem to directly influence the output pattern, other than signifying which pixel *is* the determining one.
6.  **Positional Mapping:** It seems there's a distinct 9x9 pattern associated with each of the 9 possible locations within the 3x3 input grid. The training examples show the patterns for 5 specific input locations: (1, 0), (1, 2), (0, 2), (0, 1), and (1, 1).

**Facts**

```
yaml
task_type: pattern_generation_by_position
input_grid:
  size: 3x3
  content:
    - type: background
      color: 0 (white)
    - type: signal_pixel
      count: 1
      color: non-zero (C)
      position: (r, c) # varies per example
output_grid:
  size: 9x9
  content:
    - type: pattern_pixels
      color: C # same as signal_pixel color
    - type: background_pixels
      color: 0 (white)
transformation:
  rule: select_and_color_pattern
  steps:
    - Identify the position (r, c) and color (C) of the single non-zero pixel in the input grid.
    - Select a predefined 9x9 binary pattern (0s and 1s) based uniquely on the input position (r, c).
    - Generate the output grid by replacing 1s in the selected pattern with color C and 0s with color 0 (white).
relationships:
  - The position (r, c) of the input signal_pixel determines *which* 9x9 pattern template is used.
  - The color (C) of the input signal_pixel determines the foreground *color* of the output pattern.
constants:
  - A set of 9 predefined 9x9 binary patterns, indexed by the possible input positions (0,0) through (2,2). # 5 patterns are explicitly defined by the examples
