
screen mod_paths():
    layer 'mod_Overlay'
    style_prefix 'mod'
    modal True
    default selectedStatementIndex = mod.PathDetection.selectedIndex
    default statements = mod.PathDetection.statements or []
    default colWidth = [mod.scalePxInt(40), mod.scalePxInt(280), mod.scalePxInt(150), mod.scalePxInt(300)]
    default selectedIndex = None

    use mod_Dialog('{mod_notl}Path options{/mod_notl}', [Hide('mod_paths'),Hide('mod_Confirm'),Hide('mod_CodeView')], icon='\uf184'):
        null height 10

        use mod_tableRow():
            label '#' xsize colWidth[0]
            label '{mod_notl}Active path{/mod_notl}' xsize colWidth[1]
            label '{mod_notl}Code{/mod_notl}' xsize colWidth[2]
            label '{mod_notl}Next label{/mod_notl}' xsize colWidth[3]

        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"

            for i,statement in enumerate(statements):
                use mod_tableRow(i):
                    hbox xsize colWidth[0] yalign .5:
                        if i < 9:
                            text If(selectedIndex==i, '{b}{u}'+str(i+1)+'{/u}{/b}', '{u}'+str(i+1)+'{/u}')
                            key 'alt_K_{}'.format(i+1) action ToggleScreenVariable('selectedIndex', i, None)
                        else:
                            text str(i+1)

                    hbox xsize colWidth[1] yalign .5:
                        hbox yalign .5:
                            if i == selectedStatementIndex:
                                use mod_messagebar('success', '{mod_notl}True{/mod_notl}')
                            else:
                                use mod_messagebar('error', '{mod_notl}False{/mod_notl}')

                        if statement.condition != 'True':
                            null width mod.scalePxInt(10)
                            use mod_iconButton('\uf1c2', If(selectedIndex==i, '{u}C{/u}ondition', '{mod_notl}Condition{/mod_notl}'), statement.OpenConditionView)
                            if selectedIndex==i:
                                key 'alt_K_c' action statement.OpenConditionView
                        elif selectedIndex==i:
                                key 'alt_K_c' action NullAction()

                    hbox xsize colWidth[2] yalign .5:
                        if statement.code:
                            use mod_iconButton('\ue86f', If(selectedIndex==i, '{u}S{/u}how', '{mod_notl}Show{/mod_notl}'), statement.OpenCodeView)
                            if selectedIndex==i:
                                key 'alt_K_s' action statement.OpenCodeView
                        else:
                            text 'Not found'
                            if selectedIndex==i:
                                key 'alt_K_s' action NullAction()

                    hbox xsize colWidth[3] yalign .5:
                        if statement.jumpTo:
                            use mod_iconButton('\ue163', If(selectedIndex==i, 'L{u}a{/u}bel', mod.scaleText(statement.jumpTo, 14, 'mod_button_text')), Show('mod_replay_jump', jumpTo=statement.jumpTo))
                            if selectedIndex==i:
                                key 'alt_K_a' action Show('mod_replay_jump', jumpTo=statement.jumpTo)
                        else:
                            text 'N/A'
                            if selectedIndex==i:
                                key 'alt_K_a' action NullAction()

                    hbox xsize mod.scalePxInt(150):
                        if statement.Action:
                            use mod_iconButton('\ue86c', If(selectedIndex==i, '{b}S{u}e{/u}lect{/b}', '{mod_notl}Select{/mod_notl}'), [statement.Action,Hide('mod_paths'),Hide('mod_CodeView')])
                            if selectedIndex==i:
                                key 'alt_K_e' action [statement.Action,Hide('mod_paths'),Hide('mod_CodeView')]
                                key 'K_KP_ENTER' action [statement.Action,Hide('mod_paths'),Hide('mod_CodeView')]
                                key 'K_RETURN' action [statement.Action,Hide('mod_paths'),Hide('mod_CodeView')]
                        else:
                            use mod_iconButton('\ue86c', '{mod_notl}Select{/mod_notl}')
                            use mod_iconButton('\ueb8b', action=mod.Confirm(title='Not forceable', prompt='This path cannot be force selected\nProbably because it\'s behind a call or jump'))
