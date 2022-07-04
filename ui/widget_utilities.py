

def clear_all_children(widget):
    if widget:
        for child in widget.winfo_children():
            child.destroy()