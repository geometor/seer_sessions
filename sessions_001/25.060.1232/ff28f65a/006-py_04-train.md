
## example 1
*input:*
```
2 2 0 0 0
2 2 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
*expected output:*
```
1 0 0
0 0 0
0 0 0
```
*transformed output:*
```
0 0 0 0
0 1 0 0
0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0
0 2 2 0 0
0 2 2 0 0
0 0 0 2 2
0 0 0 2 2
```
*expected output:*
```
1 0 1
0 0 0
0 0 0
```
*transformed output:*
```
0 0 0
0 1 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0
0 2 2 0 0 0 0
0 2 2 0 2 2 0
0 0 0 0 2 2 0
0 0 2 2 0 0 0
0 0 2 2 0 0 0
0 0 0 0 0 0 0
```
*expected output:*
```
1 0 1
0 1 0
0 0 0
```
*transformed output:*
```
0 0 0
0 1 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 2
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0
0 2 2 0 0 0
0 2 2 0 0 0
0 0 0 0 0 0
0 0 2 2 0 0
0 0 2 2 0 0
```
*expected output:*
```
1 0 1
0 0 0
0 0 0
```
*transformed output:*
```
0 0 0 0
0 1 0 0
0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 5
*input:*
```
0 0 0
0 2 2
0 2 2
```
*expected output:*
```
1 0 0
0 0 0
0 0 0
```
*transformed output:*
```
0 0 0
0 1 0
0 0 0
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**

## example 6
*input:*
```
0 0 0 0 2 2 0
0 0 0 0 2 2 0
0 2 2 0 0 0 0
0 2 2 0 2 2 0
0 0 0 0 2 2 0
0 2 2 0 0 0 0
0 2 2 0 0 0 0
```
*expected output:*
```
1 0 1
0 1 0
1 0 0
```
*transformed output:*
```
0 0 0
0 1 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**

## example 7
*input:*
```
0 0 0 0 2 2 0
0 2 2 0 2 2 0
0 2 2 0 0 0 0
0 0 0 0 0 2 2
2 2 0 0 0 2 2
2 2 0 2 2 0 0
0 0 0 2 2 0 0
```
*expected output:*
```
1 0 1
0 1 0
1 0 1
```
*transformed output:*
```
0 0 0
0 1 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 4
**FAILED!**

## example 8
*input:*
```
0 0 2 2 0 2 2
0 0 2 2 0 2 2
2 2 0 0 0 0 0
2 2 0 2 2 0 0
0 0 0 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```
*expected output:*
```
1 0 1
0 1 0
1 0 0
```
*transformed output:*
```
0 0 0
0 1 0
0 0 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**
