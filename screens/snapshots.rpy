
screen URM_snapshots():
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
            use mod_iconButton('\ue5c4', '{urm_notl}Back{/urm_notl}', action=SetLocalVariable('comparing', None))
            if len(comparing) > 1:
                text 'Comparing "{}" with "{}"'.format(comparing[0], comparing[1]) yalign .5
            else:
                text 'Comparing "{}" with "{}"'.format(comparing[0], 'Current variables') yalign .5
        else:
            use mod_iconButton('\ue439', '{urm_notl}Create{/urm_notl}', action=Show('URM_snapshot_create'))
    frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(5)

    if comparing:
        if len(comparing) > 1:
            use URM_snapshots_comparison(comparing[0], comparing[1])
        else:
            use URM_snapshots_comparison(comparing[0])
    
    elif len(mod.Snapshots.snapshotNames) > 0:
        null height mod.scalePxInt(10)

        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use URM_pages(snapshotsPages)
            hbox xalign 1.0 yalign .5:
                text 'Snapshots: {}'.format(len(mod.Snapshots.snapshotNames))
                null width mod.scalePxInt(10)

        use URM_tableRow(): # Headers
            label "{urm_notl}Name{/urm_notl}" xsize colWidth[0]
            label "{urm_notl}Creation time{/urm_notl}" xsize colWidth[1]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use URM_table():
                for i,name in enumerate(mod.Snapshots.snapshotNames[snapshotsPages.pageStartIndex:snapshotsPages.pageEndIndex]):
                    use URM_tableRow(i, True):
                        hbox xsize colWidth[0] yalign .5:
                            text mod.scaleText(name, 18) substitute False

                        hbox xsize colWidth[1] yalign .5:
                            text mod.Snapshots.getSnapshotTime(name)

                        hbox xsize colWidth[2]:
                            hbox spacing 2:
                                if comparingSnapshotName: # Trying to compare?
                                    if comparingSnapshotName == name:
                                        use mod_iconButton('\uf230', '{urm_notl}Cancel{/urm_notl}', action=SetLocalVariable('comparingSnapshotName', None))
                                    else:
                                        use mod_iconButton('\ueb7d', '{urm_notl}Compare{/urm_notl}', action=[SetLocalVariable('comparing', [comparingSnapshotName,name]),SetLocalVariable('comparingSnapshotName', None)])
                                else:
                                    use mod_iconButton('\ue8f2', '{urm_notl}Show changes{/urm_notl}', SetLocalVariable('comparing', [name]))
                                    use mod_iconButton('\ueb7d', '{urm_notl}Compare with...{/urm_notl}', sensitive=(len(mod.Snapshots.snapshotNames) > 1), action=SetLocalVariable('comparingSnapshotName', name))
                                    use mod_iconButton('\ue872', '{urm_notl}Remove{/urm_notl}', mod.Confirm('Are you sure you want to remove this snapshot?', Function(mod.Snapshots.delete, name), title='{urm_notl}Remove snapshot{/urm_notl}'))

    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            label "{urm_notl}There are no snapshots yet{/urm_notl}" xalign 0.5
            null height mod.scalePxInt(15)
            text "Here you can create snapshots of all current variables and later use them to list all changed variables" xalign .5
            text "(snapshots can be compared to current variables or other snapshots)" xalign .5
            text "Note: Snapshots will be lost when closing the game" style_suffix 'text_small' xalign .5 yoffset mod.scalePxInt(10)


screen URM_snapshots_comparison(old, new=None):
    style_prefix "mod"

    default changes = mod.Snapshots.findChanges(old, new)
    default comparisonColWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(20)]
    default comparisonPages = mod.Pages(len(changes), itemsPerPage=21)
    default compareDict = None
    default compareList = None

    if compareDict:
        hbox yoffset mod.scalePxInt(6):
            spacing mod.scalePxInt(5)
            use mod_iconButton('\ue5c4', '{urm_notl}Back{/urm_notl}', action=SetLocalVariable('compareDict', None))
            text 'Comparing variable "{}"'.format(compareDict['old'].name) yalign .5
        frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(6)
        use URM_snapshots_dictCompare(compareDict)

    elif compareList:
        hbox yoffset mod.scalePxInt(6):
            spacing mod.scalePxInt(5)
            use mod_iconButton('\ue5c4', '{urm_notl}Back{/urm_notl}', action=SetLocalVariable('compareList', None))
            text 'Comparing variable "{}"'.format(compareList['old'].name) yalign .5
        frame style_suffix "seperator" ysize mod.scalePxInt(2) yoffset mod.scalePxInt(6)
        use URM_snapshots_listCompare(compareList)

    elif len(changes) == 0:
        label "No changes were found" xalign 0.5 yoffset mod.scaleY(1.5)

    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use URM_pages(comparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(changes))

        use URM_tableRow(): # Headers
            label "{urm_notl}Name{/urm_notl}" xsize comparisonColWidth[0]
            label "{urm_notl}Previous{/urm_notl}" xsize comparisonColWidth[1]
            label "{urm_notl}New{/urm_notl}" xsize comparisonColWidth[2]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use URM_table():
                for var in changes[comparisonPages.pageStartIndex:comparisonPages.pageEndIndex]:
                    use URM_tableRow():
                        hbox xsize comparisonColWidth[0] yalign .5:
                            text mod.scaleText(var['old'].name, 18) substitute False

                        hbox xsize comparisonColWidth[1] yalign .5:
                            textbutton var['old'].getButtonValue(17) substitute False action Show('URM_modify_value', var=var['old'])

                        hbox xsize comparisonColWidth[2] yalign .5:
                            textbutton var['new'].getButtonValue(17) substitute False action Show('URM_modify_value', var=var['new'])

                        hbox:
                            hbox spacing 2:
                                # Remember
                                if mod.VarsStore.has(var['new'].name):
                                    use mod_iconButton('\ue4f8', '{urm_notl}Forget{/urm_notl}', Function(mod.VarsStore.forget, var['new'].name))
                                else:
                                    use mod_iconButton('\ue862', '{urm_notl}Remember{/urm_notl}', Show('URM_remember_var', varName=var['new'].name))
                                # Watch
                                if mod.VarsStore.isWatched(var['new'].name):
                                    use mod_iconButton('\ue8f5', '{urm_notl}Unwatch{/urm_notl}', Function(mod.VarsStore.unwatch, var['new'].name))
                                else:
                                    use mod_iconButton('\ue8f4', '{urm_notl}Watch{/urm_notl}', Show('URM_remember_var', varName=var['new'].name, rememberType='watchVar'))
                                # List changes
                                if var['old'].varType == 'dict' and var['new'].varType == 'dict':
                                    use mod_iconButton('\ue8f2', '{urm_notl}Show changes{/urm_notl}', SetLocalVariable('compareDict', var))
                                elif var['old'].varType == 'list' and var['new'].varType == 'list':
                                    use mod_iconButton('\ue8f2', '{urm_notl}Show changes{/urm_notl}', SetLocalVariable('compareList', var))

screen URM_snapshots_dictCompare(compareVar):
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
                use URM_pages(dictComparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(dictChanges))
                null width mod.scalePxInt(10)

        use URM_tableRow(): # Headers
            label "{urm_notl}Name{/urm_notl}" xsize dictComparisonColWidth[0]
            label "{urm_notl}Previous{/urm_notl}" xsize dictComparisonColWidth[1]
            label "{urm_notl}New{/urm_notl}" xsize dictComparisonColWidth[2]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"
            spacing mod.scalePxInt(10)

            # Results
            use URM_table():
                for var in dictChanges[dictComparisonPages.pageStartIndex:dictComparisonPages.pageEndIndex]:
                    use URM_tableRow():
                        hbox xsize dictComparisonColWidth[0] yalign .5:
                            text mod.scaleText(var['old'].name, 18) substitute False

                        hbox xsize dictComparisonColWidth[1] yalign .5:
                            textbutton var['old'].getButtonValue(17) substitute False action Show('URM_modify_value', var=var['old'])

                        hbox xsize dictComparisonColWidth[2] yalign .5:
                            textbutton var['new'].getButtonValue(17) substitute False action NullAction()

screen URM_snapshots_listCompare(compareVar):
    style_prefix "mod"

    default listChanges = mod.Snapshots.findListChanges(compareVar['old'].value, compareVar['new'].value)
    default listComparisonColWidth = [mod.scaleX(15), mod.scaleX(70)]
    default listComparisonPages = mod.Pages(len(listChanges), itemsPerPage=20)

    if len(listChanges) == 0:
        label "{urm_notl}No changes were found{/urm_notl}" xalign 0.5 yoffset mod.scaleY(1.5)
    
    else:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use URM_pages(listComparisonPages)
            hbox xalign 1.0 yalign .5:
                text 'Changes: {}'.format(len(listChanges))

        use URM_tableRow(): # Headers
            label "{urm_notl}Added/Remove{/urm_notl}" xsize listComparisonColWidth[0]
            label "{urm_notl}Value{/urm_notl}" xsize listComparisonColWidth[1]

        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            # Results
            use URM_table():
                for change in listChanges[listComparisonPages.pageStartIndex:listComparisonPages.pageEndIndex]:
                    use URM_tableRow():
                        hbox xsize listComparisonColWidth[0]:
                            text change['type']

                        hbox xsize listComparisonColWidth[1]:
                            text mod.scaleText(str(change['val']), 68) substitute False


screen URM_snapshot_create():
    layer 'Overlay'
    style_prefix "mod"

    default submitAction = Function(mod.Snapshots.create, name=mod.GetScreenInput('nameInput'))
    default nameInput = mod.Input(autoFocus=True, onEnter=[submitAction,Hide('URM_snapshot_create')])

    use mod_Dialog(title='{urm_notl}Create snapshot{/urm_notl}', closeAction=Hide('URM_snapshot_create'), modal=True, icon='\ue439'):
        text "Enter a name:"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action nameInput.Enable()
            input value nameInput

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "{urm_notl}Create{/urm_notl}" style_suffix "buttonPrimary" action [submitAction,Hide('URM_snapshot_create')]
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_snapshot_create')

