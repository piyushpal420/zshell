import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, Gdk, Pango, GLib

class CustomShellWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Custom Shell Terminal")
        self.set_default_size(800, 400)

        # Default settings (these can be modified in the appearance dialog)
        self.bg_color = Gdk.RGBA(0, 0, 0, 1)  # Black background
        self.fg_color = Gdk.RGBA(1, 1, 1, 1)  # White text
        self.font_style = "Monospace"
        self.font_size = 12

        # Create VTE Terminal widget
        self.terminal = Vte.Terminal()

        # Set terminal appearance based on saved settings
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
        """ Set the terminal appearance based on saved settings. """
        # Apply the saved background and foreground colors
        self.terminal.set_colors(self.fg_color, self.bg_color)

        # Apply the saved font style and size
        font_desc = Pango.FontDescription(f"{self.font_style} {self.font_size}")
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
        """ Open dialog to change terminal appearance. """
        settings_dialog = Gtk.Dialog("Change Appearance", self, 0, ("Cancel", Gtk.ResponseType.CANCEL, "Apply", Gtk.ResponseType.OK))

        # Create color pickers for text and background
        color_button_bg = Gtk.ColorButton()
        color_button_fg = Gtk.ColorButton()

        # Set the initial colors to the current terminal colors
        color_button_bg.set_rgba(self.bg_color)
        color_button_fg.set_rgba(self.fg_color)

        # Create drop-down for font style (ComboBoxText)
        font_style_combobox = Gtk.ComboBoxText()
        font_styles = ["Monospace", "Arial", "Courier", "Times New Roman", "Ubuntu", "DejaVu Sans Mono"]
        for style in font_styles:
            font_style_combobox.append_text(style)
        font_style_combobox.set_active(font_styles.index(self.font_style))  # Set default to current font style

        # Create slider for font size
        font_size_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        font_size_scale.set_range(8, 30)  # Font size range from 8 to 30
        font_size_scale.set_increments(1, 1)  # Increment of 1
        font_size_scale.set_value(self.font_size)  # Set current font size

        # Add widgets to the dialog
        box = settings_dialog.get_content_area()
        box.add(Gtk.Label("Choose Background Color:"))
        box.add(color_button_bg)
        box.add(Gtk.Label("Choose Text Color:"))
        box.add(color_button_fg)
        box.add(Gtk.Label("Font Style:"))
        box.add(font_style_combobox)
        box.add(Gtk.Label("Font Size:"))
        box.add(font_size_scale)

        # Show the dialog
        settings_dialog.show_all()

        # Handle dialog response
        response = settings_dialog.run()

        if response == Gtk.ResponseType.OK:
            # Apply the selected changes to the terminal appearance
            self.bg_color = color_button_bg.get_rgba()
            self.fg_color = color_button_fg.get_rgba()

            # Apply background and foreground colors
            self.terminal.set_colors(self.fg_color, self.bg_color)

            # Get the selected font style and size
            self.font_style = font_style_combobox.get_active_text()
            self.font_size = int(font_size_scale.get_value())

            # Apply the new font style and size
            font_desc = Pango.FontDescription(f"{self.font_style} {self.font_size}")
            self.terminal.set_font(font_desc)

        # Close the dialog
        settings_dialog.destroy()

if __name__ == "__main__":
    win = CustomShellWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
