
## example 1
*input:*
```
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 0 0 0 2
0 3 3 3 3 3
0 0 0 0 0 3
0 0 0 0 0 3
```
*transformed output:*
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 2 2 2 2
0 3 3 3 3 3
0 0 2 2 2 2
0 0 2 2 2 2
```
size: True
palette: True
color count: False
pixels off: 11
**FAILED!**

## example 2
*input:*
```
0 0 0
0 6 0
0 0 0
```
*expected output:*
```
0 0 0
0 6 6
0 0 6
```
*transformed output:*
```
0 0 0
0 6 6
0 6 6
```
size: True
palette: True
color count: False
pixels off: 1
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 5 0 0
0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 8 8 8 8 8
0 0 0 0 0 8
0 0 0 0 0 8
0 0 0 5 5 5
0 0 0 0 0 5
```
*transformed output:*
```
0 0 0 0 0 0
0 8 8 8 8 8
0 8 8 8 8 8
0 8 8 8 8 8
0 8 8 5 5 5
0 8 8 8 8 8
```
size: True
palette: True
color count: False
pixels off: 15
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
0 7 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 0 8 8 8
0 0 0 0 8
0 7 7 7 7
0 0 0 0 7
0 0 6 6 6
0 0 0 0 6
```
*transformed output:*
```
0 0 0 0 0
0 0 8 8 8
0 0 8 8 8
0 7 7 7 7
0 0 8 8 8
0 0 6 6 6
0 0 8 8 8
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**
