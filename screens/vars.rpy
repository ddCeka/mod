
# =====================
# VARIABLES MAIN SCREEN
# =====================
screen mod_variables():
    style_prefix "mod"
    default movingVarName = None
    default colWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(7), mod.scaleX(7), mod.scaleX(7), mod.scaleX(7)]
    default varPages = mod.Pages(len(mod.VarsStore.store), itemsPerPage=20)
    default nameSorted = None
    default expandObjectVars = []

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
            
            textbutton '{mod_notl}Variables{/mod_notl}' action SetLocalVariable('expandObjectVars', [])
            for i,var in enumerate(expandObjectVars):
                text '\ue5cc' style_suffix 'icon' yalign .5
                textbutton mod.scaleText(var.namePath[-1], 10) substitute False sensitive (i < len(expandObjectVars)-1) action SetLocalVariable('expandObjectVars', expandObjectVars[:i+1])

        null height mod.scalePxInt(10)
        frame style_suffix "separator" ysize mod.scalePxInt(2)

        use mod_objectVar(expandObjectVars)

    else:
        python:
            if len(mod.VarsStore.store) != varPages.itemCount:
                SetField(varPages, 'itemCount', len(mod.VarsStore.store))()

        hbox:
            xfill True
            hbox:
                spacing mod.scalePxInt(5)
                if mod.modFiles.file.filename or len(mod.VarsStore.store) > 0:
                    text "Remembered variables: "+str(len(mod.VarsStore.store)) yalign 0.5
                    textbutton "\ue16c" style_suffix "icon_button" hovered mod.Tooltip('Clear variables list') unhovered mod.Tooltip() action If(mod.VarsStore.store.unsaved, mod.Confirm('This will clear the list below, are you sure?', Function(mod.VarsStore.clear), title='Clear list'), Function(mod.VarsStore.clear))
                else:
                    text "Load a file or add variables using the search option"

            hbox:
                xalign 1.0
                textbutton '\ue03c' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Create variable{/mod_notl}') unhovered mod.Tooltip() action Show('mod_createVar')
                null width mod.scalePxInt(10)
        null height mod.scalePxInt(10)
        frame style_suffix "separator" ysize mod.scalePxInt(2)

        if len(mod.VarsStore.store) > 0:
            # PAGES
            fixed ysize mod.scalePxInt(50):
                hbox xalign .5 yoffset 4 spacing 2:
                    use mod_pages(varPages)

            use mod_tableRow(): # Headers
                hbox xsize colWidth[0]:
                    hbox:
                        label "{mod_notl}Name{/mod_notl}"
                        if nameSorted == 'asc':
                            textbutton '{size=-6}\ue316{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{mod_notl}Sort descending{/mod_notl}') unhovered mod.Tooltip() action [Function(mod.VarsStore.sort, reverse=True),SetLocalVariable('nameSorted', 'desc')]
                        else:
                            textbutton If(nameSorted,'{size=-6}\ue313{/size}','{size=-6}\ue5d7{/size}') yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{mod_notl}Sort ascending{/mod_notl}') unhovered mod.Tooltip() action [Function(mod.VarsStore.sort),SetLocalVariable('nameSorted', 'asc')]
                label "{mod_notl}Value{/mod_notl}" xsize colWidth[1]
                hbox xsize colWidth[2]:
                    hbox:
                        label "{mod_notl}Watch{/mod_notl}"
                        textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('Add this variable to the watchpanel\nSo you can easily view and edit it during playing', title='Watch variable')
                hbox xsize colWidth[3]:
                    hbox:
                        if not mod.StoreMonitor.isSupported:
                            label "{mod_notl}Freeze{/mod_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through mod\n{color=#ff0000}{b}This feature is not supported on the Ren\'Py version used for this game{/b}{/color}', title='Freeze variable')
                        elif mod.StoreMonitor.isAttached:
                            label "{mod_notl}Freeze{/mod_notl}"
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through mod\n{alpha=.8}{size=-5}Use with care. Freezing important variables could break stuff{/size}{/alpha}', title='Freeze variable')
                        else:
                            label "{mod_notl}Freeze{/mod_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through mod\n{color=#ff0000}{b}mod failed to initialize this feature{/b}{/color}', title='Freeze variable')
                hbox xsize colWidth[4]:
                    hbox:
                        if not mod.StoreMonitor.isSupported:
                            label "{mod_notl}Monitor{/mod_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes\n{color=#ff0000}{b}This feature is not supported on the Ren\'Py version used for this game{/b}{/color}', title='Monitor variable')
                        elif mod.StoreMonitor.isAttached:
                            label "{mod_notl}Monitor{/mod_notl}"
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes', title='Monitor variable')
                        else:
                            label "{mod_notl}Monitor{/mod_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes\n{color=#ff0000}{b}mod failed to initialize this feature{/b}{/color}', title='Monitor variable')
                hbox xsize colWidth[5]:
                    hbox:
                        label "{mod_notl}Ignore{/mod_notl}"
                        textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('Ignore this variable in path detection {font=mod/framework/MaterialIcons-Regular.ttf}\ueb80{/font} and/or codeview {font=mod/framework/MaterialIcons-Regular.ttf}\ue4f3{/font}', title='Ignore variable')

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                # Results
                use mod_table():
                    for i,(varName,props) in enumerate(list(mod.VarsStore.store.items())[varPages.pageStartIndex:varPages.pageEndIndex]):
                        use mod_tableRow(i, True):
                            hbox xsize colWidth[0] yalign .5:
                                if 'name' in props:
                                    text mod.scaleText(props['name'], 20) substitute False
                                else:
                                    text mod.scaleText(varName, 20) substitute False

                            hbox xsize colWidth[1]:
                                if mod.Var(varName).isExpandable:
                                    if len(mod.Var(varName).namePath) == 2: # A results we're seeing here could be a subitem/property
                                        textbutton mod.Var(varName).getButtonValue(23) substitute False action SetLocalVariable('expandObjectVars', [mod.Var(mod.Var(varName).namePath[0]), mod.Var(varName)])
                                    else:
                                        textbutton mod.Var(varName).getButtonValue(23) substitute False action SetLocalVariable('expandObjectVars', [mod.Var(varName)])
                                else:
                                    textbutton mod.Var(varName).getButtonValue(19) action Show('mod_modify_value', var=mod.Var(varName)) substitute False

                            hbox xsize colWidth[2]: # Watch
                                if mod.VarsStore.isWatched(varName):
                                    use mod_iconButton('\ue8f4', '{mod_notl}Yes{/mod_notl}', action=Function(mod.VarsStore.unwatch, varName))
                                else:
                                    use mod_iconButton('\ue8f5', '{mod_notl}No{/mod_notl}', action=Show('mod_remember_var', varName=varName, rememberType='watchVar', defaultName=If('name' in props, props['name'], varName)))

                            hbox xsize colWidth[3]: # Freeze
                                if mod.VarsStore.isFrozen(varName):
                                    use mod_iconButton('\ueb3b', '{mod_notl}Yes{/mod_notl}', action=Function(mod.VarsStore.unfreeze, varName), sensitive=If(mod.VarsStore.isFreezable(varName), None, False))
                                else:
                                    use mod_iconButton('\ue798', '{mod_notl}No{/mod_notl}', action=Function(mod.VarsStore.freeze, varName), sensitive=If(mod.VarsStore.isFreezable(varName), None, False))

                            hbox xsize colWidth[4]: # Monitor
                                if mod.VarsStore.isMonitored(varName):
                                    use mod_iconButton('\ue7f4', '{mod_notl}Yes{/mod_notl}', action=Function(mod.VarsStore.unmonitor, varName), sensitive=If(mod.VarsStore.isMonitorable(varName), None, False))
                                else:
                                    use mod_iconButton('\ue7f6', '{mod_notl}No{/mod_notl}', action=Function(mod.VarsStore.monitor, varName), sensitive=If(mod.VarsStore.isMonitorable(varName), None, False))

                            hbox xsize colWidth[5]: # Ignore
                                hbox spacing 2:
                                    if mod.VarsStore.isIgnored(varName, 'path'):
                                        use mod_iconButton('\ueb80', action=Function(mod.VarsStore.unignore, varName, 'path'))
                                    else:
                                        use mod_iconButton('\ue065', action=Function(mod.VarsStore.ignore, varName, 'path'))
                                    if mod.VarsStore.isIgnored(varName, 'code'):
                                        use mod_iconButton('\ue4f3', action=Function(mod.VarsStore.unignore, varName, 'code'))
                                    else:
                                        use mod_iconButton('\ue86f', action=Function(mod.VarsStore.ignore, varName, 'code'))

                            hbox spacing 2:
                                use mod_iconButton('\ue3c9', '{mod_notl}Edit{/mod_notl}', action=Show('mod_remember_var', varName=varName, defaultName=If('name' in props, props['name'], varName)))
                                use mod_iconButton('\ue872', '{mod_notl}Remove{/mod_notl}', action=mod.Confirm('Are you sure you want to remove this variable?', Function(mod.VarsStore.forget, varName), title='Remove variable'))
                                if movingVarName:
                                    if movingVarName == varName:
                                        use mod_iconButton('\uf230', '{mod_notl}Cancel{/mod_notl}', action=SetLocalVariable('movingVarName', None))
                                    else:
                                        use mod_iconButton('\ue55c', '{mod_notl}Before this{/mod_notl}', action=[Function(mod.VarsStore.changePos, movingVarName, varName),SetLocalVariable('movingVarName', None)])
                                else:
                                    use mod_iconButton('\ue89f', '{mod_notl}Move{/mod_notl}', action=SetLocalVariable('movingVarName', varName))

        else:
            vbox:
                yoffset mod.scaleY(1.5)
                xalign 0.5
                label "{mod_notl}There are no remembered variables{/mod_notl}" xalign 0.5

# ===================
# MODIFY VALUE SCREEN
# ===================
screen mod_modify_value(var, allowRemember=False):
    layer 'mod_Overlay'
    style_prefix "mod"

    default newValue = var.value
    default errorMessage = None
    default valueInput = mod.Input(
        text=str(newValue),
        autoFocus=True,
        editable=var.isEditable,
        updateScreenVariable='newValue',
        onEnter=mod.SetVarValue(var, onSuccess=Hide('mod_modify_value'), screenErrorVariable='errorMessage', newValue=modGetScreenVariable('newValue')),
    )

    on "show" action [mod.Search.queryInput.Disable(),valueInput.Enable()]

    use mod_Dialog(title=If(var.isEditable,'{mod_notl}Modify variable{/mod_notl}','{mod_notl}View variable{/mod_notl}'), closeAction=Hide('mod_modify_value'), modal=True, icon='\ue3c9'):
            vbox xminimum mod.scalePxInt(450) # To force a minimum width on the dialog
            label "[var.nameShortened]"
            null height mod.scalePxInt(10)

            text "{mod_notl}Value type: [var.varType]{/mod_notl}"
            if var.isExpandable:
                textbutton var.getButtonValue(23) substitute False action [SetField(mod.Search, 'expandObjectVars', [var]),mod.Open('search')]
            elif var.varType in ['string', 'int', 'float', 'boolean']:
                text "{mod_notl}Value: {/mod_notl}" yalign .5
                if var.varType == 'boolean':
                    textbutton "{mod_notl}[newValue]{/mod_notl}" sensitive var.isEditable action ToggleScreenVariable('newValue', True, False)
                elif var.varType in ['string', 'int', 'float']:
                    vpgrid:
                        cols 1
                        draggable True
                        mousewheel True
                        scrollbars "vertical"

                        button:
                            xminimum mod.scalePxInt(450)
                            key_events True
                            sensitive var.isEditable
                            action valueInput.Enable()
                            input value valueInput allow If(var.varType=='string', '', If(var.varType=='float','.0123456789-','0123456789-'))

            if errorMessage != None:
                use mod_messagebar('error', errorMessage)

            if allowRemember:
                null height mod.scalePxInt(10)
                hbox:
                    align (1.0,1.0)
                    spacing mod.scalePxInt(10)

                    # Remember
                    if mod.VarsStore.has(var.name):
                        use mod_iconButton('\ue4f8', '{mod_notl}Forget{/mod_notl}', Function(mod.VarsStore.forget, var.name))
                    else:
                        use mod_iconButton('\ue862', '{mod_notl}Remember{/mod_notl}', Show('mod_remember_var', varName=var.name))
                    # Watch
                    if mod.VarsStore.isWatched(var.name):
                        use mod_iconButton('\ue8f5', '{mod_notl}Unwatch{/mod_notl}', Function(mod.VarsStore.unwatch, var.name))
                    else:
                        use mod_iconButton('\ue8f4', '{mod_notl}Watch{/mod_notl}', Show('mod_remember_var', varName=var.name, rememberType='watchVar'))

            hbox:
                yoffset mod.scalePxInt(15)
                align (1.0,1.0)
                spacing mod.scalePxInt(10)

                if var.isEditable:
                    if var.varType != 'unsupported' and var.varType in ['string', 'boolean', 'int', 'float']:
                        textbutton "{mod_notl}Change{/mod_notl}" style_suffix "buttonPrimary" action valueInput.onEnter
                    textbutton "{mod_notl}Delete{/mod_notl}" style_suffix 'buttonCancel' align(0.0, 1.0) action [mod.Confirm('I hope you know what you\'re doing, are you sure you want to continue?', Function(var.delete), title='{mod_notl}Deleting a variable{/mod_notl}'),Hide('mod_modify_value')]
                    textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_modify_value')
                else:
                    textbutton "{mod_notl}Close{/mod_notl}" action Hide('mod_modify_value')

# ==================
# ADD LIST/DICT ITEM
# ==================
screen mod_add_item(parentVar):
    layer 'mod_Overlay'
    style_prefix "mod"
    
    default itemVal = ''
    default inputs = mod.InputGroup(
        [
            ('itemKey', mod.Input(text=If(parentVar.varType=='dict', '', 'auto.'), editable=(parentVar.varType=='dict'))),
            ('itemVal', mod.Input(updateScreenVariable='itemVal')),
        ],
        focusFirst=True,
        onSubmit=mod.SetVarValue(
            var=parentVar,
            onSuccess=Hide('mod_add_item'),
            screenErrorVariable='errorMessage',
            newValue=modGetScreenVariable('itemVal'),
            overruleVarType=modGetScreenVariable('valueTypes', modGetScreenVariable('valueTypeIndex')),
            operator=If(parentVar.varType=='list', 'append', '='),
            varChildKey=If(parentVar.varType=='dict', mod.GetScreenInput('itemKey', 'inputs'), None),
        ),
    )
    default errorMessage = None
    default valueTypes = ['string', 'int', 'float', 'boolean']
    default valueTypeIndex = 0

    on 'show' action [mod.Search.queryInput.Disable(),Function(inputs.focus)]
    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_Dialog(title='{mod_notl}Add item{/mod_notl}', closeAction=Hide('mod_add_item'), modal=True, icon='\ue146'):
        label '[parentVar.name]'
        if parentVar.varType=='dict':
            text "{mod_notl}Key:{/mod_notl}"
            button:
                xminimum mod.scalePxInt(450)
                key_events True
                action inputs.itemKey.Enable()
                input value inputs.itemKey
            null height mod.scalePxInt(10)

        hbox:
            text "{mod_notl}Value type:{/mod_notl} " yalign .5
            textbutton valueTypes[valueTypeIndex] action SetScreenVariable('valueTypeIndex', (valueTypeIndex+1) % len(valueTypes))

        text "{mod_notl}Value:{/mod_notl}"
        if valueTypes[valueTypeIndex] == 'boolean':
            textbutton "[itemVal]" action ToggleScreenVariable('itemVal', True, False)
        else:
            button:
                xminimum mod.scalePxInt(450)
                key_events True
                action inputs.itemVal.Enable()
                input value inputs.itemVal

        if errorMessage != None:
            use mod_messagebar('error', errorMessage)

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "{mod_notl}Add{/mod_notl}" sensitive bool(str(inputs.itemKey)) style_suffix "buttonPrimary" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_add_item')

# ============
# REMEMBER VAR
# ============
screen mod_remember_var(varName, rememberType='var', defaultName=None):
    layer 'mod_Overlay'
    style_prefix "mod"
    
    if rememberType == 'label':
        default submitAction = Function(mod.LabelsStore.remember, varName, mod.GetScreenInput('displayNameInput'))
    elif rememberType == 'watchVar':
        default submitAction = Function(mod.VarsStore.watch, varName, mod.GetScreenInput('displayNameInput'))
    else:
        default submitAction = Function(mod.VarsStore.remember, varName, mod.GetScreenInput('displayNameInput'))

    default displayNameInput = mod.Input(text=If(defaultName, defaultName, varName), autoFocus=True, onEnter=[submitAction,Hide('mod_remember_var')])

    on 'show' action [mod.Search.queryInput.Disable(),displayNameInput.Enable()]

    use mod_Dialog(title=If(rememberType=='label', '{mod_notl}Remember label{/mod_notl}', If(rememberType=='watchVar', '{mod_notl}Watch variable{/mod_notl}', '{mod_notl}Remember variable{/mod_notl}')), closeAction=Hide('mod_remember_var'), modal=True, icon=If(rememberType=='watchVar', '\ue8f4', '\ue862')):
        text "{mod_notl}Enter a name:{/mod_notl}"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action displayNameInput.Enable()
            input value displayNameInput

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            spacing mod.scalePxInt(10)
            if rememberType == 'label':
                use mod_iconButton('\ueb8b', action=mod.Confirm('Add this label to the labels tab\nSo you can easily find, play and save them', title='Remember label'))
            elif rememberType == 'watchVar':
                use mod_iconButton('\ueb8b', action=mod.Confirm('Add this variable to the watchpanel\nSo you can easily view and edit it during playing', title='Watch variable'))
            else:
                use mod_iconButton('\ueb8b', action=mod.Confirm('Add this variable to the variables tab\nSo you can easily find, edit and save them', title='Remember variable'))
            textbutton "{mod_notl}Save{/mod_notl}" style_suffix "buttonPrimary" action [submitAction,Hide('mod_remember_var')]
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_remember_var')

# ===========
# SAVE SCREEN
# ===========
screen mod_save_file():
    layer 'mod_Overlay'
    style_prefix "mod"
    
    default filenameInput = mod.Input(
        text=If(mod.modFiles.file.filename, mod.modFiles.file.filename and mod.modFiles.file.filename[:-4], mod.modFiles.stripSpecialChars(config.name)),
        autoFocus=True,
        onEnter=mod.modFiles.Save(mod.GetScreenInput('filenameInput'), Hide('mod_save_file'), 'errorMessage')
    )
    default errorMessage = None

    on 'show' action [mod.Search.queryInput.Disable(),filenameInput.Enable()]

    use mod_Dialog(title='Save file', closeAction=Hide('mod_save_file'), modal=True, icon='\ue161'):
        text "{mod_notl}Enter a filename:{/mod_notl}"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action filenameInput.Enable()
            input value filenameInput allow 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123465789-_ '

        if errorMessage != None:
            text errorMessage bold True color "#f42929"

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            spacing mod.scalePxInt(10)
            textbutton "\ueb8b" style_suffix "icon_button" yalign .5 action mod.Confirm(""".mod files can be shared with anyone and are saved in two locations:\n\n{}\n{}""".format(mod.modFiles.gameDir, mod.modFiles.saveDir or '<Secondary location unavailable in this game>'), title='mod files', promptSubstitution=False)
            textbutton "{mod_notl}Save{/mod_notl}" style_suffix "buttonPrimary" action filenameInput.onEnter
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_save_file')

# ===========
# LOAD SCREEN
# ===========
screen mod_load_file():
    layer 'mod_Overlay'
    style_prefix "mod"
    default errorMessage = None

    use mod_Dialog(title='{mod_notl}Open file{/mod_notl}', closeAction=Hide('mod_load_file'), modal=True, icon='\ue2c7'):
        text '{mod_notl}Select a file to load:{/mod_notl}'
        if len(mod.modFiles.listFiles()) == 0:
            hbox:
                ysize mod.scalePxInt(300)
                xsize mod.scalePxInt(650)
                vbox align (.5,.5) spacing mod.scalePxInt(10):
                    label 'No .mod files found' xalign .5
                    text "Looking for files in:\n{}\n{}".format(mod.modFiles.gameDir, mod.modFiles.saveDir or '')
        else:
            viewport:
                ysize mod.scalePxInt(300)
                xsize mod.scalePxInt(650)
                draggable True
                mousewheel True
                scrollbars "vertical"
                spacing 2

                vbox spacing 2:
                    for filename,file in mod.modFiles.listFiles().items():
                        hbox spacing 2:
                            button:
                                xfill True right_margin mod.scalePxInt(45)
                                action mod.modFiles.Load(filename, Hide('mod_load_file'), 'errorMessage')
                                vbox:
                                    label filename[:-4]
                                    text 'Modified: {}'.format(modTimeToText(file.mtime))
                                    if file.storeNames:
                                        hbox spacing 2:
                                            if 'vars' in file.storeNames:
                                                text '\uef54' style_suffix 'icon'
                                            if 'watched' in file.storeNames:
                                                text '\ue8f4' style_suffix 'icon'
                                            if 'labels' in file.storeNames:
                                                text '\ue54e' style_suffix 'icon'
                                            if 'replacements' in file.storeNames:
                                                text '\ue560' style_suffix 'icon'
                                            if 'textboxCustomizations' in file.storeNames:
                                                text '\ue0b7' style_suffix 'icon'

                            textbutton '\ue872' xoffset -mod.scalePxInt(45) style_suffix 'icon_button' action mod.Confirm('Are you sure you want to delete this file? This cannot be undone', mod.modFiles.Delete(file), title='Confirm deletion')

            if errorMessage != None:
                text errorMessage bold True color "#f42929"

# ==================
# VAR CHANGED SCREEN
# ==================
screen mod_var_changed(varName, prevVal):
    layer 'mod_Overlay'
    style_prefix "mod"
    default var = mod.Var(varName)
    default prevValType = mod.Var.getValType(prevVal)
    default errorMessage = None

    use mod_Dialog(title='{mod_notl}Variable changed{/mod_notl}', closeAction=Hide('mod_var_changed'), modal=True):
        label '{mod_notl}Variable{/mod_notl}'
        text "[var.name]"

        if var.varType != prevValType:
            text "{mod_notl}Type changed from [prevValType] to [var.varType]{/mod_notl}"
        else:
            text "{mod_notl}Type: [var.varType]{/mod_notl}"
        null height mod.scalePxInt(10)

        label "{mod_notl}Previous value{/mod_notl}"
        text "{mod_notl}[prevVal]{/mod_notl}"
        null height mod.scalePxInt(10)
        label "{mod_notl}New value{/mod_notl}"
        text "{mod_notl}[var.value]{/mod_notl}"

        if errorMessage != None:
            use mod_messagebar('error', errorMessage)

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            if var.varType != 'unsupported':
                textbutton "{mod_notl}Change{/mod_notl}" style_suffix "buttonPrimary" action [Show('mod_modify_value', var=var),Hide('mod_var_changed')]
                null width mod.scalePxInt(10)
            textbutton "{mod_notl}Revert{/mod_notl}" style_suffix 'buttonCancel' align(0.0, 1.0) action mod.SetVarValue(var, onSuccess=Hide('mod_var_changed'), screenErrorVariable='errorMessage', newValue=prevVal)
            null width mod.scalePxInt(10)
            textbutton "{mod_notl}Close{/mod_notl}" action Hide('mod_var_changed')

screen mod_objectVar(expandObjectVars):
    default objectPages = mod.Pages(len(expandObjectVars[-1].children), itemsPerPage=19)
    default colWidth = [mod.scaleX(25), mod.scaleX(25)]

    python:
        if len(expandObjectVars[-1].children) != objectPages.itemCount:
            SetField(objectPages, 'itemCount', len(expandObjectVars[-1].children))()

    vbox:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use mod_pages(objectPages)
            hbox xalign 1.0 yalign .5:
                text 'Items: {}'.format(len(expandObjectVars[-1].children))
                null width mod.scalePxInt(10)

        if expandObjectVars[-1].varType in ['dict','list']:
            use mod_tableRow():
                use mod_iconButton('\ue146', '{mod_notl}Add item{/mod_notl}', Show('mod_add_item', parentVar=expandObjectVars[-1]))

        # Headers
        use mod_tableRow():
            hbox xsize colWidth[0]:
                label '{mod_notl}Name{/mod_notl}'
            hbox xsize colWidth[1]:
                label '{mod_notl}Value{/mod_notl}'

        if len(expandObjectVars[-1].children) == 0:
            text '{mod_notl}No items{/mod_notl}' xalign .5 yoffset mod.scalePxInt(30)
        else:
            # Results
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                use mod_table():
                    for i,var in enumerate(expandObjectVars[-1].children[objectPages.pageStartIndex:objectPages.pageEndIndex]):
                        use mod_tableRow(i, True):
                            hbox xsize colWidth[0] yalign .5:
                                text mod.scaleText(var.namePath[-1], 23) substitute False
                            hbox xsize colWidth[1] yalign .5:
                                if var.isExpandable:
                                    textbutton var.getButtonValue(23) substitute False action AddToSet(expandObjectVars, var)
                                else:
                                    textbutton var.getButtonValue(23) substitute False action Show('mod_modify_value', var=var)
                            hbox spacing 2 yalign .5:
                                # Remember
                                if mod.VarsStore.has(var.name):
                                    use mod_iconButton('\ue4f8', '{mod_notl}Forget{/mod_notl}', Function(mod.VarsStore.forget, var.name))
                                else:
                                    use mod_iconButton('\ue862', '{mod_notl}Remember{/mod_notl}', Show('mod_remember_var', varName=var.name))
                                # Watch
                                if mod.VarsStore.isWatched(var.name):
                                    use mod_iconButton('\ue8f5', '{mod_notl}Unwatch{/mod_notl}', Function(mod.VarsStore.unwatch, var.name))
                                else:
                                    use mod_iconButton('\ue8f4', '{mod_notl}Watch{/mod_notl}', Show('mod_remember_var', varName=var.name, rememberType='watchVar'))

screen mod_createVar():
    layer 'mod_Overlay'
    style_prefix "mod"
    
    default itemName = ''
    default itemVal = ''
    default overwrite = False
    default inputs = mod.InputGroup(
        [
            ('itemName', mod.Input(updateScreenVariable='itemName')),
            ('itemVal', mod.Input(updateScreenVariable='itemVal')),
        ],
        focusFirst=True,
        onSubmit=mod.CreateVar(
            varName=modGetScreenVariable('itemName'),
            varVal=modGetScreenVariable('itemVal'),
            varType=modGetScreenVariable('valueTypes', modGetScreenVariable('valueTypeIndex')),
            onSuccess=Hide('mod_createVar'),
            screenErrorVariable='errorMessage',
            overwrite=modGetScreenVariable('overwrite'),
        ),
    )
    default errorMessage = None
    default valueTypes = ['string', 'int', 'float', 'boolean']
    default valueTypeIndex = 0

    on 'show' action [mod.Search.queryInput.Disable(),Function(inputs.focus)]
    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_Dialog(title='{mod_notl}Create variable{/mod_notl}', closeAction=Hide('mod_createVar'), modal=True, icon='\ue146'):
        text "{mod_notl}Name:{/mod_notl}"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.itemName.Enable()
            input value inputs.itemName
        null height 2
        use mod_checkbox(overwrite, 'Overwrite if exists', ToggleScreenVariable('overwrite', True, False))
        null height mod.scalePxInt(10)

        hbox:
            text "{mod_notl}Value type:{/mod_notl} " yalign .5
            textbutton valueTypes[valueTypeIndex] action SetScreenVariable('valueTypeIndex', (valueTypeIndex+1) % len(valueTypes))

        text "{mod_notl}Value:{/mod_notl}"
        if valueTypes[valueTypeIndex] == 'boolean':
            textbutton "[itemVal]" action ToggleScreenVariable('itemVal', True, False)
        else:
            button:
                xminimum mod.scalePxInt(450)
                key_events True
                action inputs.itemVal.Enable()
                input value inputs.itemVal

        if errorMessage != None:
            use mod_messagebar('error', errorMessage)

        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "{mod_notl}Add{/mod_notl}" sensitive bool(str(inputs.itemName)) style_suffix "buttonPrimary" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "{mod_notl}Cancel{/mod_notl}" action Hide('mod_createVar')
