
default smartphone.version = "1.0.1"

default smartphone.contacts = list()
default smartphone.photos = dict()
default smartphone.wallpaper = None
default smartphone.battery_level = 90
default smartphone.time = "14:12"

default smartphone.enabled = False

default smartphone.is_ringing = False
default smartphone.notification = False

default smartphone.content_stack = ["smartphone_apps_new"]

default apps = load_apps()

default smartphone.overlay_app_opacity = 0.0

default smartphone.use_old_logos = False

default smartphone.hide_lust_horny_icons = False

default smartphone.cheats_categories = ["Relationships", "Stats", "Uni"]
default smartphone.cheats_category = None



################
# Base Screens #
################
screen smartphone(for_phonecall=False):
    modal True
    style_prefix "smartphone"

    default base_folder = smartphone.config["smartphone_folder"] + "base/"
    default wallpapers = smartphone.config["smartphone_folder"] + "wallpaper/"
    default notificationbar = smartphone.config["smartphone_folder"] + "base/notificationbar/"

    if for_phonecall:
        add base_folder + "phone_new_folded.webp" at phonecall_loc
        add Crop((1567,208,706,1744), wallpapers + smartphone.wallpaper + ".webp") at phonecall_wallpaper_loc
        #add base_folder + "smartphone_overlay.webp" alpha (1-smartphone.config["overlay_opacity"]) at phonecall_loc
        add base_folder + "smartphone_overlay.webp" alpha 0.5 at phonecall_loc
        add base_folder + "smartphone_overlay.webp" alpha smartphone.overlay_app_opacity at phonecall_loc
        #add "images/smartphone/smartphone_overlay_top.webp" alpha 0.8 at phonecall_loc
    else:
        add renpy.get_showing_tags(sort=True)[0] at kawase_blur_darken
        add base_folder + "phone_new.webp"
        add wallpapers + smartphone.wallpaper + ".webp"
        add base_folder + "smartphone_overlay_wide.webp" alpha (1-smartphone.config["overlay_opacity"])
        add base_folder + "phone_app_overlay.webp" alpha smartphone.overlay_app_opacity


    if(len(smartphone.content_stack) > 0):
        if for_phonecall:
            text (actualgame.weekdays[actualgame.weekday-1]) at phonecall_notification_bar_left:
                size 35
            hbox:
                at phonecall_notification_bar_right
                imagebutton idle notificationbar + "phone_empty.webp" action NullAction() style "smartphone_button_inactive"
                null width 20
                imagebutton idle notificationbar + "phone_silent_off.webp" action NullAction() style "smartphone_button_inactive"
                null width 20
                imagebutton idle notificationbar + "wifi_connection_full.webp" action NullAction() style "smartphone_button_inactive"
                imagebutton idle notificationbar + "mobile_connection_full.webp" action NullAction() style "smartphone_button_inactive"

            text ("[smartphone.battery_level]%"):
                if(smartphone.battery_level < 5):
                    color "#D90000"
                xpos 3210
                ypos 145
                size 35

        else:
            text (actualgame.weekdays[actualgame.weekday-1]) at notificationbar_left:
                size 50
            hbox:
                # if(not for_phonecall):
                at notificationbar_right
                # else:
                    #at notificationbar_right_phonering

                #imagebutton idle "images/smartphone/notificationbar/phone_alarm.webp" action NullAction()
                imagebutton idle notificationbar + "phone_empty.webp" action NullAction() style "smartphone_button_inactive"
                null width 20
                imagebutton idle notificationbar + "phone_silent_off.webp" action NullAction() style "smartphone_button_inactive"
                null width 20
                imagebutton idle notificationbar + "wifi_connection_full.webp" action NullAction() style "smartphone_button_inactive"
                imagebutton idle notificationbar + "mobile_connection_full.webp" action NullAction() style "smartphone_button_inactive"

                #battery icon
                imagebutton:
                    if(smartphone.battery_level >= 90):
                        idle notificationbar + "battery_90.webp"
                    elif(smartphone.battery_level >= 65):
                        idle notificationbar + "battery_70.webp"
                    elif(smartphone.battery_level >= 25):
                        idle notificationbar + "battery_40.webp"
                    elif(smartphone.battery_level >= 5):
                        idle notificationbar + "battery_10.webp"
                    else:
                        idle notificationbar + "battery_0.webp"
                    action NullAction()
                    style "smartphone_button_inactive"

            text ("[smartphone.battery_level]%"):
                if(smartphone.battery_level < 5):
                    color "#D90000"
                xpos 2900
                ypos 85
                size 50

    if(len(smartphone.content_stack) <= 1) and (not for_phonecall):
        use smartphone_widget()
    use smartphone_bot_controls

    if config.developer:
        textbutton ("Phone Config"):
            xalign 1.0
            yalign 0.4
            action [Function(hide_debug_screen), Show("phone_config")]


screen smartphone_widget():
    style_prefix "smartphone"

    default widget_folder = smartphone.config["smartphone_folder"] + "base/widget/"

    hbox:
        xalign 0.5
        yalign 0.2
        spacing 20
        text smartphone.time at phone_widget:
            style "smartphone_widget"
        if(not smartphone.config["clock24hours"]):
            if smartphone.config["time_is_pm"]:
                text "pm":
                    style "smartphone_widget"
            else:
                text "am":
                    style "smartphone_widget"

    hbox:
        at phone_weather_widget
        imagebutton idle widget_folder + "phone_weather_partly_cloudy.webp" action NullAction() mouse "default"
        vbox:
            xpos 50
            text "Mostly":
                style "smartphone_weather_widget_text"
                xalign 0.5
            text "Sunny":
                style "smartphone_weather_widget_text"
                xalign 0.5
                ypos -60


screen smartphone_bot_controls():
    style_prefix "smartphone"
    default base_folder = smartphone.config["smartphone_folder"] + "base/"

    hbox at phone_bottom:
        spacing 150
        imagebutton:
            #auto base_folder + "triangle_%s.webp"
            idle Image(base_folder + "triangle_idle.svg", dpi=20)
            hover Image(base_folder + "triangle_hover.svg", dpi=20)
            action Function(smartphone_screen_pop)
            #at phone_bot_zoom

        imagebutton:
            #auto base_folder + "circle_%s.webp"
            idle Image(base_folder + "circle_idle.svg", dpi=20)
            hover Image(base_folder + "circle_hover.svg", dpi=20)
            action Function(smartphone_home)
            #at phone_bot_zoom

        imagebutton:
            #auto base_folder + "square_%s.webp"
            idle Image(base_folder + "square_idle.svg", dpi=20)
            hover Image(base_folder + "square_hover.svg", dpi=20)
            action Function(do_mini_phone)
            #at phone_bot_zoom


screen smartphone_apps_new():
    style_prefix "smartphone"
    grid 5 3 at phone_content_apps:
        #spacing 25
        for app in store.apps:
            if(app.name == "cheats") and (not renpy.has_label("start_select")):
                continue
            if(not app.disabled and app.function==AppDo.PUSH):
                vbox:
                    #xsize 250
                    xsize 400
                    #ysize 320
                    ysize 400
                    imagebutton:
                        if app.hovered:
                            #idle app.get_icon(hovered=True)
                            idle get_app_icon(app.name, hovered=True, use_old_logo=smartphone.use_old_logos)
                        else:
                            #idle app.get_icon()
                            idle get_app_icon(app.name, use_old_logo=smartphone.use_old_logos)
                        action Function(smartphone_screen_push, app.name)
                        xalign 0.5
                        hovered Function(set_app_hovered, app.name, True)
                        unhovered Function(set_app_hovered, app.name, False)

                    textbutton (app.display_name):
                        hovered Function(set_app_hovered, app.name, True)
                        unhovered Function(set_app_hovered, app.name, False)
                        action Function(smartphone_screen_push, app.name)
                        if(app.hovered):
                            text_style "smartphone_smaller_button_text_hovered"
                        else:
                            text_style "smartphone_smaller_button_text"
                        xalign 0.5
                        ypos -40

        for app in apps:
            if(not app.disabled and app.function==AppDo.URL):
                vbox:
                    #xsize 250
                    #ysize 320
                    xsize 400
                    ysize 400
                    imagebutton:
                        if app.hovered:
                            #idle app.get_icon(hovered=True)
                            idle get_app_icon(app.name, hovered=True)
                        else:
                            #idle app.get_icon()
                            idle get_app_icon(app.name)
                        action OpenURL(get_app_url(app.name))
                        xalign 0.5
                        hovered Function(set_app_hovered, app.name, True)
                        unhovered Function(set_app_hovered, app.name, False)


                    textbutton (app.display_name):
                        hovered Function(set_app_hovered, app.name, True)
                        unhovered Function(set_app_hovered, app.name, False)
                        action OpenURL(get_app_url(app.name))
                        if(app.hovered):
                            text_style "smartphone_smaller_button_text_hovered"
                        else:
                            text_style "smartphone_smaller_button_text"
                        xalign 0.5
                        ypos -40


screen phonering(p_id, reject_label, accept_label):

    default messages_folder = smartphone.config["smartphone_folder"] + "/apps/messages/"

    hbox:
        at phonecall_wallpaper_loc
        xfill True
        yfill True

        #null width 20

        #frame:
            #background Frame("images/smartphone/phonering_background.webp", 50,50)
        vbox:
            #xsize 660
            xalign 0.5
            #yalign 0.5
            ypos 50
            xsize 700
            ysize 1680
            #ysize 1200

            vbox:
                xalign 0.5
                yalign 0.3
                #xoffset 20
                #xsize 1000

                imagebutton:
                    xalign 0.5
                    idle person_get_image(p_id)
                    action NullAction()
                    mouse "default"

                null height 50

                text (person_get_phone_name(p_id)):
                    xalign 0.5
                    size 100

                null height 150

                hbox:
                    xalign 0.5

                    imagebutton:
                        idle messages_folder + "take_call_green.webp"
                        at take_call_icon_zoom
                        action [Function(close_phonering_screen), Jump(accept_label)]

                    null width 150

                    imagebutton:
                        idle messages_folder + "take_call_red.webp"
                        at take_call_icon_zoom
                        action [ Function(close_phonering_screen), Jump(reject_label)]

        #null width 20


screen mini_phone():
    default base_folder = "images/smartphone/base/"

    imagebutton:
        # if smartphone.is_ringing:
        #     if smartphone.notification:
        #         idle Composite((1000,1000), (0,0), base_folder + "smartphone_ringing_idle.webp", (0,0), base_folder + "smartphone_idle_notification.webp")
        #         hover Composite((1000,1000), (0,0), base_folder + "smartphone_ringing_hover.webp", (0,0), base_folder + "smartphone_hover_notification.webp")
        #     else:
        #         auto base_folder + "smartphone_ringing_%s.webp"
        # else:
        if not smartphone.enabled or is_in_replay():
            tooltip "Disabled"
            idle Image(base_folder + "smartphone_disabled.svg", dpi=35)
            # if smartphone.notification:
            #     idle Composite((1000,1000), (0,0), base_folder + "smartphone_disabled_idle.webp", (0,0), base_folder + "smartphone_idle_notification.webp")
            # else:
            #     idle base_folder + "smartphone_disabled_idle.webp"
        else:
            if smartphone.notification:
                idle Image(base_folder + "smartphone_notification.svg", dpi=35)
                #idle Composite((1000,1000), (0,0), base_folder + "smartphone_idle.webp", (0,0), base_folder + "smartphone_idle_notification.webp")
                #hover Composite((1000,1000), (0,0), base_folder + "smartphone_hover.webp", (0,0), base_folder + "smartphone_hover_notification.webp")
            else:
                #auto base_folder + "smartphone_%s.webp"
                #idle im.Blur(Image(base_folder + "smartphone.svg", dpi=175), 10)
                idle Image(base_folder + "smartphone.svg", dpi=35)
                #hover Image(base_folder + "smartphone_hover.svg", dpi=35)
                #hover Image(base_folder + "smartphone_hover.svg", dpi=175)
        # if("small" in config.variants) or actualgame.increase_hud_size:
        #     at mobile_phonezoom
        # else:
        #     at phonezoom
        if smartphone.enabled and not is_in_replay():
            action Function(do_mini_phone)


screen phone_config():
    add "images/bg_black.webp"
    default pers = None
    default convo_id = None

    vbox:
        xsize 3200
        ysize 2000

        null height 50

        hbox:
            xfill True
            yfill True
            viewport:
                xsize 500
                mousewheel True
                scrollbars "vertical"

                vbox:
                    for person in get_sorted_people_by_name():
                        textbutton person:
                            action SetLocalVariable("pers", person)

            viewport:
                xsize 1200
                mousewheel True
                scrollbars "vertical"
                use phone_config_person_conversations_list(pers)

            viewport:
                xsize 1469
                mousewheel True
                scrollbars "vertical"
                use phone_config_single_conversation(convo_id)

    textbutton "CLOSE":
        xalign 0.5
        yalign 1.0
        action [Function(show_debug_screen), Hide("phone_config")]


screen phone_config_person_conversations_list(pers=None):
    hbox:
        vbox:
            if(pers is None):
                text "Select Character"
            else:
                text pers:
                    underline True
                if(len(get_conversations_by_person(pers)) == 0):
                    text "No conversations"
                for convo in get_conversations_by_person(pers):
                    textbutton convo:
                        action SetScreenVariable("convo_id", convo)


screen phone_config_single_conversation(convo_id=None):
    default messages_folder = smartphone.config["smartphone_folder"] + "apps/messages/"
    default base_folder = smartphone.config["smartphone_folder"] + "base/"
    default msgboxes = smartphone.config["smartphone_folder"] + "base/msgboxes/"
    default photos_folder = smartphone.config["smartphone_folder"] + "photos/"
    default thumbnails_folder = smartphone.config["smartphone_folder"] + "photos/thumbnails/"
    default gallery_folder = smartphone.config["smartphone_folder"] + "apps/gallery/"

    vbox:
        xfill True
        spacing 10
        if(convo_id is None):
            text "Select Conversation ID"
        else:
            for msg in get_conversation_by_id(convo_id)["messages"]:
                #text msg["content"]
                #text(manipulate_text_in_brackets_dict([msg["content"]])[0])
                #text "some msg content"
                frame:
                    padding (40,20)
                    if(msg["author_id"] == "Eileen"):
                        background Frame(smartphone.config["msg_your_box"], 50,50)
                        xalign 1.0
                    else:
                        background Frame(smartphone.config["msg_their_box"], 50,50)
                        xpos 0.0
                    xmaximum 1250

                    vbox:
                        if(not msg["image"] is None) and (renpy.loadable(thumbnails_folder + "/" + msg["image"] + ".webp")):
                            hbox:
                                imagebutton:
                                    padding (20,20)
                                    idle thumbnails_folder + "/" + msg["image"] + ".webp"
                                    hover Composite((500,500),
                                        (0,0), thumbnails_folder + msg["image"] + ".webp",
                                        (0,0), gallery_folder + "photo_preview_overlay.webp"
                                    )
                                    action Function(smartphone_screen_push, "photo_view", photo=msg["image"])
                                    xalign 0.5
                                text(manipulate_text_in_brackets_dict([msg["content"]])[0]):
                                    style "smartphone_msg_text"
                                    if(msg["author_id"] == "Eileen"):
                                        text_align 0.0
                                    else:
                                        text_align 0.0
                        else:
                            text(manipulate_text_in_brackets_dict([msg["content"]])[0]):
                                style "smartphone_msg_text"
                                if(msg["author_id"] == "Eileen"):
                                    text_align 0.0
                                else:
                                    text_align 0.0



