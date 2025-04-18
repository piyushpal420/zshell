import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib

# Create a window
win = Gtk.Window()
win.set_title("C-QUENCE: A CUSTOM ZSHELL TERMINAL")
win.set_default_size(800, 400)

# Create VTE Terminal widget
terminal = Vte.Terminal()

# Path to your compiled shell binary (a.out)
shell_path = "/home/zephyr/Desktop/zshell/a.out"  # Update this if needed

# Launch your C shell inside the terminal
terminal.spawn_async(
    Vte.PtyFlags.DEFAULT,
    GLib.get_current_dir(),  # Use current working directory
    [shell_path],            # Command as a list
    [],                      # Environment (empty = inherit)
    GLib.SpawnFlags.DEFAULT,
    None,                    # Child setup
    None,                    # User data
    -1,                      # Timeout
    None,                    # Cancellable
    None                     # Callback
)

# Attach terminal to the window
win.add(terminal)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
