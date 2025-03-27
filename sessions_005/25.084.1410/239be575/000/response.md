**Perception:**

The task involves analyzing input grids containing white (0), red (2), and azure (8) pixels. The output is always a single value, either 0 or 8. The goal is to determine a rule based on the spatial relationship between the red and azure pixels that determines whether the output is 0 or 8.

Observing the examples, the red pixels consistently form 2x2 squares, while the azure pixels form objects of various shapes and sizes. The determining factor appears to be whether any part of a red object comes into contact (either side-by-side or diagonally) with any part of an azure object.

*   If any red pixel is adjacent (including diagonals) to any azure pixel, the output is 0.
*   If no red pixel is adjacent to any azure pixel, the output is 8.

**Facts:**


```yaml
task_type: classification
input_features:
  - color: white (0)
  - color: red (2)
  - color: azure (8)
output_features:
  - single_value: 0 (white) or 8 (azure)
objects:
  - type: red_pixels
    color: 2
    # note: in examples, often form 2x2 squares, but the rule seems pixel-based
  - type: azure_pixels
    color: 8
    # note: form contiguous blocks of various shapes
relationships:
  - type: adjacency
    between: red_pixels, azure_pixels
    definition: sharing a side or a corner (8 neighbors)
rule_logic:
  condition: Check if any red pixel (color 2) is adjacent (including diagonally) to any azure pixel (color 8).
  outcome_true: Output is 0.
  outcome_false: Output is 8.
```


**Natural Language Program:**

1.  Scan the input grid to locate all red pixels (value 2) and all azure pixels (value 8).
2.  For each red pixel found:
    *   Examine its 8 neighboring cells (horizontally, vertically, and diagonally adjacent).
    *   If any of these neighboring cells contains an azure pixel (value 8), then the condition is met. Stop checking and proceed to step 3.
3.  If the condition in step 2 was met (at least one red pixel is adjacent to an azure pixel), the output is 0.
4.  If the scan completes and no red pixel was found to be adjacent to an azure pixel, the output is 8.