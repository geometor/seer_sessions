
## example 1
*input:*
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 3 3 1 3 3 1
1 1 1 2 2 2 2 2 1 1 1 3 1 1 1 3 1
1 1 1 2 1 2 1 2 1 1 1 3 3 3 3 3 1
1 1 1 1 1 1 1 2 1 1 1 1 1 3 1 1 1
1 1 1 2 1 2 1 2 1 1 1 3 3 3 3 3 1
1 1 1 2 2 2 2 2 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 8 8 8 8 8 8 8 8 8 8 1 1 1 1
1 1 1 8 8 8 8 8 8 8 8 8 8 1 1 1 1
1 1 1 8 8 1 1 8 8 1 1 8 8 1 1 1 1
1 1 1 8 8 1 1 8 8 1 1 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1
1 1 1 8 8 1 1 8 8 1 1 8 8 1 1 1 1
1 1 1 8 8 1 1 8 8 1 1 8 8 1 1 1 1
```
*expected output:*
```
2 2 2 2 2
2 1 2 1 2
1 1 1 1 2
2 1 2 1 2
2 2 2 2 2
```
*transformed output:*
```
1 1 1 1 1 1 1 1
1 1 3 3 1 3 3 1
1 1 3 1 1 1 3 1
1 1 3 3 3 3 3 1
1 1 1 1 3 1 1 1
1 1 3 3 3 3 3 1
1 1 1 1 1 1 1 1
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 8 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 8 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 4 4 4 8 8 8 8
8 6 6 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 6 6 8 8 8 8 8 8 8 8 4 4 4 8 8 8 8
6 6 6 6 6 8 8 8 8 8 8 8 4 8 8 8 8 8
6 6 6 6 6 8 8 8 8 8 8 8 8 8 8 8 8 8
8 6 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 6 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
6 6 6 6 6 8 8 8 8 8 8 8 8 8 8 8 8 8
6 6 6 6 6 8 8 8 8 8 8 8 8 8 8 8 8 8
```
*expected output:*
```
8 4 8
4 4 4
8 4 8
4 4 4
8 4 8
```
*transformed output:*
```
1 1 1 1 1 1 1 1 1
1 1 1 3 1 3 1 1 1
1 1 3 3 3 3 3 1 1
1 1 1 3 1 3 1 1 1
1 1 1 1 1 1 1 1 1
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 8 8 8 2 2 2 2 2 2 2 2 2 2
2 2 2 2 8 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 8 8 8 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 8 2 2 2 2 2 2 2 2 2 2
2 2 2 2 8 8 8 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 3 2 3 2 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 2 2 3 2 2 2 2 2 2
1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2
```
*expected output:*
```
8 8 8
8 2 2
8 8 8
2 2 8
8 8 8
```
*transformed output:*
```
1 1 1 1 1 1 1 1 1
1 1 3 1 3 1 3 1 1
1 1 3 3 3 3 3 1 1
1 1 1 1 3 1 1 1 1
1 1 1 1 1 1 1 1 1
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 1 1 8 1 1 1 1 1 1 1 1
1 1 1 1 1 8 8 8 8 1 1 1 1 1 1 1 1
1 1 1 1 1 8 1 1 8 1 1 1 1 1 1 1 1
1 1 1 1 1 8 8 8 8 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 2 2 1 1 1 1 3 3 3 1 1 1 1 1
2 2 2 2 2 1 1 1 3 3 1 3 3 1 1 1 1
2 1 1 2 2 2 2 1 1 3 3 3 1 1 1 1 1
2 1 1 2 2 2 2 1 1 1 1 1 1 1 1 1 1
2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1
```
*expected output:*
```
1 3 3 3 1
3 3 1 3 3
1 3 3 3 1
```
*transformed output:*
```
1 1 1 1 1 1 1 1 1
1 1 1 3 3 3 1 1 1
1 1 3 3 1 3 3 1 1
1 1 1 3 3 3 1 1 1
1 1 1 1 1 1 1 1 1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
