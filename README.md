# Terminal-Render
Render in terminal (rendered in 15 seconds)

![work-example](https://raw.githubusercontent.com/Alick09/Terminal-Render/master/misc/example2.png "work example")


# Options

In the root you can find `options.json` file:
* `fix_coeff` - pixel_height/pixel_width value (1 by default)
* `antialiasing_level` - antialiasing level (1 by default, other values not implemented yet)
* `use_ssao` - if true ssao calculation will be performed (false by default)
* `ssao_mc_tests` - number of monte-carlo tests for ssao (10 by default)


# Implemented

* Static camera
* Rectangles and Boxes
* Terminal material (SevenColorsMaterial)
* Scene
* Simple ray casting
* 9-symbol shades rendering
* SSAO using Monte-Carlo method


# TO-DO

* Implement camera rotation using mouse
* Add support of other encodings
* Add another types of objects
* Add object loading
* Implement antialiasing
* Speed up
