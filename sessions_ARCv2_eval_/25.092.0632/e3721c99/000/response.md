Okay, let's analyze the provided examples.

**Perception of Task Elements:**

1.  **Grid Structure:** Both input and output are 30x30 grids.
2.  **Key Area:** The top portion of the grid seems to act as a legend or key. It contains distinct, relatively small shapes made of colors like yellow (4), green (3), blue (1), and red (2), separated from the lower part by a solid horizontal line (blue=1).
3.  **Work Area:** The bottom portion of the grid, below the separator line, contains various shapes made of gray (5) pixels on a white (0) background.
4.  **Transformation:** The transformation primarily affects the gray shapes in the work area. These gray shapes are replaced by colored shapes in the output.
5.  **Color Replacement Logic:** The color used to replace a gray shape in the output corresponds to the color of a shape in the key area whose shape *exactly matches* the gray shape in the input.
6.  **Preservation:** The key area, the separator line, and the white background pixels in the work area remain unchanged in the output.

**YAML Fact Documentation:**


```yaml
task_context:
  grid_size: ثابت (30x30 in examples)
  background_color: white (0)
  separator:
    exists: True
    color: blue (1)
    type: horizontal_line
    location: separates grid into upper (key) and lower (work) areas
key_area:
  location: above separator line
  content: contains multiple distinct colored objects (key patterns) on background
  key_pattern_colors: [yellow (4), green (3), blue (1), red (2)] # colors vary per example
  purpose: provides shape-color mapping templates
work_area:
  location: below separator line
  input_content: contains target objects (gray=5) on background
  output_content: target objects are replaced by colors based on shape match with key patterns
target_objects:
  input_color: gray (5)
  location: work_area
  property: contiguous shape
action:
  type: shape-based_color_replacement
  input: gray objects in work_area
  output: colored objects in work_area
  rule: >
    Find each contiguous gray object in the work area.
    Compare its shape to the shapes of the key patterns in the key area.
    If a gray object's shape matches a key pattern's shape, replace the gray object's pixels with the color of the matching key pattern in the output grid.
  unaffected_elements:
    - key_area content
    - separator line
    - background pixels in work_area
```


**Natural Language Program:**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Identify the solid horizontal separator line (color blue=1).
3.  Define the "key area" as the region above the separator line and the "work area" as the region below it.
4.  Find all distinct, contiguous, non-background colored objects within the key area (excluding the separator line itself). For each such "key pattern", record its shape (relative pixel coordinates) and its color.
5.  Find all contiguous objects composed of gray pixels (color 5) located within the work area of the input grid.
6.  For each gray object found in the work area:
    a.  Determine its shape (relative pixel coordinates).
    b.  Compare this shape against the shapes of all key patterns recorded in step 4.
    c.  If the gray object's shape exactly matches the shape of one of the key patterns:
        i.  Retrieve the color associated with the matching key pattern.
        ii. For every pixel location occupied by the current gray object in the input grid, set the corresponding pixel location in the output grid to the retrieved key pattern color.
7.  Return the final output grid.