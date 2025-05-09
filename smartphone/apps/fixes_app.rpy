

init python:

    def autofixes_fix_quests():
        refresh_quests()
        fix_possible_whitespace_in_events()
        restore_events_from_flags(add_confidence=False)
        renpy.notify("Fixing Quests: DONE")


    def autofixes_fix_char_names():
        update_replacements_dict()
        renpy.notify("Fixing character names: DONE")


    def autofixes_fix_char_schedules():
        set_daily_schedules()
        choose_fixed_location_for_chars()
        renpy.notify("Fixing character schedules: DONE")


    def autofixes_fix_missing_photos():
        add_missing_photos()
        renpy.notify("Adding missing photos: DONE")


    def autofixes_fix_laptop():
        refresh_laptop_object()
        renpy.notify("Fixing Laptop/Websites: DONE")


    def autofixes_fix_phone():
        smartphone.selected_contact = None
        refresh_apps()
        sort_msg_contacts()
        check_notification()
        actualgame.laptop.turn_off(full_off=True, no_jump=True)
        actualgame.block_calls = False
        renpy.notify("Fixing Phone/Apps: DONE")


    def autofixes_fix_audio_filters():
        renpy.music.set_audio_filter("sound", None)
        renpy.music.set_audio_filter("sound2", None)
        renpy.music.set_audio_filter("sound3", None)
        renpy.music.set_audio_filter("sound4", None)
        renpy.music.set_audio_filter("ambience", None)
        renpy.music.set_audio_filter("ambience2", None)
        renpy.music.set_audio_filter("ambience3", None)
        renpy.music.set_audio_filter("video", None)
        renpy.music.set_audio_filter("music", None)
        renpy.notify("Resetting Audio Filters: DONE")


    def autofixes_check_errors():
        mandatory_dev_checks(override=True)
        renpy.notify("Checking for Errors: DONE")


    def enable_dev_mode_count(count:int):
        if(count == 5):
            config.developer = True
            config.console = True

            #console_file = renpy.game.args.basedir + "/game/console.rpy"
            console_file = config.basedir + "/game/console.rpy"
            try:
                if(not renpy.loadable(console_file)):
                    with open(console_file, "w") as f:
                        f.write("init 1000 python:\n    config.console = True")
            except:
                pass
            renpy.notify("Developer Mode activated")



screen autofixes():
    style_prefix "smartphone"

    default dev_mode_counter = 0

    vbox at phone_content_wide:
        xfill True
        yfill True

        default warning_text = "Warning! Only apply these fixes if you are actually having issues with the game!\nSave your game before using any of these fixes!"

        default bug_report_notice = "Let me know if you are experiencing any bugs via mail at chummychonka@tutanota.com or on Discord."

        text warning_text:
            color "#ff5151"

        hbox:
            xfill True
            spacing 50

            vbox:
                textbutton("- Fix Quests/Events"):
                    action Function(autofixes_fix_quests)

                textbutton("- Fix Character Names"):
                    action Function(autofixes_fix_char_names)

                textbutton("- Fix Character Schedules"):
                    action Function(autofixes_fix_char_schedules)

                textbutton("- Fix Missing Photos"):
                    action Function(autofixes_fix_missing_photos)

                textbutton("- Fix Laptop/Websites"):
                    action Function(autofixes_fix_laptop)

                textbutton("- Fix Phone/Apps"):
                    action Function(autofixes_fix_phone)

            vbox:
                #text "Debug Info":
                #    underline True
                # textbutton("Debug Info"):
                #     text_underline True
                #     text_color gui.text_color
                #     text_hover_color gui.text_color
                #     mouse "default"
                #     action SetVariable("config.developer", True)

                textbutton("Check for Errors"):
                    action Function(autofixes_check_errors)

                null height 50

                # text "Game Version: {u}v" + str(game_version) + "{/u}":
                #     size 80
                #     xalign 1.0
                textbutton("Game Version: {u}v" + str(game_version) + "{/u}"):
                    xalign 1.0
                    text_size 80
                    text_color gui.text_color
                    text_hover_color gui.text_color
                    mouse "default"
                    action [SetScreenVariable("dev_mode_counter", dev_mode_counter+1), Function(enable_dev_mode_count, dev_mode_counter)]
                text "Started Save on: {u}v" + str(starting_version) + "{/u}":
                    size 80
                    xalign 1.0

                text ("PhoneSystem: {u}v" + smartphone.version) + "{/u}":
                    size 80
                    xalign 1.0

        text bug_report_notice:
            color "#f37cf3"



