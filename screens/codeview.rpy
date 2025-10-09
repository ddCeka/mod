
screen URM_CodeView(code, title='{urm_notl}Codeview{/urm_notl}', icon='\ue86f', details=None, detailsTitle=None):
    layer 'Overlay'
    style_prefix 'mod'
    default colorized = mod.CodeView.colorize(code)

    use mod_Dialog(title, Hide('URM_CodeView'), icon=icon, backgroundColor=mod.CodeView.colors['background'], details=details, detailsTitle=detailsTitle):
        vpgrid: # We need a vpgrid, because a viewport takes up all available height
            cols 1
            draggable True
            mousewheel True
            scrollbars "vertical"
            ymaximum mod.scaleY(60)

            text colorized size mod.scalePxInt(22) substitute False
