
transform mod_quickmenu_hover:
    on show:
        linear .2 alpha 1.0
    on hide:
        linear .2 alpha 0.0

screen mod_quickmenu:
    layer 'mod_Overlay'
    style_prefix 'mod'
    default hovered = False

    if mod.Settings.quickmenuEnabled:
        if mod.Settings.quickmenuAutoHide:
            mousearea:
                xalign mod.Settings.quickmenuAlignX
                yalign mod.Settings.quickmenuAlignY
                xysize mod.getScreenSize('mod_quickmenu_contentWrapper')
                hovered SetScreenVariable('hovered', True)
                unhovered SetScreenVariable('hovered', False)

        showif not mod.Settings.quickmenuAutoHide or hovered:
            use mod_quickmenu_contentWrapper

screen mod_quickmenu_contentWrapper:
    hbox:
        style_prefix 'quick'
        at mod_quickmenu_hover
        spacing mod.scalePxInt(4)
        xalign mod.Settings.quickmenuAlignX
        yalign mod.Settings.quickmenuAlignY

        if mod.Settings.quickmenuVertical:
            vbox:
                spacing mod.scalePxInt(4)
                use mod_quickmenu_content
        else:
            use mod_quickmenu_content

screen mod_quickmenu_content:
    if mod.Settings.quickmenuBtnBack:
        use mod_quickmenu_button('\ue045', '{mod_notl}Back{/mod_notl}', Rollback())
    if mod.Settings.quickmenuBtnSkip:
        use mod_quickmenu_button('\ue044', '{mod_notl}Skip{/mod_notl}', Skip(), Skip(True))
    if mod.Settings.quickmenuBtnAuto:
        use mod_quickmenu_button('\ue01f', '{mod_notl}Auto{/mod_notl}', Preference("auto-forward", "toggle"))
    if mod.Settings.quickmenuBtnQuicksave:
        use mod_quickmenu_button('\ue161', '{mod_notl}Q.Save{/mod_notl}', QuickSave())
    if mod.Settings.quickmenuBtnSave:
        use mod_quickmenu_button('\ueb60', '{mod_notl}Save{/mod_notl}', ShowMenu('save'))
    if mod.Settings.quickmenuBtnQuickload:
        use mod_quickmenu_button('\ue2c7', '{mod_notl}Q.Load{/mod_notl}', QuickLoad())
    if mod.Settings.quickmenuBtnLoad:
        use mod_quickmenu_button('\uf1c7', '{mod_notl}Load{/mod_notl}', ShowMenu('load'))
    if mod.Settings.quickmenuBtnMenu:
        use mod_quickmenu_button('\ue8b8', '{mod_notl}Prefs{/mod_notl}', ShowMenu('preferences'))
    if mod.Settings.quickmenuBtnAddon:
        use mod_quickmenu_button('\ueb8b', '{mod_notl}Addon{/mod_notl}', ShowMenu('addon'))
    if mod.Settings.quickmenuBtnMod:
        use mod_quickmenu_button('\ue3c9', '{mod_notl}Mod{/mod_notl}', mod.Open())
    if mod.Settings.quickmenuBtnExit:
        use mod_quickmenu_button('\ueb4f', '{mod_notl}Exit{/mod_notl}', Quit())

screen mod_quickmenu_button(icon, txt, action, alternate=None):
    if mod.Settings.quickmenuStyle == 'buttons':
        use mod_iconButton(icon, txt, action, alternate=alternate)
    elif mod.Settings.quickmenuStyle == 'iconbuttons':
        use mod_iconButton(icon, action=action, alternate=alternate)
    elif mod.Settings.quickmenuStyle == 'icons':
        textbutton icon xalign mod.Settings.quickmenuAlignX action action alternate alternate style 'mod_icon_textbutton' text_outlines [(absolute(2), '#222', 0, 0)] text_size mod.scalePxInt(28)
    else:
        textbutton txt xalign mod.Settings.quickmenuAlignX action action alternate alternate
