init python:
    #import time
    import json
    import os
    import xml.etree.ElementTree as ET

    #pressing square button
    def hide_all_phone_screens():
        store_msg_adjustment(smartphone.content_stack[len(smartphone.content_stack) - 1])
        renpy.hide_screen("call_confirmation")
        smartphone_reset_content()
        smartphone_screen_pop()

        #for i in range(len(smartphone.base_screens)):
        #    renpy.hide_screen(smartphone.base_screens[i])


    def smartphone_reset_content():
        smartphone.overlay_app_opacity = 0.0
        active_content = len(smartphone.content_stack) - 1
        renpy.hide_screen(smartphone.content_stack[active_content])
        #smartphone.content_stack = ["smartphone_apps"]
        smartphone.content_stack = ["smartphone_apps_new"]
        # if("small" in config.variants):
        #     smartphone.content_stack = ["smartphone_apps_small"]
        # else:
        #     smartphone.content_stack = ["smartphone_apps_new"]


    #pressing circle button
    def smartphone_home():
        store_msg_adjustment(smartphone.content_stack[len(smartphone.content_stack) - 1])
        for scr in smartphone.content_stack:
            if(not scr == "smartphone"):
                renpy.hide_screen(scr)
        smartphone.content_stack = ["smartphone_apps_new"]
        renpy.show_screen(smartphone.content_stack[0])
        smartphone.overlay_app_opacity = 0.0
        #smartphone_reset_content()
        #smartphone_screen_pop()
        #smartphone_update()


    def do_mini_phone():
        if smartphone.is_ringing:
            pass
        else:
            #SHOW
            if(renpy.get_screen("smartphone") is None) and (renpy.get_screen("smartphone_small") is None):
                renpy.suspend_rollback(True)
                config.rollback_enabled = False
                smartphone_update()

            #HIDE
            else:
                hide_all_phone_screens()

                renpy.suspend_rollback(False)
                config.rollback_enabled = True
                renpy.hide_screen(smartphone.content_stack[0])
                renpy.hide_screen("smartphone")


    def phone_notification():
        smartphone.notification = True
        renpy.sound.play(audio.phone_notification)


    def check_notification():
        #check if there is any notification left
        #for now only unread messages are of interest
        for k,v in store.messages.items():
            if(not k == "Eileen") and v["unread"]:
                smartphone.notification = True
                return
        smartphone.notification = False


    def set_read(contact_id):
        if(contact_id in smartphone.contacts):
            #messages[contact_id].unread = False
            store.messages[contact_id]["unread"] = False
        check_notification()


    def set_read_all():
        for contact_id in smartphone.contacts:
            set_read(contact_id)


    def set_read_all_but_unanswered():
        # don't execute on old MessageChain objects
        if(isinstance(store.messages["Aster"], MessageChain)):
            return
        for contact_id in smartphone.contacts:
            set_read(contact_id)
        check_notification()


    def contacts_add(contact_id):
        """
        Adds a contact to the phone, if it's not in there already.
        """
        if(contact_id in smartphone.contacts):
            #if config.developer:
            #    raise Exception("Tried to create duplicate entry into smartphone.contacts]!")
            return
        if(not contact_id in store.people):
            if config.developer:
                raise Exception("There is no Person object with that id!")
            return

        people[contact_id]["unknown"] = False
        smartphone.contacts.append(contact_id)
        sort_contacts()
        renpy.notify("New contact added")


    def contacts_move_up(author_id):
        if(not starting_version > 0.1) and (not game_version > 0.1):
            return
        else:
            for i in range(len(smartphone.contacts)):
                if(smartphone.contacts[i] == author_id):
                    smartphone.contacts.remove(smartphone.contacts[i])
                    smartphone.contacts.insert(0, author_id)


    def sort_contacts():
        #contacts_new = [None] * len(smartphone.contacts)
        contacts_new = []
        names_list = []

        for p in smartphone.contacts:
            names_list.append(people[p]["name"]) # get only the names to sort
        sorted_list = sorted(names_list, key=str.lower) # sort alphabetically

        for name in sorted_list:
            for p in smartphone.contacts:
                if(people[p]["name"] == name):# look for the corresponding person
                    contacts_new.append(p) # add them to our new contacts set
                    break

        smartphone.contacts = contacts_new # overwrite the actual contacts set


    def unhover_apps() -> None:
        for i in range(len(apps)):
            apps[i].hovered = False


    def smartphone_update():
        unhover_apps()
        if(not renpy.get_screen("smartphone")):
            renpy.show_screen("smartphone")
        #for i in range(len(smartphone.base_screens)):
        #    if(not renpy.get_screen(smartphone.base_screens[i])):
        #        renpy.show_screen(smartphone.base_screens[i])
                #renpy.call_screen(smartphone.base_screens[i])
        active_content = len(smartphone.content_stack) - 1
        renpy.show_screen(smartphone.content_stack[active_content])
        #renpy.call_screen(smartphone.content_stack[active_content])


    def smartphone_screen_push(new_content_screen, contact=None, img=None, vertical=False, wallpaper=None, photo=None):
        smartphone.overlay_app_opacity = 1.0
        if(new_content_screen == "contacts"):
            sort_contacts()
        #if(new_content_screen == "gallery"):
        #    smartphone.gallery.prep_page()
        # if("small" in config.variants):
        #     new_content_screen = new_content_screen + "_small"
        active_content = len(smartphone.content_stack) - 1

        # msg_chain + messages can be open at the same time
        # must make sure there is only ONE msg_chain screen at once
        if(new_content_screen == "msg_chain"):
            if("msg_chain" in smartphone.content_stack):
                #smartphone_screen_pop()
                renpy.hide_screen(smartphone.content_stack[-1])
                smartphone.content_stack.pop(len(smartphone.content_stack) - 1)
            smartphone.content_stack.append(new_content_screen)
            renpy.show_screen(new_content_screen, contact)

        elif(new_content_screen == "photo_view"):
            #renpy.show_screen(new_content_screen, contact, img, vertical, wallpaper)
            renpy.hide_screen("gallery")
            #renpy.hide_screen("msg_chain")
            renpy.hide_screen("messages")
            # if photo.vertical:
            #     renpy.show_screen("photo_view_vertical", photo)
            # else:
            #     renpy.show_screen("photo_view_horizontal", photo)
            renpy.show_screen(new_content_screen, photo)
            smartphone.content_stack.append(new_content_screen)

        else:
            renpy.hide_screen(smartphone.content_stack[active_content])
            smartphone.content_stack.append(new_content_screen)
            renpy.show_screen(new_content_screen)

        # if(not img is None):
        #     if(not contact is None):
        #         renpy.show_screen(new_content_screen, contact, img, vertical, wallpaper)
        #     else:
        #         renpy.show_screen(new_content_screen, img, vertical)
        # elif(not contact is None):
        #     renpy.show_screen(new_content_screen, contact)
        # else:
        #     renpy.show_screen(new_content_screen)


    def smartphone_screen_pop(param=None):
        if(len(smartphone.content_stack) == 1):
            return

        if("photo_view" in smartphone.content_stack):
            smartphone.photo_full = False
            #renpy.hide_screen("photo_view_horizontal")
            #renpy.hide_screen("photo_view_vertical")
            renpy.hide_screen("photo_view")
            smartphone.content_stack.remove("photo_view")
            if("gallery" in smartphone.content_stack):
                renpy.show_screen("gallery")
            else:
                renpy.show_screen("messages")
                #renpy.show_screen("msg_chain")
            return

        elif("app_settings" in smartphone.content_stack):
            renpy.hide_screen("app_settings")
            smartphone.content_stack.remove("app_settings")
            renpy.show_screen("settings")
            return

        while(True):
            unhover_apps()
            active_content = len(smartphone.content_stack) - 1
            screenname = smartphone.content_stack[active_content]
            store_msg_adjustment(screenname)
            renpy.hide_screen(screenname)
            smartphone.content_stack.pop(active_content)
            active_content = len(smartphone.content_stack) - 1 
            if(param == None):
                renpy.show_screen(smartphone.content_stack[active_content])
            else:
                renpy.show_screen(smartphone.content_stack[active_content], param)
            if(len(smartphone.content_stack) == 1):
                smartphone.overlay_app_opacity = 0.0
                break


    def store_msg_adjustment(screenname):
        if(renpy.get_screen("answer_options")):
            renpy.hide_screen("answer_options")
        #if(screenname == "msg_chain"):
        #    renpy.notify(smartphone.opened_contact.name)


    def set_app_hovered(name, val):
        for i in range(len(apps)):
            if(apps[i].name == name):
                apps[i].hovered = val


    def switch_12_hour_clock(do_12_hours=False):
        if not do_12_hours and smartphone.config["clock24hours"]:
            return
        if do_12_hours and not smartphone.config["clock24hours"]:
            return
        hours, minutes = smartphone.time.split(":")
        hours = int(hours)
        minutes = int(minutes)
        # 24h -> 12h
        if do_12_hours:
            smartphone.config["clock24hours"] = False
            if(hours > 12):
                hours -= 12
            elif(hours == 0):
                hours = 12
        # 12h -> 24h
        else:
            smartphone.config["clock24hours"] = True
            if smartphone.config["time_is_pm"] and (hours < 12):
                hours += 12
            else:
                if(hours == 12):
                    hours = 0

        if smartphone.config["clock24hours"] and hours < 12:
            smartphone.time = "0" + str(hours) + ":" + str(minutes)
        else:
            smartphone.time = str(hours) + ":" + str(minutes)


    def test_json():
        json_file = renpy.game.args.basedir + "/test_file.json"

        data_to_store = {
            "names": ["Alice", "Bob", "Xanthe"],
            "ages": [25, 30, 65],
            "scores": [85.5, 90.3, 78.0],
            "is_active": [True, False, True],
            "description": "Simple JSON storage example."
        }

        try:
            with open(json_file, "w") as file:
                json.dump(data_to_store, file, indent=4)
        except Exception as e:
            raise Exception("Could not store json file: " + json_file)


    # def save_to_json(data, file_path):
    #     """
    #     Save a dictionary of variables to a JSON file.

    #     Args:
    #         data (dict): The data to save (e.g., lists, ints, strings, booleans).
    #         file_path (str): The file path to save the JSON data.
    #     """
    #     try:
    #         with open(file_path, 'w') as file:
    #             json.dump(data, file, indent=4)
    #         print(f"Data successfully saved to '{file_path}'.")
    #     except Exception as e:
    #         print(f"An error occurred while saving data: {e}")


    # def load_from_json(file_path):
    #     """
    #     Load variables from a JSON file.

    #     Args:
    #         file_path (str): The file path of the JSON data to load.

    #     Returns:
    #         dict: The loaded data as a dictionary, or None if an error occurs.
    #     """
    #     try:
    #         with open(file_path, 'r') as file:
    #             return json.load(file)
    #     except Exception as e:
    #         print(f"An error occurred while loading data: {e}")
    #         return None


    def set_phone_battery_time():
        """
        Sets phone battery level and time to a random value dependent on daytime.
        """

        minutes = renpy.random.randint(0,59)
        # MORNING
        if(actualgame.daytime == 1):
            smartphone.battery_level = renpy.random.randint(90,100)
            hours = renpy.random.randint(7,11)
            smartphone.config["time_is_pm"] = False
        # MIDDAY
        elif(actualgame.daytime == 2):
            smartphone.battery_level = renpy.random.randint(65,80)
            smartphone.config["time_is_pm"] = True
            if smartphone.config["clock24hours"]:
                hours = renpy.random.randint(12, 16)
            else:
                hours = renpy.random.randint(0, 4)
                if(hours == 0):
                    hours = 12
        # EVENING
        elif(actualgame.daytime == 3):
            smartphone.battery_level = renpy.random.randint(25,45)
            smartphone.config["time_is_pm"] = True
            if smartphone.config["clock24hours"]:
                hours = renpy.random.randint(17,21)
            else:
                hours = renpy.random.randint(5,9)
        # NIGHT
        else:
            smartphone.battery_level = renpy.random.randint(2,14)
            smartphone.config["time_is_pm"] = True
            if smartphone.config["clock24hours"]:
                hours = renpy.random.randint(22,26)
                if(hours > 23):
                    hours -= 24
            else:
                hours = renpy.random.randint(10,14)
                if(hours > 11):
                    smartphone.config["time_is_pm"] = False
                if(hours > 12):
                    hours -= 12


        minute_string = ""
        if(minutes < 10):
            minute_string = "0" + str(minutes)
        else:
            minute_string = str(minutes)

        if smartphone.config["clock24hours"] and hours < 10:
            smartphone.time = "0" + str(hours) + ":" + minute_string
        else:
            smartphone.time = str(hours) + ":" + minute_string


    def open_phonering_screen(p_id, reject_label, accept_label):
        actualgame.extra_symbols = False
        store.phone_hud_hide = True
        if(not p_id in people):
            if config.developer:
                raise Exception("No Person by id: " + p_id)
            return
        renpy.show_screen("smartphone", True)
        renpy.show_screen("phonering", p_id, reject_label, accept_label)


    def close_phonering_screen():
        renpy.hide_screen("smartphone")
        renpy.hide_screen("phonering")
        if not smartphone.hide_lust_horny_icons:
            actualgame.extra_symbols = True
        store.phone_hud_hide = False


    def change_highlight_color():
        file_path = renpy.game.args.basedir + "/game/images/smartphone/base/smartphone(1).svg"
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Namespace handling (SVGs usually have a namespace)
        namespace = {"svg": "http://www.w3.org/2000/svg"}

        # Find all elements with a fill attribute
        for elem in root.findall(".//*[@d]", namespace):
            if elem.attrib["d"] == "M360.5 426.5L149.5 426.5L149.5 83.5L360.5 83.5Z":  
                elem.attrib["fill"] = "#ff0000"  # Change to blue

        # Save the modified SVG
        tree.write(file_path)


    def block_calls() -> bool:
        """
        returns True if phonecalls should be blocked right now
            - in story mode
            - during events
            - when actualgame.block_calls is True
        """
        if actualgame.block_calls:
            return True
        if actualgame.story_mode:
            return True
        if(not actualgame.current_event is None):
            return True

        return False


