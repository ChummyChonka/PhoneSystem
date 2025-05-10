
init python:
    def get_msgboxes_list() -> list:
        msgboxes_list = list()
        #exclude_list = [5, 6, 7]
        msgbox_list = [32, 4, 14, 30, 33, 3, 15, 18, 34, 29]
        for num in msgbox_list:
            if(num < 10):
                num = "0" + str(num)
            num = str(num)
            #msgboxes_list.append(smartphone.config["msgboxes_folder"] + "phonemsg" + num + ".webp")
            msgboxes_list.append(smartphone.config["smartphone_folder"] + "base/msgboxes/phonemsg" + num + ".webp")
        return msgboxes_list


screen settings():
    style_prefix "smartphone"
    default base_folder = "images/smartphone/base/"

    #text "Settings" at phone_title_small
    viewport at phone_content_wide:
        #area 800, 370, 2500, 1400

        vbox:
            xfill True
            #yfill True
            spacing 30
            null width 30
            hbox:
                spacing 40
                text "Enable Quick Settings:"
                if quick_menu:
                    imagebutton:
                        auto base_folder + "checkmark_filled_%s.webp"
                        at settingszoom_small
                        action [SetVariable("quick_menu", False), SetVariable("quick_menu_pref_hidden", True)]
                else:
                    imagebutton:
                        auto base_folder + "checkmark_empty_%s.webp"
                        at settingszoom_small
                        action [SetVariable("quick_menu", True), SetVariable("quick_menu_pref_hidden", False)]

            hbox:
                text _("Quick Menu Position:")
                null width 40
                if(persistent.quickmenuxalign == 0.0):
                    imagebutton:
                        #idle base_folder + "align_left_active_idle.webp"
                        idle Image(base_folder + "align_left_active_idle.svg")
                        at settingszoom_small
                        mouse "default"
                        action NullAction()
                else:
                    imagebutton:
                        #auto base_folder + "align_left_%s.webp"
                        idle Image(base_folder + "align_left_idle.svg")
                        hover Image(base_folder + "align_left_hover.svg")
                        at settingszoom_small
                        action SetVariable("persistent.quickmenuxalign", 0.0)

                if(persistent.quickmenuxalign == 0.5):
                    imagebutton:
                        idle Image(base_folder + "align_center_active_idle.svg")
                        #idle base_folder + "align_center_active_idle.webp"
                        at settingszoom_small
                        mouse "default"
                        action NullAction()
                else:
                    imagebutton:
                        #auto base_folder + "align_center_%s.webp"
                        idle Image(base_folder + "align_center_idle.svg")
                        hover Image(base_folder + "align_center_hover.svg")
                        at settingszoom_small
                        action SetVariable("persistent.quickmenuxalign", 0.5)

                if(persistent.quickmenuxalign == 1.0):
                    imagebutton:
                        #idle base_folder + "align_right_active_idle.webp"
                        idle Image(base_folder + "align_right_active_idle.svg")
                        at settingszoom_small
                        mouse "default"
                        action NullAction()
                else:
                    imagebutton:
                        #auto base_folder + "align_right_%s.webp"
                        idle Image(base_folder + "align_right_idle.svg")
                        hover Image(base_folder + "align_right_hover.svg")
                        at settingszoom_small
                        action SetVariable("persistent.quickmenuxalign", 1.0)

            hbox:
                spacing 40
                text "Extra Symbols:"
                if actualgame.extra_symbols == True:
                    imagebutton:
                        auto base_folder + "checkmark_filled_%s.webp"
                        action [SetVariable("actualgame.extra_symbols", False), SetVariable("smartphone.hide_lust_horny_icons", True)]
                        at settingszoom_small
                else:
                    imagebutton:
                        auto base_folder + "checkmark_empty_%s.webp"
                        action [SetVariable("actualgame.extra_symbols", True), SetVariable("smartphone.hide_lust_horny_icons", False)]
                        at settingszoom_small

            vbox:
                spacing 20
                hbox:
                    xfill True
                    spacing 40
                    text _("Wallpaper brightness:")
                    text str(int(smartphone.config["overlay_opacity"]*100)) + "%":
                        xalign 1.0
                #bar value VariableValue("smartphone.overlay_opacity", 1.0, step=0.05, style="slider"):
                bar value DictValue(smartphone.config, "overlay_opacity", 1.0, step=0.05, style="slider"):
                    #xsize 1000
                    xfill True
            vbox:
                xfill True
                spacing 20
                hbox:
                    xfill True
                    spacing 50
                    text _("Dialogue Box opacity:")
                    text str(int(persistent.dialogueBoxOpacity*100)) + "%":
                        xalign 1.0
                bar value VariableValue("persistent.dialogueBoxOpacity", 1.0, step=0.05, style="slider"):
                    #xsize 1000
                    xfill True

            hbox:
                spacing 40
                text _("Dialogue Box Heart overlay:")
                if actualgame.heart_overlay == True:
                    imagebutton:
                        auto base_folder + "checkmark_filled_%s.webp"
                        action SetVariable("actualgame.heart_overlay", False)
                        at settingszoom_small
                else:
                    imagebutton:
                        auto base_folder + "checkmark_empty_%s.webp"
                        action SetVariable("actualgame.heart_overlay", True)
                        at settingszoom_small


            hbox:
                spacing 40
                text "12 hour clock:"
                if smartphone.config["clock24hours"]:
                    imagebutton:
                        auto base_folder + "checkmark_empty_%s.webp"
                        at settingszoom_small
                        action Function(switch_12_hour_clock, True)
                else:
                    imagebutton:
                        auto base_folder + "checkmark_filled_%s.webp"
                        at settingszoom_small
                        action Function(switch_12_hour_clock, False)

            if(not "small" in config.variants):
                hbox:
                    spacing 40
                    text "Increase HUD size:"
                    if actualgame.increase_hud_size:
                        imagebutton:
                            auto base_folder + "checkmark_filled_%s.webp"
                            at settingszoom_small
                            action SetVariable("actualgame.increase_hud_size", False)
                    else:
                        imagebutton:
                            auto base_folder + "checkmark_empty_%s.webp"
                            at settingszoom_small
                            action SetVariable("actualgame.increase_hud_size", True)

            textbutton ("App Settings"):
                xalign 0.5
                action Function(smartphone_screen_push, "app_settings")


            # hbox:
            #     spacing 40
            #     text "Use colored map markers:"
            #     if gamemap_colored_pins:
            #         imagebutton:
            #             auto "images/smartphone/checkmark_filled_%s.webp"
            #             at settingszoom_small
            #             action SetVariable("gamemap_colored_pins", False)
            #     else:
            #         imagebutton:
            #             auto "images/smartphone/checkmark_empty_%s.webp"
            #             at settingszoom_small
            #             action SetVariable("gamemap_colored_pins", True)


screen app_settings():
    default settings_folder = smartphone.config["smartphone_folder"] + "apps/settings/"
    default msgboxes = smartphone.config["smartphone_folder"] + "base/msgboxes/"
    default messages_folder = smartphone.config["smartphone_folder"] + "apps/messages/"
    default base_folder = smartphone.config["smartphone_folder"] + "base/"

    viewport at phone_content_wide:
        draggable True
        mousewheel True
        scrollbars "vertical"

        vbox:
            xfill True

            text ("App Icons")
            add settings_folder + "app_settings_bar.webp"
            hbox:
                xalign 0.5
                spacing 50

                # OLD ICONS
                vbox:
                    vpgrid:
                        cols 4
                        spacing 10
                        for app in store.apps:
                            if(not app.disabled):
                                imagebutton:
                                    idle get_app_icon(app.name, use_old_logo=True)
                                    action NullAction()

                    textbutton("Old Icons"):
                        xalign 0.5
                        if smartphone.use_old_logos:
                            text_underline True
                            text_color gui.text_color
                        text_hover_color gui.hover_color
                        text_size 100
                        action SetVariable("smartphone.use_old_logos", True)

                # NEW ICONS
                vbox:
                    vpgrid:
                        cols 4
                        spacing 10
                        for app in store.apps:
                            if(not app.disabled):
                                imagebutton:
                                    idle get_app_icon(app.name)
                                    action NullAction()

                    textbutton("New Icons"):
                        xalign 0.5
                        if not smartphone.use_old_logos:
                            text_underline True
                            text_color gui.text_color
                        text_hover_color gui.hover_color
                        text_size 100
                        action SetVariable("smartphone.use_old_logos", False)

            null height 50
            text ("Messages App")
            add settings_folder + "app_settings_bar.webp"

            text ("Preview:")

            vbox:
                spacing 10
                xsize 1469
                xalign 0.5
                if smartphone.config["date_divider_bar"]:
                    add messages_folder + "date_divider_bar.webp":
                        ypos +70
                else:
                    null height 20

                frame:
                    if(smartphone.config["date_divider_pos"] == "left"):
                        xalign 0.1
                    if(smartphone.config["date_divider_pos"] == "center"):
                        xalign 0.5
                    if(smartphone.config["date_divider_pos"] == "right"):
                        xalign 0.9
                    background Frame(msgboxes + "phonemsg10.webp", 50,50)
                    padding (40,20)
                    if smartphone.config["date_divider_upper"]:
                        text "YESTERDAY":
                            size 50
                    else:
                        text "yesterday":
                            size 50

                frame:
                    padding (40,20)
                    background Frame (smartphone.config["msg_their_box"], 50,50)
                    xpos 0.0
                    xmaximum 1250
                    text ("This is what received messages look like."):
                        style "smartphone_msg_text"

                frame:
                    padding (40,20)
                    background Frame (smartphone.config["msg_your_box"], 50,50)
                    xalign 1.0
                    xmaximum 1250
                    text("This is what your messages look like."):
                        style "smartphone_msg_text"

            null height 50

            vbox:
                spacing 10
                text ("Their message color:")
                hbox:
                    spacing 10
                    for msgbox in get_msgboxes_list():
                        imagebutton:
                            if(smartphone.config["msg_their_box"] == msgbox):
                                idle Composite((200,200), (0,0), msgbox, (0,0), base_folder + "msgbox_selected.webp")
                                mouse "default"
                            else:
                                idle msgbox
                            action SetDict(smartphone.config, "msg_their_box", msgbox)

                text ("Your message color:")
                hbox:
                    spacing 10
                    for msgbox in get_msgboxes_list():
                        imagebutton:
                            if(smartphone.config["msg_your_box"] == msgbox):
                                idle Composite((200,200), (0,0), msgbox, (0,0), base_folder + "msgbox_selected.webp")
                                mouse "default"
                            else:
                                idle msgbox
                            action SetDict(smartphone.config, "msg_your_box", msgbox)

                null height 20

                text ("Date Divider")
                vbox:
                    xfill True
                    hbox:
                        spacing 20
                        xalign 0.5
                        textbutton ("Lowercase"):
                            if not smartphone.config["date_divider_upper"]:
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_upper", False)
                        textbutton ("Uppercase"):
                            if smartphone.config["date_divider_upper"]:
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_upper", True)

                        null width 50

                        textbutton ("Bar"):
                            if smartphone.config["date_divider_bar"]:
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_bar", True)

                        textbutton ("No Bar"):
                            if not smartphone.config["date_divider_bar"]:
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_bar", False)

                    null height 50

                    hbox:
                        spacing 20
                        xalign 0.5
                        textbutton ("Left"):
                            if(smartphone.config["date_divider_pos"] == "left"):
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_pos", "left")

                        textbutton ("Center"):
                            if(smartphone.config["date_divider_pos"] == "center"):
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_pos", "center")

                        textbutton ("Right"):
                            if(smartphone.config["date_divider_pos"] == "right"):
                                text_underline True
                            action SetDict(smartphone.config, "date_divider_pos", "right")

            null height 200

