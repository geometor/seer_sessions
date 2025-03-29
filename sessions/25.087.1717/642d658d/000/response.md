*   **Perception**: The input is a grid containing various colors, primarily a background color (red in example 1, azure in 2, gray in 3) and white (0). Scattered within the grid are specific 3-pixel patterns. These patterns consist of a central yellow pixel (4) flanked horizontally or vertically by two identical pixels of another color (C). The task is to identify these `C-4-C` (horizontal) or `C / 4 / C` (vertical) patterns, count the frequency of each color `C` involved, and determine the output color based on these frequencies. The output is not a grid but a single number representing a color.

*   **Facts**:
    
```yaml
    task_type: frequency_analysis
    input_features:
      - grid: 2D array of integers (colors)
      - patterns:
          - type: horizontal
            structure: [C, 4, C] # C is a color, 4 is yellow
            description: Three horizontally adjacent pixels where the outer two are the same color C and the middle is yellow.
          - type: vertical
            structure: # C is a color, 4 is yellow
             - [C]
             - [4]
             - [C]
            description: Three vertically adjacent pixels where the top and bottom are the same color C and the middle is yellow.
          - constraint: Color C cannot be yellow (4) or white (0).
    transformation:
      - action: identify_patterns
        description: Scan the input grid to find all instances of the described horizontal and vertical patterns.
      - action: count_frequencies
        input: identified patterns
        output: frequency map (Color C -> count)
        description: Count how many times each color C appears as the flanking color in the identified patterns.
      - action: find_most_frequent
        input: frequency map
        output: set of most frequent colors
        description: Determine the maximum frequency count among all colors C. Identify all colors C that have this maximum frequency.
      - action: select_output_color
        input: set of most frequent colors
        output: final color value
        description: From the set of most frequent colors, select the one with the smallest numerical value.
    output_feature:
      - value: integer representing the selected color.
    examples:
      - train_1:
          patterns: 3-4-3 (x2), 6-4-6 (x1), 8-4-8 (x1), 7-4-7 (x1)
          frequencies: {3: 2, 6: 1, 8: 1, 7: 1}
          max_freq: 2
          candidates: {3}
          output: 3
      - train_2:
          patterns: 3-4-3 (x2), 2-4-2 (x2)
          frequencies: {3: 2, 2: 2}
          max_freq: 2
          candidates: {2, 3}
          output: 2 # min(2, 3)
      - train_3:
          patterns: 3-4-3 (x1), 8-4-8 (x2)
          frequencies: {3: 1, 8: 2}
          max_freq: 2
          candidates: {8}
          output: 8
    ```


*   **Natural Language Program**:
    1.  Initialize a counter (dictionary or map) to store the frequency of colors found in specific patterns.
    2.  Iterate through each pixel `(r, c)` of the input grid.
    3.  At each pixel `(r, c)` containing yellow (4):
        a.  Check for a horizontal pattern: If the pixel to the left `(r, c-1)` and the pixel to the right `(r, c+1)` exist and have the same color `C`, and `C` is not yellow (4) or white (0), increment the count for color `C` in the frequency counter.
        b.  Check for a vertical pattern: If the pixel above `(r-1, c)` and the pixel below `(r+1, c)` exist and have the same color `C`, and `C` is not yellow (4) or white (0), increment the count for color `C` in the frequency counter.
    4.  After scanning the entire grid, examine the frequency counter.
    5.  If the counter is empty (no patterns found), handle this case (though not present in examples, perhaps output 0 or handle as an error). Assuming patterns are always found based on examples.
    6.  Find the maximum frequency count among all colors in the counter.
    7.  Identify all colors that have this maximum frequency.
    8.  Select the color from this group that has the minimum numerical value.
    9.  The final output is this selected color's numerical value.