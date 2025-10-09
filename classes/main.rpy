
init python:
    MF2.load(['dialogs','extra','inputs','tooltips'], 'mod', 'mods/framework')

init 52 python in mod:
    _constant = True 

    version = '1.1'
    Settings = SettingsClass()
    States = StatesClass()
    URMFiles = URMFilesClass()
    VarsStore = VarsStoreClass()
    LabelsStore = LabelsStoreClass()
    Search = SearchClass()
    Choices = ChoicesClass()
    PathDetection = PathDetectionClass()
    TextBox = TextBoxClass()
    TextRepl = TextReplacementsClass()
    Gamesaves = GameSavesClass()
    LabelMon = LabelMonClass()
    Notifications = NotificationsClass()
    Snapshots = SnapshotsClass()
    StoreMonitor = StoreMonitorClass()
    CodeView = CodeViewClass()
    ProgressBar = ProgressBarClass()

    def init():
        LabelMon.init()
        if not 's_e_n' in renpy.config.gestures:
            renpy.config.gestures['s_e_n'] = 'alt_K_m'
            States.gestureInitialized = True
        
        if not 'urm_notl' in renpy.config.custom_text_tags: 
            def notl(tag, argument, contents): return contents
            renpy.config.custom_text_tags['urm_notl'] = notl

    def afterLoad(): 
        renpy.show_screen('URM_overlay')
        if 'URM_quickmenu' not in renpy.config.overlay_screens: renpy.config.overlay_screens.append('URM_quickmenu')
        StoreMonitor.init()
        
        SetDialogTransparency(Settings.themeTransparency, doNotRebuild=True, doNotSave=True)()
        if Settings.theme != 'Default':
            SetTheme(Settings.theme, doNotSave=True)()
        
        URMFiles.autoLoad()
        
    def onLabelCalled(label, called):
        if label == 'start':
            afterLoad()
        elif label == '_start_replay':
            renpy.show_screen('URM_overlay')

    class Open(NonPicklable):
        def __init__(self, screen=None):
            self.screen = screen
        
        def __call__(self):
            if renpy.store._in_replay:
                Confirm("Do you want to end the current replay?", renpy.end_replay, title='End replay')()
            else:
                if self.screen:
                    Settings.currentScreen = self.screen
                else:
                    renpy.take_screenshot()
                    renpy.run(renpy.store.Show('URM_main'))

    def scale(percentage, size):
        return int((percentage / 100.0) * size)

    def scaleX(percentage):
        return scale(percentage, renpy.config.screen_width)

    def scaleY(percentage):
        return scale(percentage, renpy.config.screen_height)

    def scaleText(text, percentageOrPixels, style='mod_text', pixelTarget=False, escapeStyling=False, reverse=False):
        try:
            import re
            
            if pixelTarget:
                targetSize = scalePx(percentageOrPixels)
            else:
                targetSize = scaleX(percentageOrPixels)
            if escapeStyling:
                text = re.sub('\{.*?\}', '{\g<0>', text)
            else:
                text = re.sub('\{.*?\}', '', text)
            textLength = len(text)
            
            for currentLength in range(5, textLength+1):
                shortenedText = text[len(text)-currentLength:] if reverse else text[:currentLength]
                if renpy.store.Text(shortenedText, None, False, False, style=style).size()[0] > targetSize: 
                    textLength = currentLength-1 
                    break
            
            if textLength < len(text):
                if reverse:
                    return '...'+text[len(text)-textLength+1:]
                else:
                    return text[:textLength-1]+'...'
            else:
                return text[:textLength]
        except:
            return text

    def touchDragged(drags, *args, **kwargs):
        try:
            Settings.touchPosition = (drags[0].x, drags[0].y)
        except Exception as e:
            print('info: Failed to save touchbutton position: {}'.format(e))

    def progressDragged(drags, *args, **kwargs):
        try:
            Settings.progressPosition = (drags[0].x, drags[0].y)
        except Exception as e:
            print('info: Failed to save progress position: {}'.format(e))

    class OpenConsole(NonPicklable):
        def __call__(self):
            renpy.store._console.enter()

    class URMReplay(NonPicklable):
        def __init__(self, label, finishAction=None, screenErrorVariable=None):
            self.label = label
            self.finishAction = finishAction
            self.screenErrorVariable = screenErrorVariable
            self._m1_main__error = None
            self._m1_main__currentScreen = None
        
        def _m1_main__replayErrorHandler(self, short, full, traceback_fn):
            self._m1_main__error = short
            return True
        
        def __call__(self):
            if not renpy.has_label(self.label):
                mod.Confirm('The selected label does not exist')()
            else:
                if self.screenErrorVariable:
                    self._m1_main__currentScreen = renpy.current_screen()
                
                replayScope = {}
                for k, v in renpy.store.__dict__.items():
                    if not k.startswith('_') and k != 'suppress_overlay':
                        replayScope[k] = v
                
                defaultErrorHandler = renpy.display.error.report_exception 
                renpy.display.error.report_exception = self._m1_main__replayErrorHandler 
                try:
                    renpy.call_replay(self.label, replayScope)
                except:
                    pass
                renpy.display.error.report_exception = defaultErrorHandler 
                
                if self._m1_main__error and self.screenErrorVariable and self._m1_main__currentScreen: 
                    if self.screenErrorVariable in self._m1_main__currentScreen.scope:
                        self._m1_main__currentScreen.scope['errorMessage'] = 'Replay failed with error:\n{}'.format(self._m1_main__error)
                elif self.finishAction:
                    self.finishAction()
                
                renpy.restart_interaction()

init 1999 python in _console:
    console = DebugConsole()

init 999 python:
    mod.init()
        
    MF2.loadFile('mods/URM_styles.rpy', 'mod')
    MF2.loadFile('mods/screens/main.rpy', 'mod')
    MF2.loadFile('mods/screens/search.rpy', 'mod')
    MF2.loadFile('mods/screens/vars.rpy', 'mod')
    MF2.loadFile('mods/screens/snapshots.rpy', 'mod')
    MF2.loadFile('mods/screens/labels.rpy', 'mod')
    MF2.loadFile('mods/screens/watchpanel.rpy', 'mod')
    MF2.loadFile('mods/screens/textbox.rpy', 'mod')
    MF2.loadFile('mods/screens/textrepl.rpy', 'mod')
    MF2.loadFile('mods/screens/choices.rpy', 'mod')
    MF2.loadFile('mods/screens/gamesaves.rpy', 'mod')
    MF2.loadFile('mods/screens/paths.rpy', 'mod')
    MF2.loadFile('mods/screens/progress.rpy', 'mod')
    MF2.loadFile('mods/screens/options.rpy', 'mod')
    MF2.loadFile('mods/screens/utils.rpy', 'mod')
    MF2.loadFile('mods/screens/quickmenu.rpy', 'mod')
    MF2.loadFile('mods/screens/codeview.rpy', 'mod')
        
    renpy.config.after_load_callbacks.append(mod.afterLoad)
    mod.LabelMon.onLabelCalled.append(mod.onLabelCalled)
        
    if mod.Settings.skipSplashscreen:
        renpy.config.label_overrides['splashscreen'] = 'URM_splashscreen'
