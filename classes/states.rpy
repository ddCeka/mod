
init 1 python in mod:

    class StatesClass(NonPicklable):
        defaultValues = {
            'gestureInitialized': False,
        }
        _m1_states__states = {}
        
        def __init__(self):
            self._m1_states__states = {}
        
        def __getattr__(self, attr):
            if attr in StatesClass.defaultValues:
                if attr in self._m1_states__states:
                    return self._m1_states__states[attr]
                else:
                    return StatesClass.defaultValues[attr]
            else:
                print('info: Something requested an unknown state "{}"'.format(attr))
        
        def __setattr__(self, attr, value):
            if attr in StatesClass.defaultValues:
                self._m1_states__states[attr] = value    
