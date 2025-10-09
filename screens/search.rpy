
# ==================
# SEARCH MAIN SCREEN
# ==================
screen URM_search():
    style_prefix "mod"
    default colWidth = [mod.scaleX(25), mod.scaleX(25)]
    default searchPages = mod.Pages(len(mod.Search.results), itemsPerPage=20)
    default nameSorted = None
    default expandObjectVars = []

    python:
        if mod.Search.expandObjectVars:
            SetLocalVariable('expandObjectVars', mod.Search.expandObjectVars)()
            mod.Search.expandObjectVars = None

    if len(expandObjectVars):
        default xadj = ui.adjustment() # Used to auto scoll to the end

        python:
            if xadj.value == xadj.range:
                xadj.value = float('inf')

        viewport:
            xfill True ysize mod.scalePxInt(38)
            mousewheel 'horizontal'
            draggable True
            xadjustment xadj
            has hbox
            spacing 2
            
            textbutton 'Results' action SetLocalVariable('expandObjectVars', [])
            for i,var in enumerate(expandObjectVars):
                text '\ue5cc' style_suffix 'icon' yalign .5
                textbutton mod.scaleText(var.namePath[-1], 10) substitute False sensitive (i < len(expandObjectVars)-1) action SetLocalVariable('expandObjectVars', expandObjectVars[:i+1])

        null height mod.scalePxInt(10)
        frame style_suffix "seperator" ysize mod.scalePxInt(2)

        use URM_objectVar(expandObjectVars)

    else:
        python:
            if len(mod.Search.results) != searchPages.itemCount:
                SetField(searchPages, 'itemCount', len(mod.Search.results))()

        hbox:
            xfill True
            hbox:
                spacing 5
                text "Search: " yalign .5
                hbox yalign .5:
                    button:
                        xminimum mod.scalePxInt(250)
                        key_events True
                        action mod.Search.queryInput.Enable()
                        input value mod.Search.queryInput
                text " in " yalign .5
                textbutton "[mod.Search.searchType]" yalign .5 selected False action [Show('URM_search_options'),mod.Search.queryInput.Disable()]
                textbutton "{urm_notl}Search{/urm_notl}" style_suffix "buttonPrimary" yalign .5 action Function(mod.Search.doSearch)
                textbutton "{urm_notl}Reset{/urm_notl}" yalign .5 action Function(mod.Search.resetSearch)

                if mod.Search.searchType == 'labels':
                    text 'Last seen: [mod.Search.lastLabel]' yalign 0.5
                    if renpy.has_label(mod.Search.lastLabel):
                        if not mod.LabelsStore.has(mod.Search.lastLabel):
                            textbutton "\ue609" style_suffix "icon_button" yalign 0.5 hovered mod.Tooltip('Remember label') unhovered mod.Tooltip() action Show('URM_remember_var', varName=mod.Search.lastLabel, rememberType='label')
                        textbutton "\ue1c4" style_suffix "icon_button" yalign 0.5 hovered mod.Tooltip('Replay label') unhovered mod.Tooltip() action Show('URM_replay', labelName=mod.Search.lastLabel)
            hbox xalign 1.0 yalign .5 spacing 2:
                textbutton '{urm_notl}R{/urm_notl}' style_suffix If(mod.Settings.searchRecursive, 'buttonSuccess', 'buttonCancel') selected False hovered mod.Tooltip(If(mod.Settings.searchRecursive, 'Recursive search enabled', 'Recursive search disabled')) unhovered mod.Tooltip() action ToggleField(mod.Settings, 'searchRecursive', True, False) text_xalign .5 xsize mod.scalePxInt(36)
                textbutton '{urm_notl}P{/urm_notl}' style_suffix If(mod.Settings.searchPersistent, 'buttonSuccess', 'buttonCancel') selected False hovered mod.Tooltip(If(mod.Settings.searchPersistent, 'Persistent variables search enabled', 'Persistent variables search disabled')) unhovered mod.Tooltip() action ToggleField(mod.Settings, 'searchPersistent', True, False) text_xalign .5 xsize mod.scalePxInt(36)
                textbutton '{urm_notl}O{/urm_notl}' style_suffix If(mod.Settings.searchObjects, 'buttonSuccess', 'buttonCancel') selected False hovered mod.Tooltip(If(mod.Settings.searchObjects, 'Object search enabled', 'Object search disabled')) unhovered mod.Tooltip() action ToggleField(mod.Settings, 'searchObjects', True, False) text_xalign .5 xsize mod.scalePxInt(36)
                textbutton '{urm_notl}W{/urm_notl}' style_suffix If(mod.Settings.useWildcardSearch, 'buttonSuccess', 'buttonCancel') selected False hovered mod.Tooltip(If(mod.Settings.useWildcardSearch, 'Wildcard search enabled', 'Wildcard search disabled')) unhovered mod.Tooltip() action ToggleField(mod.Settings, 'useWildcardSearch', True, False) text_xalign .5 xsize mod.scalePxInt(36)
                textbutton '{urm_notl}U{/urm_notl}' style_suffix If(mod.Settings.showUnsupportedVariables, 'buttonSuccess', 'buttonCancel') selected False tooltip If(mod.Settings.showUnsupportedVariables, 'Showing unsupported vars', 'Hiding unsupported vars') action ToggleField(mod.Settings, 'showUnsupportedVariables', True, False)
                textbutton '{urm_notl}I{/urm_notl}' style_suffix If(mod.Settings.searchInternalVars, 'buttonSuccess', 'buttonCancel') selected False hovered mod.Tooltip(If(mod.Settings.searchInternalVars, 'Showing internal variables', 'Hiding internal variables')) unhovered mod.Tooltip() action ToggleField(mod.Settings, 'searchInternalVars', True, False) text_xalign .5 xsize mod.scalePxInt(36)
                null width mod.scalePxInt(10)
                
        null height mod.scalePxInt(10)
        frame style_suffix "seperator" ysize mod.scalePxInt(2)

        if len(mod.Search.results) > 0:
            # PAGES
            fixed ysize mod.scalePxInt(50):
                hbox xalign .5 yoffset 4 spacing 2:
                    use URM_pages(searchPages)
                hbox xalign 1.0 yalign .5:
                    text 'Results: {}'.format(len(mod.Search.results))
                    null width mod.scalePxInt(10)
            # Headers
            use URM_tableRow():
                hbox xsize colWidth[0]:
                    hbox:
                        label '{urm_notl}Name{/urm_notl}'
                        if nameSorted == 'asc':
                            textbutton '{size=-6}\ue316{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort descending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.Search.sort, reverse=True),SetLocalVariable('nameSorted', 'desc')]
                        else:
                            textbutton If(nameSorted,'{size=-6}\ue313{/size}','{size=-6}\ue5d7{/size}') yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort ascending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.Search.sort),SetLocalVariable('nameSorted', 'asc')]
                hbox xsize colWidth[1]:
                    label If(mod.Search.searchType=='labels', '{urm_notl}Replay{/urm_notl}', '{urm_notl}Value{/urm_notl}')
            # Results
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                use URM_table():
                    for i,var in enumerate(mod.Search.results[searchPages.pageStartIndex:searchPages.pageEndIndex]):
                        use URM_tableRow(i, True):
                            if mod.Search.searchType == 'labels': # Are we searching labels?
                                hbox xsize colWidth[0] yalign .5:
                                    text mod.scaleText(var.name, 23) substitute False
                                hbox spacing 2 yalign .5:
                                    use mod_iconButton('\ue1c4', '{urm_notl}Play{/urm_notl}', Show('URM_replay', labelName=var.name))
                                    use mod_iconButton('\ue163', '{urm_notl}Jump{/urm_notl}', Show('URM_jump', labelName=var.name))
                                    # Remember
                                    if mod.LabelsStore.has(var.name):
                                        use mod_iconButton('\ue4f8', '{urm_notl}Forget{/urm_notl}', Function(mod.LabelsStore.forget, var.name))
                                    else:
                                        use mod_iconButton('\ue862', '{urm_notl}Remember{/urm_notl}', Show('URM_remember_var', varName=var.name, rememberType='label'))
                            else: # We are searching variables
                                hbox xsize colWidth[0] yalign .5:
                                    text mod.scaleText(var.name, 23) substitute False
                                hbox xsize colWidth[1] yalign .5:
                                    if var.isExpandable:
                                        if len(var.namePath) == 2: # A results we're seeing here could be a subitem/property
                                            textbutton var.getButtonValue(23) substitute False action SetLocalVariable('expandObjectVars', [mod.Var(var.namePath[0]), var])
                                        else:
                                            textbutton var.getButtonValue(23) substitute False action SetLocalVariable('expandObjectVars', [var])
                                    else:
                                        textbutton var.getButtonValue(23) substitute False action Show('URM_modify_value', var=var)
                                hbox spacing 2 yalign .5:
                                    # Remember
                                    if mod.VarsStore.has(var.name):
                                        use mod_iconButton('\ue4f8', '{urm_notl}Forget{/urm_notl}', Function(mod.VarsStore.forget, var.name))
                                    else:
                                        use mod_iconButton('\ue862', '{urm_notl}Remember{/urm_notl}', Show('URM_remember_var', varName=var.name))
                                    # Watch
                                    if mod.VarsStore.isWatched(var.name):
                                        use mod_iconButton('\ue8f5', '{urm_notl}Unwatch{/urm_notl}', Function(mod.VarsStore.unwatch, var.name))
                                    else:
                                        use mod_iconButton('\ue8f4', '{urm_notl}Watch{/urm_notl}', Show('URM_remember_var', varName=var.name, rememberType='watchVar'))
        else: # No results
            vbox:
                yoffset mod.scaleY(1.5)
                xalign 0.5

                label "{urm_notl}No results{/urm_notl}" xalign 0.5
                if mod.Search.searchRecursive:
                    null height mod.scalePxInt(10)
                    text "You're currently doing a recursive search, use the reset button to start over" xalign 0.5
                    text "This means you're searching your previous results instead of everything" xalign 0.5 size 16

# =====================
# SEARCH OPTIONS SCREEN
# =====================
screen URM_search_options():
    layer 'Overlay'
    style_prefix "mod"

    use mod_Dialog('Search options', closeAction=Hide('URM_search_options'), modal=True, icon='\ue8b6'):
        text '{urm_notl}Search type:{/urm_notl}'
        vbox spacing 2:
            use mod_radiobutton(checked=(mod.Search.searchType=='variable names'), text='{urm_notl}Variable names{/urm_notl}', action=[SetField(mod.Search, 'searchType', 'variable names'),Hide('URM_search_options')])
            use mod_radiobutton(checked=(mod.Search.searchType=='values'), text='{urm_notl}Values{/urm_notl}', action=[SetField(mod.Search, 'searchType', 'values'),Hide('URM_search_options')])
            use mod_radiobutton(checked=(mod.Search.searchType=='labels'), text='{urm_notl}Labels/Scenes{/urm_notl}', action=[SetField(mod.Search, 'searchType', 'labels'),Hide('URM_search_options')])

        null height 20
        text 'Other options:'
        vbox spacing 2:
            hbox:
                use mod_checkbox(checked=mod.Settings.searchRecursive, text='Use recursive search', action=ToggleField(mod.Settings, 'searchRecursive', True, False))
                textbutton "\ueb8b" style_suffix "icon_button" yalign .5 hovered mod.Tooltip("Explain resursive search") unhovered mod.Tooltip() action mod.Confirm("""Enabling this feature means you'll search previous results until you reset\n\nExample:\nYou search for value {b}51{/b}, but get a lot of results\nWhen you know the value changed to""", title='Recursive search')
            hbox:
                use mod_checkbox(checked=mod.Settings.searchPersistent, text='Search in persistents', action=ToggleField(mod.Settings, 'searchPersistent', True, False))
                textbutton "\ueb8b" style_suffix "icon_button" yalign .5 hovered mod.Tooltip("Explain persistents") unhovered mod.Tooltip() action mod.Confirm("""Persistent variables are variables outside your save\n\nThose will stay the same regardless of the save you load,\nor even when you start a new game""", title='Persistent variables')
            hbox:
                use mod_checkbox(checked=mod.Settings.searchObjects, text='Search in objects/lists/dicts', action=ToggleField(mod.Settings, 'searchObjects', True, False))
                textbutton "\ueb8b" style_suffix "icon_button" yalign .5 hovered mod.Tooltip("Explain object search") unhovered mod.Tooltip() action mod.Confirm("""Objects, lists and dicts are essentually variables that contain variables\n\nFor example the object {b}player{/b} could contain the variable {b}name{/b}\nWhich is diplayed as {b}player.name{/b}""", title='search objects')
            hbox:
                use mod_checkbox(checked=mod.Settings.useWildcardSearch, text='Use wildcard search', action=ToggleField(mod.Settings, 'useWildcardSearch', True, False))
                textbutton "\ueb8b" style_suffix "icon_button" yalign .5 hovered mod.Tooltip("Explain wildcard search") unhovered mod.Tooltip() action mod.Confirm("""Enabling this feature means results will exactly match the value you've entered. {b}Unless{/b} you use a wilcard.\n\nThere are 2 types of wildcards:\n{b}*{/b} : Will match any character\n{b}?{/b} : Matches any single character""", title='Wildcard search')
            hbox:
                use mod_checkbox(checked=mod.Settings.showUnsupportedVariables, text='Show unsupported variables', action=ToggleField(mod.Settings, 'showUnsupportedVariables', True, False))
                textbutton "\ueb8b" style_suffix "icon_button" yalign .5 tooltip "Explain unsupported variables" action mod.Confirm("""Show variables that URM cannot modify""", title='Unsupported variables')
