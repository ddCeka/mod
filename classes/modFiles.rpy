
init 3 python in mod:
    _constant = True

    class modFilesClass(NonPicklable):
        def __init__(self):
            self.file = modFile()
            
            self._m1_modFiles__saveDir = None 
            self.gameDir = renpy.os.path.abspath(renpy.os.path.join(renpy.config.basedir, "game"))
        
        @property
        def saveDir(self):
            if self._m1_modFiles__saveDir == None:
                if Settings.saveDir:
                    self._m1_modFiles__saveDir = renpy.os.path.abspath(renpy.os.path.join(Settings.saveDir, renpy.config.save_directory)) 
                elif renpy.os.path.isdir(renpy.config.savedir):
                    self._m1_modFiles__saveDir = renpy.config.savedir 
                
                try:
                    renpy.os.makedirs(self.saveDir)
                except Exception:
                    pass
            
            return self._m1_modFiles__saveDir
        
        def fileExists(self, filename):
            return renpy.exists(renpy.os.path.join(self.gameDir, filename)) or (self.saveDir and renpy.exists(renpy.os.path.join(self.saveDir, filename)))
        
        def stripSpecialChars(self, str):
            import re
            return re.sub('[^A-Za-z0-9 _-]', '_', str)
        
        def listFiles(self):
            import re
            from glob import glob
            from collections import OrderedDict
            
            files = {}
            
            gameDirFiles = glob(renpy.os.path.join(re.sub(r'(\[|\])', r'[\1]', self.gameDir), '*.mod')) 
            for i,filename in enumerate(gameDirFiles):
                files[filename[len(self.gameDir)+1:]] = modFile(filename)
            
            if self.saveDir:
                saveDirFiles = glob(renpy.os.path.join(re.sub(r'(\[|\])', r'[\1]', self.saveDir), '*.mod')) 
                for i,filename in enumerate(saveDirFiles):
                    mtime = renpy.os.path.getmtime(filename)
                    name = filename[len(self.saveDir)+1:]
                    if not hasattr(files, name) or files[name].mtime < mtime:
                        files[name] = modFile(filename)
            
            files = OrderedDict(sorted(files.items()))
            
            return files
        
        def autoLoad(self):
            """ Auto load the `lastLoadedFile` if nothing is loaded """
            if not self.file.unsaved and Settings.lastLoadedFile != None and Settings.lastLoadedFile != self.file.filename:
                self.load(Settings.lastLoadedFile)
        
        def clear(self, confirm=False):
            """ Start a new file """
            if self.file.unsaved and not confirm:
                Confirm('Unsaved changes will be lost, do you want to continue?', renpy.store.Function(self.clear, confirm=True))()
            else:
                self.file = modFile()
                Settings.lastLoadedFile = None
        
        class Clear(NonPicklable):
            def __call__(self):
                modFiles.clear()
        
        def load(self, filename):
            modFile = modFile(filename)
            
            
            filepath = modFile.lastModifiedPath
            if filepath:
                modFile = self.loadLegacymodFile(filepath) or modFile
                
                self.file = modFile
                Settings.lastLoadedFile = filename
                return True
            else:
                return False
        
        class Load(NonPicklable):
            def __init__(self, filename=None, finishAction=None, screenErrorVariable=None):
                self.filename = filename
                self.finishAction = finishAction
                self.screenErrorVariable = screenErrorVariable
            
            def __call__(self):
                if not self.filename:
                    if modFiles.file.unsaved:
                        Confirm('Unsaved changes will be lost, do you want to continue?', renpy.store.Show('mod_load_file'))()
                    else:
                        renpy.show_screen('mod_load_file')
                        renpy.restart_interaction()
                else:
                    if modFiles.load(self.filename):
                        if self.finishAction:
                            self.finishAction()
                    elif self.screenErrorVariable: 
                        cs = renpy.current_screen()
                        if cs and self.screenErrorVariable in cs.scope:
                            cs.scope[self.screenErrorVariable] = 'Failed to load file'
                            renpy.restart_interaction()
        
        def loadLegacymodFile(self, filepath):
            import json
            
            jsonData = None
            try:
                f = renpy.os.open(filepath, renpy.os.O_RDONLY)
                if renpy.os.read(f, 1).decode() == '{': 
                    renpy.os.lseek(f, 0, renpy.os.SEEK_SET)
                    jsonData = json.loads(renpy.os.read(f, renpy.os.path.getsize(filepath)), object_pairs_hook=OrderedDict)
                renpy.os.close(f)
            except Exception as e:
                print(': Loading file "{}" failed with error: {}'.format(filepath, e))
                return None
            
            if jsonData:
                try:
                    newfile = modFile(renpy.os.path.split(filepath)[1])
                    for store in jsonData:
                        if store == 'replacements':
                            jsonData[store] = OrderedDict([(r['original'], r) for r in jsonData[store]]) 
                        
                        newfile.addStore(store, modFileStore(jsonData[store]))
                    
                    return newfile
                except Exception as e:
                    print(': Failed to parse contents for file "{}" with error: {}'.format(filepath, e))
                    return None
        
        def save(self, name, successAction=None, failureAction=None, overwrite=False):
            filename = self.stripSpecialChars(name)+'.mod'
            if self.fileExists(filename) and not overwrite:
                return Confirm('Do you want to overwrite the existing file?', renpy.store.Function(self.save, name, successAction, failureAction, True))()
            elif self.file and isinstance(self.file, modFile):
                if self.file.save(filename):
                    Settings.lastLoadedFile = filename
                    
                    if successAction:
                        successAction()
                    else:
                        return True
                else:
                    if failureAction:
                        failureAction()
                    else:
                        return False
        
        class Save(NonPicklable):
            def __init__(self, name=None, finishAction=None, screenErrorVariable=None):
                self.name = name
                self.finishAction = finishAction
                self.screenErrorVariable = screenErrorVariable
            
            def __call__(self):
                if self.name == None: 
                    renpy.show_screen('mod_save_file')
                    renpy.restart_interaction()
                else:
                    cs = renpy.current_screen()
                    
                    def onSuccess():
                        if self.finishAction:
                            self.finishAction()
                    
                    def onFailure():
                        if self.screenErrorVariable and cs and self.screenErrorVariable in cs.scope:
                            cs.scope[self.screenErrorVariable] = 'Failed to save file'
                            renpy.restart_interaction()
                    
                    modFiles.save(self.name if not callable(self.name) else self.name(), onSuccess, onFailure)
        
        class Delete(NonPicklable):
            def __init__(self, modFile):
                self.modFile = modFile
            
            def __call__(self):
                if isinstance(self.modFile, modFile):
                    self.modFile.delete()

    class modFileStore(OrderedDict):
        def __init__(self, data=None, unsaved=False):
            super(OrderedDict, self).__init__(data or {})
            self.unsaved = unsaved
        
        def __setitem__(self, key, val):
            super(OrderedDict, self).__setitem__(key, val)
            self.unsaved = True
        
        def __delitem__(self, key):
            if key in self:
                super(OrderedDict, self).__delitem__(key)
                self.unsaved = True
        
        def update(self, data):
            super(OrderedDict, self).update(data)
            self.unsaved = True
        
        def clear(self):
            if not self.isEmpty: self.unsaved = True
            super(OrderedDict, self).clear()
        
        @property
        def isEmpty(self):
            return not bool(self)
        
        def toJSON(self):
            import json
            return json.dumps(self)

    class modFile(NonPicklable):
        def __init__(self, filename=None):
            self.filename = renpy.os.path.split(filename)[1] if filename else filename
            self.mtime = self.mtime = renpy.os.path.getmtime(self.lastModifiedPath) if self.lastModifiedPath else None
            self._m1_modFiles__stores = None
            self._m1_modFiles__storeNames = None
        
        def getStore(self, name, doNotLoad=False):
            if self._m1_modFiles__stores and name in self._m1_modFiles__stores: 
                return self._m1_modFiles__stores[name]
            elif self._m1_modFiles__storeNames != None and name not in self._m1_modFiles__storeNames: 
                return None
            elif self._m1_modFiles__stores == None and doNotLoad == False: 
                self.load()
                return self.getStore(name, doNotLoad=True)
        
        def __getitem__(self, key):
            return self.getStore(key)
        
        def addStore(self, name, data=None):
            if self._m1_modFiles__stores == None: self._m1_modFiles__stores = {}
            if isinstance(data, modFileStore):
                self._m1_modFiles__stores[name] = data
            else:
                self._m1_modFiles__stores[name] = modFileStore(data)
        
        def clearStore(self, name):
            if self._m1_modFiles__stores and name in self._m1_modFiles__stores:
                self._m1_modFiles__stores[name].clear()
        
        @property
        def storeNames(self):
            """ Names of stores present in this file """
            if self._m1_modFiles__stores:
                return self._m1_modFiles__stores.keys()
            elif self._m1_modFiles__storeNames != None:
                return self._m1_modFiles__storeNames
            else:
                self._m1_modFiles__storeNames = self._m1_modFiles__loadStoreNames()
                return self._m1_modFiles__storeNames
        
        @property
        def unsaved(self):
            if self._m1_modFiles__stores:
                for name in self._m1_modFiles__stores:
                    if self._m1_modFiles__stores[name].unsaved:
                        return True
            return False
        
        @unsaved.setter
        def unsaved(self, val):
            if self._m1_modFiles__stores:
                for name in self._m1_modFiles__stores:
                    self._m1_modFiles__stores[name].unsaved = val
        
        @property
        def gameDirPath(self):
            if self.filename:
                return renpy.os.path.join(modFiles.gameDir, self.filename)
        
        @property
        def saveDirPath(self):
            if self.filename and modFiles.saveDir:
                return renpy.os.path.join(modFiles.saveDir, self.filename)
        
        @property
        def lastModifiedPath(self):
            if self.filename:
                
                gameDirMtime = renpy.os.path.getmtime(self.gameDirPath) if renpy.os.path.isfile(self.gameDirPath) else 0
                saveDirMtime = renpy.os.path.getmtime(self.saveDirPath) if renpy.os.path.isfile(self.saveDirPath or '') else 0
                
                selectedFile = None
                if gameDirMtime >= saveDirMtime and gameDirMtime > 0:  
                    selectedFile = self.gameDirPath
                elif saveDirMtime > 0: 
                    selectedFile = self.saveDirPath
                
                return selectedFile
        
        def _m1_modFiles__initProperties(self):
            self.addStore('properties', {'modVersion': version, 'gameId': renpy.config.save_directory})
        
        def save(self, filename=None):
            import json, zipfile, shutil
            
            if filename: self.filename = filename
            
            if self.filename:
                self._m1_modFiles__initProperties()
                
                filenameNew = self.gameDirPath + '.new'
                try:
                    with zipfile.ZipFile(filenameNew, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for entry in self._m1_modFiles__stores or {}:
                            if not self._m1_modFiles__stores[entry].isEmpty: 
                                zf.writestr(entry, self._m1_modFiles__stores[entry].toJSON())
                    
                    shutil.move(filenameNew, self.gameDirPath)
                except Exception as e:
                    print(': Failed to save file "{}" with error: {}'.format(self.gameDirPath, e))
                    return False
                
                if self.saveDirPath:
                    try:
                        shutil.copy(self.gameDirPath, self.saveDirPath)
                    except Exception as e:
                        print(': Failed to save file "{}" with error: {}'.format(self.saveDirPath, e))
                
                self.unsaved = False
                return True
            
            else: 
                return False
        
        def _m1_modFiles__loadStoreNames(self):
            import zipfile
            selectedFile = self.lastModifiedPath
            
            if selectedFile:
                if not zipfile.is_zipfile(selectedFile): return [] 
                
                try:
                    with zipfile.ZipFile(selectedFile, 'r') as zf:
                        return zf.namelist()
                except Exception as e:
                    print(': Loading storenames from file "{}" failed with error: {}'.format(selectedFile, e))
                    return []
        
        def load(self):
            import json, zipfile
            self._m1_modFiles__stores = {}
            selectedFile = self.lastModifiedPath
            
            if selectedFile:
                try:
                    with zipfile.ZipFile(selectedFile, 'r') as zf:
                        for entry in zf.namelist():
                            try:
                                self._m1_modFiles__stores[entry] = modFileStore(json.loads(zf.read(entry), object_pairs_hook=OrderedDict))
                            except Exception as e:
                                print(': Failed to parse json for entry "{}" in file "{}". {}'.format(entry, selectedFile, e))
                except Exception as e:
                    print(': Loading file "{}" failed with error: {}'.format(selectedFile, e))
                    return None
        
        def delete(self):
            try:
                if renpy.os.path.isfile(self.gameDirPath):
                    renpy.os.remove(self.gameDirPath)
            except Exception as e:
                print(': Failed to delete file "{}" with error: {}'.format(self.gameDirPath, e))
            
            if self.saveDirPath:
                try:
                    if renpy.os.path.isfile(self.saveDirPath):
                        renpy.os.remove(self.saveDirPath)
                except Exception as e:
                    print(': Failed to delete file "{}" with error: {}'.format(self.saveDirPath, e))
