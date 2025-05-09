
screen renamer():
    style_prefix "smartphone"

    viewport at phone_msg_content_wide_left:
        draggable True
        mousewheel True
        scrollbars "vertical"

        vbox:
            xfill True

            #for p in sorted(store.people, key=lambda pers: pers.name):
            #for p in sorted(people.keys()):
            for p in get_sorted_people_by_display_name():
                if(person_is_unknown(p)):
                    continue
                textbutton person_get_display_name(p):
                    xalign 0.5
                    action SetVariable("actualgame.renamer_person", p)


    viewport at phone_msg_content_wide_right:
        vbox:
            xfill True
            if(actualgame.renamer_person is None):
                null height 300
                text "Select somebody":
                    xalign 0.5
                    yalign 0.5
            else:
                null height 50

                add person_get_image(actualgame.renamer_person):
                    xalign 0.5

                #hbox:
                grid 2 4:
                    xalign 0.5
                    spacing 30

                    text "Name:"
                    if not person_check_name(actualgame.renamer_person):
                        textbutton "Not Set":
                            text_underline True
                            action Show("textinput", args=[actualgame.renamer_person, "name"])
                    else:
                        textbutton person_get_name(actualgame.renamer_person):
                            text_underline True
                            action Show("textinput", args=[actualgame.renamer_person, "name"])

                    text "Nickname:"
                    if not person_check_nickname(actualgame.renamer_person):
                        textbutton "Not Set":
                            text_underline True
                            action Show("textinput", args=[actualgame.renamer_person, "nickname"])
                    else:
                        textbutton person_get_nickname(actualgame.renamer_person):
                            text_underline True
                            action Show("textinput", args=[actualgame.renamer_person, "nickname"])

                    text "Surname:"
                    if not person_check_surname(actualgame.renamer_person):
                        textbutton "Not Set":
                            text_underline True
                            action [SetField(actualgame.renamer_person, "surname", ""), Show("textinput", args=[actualgame.renamer_person, "surname"])]
                    else:
                        textbutton person_get_surname(actualgame.renamer_person):
                            text_underline True
                            action Show("textinput", args=[actualgame.renamer_person, "surname"])

                    if(actualgame.renamer_person in petnames_from_protag):
                        text "Petname:"
                        textbutton petnames_from_protag[actualgame.renamer_person]:
                            text_underline True
                            #action [SetField(actualgame.renamer_person, "petname", ""), Show("textinput", args=[petnames_for_protag, "petname", actualgame.renamer_person])]
                            action Show("textinput", args=[petnames_from_protag, "petname", actualgame.renamer_person])

                null height 100

                text "Used for Dialogue:":
                    underline True
                    xalign 0.5
                grid 2 1:
                    xalign 0.5
                    spacing 30
                    textbutton "Name":
                        if(person_use_nickname(actualgame.renamer_person) == False):
                            text_underline True
                        action Function(person_set_display_name, actualgame.renamer_person, False)
                    textbutton "Nickname":
                        if person_use_nickname(actualgame.renamer_person):
                            text_underline True
                        action Function(person_set_display_name, actualgame.renamer_person, True)


screen textinput(args):
    modal True
    style_prefix "smartphone_textinput"
    frame:
        #background Frame("images/smartphone/msgboxes/phonemsg31.webp", 50,50)
        background Frame("gui/notify.png", 50,50)
        xminimum 2200
        xmaximum 3500
        yminimum 750
        #ysize 750
        xalign 0.5
        #yalign 0.5
        style "name_changer"

        has vbox:
            spacing 30
            xalign 0.5
            yalign 0.5

            hbox:
                spacing 30
                if(args[1] in ["name", "surname", "nickname"]):
                    text args[1].capitalize()
                    input:
                        #value FieldInputValue(args[0], args[1])
                        value DictInputValue(people[args[0]], args[1])
                # if(args[1] == "name"):
                #     text "Name:"
                # elif(args[1] == "surname"):
                #     text "Surname:"
                # elif(args[1] == "nickname"):
                #     text "Nickname:"
                elif(args[1] == "petname"):
                    text "Petname:"
                    input:
                        value DictInputValue(args[0], args[2])
                else:
                    text "ERROR"

            textbutton "Save":
                xalign 0.5
                action [Function(person_update_display_name, actualgame.renamer_person), Hide("textinput")]

