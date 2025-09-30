
screen mod_colorpicker(callback, onClose, defaultColor=None):
    layer 'mod_Overlay'
    style_prefix "mod"
    modal True

    default colorPicker = mod.ColorPicker(defaultColor)
    default colorPresets = [(0, 0, 0), (12, 19, 79), (29, 38, 125), (92, 70, 156), (212, 173, 252), (255, 255, 255)]

    use mod_Dialog(title='{mod_notl}Colorpicker{/mod_notl}', closeAction=onClose, icon='\ue40a'):
        label '{mod_notl}Current:{/mod_notl}'
        frame xsize mod.scalePxInt(230) ysize 30:
            background Solid(colorPicker.hex)
            text ''

        null height mod.scalePxInt(5)

        hbox: # Color presents
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
                text "{mod_notl}R{/mod_notl}" xalign .5 color '#ffadad' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'r', 255, step=1)
            vbox:
                text "{mod_notl}G{/mod_notl}" xalign .5 color '#adffad' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'g', 255, step=1)
            vbox:
                text "{mod_notl}B{/mod_notl}" xalign .5 color '#3572ff' size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'b', 255, step=1)
            vbox:
                text "{mod_notl}A{/mod_notl}" xalign .5 size 34 outlines [(2, '#222', 0, 0)]
                vbar xoffset 4:
                    value FieldValue(colorPicker, 'a', 1.0, step=.1)

        hbox yoffset 10:
            textbutton '{mod_notl}Apply{/mod_notl}' action [Function(callback, colorPicker.hex), onClose]
            textbutton '{mod_notl}Cancel{/mod_notl}' action onClose

screen mod_table(spacing=2):
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

screen mod_tableRow(rowIndex=0, fill=False):
    frame:
        style If(rowIndex % 2 == 0,'mod_tableRow','mod_tableRow_odd')
        xfill fill
        hbox:
            yminimum mod.scalePxInt(36)+mod.scalePxInt(4) # Button height + padding
            spacing 4
            transclude
