
style modSay_text is mod_text:
    alt None
style modSay_frame is mod_default

style mod_textboxConfigBox:
    background mod.Theme.getButtonBg(mod.Theme.colors.buttonBgDisabled, mod.Theme.colors.buttonPrimaryBgDisabled)
    padding (8, 8)

transform mod_textboxSettingFade:
    on show:
        alpha 0.0
        linear 0.2 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.2 alpha 0.0

screen mod_say(who, what):
    style_prefix 'modSay'

    vbox:
        xfill True
        yalign 1.0

        if who and mod.TextBox.Settings.whoShown:
            frame:
                if mod.TextBox.Settings.whoResizeBackground:
                    xsize mod.TextBox.whoWidth
                    xalign mod.TextBox.Settings.whoPosition
                else:
                    xfill True
                xpadding mod.TextBox.whoXPadding
                background mod.TextBox.whoBackground
                hbox xsize mod.TextBox.whoWidth xalign mod.TextBox.Settings.whoPosition:
                    text who id 'who'

        frame:
            if mod.TextBox.Settings.whatResizeBackground:
                xsize mod.TextBox.textWidth
                xalign mod.TextBox.Settings.whatPosition
            else:
                xfill True
            background mod.TextBox.whatBackground

            hbox xsize mod.TextBox.textWidth xalign mod.TextBox.Settings.whatPosition:
                spacing 20
                yminimum mod.TextBox.textHeight

                if mod.TextBox.Settings.sideImageShown and mod.TextBox.Settings.sideImagePos == 'left':
                    add mod.TextBox.sideImage

                frame:
                    xsize If(mod.TextBox.Settings.sideImageShown, mod.TextBox.textWidth-mod.TextBox.textHeight, mod.TextBox.textWidth)-(mod.TextBox.Settings.whatXPadding*2)
                    xpadding mod.TextBox.whatXPadding
                    text what id 'what'

                if mod.TextBox.Settings.sideImageShown and mod.TextBox.Settings.sideImagePos == 'right':
                    add mod.TextBox.sideImage


screen mod_textboxCustomizations():
    style_prefix "mod"
    default colWidth = [mod.scaleX(20), mod.scaleX(60)]
    default textboxPages = mod.Pages(len(mod.TextBox.Settings.store), itemsPerPage=20)

    hbox:
        spacing mod.scalePxInt(5)
        use mod_iconButton('\ue266', '{mod_notl}Add{/mod_notl}', action=Function(mod.TextBox.openCustomizer, beforeOpenAction=Hide('mod_main'), afterCloseAction=mod.Open()))
        use mod_checkbox(checked=mod.TextBox.enabled, text='{mod_notl}Enabled{/mod_notl}', action=ToggleField(mod.TextBox, 'enabled', True, False))
        if not mod.TextBox.enabled:
            text 'Custom textboxes are currently disabled, settings will not have any effect' yalign .5
    null height mod.scalePxInt(10)
    frame style_suffix "separator" ysize mod.scalePxInt(2)

    if len(mod.TextBox.Settings.store) > 0:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use mod_pages(textboxPages)
            hbox xalign 1.0 yalign .5:
                text 'Customizations: {}'.format(len(mod.TextBox.Settings.store))
                null width mod.scalePxInt(10)

        use mod_tableRow(): # Headers
            label "{mod_notl}Character{/mod_notl}" xsize colWidth[0]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use mod_table():
                for i,charVarName in enumerate(list(mod.TextBox.Settings.store.keys())[textboxPages.pageStartIndex:textboxPages.pageEndIndex]):
                    use mod_tableRow(i, True):
                        hbox xsize colWidth[0] yalign .5:
                            if charVarName == 'None':
                                text '{mod_notl}Any{/mod_notl}'
                            elif mod.Characters.getByVarName(charVarName):
                                text mod.scaleText(mod.Characters.getByVarName(charVarName).fullName, 18)
                            else:
                                text mod.scaleText(charVarName, 18)

                        hbox xsize colWidth[1]:
                            hbox spacing 2:
                                use mod_iconButton('\ue3c9', '{mod_notl}Edit{/mod_notl}', action=Function(mod.TextBox.openCustomizer, charVarName=charVarName, beforeOpenAction=Hide('mod_main'), afterCloseAction=mod.Open()))
                                use mod_iconButton('\ue872', '{mod_notl}Remove{/mod_notl}', mod.Confirm('Are you sure you want to remove this customization?', Function(mod.TextBox.Settings.remove, charVarName), title='Remove textbox customization'))
    
    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "{mod_notl}There are no customizations yet{/mod_notl}" xalign 0.5
            null height mod.scalePxInt(15)
            text "Here you can customize the textbox for each or all characters" xalign .5
            text "Use the add button a the left top to start customizing" xalign .5


screen mod_textboxCustomizer(charVarName=None):
    layer 'mod_Overlay'
    style_prefix "mod"
    modal True

    on 'show' action Function(mod.TextBox.Settings.enableTemp, charVarName=charVarName)

    use mod_Dialog(title='{mod_notl}Textbox customizer{/mod_notl}', closeAction=Function(mod.TextBox.closeCustomizer), icon='\ue0b7'):
        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"
            
            vbox spacing mod.scalePxInt(10):
                hbox spacing mod.scalePxInt(10):
                    # Character picker
                    vbox:
                        hbox:
                            text '\ue87c' style_suffix 'icon'
                            label '{mod_notl}Character{/mod_notl}'
                        hbox spacing 2:
                            if mod.TextBox.previewCharacter == mod.TextBox.demoCharacter:
                                text '{mod_notl}Any{/mod_notl}' yalign .5
                            elif mod.Characters.getByVarName(mod.TextBox.previewCharacterVarName):
                                text '{} ({})'.format(mod.Characters.getByVarName(mod.TextBox.previewCharacterVarName).displayName, mod.Characters.getByVarName(mod.TextBox.previewCharacterVarName).varName) substitute False yalign .5
                            else:
                                text str(mod.TextBox.previewCharacterVarName) yalign .5
                            textbutton '\ue3c9' style_suffix 'icon_button' action Show('mod_textboxCharacterPicker')
                            textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox, 'previewCharacter', None) sensitive (mod.TextBox.previewCharacter != mod.TextBox.demoCharacter)
                            textbutton '\ueb8b' style_suffix 'icon_button' action mod.Confirm('Select a character to apply the customization to.\n"Any" is applied to any character that doensn\'t have it\'s own customizations.', title='{mod_notl}Character selection{/mod_notl}')

                    vbox:
                        label 'Mode'
                        hbox:
                            textbutton If(mod.TextBox.Settings.customSayScreen, '{mod_notl}Full{/mod_notl}', '{mod_notl}Light{/mod_notl}') action ToggleField(mod.TextBox.Settings, 'customSayScreen', True, False)
                            textbutton '\ueb8b' style_suffix 'icon_button' action mod.Confirm('{b}Full{/b} = Use a fully customizable textbox\n{b}Light{/b} = Use the original textbox (some customization may not work)', title='{mod_notl}Textbox mode{/mod_notl}') yalign .5

                # Namebox settings
                vbox:
                    hbox:
                        text '\ue0b7' style_suffix 'icon'
                        label '{mod_notl}Namebox{/mod_notl}'
                        if mod.TextBox.Settings.customSayScreen:
                            use mod_checkbox(checked=mod.TextBox.Settings.whoShown, text='{mod_notl}Enabled{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoShown', True, False))
                        
                    showif not mod.TextBox.Settings.customSayScreen or mod.TextBox.Settings.whoShown:
                        hbox spacing mod.scalePxInt(15) at mod_textboxSettingFade:
                            vbox:
                                text '{mod_notl}Text{/mod_notl}'
                                frame style_suffix 'textboxConfigBox':
                                    has vbox
                                    hbox spacing mod.scalePxInt(10):
                                        vbox spacing 2:
                                            hbox: # Bold
                                                use mod_checkbox(checked=mod.TextBox.Settings.whoBold, text='{mod_notl}Bold{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoBold', True, False))
                                                textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoBold', None) sensitive isinstance(mod.TextBox.Settings.whoBold, bool) yalign .5
                                            hbox: # Italic
                                                use mod_checkbox(checked=mod.TextBox.Settings.whoItalic, text='{mod_notl}Italic{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoItalic', True, False))
                                                textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoItalic', None) sensitive isinstance(mod.TextBox.Settings.whoItalic, bool) yalign .5
                                            hbox: # Color
                                                use mod_iconButton('\ue40a', '{mod_notl}Color{/mod_notl}', Show('mod_colorpicker', callback=mod.TextBoxSettingCallback('whoColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whoColor))
                                                if mod.TextBox.Settings.whoColor:
                                                    frame yalign .5:
                                                        background mod.TextBox.Settings.whoColor
                                                        text ''
                                                textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoColor', None) sensitive bool(mod.TextBox.Settings.whoColor) yalign .5
                                        vbox spacing 2:
                                            if mod.TextBox.Settings.customSayScreen:
                                                text '{size=-4}{mod_notl}Alignment{/mod_notl}{/size}'
                                                hbox: # Alignment
                                                    textbutton '\ue236' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoXAlign', 0.0)
                                                    textbutton '\ue234' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoXAlign', 0.5)
                                                    textbutton '\ue237' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoXAlign', 1.0)
                                            text '{size=-4}{mod_notl}Size{/mod_notl}{/size}'
                                            hbox: # Size
                                                textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoSize', mod.max(mod.TextBox.Settings.whoSize-2, 12))
                                                text '[mod.TextBox.Settings.whoSize]' yalign .5
                                                textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoSize', mod.min(mod.TextBox.Settings.whoSize+2, 100))
                                                textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoSize', mod.TextBoxSettings.defaultValues['whoSize'])
                                    hbox spacing mod.scalePxInt(5): # Change font
                                        use mod_iconButton('\ue165', '{mod_notl}Font{/mod_notl}', action=Show('mod_textboxFontPicker', settingName='whoFont', defaultSelected=mod.TextBox.Settings.whoFont))
                                        if not mod.TextBox.Settings.customSayScreen:
                                            textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoFont', None) sensitive (mod.TextBox.Settings.whoFont != None) yalign .5
                                        if mod.TextBox.Settings.customSayScreen or mod.TextBox.Settings.whoFont != None:
                                            text (mod.TextBox.Settings.whoFont or list(mod.TextBoxSettings.fontOptions.keys())[0]) font mod.TextBox.whoFont yalign .5

                            vbox:
                                text '{mod_notl}Border{/mod_notl}'
                                frame style_suffix 'textboxConfigBox':
                                    has vbox
                                    spacing 2
                                    use mod_checkbox(checked=mod.TextBox.Settings.whoOutlinesEnabled, text='{mod_notl}Enabled{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoOutlinesEnabled', True, False))
                                    hbox: # Color
                                        use mod_iconButton('\ue40a', '{mod_notl}Color{/mod_notl}', Show('mod_colorpicker', callback=mod.TextBoxSettingCallback('whoOutlinesColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whoOutlinesColor))
                                        if mod.TextBox.Settings.whoOutlinesColor:
                                            frame yalign .5:
                                                background mod.TextBox.Settings.whoOutlinesColor
                                                text ''
                                    text '{size=-4}{mod_notl}Size{/mod_notl}{/size}'
                                    hbox: # Size
                                        textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoOutlinesWidth', mod.max(mod.TextBox.Settings.whoOutlinesWidth-1, 1))
                                        text '[mod.TextBox.Settings.whoOutlinesWidth]' yalign .5
                                        textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoOutlinesWidth', mod.min(mod.TextBox.Settings.whoOutlinesWidth+1, 10))
                                        textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoOutlinesWidth', mod.TextBoxSettings.defaultValues['whoOutlinesWidth'])

                            showif mod.TextBox.Settings.customSayScreen:
                                vbox at mod_textboxSettingFade:
                                    text '{mod_notl}Background{/mod_notl}'
                                    frame style_suffix 'textboxConfigBox':
                                        has vbox
                                        spacing 2
                                        use mod_checkbox(checked=mod.TextBox.Settings.whoBackgroundEnabled, text='{mod_notl}Enabled{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoBackgroundEnabled', True, False))
                                        hbox: # Color
                                            use mod_iconButton('\ue40a', '{mod_notl}Color{/mod_notl}', Show('mod_colorpicker', callback=mod.TextBoxSettingCallback('whoBackground'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whoBackground))
                                            frame yalign .5:
                                                background mod.TextBox.Settings.whoBackground
                                                text ''
                                        use mod_checkbox(checked=mod.TextBox.Settings.whoBackgroundGradient, text='{mod_notl}Gradient{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoBackgroundGradient', True, False))
                                        hbox: # Character color
                                            use mod_checkbox(checked=mod.TextBox.Settings.whoBackgroundCharacterColor, text='{mod_notl}Character color{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoBackgroundCharacterColor', True, False))
                                            textbutton '\ueb8b' style_suffix 'icon_button' action mod.Confirm('Use the character\'s name color (when available)\n{size=-5}{alpha=.9}Note: This still uses the transparency/alpha from the color you\'ve set{/alpha}{/size}', title='Character color') yalign .5

                            showif mod.TextBox.Settings.customSayScreen:
                                vbox at mod_textboxSettingFade:
                                    text '{mod_notl}Size/position{/mod_notl}'
                                    frame style_suffix 'textboxConfigBox':
                                        has vbox
                                        spacing 2
                                        vbox:
                                            text '{size=-4}{mod_notl}Height{/mod_notl}{/size}'
                                            hbox: # Height
                                                textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoHeight', mod.max(mod.TextBox.Settings.whoHeight-10, 50))
                                                text '[mod.TextBox.Settings.whoHeight]' yalign .5
                                                textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoHeight', mod.min(mod.TextBox.Settings.whoHeight+10, 450))
                                                textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoHeight', mod.TextBoxSettings.defaultValues['whoHeight'])
                                        vbox:
                                            text '{size=-4}{mod_notl}Width{/mod_notl}{/size}'
                                            hbox: # Width
                                                textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoWidth', mod.max(mod.TextBox.Settings.whoWidth-5, 40))
                                                text '[mod.TextBox.Settings.whoWidth]%' yalign .5
                                                textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoWidth', mod.min(mod.TextBox.Settings.whoWidth+5, 100))
                                                textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoWidth', mod.TextBoxSettings.defaultValues['whoWidth'])
                                        vbox:
                                            text '{size=-4}{mod_notl}Position{/mod_notl}{/size}'
                                            hbox: # Position
                                                textbutton '\ue5c4' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoPosition', mod.max(mod.TextBox.Settings.whoPosition-0.05, 0.0))
                                                text '{}%'.format(int(mod.TextBox.Settings.whoPosition*100)) yalign .5
                                                textbutton '\ue5c8' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoPosition', mod.min(mod.TextBox.Settings.whoPosition+0.05, 1.0))
                                                textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whoPosition', mod.TextBoxSettings.defaultValues['whoPosition'])
                                        use mod_checkbox(checked=mod.TextBox.Settings.whoResizeBackground, text='{mod_notl}Resize background{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whoResizeBackground', True, False))

                # Textbox settings
                vbox:
                    hbox:
                        text '\uf086' style_suffix 'icon'
                        label 'Text'

                    hbox spacing mod.scalePxInt(15):
                        vbox:
                            text '{mod_notl}Text{/mod_notl}'
                            frame style_suffix 'textboxConfigBox':
                                has vbox
                                spacing 2
                                hbox spacing mod.scalePxInt(10):
                                    vbox spacing 2:
                                        hbox: # Bold
                                            use mod_checkbox(checked=mod.TextBox.Settings.whatBold, text='{mod_notl}Bold{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatBold', True, False))
                                            textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatBold', None) sensitive isinstance(mod.TextBox.Settings.whatBold, bool) yalign .5
                                        hbox: # Italic
                                            use mod_checkbox(checked=mod.TextBox.Settings.whatItalic, text='{mod_notl}Italic{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatItalic', True, False))
                                            textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatItalic', None) sensitive isinstance(mod.TextBox.Settings.whatItalic, bool) yalign .5
                                        hbox: # Color
                                            use mod_iconButton('\ue40a', '{mod_notl}Color{/mod_notl}', Show('mod_colorpicker', callback=mod.TextBoxSettingCallback('whatColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whatColor))
                                            if mod.TextBox.Settings.whatColor:
                                                frame yalign .5:
                                                    background mod.TextBox.Settings.whatColor
                                                    text ''
                                            textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatColor', None) sensitive bool(mod.TextBox.Settings.whatColor) yalign .5
                                    vbox spacing 2:
                                        if mod.TextBox.Settings.customSayScreen:
                                            text '{size=-4}{mod_notl}Alignment{/mod_notl}{/size}'
                                            hbox: # Alignment
                                                textbutton '\ue236' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatAlign', 0.0)
                                                textbutton '\ue234' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatAlign', 0.5)
                                                textbutton '\ue237' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatAlign', 1.0)
                                        text '{size=-4}{mod_notl}Size{/mod_notl}{/size}'
                                        hbox: # Size
                                            textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatSize', mod.max(mod.TextBox.Settings.whatSize-2, 12))
                                            text '[mod.TextBox.Settings.whatSize]' yalign .5
                                            textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatSize', mod.min(mod.TextBox.Settings.whatSize+2, 100))
                                            textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatSize', mod.TextBoxSettings.defaultValues['whatSize'])
                                hbox: # Character color
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatColorFromCharacter, text='{mod_notl}Character color{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatColorFromCharacter', True, False))
                                    textbutton '\ueb8b' style_suffix 'icon_button' action mod.Confirm('Use the character\'s name color (when available)\n{size=-5}{alpha=.9}Note: This still uses the transparency/alpha from the color you\'ve set{/alpha}{/size}', title='Character color') yalign .5
                                hbox spacing mod.scalePxInt(5): # Change font
                                    use mod_iconButton('\ue165', '{mod_notl}Font{/mod_notl}', action=Show('mod_textboxFontPicker', settingName='whatFont', defaultSelected=mod.TextBox.Settings.whatFont))
                                    if not mod.TextBox.Settings.customSayScreen:
                                        textbutton '\ue872' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatFont', None) sensitive (mod.TextBox.Settings.whatFont != None) yalign .5
                                    if mod.TextBox.Settings.customSayScreen or mod.TextBox.Settings.whatFont != None:
                                        text (mod.TextBox.Settings.whatFont or list(mod.TextBoxSettings.fontOptions.keys())[0]) font mod.TextBox.whatFont yalign .5
                        
                        vbox:
                            text '{mod_notl}Border{/mod_notl}'
                            frame style_suffix 'textboxConfigBox':
                                has vbox
                                spacing 2
                                use mod_checkbox(checked=mod.TextBox.Settings.whatOutlinesEnabled, text='{mod_notl}Enabled{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatOutlinesEnabled', True, False))
                                hbox: # Color
                                    use mod_iconButton('\ue40a', '{mod_notl}Color{/mod_notl}', Show('mod_colorpicker', callback=mod.TextBoxSettingCallback('whatOutlinesColor'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whatOutlinesColor))
                                    if mod.TextBox.Settings.whatOutlinesColor:
                                        frame yalign .5:
                                            background mod.TextBox.Settings.whatOutlinesColor
                                            text ''
                                text '{size=-4}{mod_notl}Size{/mod_notl}{/size}'
                                hbox: # Size
                                    textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatOutlinesWidth', mod.max(mod.TextBox.Settings.whatOutlinesWidth-1, 1))
                                    text '[mod.TextBox.Settings.whatOutlinesWidth]' yalign .5
                                    textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatOutlinesWidth', mod.min(mod.TextBox.Settings.whatOutlinesWidth+1, 10))
                                    textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatOutlinesWidth', mod.TextBoxSettings.defaultValues['whatOutlinesWidth'])
                        
                        showif mod.TextBox.Settings.customSayScreen:
                            vbox at mod_textboxSettingFade:
                                text '{mod_notl}Background{/mod_notl}'
                                frame style_suffix 'textboxConfigBox':
                                    has vbox
                                    spacing 2
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatBackgroundEnabled, text='{mod_notl}Enabled{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatBackgroundEnabled', True, False))
                                    hbox: # Color
                                        use mod_iconButton('\ue40a', '{mod_notl}Color{/mod_notl}', Show('mod_colorpicker', callback=mod.TextBoxSettingCallback('whatBackground'), onClose=Hide('mod_colorpicker'), defaultColor=mod.TextBox.Settings.whatBackground))
                                        frame yalign .5:
                                            background Solid(mod.TextBox.Settings.whatBackground)
                                            text ''
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatBackgroundGradient, text='{mod_notl}Gradient{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatBackgroundGradient', True, False))
                                    hbox: # Character color
                                        use mod_checkbox(checked=mod.TextBox.Settings.whatBackgroundCharacterColor, text='{mod_notl}Character color{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatBackgroundCharacterColor', True, False))
                                        textbutton '\ueb8b' style_suffix 'icon_button' action mod.Confirm('Use the character\'s name color (when available)\n{size=-5}{alpha=.9}Note: This still uses the transparency/alpha from the color you\'ve set{/alpha}{/size}', title='Character color') yalign .5

                        showif mod.TextBox.Settings.customSayScreen:
                            vbox at mod_textboxSettingFade:
                                text '{mod_notl}Size/position{/mod_notl}'
                                frame style_suffix 'textboxConfigBox':
                                    has vbox
                                    spacing 2
                                    vbox:
                                        text '{size=-4}{mod_notl}Height{/mod_notl}{/size}'
                                        hbox: # Height
                                            textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatHeight', mod.max(mod.TextBox.Settings.whatHeight-10, 50))
                                            text '[mod.TextBox.Settings.whatHeight]' yalign .5
                                            textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatHeight', mod.min(mod.TextBox.Settings.whatHeight+10, 450))
                                            textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatHeight', mod.TextBoxSettings.defaultValues['whatHeight'])
                                    vbox:
                                        text '{size=-4}{mod_notl}Width{/mod_notl}{/size}'
                                        hbox: # Width
                                            textbutton '\ue15b' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatWidth', mod.max(mod.TextBox.Settings.whatWidth-5, 40))
                                            text '[mod.TextBox.Settings.whatWidth]%' yalign .5
                                            textbutton '\ue145' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatWidth', mod.min(mod.TextBox.Settings.whatWidth+5, 100))
                                            textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatWidth', mod.TextBoxSettings.defaultValues['whatWidth'])
                                    vbox:
                                        text '{size=-4}{mod_notl}Position{/mod_notl}{/size}'
                                        hbox: # Position
                                            textbutton '\ue5c4' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatPosition', mod.max(mod.TextBox.Settings.whatPosition-0.05, 0.0))
                                            text '{}%'.format(int(mod.TextBox.Settings.whatPosition*100)) yalign .5
                                            textbutton '\ue5c8' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatPosition', mod.min(mod.TextBox.Settings.whatPosition+0.05, 1.0))
                                            textbutton '\uf053' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'whatPosition', mod.TextBoxSettings.defaultValues['whatPosition'])
                                    use mod_checkbox(checked=mod.TextBox.Settings.whatResizeBackground, text='{mod_notl}Resize background{/mod_notl}', action=ToggleField(mod.TextBox.Settings, 'whatResizeBackground', True, False))

                # Sideimage settings
                showif mod.TextBox.Settings.customSayScreen:
                    vbox at mod_textboxSettingFade:
                        hbox:
                            text '\ue416' style_suffix 'icon'
                            label '{mod_notl}Side image{/mod_notl}'
                            use mod_checkbox(checked=mod.TextBox.Settings.sideImageShown, text='Enabled', action=ToggleField(mod.TextBox.Settings, 'sideImageShown', True, False))
                        
                        showif mod.TextBox.Settings.sideImageShown:
                            hbox at mod_textboxSettingFade:
                                text '{mod_notl}Position: {/mod_notl}' yalign .5
                                hbox:
                                    textbutton '\ue00d' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'sideImagePos', 'left')
                                    textbutton '\ue010' style_suffix 'icon_button' action SetField(mod.TextBox.Settings, 'sideImagePos', 'right')

        hbox:
            xalign 1.0
            spacing mod.scalePxInt(10)
            yoffset mod.scalePxInt(10)

            use mod_iconButton('\ueb8b', '{mod_notl}Help{/mod_notl}', Show('mod_textboxCustomizerHelp'))
            use mod_iconButton('\ue8f4', '{mod_notl}Preview{/mod_notl}', Jump('mod_textboxCustomizer'))
            use mod_iconButton('\ue86c', '{mod_notl}Apply{/mod_notl}', Function(mod.TextBox.closeCustomizer, save=True))
            use mod_iconButton('\uf230', '{mod_notl}Cancel{/mod_notl}', Function(mod.TextBox.closeCustomizer))


screen mod_textboxCustomizerHelp():
    layer 'mod_Overlay'
    style_prefix "mod"

    use mod_Dialog(title='{mod_notl}Textbox customizer{/mod_notl}', closeAction=Hide('mod_textboxCustomizerHelp'), modal=True, icon='\ue88e'):
        text 'This feature enabled you to customize the textbox displaying the game\'s dialogue.\nWhen changing settings, some will show immediately and for some you\'ll have to press the Preview button.'
        null height mod.scalePxInt(10)
        label '{mod_notl}Legend{/mod_notl}'
        hbox:
            text '\ue872' style_suffix 'icon'
            text 'Erase the value (use the game\'s value)'
        hbox:
            text '\uf053' style_suffix 'icon'
            text 'Reset value (back to initial value)'
        hbox:
            text '\ue909' style_suffix 'icon'
            text 'Using the game\'s value'
        hbox:
            text '\ue834' style_suffix 'icon'
            text '{mod_notl}Enabled{/mod_notl}'
        hbox:
            text '\ue835' style_suffix 'icon'
            text '{mod_notl}Disabled{/mod_notl}'


screen mod_textboxCharacterPicker():
    layer 'mod_Overlay'
    style_prefix "mod"
    default charFilterInput = mod.Input(autoFocus=True)

    use mod_Dialog(title='Found '+str(len(mod.Characters.all))+' characters', closeAction=Hide('mod_textboxCharacterPicker'), modal=True, icon='\ue853'):
        text '{mod_notl}Selecter a character{/mod_notl}'

        hbox:
            spacing 5
            text "{mod_notl}Filter: {/mod_notl}" yalign .5
            button:
                xminimum mod.scalePxInt(350)
                key_events True
                action charFilterInput.Enable()
                input value charFilterInput

        viewport:
            ysize mod.scalePxInt(250)
            xsize mod.scalePxInt(450)
            draggable True
            mousewheel True
            scrollbars "vertical"

            vbox:
                for char in mod.Characters.all:
                    if char.match(str(charFilterInput)):
                        textbutton char.fullName substitute False xfill True action [Hide('mod_textboxCharacterPicker'),SetField(mod.TextBox, 'previewCharacter', char.varName)]


screen mod_textboxFontPicker(settingName, defaultSelected=None):
    layer 'mod_Overlay'
    style_prefix "mod"
    default selectedFont = (defaultSelected or list(mod.TextBoxSettings.fontOptions.keys())[0])
    default fontSize = 30
    
    use mod_Dialog(title='{mod_notl}Pick a font{/mod_notl}', closeAction=Hide('mod_textboxFontPicker'), modal=True, icon='\ue165'):
        hbox spacing mod.scalePxInt(20):
            vbox:
                label '{mod_notl}Available fonts{/mod_notl}'
                for name,fontFile in mod.TextBoxSettings.fontOptions.items():
                    if renpy.loadable(fontFile):
                        textbutton name text_font fontFile action SetScreenVariable('selectedFont', name)

            vbox:
                label '{mod_notl}Preview{/mod_notl}'
                hbox:
                    text '{mod_notl}Fontsize: [fontSize]{/mod_notl}' yalign .5
                    textbutton '\ue15b' style_suffix 'icon_button' action SetScreenVariable('fontSize', mod.max(fontSize-2, 12))
                    textbutton '\ue145' style_suffix 'icon_button' action SetScreenVariable('fontSize', mod.min(fontSize+2, 60))
                null height mod.scalePxInt(20)
                text "Here's some example text to show you this font." font mod.TextBoxSettings.fontOptions[selectedFont] size fontSize
                text "And also some bold text to show." bold True font mod.TextBoxSettings.fontOptions[selectedFont] size fontSize
                text "Also some italic while we're at it" italic True font mod.TextBoxSettings.fontOptions[selectedFont] size fontSize

        hbox:
            spacing mod.scalePxInt(10)
            xalign 1.0
            use mod_iconButton('\ue86c', '{mod_notl}Select{/mod_notl}', action=[SetField(mod.TextBox.Settings, settingName, selectedFont),Hide('mod_textboxFontPicker')])
            use mod_iconButton('\uf230', '{mod_notl}Cancel{/mod_notl}', action=Hide('mod_textboxFontPicker'))


label mod_textboxCustomizer(charVarName=None):
    show screen mod_textboxCustomizer (charVarName)
    mod.TextBox.previewCharacter "Here's some text for testing purposes...\nAlso another line of text to fill up this space"
    return

label mod_textboxCustomizer_return:
    return
