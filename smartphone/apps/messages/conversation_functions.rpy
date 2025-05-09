
init python:
    def conversation_apply(c_id: str):
        if(str(c_id).strip() == ""):
            if config.developer:
                raise Exception("Cannot apply conversation without id!")
            return

        the_convo = get_conversation_by_id(c_id)
        # apply flags
        if(not the_convo["flags"] is None):
            for flag in store.conversations[c_id]["flags"]:
                flags_append(flag)

        p_id = the_convo["person"]
        if(not p_id in smartphone.contacts):
            smartphone.contacts.append(p_id)

        if(not p_id in smartphone.contacts):
            smartphone.contacts.append(p_id)

        if(not "conversations" in store.messages[p_id]):
            raise Exception(p_id + " has no messages")
        convo_day = actualgame.daycount
        if(not the_convo["day"] is None):
            convo_day = the_convo["day"]
        store.messages[p_id]["conversations"].append({
            "id" : c_id,
            "day" : convo_day
            })

        # set last_message
        store.messages[p_id]["last_message"] = store.conversations[c_id]["messages"][-1]["content"]

        # add images
        for msg in store.conversations[c_id]["messages"]:
            if("image" in msg) and (not msg["image"] is None):
                photo_name = msg["image"]
                is_vertical = msg["vertical"]
                smartphone.photos[photo_name] = {"vertical" : is_vertical}


    # def conversation_apply(convo_id: str):
    #     conversation_apply(convo_id)

    def apply_initial_conversations(p_id=None):
        if(store.conversations is None) or (len(conversations.keys()) == 0):
            raise Exception("Conversations not loaded!")

        initial_conversations = ["convo_stepdad01", "convo_aunty01", "convo_bff01", "convo_mom01"]

        for convo in initial_conversations:
            if(not convo in store.conversations.keys()):
                raise Exception("No conversation with ID: " + convo)
            conversation_apply(convo)


    def get_conversation_by_id(convo_id: str):
        if not isinstance(convo_id, str):
            raise Exception(str(convo_id) + " is not a string!")
        if(convo_id in store.conversations):
            return store.conversations[convo_id]
        elif config.developer:
            raise Exception("No conversation with id: " + convo_id)
        # for c in store.conversations:
        #     if(c.id == convo_id):
        #         return c


    def get_all_conversations():
        #msg_split = get_all_messages_split(manipulate_text_in_brackets_dict(get_all_messages()))
        msg_split = get_all_messages_split(get_all_messages())
        #msg_split = get_all_messages_split()
        #mgs_split = text_replacement(msg_split)
        max_line = len(msg_split) - 1 #csv fiscroll_positionles got 1 empty line at the end

        columns = {
            "convo_id" : 0,
            "person_id" : 1,
            "day" : 2,
            "sender" : 3,
            "content" : 4,
            "flags" : 5,
            "answers" : 6,
            "image" : 7,
            #"wallpaper" : 8,
            "vertical" : 8
        }

        result_dict = dict()

        for i in range(1, max_line):
            if(msg_split[i][columns['convo_id']] == ""):
                continue

            c_id = msg_split[i][columns['convo_id']]
            p = msg_split[i][columns['person_id']]
            #if config.developer and (not p in store.people):
            #    raise Exception("No person with id: " + p + " exists.")
            d = msg_split[i][columns['day']]
            if(d == ""):
                d = None
            else:
                d = int(d)
            flags = msg_split[i][columns['flags']]
            if(flags == ""):
                flags = None
            else:
                flags = flags.split(",") #always gets you a list
                flags = strip_from_list(flags)

            n = 1
            messages = []
            while((i+n < max_line) and (msg_split[i+n][columns['sender']] != "")):
                img = msg_split[i+n][columns['image']]
                if(img == ""):
                    img = None
                else:
                    check_can_load_file(FileType.PHOTO, img)

                s = msg_split[i+n][columns['sender']]
                if(s == "") and config.developer:
                    raise Exception("Sender is empty in Line " + str(i+n))
                c = msg_split[i+n][columns['content']]
                a = msg_split[i+n][columns['answers']]
                if(a == ""):
                    a = None
                else:
                    a = a.split(",")
                    a = strip_from_list(a)
                    #a = get_answer_options_by_id(a)
                # w = msg_split[i+n][columns['wallpaper']]
                # if(w == ""):
                #     w = None
                # else:
                #     check_can_load_file(FileType.WALLPAPER, w)

                v = msg_split[i+n][columns['vertical']]
                if(v == ""):
                    v = False
                else:
                    v = True

                messages.append({
                    "author_id" : s,
                    "content" : c,
                    "image" : img,
                    "answer_options" : a,
                    "vertical" : v,
                })

                # messages.append(Msg(
                #     author_id=s,
                #     content=c,
                #     img=img,
                #     #day=d,
                #     answer_options=a,
                #     #wallpaper=w,
                #     vertical=v
                # ))
                n = n + 1
                img = None
                s = None
                c = None

            i = i + n

            #result_list.append(Conversation(c_id, p, flags, messages))
            result_dict[c_id] = {
                "person" : p,
                "flags" : flags,
                "day" : d,
                "messages" : messages
            }
            messages = []
        return result_dict


    def get_conversations_by_person(pers: str):
        conversations_list = list()
        for convo in store.conversations:
            if(store.conversations[convo]["person"] == pers):
                conversations_list.append(convo)
        return conversations_list

