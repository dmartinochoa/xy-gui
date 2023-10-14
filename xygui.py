import os
import threading
import customtkinter as tk
from tkinter import ttk, filedialog
import scanner
import yaml
import sv_ttk


class App(tk.CTkFrame):
    def __init__(self, parent, **kwargs):
        self.scan_tab_name = "Run Scan"

        tk.CTkFrame.__init__(self, master=parent, **kwargs)
        self.parent = parent
        self.parent.title("xy-gui")
        self.mode = 'light'

        # Create a Notebook for tabs
        self.notebook = tk.CTkTabview(master=self)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.columnconfigure(0, weight=2)
        self.rowconfigure(0, weight=2)

        # Scan Configuration Tab
        config_tab = tk.CTkFrame(self.notebook)
        self.notebook.add(self.scan_tab_name)

        # Input Directory
        self.input_label = tk.CTkLabel(master=self.notebook.tab(self.scan_tab_name), text="Select target:")
        self.input_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        self.input_directory = tk.CTkEntry(master=self.notebook.tab(self.scan_tab_name))
        self.input_directory.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.input_directory.bind("<Button-1>", lambda event: self.browse_directory())

        # Scan Options
        self.config_label = tk.CTkLabel(master=self.notebook.tab(self.scan_tab_name), text="Scan type:")
        self.config_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        max_option_length = max(len(option) for option in scanner.scan_options)
        combobox_width = max(10, max_option_length)  # Minimum width of 20
        self.scan_options = tk.CTkComboBox(master=self.notebook.tab(self.scan_tab_name), values=scanner.scan_options,
                                           width=combobox_width)
        self.scan_options.set("Full Scan")
        self.scan_options.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.scan_button = tk.CTkButton(master=self.notebook.tab(self.scan_tab_name), text="Start Scan",
                                        command=threading.Thread(target=self.start_scan).start)
        self.scan_button.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

        # Scan Details Tab
        details_frame = tk.CTkFrame(self.notebook)

        details_frame.columnconfigure(0, weight=2)
        details_frame.rowconfigure(0, weight=2)
        self.notebook.add("Scan Details")

        detail_tab = tk.CTkTabview(master=self.notebook.tab("Scan Details"))
        detail_tab.grid(row=0, column=0, padx=20, pady=15)
        detail_tab.columnconfigure(0, weight=2)
        detail_tab.rowconfigure(0, weight=2)

        # overview
        overview_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Overview")
        self.config_labelDIR = tk.CTkLabel(master=detail_tab.tab("Overview"), text="Dir: ")
        self.config_labelDIR.grid(row=1, column=0, columnspan=1, padx=5, pady=3, sticky="w")
        self.config_labelURL = tk.CTkLabel(master=detail_tab.tab("Overview"), text="Url: ")
        self.config_labelURL.grid(row=2, column=0, columnspan=1, padx=5, pady=3, sticky="w")
        self.config_labelNAME = tk.CTkLabel(master=detail_tab.tab("Overview"), text="Name: ")
        self.config_labelNAME.grid(row=3, column=0, columnspan=1, padx=5, pady=3, sticky="w")
        self.config_labelSCM = tk.CTkLabel(master=detail_tab.tab("Overview"), text="SCM: ")
        self.config_labelSCM.grid(row=4, column=0, columnspan=1, padx=5, pady=3, sticky="w")
        self.config_labelTIME = tk.CTkLabel(master=detail_tab.tab("Overview"), text="Time/Id: ")
        self.config_labelTIME.grid(row=5, column=0, columnspan=1, padx=5, pady=3, sticky="w")
        self.config_labelERRORS = tk.CTkLabel(master=detail_tab.tab("Overview"), text="Errors: ")
        self.config_labelERRORS.grid(row=6, column=0, columnspan=1, padx=5, pady=3, sticky="w")
        self.config_labelRESULTS = tk.CTkLabel(master=detail_tab.tab("Overview"), text="Summary: ")
        self.config_labelRESULTS.grid(row=7, column=0, columnspan=1, padx=5, pady=3, sticky="w")

        self.config_labelDIRv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelDIRv.grid(row=1, column=1, columnspan=2, padx=5, pady=3, sticky="w")
        self.config_labelURLv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelURLv.grid(row=2, column=1, columnspan=2, padx=5, pady=3, sticky="w")
        self.config_labelNAMEv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelNAMEv.grid(row=3, column=1, columnspan=2, padx=5, pady=3, sticky="w")
        self.config_labelSCMv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelSCMv.grid(row=4, column=1, columnspan=2, padx=5, pady=3, sticky="w")
        self.config_labelTIMEv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelTIMEv.grid(row=5, column=1, columnspan=2, padx=5, pady=3, sticky="w")
        self.config_labelERRORSv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelERRORSv.grid(row=6, column=1, columnspan=2, padx=5, pady=3, sticky="w")
        self.config_labelRESULTSv = tk.CTkLabel(master=detail_tab.tab("Overview"), text=" - ")
        self.config_labelRESULTSv.grid(row=7, column=1, columnspan=2, padx=5, pady=3, sticky="w")

        # inv
        self.inv_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Inventory")
        self.inv_tab.columnconfigure(0, weight=2)
        self.inv_tab.rowconfigure(0, weight=2)

        self.inv_labelRESULTS = tk.CTkLabel(master=detail_tab.tab("Inventory"), text='', anchor='center')
        self.inv_labelRESULTS.grid(row=0, column=0, columnspan=1, padx=15, pady=3, sticky="w", )

        # Create a Treeview widget
        self.invtree = ttk.Treeview(master=detail_tab.tab("Inventory"),
                                    columns=('Asset', 'Name', 'Severity', 'Confidence'))

        # Define column headings
        self.invtree.heading('#1', text='Asset', )
        self.invtree.heading('#2', text='Name')
        self.invtree.heading('#3', text='Type')
        self.invtree.heading('#4', text='Fully Resolved')

        # Configure column widths
        self.invtree.column('#1', width=200)
        self.invtree.column('#2', width=300)
        self.invtree.column('#3', width=200, anchor='center')
        self.invtree.column('#4', width=150, anchor='center')

        # Create a vertical scrollbar
        vsb = ttk.Scrollbar(root, orient="vertical", command=self.invtree.yview)
        self.invtree.configure(yscrollcommand=vsb.set)

        # Create a horizontal scrollbar
        hsb = ttk.Scrollbar(root, orient="horizontal", command=self.invtree.xview)
        self.invtree.configure(xscrollcommand=hsb.set)

        # Enable selection
        self.invtree.selection()

        # Use grid to place widgets
        self.invtree.grid(row=1, column=0, sticky='nsew')
        self.invtree['show'] = 'headings'

        # deps
        self.deps_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Dependencies")
        self.deps_tab.columnconfigure(0, weight=2)
        self.deps_tab.rowconfigure(0, weight=2)
        # codetamper
        self.ct_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Code Tampering")
        self.ct_tab.columnconfigure(0, weight=2)
        self.ct_tab.rowconfigure(0, weight=2)
        # secrets
        self.secret_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Secrets")
        self.secret_tab.columnconfigure(0, weight=2)
        self.secret_tab.rowconfigure(0, weight=2)
        # misconf
        self.misconf_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Misconfigurations")
        self.misconf_tab.columnconfigure(0, weight=2)
        self.misconf_tab.rowconfigure(0, weight=2)

        self.misc_labelRESULTS = tk.CTkLabel(master=detail_tab.tab("Misconfigurations"), text="Total found: -",
                                             anchor='center')
        self.misc_labelRESULTS.grid(row=0, column=0, columnspan=1, padx=15, pady=3, sticky="w", )

        # Create a Treeview widget
        self.tree = ttk.Treeview(master=detail_tab.tab("Misconfigurations"),
                                 columns=('Detector', 'Location', 'Severity', 'Confidence'))

        # Define column headings
        self.tree.heading('#1', text='Detector', )
        self.tree.heading('#2', text='Location')
        self.tree.heading('#3', text='Severity')
        self.tree.heading('#4', text='Confidence')

        # Configure column widths
        self.tree.column('#1', width=250)
        self.tree.column('#2', width=380)
        self.tree.column('#3', width=100, anchor='center')
        self.tree.column('#4', width=100, anchor='center')

        # Create a vertical scrollbar
        vsb = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Create a horizontal scrollbar
        hsb = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)

        # Enable selection
        self.tree.selection()

        # Use grid to place widgets
        self.tree.grid(row=1, column=0, sticky='nsew')
        self.tree['show'] = 'headings'

        # comp
        self.comp_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("Compliance")
        self.comp_tab.columnconfigure(0, weight=2)
        self.comp_tab.rowconfigure(0, weight=2)
        # iac
        self.iac_tab = tk.CTkFrame(detail_tab)
        detail_tab.add("IAC")
        self.iac_tab.columnconfigure(0, weight=2)
        self.iac_tab.rowconfigure(0, weight=2)

        # Settings Tab
        settings_tab = tk.CTkFrame(self.notebook)
        self.notebook.add("Settings")
        settings_tab.columnconfigure(0, weight=5)
        settings_tab.rowconfigure(0, weight=10)
        self.version_label = tk.CTkLabel(master=self.notebook.tab("Settings"), text='Version: ', anchor='w')
        self.version_label.grid(row=0, column=0, columnspan=1, padx=15, pady=3, sticky="w", )
        self.usr_label = tk.CTkLabel(master=self.notebook.tab("Settings"), text='Username: ', anchor='w')
        self.usr_label.grid(row=1, column=0, columnspan=1, padx=15, pady=3, sticky="w", )
        self.pwd_label = tk.CTkLabel(master=self.notebook.tab("Settings"), text='Password: ', anchor='w')
        self.pwd_label.grid(row=2, column=0, columnspan=1, padx=15, pady=3, sticky="w", )
        self.apikey_label = tk.CTkLabel(master=self.notebook.tab("Settings"), text='Api Token: ', anchor='w')
        self.apikey_label.grid(row=3, column=0, columnspan=1, padx=15, pady=3, sticky="w", )
        self.urlenv_label = tk.CTkLabel(master=self.notebook.tab("Settings"), text='Url: ', anchor='w')
        self.urlenv_label.grid(row=4, column=0, columnspan=1, padx=15, pady=3, sticky="w", )

        self.env_label = tk.CTkLabel(master=self.notebook.tab("Settings"), text='Environment: ', anchor='w')
        self.env_label.grid(row=6, column=0, columnspan=1, padx=15, pady=3, sticky="w", )
        self.env_menu = tk.CTkOptionMenu(master=self.notebook.tab("Settings"), values=["Pro", "Dev", "Demo", "Local"],
                                         command=self.envmenu_callback)
        self.env_menu.grid(row=6, column=1, columnspan=1, padx=15, pady=3, sticky="w", )
        self.env_menu.set('Change Environment')


        self.dark_switch = tk.CTkButton(master=self.notebook.tab("Settings"), text="Toggle Theme",
                                        command=self.change_mode)

        self.dark_switch.grid(row=10, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        var_5 = tk.DoubleVar(value=75.0)
        # Scale
        self.scale = ttk.Scale(
            config_tab,
            from_=100,
            to=0,
            variable=var_5,
            command=lambda event: var_5.set(self.scale.get()),
        )
        self.scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

    def start_scan(self):
        self.scan_button.configure(text="Running " + self.scan_options.get() + " Scan...", command=self.do_nothing)
        scanner.start_scan(self.scan_options.get(), self.input_directory.get())
        self.update_scan_details()
        self.scan_button.configure(text=" Done!", command=threading.Thread(target=self.start_scan).start)

    def envmenu_callback(self, selected_mode):
        try:
            threading.Thread(target=scanner.set_config(selected_mode))
        except:
            print('Error loading xygeni config')
        self.set_xy_conf()

    def set_xy_conf(self):
        data = scanner.get_config()
        print(data)
        self.version_label.configure(text='Version: ' + data['version'])
        self.usr_label.configure(text='Username: ' + data['api']['username'])
        self.pwd_label.configure(text='Password: ' + data['api']['password'])
        self.apikey_label.configure(text='Api Token: ' + data['api']['apikey'])
        self.urlenv_label.configure(text='Url: ' + data['api']['url'])


    def do_nothing(self):
        print(':)')

    def change_mode(self):
        if self.mode == 'dark':
            self.mode = 'light'
        else:
            self.mode = 'dark'
        gui_config['theme'] = self.mode
        tk.set_appearance_mode(self.mode)
        with open("theme/gui_config.yml", 'w') as f:
            f.write(yaml.safe_dump(gui_config))

    def browse_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.input_directory.delete(0, "end")
            self.input_directory.insert(0, selected_directory)

    def update_scan_details(self):
        scan_details = scanner.parse_results()
        errorlist = {}

        try:  # details
            self.config_labelDIRv.configure(text=scan_details.inventory_data['metadata']["directory"])
            self.config_labelURLv.configure(text=scan_details.inventory_data['metadata']["scm"]["url"])
            self.config_labelNAMEv.configure(text=scan_details.inventory_data['metadata']["scm"]["fullName"])
            self.config_labelSCMv.configure(text=scan_details.inventory_data['metadata']["scm"]["kind"].title())
            self.config_labelTIMEv.configure(text=scan_details.inventory_data['metadata']['timestamp'] + '  /  UUID: ' +
                                                  scan_details.inventory_data['metadata']['uuid'])

            if scan_details.inventory_data['errors']:
                errorlist['inv'] = scan_details.inventory_data['errors']

            # inv
            self.clear_invtreeview_data()

            asset_list = (scan_details.inventory_data['assets'])

            for val in asset_list:
                asset = val['kind'].replace("_", " ").title()
                name = val['name']
                typ = val['type'].title()
                resolved = str(val['fullyResolved']).title()

                self.invtree.insert('', 'end', values=(asset, name, typ, resolved))

            inv_stats = (str(scan_details.inventory_data['statistics']['assetsByKind']).replace("_", " ")
                         .replace("'", "").replace("{", "").replace("}", "").title())
            self.inv_labelRESULTS.configure(text=inv_stats)




        except:
            print('no inv results')

        try:  # Misconf
            self.clear_treeview_data()

            if scan_details.misconf_data['errors']:
                errorlist['misconf'] = scan_details.misconf_data['errors']
            misc_num = (scan_details.misconf_data['statistics']['misconfigurations'])
            misc_list = (scan_details.misconf_data['misconfigurations'])

            self.misc_labelRESULTS.configure(text='Total found: ' + str(misc_num))
            for val in misc_list:
                did = val['detector'].replace("_", " ").title()
                loc = val['location']['filepath']
                sev = val['severity']
                cnf = val['confidence']

                self.tree.insert('', 'end', values=(did, loc, sev.title(), cnf.title()))


        except:
            print('no misconf results')

        errorformat = ''  # Dictionary to store key-value size pairs

        for key, value in errorlist.items():
            errorformat += (key.title() + ' : ' + str(len(value)))

        self.config_labelERRORSv.configure(text=str(len(errorlist)) + ' Total  ' + str(errorformat))

    def clear_treeview_data(self):
        self.tree.delete(*self.tree.get_children())

    def clear_invtreeview_data(self):
        self.invtree.delete(*self.invtree.get_children())


if __name__ == "__main__":
    root = tk.CTk()
    root.title("")
    working_directory = '/home/daniel/PycharmProjects/xygui/'

    if not os.path.exists(working_directory):
        os.makedirs(working_directory)

    with open('theme/gui_config.yml', 'r') as file:
        gui_config = yaml.safe_load(file)

    sv_ttk.set_theme(gui_config['theme'])
    tk.set_appearance_mode(gui_config['theme'])

    app = App(root)
    app.pack(fill="both", expand=True)
    app.mode = gui_config['theme']
    app.update_scan_details()
    app.set_xy_conf()
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_coordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_coordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_coordinate, y_coordinate - 20))

    root.mainloop()
