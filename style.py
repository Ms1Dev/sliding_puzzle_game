from tkinter import ttk

# configuring the style for ttk widgets in a seperate module then importing to main to reduce clutter

def configuration():
    """Configure the style of all ttk widgets"""
    style = ttk.Style()
    style.theme_use('clam')

    # three colours used for theme
    bgColour = '#071B22' # main background colour
    bgColourAlt = '#01363F' # slightly lighter bg colour used for headings
    fgColour = '#5FC7C7' # light blue for text and borders

    style.configure('TButton', 
        background=bgColour, 
        foreground=fgColour, 
        bordercolor=fgColour
    )
    style.map('TButton',
        background=[('active', bgColourAlt), ('!active', bgColour)]
    )
    style.configure('Treeview', 
        background=bgColour,
        fieldbackground=bgColour, 
        foreground=fgColour, 
        bordercolor=fgColour
    )
    style.configure('Treeview.Heading', 
        background=bgColourAlt, 
        foreground=fgColour, 
        bordercolor=fgColour
    )
    # prevent headings changing colour on hover as they do not do anything
    style.map('Treeview.Heading', 
        background=[('active', bgColourAlt)]
    )
    style.configure('TFrame', 
        background=bgColour, 
        foreground=fgColour,
        borderwidth=2,
        bordercolor=fgColour
    )
    style.configure('Header.TFrame', 
        background=bgColourAlt, 
        foreground=fgColour,
        bordercolor=fgColour
    )
    style.configure('TLabelframe', 
        background=bgColour, 
        foreground=fgColour, 
        bordercolor=fgColour
    )
    style.configure('TLabelframe.Label', 
        background=bgColour, 
        foreground=fgColour
    )
    style.configure('TLabel', 
        background=bgColourAlt, 
        foreground=fgColour
    )
    style.configure('Dark.Label', 
        background=bgColour, 
        foreground=fgColour,
        anchor='center'
    )

    return style