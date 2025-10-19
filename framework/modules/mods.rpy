init offset = -10

default persistent.custom_settings = {}
default persistent.custom_settings_default = {}

init python in settings:
    from store import persistent, Action, DictEquality

    not_set = object()

    prefs = persistent.custom_settings
    defaults = persistent.custom_settings_default

    def default(name, default):
        value = defaults.get(name, not_set)
        if value == not_set or value != default:
            defaults[name] = default
            set(name, default)

    def get(name):
        return prefs[name]

    def set(name, value):
        prefs[name] = value

    def toggle(name, a, b):
        value = prefs.get(name, not_set)
        prefs[name] = a if value != a else b

    def reset(name):
        default = defaults.get(name, not_set)
        if default != not_set:
            prefs[name] = default

    class Set(Action, DictEquality):
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def __call__(self):
            set(self.name, self.value)
            renpy.restart_interaction()

        def get_selected(self):
            return prefs.get(self.name, not_set) == self.value

    class Reset(Action, DictEquality):
        def __init__(self, name):
            self.name = name

        def __call__(self):
            reset(self.name)
            renpy.restart_interaction()

        def get_sensitive(self):
            return prefs.get(self.name, not_set) != defaults.get(self.name, not_set)

    class Toggle(Action, DictEquality):
        def __init__(self, name, true_value=True, false_value=False):
            self.name = name
            self.true_value = true_value
            self.false_value = false_value

        def __call__(self):
            toggle(self.name, self.true_value, self.false_value)
            renpy.restart_interaction()

        def get_selected(self):
            return prefs[self.name] == self.true_value


init python:
    if renpy.android:
        settings.default("crashdefendersetting", 0)

        # Attempts at fixing the texture leak plaguing
        # android devices, mainly running on Android 11 & Android 12.
        class TextureLeakFix(NoRollback):
            def __init__(self, limit=100):
                self.statements = 0

                self.set_mode(settings.get("crashdefendersetting"))

            def set_mode(self, mode):
                if mode == 3:
                    self.limit = 15
                elif mode == 2:
                    self.limit = 25
                elif mode == 1:
                    self.limit = 55
                else:
                    self.limit = 0

            def __call__(self, name):
                if renpy.is_init_phase() or self.limit == 0:
                    return

                self.statements += 1

                if self.statements > self.limit:
                    self.statements = 0

                    # Big thanks to Andykl (https://github.com/Andykl)
                    # for finding the issue and inventing this workaround.
                    # https://github.com/renpy/renpy/issues/3643

                    cache = renpy.display.im.cache
                    cache_size = cache.get_total_size()
                    cache_limit = cache.cache_limit * 0.95

                    if cache_size >= cache_limit:
                        if config.developer:
                            print("Cache limit reached, purging cache... ({}/{})\n{}".format(cache_size, cache_limit, renpy.get_filename_line()))

                        cache.clear()

                    if renpy.game.interface is not None:
                        if config.developer:
                            print("Statements limit reached, cleaning textures... ({})\n{}".format(self.limit, renpy.get_filename_line()))

                        renpy.game.interface.full_redraw = True
                        renpy.game.interface.restart_interaction = True

                        if renpy.display.draw is not None:
                            renpy.display.draw.kill_textures()

                        renpy.display.render.free_memory()

        crashdefender = TextureLeakFix()

        config.statement_callbacks.append(crashdefender)

## mods begin here
init 99:
    default preferences.gl_powersave = False
    define config.console = True
    define config.hw_video = True
    define config.has_autosave = True
    define config.autosave_on_quit = True
    define config.autosave_on_choice = True
    define config.save_on_mobile_background = True
    define config.autosave_frequency = 200
    ## define config.autosave_slots = 12
    define config.allow_skipping = True
    define config.rollback_enabled = True
    define config.hard_rollback_limit = 100
    ## define config.allow_underfull_grids = True
    define config.default_music_volume = 0.5
    define config.default_sfx_volume = 0.5
    define config.default_voice_volume = 0.5
    ## define mod = Character("Mod", color="#0f0")
    define mod_textbox = True
    default setting_current_tab = "home"
    default setting_column2 = None
    default setting_column2_name = ""
    default persistent.mod_textbox = True
    default persistent.modtext_size = gui.text_size
    default persistent.modtext_outline = 2
    default persistent.modtextbox_opacity = 0.0

    if persistent.mod_textbox == True:
        style say_label:
            outlines [ (absolute(persistent.modtext_outline), "#000", absolute(1), absolute(1)) ]
        
        style say_dialogue:
            color "#FFFFFF"
            outlines [ (absolute(persistent.modtext_outline), "#000", absolute(1), absolute(1)) ]
        
        style choice_button:
            background None
        
        style input_prompt:
            font "DejaVuSans.ttf"
            size persistent.modtext_size
            color "#FFFFFF"
            outlines [ (absolute(persistent.modtext_outline), "#000", absolute(1), absolute(1)) ]
        
        style input:
            font "DejaVuSans.ttf"
            size persistent.modtext_size
            color "#FFFFFF"
            outlines [ (absolute(persistent.modtext_outline), "#000", absolute(1), absolute(1)) ]
        
        style choice_button_text:
            font "DejaVuSans.ttf"
            size persistent.modtext_size
            idle_color "#FFF"
            hover_color "#00FF00"
            insensitive_color "#808080FF"
            idle_outlines [ (absolute(persistent.modtext_outline), "#FFF0", absolute(1), absolute(1)), (absolute(2), "#000", absolute(1), absolute(1)) ]
            hover_outlines [ (absolute(persistent.modtext_outline), "#0F08", absolute(1), absolute(1)), (absolute(2), "#000", absolute(1), absolute(1)) ]
            insensitive_outlines [ (absolute(persistent.modtext_outline), "#808080C0", absolute(1), absolute(1)), (absolute(2), "#000", absolute(1), absolute(1)) ]
        
        screen choice(items):
            style_prefix "choice"
            vbox:
                spacing 10
                xalign 0.5
                yalign 0.6
                for n, i in enumerate(items, 1):
                    if n < 10:
                        key str(n) action i.action
                        key "K_KP" + str(n) action i.action
                        textbutton str(n) + ". " + i.caption action i.action

        screen say(who, what):
            style_prefix "say"

            window:
                background Transform(style.window.background, alpha=persistent.modtextbox_opacity)
                
                if who is not None:

                    window:
                        style "namebox"
                        text who id "who":
                            outlines [ (absolute(persistent.modtext_outline), "#000", absolute(0), absolute(0)) ]

                text what id "what":
                    color "#FFFFFF"
                    size persistent.modtext_size
                    outlines [ (absolute(persistent.modtext_outline), "#000", absolute(0), absolute(0)) ]

            ## Sometimes using joiplay desktop mode in phone, side image don't have
            ## enough spaces on phone, so better change the position or remove it
            if not renpy.variant("small"):
                add SideImage() xalign 0.0 yalign 1.0

init 99 python:
    if not persistent.mod_textbox:
        persistent.modtextbox_opacity = 0.0

## Keyboard input android sometimes messed up
init -2 python:
    class GetInput(Action):
        def __init__(self,screen_name,input_id):
            self.screen_name=screen_name
            self.input_id=input_id
        def __call__(self):
            if renpy.get_widget(self.screen_name,self.input_id):
                return str(renpy.get_widget(self.screen_name,self.input_id).content)

## IC Patch
init 1 python:
    replaces = { 'step-': '', 'Step-': '' }

    def change_to_incest(text):
        replaced_text = text

        for key in replaces.keys():
            replaced_text = replaced_text.replace(key, replaces[key])

        return replaced_text

    config.say_menu_text_filter = change_to_incest

#£ Classic gallery unlocker
init 101 python:
    def _mark_label_as_seen(label):

        renpy.game.persistent._seen_ever[str(label)] = True # type: ignore
    
    def _unlock_scenes():
        
        for label in renpy.get_all_labels():
            _mark_label_as_seen(label)
            
    _unlock_scenes()
    
    for label in renpy.get_all_labels():
        renpy.game.persistent._seen_ever[label] = True
        renpy.game.seen_session[label] = True

init python:
    config.gestures["n"] = "game_menu"
    config.gestures["s"] = "hide_windows"
    config.gestures["e"] = "skip"
    config.gestures["w"] = "rollback"
    config.gestures["n_s_n"] = "performance"
    config.gestures["e_w_e"] = "fast_skip"
    config.gestures["n_w_s"] = "console"
    ## part of walkthrough mods
    gr = "{color=#00c000}"
    red = "{color=#f00}"
    blue = "{color=#00f}"
    pink = "{color=#f626a1}"
    modt = "{size=-8}"
    mark = "{image=mods/images/mark.png}"


screen mods():

    zorder 1

    drag:
        drag_name "mods"
        align (0.5, 0.5)
        drag_handle (0, 0, 1.0, 53)

        has fixed:
            xysize (800, 600)
            align (0.5, 0.5)

        if setting_current_tab == "home" or setting_current_tab == "extra" or setting_current_tab == "gesture":
            add Solid("#000000e6")
        else:
            add Solid("#000000")
        textbutton "Close" text_style "mods_toolbar_textbutton" action Return() align (0.0, 1.0) yoffset -6


        hbox:
            pos (0.015, 0.007)
            anchor (0.0, 0.0)
            spacing 70
            textbutton "Prefs" selected setting_current_tab == "home" text_style "mods_toolbar_textbutton" action [SetScreenVariable("setting_current_tab", "home"), SetScreenVariable("setting_column2", None), SetScreenVariable("setting_column2_name", "")]
            textbutton "Extra" selected setting_current_tab == "extra" text_style "mods_toolbar_textbutton" action [SetScreenVariable("setting_current_tab", "extra"), SetScreenVariable("setting_column2", None), SetScreenVariable("setting_column2_name", "")]
            if persistent.mod_textbox:
                textbutton "Textbox" selected setting_current_tab == "textbox" text_style "mods_toolbar_textbutton" action [SetScreenVariable("setting_current_tab", "textbox"), SetScreenVariable("setting_column2", None), SetScreenVariable("setting_column2_name", "")]
            textbutton "Gesture" selected setting_current_tab == "gesture" text_style "mods_toolbar_textbutton" action [SetScreenVariable("setting_current_tab", "gesture"), SetScreenVariable("setting_column2", None), SetScreenVariable("setting_column2_name", "")]


        if setting_current_tab == "home":
            text "Preferences" style "mods_home_title"

            frame:
                style "mods_frame_outline"
                has frame:
                    style "mods_frame_main"

                hbox:
                    style_prefix "mods_settings"
                    align (0.5, 0.6)
                    spacing 80
                    
                    vbox:
                        label _("HW Video")
                        textbutton _("Use Hardware") action SetVariable("config.hw_video", "True")
                        textbutton _("Use Software") action SetVariable("config.hw_video", "False")
                        
                    vbox:
                        label _("Powersave")
                        textbutton _("Enable") action Preference("gl powersave", True)
                        textbutton _("Disable") action Preference("gl powersave", False)
                        textbutton _("Auto") action Preference("gl powersave", "auto")
                        
                    vbox:
                        label _("Font Override")
                        textbutton _("Default") action Preference("font transform", None)
                        textbutton _("DejaVuSans") action Preference("font transform", "dejavusans")
                        textbutton _("Opendyslexic") action Preference("font transform", "opendyslexic")


        elif setting_current_tab == "extra":
            text "Extra" style "mods_home_title"

            frame:
                style "mods_frame_outline"
                has frame:
                    style "mods_frame_main"

                hbox:
                    style_prefix "mods_settings"
                    align (0.5, 0.6)
                    spacing 40
                    
                    vbox:
                        label _("Textbox Mod")
                        textbutton _("Enable") action SetField(persistent,"mod_textbox", True)
                        textbutton _("Disable") action SetField(persistent,"mod_textbox", False)
                    
                    vbox:
                        label _("Accessibility")
                        textbutton _("Show") action ShowMenu("_accessibility")
                        
                    vbox:
                        label _("GL2")
                        textbutton _("Enable") action SetVariable("config.gl2", True)
                        textbutton _("Disable") action SetVariable("config.gl2", False)
                    
                    vbox:
                        label _("Crash Defender") ## Mainly Android 11 & 12
                        textbutton "Off" action [settings.Set("crashdefendersetting", 0), Function(crashdefender.set_mode, 0)]
                        textbutton "Relaxed" action [settings.Set("crashdefendersetting", 1), Function(crashdefender.set_mode, 1)]
                        textbutton "Balanced" action [settings.Set("crashdefendersetting", 2), Function(crashdefender.set_mode, 2)]
                        textbutton "Aggressive" action [settings.Set("crashdefendersetting", 3), Function(crashdefender.set_mode, 3)]


        elif setting_current_tab == "textbox":
            text "Customize Textbox" style "mods_home_title"

            frame:
                style "mods_frame_outline"
                has frame:
                    style "mods_frame_main"
                
                hbox:
                    style_prefix "mods_settings"
                    align (0.5, 0.6)
                    spacing 80
                    
                    vbox:
                        label _("Text Size ([persistent.modtext_size]/50)")
                        bar:
                            value FieldValue(persistent, "modtext_size", offset=20, range=30, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.modtext_size", gui.text_size))

                        label _("Text Outline ([persistent.modtext_outline]/4)")
                        bar:
                            value FieldValue(persistent, "modtext_outline", range=4, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.modtext_outline", 2))

                        $ percent_value = int(persistent.modtextbox_opacity * 100)
                        label _("Textbox Opacity ([percent_value]%)")
                        bar:
                            value FieldValue(persistent, "modtextbox_opacity", range=1.0, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.modtextbox_opacity", 0.0))
                            
                            
        elif setting_current_tab == "gesture":
            text "Gestures" style "mods_home_title"

            frame:
                style "mods_frame_outline"
                yalign 0.75
                has frame:
                    style "mods_frame_main"
                vbox:
                    style_prefix "mods_settings"
                    align (0.5, 0.6)
                    spacing 10

                    text ("Swipe Up = Menu")
                    text ("Swipe Down = Hide")
                    text ("Swipe Left = Back")
                    text ("Swipe Right = Skip")
                    text ("Down-Right-Up = Open mod")
                    text ("Right-Left-Right = Fast-Skip to next choice")
                    text ("Up-Down-Up = Show Performance")
                    text ("Up-Left-Down = Console Screen (Type exit to close!)")


        else:
            vbox:
                pos (0.03, 0.08)
                anchor (0.0, 0.0)
                for i in getattr(store, setting_current_tab):
                    textbutton i[0] selected setting_column2_name == i[0] text_style "mods_column1_textbutton" action [SetScreenVariable("setting_column2", getattr(store, i[1])), SetScreenVariable("setting_column2_name", i[0])]

            if setting_column2 is not None:
                text setting_column2_name align (0.0, 0.078) style "mods_column2_header" xoffset 318
                vbox:
                    pos (305, 99)
                    anchor (0.0, 0.0)
                    spacing 0
                    for i in setting_column2:
                        button:
                            xysize (495, 48)
                            idle_background mod.Theme.colorAlpha(mod.Theme.background, 0.4)
                            hover_background Solid(mod.Theme.background)
                            text i[0] align (0.0, 0.5) style "mods_column2_textbutton"
                            action Show(i[1])


style game_menu_outer_frame is empty
style mods_label is gui_label
style mods_label_text is gui_label_text

style mods_home_title is text:
    size 26
    font "DejaVuSans.ttf"
    color "#fff"
    selected_color "#02ffbf"
    hover_color "#8888887f"
    align (0.5, 0.2)

style mods_toolbar_textbutton is text:
    font "DejaVuSans.ttf"
    color "#fff"
    selected_color "#02ffbf"
    hover_color "#8888887f"
    size 18

style mods_column1_textbutton is text:
    font "DejaVuSans.ttf"
    color "#fff"
    selected_color "#02ffbf"
    hover_color "#8888887f"
    size 18
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style mods_column2_header is text:
    font "DejaVuSans.ttf"
    color "#fff"
    size 18
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style mods_column2_textbutton is text:
    xoffset 15
    font "DejaVuSans.ttf"
    color "#fff"
    selected_color "#02ffbf"
    hover_color "#8888887f"
    size 14
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style mods_frame_outline is frame:
    align (0.5, 0.65)
    padding (2, 2)
    background Solid(mod.Theme.background)

style mods_frame_main is frame:
    align (0.5, 0.5)
    padding (20, 20)
    background mod.Theme.colorAlpha(mod.Theme.background, 0.4)

style mods_outer_frame:
    bottom_padding 45
    top_padding 90
    background mod.Theme.colorAlpha(mod.Theme.background, 0.4)

style mods_settings_text is text:
    font "DejaVuSans.ttf"
    color "#fff"
    size 16
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]

style mods_settings_button_text is button_text:
    font "DejaVuSans.ttf"
    color "#fff"
    selected_idle_color "#02ffbf"
    hover_color "#8888887f"
    size 16
    outlines [ (absolute(2), "#000", absolute(1), absolute(1)) ]
