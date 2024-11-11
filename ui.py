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
from bpy.types import Panel

#
# Add additional functions here
#

class LZ_PT_MainPanel(Panel):
    
    bl_label = 'Shelfomatic'
    bl_space_type = 'VIEW_3D'
    bl_region_type= 'UI'
    bl_category = 'Shelfomatic'


    def draw(self, context):

        props = context.scene.props

        row = self.layout.row()
        row.operator("Shelfomatic.op")
        row = self.layout.row()
        row.prop(props, 'shelf_type')
        row = self.layout.row()        
        row.separator()
        row.prop(props, 'scale')
        row = self.layout.row()
        row.prop(props, 'board_width')
        row = self.layout.row()
        row.prop(props, 'num_panels')
        row.prop(props, 'board_distance')
        row = self.layout.row()
        row.prop(props, 'board_thickness')
        row = self.layout.row()
        row.prop(props, 'board_height')
        row = self.layout.row()
        row.prop(props, 'distance')
        row = self.layout.row()
        row.prop(props, 'num_elements')
        row = self.layout.row()
        row.prop(props, 'bend')
        row = self.layout.row()
        row.prop(props, 'roof_height')
        row = self.layout.row()
        row.prop(props, 'roof_scale')
        row = self.layout.row()
        row.prop(props, 'panel_offset')
        row.separator()

        # Add material selection fields
        row = self.layout.row()
        row.prop_search(props, "board_material", bpy.data, "materials", text="Board Material")
        
        row = self.layout.row()
        row.prop_search(props, "vbar_material", bpy.data, "materials", text="Vertical Bar Material")


def register():
    bpy.utils.register_class(LZ_PT_MainPanel)

def unregister():
    bpy.utils.unregister_class(LZ_PT_MainPanel)
