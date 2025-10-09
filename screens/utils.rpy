
screen URM_colorpicker(callback, onClose, defaultColor=None):
    layer 'Overlay'
    style_prefix "mod"
    modal True

    default colorPicker = mod.ColorPicker(defaultColor)
    default colorPresets = [(0, 0, 0), (12, 19, 79), (29, 38, 125), (92, 70, 156), (212, 173, 252), (255, 255, 255)]

    use mod_Dialog(title='{urm_notl}Colorpicker{/urm_notl}', closeAction=onClose, icon='\ue40a'):
        label '{urm_notl}Current:{/urm_notl}'
        frame xsize mod.scalePxInt(230) ysize 30:
            background Solid(colorPicker.hex)
            text ''

        null height mod.scalePxInt(5)
        # Color presents
        hbox:
            spacing 3
            for preset in colorPresets:
                imagebutton:
                    idle Solid(Color((preset[0], preset[1], preset[2], 175)))
                    hover Solid(Color(preset))
                    xsize 20 ysize 20
                    action SetField(colorPicker, 'rgba', preset)

        null height mod.scalePxInt(10)

        hbox ysize mod.scalePxInt(250) xsize mod.scalePxInt(230):
            vbox:
                text "{urm_notl}R{/urm_notl}" xalign .5 color '#ffadad' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'r', 255, step=1)
            vbox:
                text "{urm_notl}G{/urm_notl}" xalign .5 color '#adffad' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'g', 255, step=1)
            vbox:
                text "{urm_notl}B{/urm_notl}" xalign .5 color '#3572ff' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'b', 255, step=1)
            vbox:
                text "{urm_notl}A{/urm_notl}" xalign .5 size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'a', 1.0, step=.1)
        hbox yoffset 10:
            textbutton '{urm_notl}Apply{/urm_notl}' action [Function(callback, colorPicker.hex), onClose]
            textbutton '{urm_notl}Cancel{/urm_notl}' action onClose

screen URM_table(spacing=2):
    vbox:
        spacing spacing
        transclude

style mod_tableRow is mod_default
style mod_tableRow_odd is mod_tableRow:
    background Solid(
        mod.Theme.colorAlpha(
            If(mod.Theme.isLightColor(mod.Theme.background),
                mod.Theme.backgroundDarker,
                mod.Theme.backgroundLighter,
            ),
            .5)
        )

screen URM_tableRow(rowIndex=0, fill=False):
    frame:
        style If(rowIndex % 2 == 0,'mod_tableRow','mod_tableRow_odd')
        xfill fill
        hbox:
            yminimum mod.scalePxInt(36)+mod.scalePxInt(4) # Button height + padding
            spacing 4
            transclude
