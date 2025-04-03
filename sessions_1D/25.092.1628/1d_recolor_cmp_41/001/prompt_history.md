
## train_1

**input:**
```
0 3 0 0 0 3 3 0 0 3 3 3 0 0 0 3 3 0 3 3 3 3 3 0
```


**output:**
```
0 3 0 0 0 3 3 0 0 3 3 3 0 0 0 3 3 0 2 2 2 2 2 0
```


## train_2

**input:**
```
0 0 3 3 0 0 0 3 3 0 0 3 3 3 0 0 3 3 3 3 0 0 3 0
```


**output:**
```
0 0 3 3 0 0 0 3 3 0 0 3 3 3 0 0 2 2 2 2 0 0 3 0
```


## train_3

**input:**
```
0 0 3 3 0 3 3 3 3 3 3 3 0 3 3 3 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 0 2 2 2 2 2 2 2 0 3 3 3 3 0 0 0 0 0 0 0
```

## Perception

The input and output are presented as one-dimensional arrays of integers, representing pixel colors. The primary colors involved are white (0), green (3), and red (2). The transformation appears to involve identifying specific sequences of green pixels in the input and changing their color to red in the output.

Observing the examples:
1.  **train_1:** The longest sequence of green pixels (`3 3 3 3 3`, length 5) is changed to red (`2 2 2 2 2`).
2.  **train_2:** The longest sequence of green pixels (`3 3 3 3`, length 4) is changed to red (`2 2 2 2`).
3.  **train_3:** The longest sequence of green pixels (`3 3 3 3 3 3 3`, length 7) is changed to red (`2 2 2 2 2 2 2`).

The core operation is locating the single longest contiguous block of green pixels (value 3) within the 1D input array and replacing all pixels in that block with red pixels (value 2). Other green pixels and pixels of other colors remain unchanged. If there happened to be multiple sequences of the same maximal length, the examples suggest the *first* such sequence encountered (reading left-to-right) is the one modified, though this scenario isn't explicitly demonstrated in the provided examples.

## Facts


```yaml
Task: Color replacement based on sequence length

Input:
  Type: 1D array of integers (pixels)
  Colors:
    - White (0)
    - Green (3)
    - Other colors (potentially, though not modified in examples)

Output:
  Type: 1D array of integers (pixels) - Modified version of input.

Elements:
  - Pixels: Individual cells with color values.
  - Sequences: Contiguous runs of pixels with the same color value. Specifically interested in sequences of Green (3) pixels.

Properties:
  - Sequence Length: The number of pixels in a contiguous sequence.

Actions:
  - Identify: Find all contiguous sequences of Green (3) pixels in the input array.
  - Measure: Determine the length of each Green sequence.
  - Compare: Find the maximum length among all Green sequences.
  - Select: Choose the first sequence encountered that has the maximum length.
  - Replace: Change the color value of every pixel within the selected sequence from Green (3) to Red (2).

Relationships:
  - The transformation targets the Green sequence that is longer than any other Green sequence in the input array.
  - Only the pixels within the single longest Green sequence are modified.
  - All other pixels retain their original color.
```


## Natural Language Program

1.  Receive the input as a one-dimensional array of pixel colors.
2.  Iterate through the input array to identify all contiguous sequences (runs) of green pixels (value 3). Keep track of the starting index and length of each green sequence found.
3.  Determine the maximum length found among all identified green sequences.
4.  Identify the specific green sequence that has this maximum length. If multiple sequences share the maximum length, select the one that appears earliest (smallest starting index) in the array.
5.  Create a copy of the input array to serve as the output array.
6.  Modify the output array by changing the color of all pixels within the selected longest green sequence from green (3) to red (2).
7.  Return the modified output array.
