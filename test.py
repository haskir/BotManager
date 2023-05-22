
with open(input(), "r", encoding="utf-8") as orig_file:
    strings = orig_file.readlines()
    with open("result.csv", "w", encoding="cp1251") as result:
        result.writelines(strings)