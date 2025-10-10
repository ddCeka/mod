
transform URM_quickmenu_hover:
    on show:
        linear .2 alpha 1.0
    on hide:
        linear .2 alpha 0.0

screen URM_quickmenu:
    layer 'Overlay'
    style_prefix 'mod'
    default hovered = False

    if mod.Settings.quickmenuEnabled:
        if mod.Settings.quickmenuAutoHide:
            mousearea:
                xalign mod.Settings.quickmenuAlignX
                yalign mod.Settings.quickmenuAlignY
                xysize mod.getScreenSize('URM_quickmenu_contentWrapper')
                hovered SetScreenVariable('hovered', True)
                unhovered SetScreenVariable('hovered', False)

        showif not mod.Settings.quickmenuAutoHide or hovered:
            use URM_quickmenu_contentWrapper

screen URM_quickmenu_contentWrapper:
    hbox:
        style_prefix 'quick'
        at URM_quickmenu_hover
        spacing mod.scalePxInt(4)
        xalign mod.Settings.quickmenuAlignX
        yalign mod.Settings.quickmenuAlignY

        if mod.Settings.quickmenuVertical:
            vbox:
                spacing mod.scalePxInt(4)
                use URM_quickmenu_content
        else:
            use URM_quickmenu_content

screen URM_quickmenu_content:
    if mod.Settings.quickmenuBtnBack:
        use URM_quickmenu_button('\ue045', '{urm_notl}Back{/urm_notl}', Rollback())
    if mod.Settings.quickmenuBtnSkip:
        use URM_quickmenu_button('\ue044', '{urm_notl}Skip{/urm_notl}', Skip(), Skip(True))
    if mod.Settings.quickmenuBtnAuto:
        use URM_quickmenu_button('\ue01f', '{urm_notl}Auto{/urm_notl}', Preference("auto-forward", "toggle"))
    if mod.Settings.quickmenuBtnQuicksave:
        use URM_quickmenu_button('\ue161', '{urm_notl}Q.Save{/urm_notl}', QuickSave())
    if mod.Settings.quickmenuBtnSave:
        use URM_quickmenu_button('\ueb60', '{urm_notl}Save{/urm_notl}', ShowMenu('save'))
    if mod.Settings.quickmenuBtnQuickload:
        use URM_quickmenu_button('\ue2c7', '{urm_notl}Q.Load{/urm_notl}', QuickLoad())
    if mod.Settings.quickmenuBtnLoad:
        use URM_quickmenu_button('\uf1c7', '{urm_notl}Load{/urm_notl}', ShowMenu('load'))
    if mod.Settings.quickmenuBtnMenu:
        use URM_quickmenu_button('\ue8b8', '{urm_notl}Prefs{/urm_notl}', ShowMenu('preferences'))
    if mod.Settings.quickmenuBtnMods:
        use URM_quickmenu_button('\ueb8b', '{urm_notl}Mods{/urm_notl}', ShowMenu('mods'))
    if mod.Settings.quickmenuBtnUrm:
        use URM_quickmenu_button('\ue3c9', '{urm_notl}URM{/urm_notl}', mod.Open())
    if mod.Settings.quickmenuBtnExit:
        use URM_quickmenu_button('\ueb4f', '{urm_notl}Exit{/urm_notl}', Quit())

screen URM_quickmenu_button(icon, txt, action, alternate=None):
    if mod.Settings.quickmenuStyle == 'buttons':
        use mod_iconButton(icon, txt, action, alternate=alternate)
    elif mod.Settings.quickmenuStyle == 'iconbuttons':
        use mod_iconButton(icon, action=action, alternate=alternate)
    elif mod.Settings.quickmenuStyle == 'icons':
        textbutton icon xalign mod.Settings.quickmenuAlignX action action alternate alternate style 'mod_icon_textbutton' text_outlines [(absolute(2), '#222', 0, 0)] text_size mod.scalePxInt(28)
    else:
        textbutton txt xalign mod.Settings.quickmenuAlignX action action alternate alternate
