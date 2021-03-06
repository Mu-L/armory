from typing import Optional

import arm.material.cycles as cycles
import arm.material.mat_state as mat_state
import arm.material.make_skin as make_skin
import arm.material.make_particle as make_particle
import arm.material.make_inst as make_inst
import arm.material.make_tess as make_tess
from arm.material.shader import Shader, ShaderContext
import arm.utils


def write_vertpos(vert):
    billboard = mat_state.material.arm_billboard
    particle = mat_state.material.arm_particle_flag
    # Particles
    if particle:
        if arm.utils.get_rp().arm_particles == 'On':
            make_particle.write(vert, particle_info=cycles.particle_info)
        # Billboards
        if billboard == 'spherical':
            vert.add_uniform('mat4 WV', '_worldViewMatrix')
            vert.add_uniform('mat4 P', '_projectionMatrix')
            vert.write('gl_Position = P * (WV * vec4(0.0, 0.0, spos.z, 1.0) + vec4(spos.x, spos.y, 0.0, 0.0));')
        else:
            vert.add_uniform('mat4 WVP', '_worldViewProjectionMatrix')
            vert.write('gl_Position = WVP * spos;')
    else:
        # Billboards
        if billboard == 'spherical':
            vert.add_uniform('mat4 WVP', '_worldViewProjectionMatrixSphere')
        elif billboard == 'cylindrical':
            vert.add_uniform('mat4 WVP', '_worldViewProjectionMatrixCylinder')
        else: # off
            vert.add_uniform('mat4 WVP', '_worldViewProjectionMatrix')
        vert.write('gl_Position = WVP * spos;')


def write_norpos(con_mesh: ShaderContext, vert: Shader, declare=False, write_nor=True):
    is_bone = con_mesh.is_elem('bone')
    if is_bone:
        make_skin.skin_pos(vert)
    if write_nor:
        prep = 'vec3 ' if declare else ''
        if is_bone:
            make_skin.skin_nor(vert, prep)
        else:
            vert.write_attrib(prep + 'wnormal = normalize(N * vec3(nor.xy, pos.w));')
    if con_mesh.is_elem('ipos'):
        make_inst.inst_pos(con_mesh, vert)


def write_tex_coords(con_mesh: ShaderContext, vert: Shader, frag: Shader, tese: Optional[Shader]):
    rpdat = arm.utils.get_rp()

    if con_mesh.is_elem('tex'):
        vert.add_out('vec2 texCoord')
        vert.add_uniform('float texUnpack', link='_texUnpack')
        if mat_state.material.arm_tilesheet_flag:
            if mat_state.material.arm_particle_flag and rpdat.arm_particles == 'On':
                make_particle.write_tilesheet(vert)
            else:
                vert.add_uniform('vec2 tilesheetOffset', '_tilesheetOffset')
                vert.write_attrib('texCoord = tex * texUnpack + tilesheetOffset;')
        else:
            vert.write_attrib('texCoord = tex * texUnpack;')

        if tese is not None:
            tese.write_pre = True
            make_tess.interpolate(tese, 'texCoord', 2, declare_out=frag.contains('texCoord'))
            tese.write_pre = False

    if con_mesh.is_elem('tex1'):
        vert.add_out('vec2 texCoord1')
        vert.add_uniform('float texUnpack', link='_texUnpack')
        vert.write_attrib('texCoord1 = tex1 * texUnpack;')
        if tese is not None:
            tese.write_pre = True
            make_tess.interpolate(tese, 'texCoord1', 2, declare_out=frag.contains('texCoord1'))
            tese.write_pre = False
