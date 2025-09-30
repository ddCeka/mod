
# ====================
# SETTINGS MAIN SCREEN
# ====================
screen mod_options_main(selectedOption=None):
    style_prefix "mod"
    default currentOption = selectedOption
    default buttonWidth = mod.scaleX(15)
    
    hbox:
        vbox spacing 2:
            use mod_iconButton('\ue7f4', '{mod_notl}Notifications{/mod_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_notifications'), xsize=buttonWidth)
            use mod_iconButton('\ue8f4', '{mod_notl}Watch panel{/mod_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_watchpanel'), xsize=buttonWidth)
            use mod_iconButton('\ue161', '{mod_notl}Gamesaves{/mod_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_gamesaves'), xsize=buttonWidth)
            use mod_iconButton('\ue5d2', '{mod_notl}Quickmenu{/mod_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_quickmenu'), xsize=buttonWidth)
            use mod_iconButton('\ue8b8', '{mod_notl}Miscellaneous{/mod_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_misc'), xsize=buttonWidth)
            use mod_iconButton('\ue40a', '{mod_notl}Appearance{/mod_notl}', action=SetField(mod.Settings, 'currentScreen', 'options_appearance'), xsize=buttonWidth)

        null width 5
        frame style_suffix "vseparator" xsize mod.scalePxInt(2)
        null width 5

        vbox:
            xfill True yfill True

            # if renpy.has_screen('mod_options_{}'.format(mod.Settings.currentScreen[8:])):
            #     use expression 'mod_options_{}'.format(mod.Settings.currentScreen[8:]) # THIS IS NOT AVAILABLE IN OLDER RENPY VERSIONS
            if mod.Settings.currentScreen[8:] == 'notifications':
                use mod_options_notifications()
            elif mod.Settings.currentScreen[8:] == 'watchpanel':
                use mod_options_watchpanel()
            elif mod.Settings.currentScreen[8:] == 'gamesaves':
                use mod_options_gamesaves()
            elif mod.Settings.currentScreen[8:] == 'quickmenu':
                use mod_options_quickmenu()
            elif mod.Settings.currentScreen[8:] == 'misc':
                use mod_options_misc()
            elif mod.Settings.currentScreen[8:] == 'appearance':
                use mod_options_appearance()
            else:
                label '{mod_notl}Select an option on the left{/mod_notl}' align (.5,.05)

# =============
# NOTIFICATIONS
# =============
screen mod_options_notifications():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings({
                'showReplayNotification': {
                    'title': '{mod_notl}Replay notification{/mod_notl}',
                    'description': """This option makes mod display a notification when you're in a replay\nand gives the option to quickly end it""",
                    'effective': If(mod.Settings.showReplayNotification, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                },
                'showChoicesNotification': {
                    'title': '{mod_notl}Choices notification{/mod_notl}',
                    'description': """This option makes mod display a notification when it detected choices\n\nThis notification also reports the number of hidden choices\nand gives quick access to more options regarding the choices\n\nYou can open the choices dialog by pressing Alt+C""",
                    'effective': If(mod.Settings.showChoicesNotification, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                },
                'showPathsNotification': {
                    'title': '{mod_notl}Paths notification{/mod_notl}',
                    'description': """This option makes mod display a notification when it detected a path/if-statement\nand gives quick access to more options/infor regarding the paths\n\nYou can open the choices dialog by pressing Alt+A""",
                    'effective': If(mod.Settings.showPathsNotification, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                },
                'stopSkippingOnPathDetection': {
                    'title': '{mod_notl}Stop skipping on path detection{/mod_notl}',
                    'description': """When you're skipping content and this option is enabled, skipping will be canceled on path detection""",
                    'effective': If(mod.Settings.stopSkippingOnPathDetection, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                },
                'notificationTimeout': {
                    'title': '{mod_notl}Time-out{/mod_notl}',
                    'description': """Automatically close the notification after this number of seconds""",
                    'effective': If(mod.Settings.notificationTimeout, '{mod_notl}[mod.Settings.notificationTimeout]s{/mod_notl}', '{mod_notl}Never{/mod_notl}'),
                    'options': {
                        '{mod_notl}Never{/mod_notl}': 0,
                        '{mod_notl}5s{/mod_notl}': 5,
                        '{mod_notl}10s{/mod_notl}': 10,
                    },
                },
            }, colWidth=[mod.scaleX(22),mod.scaleX(8),mod.scaleX(22),mod.scaleX(22)])

# ==========
# WATCHPANEL
# ==========
screen mod_options_watchpanel():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(mod.OrderedDict([
                ('showWatchPanel', {
                    'title': '{mod_notl}Enable watchpanel{/mod_notl}',
                    'effective': If(mod.Settings.showWatchPanel, '{mod_notl}Enabled{/mod_notl}', '{mod_notl}Disabled{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('watchpanelToggleKey', {
                    'title': '{mod_notl}Toggle using M-key{/mod_notl}',
                    'description': """Quickly open/close the watchpanel using this key""",
                    'effective': If(mod.Settings.watchpanelToggleKey, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': 'M',
                        '{mod_notl}Off{/mod_notl}': '',
                    },
                }),
                ('watchpanelHideToggleButton', {
                    'title': '{mod_notl}Hide togglebutton{/mod_notl}',
                    'description': """This removes the arrow button in the top corner\nNote: This only works when "Toggle using M-key" is enabled""",
                    'effective': If(mod.Settings.watchpanelHideToggleButton, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('watchPanelPos', {
                    'title': '{mod_notl}Panel position{/mod_notl}',
                    'effective': If(mod.Settings.watchPanelPos=='r', '{mod_notl}Right{/mod_notl}', '{mod_notl}Left{/mod_notl}'),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Left{/mod_notl}', 'l'),
                        ('{mod_notl}Right{/mod_notl}', 'r'),
                    ]),
                }),
                ('watchPanelFileLine', {
                    'title': '{mod_notl}Current file:line{/mod_notl}',
                    'description': 'Show the last ran file:line of code',
                    'effective': If(mod.Settings.watchPanelFileLine==2, '{mod_notl}Compact{/mod_notl}', If(mod.Settings.watchPanelFileLine==1, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}')),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Show{/mod_notl}', 1),
                        ('{mod_notl}Compact{/mod_notl}', 2),
                        ('{mod_notl}Hide{/mod_notl}', 0),
                    ]),
                }),
                ('watchPanelCurrentLabel', {
                    'title': '{mod_notl}Last seen label{/mod_notl}',
                    'description': 'Shows the current label we\'re in',
                    'effective': If(mod.Settings.watchPanelCurrentLabel==2, '{mod_notl}Compact{/mod_notl}', If(mod.Settings.watchPanelCurrentLabel==1, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}')),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Show{/mod_notl}', 1),
                        ('{mod_notl}Compact{/mod_notl}', 2),
                        ('{mod_notl}Hide{/mod_notl}', 0),
                    ]),
                }),
                ('watchPanelChoiceDetection', {
                    'title': '{mod_notl}Choice detection{/mod_notl}',
                    'description': '{mod_notl}Shows information about the current choice{/mod_notl}',
                    'effective': If(mod.Settings.watchPanelChoiceDetection==2, '{mod_notl}Compact{/mod_notl}', If(mod.Settings.watchPanelChoiceDetection==1, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}')),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Show{/mod_notl}', 1),
                        ('{mod_notl}Compact{/mod_notl}', 2),
                        ('{mod_notl}Hide{/mod_notl}', 0),
                    ]),
                }),
                ('watchPanelPathDetection', {
                    'title': '{mod_notl}Path detection{/mod_notl}',
                    'description': '{mod_notl}Shows information about a detected path{/mod_notl}',
                    'effective': If(mod.Settings.watchPanelPathDetection==2, '{mod_notl}Compact{/mod_notl}', If(mod.Settings.watchPanelPathDetection==1, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}')),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Show{/mod_notl}', 1),
                        ('{mod_notl}Compact{/mod_notl}', 2),
                        ('{mod_notl}Hide{/mod_notl}', 0),
                    ]),
                }),
                ('watchPanelProgress', {
                    'title': '{mod_notl}Progress{/mod_notl}',
                    'description': '{mod_notl}Shows how much of the content has been seen (in all playthroughs combined){/mod_notl}',
                    'effective': If(mod.Settings.watchPanelProgress==2, '{mod_notl}Compact{/mod_notl}', If(mod.Settings.watchPanelProgress==1, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}')),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Show{/mod_notl}', 1),
                        ('{mod_notl}Compact{/mod_notl}', 2),
                        ('{mod_notl}Hide{/mod_notl}', 0),
                    ]),
                }),
                ('watchPanelVars', {
                    'title': '{mod_notl}Watched variables{/mod_notl}',
                    'effective': If(mod.Settings.watchPanelVars==2, '{mod_notl}Compact{/mod_notl}', If(mod.Settings.watchPanelVars==1, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}')),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Show{/mod_notl}', 1),
                        ('{mod_notl}Compact{/mod_notl}', 2),
                        ('{mod_notl}Hide{/mod_notl}', 0),
                    ]),
                }),
            ]), colWidth=[mod.scaleX(16),mod.scaleX(9),mod.scaleX(25),mod.scaleX(25)])

# =========
# LOAD/SAVE
# =========
screen mod_options_gamesaves():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(mod.OrderedDict([
                ('askSaveName', {
                    'title': '{mod_notl}Ask name before saving{/mod_notl}',
                    'effective': If(mod.Settings.askSaveName, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('quickResumeSaveHotKey', {
                    'title': 'Save {b}quick resume{/b} with Alt+Q',
                    'effective': If(mod.Settings.quickResumeSaveHotKey, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('quickSaveHotKey', {
                    'title': '{b}Quick save{/b} with Alt+S',
                    'effective': If(mod.Settings.quickSaveHotKey, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('quickLoadHotKey', {
                    'title': 'Load last {b}quick save{/b} with Alt+L',
                    'effective': If(mod.Settings.quickLoadHotKey, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
            ]))

# ==================
# Quickmenu settings
# ==================
screen mod_options_quickmenu():
    style_prefix 'mod'
    default colWidth = [mod.scaleX(15),mod.scaleX(10),mod.scaleX(25),mod.scaleX(25)]

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(mod.OrderedDict([
                ('quickmenuEnabled', {
                    'title': '{mod_notl}Quickmenu{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuEnabled, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('quickmenuAlignX', {
                    'title': '{mod_notl}Horizontal alignment{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuAlignX==0, '{mod_notl}Left{/mod_notl}', If(mod.Settings.quickmenuAlignX==.5, '{mod_notl}Center{/mod_notl}', '{mod_notl}Right{/mod_notl}')),
                    'options': {
                        '{mod_notl}Left{/mod_notl}': 0.0,
                        '{mod_notl}Center{/mod_notl}': 0.5,
                        '{mod_notl}Right{/mod_notl}': 1.0,
                    },
                }),
                ('quickmenuAlignY', {
                    'title': '{mod_notl}Vertical alignment{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuAlignY==0, '{mod_notl}Top{/mod_notl}', If(mod.Settings.quickmenuAlignY==.5, '{mod_notl}Middle{/mod_notl}', '{mod_notl}Bottom{/mod_notl}')),
                    'options': {
                        '{mod_notl}Top{/mod_notl}': 0.0,
                        '{mod_notl}Middle{/mod_notl}': 0.5,
                        '{mod_notl}Bottom{/mod_notl}': 1.0,
                    },
                }),
                ('quickmenuVertical', {
                    'title': '{mod_notl}Orientation{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuVertical, '{mod_notl}Vertical{/mod_notl}', '{mod_notl}Horizontal{/mod_notl}'),
                    'options': {
                        '{mod_notl}Vertical{/mod_notl}': True,
                        '{mod_notl}Horizontal{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnBack', {
                    'title': '{mod_notl}{b}Button:{/b} Back{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnBack, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnSkip', {
                    'title': '{mod_notl}{b}Button:{/b} Skip{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnSkip, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnAuto', {
                    'title': '{mod_notl}{b}Button:{/b} Auto{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnAuto, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnQuicksave', {
                    'title': '{mod_notl}{b}Button:{/b} Quicksave{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnQuicksave, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnSave', {
                    'title': '{mod_notl}{b}Button:{/b} Save{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnSave, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnQuickload', {
                    'title': '{mod_notl}{b}Button:{/b} Quickload{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnQuickload, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnLoad', {
                    'title': '{mod_notl}{b}Button:{/b} Load{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnLoad, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnMenu', {
                    'title': '{mod_notl}{b}Button:{/b} Menu{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnMenu, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnAddon', {
                    'title': '{mod_notl}{b}Button:{/b} Mods{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnAddon, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnMod', {
                    'title': '{mod_notl}{b}Button:{/b} mod{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnMod, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuBtnExit', {
                    'title': '{mod_notl}{b}Button:{/b} Exit{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuBtnExit, '{mod_notl}Show{/mod_notl}', '{mod_notl}Hide{/mod_notl}'),
                    'options': {
                        '{mod_notl}Show{/mod_notl}': True,
                        '{mod_notl}Hide{/mod_notl}': False,
                    },
                }),
                ('quickmenuAutoHide', {
                    'title': '{mod_notl}Auto hide{/mod_notl}',
                    'description': 'Only show the quickmenu when you hover the area',
                    'effective': If(mod.Settings.quickmenuAutoHide, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('quickmenuStyle', {
                    'title': '{mod_notl}Style{/mod_notl}',
                    'effective': If(mod.Settings.quickmenuStyle=='buttons', '{mod_notl}Buttons{/mod_notl}', If(mod.Settings.quickmenuStyle=='iconbuttons', '{mod_notl}Iconbuttons{/mod_notl}', If(mod.Settings.quickmenuStyle=='icons', '{mod_notl}Icons{/mod_notl}', '{mod_notl}Default{/mod_notl}'))),
                    'options': mod.OrderedDict([
                        ('{mod_notl}Default{/mod_notl}', 'default'),
                        ('{mod_notl}Buttons{/mod_notl}', 'buttons'),
                        ('{mod_notl}Iconbuttons{/mod_notl}', 'iconbuttons'),
                        ('{mod_notl}Icons{/mod_notl}', 'icons'),
                    ]),
                }),
            ]), colWidth)

# =============
# MISCELLANEOUS
# =============
screen mod_options_misc():
    style_prefix 'mod'

    vbox yfill True:
        vbox yoffset 20:
            use mod_options_settings(mod.OrderedDict([
                ('consoleHotKey', {
                    'title': '{mod_notl}Open console with Alt+O{/mod_notl}',
                    'description': """Open the Ren'Py console. Even when it's disabled in the Ren'Py config""",
                    'effective': If(mod.Settings.consoleHotKey, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('skipSplashscreen', {
                    'title': '{mod_notl}Skip splashscreen{/mod_notl}',
                    'description': """This option skips the splashscreen at the start of the game (if any) and takes you directly to the menu""",
                    'effective': If(mod.Settings.skipSplashscreen, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('codeViewShowAll', {
                    'title': '{mod_notl}Show all code in the codeview{/mod_notl}',
                    'description': """When this option is turned off, all less relevant code is hidden in choice/path detection\nStuff like \"renpy.pause()\" and \"renpy.play('someaudio.mp3')\"""",
                    'effective': If(mod.Settings.codeViewShowAll, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('progressShown', {
                    'title': '{mod_notl}Show progressbar{/mod_notl}',
                    'description': "Shows a draggable progressbar, this bar shows how much of the dialogue has been seen (in all playthroughs combined)",
                    'effective': If(mod.Settings.progressShown, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('progressShowNew', {
                    'title': '{mod_notl}Show progressbar newly seen{/mod_notl}',
                    'description': "Show the amount of dialogue that has been seen for the first time during the current session in the progressbar",
                    'effective': If(mod.Settings.progressShowNew, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
                ('touchEnabled', {
                    'title': '{mod_notl}Enable touch control{/mod_notl}',
                    'description': """This will show a Gear logo on screen that you can drag around and click to open mod\n{size=-6}{alpha=.9}When you disable this on a touch device, you're still able to open mod by drawing an U on screen (down-right-up){/alpha}{/size}""",
                    'effective': If(mod.Settings.touchEnabled, '{mod_notl}On{/mod_notl}', '{mod_notl}Off{/mod_notl}'),
                    'options': {
                        '{mod_notl}On{/mod_notl}': True,
                        '{mod_notl}Off{/mod_notl}': False,
                    },
                }),
            ]))

# ==========
# APPEARANCE
# ==========
screen mod_options_appearance():
    style_prefix 'mod'
    default colWidth = [mod.scaleX(15),mod.scaleX(10),mod.scaleX(20),mod.scaleX(20)]

    vbox:
        use mod_tableRow():
            hbox xsize colWidth[0]:
                hbox:
                    label '{mod_notl}Setting{/mod_notl}'
                    textbutton '\uf1c0' yoffset -mod.scalePxInt(4) style_suffix 'icon_textbutton' action mod.Confirm("""There are 2 settings levels:\n{b}Local{/b}: The setting for the current game\n{b}Global{/b}: The setting for all games (that don't have a local setting)\n\nThe value under {b}Effective{/b} is the setting used in the current game""", title='Settings explanation')
            hbox xsize colWidth[1]:
                label '{mod_notl}Effective{/mod_notl}'
            hbox xsize colWidth[2]:
                label '{mod_notl}Local{/mod_notl}'
            hbox xsize colWidth[3]:
                hbox:
                    label '{mod_notl}Global{/mod_notl}'
                    if mod.Settings.globalAvailable == False:
                        textbutton '\uf1c0' yoffset -mod.scalePxInt(4) text_color mod.Theme.colors.errorText style_suffix 'icon_textbutton' action mod.Confirm('Global settings are unavailable in this game', title='{mod_notl}Global settings unavailable{/mod_notl}')

        use mod_table(spacing=mod.scalePxInt(10)):
            use mod_tableRow(0, True):
                hbox xsize colWidth[0]:
                    text '{mod_notl}Transparency{/mod_notl}'
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
                    use mod_iconButton('\ue872', '{mod_notl}Clear{/mod_notl}', mod.SetDialogTransparency(None, globalSetting=False), sensitive=(mod.Settings.get('themeTransparency', globalSetting=False)!=None))
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
                    use mod_iconButton('\ue872', '{mod_notl}Default{/mod_notl}', mod.SetDialogTransparency(None, globalSetting=True), sensitive=If(mod.Settings.globalAvailable, None, False))

            use mod_tableRow(1, True):
                hbox xsize colWidth[0]:
                    text '{mod_notl}Theme{/mod_notl}'
                hbox xsize colWidth[1]:
                    text '[mod.Settings.theme]'
                vbox xsize colWidth[2] spacing mod.scalePxInt(10):
                    for name in mod.availableThemes:
                        use mod_options_themeOption(name, globalSetting=False)
                    use mod_iconButton('\ue872', '{mod_notl}Clear{/mod_notl}', mod.SetTheme(None, globalSetting=False), sensitive=(mod.Settings.get('theme', globalSetting=False)!=None))
                vbox xsize colWidth[3] spacing mod.scalePxInt(10):
                    for name in mod.availableThemes:
                        use mod_options_themeOption(name, globalSetting=True)


screen mod_options_themeOption(themeName, globalSetting=None):
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
screen mod_options_settings(settings, colWidth=[mod.scaleX(25),mod.scaleX(10),mod.scaleX(20),mod.scaleX(20)]):
    style_prefix 'mod'

    use mod_tableRow():
        hbox xsize colWidth[0]:
            hbox:
                label '{mod_notl}Setting{/mod_notl}'
                textbutton '\uf1c0' yoffset -mod.scalePxInt(4) style_suffix 'icon_textbutton' action mod.Confirm("""There are 2 settings levels:\n{b}Local{/b}: The setting for the current game\n{b}Global{/b}: The setting for all games (that don't have a local setting)\n\nThe value under {b}Effective{/b} is the setting used in the current game""", title='Settings explanation')
        hbox xsize colWidth[1]:
            label '{mod_notl}Effective{/mod_notl}'
        hbox xsize colWidth[2]:
            label '{mod_notl}Local{/mod_notl}'
        hbox xsize colWidth[3]:
            hbox:
                label '{mod_notl}Global{/mod_notl}'
                if mod.Settings.globalAvailable == False:
                    textbutton '\uf1c0' yoffset -mod.scalePxInt(4) text_color mod.Theme.colors.errorText style_suffix 'icon_textbutton' action mod.Confirm('Global settings are unavailable in this game', title='{mod_notl}Global settings unavailable{/mod_notl}')

    use mod_table():
        for i,(settingName,setting) in enumerate(settings.items()):
            use mod_tableRow(i, True):
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
                            use mod_radiobutton(mod.Settings.get(settingName, globalSetting=False)==setting['options'][option], option, mod.SetmodSetting(settingName, setting['options'][option]))
                        use mod_iconButton('\ue872', '{mod_notl}Clear{/mod_notl}', mod.SetmodSetting(settingName, None), sensitive=(mod.Settings.get(settingName, globalSetting=False)!=None))
                hbox xsize colWidth[3]:
                    hbox spacing 2 box_wrap True:
                        for option in setting['options']:
                            use mod_radiobutton(mod.Settings.get(settingName, globalSetting=True)==setting['options'][option], option, mod.SetmodSetting(settingName, setting['options'][option], globalSetting=True), sensitive=If(mod.Settings.globalAvailable, None, False))
                        use mod_iconButton('\ue872', '{mod_notl}Default{/mod_notl}', mod.SetmodSetting(settingName, None, globalSetting=True), sensitive=If(mod.Settings.globalAvailable, None, False))
