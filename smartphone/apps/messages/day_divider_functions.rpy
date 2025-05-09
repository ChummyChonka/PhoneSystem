
init python:
    def put_day_divider(msg) -> bool:
        msg_age = get_msg_age(msg)
        if(smartphone.msg_age != msg_age):
            smartphone.msg_age = msg_age
            return True
        return False


    def get_msg_age(msg) -> int:
        age = 0
        age = actualgame.daycount - msg["day"]
        if(age < 0):
            age = 0
        return age


    def get_msg_age_text(msg) -> str:

        age_dict = {
            0: "today",
            1: "yesterday",
            2: "two days ago",
            3: "three days ago",
            4: "four days ago",
            5: "five days ago",
            6: "six days ago",
            7: "one week ago",
            14: "two weeks ago",
            21: "three weeks ago",
            28: "four weeks ago",
            30: "one month ago",
            60: "two months ago",
            90: "three months ago",
            120: "four months ago",
            150: "five months ago",
            180: "half a year ago",
            365: "one year ago",
            730: "two years ago",
            1095: "thee years ago",
            1460: "four years ago",
            1825: "five years ago",
            2000: "in an ancient past"
        }

        msg_age = get_msg_age(msg)
        sorted_keys = sorted(age_dict.keys())
        largest_key = 0
        for key in sorted_keys:
            if key <= msg_age:
                largest_key = key
            else:
                break
        if smartphone.config["date_divider_upper"]:
            return age_dict[largest_key].upper()
        return age_dict[largest_key]


    def reset_msg_age():
        smartphone.msg_age = 0


    def set_msg_divider_age(msg_age: int):
        #smartphone.msg_age = get_msg_age(msg)
        smartphone.msg_age = msg_age

