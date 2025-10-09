
# ====================
# SETTINGS MAIN SCREEN
# ====================
screen URM_options_main(selectedOption=None):
    style_prefix "mod"
    default currentOption = selectedOption
    default buttonWidth = mod.scaleX(15)
    
    hbox:
        vbox spacing 2:
            use mod_iconButton('\ue7f4', '{urm_notl}Notifications{/urm_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_notifications'), xsize=buttonWidth)
            use mod_iconButton('\ue8f4', '{urm_notl}Watch panel{/urm_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_watchpanel'), xsize=buttonWidth)
            use mod_iconButton('\ue161', '{urm_notl}Gamesaves{/urm_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_gamesaves'), xsize=buttonWidth)
            use mod_iconButton('\ue5d2', '{urm_notl}Quickmenu{/urm_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_quickmenu'), xsize=buttonWidth)
            use mod_iconButton('\ue8b8', '{urm_notl}Miscellaneous{/urm_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_misc'), xsize=buttonWidth)
            use mod_iconButton('\ue40a', '{urm_notl}Appearance{/urm_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_appearance'), xsize=buttonWidth)

        null width 5
        frame style_suffix "vseperator" xsize mod.scalePxInt(2)
        null width 5

        vbox:
            xfill True yfill True

            if mod.Settings.currentScreen[8:] == 'notifications':
                use URM_options_notifications()
            elif mod.Settings.currentScreen[8:] == 'watchpanel':
                use URM_options_watchpanel()
            elif mod.Settings.currentScreen[8:] == 'gamesaves':
                use URM_options_gamesaves()
            elif mod.Settings.currentScreen[8:] == 'quickmenu':
                use URM_options_quickmenu()
            elif mod.Settings.currentScreen[8:] == 'misc':
                use URM_options_misc()
            elif mod.Settings.currentScreen[8:] == 'appearance':
                use URM_options_appearance()
            else:
                label '{urm_notl}Select an option on the left{/urm_notl}' align (.5,.05)

# =============
# NOTIFICATIONS
# =============
screen URM_options_notifications():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use URM_options_settings({
                'showReplayNotification': {
                    'title': '{urm_notl}Replay notification{/urm_notl}',
                    'description': """This option makes URM display a notification when you're in a replay\nand gives the option to quickly end it""",
                    'effective': If(mod.Settings.showReplayNotification, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                },
                'showChoicesNotification': {
                    'title': '{urm_notl}Choices notification{/urm_notl}',
                    'description': """This option makes URM display a notification when it detected choices\n\nThis notification also reports the number of hidden choices\nand gives quick access to more options regarding the choices\n\nYou can open the choices dialog by pressing Alt+C""",
                    'effective': If(mod.Settings.showChoicesNotification, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                },
                'showPathsNotification': {
                    'title': '{urm_notl}Paths notification{/urm_notl}',
                    'description': """This option makes URM display a notification when it detected a path/if-statement\nand gives quick access to more options/infor regarding the paths\n\nYou can open the choices dialog by pressing Alt+A""",
                    'effective': If(mod.Settings.showPathsNotification, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                },
                'stopSkippingOnPathDetection': {
                    'title': '{urm_notl}Stop skipping on path detection{/urm_notl}',
                    'description': """When you're skipping content and this option is enabled, skipping will be canceled on path detection""",
                    'effective': If(mod.Settings.stopSkippingOnPathDetection, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                },
                'notificationTimeout': {
                    'title': '{urm_notl}Time-out{/urm_notl}',
                    'description': """Automatically close the notification after this number of seconds""",
                    'effective': If(mod.Settings.notificationTimeout, '{urm_notl}[mod.Settings.notificationTimeout]s{/urm_notl}', '{urm_notl}Never{/urm_notl}'),
                    'options': {
                        '{urm_notl}Never{/urm_notl}': 0,
                        '{urm_notl}5s{/urm_notl}': 5,
                        '{urm_notl}10s{/urm_notl}': 10,
                    },
                },
            }, colWidth=[mod.scaleX(22),mod.scaleX(8),mod.scaleX(22),mod.scaleX(22)])

# ==========
# WATCHPANEL
# ==========
screen URM_options_watchpanel():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use URM_options_settings(mod.OrderedDict([
                ('showWatchPanel', {
                    'title': '{urm_notl}Enable watchpanel{/urm_notl}',
                    'effective': If(mod.Settings.showWatchPanel, '{urm_notl}Enabled{/urm_notl}', '{urm_notl}Disabled{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('watchpanelToggleKey', {
                    'title': '{urm_notl}Toggle using M-key{/urm_notl}',
                    'description': """Quickly open/close the watchpanel using this key""",
                    'effective': If(mod.Settings.watchpanelToggleKey, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': 'M',
                        '{urm_notl}Off{/urm_notl}': '',
                    },
                }),
                ('watchpanelHideToggleButton', {
                    'title': '{urm_notl}Hide togglebutton{/urm_notl}',
                    'description': """This removes the arrow button in the top corner\nNote: This only works when "Toggle using M-key" is enabled""",
                    'effective': If(mod.Settings.watchpanelHideToggleButton, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('watchPanelPos', {
                    'title': '{urm_notl}Panel position{/urm_notl}',
                    'effective': If(mod.Settings.watchPanelPos=='r', '{urm_notl}Right{/urm_notl}', '{urm_notl}Left{/urm_notl}'),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Left{/urm_notl}', 'l'),
                        ('{urm_notl}Right{/urm_notl}', 'r'),
                    ]),
                }),
                ('watchPanelFileLine', {
                    'title': '{urm_notl}Current file:line{/urm_notl}',
                    'description': 'Show the last ran file:line of code',
                    'effective': If(mod.Settings.watchPanelFileLine==2, '{urm_notl}Compact{/urm_notl}', If(mod.Settings.watchPanelFileLine==1, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}')),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Show{/urm_notl}', 1),
                        ('{urm_notl}Compact{/urm_notl}', 2),
                        ('{urm_notl}Hide{/urm_notl}', 0),
                    ]),
                }),
                ('watchPanelCurrentLabel', {
                    'title': '{urm_notl}Last seen label{/urm_notl}',
                    'description': 'Shows the current label we\'re in',
                    'effective': If(mod.Settings.watchPanelCurrentLabel==2, '{urm_notl}Compact{/urm_notl}', If(mod.Settings.watchPanelCurrentLabel==1, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}')),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Show{/urm_notl}', 1),
                        ('{urm_notl}Compact{/urm_notl}', 2),
                        ('{urm_notl}Hide{/urm_notl}', 0),
                    ]),
                }),
                ('watchPanelChoiceDetection', {
                    'title': '{urm_notl}Choice detection{/urm_notl}',
                    'description': '{urm_notl}Shows information about the current choice{/urm_notl}',
                    'effective': If(mod.Settings.watchPanelChoiceDetection==2, '{urm_notl}Compact{/urm_notl}', If(mod.Settings.watchPanelChoiceDetection==1, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}')),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Show{/urm_notl}', 1),
                        ('{urm_notl}Compact{/urm_notl}', 2),
                        ('{urm_notl}Hide{/urm_notl}', 0),
                    ]),
                }),
                ('watchPanelPathDetection', {
                    'title': '{urm_notl}Path detection{/urm_notl}',
                    'description': '{urm_notl}Shows information about a detected path{/urm_notl}',
                    'effective': If(mod.Settings.watchPanelPathDetection==2, '{urm_notl}Compact{/urm_notl}', If(mod.Settings.watchPanelPathDetection==1, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}')),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Show{/urm_notl}', 1),
                        ('{urm_notl}Compact{/urm_notl}', 2),
                        ('{urm_notl}Hide{/urm_notl}', 0),
                    ]),
                }),
                ('watchPanelProgress', {
                    'title': '{urm_notl}Progress{/urm_notl}',
                    'description': '{urm_notl}Shows how much of the content has been seen (in all playthroughs combined){/urm_notl}',
                    'effective': If(mod.Settings.watchPanelProgress==2, '{urm_notl}Compact{/urm_notl}', If(mod.Settings.watchPanelProgress==1, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}')),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Show{/urm_notl}', 1),
                        ('{urm_notl}Compact{/urm_notl}', 2),
                        ('{urm_notl}Hide{/urm_notl}', 0),
                    ]),
                }),
                ('watchPanelVars', {
                    'title': '{urm_notl}Watched variables{/urm_notl}',
                    'effective': If(mod.Settings.watchPanelVars==2, '{urm_notl}Compact{/urm_notl}', If(mod.Settings.watchPanelVars==1, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}')),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Show{/urm_notl}', 1),
                        ('{urm_notl}Compact{/urm_notl}', 2),
                        ('{urm_notl}Hide{/urm_notl}', 0),
                    ]),
                }),
            ]), colWidth=[mod.scaleX(16),mod.scaleX(9),mod.scaleX(25),mod.scaleX(25)])

# =========
# LOAD/SAVE
# =========
screen URM_options_gamesaves():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use URM_options_settings(mod.OrderedDict([
                ('askSaveName', {
                    'title': '{urm_notl}Ask name before saving{/urm_notl}',
                    'effective': If(mod.Settings.askSaveName, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('quickResumeSaveHotKey', {
                    'title': 'Save {b}quick resume{/b} with Alt+Q',
                    'effective': If(mod.Settings.quickResumeSaveHotKey, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('quickSaveHotKey', {
                    'title': '{b}Quick save{/b} with Alt+S',
                    'effective': If(mod.Settings.quickSaveHotKey, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('quickLoadHotKey', {
                    'title': 'Load last {b}quick save{/b} with Alt+L',
                    'effective': If(mod.Settings.quickLoadHotKey, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
            ]))

# ==================
# Quickmenu settings
# ==================
screen URM_options_quickmenu():
    style_prefix 'mod'
    default colWidth = [mod.scaleX(15),mod.scaleX(10),mod.scaleX(25),mod.scaleX(25)]

    vbox yfill True:
        vbox yoffset 20:
            use URM_options_settings(mod.OrderedDict([
                ('quickmenuEnabled', {
                    'title': '{urm_notl}Quickmenu{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuEnabled, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('quickmenuAlignX', {
                    'title': '{urm_notl}Horizontal alignment{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuAlignX==0, '{urm_notl}Left{/urm_notl}', If(mod.Settings.quickmenuAlignX==.5, '{urm_notl}Center{/urm_notl}', '{urm_notl}Right{/urm_notl}')),
                    'options': {
                        '{urm_notl}Left{/urm_notl}': 0.0,
                        '{urm_notl}Center{/urm_notl}': 0.5,
                        '{urm_notl}Right{/urm_notl}': 1.0,
                    },
                }),
                ('quickmenuAlignY', {
                    'title': '{urm_notl}Vertical alignment{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuAlignY==0, '{urm_notl}Top{/urm_notl}', If(mod.Settings.quickmenuAlignY==.5, '{urm_notl}Middle{/urm_notl}', '{urm_notl}Bottom{/urm_notl}')),
                    'options': {
                        '{urm_notl}Top{/urm_notl}': 0.0,
                        '{urm_notl}Middle{/urm_notl}': 0.5,
                        '{urm_notl}Bottom{/urm_notl}': 1.0,
                    },
                }),
                ('quickmenuVertical', {
                    'title': '{urm_notl}Orientation{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuVertical, '{urm_notl}Vertical{/urm_notl}', '{urm_notl}Horizontal{/urm_notl}'),
                    'options': {
                        '{urm_notl}Vertical{/urm_notl}': True,
                        '{urm_notl}Horizontal{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnBack', {
                    'title': '{urm_notl}{b}Button:{/b} Back{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnBack, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnSkip', {
                    'title': '{urm_notl}{b}Button:{/b} Skip{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnSkip, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnAuto', {
                    'title': '{urm_notl}{b}Button:{/b} Auto{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnAuto, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnQuicksave', {
                    'title': '{urm_notl}{b}Button:{/b} Quicksave{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnQuicksave, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnSave', {
                    'title': '{urm_notl}{b}Button:{/b} Save{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnSave, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnQuickload', {
                    'title': '{urm_notl}{b}Button:{/b} Quickload{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnQuickload, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnLoad', {
                    'title': '{urm_notl}{b}Button:{/b} Load{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnLoad, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnMenu', {
                    'title': '{urm_notl}{b}Button:{/b} Menu{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnMenu, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnMods', {
                    'title': '{urm_notl}{b}Button:{/b} Mods{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnMods, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnUrm', {
                    'title': '{urm_notl}{b}Button:{/b} URM{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnUrm, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuBtnExit', {
                    'title': '{urm_notl}{b}Button:{/b} Exit{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuBtnExit, '{urm_notl}Show{/urm_notl}', '{urm_notl}Hide{/urm_notl}'),
                    'options': {
                        '{urm_notl}Show{/urm_notl}': True,
                        '{urm_notl}Hide{/urm_notl}': False,
                    },
                }),
                ('quickmenuAutoHide', {
                    'title': '{urm_notl}Auto hide{/urm_notl}',
                    'description': 'Only show the quickmenu when you hover the area',
                    'effective': If(mod.Settings.quickmenuAutoHide, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('quickmenuStyle', {
                    'title': '{urm_notl}Style{/urm_notl}',
                    'effective': If(mod.Settings.quickmenuStyle=='buttons', '{urm_notl}Buttons{/urm_notl}', If(mod.Settings.quickmenuStyle=='iconbuttons', '{urm_notl}Iconbuttons{/urm_notl}', If(mod.Settings.quickmenuStyle=='icons', '{urm_notl}Icons{/urm_notl}', '{urm_notl}Default{/urm_notl}'))),
                    'options': mod.OrderedDict([
                        ('{urm_notl}Default{/urm_notl}', 'default'),
                        ('{urm_notl}Buttons{/urm_notl}', 'buttons'),
                        ('{urm_notl}Iconbuttons{/urm_notl}', 'iconbuttons'),
                        ('{urm_notl}Icons{/urm_notl}', 'icons'),
                    ]),
                }),
            ]), colWidth)

# =============
# MISCELLANEOUS
# =============
screen URM_options_misc():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use URM_options_settings(mod.OrderedDict([
                ('consoleHotKey', {
                    'title': '{urm_notl}Open console with Alt+O{/urm_notl}',
                    'description': """Open the Ren'Py console. Even when it's disabled in the Ren'Py config""",
                    'effective': If(mod.Settings.consoleHotKey, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('skipSplashscreen', {
                    'title': '{urm_notl}Skip splashscreen{/urm_notl}',
                    'description': """This option skips the splashscreen at the start of the game (if any) and takes you directly to the menu""",
                    'effective': If(mod.Settings.skipSplashscreen, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('codeViewShowAll', {
                    'title': '{urm_notl}Show all code in the codeview{/urm_notl}',
                    'description': """When this option is turned off, all less relevant code is hidden in choice/path detection\nStuff like \"renpy.pause()\" and \"renpy.play('someaudio.mp3')\"""",
                    'effective': If(mod.Settings.codeViewShowAll, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('progressShown', {
                    'title': '{urm_notl}Show progressbar{/urm_notl}',
                    'description': "Shows a draggable progressbar, this bar shows how much of the dialogue has been seen (in all playthroughs combined)",
                    'effective': If(mod.Settings.progressShown, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
                ('progressShowNew', {
                    'title': '{urm_notl}Show progressbar newly seen{/urm_notl}',
                    'description': "Show the amount of dialogue that has been seen for the first time during the current session in the progressbar",
                    'effective': If(mod.Settings.progressShowNew, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),                
                ('touchEnabled', { # We only show this option on non-touch devices
                    'title': '{urm_notl}Enable touch control{/urm_notl}',
                    'description': """This will show a gear logo on screen that you can drag around and click to open URM\n{size=-6}{alpha=.9}When you disable this on a touch device, you're still able to open URM by drawing an U on screen (down-right-up){/alpha}{/size}""",
                    'effective': If(mod.Settings.touchEnabled, '{urm_notl}On{/urm_notl}', '{urm_notl}Off{/urm_notl}'),
                    'options': {
                        '{urm_notl}On{/urm_notl}': True,
                        '{urm_notl}Off{/urm_notl}': False,
                    },
                }),
            ]))

# ==========
# APPEARANCE
# ==========
screen URM_options_appearance():
    style_prefix 'mod'
    default colWidth = [mod.scaleX(15),mod.scaleX(10),mod.scaleX(20),mod.scaleX(20)]

    vbox:
        use URM_tableRow():
            hbox xsize colWidth[0]:
                hbox:
                    label '{urm_notl}Setting{/urm_notl}'
                    textbutton '\uf1c0' yoffset -mod.scalePxInt(4) style_suffix 'icon_textbutton' action mod.Confirm("""There are 2 settings levels:\n{b}Local{/b}: The setting for the current game\n{b}Global{/b}: The setting for all games (that don't have a local setting)\n\nThe value under {b}Effective{/b} is the setting used in the current game""", title='Settings explanation')
            hbox xsize colWidth[1]:
                label '{urm_notl}Effective{/urm_notl}'
            hbox xsize colWidth[2]:
                label '{urm_notl}Local{/urm_notl}'
            hbox xsize colWidth[3]:
                hbox:
                    label '{urm_notl}Global{/urm_notl}'
                    if mod.Settings.globalAvailable == False:
                        textbutton '\uf1c0' yoffset -mod.scalePxInt(4) text_color mod.Theme.colors.errorText style_suffix 'icon_textbutton' action mod.Confirm('Global settings are unavailable in this game', title='{urm_notl}Global settings unavailable{/urm_notl}')

        use URM_table(spacing=mod.scalePxInt(10)):
            use URM_tableRow(0, True):
                hbox xsize colWidth[0]:
                    text '{urm_notl}Transparency{/urm_notl}'
                hbox xsize colWidth[1]:
                    text str(int(mod.Settings.themeTransparency*100))+'%'
                vbox xsize colWidth[2] spacing mod.scalePxInt(10):
                    hbox spacing mod.scalePxInt(10):
                        textbutton '0%' action mod.SetDialogTransparency(0, globalSetting=False)
                        textbutton '10%' action mod.SetDialogTransparency(0.1, globalSetting=False)
                        textbutton '20%' action mod.SetDialogTransparency(0.2, globalSetting=False)
                        textbutton '30%' action mod.SetDialogTransparency(0.3, globalSetting=False)
                        textbutton '40%' action mod.SetDialogTransparency(0.4, globalSetting=False)
                    hbox spacing mod.scalePxInt(10):
                        textbutton '5%' action mod.SetDialogTransparency(0.05, globalSetting=False)
                        textbutton '15%' action mod.SetDialogTransparency(0.15, globalSetting=False)
                        textbutton '25%' action mod.SetDialogTransparency(0.25, globalSetting=False)
                        textbutton '35%' action mod.SetDialogTransparency(0.35, globalSetting=False)
                        textbutton '45%' action mod.SetDialogTransparency(0.45, globalSetting=False)
                    use mod_iconButton('\ue872', '{urm_notl}Clear{/urm_notl}', mod.SetDialogTransparency(None, globalSetting=False), sensitive=(mod.Settings.get('themeTransparency', globalSetting=False)!=None))
                vbox xsize colWidth[3] spacing mod.scalePxInt(10):
                    hbox spacing mod.scalePxInt(10):
                        textbutton '0%' action mod.SetDialogTransparency(0, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '10%' action mod.SetDialogTransparency(0.1, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '20%' action mod.SetDialogTransparency(0.2, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '30%' action mod.SetDialogTransparency(0.3, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '40%' action mod.SetDialogTransparency(0.4, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                    hbox spacing mod.scalePxInt(10):
                        textbutton '5%' action mod.SetDialogTransparency(0.05, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '15%' action mod.SetDialogTransparency(0.15, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '25%' action mod.SetDialogTransparency(0.25, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '35%' action mod.SetDialogTransparency(0.35, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                        textbutton '45%' action mod.SetDialogTransparency(0.45, globalSetting=True) sensitive If(mod.Settings.globalAvailable, None, False)
                    use mod_iconButton('\ue872', '{urm_notl}Default{/urm_notl}', mod.SetDialogTransparency(None, globalSetting=True), sensitive=If(mod.Settings.globalAvailable, None, False))

            use URM_tableRow(1, True):
                hbox xsize colWidth[0]:
                    text '{urm_notl}Theme{/urm_notl}'
                hbox xsize colWidth[1]:
                    text '[mod.Settings.theme]'
                vbox xsize colWidth[2] spacing mod.scalePxInt(10):
                    for name in mod.availableThemes:
                        use URM_options_themeOption(name, globalSetting=False)
                    use mod_iconButton('\ue872', '{urm_notl}Clear{/urm_notl}', mod.SetTheme(None, globalSetting=False), sensitive=(mod.Settings.get('theme', globalSetting=False)!=None))
                vbox xsize colWidth[3] spacing mod.scalePxInt(10):
                    for name in mod.availableThemes:
                        use URM_options_themeOption(name, globalSetting=True)

screen URM_options_themeOption(themeName, globalSetting=None):
    style_prefix 'mod'
    hbox:
        spacing mod.scalePxInt(10)
        frame:
            background mod.Theme.getButtonBg(mod.availableThemes[themeName]['background'], mod.availableThemes[themeName]['text'])
            ysize mod.scalePxInt(36)
            yalign .5
            hbox:
                spacing mod.scalePxInt(10)
                frame:
                    background mod.Theme.getButtonBg(mod.availableThemes[themeName]['primary'], mod.availableThemes[themeName]['text'])
                    xsize mod.scalePxInt(28)
                frame:
                    background mod.Theme.getButtonBg(mod.availableThemes[themeName]['secondary'], mod.availableThemes[themeName]['text'])
                    xsize mod.scalePxInt(28)
                frame:
                    background mod.Theme.getButtonBg(mod.availableThemes[themeName]['tertiary'], mod.availableThemes[themeName]['text'])
                    xsize mod.scalePxInt(28)
        use mod_radiobutton(mod.Settings.get('theme', globalSetting)==themeName, themeName, mod.SetTheme(themeName, globalSetting), sensitive=If(not globalSetting or mod.Settings.globalAvailable, None, False))

# ======================
# CREATE A SETTINGS GRID
# ======================
screen URM_options_settings(settings, colWidth=[mod.scaleX(25),mod.scaleX(10),mod.scaleX(20),mod.scaleX(20)]):
    style_prefix 'mod'

    use URM_tableRow():
        hbox xsize colWidth[0]:
            hbox:
                label '{urm_notl}Setting{/urm_notl}'
                textbutton '\uf1c0' yoffset -mod.scalePxInt(4) style_suffix 'icon_textbutton' action mod.Confirm("""There are 2 settings levels:\n{b}Local{/b}: The setting for the current game\n{b}Global{/b}: The setting for all games (that don't have a local setting)\n\nThe value under {b}Effective{/b} is the setting used in the current game""", title='Settings explanation')
        hbox xsize colWidth[1]:
            label '{urm_notl}Effective{/urm_notl}'
        hbox xsize colWidth[2]:
            label '{urm_notl}Local{/urm_notl}'
        hbox xsize colWidth[3]:
            hbox:
                label '{urm_notl}Global{/urm_notl}'
                if mod.Settings.globalAvailable == False:
                    textbutton '\uf1c0' yoffset -mod.scalePxInt(4) text_color mod.Theme.colors.errorText style_suffix 'icon_textbutton' action mod.Confirm('Global settings are unavailable in this game', title='{urm_notl}Global settings unavailable{/urm_notl}')

    use URM_table():
        for i,(settingName,setting) in enumerate(settings.items()):
            use URM_tableRow(i, True):
                hbox xsize colWidth[0] yalign .5:
                    hbox yalign .5 spacing 2:
                        text setting['title'] yalign .5
                        if 'description' in setting:
                            textbutton '{size=-8}\uf1c0{/size}' style_suffix 'icon_textbutton' action mod.Confirm(setting['description'], title=setting['title'])
                hbox xsize colWidth[1] yalign .5:
                    text setting['effective']
                hbox xsize colWidth[2]:
                    hbox spacing 2 box_wrap True:
                        for option in setting['options']:
                            use mod_radiobutton(mod.Settings.get(settingName, globalSetting=False)==setting['options'][option], option, mod.SetURMSetting(settingName, setting['options'][option]))
                        use mod_iconButton('\ue872', '{urm_notl}Clear{/urm_notl}', mod.SetURMSetting(settingName, None), sensitive=(mod.Settings.get(settingName, globalSetting=False)!=None))
                hbox xsize colWidth[3]:
                    hbox spacing 2 box_wrap True:
                        for option in setting['options']:
                            use mod_radiobutton(mod.Settings.get(settingName, globalSetting=True)==setting['options'][option], option, mod.SetURMSetting(settingName, setting['options'][option], globalSetting=True), sensitive=If(mod.Settings.globalAvailable, None, False))
                        use mod_iconButton('\ue872', '{urm_notl}Default{/urm_notl}', mod.SetURMSetting(settingName, None, globalSetting=True), sensitive=If(mod.Settings.globalAvailable, None, False))
