
style mod_separator is mod_default:
    background mod.Theme.primary
    ysize 2
style mod_vseparator is mod_default:
    background mod.Theme.primary
    xsize 2

style mod_text_small is mod_text:
    size mod.scalePxInt(20)
style mod_description is mod_text_small:
    color mod.Theme.textTranslucent140

style mod_icon_textbutton is mod_icon_button:
    background None
    hover_background None
    selected_idle_background None
    insensitive_background None
    padding (0,0)
style mod_icon_textbutton_text is mod_icon_button_text

style mod_header_text is mod_label_text:
    color mod.Theme.secondary
    outlines [(absolute(1), mod.Theme.secondaryDarker, absolute(1), absolute(1)),(absolute(1), mod.Theme.secondaryLighter, absolute(-1), absolute(-1))]
    size mod.scalePxInt(28)

style mod_thumbnailButton is mod_button:
    padding (2, 2)

style mod_hbox is mod_default
style mod_vbox is mod_default  
style mod_vpgrid is mod_default

style mod_input is mod_button_text
