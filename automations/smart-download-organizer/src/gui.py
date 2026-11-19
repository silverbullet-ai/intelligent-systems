import customtkinter as ctk

from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from scanner import scan_folder

from categorizer import (
    load_rules,
    categorize_files,
    get_category_summary
)

from organizer import (
    create_organization_plan,
    organize_files,
    undo_organization,
    load_movement_history
)

from config_manager import (
    load_config,
    add_category,
    remove_category,
    add_extension,
    remove_extension,
    set_default_category,
    reset_config
)


class SmartDownloadOrganizer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart Download Organizer")
        self.geometry("1250x780")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.selected_folder = None
        self.files = []
        self.organization_plan = []
        self.movement_history = []

        try:
            self.movement_history = load_movement_history()
        except ValueError as error:
            messagebox.showerror("History Loading Error", str(error))

        self.create_widgets()
        self.update_undo_button()

    # ==================================================
    # MAIN GUI
    # ==================================================

    def create_widgets(self):

        self.heading = ctk.CTkLabel(
            self,
            text="Smart Download Organizer",
            font=("Segoe UI", 28, "bold")
        )
        self.heading.pack(pady=(25, 5))

        self.description = ctk.CTkLabel(
            self,
            text="Scan, categorize and organize your files intelligently.",
            font=("Segoe UI", 14)
        )
        self.description.pack(pady=(0, 20))

        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.pack(fill="x", padx=30, pady=10)

        self.folder_label = ctk.CTkLabel(
            self.folder_frame,
            text="No folder selected",
            anchor="w"
        )
        self.folder_label.pack(
            side="left", fill="x", expand=True, padx=15, pady=15
        )

        self.browse_button = ctk.CTkButton(
            self.folder_frame,
            text="Browse Folder",
            command=self.select_folder
        )
        self.browse_button.pack(side="right", padx=15, pady=10)

        self.recursive_var = ctk.BooleanVar(value=False)

        self.recursive_checkbox = ctk.CTkCheckBox(
            self,
            text="Include subfolders",
            variable=self.recursive_var
        )
        self.recursive_checkbox.pack(anchor="w", padx=35, pady=10)

        # Main actions
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(fill="x", padx=30, pady=10)

        self.scan_button = ctk.CTkButton(
            self.action_frame,
            text="Scan Folder",
            width=150,
            height=38,
            command=self.scan_selected_folder
        )
        self.scan_button.pack(side="left", padx=7, pady=12)

        self.preview_button = ctk.CTkButton(
            self.action_frame,
            text="Preview Organization",
            width=175,
            height=38,
            command=self.preview_organization,
            state="disabled"
        )
        self.preview_button.pack(side="left", padx=7, pady=12)

        self.organize_button = ctk.CTkButton(
            self.action_frame,
            text="Organize Files",
            width=145,
            height=38,
            command=self.execute_organization,
            state="disabled"
        )
        self.organize_button.pack(side="left", padx=7, pady=12)

        self.undo_button = ctk.CTkButton(
            self.action_frame,
            text="Undo Organization",
            width=165,
            height=38,
            command=self.undo_last_organization,
            state="disabled"
        )
        self.undo_button.pack(side="left", padx=7, pady=12)

        self.history_button = ctk.CTkButton(
            self.action_frame,
            text="Activity History",
            width=145,
            height=38,
            command=self.show_activity_history
        )
        self.history_button.pack(side="left", padx=7, pady=12)

        # Configuration gets its own row.
        self.settings_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.settings_frame.pack(
            fill="x", padx=30, pady=(0, 5)
        )

        self.config_button = ctk.CTkButton(
            self.settings_frame,
            text="Manage Categories & Rules",
            width=210,
            height=34,
            command=self.show_config_window
        )
        self.config_button.pack(side="right", padx=7, pady=5)

        # Statistics
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=30, pady=10)

        self.total_files_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Files: 0",
            font=("Segoe UI", 14, "bold")
        )
        self.total_files_label.pack(side="left", padx=20, pady=15)

        self.total_size_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Size: 0 B",
            font=("Segoe UI", 14, "bold")
        )
        self.total_size_label.pack(side="left", padx=20, pady=15)

        self.inaccessible_label = ctk.CTkLabel(
            self.stats_frame,
            text="Inaccessible: 0",
            font=("Segoe UI", 14, "bold")
        )
        self.inaccessible_label.pack(side="left", padx=20, pady=15)

        self.category_label = ctk.CTkLabel(
            self,
            text="Category Summary: No scan performed",
            font=("Segoe UI", 12),
            anchor="w"
        )
        self.category_label.pack(fill="x", padx=35, pady=5)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(
            fill="both", expand=True, padx=30, pady=(5, 10)
        )

        self.create_results_table()

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            font=("Segoe UI", 12)
        )
        self.status_label.pack(fill="x", padx=35, pady=(5, 15))

    # ==================================================
    # RESULTS TABLE
    # ==================================================

    def create_results_table(self):

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#242424",
            foreground="white",
            fieldbackground="#242424",
            rowheight=30,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#343638",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#1f6aa5")],
            foreground=[("selected", "white")]
        )

        columns = (
            "name",
            "extension",
            "size",
            "category",
            "details"
        )

        # Configure the table frame's grid.
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("name", text="File Name")
        self.tree.heading("extension", text="Extension")
        self.tree.heading("size", text="Size")
        self.tree.heading("category", text="Category")
        self.tree.heading(
            "details",
            text="Modified / Destination / Status"
        )

        # Column widths.
        self.tree.column(
            "name",
            width=280,
            minwidth=150,
            stretch=False
        )

        self.tree.column(
            "extension",
            width=110,
            minwidth=80,
            stretch=False
        )

        self.tree.column(
            "size",
            width=110,
            minwidth=80,
            stretch=False
        )

        self.tree.column(
            "category",
            width=150,
            minwidth=100,
            stretch=False
        )

        self.tree.column(
            "details",
            width=650,
            minwidth=300,
            stretch=False
        )

        # Scrollbars.
        self.scrollbar_y = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.scrollbar_x = ttk.Scrollbar(
            self.table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set
        )

        # Grid layout ensures both scrollbars remain visible
        # and correctly connected to the Treeview.
        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 0),
            pady=(10, 0)
        )

        self.scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 10),
            pady=(10, 0)
        )

        self.scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(10, 0),
            pady=(0, 10)
        )

    # ==================================================
    # HISTORY STATE
    # ==================================================

    def refresh_movement_history(self):

        self.movement_history = load_movement_history()
        self.update_undo_button()

    def update_undo_button(self):

        if self.movement_history:
            self.undo_button.configure(state="normal")
        else:
            self.undo_button.configure(state="disabled")

    # ==================================================
    # FOLDER SELECTION AND CLEARING
    # ==================================================

    def select_folder(self):

        folder = filedialog.askdirectory(
            title="Select a folder to organize"
        )

        if folder:
            self.selected_folder = folder
            self.folder_label.configure(text=folder)
            self.clear_results()

            self.status_label.configure(
                text="Folder selected. Ready to scan."
            )

    def clear_results(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.files = []
        self.organization_plan = []

        self.total_files_label.configure(text="Total Files: 0")
        self.total_size_label.configure(text="Total Size: 0 B")
        self.inaccessible_label.configure(text="Inaccessible: 0")

        self.category_label.configure(
            text="Category Summary: No scan performed"
        )

        self.preview_button.configure(state="disabled")
        self.organize_button.configure(state="disabled")

        self.update_undo_button()

    # ==================================================
    # SCANNING
    # ==================================================

    def scan_selected_folder(self):

        if not self.selected_folder:
            messagebox.showwarning(
                "No Folder Selected",
                "Please select a folder first."
            )
            return

        self.clear_results()

        self.scan_button.configure(
            state="disabled",
            text="Scanning..."
        )

        self.status_label.configure(text="Scanning folder...")
        self.update_idletasks()

        try:
            self.files, summary = scan_folder(
                self.selected_folder,
                recursive=self.recursive_var.get()
            )

            rules = load_rules()

            self.files = categorize_files(
                self.files,
                rules
            )

            category_summary = get_category_summary(self.files)

            for file in self.files:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        file["name"],
                        file["extension"],
                        file["size"],
                        file["category"],
                        file["modified"]
                    )
                )

            self.total_files_label.configure(
                text=f"Total Files: {summary['total_files']}"
            )

            self.total_size_label.configure(
                text=f"Total Size: {summary['total_size']}"
            )

            self.inaccessible_label.configure(
                text=f"Inaccessible: {summary['inaccessible_files']}"
            )

            category_text = " | ".join(
                f"{category}: {count}"
                for category, count in category_summary.items()
            )

            self.category_label.configure(
                text=f"Categories: {category_text or 'None'}"
            )

            if self.files:
                self.preview_button.configure(state="normal")

            self.status_label.configure(
                text=f"Scan completed. {len(self.files)} files found."
            )

        except (OSError, ValueError, KeyError) as error:

            self.files = []

            self.status_label.configure(text="Scan failed.")

            messagebox.showerror(
                "Scan Error",
                str(error)
            )

        finally:
            self.scan_button.configure(
                state="normal",
                text="Scan Folder"
            )

    # ==================================================
    # ORGANIZATION PREVIEW
    # ==================================================

    def preview_organization(self):

        if not self.files:
            messagebox.showwarning(
                "No Files",
                "Please scan a folder before generating a preview."
            )
            return

        try:
            self.organization_plan = create_organization_plan(
                self.files,
                self.selected_folder
            )

            if not self.organization_plan:

                messagebox.showinfo(
                    "Nothing to Organize",
                    "No files need to be organized."
                )

                self.organize_button.configure(state="disabled")
                return

            for item in self.tree.get_children():
                self.tree.delete(item)

            for item in self.organization_plan:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        item["name"],
                        Path(item["source"]).suffix or "No extension",
                        "-",
                        item["category"],
                        item["destination"]
                    )
                )

            self.organize_button.configure(state="normal")

            self.status_label.configure(
                text=f"Preview ready: {len(self.organization_plan)} files."
            )

            messagebox.showinfo(
                "Preview Generated",
                f"{len(self.organization_plan)} files are ready "
                "for organization.\n\n"
                "Review the proposed destinations before proceeding.\n\n"
                "No files have been moved."
            )

        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror(
                "Preview Error",
                str(error)
            )

    # ==================================================
    # EXECUTE ORGANIZATION
    # ==================================================

    def execute_organization(self):

        if not self.organization_plan:
            return

        confirmation = messagebox.askyesno(
            "Confirm Organization",
            f"Are you sure you want to organize "
            f"{len(self.organization_plan)} files?\n\n"
            "Files will be moved into category folders.\n"
            "Existing files will not be overwritten.\n"
            "You can attempt to undo successful moves afterward."
        )

        if not confirmation:
            return

        self.organize_button.configure(
            state="disabled",
            text="Organizing..."
        )

        self.update_idletasks()

        try:
            self.movement_history = organize_files(
                self.organization_plan
            )

            moved_count = sum(
                item["status"] == "Moved"
                for item in self.organization_plan
            )

            failed_count = sum(
                item["status"] != "Moved"
                for item in self.organization_plan
            )

            for item in self.tree.get_children():
                self.tree.delete(item)

            for item in self.organization_plan:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        item["name"],
                        Path(item["source"]).suffix or "No extension",
                        "-",
                        item["category"],
                        item["status"]
                    )
                )

            self.organization_plan = []

            self.update_undo_button()

            self.status_label.configure(
                text=f"Organization completed. {moved_count} files moved."
            )

            messagebox.showinfo(
                "Organization Complete",
                f"Successfully moved: {moved_count} files\n"
                f"Failed or skipped: {failed_count} files\n\n"
                "You can use Undo Organization to restore "
                "successfully moved files."
            )

        except (OSError, ValueError) as error:

            messagebox.showerror(
                "Organization Error",
                str(error)
            )

            try:
                self.refresh_movement_history()
            except ValueError:
                pass

        finally:
            self.organize_button.configure(
                state="disabled",
                text="Organize Files"
            )

    # ==================================================
    # UNDO ORGANIZATION
    # ==================================================

    def undo_last_organization(self):

        try:
            self.refresh_movement_history()

        except ValueError as error:
            messagebox.showerror("History Error", str(error))
            return

        if not self.movement_history:
            return

        confirmation = messagebox.askyesno(
            "Confirm Undo",
            f"There are {len(self.movement_history)} "
            "file movements in the saved history.\n\n"
            "Do you want to attempt to restore these files "
            "to their original locations?"
        )

        if not confirmation:
            return

        self.undo_button.configure(
            state="disabled",
            text="Restoring..."
        )

        self.update_idletasks()

        try:
            results = undo_organization(self.movement_history)

            restored = sum(
                result["status"] == "Restored"
                for result in results
            )

            failed = len(results) - restored

            self.refresh_movement_history()

            self.status_label.configure(
                text=f"Undo completed. {restored} files restored."
            )

            messagebox.showinfo(
                "Undo Completed",
                f"Successfully restored: {restored} files\n"
                f"Could not restore: {failed} files\n\n"
                "Check Activity History for remaining movements."
            )

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Undo Error",
                str(error)
            )

        finally:
            self.undo_button.configure(
                text="Undo Organization"
            )

            self.update_undo_button()

    # ==================================================
    # ACTIVITY HISTORY
    # ==================================================

    def show_activity_history(self):

        try:
            self.refresh_movement_history()

        except ValueError as error:
            messagebox.showerror("History Error", str(error))
            return

        history_window = ctk.CTkToplevel(self)

        history_window.title("Activity History")
        history_window.geometry("1050x520")
        history_window.minsize(750, 350)
        history_window.transient(self)

        heading = ctk.CTkLabel(
            history_window,
            text="Organization Activity History",
            font=("Segoe UI", 22, "bold")
        )
        heading.pack(pady=(20, 10))

        description = ctk.CTkLabel(
            history_window,
            text="Review outstanding file movements and their original locations."
        )
        description.pack(pady=(0, 15))

        summary_label = ctk.CTkLabel(
            history_window,
            text=f"Outstanding movements: {len(self.movement_history)}",
            font=("Segoe UI", 13, "bold")
        )
        summary_label.pack(pady=5)

        table_frame = ctk.CTkFrame(history_window)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "name",
            "source",
            "destination",
            "moved_at"
        )

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        tree.heading("name", text="File Name")
        tree.heading("source", text="Original Location")
        tree.heading("destination", text="Organized Location")
        tree.heading("moved_at", text="Moved At")

        tree.column("name", width=180, minwidth=120, stretch=False)
        tree.column("source", width=450, minwidth=250, stretch=False)
        tree.column("destination", width=450, minwidth=250, stretch=False)
        tree.column("moved_at", width=200, minwidth=150, stretch=False)

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 0),
            pady=(10, 0)
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 10),
            pady=(10, 0)
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(10, 0),
            pady=(0, 10)
        )

        for movement in self.movement_history:

            tree.insert(
                "",
                "end",
                values=(
                    movement.get("name", ""),
                    movement.get("source", ""),
                    movement.get("destination", ""),
                    movement.get("moved_at", "")
                )
            )

        if not self.movement_history:

            empty_label = ctk.CTkLabel(
                history_window,
                text="No outstanding organization history available.",
                font=("Segoe UI", 14)
            )

            empty_label.pack(pady=10)

        close_button = ctk.CTkButton(
            history_window,
            text="Close",
            command=history_window.destroy
        )

        close_button.pack(pady=(5, 20))

    # ==================================================
    # CONFIGURATION WINDOW
    # ==================================================

    def show_config_window(self):

        try:
            self.current_config = load_config()

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Configuration Error",
                str(error)
            )
            return

        self.config_window = ctk.CTkToplevel(self)

        self.config_window.title("Manage Categories and Rules")
        self.config_window.geometry("850x650")
        self.config_window.minsize(720, 560)
        self.config_window.transient(self)
        self.config_window.grab_set()

        self.config_window.grid_columnconfigure(0, weight=1)
        self.config_window.grid_rowconfigure(2, weight=1)

        heading = ctk.CTkLabel(
            self.config_window,
            text="Manage Categories & Rules",
            font=("Segoe UI", 23, "bold")
        )

        heading.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 4),
            sticky="w"
        )

        description = ctk.CTkLabel(
            self.config_window,
            text="Create categories, assign file extensions, and choose the default category.",
            font=("Segoe UI", 12)
        )

        description.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 12),
            sticky="w"
        )

        content_frame = ctk.CTkFrame(self.config_window)

        content_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=8,
            sticky="nsew"
        )

        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(1, weight=1)

        categories_heading = ctk.CTkLabel(
            content_frame,
            text="Categories",
            font=("Segoe UI", 15, "bold")
        )

        categories_heading.grid(
            row=0,
            column=0,
            padx=12,
            pady=(12, 6),
            sticky="w"
        )

        extensions_heading = ctk.CTkLabel(
            content_frame,
            text="Extensions in selected category",
            font=("Segoe UI", 15, "bold")
        )

        extensions_heading.grid(
            row=0,
            column=1,
            padx=12,
            pady=(12, 6),
            sticky="w"
        )

        self.category_list_frame = ctk.CTkScrollableFrame(
            content_frame,
            label_text="Select a category"
        )

        self.category_list_frame.grid(
            row=1,
            column=0,
            padx=10,
            pady=8,
            sticky="nsew"
        )

        self.extension_list = ctk.CTkTextbox(
            content_frame,
            height=250,
            font=("Consolas", 13)
        )

        self.extension_list.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
            sticky="nsew"
        )

        self.extension_list.configure(state="disabled")

        # Category controls
        category_controls = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )

        category_controls.grid(
            row=2,
            column=0,
            padx=10,
            pady=8,
            sticky="ew"
        )

        self.new_category_entry = ctk.CTkEntry(
            category_controls,
            placeholder_text="New category name"
        )

        self.new_category_entry.pack(
            fill="x",
            pady=4
        )

        ctk.CTkButton(
            category_controls,
            text="Add Category",
            command=self.add_config_category
        ).pack(fill="x", pady=4)

        ctk.CTkButton(
            category_controls,
            text="Remove Selected Category",
            fg_color="#9b3434",
            hover_color="#7d2929",
            command=self.remove_config_category
        ).pack(fill="x", pady=4)

        # Extension controls
        extension_controls = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )

        extension_controls.grid(
            row=2,
            column=1,
            padx=10,
            pady=8,
            sticky="ew"
        )

        self.new_extension_entry = ctk.CTkEntry(
            extension_controls,
            placeholder_text="Extension (e.g. .pdf)"
        )

        self.new_extension_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 6)
        )

        ctk.CTkButton(
            extension_controls,
            text="Add Extension",
            width=125,
            command=self.add_config_extension
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            extension_controls,
            text="Remove Selected",
            width=125,
            command=self.remove_config_extension
        ).pack(side="left", padx=4)

        # Default category section
        default_frame = ctk.CTkFrame(self.config_window)

        default_frame.grid(
            row=3,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )

        default_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            default_frame,
            text="Default category:",
            font=("Segoe UI", 13, "bold")
        ).grid(
            row=0,
            column=0,
            padx=12,
            pady=12,
            sticky="w"
        )

        self.default_category_entry = ctk.CTkEntry(default_frame)

        self.default_category_entry.grid(
            row=0,
            column=1,
            padx=8,
            pady=12,
            sticky="ew"
        )

        ctk.CTkButton(
            default_frame,
            text="Update Default",
            width=130,
            command=self.update_default_category
        ).grid(
            row=0,
            column=2,
            padx=12,
            pady=12
        )

        # Footer controls
        footer = ctk.CTkFrame(
            self.config_window,
            fg_color="transparent"
        )

        footer.grid(
            row=4,
            column=0,
            padx=20,
            pady=(4, 16),
            sticky="ew"
        )

        ctk.CTkButton(
            footer,
            text="Reset to Defaults",
            fg_color="#9b3434",
            hover_color="#7d2929",
            command=self.reset_configuration
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            footer,
            text="Close",
            command=self.config_window.destroy
        ).pack(side="right", padx=5)

        self.selected_config_category = None

        self.refresh_config_window()

    def refresh_config_window(self):

        self.current_config = load_config()

        for widget in self.category_list_frame.winfo_children():
            widget.destroy()

        categories = self.current_config["categories"]

        for category in categories:

            button = ctk.CTkButton(
                self.category_list_frame,
                text=category,
                anchor="w",
                command=lambda name=category: self.select_config_category(name)
            )

            button.pack(fill="x", padx=5, pady=4)

        default_category = self.current_config["default_category"]

        self.default_category_entry.delete(0, "end")
        self.default_category_entry.insert(0, default_category)

        if self.selected_config_category not in categories:

            self.selected_config_category = (
                next(iter(categories)) if categories else None
            )

        self.display_config_extensions()

    def select_config_category(self, category):

        self.selected_config_category = category
        self.display_config_extensions()

    def display_config_extensions(self):

        self.extension_list.configure(state="normal")
        self.extension_list.delete("1.0", "end")

        category = self.selected_config_category

        if category:

            extensions = self.current_config["categories"].get(
                category,
                []
            )

            self.extension_list.insert(
                "1.0",
                "\n".join(extensions) if extensions
                else "No extensions assigned."
            )

        else:
            self.extension_list.insert(
                "1.0",
                "No category selected."
            )

        self.extension_list.configure(state="disabled")

    def add_config_category(self):

        category = self.new_category_entry.get().strip()

        if not category:

            messagebox.showwarning(
                "Missing Category",
                "Enter a category name first.",
                parent=self.config_window
            )

            return

        try:
            self.current_config = add_category(
                category,
                config=self.current_config
            )

            self.new_category_entry.delete(0, "end")
            self.selected_config_category = category

            self.refresh_config_window()

            messagebox.showinfo(
                "Category Added",
                f"'{category}' was added successfully.",
                parent=self.config_window
            )

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Unable to Add Category",
                str(error),
                parent=self.config_window
            )

    def remove_config_category(self):

        category = self.selected_config_category

        if not category:

            messagebox.showwarning(
                "No Category Selected",
                "Select a category to remove.",
                parent=self.config_window
            )

            return

        if not messagebox.askyesno(
            "Confirm Removal",
            f"Remove the '{category}' category and its extension rules?",
            parent=self.config_window
        ):
            return

        try:
            self.current_config = remove_category(
                category,
                config=self.current_config
            )

            self.selected_config_category = None

            self.refresh_config_window()

            messagebox.showinfo(
                "Category Removed",
                f"'{category}' was removed.",
                parent=self.config_window
            )

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Unable to Remove Category",
                str(error),
                parent=self.config_window
            )

    def add_config_extension(self):

        category = self.selected_config_category
        extension = self.new_extension_entry.get().strip()

        if not category:

            messagebox.showwarning(
                "No Category Selected",
                "Select a category first.",
                parent=self.config_window
            )

            return

        if not extension:

            messagebox.showwarning(
                "Missing Extension",
                "Enter an extension such as .pdf.",
                parent=self.config_window
            )

            return

        try:
            self.current_config = add_extension(
                category,
                extension,
                config=self.current_config
            )

            self.new_extension_entry.delete(0, "end")
            self.refresh_config_window()

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Unable to Add Extension",
                str(error),
                parent=self.config_window
            )

    def remove_config_extension(self):

        category = self.selected_config_category

        if not category:

            messagebox.showwarning(
                "No Category Selected",
                "Select a category first.",
                parent=self.config_window
            )

            return

        try:
            selected_text = self.extension_list.get(
                "sel.first",
                "sel.last"
            ).strip()

        except Exception:
            selected_text = ""

        if not selected_text or selected_text == "No extensions assigned.":

            messagebox.showwarning(
                "No Extension Selected",
                "Highlight an extension in the list before removing it.",
                parent=self.config_window
            )

            return

        try:
            self.current_config = remove_extension(
                category,
                selected_text,
                config=self.current_config
            )

            self.refresh_config_window()

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Unable to Remove Extension",
                str(error),
                parent=self.config_window
            )

    def update_default_category(self):

        category = self.default_category_entry.get().strip()

        if not category:

            messagebox.showwarning(
                "Missing Default Category",
                "Enter a default category name.",
                parent=self.config_window
            )

            return

        try:
            self.current_config = set_default_category(
                category,
                config=self.current_config
            )

            self.refresh_config_window()

            messagebox.showinfo(
                "Default Updated",
                f"Unmatched files will be assigned to '{category}'.",
                parent=self.config_window
            )

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Unable to Update Default",
                str(error),
                parent=self.config_window
            )

    def reset_configuration(self):

        if not messagebox.askyesno(
            "Reset Configuration",
            "Restore all categories and extensions to their default settings?",
            parent=self.config_window
        ):
            return

        try:
            self.current_config = reset_config()

            self.selected_config_category = None

            self.refresh_config_window()

            messagebox.showinfo(
                "Configuration Reset",
                "The default categories and rules have been restored.",
                parent=self.config_window
            )

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Reset Failed",
                str(error),
                parent=self.config_window
            )


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================

if __name__ == "__main__":

    app = SmartDownloadOrganizer()
    app.mainloop()