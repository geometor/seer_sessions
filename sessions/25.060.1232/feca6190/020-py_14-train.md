
## example 1
*input:*
```
1 0 7 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1 0 7
0 0 0 0 0 0 1 0 7 0
0 0 0 0 0 1 0 7 0 0
0 0 0 0 1 0 7 0 0 0
0 0 0 1 0 7 0 0 0 0
0 0 1 0 7 0 0 0 0 0
0 1 0 7 0 0 0 0 0 0
1 0 7 0 0 0 0 0 0 0
```
*transformed output:*
```
1 0 7 0 0
0 1 0 7 0
0 0 1 0 7
7 0 0 1 0
0 7 0 0 1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 2 0 0
```
*expected output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
0 0 0 2 0
0 0 2 0 0
```
*transformed output:*
```
0 0 2 0 0
0 0 0 2 0
0 0 0 0 2
2 0 0 0 0
0 2 0 0 0
```
size: True
palette: True
color count: False
pixels off: 6
**FAILED!**

## example 3
*input:*
```
4 0 6 0 8
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 4 0 6
0 0 0 0 0 0 0 0 0 0 0 4 0 6 0
0 0 0 0 0 0 0 0 0 0 4 0 6 0 8
0 0 0 0 0 0 0 0 0 4 0 6 0 8 0
0 0 0 0 0 0 0 0 4 0 6 0 8 0 0
0 0 0 0 0 0 0 4 0 6 0 8 0 0 0
0 0 0 0 0 0 4 0 6 0 8 0 0 0 0
0 0 0 0 0 4 0 6 0 8 0 0 0 0 0
0 0 0 0 4 0 6 0 8 0 0 0 0 0 0
0 0 0 4 0 6 0 8 0 0 0 0 0 0 0
0 0 4 0 6 0 8 0 0 0 0 0 0 0 0
0 4 0 6 0 8 0 0 0 0 0 0 0 0 0
4 0 6 0 8 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
4 0 6 0 8
8 4 0 6 0
0 8 4 0 6
6 0 8 4 0
0 6 0 8 4
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
0 9 0 8 4
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 9 0 8
0 0 0 0 0 0 0 0 0 0 0 9 0 8 4
0 0 0 0 0 0 0 0 0 0 9 0 8 4 0
0 0 0 0 0 0 0 0 0 9 0 8 4 0 0
0 0 0 0 0 0 0 0 9 0 8 4 0 0 0
0 0 0 0 0 0 0 9 0 8 4 0 0 0 0
0 0 0 0 0 0 9 0 8 4 0 0 0 0 0
0 0 0 0 0 9 0 8 4 0 0 0 0 0 0
0 0 0 0 9 0 8 4 0 0 0 0 0 0 0
0 0 0 9 0 8 4 0 0 0 0 0 0 0 0
0 0 9 0 8 4 0 0 0 0 0 0 0 0 0
0 9 0 8 4 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 9 0 8 4
4 0 9 0 8
8 4 0 9 0
0 8 4 0 9
9 0 8 4 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 5
*input:*
```
0 4 0 0 0
```
*expected output:*
```
0 0 0 0 0
0 0 0 0 4
0 0 0 4 0
0 0 4 0 0
0 4 0 0 0
```
*transformed output:*
```
0 4 0 0 0
0 0 4 0 0
0 0 0 4 0
0 0 0 0 4
4 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 7
**FAILED!**
