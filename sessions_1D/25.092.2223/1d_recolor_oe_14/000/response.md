## Perception

The input and output are 1-dimensional sequences of pixels.
The input contains only white (0) and maroon (9) pixels.
The output contains white (0), blue (1), and azure (8) pixels.
White pixels in the input remain white in the output.
Maroon pixels in the input change color in the output.
The transformation appears to operate on contiguous sequences (runs) of maroon pixels.
The color a run of maroon pixels transforms into depends on the length of that run.
Observing the examples:
- Runs of length 2 (even) become blue (1).
- Runs of length 3 (odd) become azure (8).
- Runs of length 4 (even) become blue (1).
- Runs of length 5 (odd) become azure (8).
- Runs of length 6 (even) become blue (1).
The rule seems to be: change runs of maroon pixels with even length to blue, and runs of maroon pixels with odd length to azure.

## Facts


```yaml
elements:
  - type: sequence
    description: 1-dimensional array of pixels.
  - type: pixel
    properties:
      - color: integer value from 0-9

objects:
  - type: run
    description: A contiguous subsequence of pixels of the same color.
    properties:
      - color: The color of the pixels in the run.
      - length: The number of pixels in the run.

transformations:
  - type: color_change
    input_objects:
      - type: run
        properties:
          - color: 9 (maroon)
    output_objects:
      - type: run
        properties:
          - color: depends on input run length
          - length: same as input run length
    condition: The color of the output run depends on the parity of the length of the input run.
      - if length is even: output color is 1 (blue)
      - if length is odd: output color is 8 (azure)
  - type: color_preservation
    input_objects:
      - type: run
        properties:
          - color: 0 (white)
    output_objects:
      - type: run
        properties:
          - color: 0 (white)
          - length: same as input run length
    condition: Runs of white pixels remain unchanged.

relationships:
  - type: sequence_mapping
    description: Each pixel in the input sequence maps to a corresponding pixel in the output sequence.
  - type: run_mapping
    description: Each contiguous run of pixels in the input maps to a contiguous run of pixels of the same length in the output. The color mapping depends on the input run's color and length.
```


## Natural Language Program

1.  Initialize an empty output sequence with the same length as the input sequence.
2.  Iterate through the input sequence, identifying contiguous runs of pixels with the same color.
3.  For each identified run:
    a.  Get the starting index, ending index, color, and length of the run.
    b.  If the color of the run is white (0), fill the corresponding positions (from start index to end index) in the output sequence with white (0).
    c.  If the color of the run is maroon (9):
        i.  Check the length of the run.
        ii. If the length is even, fill the corresponding positions in the output sequence with blue (1).
        iii. If the length is odd, fill the corresponding positions in the output sequence with azure (8).
4.  Return the completed output sequence.