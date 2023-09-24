# DQBCTEGS
## DQ: Blender Collection To Empty Godot Saver

![This is what the conversion looks like](./readme/preview.png)

# What does this plugin do?
This plugin generates a save of your .blend file which transfers over blender collections (and their Godot-related flags) to Godot.

- -noimp & -col flag works with collections.
- you can use -imp/nocol flag on an object to negate a -noimp/col flag on a parent collection. -imp/col flag can also be chained with one more flag: -imp-colonly will get imported, with a -colonly flag

# How to use
1. Load the .py from [releases](https://github.com/SwatDoge/DQBCTEGS/tags) in blender as a plugin.
2. Save your project as .blend in your project. When saving it will generate a godot_\<filename\>.blend
3. You can import this godot_\<filename\>.blend into your project, enjoy your collections!

# Planned
- support for more flags
