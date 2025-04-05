
## train_1

**input:**
```
0 0 0 0 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 7 7 0 0
```


## train_2

**input:**
```
2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 7 7
```


## train_4

**input:**
```
0 0 0 1 1 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 0 0 0
```


## train_5

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 2 2 2 2 2 2
```


## train_7

**input:**
```
0 0 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 2 0 0 0 0 0
```

**Perception of Task Elements:**

The task operates on fixed-length sequences of integers (length 12 in the examples). Each input sequence contains a single contiguous block of non-zero integers, surrounded by zeros. The zeros appear to represent empty space or a background. The transformation involves relocating the non-zero block within the sequence. The non-zero block itself remains unchanged in terms of the numbers it contains and their order. The surrounding zeros are adjusted to accommodate the moved block.

**YAML Fact Sheet:**


```yaml
Data:
  Type: Sequence (List) of Integers
  Length: Fixed (12 in examples)
  Elements: Integers, including zero and non-zero values

Objects:
  - Name: Background
    Representation: Integer 0
    Role: Fills empty space in the sequence
  - Name: Pattern
    Representation: Contiguous sequence of non-zero integers
    Properties:
      - Values: The specific non-zero integers making up the pattern.
      - Length: The number of integers in the pattern.
      - Position: The starting index of the pattern in the input sequence.
    Cardinality: Exactly one per input sequence.

Action:
  Name: Shift Right
  Target: The Pattern object
  Parameter:
    - Name: Shift Distance
      Value: 4 positions
  Result: The Pattern object is moved 4 positions to the right within the sequence. The original positions occupied by the Pattern are filled with the Background value (0).

Relationships:
  - The Pattern is embedded within the Background.
  - The output sequence preserves the length, the Pattern's content, and the Background representation, but the Pattern's position is altered relative to the input.
```


**Natural Language Program:**

1.  Scan the input sequence to locate the start and end indices of the single contiguous block of non-zero numbers (the "pattern").
2.  Determine the starting index of this pattern.
3.  Create a new output sequence of the same length as the input, initially filled entirely with zeros.
4.  Calculate the new starting index for the pattern by adding 4 to its original starting index.
5.  Copy the identified pattern (the sequence of non-zero numbers) from the input into the output sequence, placing it starting at the calculated new index.
6.  The output sequence, now containing the shifted pattern and zeros elsewhere, is the result.
