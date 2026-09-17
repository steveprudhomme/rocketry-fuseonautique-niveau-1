"""Fixed camera detail of smoke advection, without modifying the saved scene."""
import bpy
from pathlib import Path
from mathutils import Vector
s=bpy.context.scene;cam=s.camera;cam.animation_data_clear();cam.location=(9,-15,7);target=Vector((-2,0,3.5));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=43
s.frame_start=61;s.frame_end=301;s.render.filepath=str(Path('work/atmosphere-v4/detail/fumee-').resolve());bpy.ops.render.render(animation=True)
