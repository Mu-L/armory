from arm.logicnode.arm_nodes import *

class ColorgradingGetHighlightNode(ArmLogicTreeNode):
    """TO DO."""
    bl_idname = 'LNColorgradingGetHighlightNode'
    bl_label = 'Colorgrading Get Highlight'
    arm_section = 'colorgrading'
    arm_version = 1

    def init(self, context):
        super(ColorgradingGetHighlightNode, self).init(context)
        self.add_output('NodeSocketFloat', 'HightlightMin')
        self.add_output('NodeSocketVector', 'Saturation')
        self.add_output('NodeSocketVector', 'Contrast')
        self.add_output('NodeSocketVector', 'Gamma')
        self.add_output('NodeSocketVector', 'Gain')
        self.add_output('NodeSocketVector', 'Offset')
