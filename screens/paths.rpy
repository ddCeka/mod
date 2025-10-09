
screen URM_paths():
    layer 'Overlay'
    style_prefix 'mod'
    modal True
    default selectedStatementIndex = mod.PathDetection.selectedIndex
    default statements = mod.PathDetection.statements or []
    default colWidth = [mod.scalePxInt(40), mod.scalePxInt(280), mod.scalePxInt(150), mod.scalePxInt(300)]
    default selectedIndex = None

    use mod_Dialog('{urm_notl}Path options{/urm_notl}', [Hide('URM_paths'),Hide('mod_Confirm'),Hide('URM_CodeView')], icon='\uf184'):
        null height 10

        use URM_tableRow():
            label '#' xsize colWidth[0]
            label '{urm_notl}Active path{/urm_notl}' xsize colWidth[1]
            label '{urm_notl}Code{/urm_notl}' xsize colWidth[2]
            label '{urm_notl}Next label{/urm_notl}' xsize colWidth[3]

        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"

            for i,statement in enumerate(statements):
                use URM_tableRow(i):
                    hbox xsize colWidth[0] yalign .5:
                        if i < 9:
                            text If(selectedIndex==i, '{b}{u}'+str(i+1)+'{/u}{/b}', '{u}'+str(i+1)+'{/u}')
                            key 'alt_K_{}'.format(i+1) action ToggleScreenVariable('selectedIndex', i, None)
                        else:
                            text str(i+1)
                    hbox xsize colWidth[1] yalign .5:
                        hbox yalign .5:
                            if i == selectedStatementIndex:
                                use mod_messagebar('success', '{urm_notl}True{/urm_notl}')
                            else:
                                use mod_messagebar('error', '{urm_notl}False{/urm_notl}')
                        if statement.condition != 'True':
                            null width mod.scalePxInt(10)
                            use mod_iconButton('\uf1c2', If(selectedIndex==i, '{u}C{/u}ondition', '{urm_notl}Condition{/urm_notl}'), statement.OpenConditionView)
                            if selectedIndex==i:
                                key 'alt_K_c' action statement.OpenConditionView
                        elif selectedIndex==i:
                                key 'alt_K_c' action NullAction()
                    hbox xsize colWidth[2] yalign .5:
                        if statement.code:
                            use mod_iconButton('\ue86f', If(selectedIndex==i, '{u}S{/u}how', '{urm_notl}Show{/urm_notl}'), statement.OpenCodeView)
                            if selectedIndex==i:
                                key 'alt_K_s' action statement.OpenCodeView
                        else:
                            text 'Not found'
                            if selectedIndex==i:
                                key 'alt_K_s' action NullAction()
                    hbox xsize colWidth[3] yalign .5:
                        if statement.jumpTo:
                            use mod_iconButton('\ue163', If(selectedIndex==i, 'L{u}a{/u}bel', mod.scaleText(statement.jumpTo, 14, 'URM_button_text')), Show('URM_replay_jump', jumpTo=statement.jumpTo))
                            if selectedIndex==i:
                                key 'alt_K_a' action Show('URM_replay_jump', jumpTo=statement.jumpTo)
                        else:
                            text 'N/A'
                            if selectedIndex==i:
                                key 'alt_K_a' action NullAction()
                    hbox xsize mod.scalePxInt(150):
                        if statement.Action:
                            use mod_iconButton('\ue86c', If(selectedIndex==i, '{b}S{u}e{/u}lect{/b}', '{urm_notl}Select{/urm_notl}'), [statement.Action,Hide('URM_paths'),Hide('URM_CodeView')])
                            if selectedIndex==i:
                                key 'alt_K_e' action [statement.Action,Hide('URM_paths'),Hide('URM_CodeView')]
                                key 'K_KP_ENTER' action [statement.Action,Hide('URM_paths'),Hide('URM_CodeView')]
                                key 'K_RETURN' action [statement.Action,Hide('URM_paths'),Hide('URM_CodeView')]
                        else:
                            use mod_iconButton('\ue86c', '{urm_notl}Select{/urm_notl}')
                            use mod_iconButton('\ueb8b', action=mod.Confirm(title='Not forceable', prompt='This path cannot be force selected\nProbably because it\'s behind a call or jump'))
