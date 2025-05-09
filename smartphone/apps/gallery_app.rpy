
default smartphone.photo_full = False


screen photo_taking(vertical, img):
    modal True

    if auto_skip_choices:
        timer 0.1 action Function(take_photo, img)

    default camera_folder = smartphone.config["smartphone_folder"] + "base/camera/"

    imagebutton:
        idle camera_folder + "taking_photo_idle.webp"
        xalign 0.5
        yalign 0.5
    imagebutton:
        auto camera_folder + "photo_button_%s.webp"
        action Function(take_photo, img)
        if vertical:
            xalign 0.5
            yalign 0.97
        else:
            xalign 0.9
            yalign 0.5


screen photo_view(photo):
    style_prefix "smartphone"

    default base_folder = smartphone.config["smartphone_folder"] + "base/"
    default photos = smartphone.config["smartphone_folder"] + "photos/"
    default gallery_folder = smartphone.config["smartphone_folder"] + "apps/gallery/"

    viewport at phone_content_wide:
        draggable True
        mousewheel True
        scrollbars "both"
        vscrollbar_unscrollable "hide"
        scrollbar_unscrollable "hide"

        imagebutton:
            idle photos + photo + ".webp"
            if(not smartphone.photo_full):
                if smartphone.photos[photo]["vertical"]:
                    at phone_photo_vertical
                    ypadding 30
                    xpadding 1300
                else:
                    at phone_photo_horizontal
                    ypadding 500
                    xpadding 25
            mouse "default"
            action NullAction()

    hbox:
        xalign 0.75
        yalign 0.1

        if(not smartphone.photo_full):
            imagebutton:
                #at phone_photo_zoom_button
                #auto gallery_folder + "set_wallpaper_%s.webp"
                idle Image(gallery_folder + "set_wallpaper_idle.svg", dpi=500)
                hover Image(gallery_folder + "set_wallpaper_hover.svg", dpi=500)
                action [SetVariable("smartphone.wallpaper", photo), Notify("Wallpaper changed")]

        imagebutton:
            #at phone_photo_zoom_button
            if smartphone.photo_full:
                #auto base_folder + "stop_fullscreen_%s.webp"
                idle Image(gallery_folder + "stop_fullscreen_idle.svg", dpi=500)
                hover Image(gallery_folder + "stop_fullscreen_hover.svg", dpi=500)
                action SetVariable("smartphone.photo_full", False)
            else:
                #auto base_folder + "start_fullscreen_%s.webp"
                idle Image(gallery_folder + "start_fullscreen_idle.svg", dpi=500)
                hover Image(gallery_folder + "start_fullscreen_hover.svg", dpi=500)
                action SetVariable("smartphone.photo_full", True)


screen gallery():
    style_prefix "smartphone"

    default thumbnails = smartphone.config["smartphone_folder"] + "photos/thumbnails/"
    default photos = smartphone.config["smartphone_folder"] + "photos/"
    default gallery_folder = smartphone.config["smartphone_folder"] + "apps/gallery/"

    vpgrid at phone_content_wide_gallery:
        draggable True
        mousewheel True
        ymaximum 1752

        cols 4

        top_margin 40
        spacing 40

        #for photo_key in reversed(smartphone.config["photos"].keys()):
        for photo_key in reversed(smartphone.photos.keys()):
            imagebutton:
                idle thumbnails + photo_key + ".webp"
                hover Composite((500,500),
                    (0,0), thumbnails + photo_key + ".webp",
                    (0,0), gallery_folder + "photo_preview_overlay.webp"
                )
                action Function(smartphone_screen_push, "photo_view", photo=photo_key)



