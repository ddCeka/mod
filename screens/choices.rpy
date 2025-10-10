
screen URM_choices():
    layer 'Overlay'
    style_prefix 'mod'
    modal True
    default choices = mod.Choices.currentChoices or []
    default colWidth = [mod.scalePxInt(40), mod.scalePxInt(350), mod.scalePxInt(260), mod.scalePxInt(150), mod.scalePxInt(300), mod.scalePxInt(150)]
    default selectedIndex = None

    use mod_Dialog('{urm_notl}Choices{/urm_notl}', [Hide('URM_choices'),Hide('mod_Confirm'),Hide('URM_CodeView')], icon='\ue896'):
        null height 10

        use URM_tableRow():
            label '#' xsize colWidth[0]
            label '{urm_notl}Choice{/urm_notl}' xsize colWidth[1]
            label '{urm_notl}Visible{/urm_notl}' xsize colWidth[2]
            label '{urm_notl}Code{/urm_notl}' xsize colWidth[3]
            label '{urm_notl}Next label{/urm_notl}' xsize colWidth[4]

        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"

            for i,choice in enumerate(choices):
                use URM_tableRow(i):
                    hbox xsize colWidth[0] yalign .5:
                        if i < 9:
                            text If(selectedIndex==i, '{b}{u}'+str(i+1)+'{/u}{/b}', '{u}'+str(i+1)+'{/u}')
                            key 'alt_K_{}'.format(i+1) action ToggleScreenVariable('selectedIndex', i, None)
                        else:
                            text str(i+1)

                    hbox xsize colWidth[1] yalign .5:
                        hbox:
                            text mod.scaleText(choice.text, 14) substitute False  yalign .5
                            null width mod.scalePxInt(10)
                            if choice.text in mod.TextRepl.store:
                                use mod_iconButton('\ue560', action=Show('URM_add_textrepl', defaultOriginal=choice.text, defaultReplacement=mod.TextRepl.store[choice.text]['replacement'], blockOriginal=True))
                            else:
                                use mod_iconButton('\ue560', action=Show('URM_add_textrepl', defaultOriginal=choice.text, defaultReplacement=choice.text, blockOriginal=True))

                    hbox xsize colWidth[2] yalign .5:
                        if choice.isVisible:
                            use mod_messagebar('success', '{urm_notl}True{/urm_notl}')
                        else:
                            use mod_messagebar('error', '{urm_notl}False{/urm_notl}')
                        if choice.condition != 'True':
                            null width mod.scalePxInt(10)
                            use mod_iconButton('\uf1c2', If(selectedIndex==i, '{u}C{/u}ondition', '{urm_notl}Condition{/urm_notl}'), choice.OpenConditionView)
                            if selectedIndex==i:
                                key 'alt_K_c' action choice.OpenConditionView
                        elif selectedIndex==i:
                            key 'alt_K_c' action NullAction()

                    hbox xsize colWidth[3] yalign .5:
                        if choice.code:
                            use mod_iconButton('\ue86f', If(selectedIndex==i, '{u}S{/u}how', '{urm_notl}Show{/urm_notl}'), choice.OpenCodeView)
                            if selectedIndex==i:
                                key 'alt_K_s' action choice.OpenCodeView
                        else:
                            text 'Not found'
                            if selectedIndex==i:
                                key 'alt_K_s' action NullAction()

                    hbox xsize colWidth[4] yalign .5:
                        if choice.jumpTo:
                            use mod_iconButton('\ue163', If(selectedIndex==i, 'L{u}a{/u}bel', mod.scaleText(choice.jumpTo, 14, 'URM_button_text')), Show('URM_replay_jump', jumpTo=choice.jumpTo, choiceName=choice.text))
                            if selectedIndex==i:
                                key 'alt_K_a' action Show('URM_replay_jump', jumpTo=choice.jumpTo, choiceName=choice.text)
                        else:
                            text 'N/A'
                            if selectedIndex==i:
                                key 'alt_K_a' action NullAction()

                    hbox xsize colWidth[5]:
                        use mod_iconButton('\ue86c', If(selectedIndex==i, '{b}S{u}e{/u}lect{/b}', '{urm_notl}Select{/urm_notl}'), [Hide('URM_choices'),Hide('URM_CodeView'),choice.Action], sensitive=True)
                        if selectedIndex==i:
                            key 'alt_K_e' action [Hide('URM_choices'),Hide('URM_CodeView'),choice.Action]
                            key 'K_KP_ENTER' action [Hide('URM_choices'),Hide('URM_CodeView'),choice.Action]
                            key 'K_RETURN' action [Hide('URM_choices'),Hide('URM_CodeView'),choice.Action]
