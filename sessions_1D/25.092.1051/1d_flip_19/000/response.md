**Perception of Task Elements**

The task operates on 1-dimensional grids (rows). Each input grid contains a single contiguous block of non-white pixels (pixels with values 1-9) surrounded by white pixels (value 0). The white pixels act as background or padding. The transformation modifies the arrangement of colors *within* the non-white block, while the positions of the white pixels and the overall location of the non-white block remain unchanged. Specifically, the first pixel of the non-white block is moved to the end of that block, and all other pixels within the block shift one position to the left.

**YAML Facts**


```yaml
task_type: array_manipulation
grid_dimensionality: 1D
grid_size: variable width (1xN)
pixel_colors: 0-9 representing colors (0=white, 1-9=non-white)

input_features:
  - background:
      color: white (0)
      description: Surrounds the main object.
  - object:
      description: A single contiguous block of non-white pixels.
      composition: Sequence of non-white colors (1-9).
      location: Varies across examples.
      size: Varies across examples (length >= 2).

output_features:
  - background:
      description: Identical in position and color to the input background.
  - object:
      description: The same contiguous block as in the input, but with rearranged colors.
      composition: The sequence of non-white colors from the input object, cyclically shifted left by one position.
      location: Same indices as the input object block.
      size: Same length as the input object block.

transformation:
  - identify: Locate the start and end indices of the contiguous block of non-white pixels.
  - extract: Get the sequence of colors within this block.
  - manipulate: Perform a left cyclic shift on the extracted sequence (move the first element to the end).
  - replace: Place the manipulated sequence back into the original start and end indices in the grid.
  - invariant: White pixels (value 0) remain unchanged.
```


**Natural Language Program**

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through the input grid to find the start index and end index of the contiguous sequence of non-white pixels (pixels with values greater than 0).
3.  Extract the sub-sequence of non-white pixel values from the identified start index to the end index.
4.  If the extracted sub-sequence contains more than one element:
    a.  Store the value of the first element of the sub-sequence.
    b.  Shift all subsequent elements in the sub-sequence one position to the left.
    c.  Place the stored first element's value into the last position of the sub-sequence.
5.  Replace the pixel values in the output grid from the start index to the end index with the modified sub-sequence.
6.  Return the modified output grid.