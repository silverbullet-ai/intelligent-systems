
import tkinter as tk

from src.gui import SmartDownloadOrganizer
from src.app_paths import get_resource_path


def set_application_icon(app):
    """Apply the application icon when the resource is available."""

    icon_path = get_resource_path(
        "assets/icons/app_icon.ico"
    )

    try:
        if icon_path.exists():
            app.iconbitmap(str(icon_path))

    except tk.TclError:
        # Continue launching even if the icon cannot be loaded.
        pass


def main():
    """Create and launch the application."""

    app = SmartDownloadOrganizer()
    set_application_icon(app)
    app.mainloop()


if __name__ == "__main__":
    main()
