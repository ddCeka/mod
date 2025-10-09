
transform mod_fadeinout:
    on show:
        alpha 0.0
        linear 0.3 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0

style mod_default is default:
    background None
    hover_background None
    selected_background None
    selected_hover_background None
    insensitive_background None

    xalign .0 yalign .0
    xpadding 0 ypadding 0
    xmargin 0 ymargin 0
    spacing 0 line_spacing 0

style mod_text is mod_default:
    font 'mods/framework/Roboto-Regular.ttf'
    color mod.Theme.text
    size mod.scalePxInt(24)
    text_align 0.0
    outlines []
    alt ''

style mod_label is mod_default
style mod_label_text is mod_text:
    bold True

style mod_icon is mod_text:
    font 'mods/framework/MaterialIconsOutlined-Regular.otf'

style mod_iconSolid is mod_icon:
    font 'mods/framework/MaterialIcons-Regular.ttf'

style mod_overlay:
    background mod.Theme.colorAlpha(mod.Theme.background, 0.4)

style mod_frame is mod_default:
    background Solid(mod.Theme.background)
    padding (mod.scalePxInt(7), mod.scalePxInt(5))

style mod_vscrollbar:
    xsize mod.scalePxInt(15)
    ysize None # Prevent fixed height
    left_bar Solid(mod.Theme.colors.scrollBg)
    right_bar Solid(mod.Theme.colors.scrollBg)
    thumb Solid(mod.Theme.colors.scrollThumb)
    hover_thumb Solid(mod.Theme.colors.scrollThumbHover)
    unscrollable 'hide'

# We cannot inherit `mod_vscrollbar`, because it will invert the scrollbar for some reason
style mod_vbar:
    xsize mod.scalePxInt(15)
    left_bar Solid(mod.Theme.colors.scrollBg)
    right_bar Solid(mod.Theme.colors.scrollBg)
    thumb Solid(mod.Theme.colors.scrollThumb)
    hover_thumb Solid(mod.Theme.colors.scrollThumbHover)
    unscrollable 'hide'
