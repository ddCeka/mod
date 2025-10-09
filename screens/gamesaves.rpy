
screen URM_gamesaves():
    style_prefix 'mod'
    default slotRegEx = '([0-9]+|quick)-([0-9]+)'

    hbox:
        vbox xsize mod.scaleX(22.8):
            hbox xsize mod.scaleX(22.8):
                label '{urm_notl}Quick resume{/urm_notl}' yalign .5
                textbutton "\ueb8b" style_suffix "icon_button" xalign 1.0 hovered mod.Tooltip("Explain quick resume") unhovered mod.Tooltip() action mod.Confirm("""The game will immediately load this save after starting the game\nThis skips the title screen and menu, you're directly back in the game\n\n{b}IMPORTANT:{/b} This save will be deleted after it has been loaded""", title='Quick resume')
            use URM_gamesaves_button('_reload-1')

            null height mod.scalePxInt(10)

            label '{urm_notl}Newest save{/urm_notl}'
            use URM_gamesaves_button(renpy.newest_slot(slotRegEx))

        null width mod.scalePxInt(10)
        frame style_suffix "vseperator" xsize mod.scalePxInt(2)
        null width mod.scalePxInt(10)

        vbox:
            fixed ysize mod.scalePxInt(45):
                hbox:
                    text mod.Gamesaves.pageName yalign .5 substitute False style_suffix 'label_text'
                    null width mod.scalePxInt(10)
                    textbutton "\ue9a2" style_suffix "icon_button" xalign 1.0 hovered mod.Tooltip("{urm_notl}Rename page{/urm_notl}") unhovered mod.Tooltip() action Show('URM_gamesaves_pagename')
                # PAGES
                hbox xalign 1.0:
                    textbutton "\ue5dc" style_suffix 'icon_button' sensitive (mod.Gamesaves.page != 1) action SetField(mod.Gamesaves, 'page', 1) yalign .5 hovered mod.Tooltip('Go to first page') unhovered mod.Tooltip()
                    textbutton "\ue408" style_suffix 'icon_button' sensitive (mod.Gamesaves.page != mod.Gamesaves.prevPage) action SetField(mod.Gamesaves, 'page', mod.Gamesaves.prevPage) yalign .5 hovered mod.Tooltip('Go to previous page') unhovered mod.Tooltip()

                    textbutton 'A' sensitive ('auto' != mod.Gamesaves.page) action SetField(mod.Gamesaves, 'page', 'auto') hovered mod.Tooltip('Go to auto save page') unhovered mod.Tooltip()
                    textbutton 'Q' sensitive ('quick' != mod.Gamesaves.page) action SetField(mod.Gamesaves, 'page', 'quick') hovered mod.Tooltip('Go to quick save page') unhovered mod.Tooltip()
                    for page in mod.Gamesaves.pageRange:
                        textbutton If(page<10, '0[page]', '[page]') sensitive (page != mod.Gamesaves.page) action SetField(mod.Gamesaves, 'page', page)

                    textbutton "\ue409" style_suffix 'icon_button' action SetField(mod.Gamesaves, 'page', mod.Gamesaves.nextPage) yalign .5 hovered mod.Tooltip('Go to next page') unhovered mod.Tooltip()
                    textbutton "\uf045" style_suffix 'icon_button' action Show('URM_gamesaves_pagenumber') yalign .5 hovered mod.Tooltip('Enter page number') unhovered mod.Tooltip()

            frame style_suffix "seperator" ysize mod.scalePxInt(2)
            null height mod.scalePxInt(10)
            
            vpgrid:
                xfill True yfill True
                cols 3
                mousewheel True
                draggable True
                scrollbars "vertical"
                spacing mod.scalePxInt(10)

                for position in range(1,10):
                    use URM_gamesaves_button('{}-{}'.format(mod.Gamesaves.page, position))

screen URM_gamesaves_button(slot):
    default thumbnailScale = 22.8

    vbox:
        button:
            style_suffix 'thumbnailButton'
            xsize mod.scaleX(thumbnailScale) ysize mod.scaleY(thumbnailScale)
            if renpy.can_load(slot):
                action Function(mod.Gamesaves.load, slot)
                add mod.GameSavesClass.SlotScreenshot(slot) xalign .5 yalign .5
                label mod.Gamesaves.slotTime(slot) xalign .5 text_outlines [(absolute(2), mod.Theme.background, 0, 0)]
                text mod.Gamesaves.slotName(slot) xalign .5 yalign 1.0 substitute False text_align .5 outlines [(absolute(2), mod.Theme.background, 0, 0)]
            else:
                action Function(mod.Gamesaves.save, slot)
                text 'Empty' xalign .5 yalign .5

        null height 2
        hbox xsize mod.scaleX(thumbnailScale):
            hbox spacing 2:
                textbutton "\ue2c7" style_suffix "icon_button" hovered mod.Tooltip('{urm_notl}Load game{/urm_notl}') unhovered mod.Tooltip() action If(renpy.can_load(slot), Function(mod.Gamesaves.load, slot), None)
                textbutton "\ue161" style_suffix "icon_button" hovered mod.Tooltip('{urm_notl}Save game{/urm_notl}') unhovered mod.Tooltip() action Function(mod.Gamesaves.save, slot)
            hbox xalign 1.0 spacing 2:
                textbutton "\ue89f" style_suffix "icon_button" hovered mod.Tooltip('{urm_notl}Move save{/urm_notl}') unhovered mod.Tooltip() action If(renpy.can_load(slot), Function(mod.Gamesaves.move, slot), None)
                textbutton "\ue173" style_suffix "icon_button" hovered mod.Tooltip('{urm_notl}Copy save{/urm_notl}') unhovered mod.Tooltip() action If(renpy.can_load(slot), Function(mod.Gamesaves.copy, slot), None)
                textbutton "\ue872" style_suffix "icon_button" hovered mod.Tooltip('{urm_notl}Delete save{/urm_notl}') unhovered mod.Tooltip() action If(renpy.can_load(slot), Function(mod.Gamesaves.delete, slot), None)

screen URM_gamesaves_selectslot(defaultPage, defaultPosition, callback, confirmButtonText='{urm_notl}OK{/urm_notl}'):
    layer 'Overlay'
    style_prefix "mod"
    
    default inputs = mod.InputGroup([
            ('page', mod.Input(text=defaultPage)),
            ('position', mod.Input(text=defaultPosition)),
        ],
        focusFirst=True,
        onSubmit=[Function(callback, mod.GetScreenInput('page', 'inputs'), mod.GetScreenInput('position', 'inputs')),Hide('URM_gamesaves_selectslot')],
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_Dialog(title='{urm_notl}Select save slot{/urm_notl}', closeAction=Hide('URM_gamesaves_selectslot'), modal=True, icon='\ue161'):
        text "Page:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.page.Enable()
            input value inputs.page allow '0123456789'

        text "Position:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.position.Enable()
            input value inputs.position allow '123456789' length 1
        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton confirmButtonText style_suffix "buttonPrimary" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_gamesaves_selectslot')

screen URM_gamesaves_pagenumber():
    layer 'Overlay'
    style_prefix "mod"
    
    default pageInput = mod.Input(text=str(mod.Gamesaves.page), autoFocus=True, onEnter=[mod.Gamesaves.SetPage(mod.GetScreenInput('pageInput')),Hide('URM_gamesaves_pagenumber')])

    use mod_Dialog(title='{urm_notl}Enter a page number{/urm_notl}', closeAction=Hide('URM_gamesaves_pagenumber'), modal=True, icon='\uf045'):
        text "Page:"
        button:
            xminimum mod.scalePxInt(350)
            key_events True
            action pageInput.Enable()
            input value pageInput allow '0123456789'
        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton '{urm_notl}Open{/urm_notl}' style_suffix "buttonPrimary" action pageInput.onEnter
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_gamesaves_pagenumber')

screen URM_gamesaves_pagename():
    layer 'Overlay'
    style_prefix "mod"
    
    default pageNameInput = mod.Input(text=mod.Gamesaves.pageName, autoFocus=True, onEnter=[mod.Gamesaves.SetPageName(mod.GetScreenInput('pageNameInput')),Hide('URM_gamesaves_pagename')])

    use mod_Dialog(title='{urm_notl}Change page name{/urm_notl}', closeAction=Hide('URM_gamesaves_pagename'), modal=True, icon='\ue9a2'):
        text "{urm_notl}Page name:{/urm_notl}"
        button:
            xminimum mod.scalePxInt(350)
            key_events True
            action pageNameInput.Enable()
            input value pageNameInput length 50

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton '{urm_notl}Change{/urm_notl}' style_suffix "buttonPrimary" action pageNameInput.onEnter
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_gamesaves_pagename')

screen URM_gamesaves_savename(callback):
    layer 'Overlay'
    style_prefix "mod"
    
    default inputSaveName = mod.Input(autoFocus=True, onEnter=[Function(callback, mod.GetScreenInput('inputSaveName')),Hide('URM_gamesaves_savename')])

    use mod_Dialog(title='{urm_notl}Save description{/urm_notl}', closeAction=Hide('URM_gamesaves_savename'), modal=True, icon='\ue161'):
        text "{urm_notl}Save name:{/urm_notl}"
        button:
            xminimum mod.scalePxInt(350)
            key_events True
            action inputSaveName.Enable()
            input value inputSaveName length 150
        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton '{urm_notl}Save{/urm_notl}' style_suffix "buttonPrimary" action inputSaveName.onEnter
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_gamesaves_savename')
