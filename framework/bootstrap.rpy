
init -1000 python in MF2:
    _constant = True


    from collections import OrderedDict
    availableModules = OrderedDict([
        ('main', ['bootstrap.rpy','modules/01utils.rpy']), 
        ('fonts', ['MaterialIcons-Regular.ttf','MaterialIconsOutlined-Regular.otf','Roboto-Regular.ttf']),
        ('theming', ['fonts','modules/10theme.rpy','theme.rpy.','screens/buttons.rpy.','screens/messagebars.rpy.']),
        ('dialogs', ['theming','modules/dialogs.rpy','screens/dialogs.rpy.']),
        ('extra', ['modules/addon.rpy']),
        ('inputs', ['modules/inputs.rpy']),
        ('screeninjector', ['modules/screeninjector.rpy']),
        ('screenreader', ['modules/screenreader.rpy']),
        ('tooltips', ['modules/tooltips.rpy']),
    ])

    def load(modules, modName, mfPath, minVersion='6.99.14'):
        
        if renpy.version_only < minVersion: raise Exception(': This mod ({}) does not support Ren\'Py version {}. Lowest supported version is {}'.format(modName, renpy.version_only, minVersion))
        
        if not 'main' in modules: modules.append('main') 
        
        archivePath = findArchivePath('{}/bootstrap.rpyc'.format(mfPath))
        if archivePath: 
            if hasattr(renpy.store, modName) and isinstance(getattr(renpy.store, modName), renpy.python.StoreModule):
                getattr(renpy.store, modName).archivePath = archivePath
        
        filesToLoad = []
        def addFilesToLoad(files):
            for file in files:
                if file in availableModules: 
                    addFilesToLoad(availableModules[file])
                elif file not in filesToLoad:
                    filesToLoad.append(file)
        
        for availableModule in availableModules:
            if availableModule in modules:
                addFilesToLoad(availableModules[availableModule])
        
        for fn in filesToLoad:
            fullFn = '{}/{}'.format(mfPath, fn)
            loadFile(fullFn, modName, mfPath)

    def loadFile(fullFn, modName, mfPath=None):
        ext = renpy.os.path.splitext(fullFn)[1].lower()
        
        if ext in ['.rpy']: 
            loadableSource = renpy.loadable(fullFn)
            loadableTransformed = renpy.loadable(fullFn+'t')
            
            if loadableSource or loadableTransformed: 
                try:
                    modFile = renpy.loader.load(fullFn+'t') if loadableTransformed else renpy.loader.load(fullFn)
                    modFileContents = modFile.read().decode()
                    if loadableSource: 
                        modFileContents = modFileContents.replace('_ModName_', modName) 
                        if mfPath: modFileContents = modFileContents.replace('_MFPath_', mfPath) 
                    modFileLoaded = (renpy.load_string(modFileContents, fullFn) != None) 
                    if not modFileLoaded: raise Exception(renpy.get_parse_errors()) 
                except Exception as e:
                    raise Exception('0: Failed to load file "{}". {}'.format(fullFn, e))
            
            elif ext == '.rpy': 
                fullFn = fullFn[:-6] + 'rpyc'
                if not renpy.loadable(fullFn):
                    raise Exception(': File "{}" not found'.format(fullFn))
            
            else:
                raise Exception(': File "{}" not found'.format(fullFn))

    def findArchivePath(fullFn):
        """ Find the archive path for a certain file """
        for archiveName,files in renpy.loader.archives:
            if fullFn in files:
                archivePath = renpy.os.path.abspath(renpy.os.path.join(renpy.config.basedir, 'game', archiveName))
                if not renpy.os.path.isfile(archivePath) and renpy.os.path.isfile(archivePath+'.rpa'): 
                    archivePath = archivePath+'.rpa'
                return archivePath

init 999 python:
    if not 'Overlay' in config.layers: config.layers.append('mod_Overlay') 
