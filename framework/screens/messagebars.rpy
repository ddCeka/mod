

screen mod_messagebar(kind, message, icon=None, substitute=True):
    style_prefix 'mod'

    frame:
        background Solid(getattr(mod.Theme.colors, '{}Bg'.format(kind)))
        padding (4, 2)

        hbox:
            spacing mod.scalePxInt(4)
            if isinstance(icon, basestring):
                text icon style_suffix 'icon'
            elif icon == None:
                if kind in ['warning','severeWarning']:
                    text '\ue8b2' style_suffix 'icon' color getattr(mod.Theme.colors, '{}Text'.format(kind)) yalign .5
                elif kind == 'error':
                    text '\ue001' style_suffix 'icon' color getattr(mod.Theme.colors, '{}Text'.format(kind)) yalign .5
                elif kind == 'success':
                    text '\ue86c' style_suffix 'icon' color getattr(mod.Theme.colors, '{}Text'.format(kind)) yalign .5


            text message substitute substitute color getattr(mod.Theme.colors, '{}Text'.format(kind))
