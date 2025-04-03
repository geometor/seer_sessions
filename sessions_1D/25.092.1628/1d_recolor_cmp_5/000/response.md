**Perception:**

The input is a one-dimensional sequence of pixels, primarily composed of white (0) and green (3). The output maintains the same length and structure but introduces red (2) pixels. The transformation rule appears to depend on the length of contiguous runs of green pixels. Specifically, horizontal runs of exactly five green pixels in the input are replaced by runs of five red pixels in the output. Runs of green pixels with lengths other than five, as well as all white pixels, remain unchanged in the output.

**Facts:**


```yaml
task_type: color_transformation
input_dimensionality: 1D
output_dimensionality: 1D
colors_present:
  input: [white, green]
  output: [white, green, red]
objects:
  - type: contiguous_run
    color: green
    properties:
      - length
actions:
  - type: conditional_color_change
    condition:
      object_type: contiguous_run
      color: green
      property: length
      value: 5
    target_color: red
unchanged_elements:
  - type: pixel
    color: white
  - type: contiguous_run
    color: green
    condition_not_met: length is not 5
```


**Natural Language Program:**

1.  Iterate through the input sequence to identify contiguous horizontal runs of green (3) pixels.
2.  For each identified run of green pixels, determine its length.
3.  If the length of the green run is exactly 5, change the color of all pixels within that run to red (2) in the output sequence.
4.  If the length of the green run is not 5, keep the color of all pixels within that run as green (3) in the output sequence.
5.  All white (0) pixels in the input sequence remain white (0) in the output sequence.
6.  Construct the final output sequence based on these rules.