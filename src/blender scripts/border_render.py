# $ blender -b <file.blend> -P border_render.py -- <minx> <maxx> <miny> <maxy> <frame_number>
import bpy
import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]

scn = bpy.data.scenes["Scene"]

frame = int(argv[4])
scn.frame_set(frame)
scn = bpy.context.scene

scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_mode = 'RGBA'

# setup the render border
scn.render.use_border = True
scn.render.use_compositing = False
scn.render.film_transparent = True
scn.render.border_min_x = float(argv[0])
scn.render.border_max_x = float(argv[1])
scn.render.border_min_y = float(argv[2])
scn.render.border_max_y = float(argv[3])

# render a still frame
scn.render.filepath = '//br.png'
bpy.ops.render.render(write_still=True)