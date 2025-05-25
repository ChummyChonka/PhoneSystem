
default smartphone.msg_age = 0
default smartphone.hovered_contact = None
default smartphone.selected_contact = "Aster"
default smartphone.choosing_answer = False

default caller_fill = ""
image caller_background = "images/phonecalls/backgrounds/phonecall_background_[caller_fill].webp"
default actualgame.callee_id = None
default actualgame.called_same_location = False
default actualgame.block_calls = True
default actualgame.phonecall_decider = 0
default actualgame.locations_decider = 0

default conversations = dict()
default messages = dict()


init python:
    last_vp_change = 0

    class OnViewportChange(Action):
        """
        Class for a 'changed' callback for a viewport whose scroll position is to be saved.
        When the viewport position changes, the __call__ function is run.
        """
        def __init__(self):
            pass
            #self.contact = contact

        def __call__(self, value):
            store.messages[smartphone.selected_contact]["scroll_position"] = value


    def initialize_adjustment():
        """
        Returns the yadjustment property for a viewport whose scroll position is to be saved.
        """
        return ui.adjustment(range=1, value=get_current_viewport_position(), changed=OnViewportChange())


    def get_current_viewport_position():
        return store.messages[smartphone.selected_contact]["scroll_position"]


    def scroll_down(contact, amount=10000):
        '''
        Increases position of viewport for Person.
        '''
        store.messages[contact]["scroll_position"] += amount
        reset_message_screen()

    # def show_screen_answers(contact, msg):
    #     if(config.developer):
    #         renpy.notify(msg.answer_options)
    #     #renpy.show_screen("answer_options", msg.answer_options)
    #     renpy.show_screen("answer_options", contact, msg)





    def reset_message_screen():
        '''
        Hides msg_chain screen and shows it again.
        '''
        if(not renpy.get_screen("messages") is None):
            smartphone_screen_pop()
            smartphone_screen_push("messages")




    def get_oldest_convo_age(p_id:str) -> int:
        if(len(store.messages[p_id]["conversations"]) == 0):
            return 0
        return store.messages[p_id]["conversations"][0]["day"]


    # def get_oldest_msg(p_id):
    #     return store.messages[p_id]["conversations"][0]["messages"]


    def add_photo(filename:str, vertical=False):
        if(filename in smartphone.photos.keys()):
            return
        smartphone.photos[filename] = {"vertical" : vertical}

        #         for photo in smartphone.photos:
#             if(photo.is_same_photo(filename)):
#                 return
#         smartphone.photos.append(Photo(filename, vertical))



#######################################################
#################### SCREENS ##########################
#######################################################


screen call_confirmation():
    modal True

    default messages_folder = smartphone.config["smartphone_folder"] + "apps/messages/"

    add messages_folder + "darken.webp"

    vbox:
        xalign 0.5
        yalign 0.5

        frame:
            #background Frame("images/smartphone/msg_chain_top_frame.webp", 50,50)
            background Frame("gui/notify.png", 50,50)
            padding (50,50)

            vbox:
                spacing 20
                text "Do you want to call " + person_get_name(smartphone.selected_contact) + "?"

                hbox:
                    xalign 0.5
                    spacing 50

                    imagebutton:
                        idle messages_folder + "take_call_green.webp"
                        at take_call_icon_zoom
                        action [SetVariable("actualgame.callee_id", smartphone.selected_contact), Jump("phonecalls_base")]

                    imagebutton:
                        idle messages_folder + "take_call_red.webp"
                        at take_call_icon_zoom
                        action Hide("call_confirmation")


screen answer_options(contact, msg):
    style_prefix "smartphone"

    default msgboxes = smartphone.config["smartphone_folder"] + "base/msgboxes/"

    frame:
        background Frame(msgboxes + "phonemsg32.webp", 50,50,50,50)
        xalign 0.85
        yalign 0.7
        hbox:
            null width 50
            vbox:
                if("small" in config.variants):
                    text _("{size=100}{u}Choose your answer:{/u}{/size}")
                else:
                    text _("{u}Choose your answer:{/u}")
                null height 50
                spacing 30

                for option in msg.answer_options:
                    frame:
                        padding (20,20)
                        background Frame(msgboxes + "phonemsg33.webp", 50,50,50,50)
                        textbutton (get_conversation_by_id(option).messages[0].content):
                            action [Function(handle_new_answer, contact, msg, option), Hide("answer_options")]
                null height 50
            null width 50


screen messages():
    style_prefix "smartphone"

    default messages_folder = smartphone.config["smartphone_folder"] + "apps/messages/"

    viewport at phone_msg_content_wide_left:
        mousewheel True
        draggable True

        vbox:
            #for p_id in smartphone.contacts if(not store.messages[p_id]["last_message"] is None):
            for p_id in get_smartphone_contacts_with_messages(fill_empty=True):
                frame:
                    ysize 260
                    xsize 740

                    if(p_id == "empty"):
                        background Frame(messages_folder + "messages_frame_empty.webp", 50,50)
                    else:
                        if(messages[p_id]["unread"]):
                            if(smartphone.hovered_contact == p_id):
                                background Frame(messages_folder + "messages_frame_unread_hover.webp", 50,50)
                            else:
                                background Frame(messages_folder + "messages_frame_unread.webp", 50,50)
                        else:
                            if(smartphone.hovered_contact == p_id):
                                background Frame(messages_folder + "messages_frame_hovered.webp", 50,50)
                            else:
                                background Frame(messages_folder + "messages_frame.webp", 50,50)

                        hbox:
                            ypos -10
                            vbox:
                                yfill True
                                xsize 120

                                imagebutton:
                                    #xsize 200
                                    yfill True
                                    xalign 0.5
                                    yalign 0.5
                                    idle person_get_small_image(p_id)
                                    hovered SetVariable("smartphone.hovered_contact", p_id)
                                    unhovered SetVariable("smartphone.hovered_contact", None)
                                    action [Function(set_read, p_id), SetVariable("smartphone.selected_contact", p_id), Function(reset_message_screen)]
                            vbox:
                                ypos -20
                                xfill True
                                hbox:
                                    xfill True
                                    if person_is_unknown(p_id):
                                        textbutton ("Unknown"):
                                            if(smartphone.hovered_contact == p_id):
                                                text_color "#e06666"
                                            xfill True
                                            text_bold True
                                            text_kerning 7
                                            hovered SetVariable("smartphone.hovered_contact", p_id)
                                            unhovered SetVariable("smartphone.hovered_contact", None)
                                            action [Function(set_read, p_id), SetVariable("smartphone.selected_contact", p_id), Function(reset_message_screen)]
                                    else:
                                        textbutton person_get_display_name(p_id):
                                            if(smartphone.hovered_contact == p_id):
                                                text_color "#e06666"
                                            xfill True
                                            text_bold True
                                            text_kerning 7
                                            hovered SetVariable("smartphone.hovered_contact", p_id)
                                            unhovered SetVariable("smartphone.hovered_contact", None)
                                            action [Function(set_read, p_id), SetVariable("smartphone.selected_contact", p_id), Function(reset_message_screen)]

                                    if messages[p_id]["unread"]:
                                        add messages_folder + "message_unread_marker.webp" yalign 0.5 xpos -100

                                if(not messages[p_id]["last_message"] is None):
                                    #manipulate_text_in_brackets_dict
                                    textbutton (manipulate_text_in_brackets_dict([get_last_message_shortened(p_id, 55)])):
                                        style_prefix "smartphone_last_msg"
                                        xpos +20
                                        #xsize 550
                                        xfill True
                                        ysize 100
                                        ypos -10
                                        hovered SetVariable("smartphone.hovered_contact", p_id)
                                        unhovered SetVariable("smartphone.hovered_contact", None)
                                        action [Function(set_read, p_id), SetVariable("smartphone.selected_contact", p_id), Function(reset_message_screen)]

    use msg_chain


screen msg_chain():
    default messages_folder = smartphone.config["smartphone_folder"] + "apps/messages/"
    default base_folder = smartphone.config["smartphone_folder"] + "base/"
    default msgboxes = smartphone.config["smartphone_folder"] + "base/msgboxes/"
    default photos_folder = smartphone.config["smartphone_folder"] + "photos/"
    default thumbnails_folder = smartphone.config["smartphone_folder"] + "photos/thumbnails/"
    default gallery_folder = smartphone.config["smartphone_folder"] + "apps/gallery/"

    vbox at phone_msg_content_wide_right:
        if(smartphone.selected_contact is None):
            null height 100
        else:
            $ set_read(smartphone.selected_contact)
            $ reset_msg_age()
            vbox:
                xfill True

                frame:
                    background Frame(messages_folder + "msg_chain_top_frame.webp", 50,50)
                    xfill True
                    xpadding 50

                    hbox:
                        xfill True
                        ysize 100

                        hbox:
                            xalign 0.0
                            spacing 30
                            add person_get_image(smartphone.selected_contact) at contactzoom
                            if person_is_unknown(smartphone.selected_contact):
                                text "Unknown":
                                    yalign 0.5
                            else:
                                text person_get_display_name(smartphone.selected_contact):
                                    yalign 0.5

                        imagebutton:
                            yalign 0.5
                            xalign 1.0
                            at phone_message_call_button
                            if block_calls():
                                idle base_folder + "phonecall_disabled.webp"
                                action NullAction()
                                tooltip "You can only make phonecalls outside of events"
                                mouse "default"
                            else:
                                auto base_folder + "phonecall_%s.webp"
                                action [SetVariable("actualgame.callee_id", smartphone.selected_contact), Show("call_confirmation")]

                hbox:
                    xfill True
                    null width 30

                    viewport id "msg_chain":
                        mousewheel True
                        draggable True
                        #yadjustment initialize_adjustment(smartphone.selected_contact)
                        yadjustment initialize_adjustment()

                        vbox:
                            xfill True
                            spacing 10

                            #null height 20

                            # if smartphone.config["date_divider_bar"]:
                            #     add messages_folder + "date_divider_bar.webp":
                            #         ypos +70
                            # else:
                            #     null height 20
                            # frame:
                            #     if(smartphone.config["date_divider_pos"] == "left"):
                            #         xalign 0.1
                            #     if(smartphone.config["date_divider_pos"] == "center"):
                            #         xalign 0.5
                            #     if(smartphone.config["date_divider_pos"] == "right"):
                            #         xalign 0.9
                            #     background Frame(msgboxes + "phonemsg10.webp", 50,50)
                            #     padding (40,20)
                                #text get_msg_age_text(store.messages[smartphone.selected_contact].messages[0]):
                                #text get_msg_age_text(get_oldest_convo_age(smartphone.selected_contact)):
                                #text "HUHRENSOHN":
                                #    size 50
                                #$ set_msg_divider_age(store.messages[smartphone.selected_contact].messages[0])
                            $ set_msg_divider_age(get_oldest_convo_age(smartphone.selected_contact))


                            #for msg in messages[smartphone.selected_contact].messages:
                            for msg in get_messages_from_applied_conversations(smartphone.selected_contact):
                                if put_day_divider(msg):
                                    null height 20

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
                                        text get_msg_age_text(msg):
                                            size 50

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
                                        # works when game is run straight from renpy, not in release version though
                                        #if(not msg["image"] is None) and (("android" in config.variants) or (renpy.loadable(thumbnails_folder + "/" + msg["image"] + ".webp"))):
                                        if(not msg["image"] is None):
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

                                #if(msg == messages[smartphone.selected_contact]["last_message"]):
                                if(msg == get_messages_from_applied_conversations(smartphone.selected_contact)[-1]):

                                    # add to contacts button
                                    if person_is_unknown(smartphone.selected_contact):
                                        frame:
                                            padding (20,20)
                                            background Frame(msgboxes + "phonemsg33.webp", 50,50,50,50)
                                            xalign 1.0
                                            hbox:
                                                null width 100
                                                textbutton _("Add to contacts"):
                                                    #action Function(contacts_add, smartphone.selected_contact)
                                                    action Function(person_add_to_contacts, smartphone.selected_contact)
                                                null width 100

                                    #elif((not msg.answer_options is None) and (not msg.answered)):
                                    elif(not msg.get("answer_options") is None) and (msg.get("answered") is None):
                                        # choose answer button
                                        if(not smartphone.choosing_answer):
                                            frame:
                                                padding (20,20)
                                                background Frame(msgboxes + "phonemsg33.webp", 50,50,50,50)
                                                xalign 1.0
                                                hbox:
                                                    null width 100
                                                    textbutton ("choose answer..."):
                                                        #text_hover_color "#000000"
                                                        action [SetVariable("smartphone.choosing_answer", True), Function(scroll_down, smartphone.selected_contact)]
                                                    null width 100

                                        # actual answer options
                                        else:
                                            frame:
                                                background Frame(msgboxes + "phonemsg32.webp", 50,50,50,50)
                                                xfill True
                                                hbox:
                                                    vbox:
                                                        xfill True
                                                        spacing 30
                                                        text _("Choose your answer:"):
                                                            underline True
                                                            if("small" in config.variants):
                                                                size 100
                                                        #for option in msg.answer_options:
                                                        for option in msg["answer_options"]:
                                                            frame:
                                                                padding (20,20)
                                                                xalign 0.5
                                                                background Frame(msgboxes + "phonemsg33.webp", 50,50,50,50)
                                                                #textbutton manipulate_text_in_brackets_dict([get_conversation_by_id(option).messages[0]["content"]]):
                                                                textbutton manipulate_text_in_brackets_dict([get_conversation_by_id(option)["messages"][0]["content"]]):
                                                                    #text_hover_color "#000000"
                                                                    action [Function(handle_new_answer, smartphone.selected_contact, msg, option), SetVariable("smartphone.choosing_answer", False)]

                    null width 100

