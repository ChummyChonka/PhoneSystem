

default smartphone.guide_hovered_event = None
default smartphone.guide_opened_event = None


init python:
    def set_guide_quest_number(increase=True):
        current_quest = store.quests[actualgame.guide_selected_quest].quest_id
        key_list = list(get_unlocked_quests().keys())
        counter = 0
        for q in key_list:
            if(q == current_quest):
                break
            counter += 1

        if increase:
            counter += 1
        else:
            counter -= 1

        actualgame.guide_selected_quest = [q.quest_id for q in store.quests].index(key_list[counter])


    def enable_guide_forward_arrow() -> bool:
        unlocked_quests = list(get_unlocked_quests().keys())
        the_key = store.quests[actualgame.guide_selected_quest].quest_id

        if(the_key in unlocked_quests):
            index = unlocked_quests.index(the_key)
            return index < len(unlocked_quests) - 1
        else:
            return False



screen guide():
    style_prefix "smartphone_guide"
    default base_folder = smartphone.config["smartphone_folder"] + "base/"
    default boxes_folder = smartphone.config["smartphone_folder"] + "base/msgboxes/"

    vbox at phone_content_wide:
        xfill True
        yfill True

        null height 50

        frame:
            background Frame(boxes_folder + "phonemsg18.webp", 50,50)
            padding (20,20)
            ysize 200

            hbox:
                xfill True
                xalign 0.5
                yalign 0.5

                # arrow back
                imagebutton:
                    at phone_button_zoom
                    xalign 0.3
                    if(actualgame.guide_selected_quest > 0):
                        #auto base_folder + "arrow_left_simple_%s.webp"
                        idle Image(base_folder + "arrow_left_simple_idle.svg")
                        hover Image(base_folder + "arrow_left_simple_hover.svg")
                        action Function(set_guide_quest_number, increase=False)
                    else:
                        idle base_folder + "arrow_simple_empty.webp"
                        action NullAction()
                        style "smartphone_button_inactive"

                vbox:
                    xalign 0.5
                    xsize 1200
                    hbox:
                        xalign 0.5
                        #text "[actualgame.guide_selected_quest+1] - "
                        text store.quests[actualgame.guide_selected_quest].name

                # arrow forward
                imagebutton:
                    at phone_button_zoom
                    xalign 0.7
                    if enable_guide_forward_arrow():
                        #auto base_folder + "arrow_right_simple_%s.webp"
                        idle Image(base_folder + "arrow_right_simple_idle.svg")
                        hover Image(base_folder + "arrow_right_simple_hover.svg")
                        action Function(set_guide_quest_number, increase=True)
                    else:
                        idle base_folder + "arrow_simple_empty.webp"
                        action NullAction()
                        style "smartphone_button_inactive"

        null height 50

        viewport:
            draggable True
            mousewheel True

            vbox:
                spacing 30

                for event in store.quests[actualgame.guide_selected_quest].events:
                    if event.is_unlocked():
                        hbox:
                            spacing 30
                            box_wrap True

                            frame:
                                if event.done and (smartphone.guide_hovered_event == event.event_id):
                                    background Frame(boxes_folder + "phonemsg29.webp", 50,50)
                                elif event.done:
                                    background Frame(boxes_folder + "phonemsg22.webp", 50,50)
                                elif event.locked and (smartphone.guide_hovered_event == event.event_id):
                                    background Frame(boxes_folder + "phonemsg17.webp", 50,50)
                                elif event.locked:
                                    background Frame(boxes_folder + "phonemsg16.webp", 50,50)
                                elif (smartphone.guide_hovered_event == event.event_id):
                                    background Frame(boxes_folder + "phonemsg30.webp", 50,50)
                                else:
                                    background Frame(boxes_folder + "phonemsg25.webp", 50,50)
                                padding (0,0)
                                #xmaximum 1900
                                xsize 1900
                                yminimum 200

                                vbox:
                                    #xfill True
                                    #yminimum 200
                                    #box_wrap True

                                    spacing 0

                                    if event.done:
                                        textbutton event.guide_name:
                                            xsize 1900
                                            ysize 200
                                            hovered SetVariable("smartphone.guide_hovered_event", event.event_id)
                                            unhovered SetVariable("smartphone.guide_hovered_event", None)
                                            if(smartphone.guide_opened_event == event.event_id):
                                                action SetVariable("smartphone.guide_opened_event", None)
                                            else:
                                                action SetVariable("smartphone.guide_opened_event", event.event_id)

                                        if(smartphone.guide_opened_event == event.event_id):
                                            textbutton get_event_description(event.event_id):
                                                xsize 1900
                                                text_size 65
                                                yminimum 100
                                                hovered SetVariable("smartphone.guide_hovered_event", event.event_id)
                                                unhovered SetVariable("smartphone.guide_hovered_event", None)
                                                action SetVariable("smartphone.guide_opened_event", None)

                                            null height 20

                                    elif event.locked:
                                        textbutton "Event locked":
                                            xfill True
                                            ysize 200
                                            hovered SetVariable("smartphone.guide_hovered_event", event.event_id)
                                            unhovered SetVariable("smartphone.guide_hovered_event", None)
                                            action NullAction()
                                    else:
                                        # if(event.guide_info is None):
                                        #     if(not renpy.has_label("start_select")):
                                        #         text "Get the {a=https://linktr.ee/chummychonka}{color=#3e8fff}{u}Special Edition{/u}{/color}{/a} by supporting me to unlock this event.":
                                        #             size 65
                                        #             xalign 0.5
                                        #             yalign 0.5
                                        #     else:
                                        #         text "SPECIAL EDITION EXCLUSIVE":
                                        #             xalign 0.5
                                        #             yalign 0.5
                                        # else:
                                        textbutton "Click here to get a hint...":
                                                hovered SetVariable("smartphone.guide_hovered_event", event.event_id)
                                                unhovered SetVariable("smartphone.guide_hovered_event", None)
                                                ysize 200
                                                xsize 1900
                                                if(smartphone.guide_opened_event == event.event_id):
                                                    action SetVariable("smartphone.guide_opened_event", None)
                                                else:
                                                    action SetVariable("smartphone.guide_opened_event", event.event_id)

                                        if(smartphone.guide_opened_event == event.event_id):
                                            textbutton event.get_guide_info():
                                                text_size 65
                                                hovered SetVariable("smartphone.guide_hovered_event", event.event_id)
                                                unhovered SetVariable("smartphone.guide_hovered_event", None)
                                                xsize 1900
                                                action SetVariable("smartphone.guide_opened_event", None)
                                            null height 20


                            imagebutton:
                                yalign 0.5
                                style "smartphone_button_inactive"
                                at phone_guide_checkmarks
                                if event.done:
                                    idle base_folder + "checkmark_filled_idle.webp"
                                elif event.locked:
                                    idle base_folder + "checkmark_crossed_idle.webp"
                                else:
                                    idle base_folder + "checkmark_empty_idle.webp"
                                action NullAction()

