
screen mod_snapshots():
    style_prefix "mod"
    default comparingSnapshotName = None
    default colWidth = [mod.scaleX(20), mod.scaleX(12), mod.scaleX(60)]
    default comparing = None
    default snapshotsPages = mod.Pages(len(mod.Snapshots.snapshotNames), itemsPerPage=20)

    python:
        if len(mod.Snapshots.snapshotNames) != snapshotsPages.itemCount:
            SetField(snapshotsPages, 'itemCount', len(mod.Snapshots.snapshotNames))()

    hbox:
        spacing mod.scalePxInt(5)
        if comparing:
            use mod_iconButton('\ue5c4', '{mod_notl}Back{/mod_notl}', action=SetLocalVariable('comparing', None))
            if len(comparing) > 1:
                text 'Comparing "{}" with "{}"'.format(comparing[0], comparing[1]) yalign .5
            else:
                text 'Comparing "{}" with "{}"'.format(comparing[0], 'Current variables') yalign .5
        else:
            use mod_iconButton('\ue439', '{mod_notl}Create{/mod_notl}', action=Show('mod_snapshot_create'))
    frame style_suffix "separator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)

    if comparing:
        if len(comparing) > 1:
            use mod_snapshots_comparison(comparing[0], comparing[1])
        else:
            use mod_snapshots_comparison(comparing[0])
    
    elif len(mod.Snapshots.snapshotNames) > 0:
        null height mod.scalePxInt(10)

        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use mod_pages(snapshotsPages)
            hbox xalign 1.0 yalign .5:
                text 'Snapshots: {}'.format(len(mod.Snapshots.snapshotNames))
                null width mod.scalePxInt(10)

        use mod_tableRow(): # Headers
            label "{mod_notl}Name{/mod_notl}" xsize colWidth[0]
            label "{mod_notl}Creation time{/mod_notl}" xsize colWidth[1]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use mod_table():
                for i,name in enumerate(mod.Snapshots.snapshotNames[snapshotsPages.pageStartIndex:snapshotsPages.pageEndIndex]):
                    use mod_tableRow(i, True):
                        hbox xsize colWidth[0] yalign .5:
                            text mod.scaleText(name, 18) substitute False

                        hbox xsize colWidth[1] yalign .5:
                            text mod.Snapshots.getSnapshotTime(name)

                        hbox xsize colWidth[2]:
                            hbox spacing 2:
                                if comparingSnapshotName: # Trying to compare?
                                    if comparingSnapshotName == name:
                                        use mod_iconButton('\uf230', '{mod_notl}Cancel{/mod_notl}', action=SetLocalVariable('comparingSnapshotName', None))
                                    else:
                                        use mod_iconButton('\ueb7d', '{mod_notl}Compare{/mod_notl}', action=[SetLocalVariable('comparing', [comparingSnapshotName,name]),SetLocalVariable('comparingSnapshotName', None)])
                                else:
                                    use mod_iconButton('\ue8f2', '{mod_notl}Show changes{/mod_notl}', SetLocalVariable('comparing', [name]))
                                    use mod_iconButton('\ueb7d', '{mod_notl}Compare with...{/mod_notl}', sensitive=(len(mod.Snapshots.snapshotNames) > 1), action=SetLocalVariable('comparingSnapshotName', name))
                                    use mod_iconButton('\ue872', '{mod_notl}Remove{/mod_notl}', mod.Confirm('Are you sure you want to remove this snapshot?', Function(mod.Snapshots.delete, name), title='{mod_notl}Remove snapshot{/mod_notl}'))

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "{mod_notl}There are no snapshots yet{/mod_notl}" xalign 0.5
            null height mod.scalePxInt(15)
            text "Here you can create snapshots of all current variables and later use them to list all changed variables" xalign .5
            text "(snapshots can be compared to current variables or other snapshots)" xalign .5
            text "Note: Snapshots will be lost when closing the game" style_suffix 'text_small' xalign .5 yoffset mod.scalePxInt(10)


screen mod_snapshots_comparison(old, new=None):
    style_prefix "mod"

    default changes = mod.Snapshots.findChanges(old, new)
    default comparisonColWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(20)]
    default comparisonPages = mod.Pages(len(changes), itemsPerPage=21)
    default compareDict = None
    default compareList = None

    if compareDict:
        hbox yoffset mod.scalePxInt(6):
            spacing mod.scalePxInt(5)
            use mod_iconButton('\ue5c4', '{mod_notl}Back{/mod_notl}', action=SetLocalVariable('compareDict', None))
            text 'Comparing variable "{}"'.format(compareDict['old'].name) yalign .5
        frame style_suffix "separator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(6)
        use mod_snapshots_dictCompare(compareDict)

    elif compareList:
        hbox yoffset mod.scalePxInt(6):
            spacing mod.scalePxInt(5)
            use mod_iconButton('\ue5c4', '{mod_notl}Back{/mod_notl}', action=SetLocalVariable('compareList', None))
            text 'Comparing variable "{}"'.format(compareList['old'].name) yalign .5
        frame style_suffix "separator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(6)
        use mod_snapshots_listCompare(compareList)

    elif len(changes) == 0:
        label "No changes were found" xalign 0.5 yoffset mod.scaleY(1.5)

    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use mod_pages(comparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(changes))

        use mod_tableRow(): # Headers
            label "{mod_notl}Name{/mod_notl}" xsize comparisonColWidth[0]
            label "{mod_notl}Previous{/mod_notl}" xsize comparisonColWidth[1]
            label "{mod_notl}New{/mod_notl}" xsize comparisonColWidth[2]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use mod_table():
                for var in changes[comparisonPages.pageStartIndex:comparisonPages.pageEndIndex]:
                    use mod_tableRow():
                        hbox xsize comparisonColWidth[0] yalign .5:
                            text mod.scaleText(var['old'].name, 18) substitute False

                        hbox xsize comparisonColWidth[1] yalign .5:
                            textbutton var['old'].getButtonValue(17) substitute False action Show('mod_modify_value', var=var['old'])

                        hbox xsize comparisonColWidth[2] yalign .5:
                            textbutton var['new'].getButtonValue(17) substitute False action Show('mod_modify_value', var=var['new'])

                        hbox:
                            hbox spacing 2:
                                # Remember
                                if mod.VarsStore.has(var['new'].name):
                                    use mod_iconButton('\ue4f8', '{mod_notl}Forget{/mod_notl}', Function(mod.VarsStore.forget, var['new'].name))
                                else:
                                    use mod_iconButton('\ue862', '{mod_notl}Remember{/mod_notl}', Show('mod_remember_var', varName=var['new'].name))
                                # Watch
                                if mod.VarsStore.isWatched(var['new'].name):
                                    use mod_iconButton('\ue8f5', '{mod_notl}Unwatch{/mod_notl}', Function(mod.VarsStore.unwatch, var['new'].name))
                                else:
                                    use mod_iconButton('\ue8f4', '{mod_notl}Watch{/mod_notl}', Show('mod_remember_var', varName=var['new'].name, rememberType='watchVar'))
                                # List changes
                                if var['old'].varType == 'dict' and var['new'].varType == 'dict':
                                    use mod_iconButton('\ue8f2', '{mod_notl}Show changes{/mod_notl}', SetLocalVariable('compareDict', var))
                                elif var['old'].varType == 'list' and var['new'].varType == 'list':
                                    use mod_iconButton('\ue8f2', '{mod_notl}Show changes{/mod_notl}', SetLocalVariable('compareList', var))

screen mod_snapshots_dictCompare(compareVar):
    style_prefix "mod"

    default dictChanges = mod.Snapshots.findDictChanges(compareVar['old'].value, compareVar['new'].value)
    default dictComparisonColWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(20)]
    default dictComparisonPages = mod.Pages(len(dictChanges), itemsPerPage=20)

    if len(dictChanges) == 0:
        label "No changes were found" xalign 0.5 yoffset mod.scaleY(1.5)
    
    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use mod_pages(dictComparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(dictChanges))
                null width mod.scalePxInt(10)

        use mod_tableRow(): # Headers
            label "{mod_notl}Name{/mod_notl}" xsize dictComparisonColWidth[0]
            label "{mod_notl}Previous{/mod_notl}" xsize dictComparisonColWidth[1]
            label "{mod_notl}New{/mod_notl}" xsize dictComparisonColWidth[2]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"
            spacing mod.scalePxInt(10)

            # Results
            use mod_table():
                for var in dictChanges[dictComparisonPages.pageStartIndex:dictComparisonPages.pageEndIndex]:
                    use mod_tableRow():
                        hbox xsize dictComparisonColWidth[0] yalign .5:
                            text mod.scaleText(var['old'].name, 18) substitute False

                        hbox xsize dictComparisonColWidth[1] yalign .5:
                            textbutton var['old'].getButtonValue(17) substitute False action Show('mod_modify_value', var=var['old'])

                        hbox xsize dictComparisonColWidth[2] yalign .5:
                            textbutton var['new'].getButtonValue(17) substitute False action NullAction()

screen mod_snapshots_listCompare(compareVar):
    style_prefix "mod"

    default listChanges = mod.Snapshots.findListChanges(compareVar['old'].value, compareVar['new'].value)
    default listComparisonColWidth = [mod.scaleX(15), mod.scaleX(70)]
    default listComparisonPages = mod.Pages(len(listChanges), itemsPerPage=20)

    if len(listChanges) == 0:
        label "{mod_notl}No changes were found{/mod_notl}" xalign 0.5 yoffset mod.scaleY(1.5)
    
    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use mod_pages(listComparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(listChanges))

        use mod_tableRow(): # Headers
            label "{mod_notl}Added/Remove{/mod_notl}" xsize listComparisonColWidth[0]
            label "{mod_notl}Value{/mod_notl}" xsize listComparisonColWidth[1]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use mod_table():
                for change in listChanges[listComparisonPages.pageStartIndex:listComparisonPages.pageEndIndex]:
                    use mod_tableRow():
                        hbox xsize listComparisonColWidth[0]:
                            text change['type']

                        hbox xsize listComparisonColWidth[1]:
                            text mod.scaleText(str(change['val']), 68) substitute False


screen mod_snapshot_create():
    layer 'mod_Overlay'
    style_prefix "mod"

    default submitAction = Function(mod.Snapshots.create, name=mod.GetScreenInput('nameInput'))
    default nameInput = mod.Input(autoFocus=True, onEnter=[submitAction,Hide('mod_snapshot_create')])

    use mod_Dialog(title='{mod_notl}Create snapshot{/mod_notl}', closeAction=Hide('mod_snapshot_create'), modal=True, icon='\ue439'):
        text "Enter a name:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action nameInput.Enable()
            input value nameInput

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "{mod_notl}Create{/mod_notl}" style_suffix "buttonPrimary" action [submitAction,Hide('mod_snapshot_create')]
            null width mod.scalePxInt(10)
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_snapshot_create')

