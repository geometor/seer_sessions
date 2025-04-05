
## train_1

**input:**
```
0 2 0 0 1 2 0 0 0 0 2 0
```


**output:**
```
2 2 2 1 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 1 1 0 1 2 2 0 1 0
```


**output:**
```
2 2 1 1 1 1 0 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 0 2 2 0 1 2 0 0 2
```


**output:**
```
2 2 2 2 1 1 1 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 2 0 0 2 0 1 0 0
```


**output:**
```
2 2 1 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
1 1 0 2 1 2 0 0 1 0 1 0
```


**output:**
```
2 2 1 1 1 1 1 0 0 0 0 0
```


## train_6

**input:**
```
1 1 0 1 1 0 1 0 0 0 2 0
```


**output:**
```
2 1 1 1 1 1 0 0 0 0 0 0
```


## train_7

**input:**
```
1 0 0 1 0 2 0 1 0 1 0 0
```


**output:**
```
2 1 1 1 1 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

The task takes a sequence of digits (specifically 0, 1, and 2) presented as a space-separated string. The output is another sequence of the same digits, also space-separated, and having the same length as the input. The core transformation appears to involve rearranging the digits from the input sequence. Upon inspection, the output sequence consistently contains the same count of each digit (0s, 1s, and 2s) as the input sequence, but arranged in descending numerical order (all 2s first, then all 1s, then all 0s).

**YAML Facts:**


```yaml
objects:
  - name: input_sequence
    type: list
    properties:
      - contains: digits (0, 1, 2)
      - length: fixed (12 in examples)
  - name: output_sequence
    type: list
    properties:
      - contains: digits (0, 1, 2)
      - length: same as input_sequence
      - order: descending numerical value (2s, then 1s, then 0s)
actions:
  - name: sort_digits
    input: input_sequence
    output: output_sequence
    description: Arranges the digits from the input sequence into descending order.
relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    via: sort_digits
  - type: conservation
    description: The count of each distinct digit (0, 1, 2) is preserved between the input_sequence and the output_sequence.
```


**Natural Language Program:**

1.  Read the input string.
2.  Parse the string into a sequence of individual integer digits.
3.  Sort this sequence of digits in descending numerical order (largest to smallest).
4.  Format the sorted sequence back into a space-separated string.
5.  Output the resulting string.
