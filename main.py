import re

'''
校验两个提交的 strings.xml 资源文件的占位符的异同
'''
pathArray = ['values',
             'values-ar',
             'values-de',
             'values-es',
             'values-fr',
             'values-it']


def generate_map(text):
    array = re.findall(r'<string [\S\s]+?</string>', text)
    my_map = {}
    for row in array:
        key = re.search(r"(?<=name=\")\S+?(?=\")", row)
        if key:
            key = key.group()
        else:
            continue

        yes = re.findall(r'%\d*\$*[sd]+', row)
        if yes:
            all_placeholder = ""
            for j_index, j in enumerate(yes):
                all_placeholder += j + ("," if (j_index < len(yes) - 1) else "")
            my_map[key] = all_placeholder
    return my_map


new_string_key = set()


def __test_list_key_value(file_path):
    f = open(file_path, 'r')
    text = f.read()
    map = generate_map(text)
    for item in map:
        print(item, map[item])


def show_diff(file_path_1, file_path_2):
    f1 = open(file_path_1, 'r')
    f2 = open(file_path_2, 'r')
    text1 = f1.read()
    text2 = f2.read()
    map1 = generate_map(text1)
    map2 = generate_map(text2)
    for key in map1:
        if key in map2:
            if map2[key] != map1[key]:
                print("键", key, "老的", map1[key], "新的", map2[key])
        else:
            print("删除的键：", key)
    for key in map2:
        if key not in map1:
            new_string_key.add(key)

    f1.close()
    f2.close()


if __name__ == '__main__':

    print("\n\n\n\n纵向比较")
    for i in range(0, 6):
        print("\n\n\n\n---------------- " + pathArray[i] + " ----------------")
        show_diff('lang/lang_old/' + pathArray[i] + "/strings.xml",
                  'lang/lang_new/' + pathArray[i] + "/strings.xml")
    print("\n\n\n\n")
    for new_key in new_string_key:
        print("新增的键：", "----------------", new_key, "----------------")

    print("\n\n\n\n横向比较")
    for i in range(1, 6):
        print("\n\n\n\n---------------- " + pathArray[i] + " ----------------")
        show_diff('lang/lang_new/' + pathArray[0] + "/strings.xml",
                  'lang/lang_new/' + pathArray[i] + "/strings.xml")


        # __test_list_key_value('lang/lang_new/' + pathArray[5] + "/strings.xml")
