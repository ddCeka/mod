
style mod_button is mod_default:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonBg, mod.Theme.colors.buttonBorder)
    hover_background mod.Theme.getButtonBg(mod.Theme.colors.buttonBgHover, mod.Theme.colors.buttonBorder)
    selected_idle_background mod.Theme.getButtonBg(mod.Theme.colors.buttonBgHover, mod.Theme.colors.buttonBorder)
    insensitive_background mod.Theme.getButtonBg(mod.Theme.colors.buttonBgDisabled, mod.Theme.colors.buttonBorderDisabled)
    padding (mod.scalePxInt(8), mod.scalePxInt(4))
    xminimum None yminimum mod.scalePxInt(36)
    xmaximum None ymaximum None

style mod_button_text is mod_text:
    color mod.Theme.colors.buttonText
    insensitive_color mod.Theme.colors.buttonTextDisabled
    yalign .5

style mod_buttonPrimary is mod_button:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonPrimaryBg, mod.Theme.colors.buttonPrimaryBorder)
    hover_background mod.Theme.getButtonBg(mod.Theme.colors.buttonPrimaryBgHover, mod.Theme.colors.buttonPrimaryBorder)
    selected_idle_background mod.Theme.getButtonBg(mod.Theme.colors.buttonPrimaryBgHover, mod.Theme.colors.buttonPrimaryBorder)
    insensitive_background mod.Theme.getButtonBg(mod.Theme.colors.buttonPrimaryBgDisabled, mod.Theme.colors.buttonPrimaryBorder)

style mod_buttonPrimary_text is mod_button_text:
    color mod.Theme.colors.buttonPrimaryText
    insensitive_color mod.Theme.colors.buttonPrimaryTextDisabled

style mod_buttonSecondary is mod_button:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonSecondaryBg, mod.Theme.colors.buttonSecondaryBorder)
    hover_background mod.Theme.getButtonBg(mod.Theme.colors.buttonSecondaryBgHover, mod.Theme.colors.buttonSecondaryBorder)
    selected_idle_background mod.Theme.getButtonBg(mod.Theme.colors.buttonSecondaryBgHover, mod.Theme.colors.buttonSecondaryBorder)
    insensitive_background mod.Theme.getButtonBg(mod.Theme.colors.buttonSecondaryBgDisabled, mod.Theme.colors.buttonSecondaryBorderDisabled)

style mod_buttonSecondary_text is mod_button_text:
    color mod.Theme.colors.buttonSecondaryText
    insensitive_color mod.Theme.colors.buttonSecondaryTextDisabled

style mod_buttonCancel is mod_button:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonCancelBg, mod.Theme.colors.buttonCancelBorder)
    hover_background mod.Theme.getButtonBg(mod.Theme.colors.buttonCancelBgHover, mod.Theme.colors.buttonCancelBorder)
    selected_idle_background mod.Theme.getButtonBg(mod.Theme.colors.buttonCancelBgHover, mod.Theme.colors.buttonCancelBorder)
    insensitive_background mod.Theme.getButtonBg(mod.Theme.colors.buttonCancelBgDisabled, mod.Theme.colors.buttonCancelBorderDisabled)

style mod_buttonCancel_text is mod_button_text:
    color mod.Theme.colors.buttonCancelText
    insensitive_color mod.Theme.colors.buttonCancelTextDisabled

style mod_buttonSuccess is mod_button:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonSuccessBg, mod.Theme.colors.buttonSuccessBorder)
    hover_background mod.Theme.getButtonBg(mod.Theme.colors.buttonSuccessBgHover, mod.Theme.colors.buttonSuccessBorder)
    selected_idle_background mod.Theme.getButtonBg(mod.Theme.colors.buttonSuccessBgHover, mod.Theme.colors.buttonSuccessBorder)
    insensitive_background mod.Theme.getButtonBg(mod.Theme.colors.buttonSuccessBgDisabled, mod.Theme.colors.buttonSuccessBorderDisabled)

style mod_buttonSuccess_text is mod_button_text:
    color mod.Theme.colors.buttonSuccessText
    insensitive_color mod.Theme.colors.buttonSuccessTextDisabled

style mod_icon_button is mod_button
style mod_icon_button_text is mod_button_text:
    font 'mod/framework/MaterialIconsOutlined-Regular.otf'
    hover_font 'mod/framework/MaterialIcons-Regular.ttf'

##############
# ICONBUTTON #
##############
screen mod_iconButton(icon, text=None, action=None, xsize=None, sensitive=None, alternate=None):
    style_prefix 'mod'

    button:
        xsize xsize
        sensitive sensitive
        action action
        alternate alternate
        if text: # It's a button with text?
            hbox:
                hbox xsize mod.scalePxInt(30) yalign .5: # We want this size fixed, to prevent resizing on icon change
                    text icon style_suffix 'icon_button_text'
                if text:
                    text text style_suffix 'button_text' yalign .5
        else: # Icon only button
            text icon style_suffix 'icon_button_text' yalign .5
# We have this screen because in some cases updating the `icon` won't work
screen mod_checkbox(checked, text, action=None, xsize=None, sensitive=None):
    style_prefix 'mod'

    button:
        xsize xsize
        sensitive sensitive
        action action
        hbox:
            hbox xsize mod.scalePxInt(30) yalign .5: # We want this size fixed, to prevent resizing on icon change
                if checked:
                    text '\ue834' style_suffix 'icon_button_text' 
                elif checked == False:
                    text '\ue835' style_suffix 'icon_button_text'
                else:
                    text '\ue909' style_suffix 'icon_button_text'
            text text style_suffix 'button_text' yalign .5
# We have this screen because in some cases updating the `icon` won't work
screen mod_radiobutton(checked, text, action=None, xsize=None, sensitive=None):
    style_prefix 'mod'

    button:
        xsize xsize
        sensitive sensitive
        action action
        hbox:
            hbox xsize mod.scalePxInt(30) yalign .5: # We want this size fixed, to prevent resizing on icon change
                if checked:
                    text '\ue837' style_suffix 'icon_button_text' 
                else:
                    text '\ue836' style_suffix 'icon_button_text'
            text text style_suffix 'button_text' yalign .5