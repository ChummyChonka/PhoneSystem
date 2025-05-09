
init python:

    def strip_from_list(somelist: list) -> list:
        for i in range(len(somelist)):
            somelist[i] = somelist[i].strip()
        return somelist


    def setup_msg_chains() -> dict:
        messages_dict = dict()
        for k in store.people.keys():
            messages_dict[k] = {
                "last_message" : None,
                "conversations" : list(),
                "unread" : False,
                "scroll_position" : 0,
            }
        return messages_dict


    def message_choose_answer(msg, option):
        if(not msg["answer_options"] is None) and (len(msg["answer_options"]) > option) and (option >= 0):
            conversation_apply(msg["answer_options"][option])
            msg["answered"] = True


    def get_last_message_shortened(p_id: str, max_length=None) -> str:
        last_message = store.messages[p_id]["last_message"]
        if(last_message is None):
            return ""
        if(max_length is None) or (len(last_message) <= max_length):
            return last_message
        else:
            return last_message[:max_length] + "..."


    def set_last_message(p_id: str):
        last_convo_id = store.messages[p_id]["conversations"][-1]["id"]
        store.messages[p_id]["last_message"] = get_conversation_by_id(last_convo_id)["messages"][-1]["content"]


    def get_all_messages() -> list:
        #load the file into a list
        filename = "extras/text_messages.csv"
        msg_list = get_csv_as_list(filename)
        return msg_list


    def get_all_messages_split(to_split=None) -> list:
        if(to_split is None):
            to_split = get_all_messages()
        split_list = []
        for line in to_split:
            line_split = line.split(";")
            split_list.append(line_split)
        return split_list


    def manipulate_text_in_brackets_dict(string_list:list, test_mode=False, replacements_extra=None) -> str:
        if(not type(string_list) is list):
            raise Exception("Function needs to be called with a string list, instead got: ", string_list)
        manipulated_list = []
        if(replacements_extra is None):
            update_replacements_dict()
            replacements_extra = store.replacements

        for line in string_list:
            parts = line.split("[")
            manipulated_line = parts[0]

            for part in parts[1:]:
                # Split at closing bracket
                try:
                    text, remainder = part.split("]", 1)
                except ValueError:
                    raise Exception(string_list)
                replacement = replacements_extra.get(text)
                if config.developer and (replacement is None):
                    raise Exception("Could not find a replacement for " + text)
                manipulated_line += replacement + remainder

            manipulated_list.append(manipulated_line)

        return manipulated_list


    def get_messages_from_applied_conversations(p_id: str) -> list:
        messages_list = list()
        for convo in store.messages[p_id]["conversations"]:
            convo_id = convo["id"]
            convo_day = convo["day"]
            for msg in store.conversations[convo_id]["messages"]:
                msg_to_add = msg
                msg_to_add["day"] = convo_day
                messages_list.append(msg_to_add)

        return messages_list


    def handle_new_answer(contact, msg, option):
        conversation_apply(option)
        msg["answered"] = True
        store.messages[contact]["unread"] = False
        scroll_down(contact)


    def get_smartphone_contacts_with_messages(fill_empty=False) -> list:
        contacts_list = list()
        fill_amount = 7

        for p_id in smartphone.contacts:
            if(len(store.messages[p_id]["conversations"]) > 0):
                contacts_list.append(p_id)

        for k,v in store.messages.items():
            if(k == "Eileen"):
                continue
            for i in range(len(store.messages[k]["conversations"])):
                try:
                    store.messages[k]["conversations"][i]["day"] = int(store.messages[k]["conversations"][i]["day"])
                except ValueError:
                    store.messages[k]["conversations"][i]["day"] = int(actualgame.daycount)

        #contacts_list.sort(key=lambda )
        contacts_list.sort(key=lambda pers: store.messages[pers]["conversations"][-1]["day"], reverse=True)

        if fill_empty:
            if(len(contacts_list) < fill_amount):
                to_fill = fill_amount - len(contacts_list)
                for i in range(to_fill):
                    contacts_list.append("empty")

        return contacts_list


