init python:
    def set_current_contact(p_id: str):
        if(p_id == ""):
            smartphone.selected_contact = None
        else:
            smartphone.selected_contact = p_id


screen stats():
    style_prefix "smartphone"
    #text "Stats" at phone_title_small
    #add "images/smartphone/phone_app_overlay.webp"
    #add "images/smartphone/phone_app_overlay_top.webp"
    viewport at phone_content_wide_left:
        #area 700, 370, 2500, 1400
        draggable True
        mousewheel True

        vbox:
            #style "smartphone_area_small"
            #xsize 1200
            xfill True
            #yfill True
            xalign 0.5
            spacing 75

            hbox:
                xfill True
                text "{u}" + person_get_name('Eileen') + "{/u}"
                hbox:
                    xalign 1.0
                    text _("$")
                    text str(protagonist.get_stat(Stats.MONEY))

            null height 20

            vbox:
                spacing 10
                xfill True
                hbox:
                    xfill True
                    text _("Self-Confidence:")
                    text "[protagonist.confidence]":
                        xalign 1.0
                bar value StaticValue(value=protagonist.confidence, range=10)

            vbox:
                spacing 10
                xfill True
                hbox:
                    xfill True
                    text _("Fitness:")
                    text "[protagonist.fitness]":
                        xalign 1.0
                bar value StaticValue(value=protagonist.fitness, range=10)

            vbox:
                spacing 10
                xfill True
                hbox:
                    xfill True
                    text _("Lust Energy:")
                    text str(protagonist.get_stat(Stats.LUST_ENERGY)):
                        xalign 1.0
                bar value StaticValue(value=protagonist.get_stat(Stats.LUST_ENERGY), range=10)

            vbox:
                spacing 10
                xfill True
                hbox:
                    xfill True
                    text _("Horniness:")
                    text str(protagonist.get_stat(Stats.HORNY)):
                        xalign 1.0
                bar value StaticValue(value=protagonist.get_stat(Stats.HORNY), range=10)

            # vbox:
            #     spacing 10
            #     xfill True
            #     hbox:
            #         xfill True
            #         text _("Fighting Ability:")
            #         text "[protagonist.fight]":
            #             xalign 1.0
            #     bar value StaticValue(value=protagonist.fight, range=10)


    viewport at phone_content_wide_right:
        mousewheel True
        draggable True
        scrollbars "vertical"

        vbox:
            spacing 10
            for p_id in smartphone.contacts:
                frame:
                    #background Frame("images/smartphone/msgboxes/phonemsg31.webp", 50,50)
                    background Frame("gui/notify.png", 50,50)

                    padding (0,50)

                    has hbox:
                        #xfill True
                        xsize 1000
                        ysize 200
                        #spacing 20

                        imagebutton:
                            yalign 0.5
                            xpos 20
                            idle person_get_image(p_id)
                            at contactzoom_small
                            mouse "default"
                            action NullAction()
                            #action Function(set_current_contact, contact)

                        vbox:
                            text (person_get_name(p_id)):
                                yalign 0.5
                                #xpos -10
                                underline True
                                #action Function(set_current_contact, contact)

                            #text _("Relationship")
                            #text "[smartphone.small_selected_contact.relationship]/[smartphone.small_selected_contact.relationship_max]":
                            text "Relationship: [person_get_relationship(p_id)]/[RELATIONSHIP_MAX]":
                                size 80

