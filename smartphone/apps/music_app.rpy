
#music
transform musicbuttonszoom:
    zoom 0.2

transform musicbuttonszoom_small:
    zoom 0.15


init python:
    def get_play_time() -> str:
        minutes = gamemusic.pos // 60
        seconds = gamemusic.pos % 60
        return f"{minutes}:{seconds:02d}"



screen music():
    style_prefix "smartphone"
    $ gamemusic.update_song_position()

    default music_folder = smartphone.config["smartphone_folder"] + "apps/music/"
    timer 1.0 action Function(gamemusic.update_song_position) repeat True

    hbox at phone_content_wide:
        spacing 50

        vbox:
            xsize 1000
            text "Currently Playing:"
            null height 20
            text ">> {u}[gamemusic.currently_playing_short]{/u} <<":
                xalign 0.5
            text get_play_time():
                xalign 0.5
            bar value gamemusic.pos range gamemusic.get_song_duration()

            hbox:
                spacing 20
                ypos 15
                xalign 0.5

                #play button
                imagebutton:
                    if(gamemusic.state == MusicState.PLAYING):
                        idle music_folder + "music_playing_idle.webp"
                        hover music_folder + "music_playing_hover.webp"
                        action NullAction()
                    else:
                        idle music_folder + "music_play_idle.webp"
                        hover music_folder + "music_play_hover.webp"
                        if(gamemusic.state == MusicState.PAUSED): #paused
                            action [PauseAudio("music", "toggle"), SetVariable("gamemusic.state", MusicState.PLAYING)]
                        else: #stopped
                            action [Play("music", gamemusic.currently_playing), SetVariable("gamemusic.state", MusicState.PLAYING)]
                    at musicbuttonszoom

                #pause button
                imagebutton:
                    if(gamemusic.state == MusicState.PAUSED): #paused
                        idle music_folder + "music_paused_idle.webp"
                        hover music_folder + "music_paused_hover.webp"
                        action NullAction()
                    else:
                        idle music_folder + "music_pause_idle.webp"
                        hover music_folder + "music_pause_hover.webp"
                        if(gamemusic.state == 0): #stopped
                            action NullAction()
                        else:
                            action [PauseAudio("music", "toggle"), SetVariable("gamemusic.state", MusicState.PAUSED)]
                    at musicbuttonszoom


                #stop button
                imagebutton:
                    if(gamemusic.state == MusicState.STOPPED): #stopped
                        idle music_folder + "music_stopped_idle.webp"
                        hover music_folder + "music_stopped_hover.webp"
                        action NullAction()
                    else:
                        idle music_folder + "music_stop_idle.webp"
                        hover music_folder + "music_stop_hover.webp"
                        action [Stop("music"), SetVariable("gamemusic.state", MusicState.STOPPED)]
                    at musicbuttonszoom

            null height 20
            text "Music Volume:"
            bar value Preference("music volume") #at transform
                #xsize 800


        vbox:
            text "{u}Music:{/u}"
            viewport:
                mousewheel True
                scrollbars "vertical"
                draggable True
                vbox:
                    for song in gamemusic.get_all_songs():
                        textbutton song:
                            action Function(gamemusic.play_song, song)
                    #for location in gamemusic.per_location.keys():
                    #    textbutton get_song_title_from_path(gamemusic.per_location[location]):
                    #        action Function(gamemusic.play_song, str(gamemusic.per_location[location]))
                            #action Notify(str(gamemusic.per_location[location]))
        #     xsize 800
        #     ysize 950
        #     spacing 10
        #     vbox:
        #         #xalign 0.5
        #         #yalign 0.3
        #         #xsize 800
        #         #for track in get_music():
        #         for track in smartphone.music_list:
        #             textbutton(track[25:-4]):
        #                 action [SetVariable("gamemusic.currently_playing", track), SetVariable("gamemusic.currently_playing_short", track[25:-4]), SetVariable("gamemusic.state", 1), Play("music", track)]
        #                 #action [Function(set_music_variables(track)), Play("music", track)]

