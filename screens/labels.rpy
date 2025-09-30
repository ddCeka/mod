
# =============
# LABELS SCREEN
# =============
screen mod_labels():
    style_prefix "mod"
    default thumbnailScale = 22.8
    default movingLabelName = None
    default colWidth = [mod.scaleX(20), mod.scaleX(20)]
    default labelListPages = mod.Pages(len(mod.LabelsStore.store), itemsPerPage=20)
    default labelThumbPages = mod.Pages(len(mod.LabelsStore.store), itemsPerPage=12)
    default nameSorted = None
    
    hbox:
        xfill True
        hbox:
            spacing mod.scalePxInt(5)
            if mod.modFiles.file.filename or len(mod.LabelsStore.store) > 0:
                text "Remembered labels: "+str(len(mod.LabelsStore.store)) yalign 0.5
                textbutton "\ue16c" style_suffix "icon_button" action If(mod.LabelsStore.store.unsaved, mod.Confirm('This will clear the list below, are you sure?', Function(mod.LabelsStore.clear)), Function(mod.LabelsStore.clear))
            else:
                text "Load a file or add labels using the search option"

        hbox:
            xalign 1.0
            if mod.Settings.labelsView == 'list':
                textbutton "\ue3b6" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Show thumbnails{/mod_notl}') unhovered mod.Tooltip() action SetField(mod.Settings, 'labelsView', 'thumbnails')
            else:
                textbutton "\ue8ef" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Show list{/mod_notl}') unhovered mod.Tooltip() action SetField(mod.Settings, 'labelsView', 'list')
    null height mod.scalePxInt(5)
    frame style_suffix "separator" ysize mod.scalePxInt(2)
    
    if len(mod.LabelsStore.store) > 0:
        # =========
        # LIST VIEW
        # =========
        if mod.Settings.labelsView == 'list':
            python:
                if len(mod.LabelsStore.store) != labelListPages.itemCount:
                    SetField(labelListPages, 'itemCount', len(mod.LabelsStore.store))()

            # PAGES
            fixed ysize mod.scalePxInt(50):
                hbox xalign .5 yoffset 4 spacing 2:
                    use mod_pages(labelListPages)

            use mod_tableRow(): # Headers
                hbox xsize colWidth[0]:
                    hbox:
                        label "{mod_notl}Name{/mod_notl}"
                        if nameSorted == 'asc':
                            textbutton '{size=-6}\ue316{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{mod_notl}Sort descending{/mod_notl}') unhovered mod.Tooltip() action [Function(mod.LabelsStore.sort, reverse=True),SetLocalVariable('nameSorted', 'desc')]
                        else:
                            textbutton If(nameSorted,'{size=-6}\ue313{/size}','{size=-6}\ue5d7{/size}') yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{mod_notl}Sort ascending{/mod_notl}') unhovered mod.Tooltip() action [Function(mod.LabelsStore.sort),SetLocalVariable('nameSorted', 'asc')]
                label "{mod_notl}Replay{/mod_notl}" xsize colWidth[1]

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                # Results
                use mod_table():
                    for i,(labelName,props) in enumerate(list(mod.LabelsStore.store.items())[labelListPages.pageStartIndex:labelListPages.pageEndIndex]):
                        use mod_tableRow(i, True):
                            hbox xsize colWidth[0] yalign .5:
                                if 'name' in props:
                                    text mod.scaleText(props['name'], 20) substitute False
                                else:
                                    text mod.scaleText(labelName, 20) substitute False
                            hbox xsize colWidth[1]:
                                hbox spacing 2:
                                    use mod_iconButton('\ue1c4', '{mod_notl}Play{/mod_notl}', action=Show('mod_replay', labelName=labelName))
                                    use mod_iconButton('\ue163', '{mod_notl}Jump{/mod_notl}', action=Show('mod_jump', labelName=labelName))
                            hbox spacing 2:
                                use mod_iconButton('\ue3c9', '{mod_notl}Edit{/mod_notl}', action=Show('mod_remember_var', varName=labelName, rememberType='label', defaultName=If('name' in props, props['name'], labelName)))
                                use mod_iconButton('\ue872', '{mod_notl}Remove{/mod_notl}', action=mod.Confirm('Are you sure you want to remove this label?', Function(mod.LabelsStore.forget, labelName), title='Remove label'))
                                if movingLabelName:
                                    if movingLabelName == labelName:
                                        use mod_iconButton('\uf230', '{mod_notl}Cancel{/mod_notl}', action=SetLocalVariable('movingLabelName', None))
                                    else:
                                        use mod_iconButton('\ue55c', '{mod_notl}Before this{/mod_notl}', action=[Function(mod.LabelsStore.changePos, movingLabelName, labelName),SetLocalVariable('movingLabelName', None)])
                                else:
                                    use mod_iconButton('\ue89f', '{mod_notl}Move{/mod_notl}', action=SetLocalVariable('movingLabelName', labelName))

        # ===============
        # THUMBNAILS VIEW
        # ===============
        else:
            python:
                if len(mod.LabelsStore.store) != labelThumbPages.itemCount:
                    SetField(labelThumbPages, 'itemCount', len(mod.LabelsStore.store))()

            # PAGES
            fixed ysize mod.scalePxInt(50):
                hbox xalign .5 yoffset 4 spacing 2:
                    use mod_pages(labelThumbPages)

            vpgrid:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"
                cols 4
                spacing mod.scalePxInt(10)

                for i,(labelName,props) in enumerate(list(mod.LabelsStore.store.items())[labelThumbPages.pageStartIndex:labelThumbPages.pageEndIndex]):
                    vbox:
                        button:
                            style_suffix 'thumbnailButton'
                            xsize mod.scaleX(thumbnailScale) ysize mod.scaleY(thumbnailScale)
                            action Show('mod_replay', labelName=labelName)
                            add Transform(mod.LabelImage(mod.Label(labelName)), alpha=.7)
                            if 'name' in props:
                                text mod.scaleText(props['name'], thumbnailScale-2) color If(renpy.has_label(labelName), '#fff', '#d00') xalign .5 yalign 1.0 substitute False
                            else:
                                text mod.scaleText(labelName, thumbnailScale-2) color If(renpy.has_label(labelName), '#fff', '#d00') xalign .5 yalign 1.0 substitute False

                        null height 2
                        hbox:
                            xsize mod.scaleX(thumbnailScale)
                            hbox spacing 2:
                                textbutton "\ue1c4" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Replay{/mod_notl}') unhovered mod.Tooltip() action Show('mod_replay', labelName=labelName)
                                textbutton "\ue163" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Jump{/mod_notl}') unhovered mod.Tooltip() action Show('mod_jump', labelName=labelName)
                            hbox spacing 2:
                                xalign 1.0
                                textbutton "\ue3c9" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Edit{/mod_notl}') unhovered mod.Tooltip() action Show('mod_remember_var', varName=labelName, rememberType='label', defaultName=If('name' in props, props['name'], labelName))
                                textbutton "\ue872" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Remove{/mod_notl}') unhovered mod.Tooltip() action mod.Confirm('Are you sure you want to remove this label?', Function(mod.LabelsStore.forget, labelName), title='{mod_notl}Remove label{/mod_notl}')
                                if movingLabelName:
                                    if movingLabelName == labelName:
                                        textbutton '\uf230' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Cancel{/mod_notl}') unhovered mod.Tooltip() action SetLocalVariable('movingLabelName', None)
                                    else:
                                        textbutton '\ue55c' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Before this{/mod_notl}') unhovered mod.Tooltip() action [Function(mod.LabelsStore.changePos, movingLabelName, labelName),SetLocalVariable('movingLabelName', None)]
                                else:
                                    textbutton '\ue89f' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Move{/mod_notl}') unhovered mod.Tooltip()  action SetLocalVariable('movingLabelName', labelName)

                # Fill up till we have 4 columns (this is needed since Ren'Py 7.5)
                for i in range(len(list(mod.LabelsStore.store.items())[labelThumbPages.pageStartIndex:labelThumbPages.pageEndIndex]) % 4):
                    null
            

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "{mod_notl}There are no remembered labels{/mod_notl}" xalign 0.5

# =============
# REPLAY SCREEN
# =============
screen mod_replay(labelName):
    layer 'mod_Overlay'
    style_prefix "mod"
    default errorMessage = None

    use mod_Dialog('Start a replay', closeAction=Hide('mod_replay'), modal=True, icon='\ue1c4'):
        if renpy.has_label(labelName):
            text 'You can end the replay by pressing Alt+M or by choosing "End Replay" in the game menu'
        else:
            text '{mod_notl}The selected label does not exist{/mod_notl}'

        if errorMessage != None:
            null height mod.scalePxInt(10)
            hbox xalign .5:
                use mod_messagebar('error', errorMessage)

        hbox:
            yoffset mod.scalePxInt(15) xalign .5
            if renpy.has_label(labelName):
                key 'K_KP_ENTER' action mod.modReplay(labelName, Hide('mod_replay'), 'errorMessage')
                key 'K_RETURN' action mod.modReplay(labelName, Hide('mod_replay'), 'errorMessage')
                textbutton "{mod_notl}Start{/mod_notl}" style_suffix "buttonPrimary" action mod.modReplay(labelName, Hide('mod_replay'), 'errorMessage')
                null width mod.scalePxInt(10)
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_replay')

# ===========
# JUMP SCREEN
# ===========
screen mod_jump(labelName):
    layer 'mod_Overlay'
    style_prefix "mod"

    use mod_Dialog('{mod_notl}Jump to label{/mod_notl}', closeAction=Hide('mod_jump'), modal=True, icon='\ue163'):
        if renpy.has_label(labelName):
            text 'You are about to jump to a label, this will affect your game' color '#990000' bold True xalign .5
            text 'If you want to play the label without it affecting your game, go back and choose the replay option' xalign .5
            null height 10
            text '(Only use this option if you know what you\'re doing. Your game will continue from the label you\'re jumping to)' color '#AAA' style_suffix 'text_small' xalign .5
        else:
            text '{mod_notl}The selected label does not exist{/mod_notl}'

        hbox:
            yoffset mod.scalePxInt(15) xalign .5
            if renpy.has_label(labelName):
                key 'K_KP_ENTER' action [Hide('mod_jump'),Hide('mod_main'),Jump(labelName)]
                key 'K_RETURN' action [Hide('mod_jump'),Hide('mod_main'),Jump(labelName)]
                textbutton "{mod_notl}Jump{/mod_notl}" style_suffix "buttonPrimary" action [Hide('mod_jump'),Hide('mod_main'),Jump(labelName)]
                null width mod.scalePxInt(10)
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_jump')

# ==================
# REPLAY JUMP SCREEN
# ==================
screen mod_replay_jump(jumpTo, choiceName=None, dialogTitle='{mod_notl}Next label{/mod_notl}'):
    layer 'mod_Overlay'
    style_prefix 'mod'
    default errorMessage = None

    use mod_Dialog(dialogTitle, Hide('mod_replay_jump'), modal=True, icon='\ue1c4'):
        if choiceName:
            hbox:
                label '{mod_notl}Choice {/mod_notl}'
                text choiceName
        hbox:
            label '[dialogTitle] '
            text jumpTo

        vbox:
            yoffset mod.scalePxInt(15)
            spacing mod.scalePxInt(15)

            if errorMessage != None:
                use mod_messagebar('error', errorMessage)

            vbox:
                text 'Playing the label will {b}not{/b} affect your current gameplay (it starts in replay mode)\nand you will return here after ending the replay (press Alt+M)' text_align .5

            hbox: # Buttons
                xalign 0.5
                spacing mod.scalePxInt(20)

                use mod_iconButton('\ue1c4', '{u}P{/u}lay', mod.modReplay(jumpTo, Hide('mod_replay_jump'), 'errorMessage'))
                key 'alt_K_p' action mod.modReplay(jumpTo, Hide('mod_replay_jump'), 'errorMessage')
                use mod_iconButton('\ue4f8', '{u}R{/u}emember', [Hide('mod_replay_jump'),Show('mod_remember_var', varName=jumpTo, rememberType='label')])
                key 'alt_K_r' action [Hide('mod_replay_jump'),Show('mod_remember_var', varName=jumpTo, rememberType='label')]
                textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_replay_jump')
