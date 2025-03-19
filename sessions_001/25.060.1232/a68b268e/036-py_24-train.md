
## example 1
*input:*
```
0 7 7 7 1 0 4 0 4
7 7 7 0 1 4 4 0 0
0 0 0 0 1 0 0 0 4
7 0 0 0 1 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 1 6 6 6 0
0 0 8 8 1 0 0 0 0
8 0 8 0 1 6 0 0 6
0 0 0 8 1 0 0 0 0
```
*expected output:*
```
6 7 7 7
7 7 7 8
8 0 8 4
7 0 0 8
```
*transformed output:*
```
0 0 0 4
0 0 0 4
0 0 0 4
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 2
*input:*
```
7 7 7 0 1 0 4 0 0
7 0 7 0 1 4 0 4 4
0 7 0 7 1 4 0 4 4
0 0 0 7 1 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 8 0 1 6 0 0 6
0 0 0 0 1 6 0 0 0
0 0 0 0 1 6 6 0 6
8 8 8 0 1 6 0 6 6
```
*expected output:*
```
7 7 7 6
7 0 7 4
4 7 4 7
8 8 8 7
```
*transformed output:*
```
7 7 7 0
7 7 7 0
7 7 7 0
7 7 7 6
```
size: True
palette: True
color count: False
pixels off: 10
**FAILED!**

## example 3
*input:*
```
0 0 7 7 1 0 4 4 0
0 0 0 7 1 0 0 4 4
7 7 7 7 1 0 0 0 4
0 7 0 0 1 0 4 4 0
1 1 1 1 1 1 1 1 1
0 0 8 8 1 0 6 6 6
0 0 0 0 1 0 0 6 0
0 0 0 8 1 6 0 6 0
8 0 0 0 1 6 6 0 0
```
*expected output:*
```
0 4 7 7
0 0 4 7
7 7 7 7
8 7 4 0
```
*transformed output:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 4
*input:*
```
7 7 0 0 1 4 4 0 4
7 0 7 0 1 4 0 0 0
7 0 0 7 1 4 4 4 0
7 0 7 7 1 4 0 4 4
1 1 1 1 1 1 1 1 1
0 0 8 0 1 0 0 0 0
0 0 8 0 1 6 6 0 0
0 0 8 0 1 0 6 6 6
0 8 0 8 1 0 6 6 0
```
*expected output:*
```
7 7 8 4
7 6 7 0
7 4 4 7
7 8 7 7
```
*transformed output:*
```
7 7 7 4
7 7 7 4
7 7 7 4
7 7 7 0
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**

## example 5
*input:*
```
7 7 0 0 1 0 0 0 4
7 0 0 0 1 4 4 4 4
7 0 7 0 1 4 0 0 0
0 7 7 0 1 4 4 4 0
1 1 1 1 1 1 1 1 1
8 0 8 0 1 6 6 6 6
0 0 8 8 1 0 0 6 0
0 0 0 0 1 0 6 0 6
8 8 8 8 1 0 0 0 6
```
*expected output:*
```
7 7 8 4
7 4 4 4
7 6 7 6
4 7 7 8
```
*transformed output:*
```
7 7 7 4
7 7 7 4
7 7 7 4
7 7 7 6
```
size: True
palette: True
color count: False
pixels off: 7
**FAILED!**

## example 6
*input:*
```
7 0 0 7 1 4 4 4 0
0 7 7 7 1 4 4 0 4
7 7 7 0 1 4 4 0 4
7 7 7 0 1 0 4 0 0
1 1 1 1 1 1 1 1 1
8 8 0 8 1 6 6 6 6
0 8 8 8 1 0 0 0 6
0 8 0 8 1 0 0 6 0
8 8 0 8 1 0 6 0 0
```
*expected output:*
```
7 4 4 7
4 7 7 7
7 7 7 4
7 7 7 8
```
*transformed output:*
```
7 7 7 0
7 7 7 0
7 7 7 0
7 7 7 0
```
size: True
palette: False
color count: False
pixels off: 7
**FAILED!**
