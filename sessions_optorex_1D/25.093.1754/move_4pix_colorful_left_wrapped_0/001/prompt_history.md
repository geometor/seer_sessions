
## train_1

**input:**
```
7 8 7 2 0 0 0 0 8 1 2 7
```


**output:**
```
0 0 0 0 8 1 2 7 7 8 7 2
```


## train_2

**input:**
```
0 0 0 0 0 3 8 8 1 6 0 0
```


**output:**
```
0 3 8 8 1 6 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
2 2 9 5 0 0 0 0 7 5 9 5
```


**output:**
```
0 0 0 0 7 5 9 5 2 2 9 5
```


## train_5

**input:**
```
3 3 1 7 1 6 5 8 5 0 0 1
```


**output:**
```
1 6 5 8 5 0 0 1 3 3 1 7
```


## train_6

**input:**
```
0 0 0 0 0 4 3 6 9 0 0 0
```


**output:**
```
0 4 3 6 9 0 0 0 0 0 0 0
```


## train_7

**input:**
```
1 0 0 0 5 1 9 3 9 3 1 1
```


**output:**
```
5 1 9 3 9 3 1 1 1 0 0 0
```

**Perception:**

The input is a sequence of 12 integers. The output is also a sequence of 12 integers, which appears to be a rearrangement of the input sequence. By comparing the input and output sequences across the examples, a consistent pattern emerges. The input sequence seems to be divided into two subsequences. The first subsequence consists of the first 4 integers, and the second subsequence consists of the remaining 8 integers. The output sequence is formed by placing the second subsequence first, followed by the first subsequence.

**Facts:**


```yaml
task_description: Rearrange a sequence of 12 integers by swapping two fixed-length blocks.
elements:
  - type: sequence
    role: input
    subtype: integer
    length: 12
    representation: space-separated string
  - type: sequence
    role: output
    subtype: integer
    length: 12
    representation: space-separated string
transformation:
  action: split
  input: input sequence
  parameters:
    split_index: 4 # Split after the 4th element (index 3)
  outputs:
    - name: part1
      elements: input[0:4]
    - name: part2
      elements: input[4:12]
  action: concatenate
  inputs:
    - part2
    - part1
  output: output sequence
relationship:
  output_sequence = concatenate(part2, part1) where part1 = input[0:4] and part2 = input[4:12]
```


**Natural Language Program:**

1.  Take the input sequence of 12 integers.
2.  Divide the input sequence into two parts:
    *   The first part consists of the first 4 integers.
    *   The second part consists of the remaining 8 integers (from the 5th to the 12th integer).
3.  Construct the output sequence by concatenating the second part followed by the first part.
