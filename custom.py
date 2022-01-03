index_to_cardinal_table = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "ninth",
    "tenth",
    "eleventh",
    "twelfth",
    "thirteenth",
    "fourteenth",
    "fifteenth",
    "sixteenth",
    "seventeenth",
    "eighteenth",
    "nineteenth",
    "twentieth",
    "1st",
    "2nd",
    "3rd",
    "4th",
    "5th",
    "6th",
    "7th",
    "8th",
    "9th",
    "10th",
    "11th",
    "12th",
    "13th",
    "14th",
    "15th",
    "16th",
    "17th",
    "18th",
    "19th",
    "20th"
]

cardinal_to_index_table = {
    "first":0,"1st":0,
    "second":1,"2nd":1,
    "third":2,"3rd":2,
    "fourth":3,"4th":3,
    "fifth":4,"5th":4,
    "sixth":5,"6th":5,
    "seventh":6,"7th":6,
    "eighth":7,"8th":7,
    "ninth":8,"9th":8,
    "tenth":9,"10th":9,
    "eleventh":10,"11th":10,
    "twelfth":11,"12th":11,
    "thirteenth":12,"13th":12,
    "fourteenth":13,"14th":13,
    "fifteenth":14,"15th":14,
    "sixteenth":15,"16th":15,
    "seventeenth":16,"17th":16,
    "eighteenth":17,"18th":17,
    "nineteenth":18,"19th":18,
    "twentieth":19,"20th":19,
}

def genderize(in_text, gender):
    #Spivak
    if gender == 0:
        in_text = in_text.replace("%s", "e")
        in_text = in_text.replace("%S", "E")
        in_text = in_text.replace("%o", "em")
        in_text = in_text.replace("%O", "Em")
        in_text = in_text.replace("%p", "eir")
        in_text = in_text.replace("%P", "Eir")
        in_text = in_text.replace("%q", "eirs")
        in_text = in_text.replace("%Q", "Eirs")
        in_text = in_text.replace("%r", "emself")
        in_text = in_text.replace("%R", "Emself")

    #Feminine
    elif gender == 1:
        in_text = in_text.replace("%s", "she")
        in_text = in_text.replace("%S", "She")
        in_text = in_text.replace("%o", "her")
        in_text = in_text.replace("%O", "Her")
        in_text = in_text.replace("%p", "her")
        in_text = in_text.replace("%P", "Her")
        in_text = in_text.replace("%q", "hers")
        in_text = in_text.replace("%Q", "hers")
        in_text = in_text.replace("%r", "herself")
        in_text = in_text.replace("%R", "Herself")

    #Masculine
    elif gender == 2:
        in_text = in_text.replace("%s", "he")
        in_text = in_text.replace("%S", "He")
        in_text = in_text.replace("%o", "him")
        in_text = in_text.replace("%O", "Him")
        in_text = in_text.replace("%p", "his")
        in_text = in_text.replace("%P", "His")
        in_text = in_text.replace("%q", "his")
        in_text = in_text.replace("%Q", "His")
        in_text = in_text.replace("%r", "himself")
        in_text = in_text.replace("%R", "Himself")
    return in_text

def cardinal_to_index(cardinal):
    return cardinal_to_index_table[cardinal]

def index_to_cardinal(index):
    return index_to_cardinal_table[index]
    
def is_valid_cardinal(cardinal):
    try:
        return index_to_cardinal_table.index(cardinal) >= 0
    except:
        return False

def print_cardinal_list(msg, objs, caller):
    caller.msg(msg)
    count = 0
    for obj in objs:
        caller.msg(f"  ({index_to_cardinal(count)}) {obj} ({obj.location})")
        count += 1
    return
