import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, Gdk, Pango, GLib

class CustomShellWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Custom Shell Terminal")
        self.set_default_size(800, 400)

        # Create VTE Terminal widget
        self.terminal = Vte.Terminal()

        # Set terminal appearance
        self.set_terminal_appearance()

        # Create and add a button to change appearance
        self.settings_button = Gtk.Button(label="Change Appearance")
        self.settings_button.connect("clicked", self.on_settings_button_clicked)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.terminal, True, True, 0)
        box.pack_start(self.settings_button, False, False, 0)
        self.add(box)

        # Start the shell process
        self.start_shell()

    def set_terminal_appearance(self):
        """ Set the initial terminal appearance. """
        # Set background color (black) using VTE's set_colors method
        self.terminal.set_colors(Gdk.RGBA(1, 1, 1, 1), Gdk.RGBA(0, 0, 0, 1))  # White text on black background

        # Set the font size and style using Pango.FontDescription
        font_desc = Pango.FontDescription("Monospace 12")
        self.terminal.set_font(font_desc)

    def start_shell(self):
        """ Start the shell process in the terminal. """
        shell_path = "./a.out"  # Path to your shell executable
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,                          # Working directory (None = current)
            [shell_path],                  # Command as a list
            [],                            # Environment (empty = inherit)
            GLib.SpawnFlags.DEFAULT,
            None,                          # Child setup
            None,                          # User data
            -1,                            # Timeout
            None,                          # Cancellable
            None                           # Callback
        )

    def on_settings_button_clicked(self, button):
        """ Change terminal appearance on button click. """
        settings_dialog = Gtk.Dialog("Change Appearance", self, 0, ("Cancel", Gtk.ResponseType.CANCEL, "Apply", Gtk.ResponseType.OK))

        # Create color pickers for text and background
        color_button_bg = Gtk.ColorButton()
        color_button_fg = Gtk.ColorButton()

        # Set the initial colors to the current terminal colors
        color_button_bg.set_rgba(Gdk.RGBA(0, 0, 0, 1))  # Black background
        color_button_fg.set_rgba(Gdk.RGBA(1, 1, 1, 1))  # White text

        # Add widgets to the dialog
        box = settings_dialog.get_content_area()
        box.add(Gtk.Label("Choose Background Color:"))
        box.add(color_button_bg)
        box.add(Gtk.Label("Choose Text Color:"))
        box.add(color_button_fg)

        # Show the dialog
        settings_dialog.show_all()

        # Handle dialog response
        response = settings_dialog.run()

        if response == Gtk.ResponseType.OK:
            # Apply the selected changes to the terminal appearance
            bg_color = color_button_bg.get_rgba()
            fg_color = color_button_fg.get_rgba()

            # Apply background and foreground colors
            self.terminal.set_colors(fg_color, bg_color)

        # Close the dialog
        settings_dialog.destroy()

if __name__ == "__main__":
    win = CustomShellWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
