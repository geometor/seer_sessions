
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
1 0
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
0 1
```
size: False
palette: True
color count: False
pixels off: None
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
0 1 1 0
```
size: False
palette: True
color count: False
pixels off: None
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
0 1 1
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

```
**ERROR**: Could not save image: 'NoneType' object has no attribute 'to_image'

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
0 1 0 0
```
size: False
palette: True
color count: False
pixels off: None
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
1 1 0 1
```
size: False
palette: True
color count: False
pixels off: None
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
1 0 1 1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
