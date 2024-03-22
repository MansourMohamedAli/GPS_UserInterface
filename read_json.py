clients_from_json = {"VB1": ["199.199.199.01", "MAC1"],
                     "VB2": ["199.199.199.02", "MAC2"],
                     "VB3": ["199.199.199.03", "MAC3"],
                     "VB4": ["199.199.199.01", "MAC4"],
                     "VB5": ["199.199.199.01", "MAC1"],
                     "VB6": ["199.199.199.02", "MAC2"],
                     "VB7": ["199.199.199.03", "MAC3"],
                     "VB8": ["199.199.199.01", "MAC4"],
                     "VB9": ["199.199.199.01", "MAC4"]}

commands_from_json = {"Load Graphic 1": "111",
                      "Load Graphic 2": "222",
                      "Load Graphic 3": "333",
                      "Load Graphic 4": "444",
                      "Load Graphic 5": "555"}

tab_clients_from_json = {"Tab 1": ["VB1", "VB2", "VB3"],
                         "Tab 2": ["VB4", "VB5", "VB6"],
                         "Tab 3": ["VB7", "VB8", "VB9"]}

tab_commands_from_json = {"1": [["Load_tab1", "Load_tab2", "Load_tab3"], ["test"], [None]],
                          "2": [["Load_tab4", "Load_tab5", "Load_tab6"], [None], [None]],
                          "3": [["Load_tab7", "Load_tab8", "Load_tab9"], [None], [None]]}

configurations = {"load1": [clients_from_json, commands_from_json, tab_clients_from_json, tab_commands_from_json],
                  "load2": ["clients", "commands", "tab_clients", "tab_commands"]}

