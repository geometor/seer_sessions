## Perception

The input data consists of grids (matrices) containing numerical digits. Each grid primarily uses two digits: zero ('0') and a single non-zero digit ('2', '6', or '4' in the examples). The non-zero digit is consistent within each input grid. The zero digit appears to function as a background or separator.

The input grids exhibit a structure often involving alternating rows of all zeros and rows primarily composed of the non-zero digit. Crucially, some rows contain a mixture of zeros and the non-zero digit, specifically featuring a contiguous block of the non-zero digit bounded by zeros (e.g., `... 0 N N N 0 ...`).

The output is a smaller, solid rectangular grid composed entirely of the non-zero digit identified from the input. The dimensions of this output grid appear related to the length of the bounded block of non-zero digits found within the mixed rows of the input.

The transformation involves:
1.  Identifying the unique non-zero digit (`N`) in the input grid.
2.  Locating rows containing the pattern of a sequence of `N`s surrounded by `0`s.
3.  Measuring the length (`W`) of this sequence of `N`s.
4.  Determining the height (`H`) of the output grid based on `W`. The observed rule is H=W, unless W=4, in which case H=5.
5.  Generating an `H x W` grid filled with the digit `N`.

## Facts


```yaml
elements:
  - object: input_grid
    properties:
      - type: grid (matrix) of digits
      - contains: primarily two digits - zero and one unique non-zero digit (N)
      - structure: rows can be all zeros, mostly N, or contain patterns like '0 N...N 0'
  - object: non_zero_digit
    properties:
      - type: digit (e.g., '2', '6', '4')
      - role: foreground color/value
      - uniqueness: only one type per input grid
  - object: zero_digit
    properties:
      - type: digit ('0')
      - role: background color/separator
  - object: pattern_block
    properties:
      - type: contiguous sequence of non_zero_digits
      - location: found within input grid rows that also contain zero_digits
      - structure: bounded by zero_digits (or grid edges acting as boundaries), e.g., '0 N...N 0'
      - characteristic: length (W)
  - object: output_grid
    properties:
      - type: grid (matrix) of digits
      - composition: filled entirely with the non_zero_digit (N) from the input
      - dimensions: H rows x W columns
      - relationship_to_input:
          - W (width) is determined by the length of the pattern_block.
          - H (height) is determined by W (H=W, except if W=4 then H=5).

actions:
  - identify: the unique non_zero_digit (N) in the input_grid.
  - locate: rows in the input_grid containing the pattern_block ('0 N...N 0').
  - measure: the length (W) of the pattern_block.
  - calculate: the output height (H) based on W (H=W, or H=5 if W=4).
  - generate: the output_grid of size H x W, filled with N.

relationships:
  - output_grid width (W) is equal to the pattern_block length (W).
  - output_grid height (H) depends conditionally on the pattern_block length (W).
  - output_grid cell value is the non_zero_digit from the input_grid.
```


## Natural Language Program

1.  Identify the unique non-zero digit (`N`) present in the input grid.
2.  Scan each row of the input grid to find rows containing a contiguous sequence of `N`s that is immediately preceded and followed by a `0`.
3.  Determine the length (`W`) of this contiguous sequence of `N`s. (Assume this length is consistent if multiple such sequences exist).
4.  Calculate the height (`H`) for the output grid: if `W` is 4, set `H` to 5; otherwise, set `H` equal to `W`.
5.  Create a new grid with `H` rows and `W` columns.
6.  Fill every cell of this new grid with the non-zero digit `N`.
7.  Return the newly created grid as the output.