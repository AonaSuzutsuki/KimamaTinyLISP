
class Cell:
    def __init__(self, value):
        self.kind = 0  # CONS, NODE, LEAF
        self._head = None
        self._tail = None

    def set_left(self, left):
        self._head = left

    def set_right(self, right):
        self._tail = right


def replace_newline(text):
    text = text.replace('\r\n', '\r')
    text = text.replace('\r', '\n')
    return text


def mtoken(text):
    text = replace_newline(text).replace('\n', '')
    text = text.replace('(', ' ( ').replace(')', ' ) ').split()
    return text


def parse(tokens):
    token = tokens.pop(0)
    if token == '(':
        list = []
        while tokens[0] != ')':
            list.append(parse(tokens))
        tokens.pop(0)  # pop off ']'
        return list
    return token


def flatten(nested_list):
    """深さ優先探索の要領で入れ子のリストをフラットにする関数"""
    # フラットなリストとフリンジを用意
    flat_list = []
    fringe = [nested_list]

    while len(fringe) > 0:
        node = fringe.pop(0)
        # ノードがリストであれば子要素をフリンジに追加
        # リストでなければそのままフラットリストに追加
        if isinstance(node, list):
            fringe = node + fringe
        else:
            flat_list.append(node)

    return flat_list



def parse2(tokens):
    if tokens[0] == 'LIST':
        aList = []
        token = tokens[1:]
        for elem in token:
            aList.append(parse2(elem))
        return aList
    elif tokens[0] == 'ATOM':
        token = tokens[1]
        return resolve(token)
    else:
        return 0


def resolve(atom):
    (id, val) = atom
    if id == 'IDENTIFIER':
        return str(val)
    elif id == 'INTEGER':
        return int(val)
    elif id == 'FLOAT':
        return float(val)


def car(list):
    if isinstance(list, str):
        return list
    return list[0]


def cdr(list):
    return list[1:]


def parser3(tokens):
    if tokens[0] == 'LIST':
        aList = []


def parse4(aList, rList):
    for elem in aList:
        if isinstance(elem, list):
            #print('car', car(elem))
            celem = car(elem)
            if celem == 'LIST': # ネストされたリスト判定
                #print(elem)
                rList.append(parse4(cdr(elem), []))
            elif celem == 'ATOM': # アトム判定
                (id, val) = cdr(elem)[0]
                val = resolve4(id, val)
                rList.append(val)
                #print(val)
            else:
                parse4(elem, rList)

            #if len(elem) == 2:
                #(id, val) = elem
                #if not isinstance(val, list):
                 #   print(id, val)
        elif elem == 'LIST': # 一番初めのリスト判定
            parse4(elem, rList)
    #print(rList)
    return rList
    # else:
    # print(elem)


def resolve4(id, val):
    if id == 'IDENTIFIER':
        return str(val)
    elif id == 'INTEGER':
        return int(val)
    elif id == 'FLOAT':
        return float(val)


text = """
(LIST
        (
            (
                (ATOM
                    (IDENTIFIER defun))
                (ATOM
                    (IDENTIFIER test)))
            (LIST
                (
                    (
                        (ATOM
                            (IDENTIFIER lambda))
                        (LIST
                            (
                                (
                                    (ATOM
                                        (IDENTIFIER a))
                                    (ATOM
                                        (IDENTIFIER b)))
                                (ATOM
                                    (IDENTIFIER c)))))
                    (LIST
                        (
                            (
                                (ATOM
                                    (IDENTIFIER +))
                                (ATOM
                                    (IDENTIFIER a)))
                            (LIST
                                (
                                    (
                                        (ATOM
                                            (IDENTIFIER +))
                                        (ATOM
                                            (IDENTIFIER b)))
                                    (ATOM
                                        (IDENTIFIER c))))))))))
"""
text2 = """
(LIST
        (
            (
                (ATOM
                    (IDENTIFIER +))
                (ATOM
                    (INTEGER 1)))
            (LIST
                (
                    (
                        (ATOM
                            (IDENTIFIER +))
                        (ATOM
                            (INTEGER 1)))
                    (ATOM
                        (INTEGER 2))))))
"""
# ['LIST', [[['ATOM', ['IDENTIFIER', '+']], ['ATOM', ['INTEGER', '1']]], ['ATOM', ['INTEGER', '2']]]]

alist = parse(mtoken(text))
print(alist)
print(parse4(alist, []))
alist = parse(mtoken(text2))
print(alist)
print(parse4(alist, []))

alist = parse2(alist)
print(alist)
