
## train_1

**input:**
```
3 0 3 0 3 0 0 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 0 0 0
```


## train_2

**input:**
```
3 0 0 3 3 3 3 3 0 3 0 0
```


**output:**
```
0 0 0 3 3 3 3 3 0 0 0 0
```


## train_3

**input:**
```
0 5 5 0 5 0 0 0 5 0 5 0
```


**output:**
```
0 5 5 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 2 0 0 0 2 2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 2 2 2 2 2 2 2
```


## train_5

**input:**
```
0 4 4 4 4 4 4 4 4 4 0 4
```


**output:**
```
0 4 4 4 4 4 4 4 4 4 0 0
```


## train_6

**input:**
```
1 1 0 0 0 1 0 0 1 0 0 0
```


**output:**
```
1 1 0 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 6 0 0 6 0 6 0 0 0 6 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 6 6
```

Okay, let's break down the transformation.

**Perception of the Elements:**

1.  **Input/Output Data Type:** Both input and output are sequences (represented as space-separated strings) of single-digit non-negative integers.
2.  **Core Operation:** The transformation modifies the input sequence by selectively changing some non-zero numbers to zero. The positions of the zeros in the input generally seem to be preserved, unless a non-zero number at that position is changed to zero.
3.  **Key Pattern:** The transformation appears to operate on contiguous blocks (or runs) of identical non-zero numbers. For each unique non-zero number present in the input (e.g., '3' in `train_1`, '5' in `train_3`), the rule identifies all contiguous blocks of that number.
4.  **Filtering Logic:** Within the set of blocks for a specific number, the block with the maximum length is identified. Only the elements belonging to this longest block are retained in the output sequence. All other occurrences of that same number (belonging to shorter blocks) are replaced with 0.
5.  **Independence:** This process seems to be applied independently for each distinct non-zero value found in the input sequence.

**YAML Facts:**


```yaml
task_elements:
  - object: Sequence
    description: A list of single-digit integers.
    properties:
      - length: The number of elements in the sequence.
      - elements: The individual integers in the sequence.

  - object: Element
    description: A single integer within the sequence.
    properties:
      - value: The integer itself (0-9).
      - position: The index of the element in the sequence.

  - object: Block
    description: A contiguous sub-sequence of identical non-zero elements.
    properties:
      - value: The non-zero integer that makes up the block.
      - start_index: The position of the first element of the block.
      - end_index: The position of the last element of the block.
      - length: The number of elements in the block (end_index - start_index + 1).

relationships:
  - type: BelongsTo
    description: An Element belongs to a Sequence.
  - type: Forms
    description: Multiple contiguous Elements with the same non-zero value form a Block.

actions:
  - action: IdentifyBlocks
    description: For a given non-zero value N, find all contiguous Blocks of N within the input Sequence.
    inputs:
      - Sequence
      - N (non-zero integer value)
    outputs:
      - List of Blocks (each containing value, start_index, end_index, length)

  - action: FindLongestBlock
    description: From a list of Blocks for a specific value N, find the Block with the maximum length. (Assumes a unique longest block based on examples).
    inputs:
      - List of Blocks for value N
    outputs:
      - The single Block with the greatest length.

  - action: FilterSequence
    description: Create the output sequence by preserving elements belonging to the longest block for each non-zero value and replacing all other non-zero elements with 0.
    inputs:
      - Input Sequence
      - Set of longest Blocks (one for each unique non-zero value in the input)
    outputs:
      - Output Sequence
```


**Natural Language Program:**

1.  Initialize the output sequence as a copy of the input sequence.
2.  Identify all unique non-zero integer values present in the input sequence.
3.  For each unique non-zero value `N` identified:
    a.  Find all contiguous blocks (runs) of `N` within the input sequence. Record their start index, end index, and length.
    b.  If no blocks of `N` are found, continue to the next unique non-zero value.
    c.  Determine the maximum length among all found blocks of `N`.
    d.  Identify the specific block of `N` that has this maximum length. (Based on the examples, there appears to be only one such block for each `N`). Let this be the `longest_block`.
    e.  Iterate through all the originally found blocks of `N`. For every block that is *not* the `longest_block`:
        i.  Iterate through the indices from the block's start index to its end index.
        ii. Set the element at each of these indices in the *output* sequence to 0.
4.  Return the modified output sequence.
