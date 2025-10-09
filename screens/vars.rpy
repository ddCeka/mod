
# =====================
# VARIABLES MAIN SCREEN
# =====================
screen URM_variables():
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
            
            textbutton '{urm_notl}Variables{/urm_notl}' action SetLocalVariable('expandObjectVars', [])
            for i,var in enumerate(expandObjectVars):
                text '\ue5cc' style_suffix 'icon' yalign .5
                textbutton mod.scaleText(var.namePath[-1], 10) substitute False sensitive (i < len(expandObjectVars)-1) action SetLocalVariable('expandObjectVars', expandObjectVars[:i+1])

        null height mod.scalePxInt(10)
        frame style_suffix "seperator" ysize mod.scalePxInt(2)

        use URM_objectVar(expandObjectVars)

    else:
        python:
            if len(mod.VarsStore.store) != varPages.itemCount:
                SetField(varPages, 'itemCount', len(mod.VarsStore.store))()

        hbox:
            xfill True
            hbox:
                spacing mod.scalePxInt(5)
                if mod.URMFiles.file.filename or len(mod.VarsStore.store) > 0:
                    text "Remembered variables: "+str(len(mod.VarsStore.store)) yalign 0.5
                    textbutton "\ue16c" style_suffix "icon_button" hovered mod.Tooltip('Clear variables list') unhovered mod.Tooltip() action If(mod.VarsStore.store.unsaved, mod.Confirm('This will clear the list below, are you sure?', Function(mod.VarsStore.clear), title='Clear list'), Function(mod.VarsStore.clear))
                else:
                    text "Load a file or add variables using the search option"
            hbox:
                xalign 1.0
                textbutton '\ue03c' style_suffix 'icon_button' hovered mod.Tooltip('{urm_notl}Create variable{/urm_notl}') unhovered mod.Tooltip() action Show('URM_createVar')
                null width mod.scalePxInt(10)
        null height mod.scalePxInt(10)
        frame style_suffix "seperator" ysize mod.scalePxInt(2)

        if len(mod.VarsStore.store) > 0:
            # PAGES
            fixed ysize mod.scalePxInt(50):
                hbox xalign .5 yoffset 4 spacing 2:
                    use URM_pages(varPages)
            # Headers
            use URM_tableRow():
                hbox xsize colWidth[0]:
                    hbox:
                        label "{urm_notl}Name{/urm_notl}"
                        if nameSorted == 'asc':
                            textbutton '{size=-6}\ue316{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort descending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.VarsStore.sort, reverse=True),SetLocalVariable('nameSorted', 'desc')]
                        else:
                            textbutton If(nameSorted,'{size=-6}\ue313{/size}','{size=-6}\ue5d7{/size}') yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort ascending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.VarsStore.sort),SetLocalVariable('nameSorted', 'asc')]
                label "{urm_notl}Value{/urm_notl}" xsize colWidth[1]
                hbox xsize colWidth[2]:
                    hbox:
                        label "{urm_notl}Watch{/urm_notl}"
                        textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('Add this variable to the watchpanel\nSo you can easily view and edit it during playing', title='Watch variable')
                hbox xsize colWidth[3]:
                    hbox:
                        if not mod.StoreMonitor.isSupported:
                            label "{urm_notl}Freeze{/urm_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through URM\n{color=#ff0000}{b}This feature is not supported on the Ren\'Py version used for this game{/b}{/color}', title='Freeze variable')
                        elif mod.StoreMonitor.isAttached:
                            label "{urm_notl}Freeze{/urm_notl}"
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through URM\n{alpha=.8}{size=-5}Use with care. Freezing important variables could break stuff{/size}{/alpha}', title='Freeze variable')
                        else:
                            label "{urm_notl}Freeze{/urm_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('A frozen variable cannot change until you unfreeze it\nYou can only change it through URM\n{color=#ff0000}{b}URM failed to initialize this feature{/b}{/color}', title='Freeze variable')
                hbox xsize colWidth[4]:
                    hbox:
                        if not mod.StoreMonitor.isSupported:
                            label "{urm_notl}Monitor{/urm_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes\n{color=#ff0000}{b}This feature is not supported on the Ren\'Py version used for this game{/b}{/color}', title='Monitor variable')
                        elif mod.StoreMonitor.isAttached:
                            label "{urm_notl}Monitor{/urm_notl}"
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes', title='Monitor variable')
                        else:
                            label "{urm_notl}Monitor{/urm_notl}" text_color '#ff0000'
                            textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('You\'ll receive a notification when this variable changes\n{color=#ff0000}{b}URM failed to initialize this feature{/b}{/color}', title='Monitor variable')
                hbox xsize colWidth[5]:
                    hbox:
                        label "{urm_notl}Ignore{/urm_notl}"
                        textbutton '{size=-6}\uf1c0{/size}' yoffset mod.scalePxInt(-8) style_suffix 'icon_textbutton' action mod.Confirm('Ignore this variable in path detection {font=mods/framework/MaterialIcons-Regular.ttf}\ueb80{/font} and/or codeview {font=mods/framework/MaterialIcons-Regular.ttf}\ue4f3{/font}', title='Ignore variable')
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"
                # Results
                use URM_table():
                    for i,(varName,props) in enumerate(list(mod.VarsStore.store.items())[varPages.pageStartIndex:varPages.pageEndIndex]):
                        use URM_tableRow(i, True):
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
                                    textbutton mod.Var(varName).getButtonValue(19) action Show('URM_modify_value', var=mod.Var(varName)) substitute False
                            hbox xsize colWidth[2]: # Watch
                                if mod.VarsStore.isWatched(varName):
                                    use mod_iconButton('\ue8f4', '{urm_notl}Yes{/urm_notl}', action=Function(mod.VarsStore.unwatch, varName))
                                else:
                                    use mod_iconButton('\ue8f5', '{urm_notl}No{/urm_notl}', action=Show('URM_remember_var', varName=varName, rememberType='watchVar', defaultName=If('name' in props, props['name'], varName)))
                            hbox xsize colWidth[3]: # Freeze
                                if mod.VarsStore.isFrozen(varName):
                                    use mod_iconButton('\ueb3b', '{urm_notl}Yes{/urm_notl}', action=Function(mod.VarsStore.unfreeze, varName), sensitive=If(mod.VarsStore.isFreezable(varName), None, False))
                                else:
                                    use mod_iconButton('\ue798', '{urm_notl}No{/urm_notl}', action=Function(mod.VarsStore.freeze, varName), sensitive=If(mod.VarsStore.isFreezable(varName), None, False))
                            hbox xsize colWidth[4]: # Monitor
                                if mod.VarsStore.isMonitored(varName):
                                    use mod_iconButton('\ue7f4', '{urm_notl}Yes{/urm_notl}', action=Function(mod.VarsStore.unmonitor, varName), sensitive=If(mod.VarsStore.isMonitorable(varName), None, False))
                                else:
                                    use mod_iconButton('\ue7f6', '{urm_notl}No{/urm_notl}', action=Function(mod.VarsStore.monitor, varName), sensitive=If(mod.VarsStore.isMonitorable(varName), None, False))
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
                                use mod_iconButton('\ue3c9', '{urm_notl}Edit{/urm_notl}', action=Show('URM_remember_var', varName=varName, defaultName=If('name' in props, props['name'], varName)))
                                use mod_iconButton('\ue872', '{urm_notl}Remove{/urm_notl}', action=mod.Confirm('Are you sure you want to remove this variable?', Function(mod.VarsStore.forget, varName), title='Remove variable'))
                                if movingVarName:
                                    if movingVarName == varName:
                                        use mod_iconButton('\uf230', '{urm_notl}Cancel{/urm_notl}', action=SetLocalVariable('movingVarName', None))
                                    else:
                                        use mod_iconButton('\ue55c', '{urm_notl}Before this{/urm_notl}', action=[Function(mod.VarsStore.changePos, movingVarName, varName),SetLocalVariable('movingVarName', None)])
                                else:
                                    use mod_iconButton('\ue89f', '{urm_notl}Move{/urm_notl}', action=SetLocalVariable('movingVarName', varName))
        else:
            vbox:
                yoffset mod.scaleY(1.5)
                xalign 0.5
                label "{urm_notl}There are no remembered variables{/urm_notl}" xalign 0.5

# ===================
# MODIFY VALUE SCREEN
# ===================
screen URM_modify_value(var, allowRemember=False):
    layer 'Overlay'
    style_prefix "mod"

    default newValue = var.value
    default errorMessage = None
    default valueInput = mod.Input(
        text=str(newValue),
        autoFocus=True,
        editable=var.isEditable,
        updateScreenVariable='newValue',
        onEnter=mod.SetVarValue(var, onSuccess=Hide('URM_modify_value'), screenErrorVariable='errorMessage', newValue=URMGetScreenVariable('newValue')),
    )

    on "show" action [mod.Search.queryInput.Disable(),valueInput.Enable()]

    use mod_Dialog(title=If(var.isEditable,'{urm_notl}Modify variable{/urm_notl}','{urm_notl}View variable{/urm_notl}'), closeAction=Hide('URM_modify_value'), modal=True, icon='\ue3c9'):
            vbox xminimum mod.scalePxInt(450) # To force a minimum width on the dialog
            label "[var.nameShortened]"
            null height mod.scalePxInt(10)

            text "{urm_notl}Value type: [var.varType]{/urm_notl}"
            if var.isExpandable:
                textbutton var.getButtonValue(23) substitute False action [SetField(mod.Search, 'expandObjectVars', [var]),mod.Open('search')]
            elif var.varType in ['string', 'int', 'float', 'boolean']:
                text "{urm_notl}Value: {/urm_notl}" yalign .5
                if var.varType == 'boolean':
                    textbutton "{urm_notl}[newValue]{/urm_notl}" sensitive var.isEditable action ToggleScreenVariable('newValue', True, False)
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
                        use mod_iconButton('\ue4f8', '{urm_notl}Forget{/urm_notl}', Function(mod.VarsStore.forget, var.name))
                    else:
                        use mod_iconButton('\ue862', '{urm_notl}Remember{/urm_notl}', Show('URM_remember_var', varName=var.name))
                    # Watch
                    if mod.VarsStore.isWatched(var.name):
                        use mod_iconButton('\ue8f5', '{urm_notl}Unwatch{/urm_notl}', Function(mod.VarsStore.unwatch, var.name))
                    else:
                        use mod_iconButton('\ue8f4', '{urm_notl}Watch{/urm_notl}', Show('URM_remember_var', varName=var.name, rememberType='watchVar'))
            hbox:
                yoffset mod.scalePxInt(15)
                align (1.0,1.0)
                spacing mod.scalePxInt(10)

                if var.isEditable:
                    if var.varType != 'unsupported' and var.varType in ['string', 'boolean', 'int', 'float']:
                        textbutton "{urm_notl}Change{/urm_notl}" style_suffix "buttonPrimary" action valueInput.onEnter
                    textbutton "{urm_notl}Delete{/urm_notl}" style_suffix 'buttonCancel' align(0.0, 1.0) action [mod.Confirm('I hope you know what you\'re doing, are you sure you want to continue?', Function(var.delete), title='{urm_notl}Deleting a variable{/urm_notl}'),Hide('URM_modify_value')]
                    textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_modify_value')
                else:
                    textbutton "{urm_notl}Close{/urm_notl}" action Hide('URM_modify_value')

# ==================
# ADD LIST/DICT ITEM
# ==================
screen URM_add_item(parentVar):
    layer 'Overlay'
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
            onSuccess=Hide('URM_add_item'),
            screenErrorVariable='errorMessage',
            newValue=URMGetScreenVariable('itemVal'),
            overruleVarType=URMGetScreenVariable('valueTypes', URMGetScreenVariable('valueTypeIndex')),
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

    use mod_Dialog(title='{urm_notl}Add item{/urm_notl}', closeAction=Hide('URM_add_item'), modal=True, icon='\ue146'):
        label '[parentVar.name]'
        if parentVar.varType=='dict':
            text "{urm_notl}Key:{/urm_notl}"
            button:
                xminimum mod.scalePxInt(450)
                key_events True
                action inputs.itemKey.Enable()
                input value inputs.itemKey
            null height mod.scalePxInt(10)
        hbox:
            text "{urm_notl}Value type:{/urm_notl} " yalign .5
            textbutton valueTypes[valueTypeIndex] action SetScreenVariable('valueTypeIndex', (valueTypeIndex+1) % len(valueTypes))

        text "{urm_notl}Value:{/urm_notl}"
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
            textbutton "{urm_notl}Add{/urm_notl}" sensitive bool(str(inputs.itemKey)) style_suffix "buttonPrimary" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_add_item')

# ============
# REMEMBER VAR
# ============
screen URM_remember_var(varName, rememberType='var', defaultName=None):
    layer 'Overlay'
    style_prefix "mod"
    
    if rememberType == 'label':
        default submitAction = Function(mod.LabelsStore.remember, varName, mod.GetScreenInput('displayNameInput'))
    elif rememberType == 'watchVar':
        default submitAction = Function(mod.VarsStore.watch, varName, mod.GetScreenInput('displayNameInput'))
    else:
        default submitAction = Function(mod.VarsStore.remember, varName, mod.GetScreenInput('displayNameInput'))

    default displayNameInput = mod.Input(text=If(defaultName, defaultName, varName), autoFocus=True, onEnter=[submitAction,Hide('URM_remember_var')])

    on 'show' action [mod.Search.queryInput.Disable(),displayNameInput.Enable()]

    use mod_Dialog(title=If(rememberType=='label', '{urm_notl}Remember label{/urm_notl}', If(rememberType=='watchVar', '{urm_notl}Watch variable{/urm_notl}', '{urm_notl}Remember variable{/urm_notl}')), closeAction=Hide('URM_remember_var'), modal=True, icon=If(rememberType=='watchVar', '\ue8f4', '\ue862')):
        text "{urm_notl}Enter a name:{/urm_notl}"
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
            textbutton "{urm_notl}Save{/urm_notl}" style_suffix "buttonPrimary" action [submitAction,Hide('URM_remember_var')]
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_remember_var')

# ===========
# SAVE SCREEN
# ===========
screen URM_save_file():
    layer 'Overlay'
    style_prefix "mod"
    
    default filenameInput = mod.Input(
        text=If(mod.URMFiles.file.filename, mod.URMFiles.file.filename and mod.URMFiles.file.filename[:-4], mod.URMFiles.stripSpecialChars(config.name)),
        autoFocus=True,
        onEnter=mod.URMFiles.Save(mod.GetScreenInput('filenameInput'), Hide('URM_save_file'), 'errorMessage')
    )
    default errorMessage = None

    on 'show' action [mod.Search.queryInput.Disable(),filenameInput.Enable()]

    use mod_Dialog(title='Save file', closeAction=Hide('URM_save_file'), modal=True, icon='\ue161'):
        text "{urm_notl}Enter a filename:{/urm_notl}"
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
            textbutton "\ueb8b" style_suffix "icon_button" yalign .5 action mod.Confirm(""".URM files can be shared with anyone and are saved in two locations:\n\n{}\n{}""".format(mod.URMFiles.gameDir, mod.URMFiles.saveDir or '<Secondary location unavailable in this game>'), title='URM files', promptSubstitution=False)
            textbutton "{urm_notl}Save{/urm_notl}" style_suffix "buttonPrimary" action filenameInput.onEnter
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_save_file')

# ===========
# LOAD SCREEN
# ===========
screen URM_load_file():
    layer 'Overlay'
    style_prefix "mod"
    default errorMessage = None

    use mod_Dialog(title='{urm_notl}Open file{/urm_notl}', closeAction=Hide('URM_load_file'), modal=True, icon='\ue2c7'):
        text '{urm_notl}Select a file to load:{/urm_notl}'
        if len(mod.URMFiles.listFiles()) == 0:
            hbox:
                ysize mod.scalePxInt(300)
                xsize mod.scalePxInt(650)
                vbox align (.5,.5) spacing mod.scalePxInt(10):
                    label 'No .urm files found' xalign .5
                    text "Looking for files in:\n{}\n{}".format(mod.URMFiles.gameDir, mod.URMFiles.saveDir or '')
        else:
            viewport:
                ysize mod.scalePxInt(300)
                xsize mod.scalePxInt(650)
                draggable True
                mousewheel True
                scrollbars "vertical"
                spacing 2
                vbox spacing 2:
                    for filename,file in mod.URMFiles.listFiles().items():
                        hbox spacing 2:
                            button:
                                xfill True right_margin mod.scalePxInt(45)
                                action mod.URMFiles.Load(filename, Hide('URM_load_file'), 'errorMessage')
                                vbox:
                                    label filename[:-4]
                                    text 'Modified: {}'.format(URMTimeToText(file.mtime))
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

                            textbutton '\ue872' xoffset -mod.scalePxInt(45) style_suffix 'icon_button' action mod.Confirm('Are you sure you want to delete this file? This cannot be undone', mod.URMFiles.Delete(file), title='Confirm deletion')
            if errorMessage != None:
                text errorMessage bold True color "#f42929"

# ==================
# VAR CHANGED SCREEN
# ==================
screen URM_var_changed(varName, prevVal):
    layer 'Overlay'
    style_prefix "mod"
    default var = mod.Var(varName)
    default prevValType = mod.Var.getValType(prevVal)
    default errorMessage = None

    use mod_Dialog(title='{urm_notl}Variable changed{/urm_notl}', closeAction=Hide('URM_var_changed'), modal=True):
        label '{urm_notl}Variable{/urm_notl}'
        text "[var.name]"

        if var.varType != prevValType:
            text "{urm_notl}Type changed from [prevValType] to [var.varType]{/urm_notl}"
        else:
            text "{urm_notl}Type: [var.varType]{/urm_notl}"
        null height mod.scalePxInt(10)

        label "{urm_notl}Previous value{/urm_notl}"
        text "{urm_notl}[prevVal]{/urm_notl}"
        null height mod.scalePxInt(10)
        label "{urm_notl}New value{/urm_notl}"
        text "{urm_notl}[var.value]{/urm_notl}"

        if errorMessage != None:
            use mod_messagebar('error', errorMessage)
        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            if var.varType != 'unsupported':
                textbutton "{urm_notl}Change{/urm_notl}" style_suffix "buttonPrimary" action [Show('URM_modify_value', var=var),Hide('URM_var_changed')]
                null width mod.scalePxInt(10)
            textbutton "{urm_notl}Revert{/urm_notl}" style_suffix 'buttonCancel' align(0.0, 1.0) action mod.SetVarValue(var, onSuccess=Hide('URM_var_changed'), screenErrorVariable='errorMessage', newValue=prevVal)
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Close{/urm_notl}" action Hide('URM_var_changed')

screen URM_objectVar(expandObjectVars):
    default objectPages = mod.Pages(len(expandObjectVars[-1].children), itemsPerPage=19)
    default colWidth = [mod.scaleX(25), mod.scaleX(25)]

    python:
        if len(expandObjectVars[-1].children) != objectPages.itemCount:
            SetField(objectPages, 'itemCount', len(expandObjectVars[-1].children))()

    vbox:
        # PAGES
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use URM_pages(objectPages)
            hbox xalign 1.0 yalign .5:
                text 'Items: {}'.format(len(expandObjectVars[-1].children))
                null width mod.scalePxInt(10)

        if expandObjectVars[-1].varType in ['dict','list']:
            use URM_tableRow():
                use mod_iconButton('\ue146', '{urm_notl}Add item{/urm_notl}', Show('URM_add_item', parentVar=expandObjectVars[-1]))
        # Headers
        use URM_tableRow():
            hbox xsize colWidth[0]:
                label '{urm_notl}Name{/urm_notl}'
            hbox xsize colWidth[1]:
                label '{urm_notl}Value{/urm_notl}'

        if len(expandObjectVars[-1].children) == 0:
            text '{urm_notl}No items{/urm_notl}' xalign .5 yoffset mod.scalePxInt(30)
        else:
            # Results
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                use URM_table():
                    for i,var in enumerate(expandObjectVars[-1].children[objectPages.pageStartIndex:objectPages.pageEndIndex]):
                        use URM_tableRow(i, True):
                            hbox xsize colWidth[0] yalign .5:
                                text mod.scaleText(var.namePath[-1], 23) substitute False
                            hbox xsize colWidth[1] yalign .5:
                                if var.isExpandable:
                                    textbutton var.getButtonValue(23) substitute False action AddToSet(expandObjectVars, var)
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

screen URM_createVar():
    layer 'Overlay'
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
            varName=URMGetScreenVariable('itemName'),
            varVal=URMGetScreenVariable('itemVal'),
            varType=URMGetScreenVariable('valueTypes', URMGetScreenVariable('valueTypeIndex')),
            onSuccess=Hide('URM_createVar'),
            screenErrorVariable='errorMessage',
            overwrite=URMGetScreenVariable('overwrite'),
        ),
    )
    default errorMessage = None
    default valueTypes = ['string', 'int', 'float', 'boolean']
    default valueTypeIndex = 0

    on 'show' action [mod.Search.queryInput.Disable(),Function(inputs.focus)]
    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_Dialog(title='{urm_notl}Create variable{/urm_notl}', closeAction=Hide('URM_createVar'), modal=True, icon='\ue146'):
        text "{urm_notl}Name:{/urm_notl}"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.itemName.Enable()
            input value inputs.itemName
        null height 2
        use mod_checkbox(overwrite, 'Overwrite if exists', ToggleScreenVariable('overwrite', True, False))
        null height mod.scalePxInt(10)
        hbox:
            text "{urm_notl}Value type:{/urm_notl} " yalign .5
            textbutton valueTypes[valueTypeIndex] action SetScreenVariable('valueTypeIndex', (valueTypeIndex+1) % len(valueTypes))
        text "{urm_notl}Value:{/urm_notl}"
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
            textbutton "{urm_notl}Add{/urm_notl}" sensitive bool(str(inputs.itemName)) style_suffix "buttonPrimary" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_createVar')
