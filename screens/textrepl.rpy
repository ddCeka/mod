
# =====================
# TEXTREPL. MAIN SCREEN
# =====================
screen URM_textrepl():
    style_prefix "mod"
    default movingOriginal = None
    default colWidth = [mod.scaleX(20), mod.scaleX(20), mod.scaleX(13)]
    default textreplPages = mod.Pages(len(mod.TextRepl.store), itemsPerPage=20)
    default listSorted = None

    python:
        if len(mod.TextRepl.store) != textreplPages.itemCount:
            SetField(textreplPages, 'itemCount', len(mod.TextRepl.store))()
    
    hbox:
        xfill True
        hbox:
            spacing 5
            if mod.URMFiles.file.filename or len(mod.TextRepl.store) > 0:
                text "Text replacements: "+str(len(mod.TextRepl.store)) yalign 0.5
                textbutton "\ue16c" style_suffix "icon_button" action If(mod.TextRepl.store.unsaved, mod.Confirm('This will clear the list below, are you sure?', Function(mod.TextRepl.clear), title='Clear list'), Function(mod.TextRepl.clear))
            else:
                text "Load a file or add text replacements using the buttons on the right"
        hbox spacing 2:
            xalign 1.0
            textbutton "\uf106" sensitive (not mod.TextRepl.incompatible) style_suffix "icon_button" hovered mod.Tooltip('Rename a character') unhovered mod.Tooltip() action Show('URM_rename_character')
            textbutton "\ue266" sensitive (not mod.TextRepl.incompatible) style_suffix "icon_button" hovered mod.Tooltip('Add text replacement') unhovered mod.Tooltip() action Show('URM_add_textrepl')
            null width mod.scalePxInt(10)
    null height mod.scalePxInt(5)
    frame style_suffix "seperator" ysize mod.scalePxInt(2)
    
    if len(mod.TextRepl.store) > 0:
        fixed ysize mod.scalePxInt(50):
            hbox xalign .5 yoffset 4 spacing 2:
                use URM_pages(textreplPages)
        # Headers
        use URM_tableRow():
            hbox xsize colWidth[0]:
                hbox:
                    label "{urm_notl}Original{/urm_notl}"
                    if listSorted == 'originalDesc':
                        textbutton '{size=-6}\ue313{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort ascending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.TextRepl.sort),SetLocalVariable('listSorted', 'originalAsc')]
                    elif listSorted == 'originalAsc':
                        textbutton '{size=-6}\ue316{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort descending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.TextRepl.sort, reverse=True),SetLocalVariable('listSorted', 'originalDesc')]
                    else:
                        textbutton '{size=-6}\ue5d7{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort ascending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.TextRepl.sort),SetLocalVariable('listSorted', 'originalAsc')]
            hbox xsize colWidth[1]:
                hbox:
                    label "{urm_notl}Replacement{/urm_notl}"
                    if listSorted == 'replacementDesc':
                        textbutton '{size=-6}\ue313{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort ascending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.TextRepl.sort, sortReplacement=True),SetLocalVariable('listSorted', 'replacementAsc')]
                    elif listSorted == 'replacementAsc':
                        textbutton '{size=-6}\ue316{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort descending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.TextRepl.sort, sortReplacement=True, reverse=True),SetLocalVariable('listSorted', 'replacementDesc')]
                    else:
                        textbutton '{size=-6}\ue5d7{/size}' yoffset mod.scalePxInt(-4) style_suffix 'icon_textbutton' hovered mod.Tooltip('{urm_notl}Sort ascending{/urm_notl}') unhovered mod.Tooltip() action [Function(mod.TextRepl.sort, sortReplacement=True),SetLocalVariable('listSorted', 'replacementAsc')]
            label "{urm_notl}Case insensitive{/urm_notl}" xsize colWidth[2]
        # Results
        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            scrollbars "vertical"

            use URM_table():
                for i,(original,replacement) in enumerate(list(mod.TextRepl.store.items())[textreplPages.pageStartIndex:textreplPages.pageEndIndex]):
                    use URM_tableRow(i, True):
                        hbox xsize colWidth[0] yalign .5:
                            text mod.scaleText(replacement['original'], 18, escapeStyling=True) substitute False
                        hbox xsize colWidth[1] yalign .5:
                            text mod.scaleText(replacement['replacement'], 18, escapeStyling=True) substitute False
                        hbox xsize colWidth[2] yalign .5:
                            text mod.scaleText(If('caseInsensitive' in replacement and replacement['caseInsensitive'], 'Yes', 'No'), 5)
                        hbox spacing 2:
                            if 'characterVar' in replacement and replacement['characterVar']:
                                use mod_iconButton('\ue3c9', '{urm_notl}Edit{/urm_notl}', Show('URM_add_textrepl', characterVar=replacement['characterVar'], defaultReplacement=replacement['replacement']))
                            else:
                                use mod_iconButton('\ue3c9', '{urm_notl}Edit{/urm_notl}', Show('URM_add_textrepl', defaultOriginal=replacement['original'], defaultReplacement=replacement['replacement'], defaultCaseInsensitive=('caseInsensitive' in replacement and replacement['caseInsensitive']), defaultReplacePartialWords=('replacePartialWords' in replacement and replacement['replacePartialWords'])))
                            use mod_iconButton('\ue872', '{urm_notl}Remove{/urm_notl}', mod.Confirm('Are you sure you want to remove this text replacement?', Function(mod.TextRepl.remove, original), title='Remove text replacement'))
                            if movingOriginal:
                                if movingOriginal == replacement['original']:
                                    use mod_iconButton('\uf230', '{urm_notl}Cancel{/urm_notl}', action=SetLocalVariable('movingOriginal', None))
                                else:
                                    use mod_iconButton('\ue55c', '{urm_notl}Before this{/urm_notl}', action=[Function(mod.TextRepl.changePos, movingOriginal, replacement['original']),SetLocalVariable('movingOriginal', None)])
                            else:
                                use mod_iconButton('\ue89f', '{urm_notl}Move{/urm_notl}', action=SetLocalVariable('movingOriginal', replacement['original']))
    else:
        vbox:
            yoffset mod.scaleY(1.5)
            xalign 0.5
            if mod.TextRepl.incompatible:
                label "Text replacement is not compatible with the used Ren'Py version" text_color "#f42929" xalign 0.5
            else:
                label "There are no text replacements" xalign 0.5

# ==================
# CHARACTER RENAMING
# ==================
screen URM_rename_character():
    layer 'Overlay'
    style_prefix "mod"
    default charFilterInput = mod.Input(autoFocus=True)

    textbutton "" style_suffix "overlay" xfill True yfill True action NullAction() at mod_fadeinout

    use mod_Dialog(title='Found '+str(len(mod.Characters.all))+' characters', closeAction=Hide('URM_rename_character'), modal=True, icon='\ue560'):
        text '{urm_notl}Selecter a character to rename{/urm_notl}'

        hbox:
            spacing 5
            text "{urm_notl}Filter: {/urm_notl}" yalign .5
            button:
                xminimum mod.scalePxInt(350)
                key_events True
                action charFilterInput.Enable()
                input value charFilterInput

        null height 2
        viewport:
            ysize mod.scalePxInt(250)
            xsize mod.scalePxInt(450)
            draggable True
            mousewheel True
            scrollbars "vertical"
            vbox spacing 2:
                for char in mod.Characters.all:
                    if char.match(str(charFilterInput)):
                        textbutton char.fullName substitute False xfill True action [Hide('URM_rename_character'),Show('URM_add_textrepl', characterVar=char.varName)]

# ====================
# Add text replacement
# ====================
screen URM_add_textrepl(characterVar=None, defaultOriginal='', defaultReplacement='', defaultCaseInsensitive=False, defaultReplacePartialWords=False, blockOriginal=False):
    layer 'Overlay'
    style_prefix "mod"
    default caseInsensitive = defaultCaseInsensitive
    default replacePartialWords = defaultReplacePartialWords
    default character = If(characterVar, mod.Characters.getByVarName(characterVar), None)
    default inputs = mod.InputGroup(
        [
            ('original', mod.Input(text=(character and character.name or defaultOriginal), editable=(not (character or blockOriginal)))),
            ('replacement', mod.Input(text=defaultReplacement)),
        ],
        focusFirst=True,
        onSubmit=[mod.TextRepl.AddReplacement(mod.GetScreenInput('original', 'inputs'), mod.GetScreenInput('replacement','inputs'), URMGetScreenVariable('characterVar'), URMGetScreenVariable('caseInsensitive'), URMGetScreenVariable('replacePartialWords')),Hide('URM_add_textrepl')]
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use mod_Dialog(title='{urm_notl}Add text replacement{/urm_notl}', closeAction=Hide('URM_add_textrepl'), modal=True, icon='\ue560'):
        text "{urm_notl}Original:{/urm_notl}"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action If(character or blockOriginal, None, inputs.original.Enable())
            input value inputs.original

        text "{urm_notl}Replacement:{/urm_notl}"
        button:
            xminimum mod.scalePxInt(450)
            key_events True
            action inputs.replacement.Enable()
            input value inputs.replacement

        if not character:
            null height 2
            vbox spacing 2:
                use mod_checkbox(checked=caseInsensitive, text='{urm_notl}Case insensitive{/urm_notl}', action=ToggleScreenVariable('caseInsensitive', True, False))
                hbox:
                    use mod_checkbox(checked=replacePartialWords, text='{urm_notl}Replace parts of words{/urm_notl}', action=ToggleScreenVariable('replacePartialWords', True, False))
                    textbutton "\ueb8b" style_suffix "icon_button" yalign .5 hovered mod.Tooltip("{urm_notl}Explain partial replacements{/urm_notl}") unhovered mod.Tooltip() action mod.Confirm("""When this option is enabled the original text will also match parts of words. Otherwise it will only match whole words\n\nExample:\nOriginal: {b}URM{/b}\nReplacement: {b}Universal Ren'Py Mod{/b}\n\nOption enabled:\n{b}URMod{/b} will become {b}Universal Ren'Py Modod{/b}\n(notice the extra {b}od{/b} because we only replaced the {b}URM{/b} part)\n\nOption disabled:\n{b}URMod{/b} will not be replace, because it doesn't match the original {b}URM{/b} as a whole word""", title='Partial replacements')
        hbox:
            yoffset mod.scalePxInt(15)
            align (1.0,1.0)
            textbutton "{urm_notl}Add{/urm_notl}" sensitive bool(str(inputs.original)) style_suffix "buttonPrimary" action inputs.onSubmit
            null width mod.scalePxInt(10)
            textbutton "{urm_notl}Cancel{/urm_notl}" action Hide('URM_add_textrepl')
