
style mod_dialog is mod_frame:
    background mod.generateDialogBackground()
    padding (2, 2)

style mod_dialogContent is mod_frame:
    background None
    yoffset mod.scalePxInt(-20)
    padding (mod.scalePxInt(20), 0, mod.scalePxInt(20), mod.scalePxInt(10))

style mod_dialogButtons:
    yoffset mod.scalePxInt(-40)
    xalign 0.0

style mod_dialogButton is mod_button:
    background Solid(mod.Theme.colors.buttonBg)
    hover_background Solid(mod.Theme.colors.buttonBgHover)
    ysize mod.scalePxInt(38)
    padding (mod.scalePxInt(16),0)

style mod_dialogCloseButton is mod_dialogButton:
    background Solid(mod.Theme.colors.errorText)
    hover_background Solid(mod.Theme.colorBrightness(mod.Theme.colors.errorText, 30))

style mod_dialogIcon is mod_iconSolid:
    size mod.scalePxInt(28)

# ======
# DIALOG
# ======
screen mod_Dialog(title=None, closeAction=None, xsize=None, modal=False, icon=None, backgroundColor=None, details=None, detailsTitle=None):
    style_prefix 'mod'
    default dialogBackground = backgroundColor and mod.generateDialogBackground(backgroundColor)

    if closeAction:
        key 'K_ESCAPE' action closeAction

    if modal:
        textbutton "" style_suffix "overlay" xfill True yfill True action NullAction() at mod_fadeinout

    drag:
        draggable True
        drag_handle (0, 0, 1.0, mod.scalePxInt(42))
        if renpy.variant('touch'):
            align (.5,.6)
        else:
            align (.5,.6)

        frame:
            style_suffix 'dialog'
            if dialogBackground:
                background dialogBackground
            vbox: # Do not use `has vbox` here, for older Ren'Py versions
                frame:
                    background None
                    ysize mod.scalePxInt(40)
                    padding (mod.scalePxInt(4), 0)
                    hbox spacing mod.scalePxInt(4) yalign .5:
                        if icon:
                            text icon style_suffix 'mod_dialogIcon' yalign .5
                        if title:
                            label title yalign .5

                hbox:
                    style_suffix 'dialogButtons'
                    
                    button:
                        style_suffix 'dialogCloseButton'
                        if closeAction:
                            text 'x' size mod.scalePxInt(24) yalign .5 color mod.Theme.colors.errorBg
                            action closeAction
                        else:
                            background None
                            text 'x' size mod.scalePxInt(24) yalign .5 color '#fff0'
                    if details:
                        button:
                            style_suffix 'dialogButton'
                            text '?' size mod.scalePxInt(24) yalign .5
                            action mod.Confirm(details, title=detailsTitle)

                button:
                    key_events True # We need this to still trigger key events defined inside of this button
                    action NullAction() # Prevent clicking through
                    style_suffix 'dialogContent'
                    has vbox
                    transclude

# ==============
# CONFIRM SCREEN
# ==============
screen mod_Confirm(prompt, yes=None, no=None, title=None, modal=True, promptSubstitution=True):
    layer 'Overlay'
    style_prefix 'mod'

    use mod_Dialog(title, closeAction=no, modal=modal):
        if promptSubstitution:
            text '[prompt]' xalign .5 text_align .5
        else:
            text '[prompt!q]' xalign .5 text_align .5

        hbox:
            yoffset mod.scalePxInt(15)
            xalign 0.5
            if yes:
                key 'K_KP_ENTER' action [Function(yes),Hide('mod_Confirm')]
                key 'K_RETURN' action [Function(yes),Hide('mod_Confirm')]
                textbutton "Yes" style_suffix "buttonPrimary" action [Function(yes),Hide('mod_Confirm')]
                null width mod.scalePxInt(20) # We don't use spacing on the hbox, because this will also space between `key` statements
                if no:
                    key 'K_ESCAPE' action [Function(no),Hide('mod_Confirm')]
                    textbutton "No" action [Function(no),Hide('mod_Confirm')]
                else:
                    key 'K_ESCAPE' action Hide('mod_Confirm')
                    textbutton "No" action Hide('mod_Confirm')
            else:
                key 'K_KP_ENTER' action Hide('mod_Confirm')
                key 'K_RETURN' action Hide('mod_Confirm')
                key 'K_ESCAPE' action Hide('mod_Confirm')
                textbutton "OK" style_suffix "buttonPrimary" action Hide('mod_Confirm')
