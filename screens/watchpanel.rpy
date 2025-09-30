
transform mod_choicesnotification_slide(width, position='l'):
    xoffset If(position == 'r', width, -width)
    alpha 0.0
    on show, appear:
        linear .2 xoffset 0 alpha 1.0
    on hide:
        linear .2 xoffset If(position == 'r', width, -width) alpha 0.0

transform mod_notification_slide(width, position='l'):
    xoffset If(position == 'r', width, -width)
    linear .2 xoffset 0
    on hide:
        linear .2 xoffset If(position == 'r', width, -width)

style mod_watchpanelItem is mod_frame:
    padding (6, 4)
    background None

style mod_watchpanelItemButton is mod_watchpanelItem:
    hover_background mod.Theme.colors.buttonBgHover
    selected_idle_background mod.Theme.colors.buttonBgHover
    insensitive_background None

# ===========
# MAIN SCREEN
# ===========
screen mod_watchpanel():
    layer 'mod_Overlay'
    style_prefix "mod"
    modal True
    default movingVarName = None
    default panelWidth = mod.scaleX(15)

    frame:
        xalign If(mod.Settings.watchPanelPos == 'r', 1.0, 0.0)
        style_suffix 'dialog'
        at mod_fadeinout
        xmargin -3 ymargin -3
        xsize panelWidth
        yfill True
        has vbox
        xfill True

        hbox:
            xfill True ysize mod.scalePx(46)
            text "{mod_notl}mod{/mod_notl}" style_suffix "header_text" yalign .5 xoffset mod.scalePx(3)
            hbox spacing 2:
                xalign 1.0
                button:
                    style_suffix 'titleBarButton'
                    text "\ue895" style_suffix 'icon_button_text' yalign .5
                    hovered mod.Tooltip('{mod_notl}Open mod{/mod_notl}') unhovered mod.Tooltip()
                    action mod.Open()
                button:
                    style_suffix 'titleBarButton'
                    text If(mod.Settings.watchPanelPos == 'r', "\ue5cc","\ue5cb") style_suffix 'icon_button_text' yalign .5
                    hovered mod.Tooltip('{mod_notl}Hide panel{/mod_notl}') unhovered mod.Tooltip()
                    action SetField(mod.Settings, 'collapsedWatchPanel', True)
        if mod.Tooltip.get('mod_overlay'):
            text mod.Tooltip.get('mod_overlay') xalign .5
        else:
            label '{mod_notl}Watchpanel{/mod_notl}' xalign .5

        frame style_suffix "separator" background mod.Theme.secondary

        use mod_watchPanelFileLine(panelWidth)
        use mod_watchPanelLabel(panelWidth)
        use mod_watchPanelChoiceDetection(panelWidth)
        use mod_watchPanelPathDetection(panelWidth)
        use mod_watchPanelProgress(panelWidth)

        #
        # Watching
        #
        if mod.Settings.watchPanelVars > 0:
            if len(mod.VarsStore.watchedStore) == 0:
                null height 2
                text "{mod_notl}There are no watched variables{/mod_notl}" text_align .5 xalign .5
            else:
                vpgrid:
                    yfill True
                    xfill True
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    cols 1

                    for varName,varProps in list(mod.VarsStore.watchedStore.items()):
                        vbox:
                            frame:
                                style_suffix 'watchpanelItem'
                                has vbox
                                spacing 5
                                if 'name' in varProps:
                                    text mod.scaleText(varProps['name'], 12) bold True substitute False
                                else:
                                    text mod.scaleText(varName, 12) bold True substitute False
                                textbutton mod.Var(varName).getButtonValue(12) hovered mod.Tooltip('{mod_notl}Modify value{/mod_notl}') unhovered mod.Tooltip() action Show('mod_modify_value', var=mod.Var(varName)) substitute False
                                if mod.Settings.watchPanelVars < 2: # NOT compact
                                    hbox spacing 2:
                                        textbutton "\ue8f4" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Change variable{/mod_notl}') unhovered mod.Tooltip() action Show('mod_remember_var', varName=varName, rememberType='watchVar', defaultName=If('name' in varProps, varProps['name'], varName))
                                        textbutton "\ue872" style_suffix "icon_button" hovered mod.Tooltip('{mod_notl}Remove from list{/mod_notl}') unhovered mod.Tooltip() action mod.Confirm('Are you sure you want to remove this variable?', Function(mod.VarsStore.unwatch, varName), title='{mod_notl}Remove variable{/mod_notl}')
                                        if movingVarName:
                                            if movingVarName == varName:
                                                textbutton '\uf230' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Cancel{/mod_notl}') unhovered mod.Tooltip() action SetLocalVariable('movingVarName', None)
                                            else:
                                                textbutton '\ue55c' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Before this{/mod_notl}') unhovered mod.Tooltip() action [Function(mod.VarsStore.changePosWatched, movingVarName, varName),SetLocalVariable('movingVarName', None)]
                                        else:
                                            textbutton '\ue89f' style_suffix 'icon_button' hovered mod.Tooltip('{mod_notl}Move{/mod_notl}') unhovered mod.Tooltip() action SetLocalVariable('movingVarName', varName)
                            
                            frame style_suffix "separator" background mod.Theme.secondary

screen mod_watchPanelFileLine(panelWidth):
    style_prefix "mod"

    if mod.Settings.watchPanelFileLine > 0:
        button xsize panelWidth:
            style_suffix 'watchpanelItemButton'
            if mod.Settings.watchPanelFileLine == 2: # Compact
                hbox:
                    text '\ue86f' style_suffix 'icon_button_text'
                    null width 2
                    text mod.scaleText(mod.currentFileNameLine(), 13, reverse=True) style_suffix 'button_text' substitute False
            else:
                vbox:
                    label '{mod_notl}Current file:line{/mod_notl}'
                    text mod.scaleText(mod.currentFileNameLine(), 14, reverse=True) style_suffix 'button_text' substitute False
            hovered mod.Tooltip('{mod_notl}Show full name:line{/mod_notl}') unhovered mod.Tooltip()
            action mod.Confirm('Last executed line:\n{}'.format(mod.currentFilePathLine()), title='{mod_notl}Current file:line{/mod_notl}')

        frame style_suffix "separator" background mod.Theme.secondary

screen mod_watchPanelLabel(panelWidth):
    style_prefix "mod"

    if mod.Settings.watchPanelCurrentLabel > 0:
        if mod.Settings.watchPanelCurrentLabel == 2: # Compact
            button xsize panelWidth:
                style_suffix 'watchpanelItemButton'
                hbox:
                    text '\ue54e' style_suffix 'icon_button_text'
                    null width 2
                    text mod.scaleText(mod.Search.lastLabel, 13) style_suffix 'button_text' substitute False
                hovered mod.Tooltip('{mod_notl}Show label info{/mod_notl}') unhovered mod.Tooltip()
                action Show('mod_replay_jump', jumpTo=mod.Search.lastLabel, dialogTitle='{mod_notl}Last seen label{/mod_notl}')

        else:
            frame:
                style_suffix 'watchpanelItem'
                has vbox

                label '{mod_notl}Last seen label{/mod_notl}'
                text mod.scaleText(mod.Search.lastLabel, 14) yalign 0.5 substitute False
                if renpy.has_label(mod.Search.lastLabel):
                    hbox spacing 2:
                        if not mod.LabelsStore.has(mod.Search.lastLabel):
                            textbutton "\ue609" style_suffix "icon_button" yalign 0.5 hovered mod.Tooltip('{mod_notl}Remember label{/mod_notl}') unhovered mod.Tooltip() action Show('mod_remember_var', varName=mod.Search.lastLabel, rememberType='label')
                        textbutton "\ue1c4" style_suffix "icon_button" yalign 0.5 hovered mod.Tooltip('{mod_notl}Replay label{/mod_notl}') unhovered mod.Tooltip() action Show('mod_replay', labelName=mod.Search.lastLabel)

        frame style_suffix "separator" background mod.Theme.secondary

screen mod_watchPanelChoiceDetection(panelWidth):
    style_prefix "mod"

    if mod.Settings.watchPanelChoiceDetection > 0:
        if mod.Settings.watchPanelChoiceDetection == 2: # Compact
            button xsize panelWidth:
                style_suffix 'watchpanelItemButton'
                hbox:
                    text '\ue896' style_suffix 'icon_button_text'
                    null width 2
                    if mod.Choices.isDisplayingChoice:
                        text '[mod.Choices.hiddenCount] hidden choices' style_suffix 'button_text'
                    else:
                        text '{mod_notl}No choices detected{/mod_notl}' style_suffix 'button_text'
                if mod.Choices.isDisplayingChoice:
                    hovered mod.Tooltip('{mod_notl}Show choices{/mod_notl}') unhovered mod.Tooltip()
                    action Show('mod_choices')

        else:
            frame:
                style_suffix 'watchpanelItem'
                has vbox

                label '{mod_notl}Displaying choice?{/mod_notl}'
                if mod.Choices.isDisplayingChoice:
                    hbox:
                        xfill True
                        text 'Yes ([mod.Choices.hiddenCount] hidden)' yalign .5
                        textbutton '\ue896' style_suffix 'icon_button' xalign 1.0 hovered mod.Tooltip('Show choices') unhovered mod.Tooltip() action Show('mod_choices')
                else:
                    text '{mod_notl}No{/mod_notl}'

        frame style_suffix "separator" background mod.Theme.secondary

screen mod_watchPanelPathDetection(panelWidth):
    style_prefix "mod"

    if mod.Settings.watchPanelPathDetection > 0:
        if mod.Settings.watchPanelPathDetection == 2: # Compact
            button xsize panelWidth:
                style_suffix 'watchpanelItemButton'
                hbox:
                    text '\uf184' style_suffix 'icon_button_text'
                    null width 2
                    if mod.PathDetection.pathIsNext:
                        text '[mod.PathDetection.statementsCount] paths detected' style_suffix 'button_text'
                    else:
                        text '{mod_notl}No path detected{/mod_notl}' style_suffix 'button_text'
                if mod.PathDetection.pathIsNext:
                    hovered mod.Tooltip('{mod_notl}Show paths{/mod_notl}') unhovered mod.Tooltip()
                    action Show('mod_paths')

        else:
            frame:
                style_suffix 'watchpanelItem'
                has vbox

                label 'Detected path?'
                if mod.PathDetection.pathIsNext:
                    hbox:
                        xfill True
                        text '[mod.PathDetection.statementsCount] paths' yalign .5
                        textbutton '\uf184' style_suffix 'icon_button' xalign 1.0 hovered mod.Tooltip('Show options') unhovered mod.Tooltip() action Show('mod_paths')
                else:
                    text '{mod_notl}No{/mod_notl}'

        frame style_suffix "separator" background mod.Theme.secondary

screen mod_watchPanelProgress(panelWidth):
    style_prefix "mod"

    if mod.Settings.watchPanelProgress > 0:
        button xsize panelWidth:
            style_suffix 'watchpanelItemButton'
            if mod.Settings.watchPanelProgress == 2: # Compact
                hbox:
                    text '\uf1c5' style_suffix 'icon_button_text'
                    null width 2
                    text "[mod.ProgressBar.percentage]% {size=-8}([mod.ProgressBar.seen]/[mod.ProgressBar.total]){/size}" style_suffix 'button_text'
            else:
                vbox:
                    label 'Progress'
                    text '[mod.ProgressBar.percentage]% {size=-8}([mod.ProgressBar.seen]/[mod.ProgressBar.total]){/size}' style_suffix 'button_text'
            action ToggleField(mod.Settings, 'progressShown', True, False)

        frame style_suffix "separator" background mod.Theme.secondary

style mod_notification is mod_default:
    background AlphaMask(Solid(mod.Theme.colors.buttonBg), Frame('mod/images/notificationMask.png', 236, 0, 0, 0))
    hover_background AlphaMask(Solid(mod.Theme.colors.buttonBgHover), Frame('mod/images/notificationMask.png', 236, 0, 0, 0))
    selected_idle_background AlphaMask(Solid(mod.Theme.colors.buttonBgHover), Frame('mod/images/notificationMask.png', 236, 0, 0, 0))
    insensitive_background AlphaMask(Solid(mod.Theme.colors.buttonBgDisabled), Frame('mod/images/notificationMask.png', 236, 0, 0, 0))
    padding (mod.scalePxInt(8), mod.scalePxInt(8))

style mod_notification_text is mod_button_text:
    outlines [(absolute(1), mod.Theme.colors.buttonBg, 0, 0)]

screen mod_notifications():
    layer 'mod_Overlay'
    style_prefix "mod"
    default width = mod.scalePxInt(270)

    vbox:
        yoffset If(mod.Settings.showWatchPanel and mod.Settings.collapsedWatchPanel, mod.scalePxInt(45), 5) # We need some yoffset if the watchpanel togglebutton is there
        xalign If(mod.Settings.watchPanelPos == 'r', 1.0, 0.0)
        xoffset (If(mod.Settings.showWatchPanel and not mod.Settings.collapsedWatchPanel, mod.scaleX(15), 0) * If(mod.Settings.watchPanelPos == 'r', -1, 1)) # Offset notification when the panel is open, multiply by 1 or -1 for left or right panel
        spacing 2

        # ==========
        # END REPLAY
        # ==========
        showif mod.Settings.showReplayNotification and _in_replay and (not mod.Settings.showWatchPanel or mod.Settings.collapsedWatchPanel):
            key 'alt_K_e' action EndReplay(False)
            button:
                style_suffix 'notification'
                xminimum width
                action mod.Confirm("Do you want to end the current replay?", renpy.end_replay, title='End replay')
                
                vbox:
                    hbox:
                        text '\uef71' style_suffix 'icon_button_text'
                        null width mod.scalePxInt(4)
                        text '{u}E{/u}nd replay' style_suffix 'notification_text' bold True

        # ====================
        # Choices notification
        # ====================
        showif mod.Settings.showChoicesNotification and mod.Choices.isDisplayingChoice and (not mod.Settings.showWatchPanel or mod.Settings.collapsedWatchPanel):
            key 'alt_K_c' action Show('mod_choices')
            button:
                at mod_choicesnotification_slide(width, mod.Settings.watchPanelPos)
                style_suffix 'notification'
                xminimum width
                action Show('mod_choices')

                vbox:
                    hbox:
                        text '\ue896' style_suffix 'icon_button_text'
                        null width mod.scalePxInt(4)
                        text '{u}C{/u}hoices detected' style_suffix 'notification_text' bold True
                    if mod.Choices.hiddenCount > 0:
                        text '[mod.Choices.hiddenCount] hidden' style_suffix 'notification_text'

        # ==================
        # Paths notification
        # ==================
        showif mod.Settings.showPathsNotification and mod.PathDetection.pathIsNext and (not mod.Settings.showWatchPanel or mod.Settings.collapsedWatchPanel):
            if mod.Settings.stopSkippingOnPathDetection:
                on 'show' action mod.CancelSkipping()

            key 'alt_K_a' action Show('mod_paths')
            button:
                at mod_choicesnotification_slide(width, mod.Settings.watchPanelPos)
                style_suffix 'notification'
                xminimum width
                action Show('mod_paths')

                vbox:
                    hbox:
                        text '\uf184' style_suffix 'icon_button_text'
                        null width mod.scalePxInt(4)
                        text 'P{u}a{/u}th detected' style_suffix 'notification_text' bold True
                    text '[mod.PathDetection.statementsCount] options' style_suffix 'notification_text'

        # ==================
        # TEMP NOTIFICATIONS
        # ==================
        for notif in mod.Notifications.notifications:
            button:
                at mod_notification_slide(width, mod.Settings.watchPanelPos)
                style_suffix 'notification'
                xminimum width
                action notif

                vbox:
                    text mod.scaleText(notif.label, 260, style='mod_label_text', pixelTarget=True) style_suffix 'notification_text' bold True
                    if notif.text:
                        text mod.scaleText(notif.text, 260, pixelTarget=True) style_suffix 'notification_text'

        if len(mod.Notifications.notifications):
            button:
                at mod_notification_slide(width, mod.Settings.watchPanelPos)
                style_suffix 'notification'
                xminimum width
                action Function(mod.Notifications.clear)

                hbox:
                    text '\ue92b' style_suffix 'icon_button_text' yalign .5
                    text '{mod_notl}Dismiss all{/mod_notl}' style_suffix 'notification_text'
