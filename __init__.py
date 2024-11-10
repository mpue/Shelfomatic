# Blender Add-on Template
# Contributor(s): Aaron Powell (aaron@lunadigital.tv)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy.types import PropertyGroup
from bpy.props import PointerProperty
from mathutils import Vector
import math

bl_info = {
        "name": "Shelfomatic",
        "description": "A ahelf generator.",
        "author": "Matthias Pueski / Jens Gebauer",
        "version": (1, 0),
        "blender": (2, 80, 0),
        "location": "Tools",
        "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "http://my.wiki.url",
        "tracker_url": "http://my.bugtracker.url",
        "support": "COMMUNITY",
        "category": "Shelfomatic"
        }

def update_func(self,context):
    bpy.data.objects['Shelfomatic'].select_set(True)
    bpy.ops.object.delete()
    bpy.ops.Shelfomatic.op()

class Shelfomatic_PG_Props(PropertyGroup):

    enum_options = [
        ("TYPE_A", "Latten", "A classic shelf" ,"MOD_LATTICE",1),
    ]

    shelf_type : bpy.props.EnumProperty(name = "Shelf type",items=enum_options, default="TYPE_A")
    num_panels : bpy.props.IntProperty(name="Num boards", min=1, default=2,update=update_func)
    board_thickness : bpy.props.FloatProperty(name="Board width",min = 0.1, default=0.25, update=update_func)
    board_height : bpy.props.FloatProperty(name="Board height", min = 0.1, default=1.5,update=update_func)
    board_distance : bpy.props.FloatProperty(name="Board distance", min = 0.1, default=4,update=update_func)    
    vbar_width : bpy.props.FloatProperty(name="Vertical bar width", min = 1, default=1,update=update_func)
    roof_scale : bpy.props.FloatProperty(name="Tip scale", min = 0.1,default=0.3,update=update_func)
    roof_height : bpy.props.FloatProperty(name="Tip height", min = 0.1,default=1,update=update_func)
    distance : bpy.props.FloatProperty(name="Vertical Bar distance", min = 0,default=4,update=update_func)
    num_elements : bpy.props.IntProperty(name="Num bars", min=1, default=8,update=update_func)
    bend : bpy.props.FloatProperty(name="Bend factor", default=0.0,update=update_func)
    
    scale : FloatVectorProperty(
        name="Lath scale",
        default=(2.0, 0.3, 8.0),
        subtype='TRANSLATION',
        description="scaling",
        update=update_func
    )

    panel_offset : FloatVectorProperty(
        name="Panel offset",
        default=(0.0, 0.5, 2.0),
        subtype='TRANSLATION',
        description="scaling",
        update=update_func
    )        

class ShelfomaticOperator(bpy.types.Operator):

    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "shelfomatic.op"
    bl_label = "Add Shelfomatic"


    def execute(self, context):
        props = context.scene.props        
        bpy.ops.object.select_all(action='DESELECT')

        if context.scene.props.shelf_type == 'TYPE_A':
            self.add_element(context, props.num_elements,props.distance)

        elif context.scene.props.shelf_type == 'TYPE_A':
            pass

        else:
            pass

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        return True

    def add_element(self, context, num_elements, distance=2.0):
        props = context.scene.props

        scale_x = props.scale.x
        scale_y = props.scale.y
        scale_z = props.scale.z
        distance = props.distance
        props.panel_offset.y = props.board_thickness / 2
        thickness_offset = props.board_thickness    


        for num in range(num_elements):
            _z = 1
            _roof_dist = _z + 0.5
            _cap_scale_x = props.roof_scale
            _cap_scale_y = props.roof_scale
            _vbar_width = props.vbar_width

            # Original vertices (side 1)
            verts = [
                Vector((-_vbar_width / 2 * scale_x + num * distance, 1 * scale_y, 0)), # 0
                Vector((_vbar_width / 2 * scale_x + num * distance, 1 * scale_y, 0)),  # 1
                Vector((_vbar_width / 2 * scale_x + num * distance, -1 * scale_y, 0)), # 2
                Vector((-_vbar_width / 2 * scale_x + num * distance, -1 * scale_y, 0)),# 3

                Vector((-_vbar_width / 2 * scale_x + num * distance, 1 * scale_y, _z * scale_z)), # 4
                Vector((_vbar_width / 2 * scale_x + num * distance, 1 * scale_y, _z * scale_z)),  # 5
                Vector((_vbar_width / 2 * scale_x + num * distance, -1 * scale_y, _z * scale_z)), # 6
                Vector((-_vbar_width / 2 * scale_x + num * distance, -1 * scale_y, _z * scale_z)), # 7

                Vector((-_vbar_width / 2 * _cap_scale_x + num * distance, 1 * _cap_scale_y, _roof_dist + _z * scale_z * props.roof_height)), # 8
                Vector((_vbar_width / 2 * _cap_scale_x + num * distance, 1 * _cap_scale_y, _roof_dist + _z * scale_z * props.roof_height)),  # 9
                Vector((_vbar_width / 2 * _cap_scale_x + num * distance, -1 * _cap_scale_y, _roof_dist + _z * scale_z * props.roof_height)), # 10
                Vector((-_vbar_width / 2 * _cap_scale_x + num * distance, -1 * _cap_scale_y, _roof_dist + _z * scale_z * props.roof_height))  # 11
            ]

            # Mirrored vertices on the opposite side (side 2) with offset along Y-axis
            verts += [
                Vector((-_vbar_width / 2 * scale_x + num * distance, 1 * scale_y + thickness_offset, 0)), # 12
                Vector((_vbar_width / 2 * scale_x + num * distance, 1 * scale_y + thickness_offset, 0)),  # 13
                Vector((_vbar_width / 2 * scale_x + num * distance, -1 * scale_y + thickness_offset, 0)), # 14
                Vector((-_vbar_width / 2 * scale_x + num * distance, -1 * scale_y + thickness_offset, 0)),# 15

                Vector((-_vbar_width / 2 * scale_x + num * distance, 1 * scale_y + thickness_offset, _z * scale_z)), # 16
                Vector((_vbar_width / 2 * scale_x + num * distance, 1 * scale_y + thickness_offset, _z * scale_z)),  # 17
                Vector((_vbar_width / 2 * scale_x + num * distance, -1 * scale_y + thickness_offset, _z * scale_z)), # 18
                Vector((-_vbar_width / 2 * scale_x + num * distance, -1 * scale_y + thickness_offset, _z * scale_z)), # 19

                Vector((-_vbar_width / 2 * _cap_scale_x + num * distance, 1 * _cap_scale_y + thickness_offset, _roof_dist + _z * scale_z * props.roof_height)), # 20
                Vector((_vbar_width / 2 * _cap_scale_x + num * distance, 1 * _cap_scale_y + thickness_offset, _roof_dist + _z * scale_z * props.roof_height)),  # 21
                Vector((_vbar_width / 2 * _cap_scale_x + num * distance, -1 * _cap_scale_y + thickness_offset, _roof_dist + _z * scale_z * props.roof_height)), # 22
                Vector((-_vbar_width / 2 * _cap_scale_x + num * distance, -1 * _cap_scale_y + thickness_offset, _roof_dist + _z * scale_z * props.roof_height))  # 23
            ]

            edges = []
            
            # Define faces to connect both sides (including the thickness offset)
            faces = [
                # Side 1 faces
                [0, 1, 2, 3], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [0, 3, 7, 4],
                [4, 5, 9, 8], [5, 6, 10, 9], [6, 7, 11, 10], [7, 4, 8, 11], [8, 9, 10, 11],
                # Side 2 faces
                [12, 13, 14, 15], [12, 13, 17, 16], [13, 14, 18, 17], [14, 15, 19, 18], [12, 15, 19, 16],
                [16, 17, 21, 20], [17, 18, 22, 21], [18, 19, 23, 22], [19, 16, 20, 23], [20, 21, 22, 23],
            ]
            mesh = bpy.data.meshes.new(name="Shelfomatic")
            obj = bpy.data.objects.new("Shelfomatic", mesh)
            mesh.from_pydata(verts, edges, faces)
            # bpy.ops.transform.rotate(value=math.radians(num), orient_axis='Z')
            # useful for development when the mesh may be invalid.
            # mesh.validate(verbose=True)
            # object_data_add(context, mesh, operator=self)

            collection = bpy.context.collection
            collection.objects.link(obj)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            num_panels = props.num_panels
            _board_distance = props.board_distance

            for i in range(0, num_panels):

                _ox = props.panel_offset.x
                _oy = props.panel_offset.y
                _oz = props.panel_offset.z

                panel_verts = [
                    Vector((_ox - _vbar_width / 2 * scale_x + distance * num , _oy + scale_y * 0.5 - props.board_thickness / 2, _oz +  props.board_height / 2 + _board_distance * i)), # back left botttom
                    Vector((_ox - _vbar_width / 2 * scale_x + distance * num , _oy + scale_y * 0.5 - props.board_thickness / 2, _oz + -props.board_height / 2 + _board_distance * i)), # front left bottom 
                    Vector((_ox - _vbar_width / 2 * scale_x + distance * num , _oy + scale_y * 0.5 + props.board_thickness / 2, _oz +  props.board_height / 2 + _board_distance * i)), # back left top
                    Vector((_ox - _vbar_width / 2 * scale_x + distance * num , _oy + scale_y * 0.5 + props.board_thickness / 2, _oz + -props.board_height / 2 + _board_distance * i)), # front left top
                    Vector((_ox + _vbar_width / 2 * scale_x + distance * num + (distance) -_vbar_width * scale_x  ,_oy + scale_y * 0.5 - props.board_thickness / 2, _oz +  props.board_height / 2 + _board_distance * i)), # back left botttom
                    Vector((_ox + _vbar_width / 2 * scale_x + distance * num + (distance) -_vbar_width * scale_x ,_oy + scale_y * 0.5 - props.board_thickness / 2, _oz + -props.board_height / 2 + _board_distance * i)), # front left bottom 
                    Vector((_ox + _vbar_width / 2 * scale_x + distance * num + (distance) -_vbar_width * scale_x ,_oy + scale_y * 0.5 + props.board_thickness / 2, _oz +  props.board_height / 2 + _board_distance * i)), # back left top
                    Vector((_ox + _vbar_width / 2 * scale_x + distance * num + (distance) -_vbar_width * scale_x ,_oy + scale_y * 0.5 + props.board_thickness / 2, _oz + -props.board_height / 2 + _board_distance * i)) # front left top 
                ]
                panel_edges = []

                panel_faces = []

                if num == 0:
                    panel_faces = [
                        [ 0, 1, 3, 2], # bottom
                        #[ 4, 5, 7, 6], # top
                        [ 0, 1, 5, 4], # left
                        [ 2, 3, 7, 6], # right
                        [ 0, 2, 6, 4], # front
                        [ 1, 3, 7, 5]  # back
                    ]
                elif num == num_elements-1:
                    panel_faces = [
                        #[ 0, 1, 3, 2], # bottom
                        [ 4, 5, 7, 6], # top
                        [ 0, 1, 5, 4], # left
                        [ 2, 3, 7, 6], # right
                        [ 0, 2, 6, 4], # front
                        [ 1, 3, 7, 5]  # back
                    ]
                else:
                    panel_faces = [
                        #[ 0, 1, 3, 2], # bottom
                        #[ 4, 5, 7, 6], # top
                        [ 0, 1, 5, 4], # left
                        [ 2, 3, 7, 6], # right
                        [ 0, 2, 6, 4], # front
                        [ 1, 3, 7, 5]  # back
                    ]

                panel_mesh = bpy.data.meshes.new(name="Shelfomatic_hold")
                panel_obj = bpy.data.objects.new("Shelfomatic_hold", panel_mesh)
                panel_mesh.from_pydata(panel_verts, panel_edges, panel_faces)                
                # object_data_add(context, panel_mesh, operator=self)
                collection = bpy.context.collection
                collection.objects.link(panel_obj)
                bpy.context.view_layer.objects.active = panel_obj
                panel_obj.select_set(True)

            bpy.ops.object.join()

        selected_object = bpy.context.active_object
        selected_object.name = "Shelfomatic"

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.smart_project()
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add the SimpleDeform modifier to the selected object
        modifier = selected_object.modifiers.new(name="MySimpleDeform", type='SIMPLE_DEFORM')

        # Set the deformation type (BEND, TWIST, TAPER, STRETCH)
        modifier.deform_method = 'BEND'
        modifier.deform_axis='Z'
        
        # Set the factor to control the strength of the deformation
        modifier.factor = props.bend  # Adjust this value to control the amount of deformation

        # Update the scene to see the changes
        bpy.context.view_layer.update()


def register():
    from . import properties
    from . import ui
    bpy.utils.register_class(ShelfomaticOperator)
    bpy.utils.register_class(Shelfomatic_PG_Props)
    properties.register()
    ui.register()
    bpy.types.Scene.props = PointerProperty(type=Shelfomatic_PG_Props)



def unregister():
    from . import properties
    from . import ui
    properties.unregister()
    ui.unregister()
    bpy.utils.unregister_class(ShelfomaticOperator)  
    bpy.utils.unregister_class(Shelfomatic_PG_Props)

if __name__ == '__main__':
    register()
