
style mod_progressBar_back:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonBg, mod.Theme.colors.buttonBorder)
    padding (2, 2)

style mod_progressBar_back_translucent is mod_progressBar_back:
    background Transform(mod.Theme.getButtonBg(mod.Theme.colors.buttonBg, mod.Theme.colors.buttonBorder), alpha=.3)

style mod_progressBar_fore:
    background mod.Theme.secondary
    yfill True

style mod_progressBar_fore_translucent is mod_progressBar_fore:
    background Transform(mod.Theme.secondary, alpha=.3)

screen mod_progress():
    default hovered = False

    drag:
        draggable True
        if mod.Settings.progressPosition:
            pos mod.Settings.progressPosition
        else:
            align (.5,.5)
        dragged mod.progressDragged
        hovered SetLocalVariable('hovered', True)
        unhovered SetLocalVariable('hovered', False)

        use mod_progressBar(translucent=not hovered)

screen mod_progressBar(translucent=False):
    style_prefix 'mod'

    python:
        barWidth = mod.min(mod.max(250, mod.ProgressBar.textWidth), mod.scaleX(75))+mod.scalePxInt(18)

    frame:
        style_suffix If(translucent, 'progressBar_back_translucent', 'progressBar_back')
        xysize (int(barWidth)+4, mod.scalePxInt(40))
        frame style_suffix If(translucent, 'progressBar_fore_translucent', 'progressBar_fore') xsize int(barWidth*(mod.ProgressBar.percentage/100))
        text mod.ProgressBar.text yalign .5 xalign .5
