
style mod_titleBarButton is mod_dialogCloseButton:
    background mod.Theme.colors.buttonBg
    hover_background mod.Theme.colors.buttonBgHover
    yoffset 0
    padding (mod.scalePxInt(8),0)

style mod_tab is mod_buttonSecondary:
    background mod.Theme.colorAlpha(mod.Theme.colors.buttonSecondaryBg, .4)
    hover_background mod.Theme.colors.buttonSecondaryBgHover
    selected_idle_background mod.Theme.colors.buttonSecondaryBgHover
    insensitive_background mod.Theme.colors.buttonSecondaryBgDisabled

transform mod_blink:
    linear .5 alpha .65
    linear .5 alpha 1.0
    pause 1.0
    repeat

screen URM_overlay():
    layer 'Overlay'
    style_prefix "mod"

    key "alt_K_m" action mod.Open()
    if mod.Settings.quickResumeSaveHotKey:
        key "alt_K_q" action mod.Gamesaves.Save('_reload-1', name='', overwrite=True, notify='Quick resume saved')
    if mod.Settings.quickSaveHotKey:
        key "alt_K_s" action QuickSave()
    if mod.Settings.quickLoadHotKey:
        key "alt_K_l" action QuickLoad()
    if mod.Settings.consoleHotKey:
        key "alt_K_o" action mod.OpenConsole()
    # Prevent the Shift+O when console is disabled
    if not config.console and not config.developer:
        key "shift_K_o" action NullAction()

    if mod.Settings.showWatchPanel:
        # Watchpanel toggle key
        if mod.Settings.watchpanelToggleKey and isinstance(mod.Settings.watchpanelToggleKey, basestring):
            key "K_{}".format(mod.Settings.watchpanelToggleKey[0].lower()) action ToggleField(mod.Settings, 'collapsedWatchPanel', True, False)

        if mod.Settings.collapsedWatchPanel:
            if not mod.Settings.watchpanelHideToggleButton or not mod.Settings.watchpanelToggleKey:
                if mod.Settings.watchPanelPos == 'r': # Position right
                    textbutton "\ue5cb" style_suffix "icon_button" align (1.0, 0.0) action SetField(mod.Settings, 'collapsedWatchPanel', False)
                else:
                    textbutton "\ue5cc" style_suffix "icon_button" align (0.0, 0.0) action SetField(mod.Settings, 'collapsedWatchPanel', False)
        else:
            use URM_watchpanel
    # # Detection notifications
    use URM_notifications
    # Show the touch buttton
    if mod.Settings.touchEnabled or (renpy.variant("touch") and not mod.States.gestureInitialized):
        drag:
            draggable True
            if mod.Settings.touchPosition:
                pos mod.Settings.touchPosition
            else:
                align (.5,.5)
            clicked mod.Open()
            dragged mod.touchDragged

            idle_child Transform('mods/images/logo.png', alpha=.8, zoom=mod.getScaleFactor())
            hover_child Transform('mods/images/logo.png', zoom=mod.getScaleFactor())
    # Show progressbar
    if mod.Settings.progressShown:
        use URM_progress

# ===========
# MAIN SCREEN
# ===========
screen URM_main():
    layer 'Overlay'
    style_prefix "mod"
    modal True

    key "ctrl_K_n" action mod.URMFiles.Clear()
    key "ctrl_K_o" action mod.URMFiles.Load()
    key "ctrl_K_s" action mod.URMFiles.Save()
    key 'K_ESCAPE' action Hide('URM_main')

    frame:
        at mod_fadeinout
        style_suffix 'dialog'
        xfill True yfill True
        xmargin mod.scalePxInt(-3) ymargin mod.scalePxInt(-3)

        hbox:
            ysize mod.scalePxInt(42) xoffset mod.scalePxInt(3)
            add renpy.display.im.FactorScale('mods/images/logo.png', mod.getScaleFactor()*.95) yalign .5
        hbox:
            align (0.03, 0.0)
            spacing 2
            button: # Panel
                style_suffix 'titleBarButton'
                text If(mod.Settings.showWatchPanel, '\ue8f4', '\ue8f5') style_suffix 'icon_button_text' yalign .5
                hovered mod.Tooltip("{urm_notl}Toggle watchpanel{/urm_notl}") unhovered mod.Tooltip()
                action ToggleField(mod.Settings, 'showWatchPanel', True, False)
            button: # Close
                style_suffix 'dialogCloseButton'
                yoffset 0
                hovered mod.Tooltip('{urm_notl}Close URM{/urm_notl}') unhovered mod.Tooltip()
                text 'x' size mod.scalePxInt(24) yalign .5 color mod.Theme.colors.errorBg
                action Hide('URM_main')

        vbox:
            xfill True
            # Header
            vbox:
                ysize mod.scalePxInt(46)
                align (0.5, 0.0)
                text "Universal Ren'Py Mod" style_suffix "header_text" yalign .5
            # File buttons
            hbox:
                xalign 1.0 spacing 2
                if mod.Tooltip.currentText:
                    text mod.Tooltip.currentText yalign 0.5
                else:
                    if mod.URMFiles.file.filename:
                        text 'Loaded: [mod.URMFiles.file.filename]' yalign 0.5
                        if mod.URMFiles.file.unsaved:
                            label "*" yalign 0.5
                    elif mod.URMFiles.file.unsaved:
                        label "{urm_notl}Unsaved{/urm_notl}" yalign 0.5
                null width mod.scalePxInt(10)
                textbutton "\ue24d" style_suffix "icon_button" hovered mod.Tooltip('New (Ctrl+N)') unhovered mod.Tooltip() action mod.URMFiles.Clear() # New
                textbutton "\ue2c7" style_suffix "icon_button" hovered mod.Tooltip('Open (Ctrl+O)') unhovered mod.Tooltip() action mod.URMFiles.Load() # Open
                textbutton "\ue161" style_suffix "icon_button" hovered mod.Tooltip('Save (Ctrl+S)') unhovered mod.Tooltip() action mod.URMFiles.Save() # Save
                null width mod.scalePxInt(10)

            null height mod.scalePxInt(10)
            frame style_suffix "seperator"
            hbox:
                # Tabs
                vbox:
                    use URM_tabbutton('{urm_notl}Search{/urm_notl}', '\ue880', 'search')
                    use URM_tabbutton('{urm_notl}Variables{/urm_notl}', '\uef54', 'variables')
                    use URM_tabbutton('{urm_notl}Snapshots{/urm_notl}', '\ue412', 'snapshots')
                    use URM_tabbutton('{urm_notl}Labels{/urm_notl}', '\ue54e', 'labels')
                    use URM_tabbutton('{urm_notl}Renaming{/urm_notl}', '\ue560', 'textrepl')
                    use URM_tabbutton('{urm_notl}Textboxes{/urm_notl}', '\ue0b7', 'textboxCustomizations')
                    use URM_tabbutton('{urm_notl}Gamesaves{/urm_notl}', '\ue161', 'gamesaves')
                    use URM_tabbutton('{urm_notl}Options{/urm_notl}', '\ue8b8', 'options')
                frame style_suffix "vseperator"
                null width mod.scalePxInt(10)
                # Content
                vbox:
                    null height mod.scalePxInt(10)

                    if mod.Settings.currentScreen == 'search':
                        use URM_search()
                    elif mod.Settings.currentScreen == 'variables':
                        use URM_variables()
                    elif mod.Settings.currentScreen == 'snapshots':
                        use URM_snapshots()
                    elif mod.Settings.currentScreen == 'labels':
                        use URM_labels()
                    elif mod.Settings.currentScreen == 'textrepl':
                        use URM_textrepl()
                    elif mod.Settings.currentScreen == 'textboxCustomizations':
                        use URM_textboxCustomizations()
                    elif mod.Settings.currentScreen == 'gamesaves':
                        use URM_gamesaves()
                    elif isinstance(mod.Settings.currentScreen, basestring) and mod.Settings.currentScreen.startswith('options'):
                        use URM_options_main(mod.Settings.currentScreen[8:])

# =========
# TABBUTTON
# =========
screen URM_tabbutton(title, icon, name):
    button:
        style_suffix 'tab'
        xsize mod.scalePxInt(100) ysize mod.scalePxInt(80)
        vbox:
            yalign .5 xalign .5
            text icon style_suffix 'icon_button_text' xalign .5 size mod.scalePxInt(38)
            null width 2
            label title xalign .5 text_size mod.scalePxInt(12)
        selected (isinstance(mod.Settings.currentScreen, basestring) and mod.Settings.currentScreen.startswith(name))
        action SetField(mod.Settings, 'currentScreen', name)
    frame style_suffix "seperator" xsize mod.scalePxInt(100) background mod.Theme.secondary

# =====================
# SPLASHSCREEN OVERRIDE
# =====================
label URM_splashscreen:
    $ del config.label_overrides['splashscreen']
    if not mod.Settings.skipSplashscreen and renpy.has_label('splashscreen'):
        call _splashscreen

    return

# =============================================================================
# Pages screen to use inside other screens (pass mod.Pages() object as argument)
# =============================================================================
screen URM_pages(pages):
    if pages.pageCount:
        textbutton "\ue5dc" style_suffix 'icon_button' sensitive (pages.currentPage>1) action SetField(pages, 'currentPage', 1) yalign .5 hovered mod.Tooltip('{urm_notl}Go to first page{/urm_notl}') unhovered mod.Tooltip()
        textbutton "\ue408" style_suffix 'icon_button' sensitive (pages.currentPage>1) action SetField(pages, 'currentPage', pages.currentPage-1) yalign .5 hovered mod.Tooltip('{urm_notl}Go to previous page{/urm_notl}') unhovered mod.Tooltip()

        for page in pages.pageRange:
            textbutton If(page<10, '0[page]', '[page]') sensitive (page != pages.currentPage) action SetField(pages, 'currentPage', page)

        textbutton "\ue409" style_suffix 'icon_button' sensitive (pages.currentPage<pages.pageCount) action SetField(pages, 'currentPage', pages.currentPage+1) yalign .5 hovered mod.Tooltip('{urm_notl}Go to next page{/urm_notl}') unhovered mod.Tooltip()
        textbutton "\ue5dd" style_suffix 'icon_button' sensitive (pages.currentPage<pages.pageCount) action SetField(pages, 'currentPage', pages.pageCount) yalign .5 hovered mod.Tooltip('{urm_notl}Go to last page{/urm_notl}') unhovered mod.Tooltip()
