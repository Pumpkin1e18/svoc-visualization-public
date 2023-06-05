# original_text = "Ed O'Kelley was the man who shot the man who shot Jesse James."
# result_id = ['1', '2']
# result_type = ['Subject', 'Verb']
# result_range = [['0', '11'], ['20', '23']]
from collections import deque

result_id = []
result_type = []
result_range = []
id = []
deprel = []
misc = []
edges = []
name = []
xpos = []
parent = []         # Union-Find木、親のIDを保存する


# アノテーションの設定
def setting_of_annotation():
    # アノテーションの設定
    html_text = f"""
    <script type="text/javascript">
    var collData1 = {{
        entity_types: [ 
            {{
                type: 'Subject',
                labels : ['S'],
                bgColor: '#a4bced',
                borderColor: 'darken'
            }}, {{
                type: 'Verb',
                labels: ['V'],
                bgColor: '#adf6a2',
                borderColor: 'darken'
            }}, {{
                type: 'Object',
                labels: ['O'],
                bgColor: '#ffa22b',
                borderColor: 'darken'
            }}, {{
                type: 'Complement',
                labels: ['C'],
                bgColor: '#ffe8be',
                borderColor: 'darken'
            }}, {{
                type: 'Modifier',
                labels: ['M'],
                bgColor: '#e4cbf6',
                borderColor: 'darken'
            }}, {{
                type: 'be',
                labels: ['be動詞'],
                bgColor: '#ffe8be',
                borderColor: 'darken'
            }}, {{
                type: 'auxiliary',
                labels: ['助動詞'],
                bgColor: '#ffe8be',
                borderColor: 'darken'
            }}
        ]
    }};
    collData1['relation_types'] = [{{
        type: 'Anaphora',
        labels: ['修飾'],
        // dashArray allows you to adjust the style of the relation arc
        dashArray: '50,3',
        color: 'purple',
    }}];
    </script>
    """
    return html_text


# アノテーションの適用
def application_of_annotation(original_text):
    # アノテーションの適用
    # Format: [${ID}, ${TYPE}, [[${START}, ${END}]]]
    
    # html_text += f"""
    # <script type="text/javascript">
    # var docData1 = {{
    #     text     : "Ed O'Kelley was the man who shot the man who shot Jesse James.",
    #     entities : [
    #         ['1', 'Subject', [[0, 11]]],
    #         ['2', 'Verb', [[20, 23]]],
    #         ['3', 'Object', [[37, 40]]],
    #         ['4', 'Complement', [[50, 61]]],
    #     ],
    # }};
    # docData2['relations'] = [
    #     // Format: [${ID}, ${TYPE}, [[${ARGNAME}, ${TARGET}], [${ARGNAME}, ${TARGET}]]]
    #     ['R1', 'Anaphora', [['Anaphor', '3'], ['Entity', '4']]]
    # ];
    # </script>
    # """

    global parent
    ID = result_id
    TYPE = result_type
    RANGE = result_range

    html_text = f"""
    <script type="text/javascript">
    var docData1 = {{
        text     : "{ original_text }",
        entities : ["""

    for i in range(0, len(ID)):
        print(str(ID[i]) + ' - ' + str(TYPE[i]))
        html_text += f"""
            ['{ID[i]}', '{TYPE[i]}', [[ {RANGE[i][0]}, {RANGE[i][1]} ]]],"""

    html_text += f"""
        ],
    }};
    docData1['relations'] = ["""
    for i in range(1, len(edges)):
        for j in edges[i]:
            is_Modifier = False
            for k in range(0, len(ID)):
                if str(j) == str(ID[k]) and TYPE[k] == 'Modifier':
                    is_Modifier = True
            if is_Modifier == True and name[j] != 'However':
            # if deprel[j][0:3] == 'obl' or deprel[j][0:3] == 'adv' or deprel[j] == 'nmod':
                html_text += f"""
                    ['R{ j }', 'Anaphora', [['Anaphor', '{ j }'], ['Entity', '{ parent[i] }']]],"""
    html_text += f"""
    ]
    </script>
    """
    return html_text

# result変数に追加
def add_result(ID, TYPE, RANGE):
    result_id.append(ID)
    result_type.append(TYPE)
    result_range.append(RANGE)


# 節を結合するdfs
def union_dfs(now_node_id, par, visited, start_idx, end_idx, DICTIONARY):
    global parent
    dictionary = DICTIONARY.copy()
    dictionary.append('cc')
    for node_id in edges[now_node_id]:
        # 結合できるなら結合する
        for dic in dictionary:
            if deprel[node_id] == dic:
                start_idx = min([start_idx, misc[node_id][0]])
                end_idx = max([end_idx, misc[node_id][1]])
                parent[node_id] = par
                visited[node_id] = True
    start_idx = min([start_idx, misc[now_node_id][0]])
    end_idx = max([end_idx, misc[now_node_id][1]])
    return start_idx, end_idx


# 受動態の主語をまとめる
def nsubj_pass(now_node_id, visited, dictionary):
    start_idx = misc[now_node_id][0]
    end_idx = misc[now_node_id][1]
    for node_id in edges[now_node_id]:
        # 結合できるなら結合する
        for dic in dictionary:
            if deprel[node_id] == dic:
                start_idx = min([start_idx, misc[node_id][0]])
                end_idx = max([end_idx, misc[node_id][1]])
                parent[node_id] = now_node_id
                visited[node_id] = True
    add_result(now_node_id, 'Subject', [start_idx, end_idx])


# 無条件にnow_node_idのノードとその子孫を結合する
def unite_clause(now_node_id, par, visited, start_idx, end_idx):
    if visited[now_node_id] == True:
        return start_idx, end_idx
    visited[now_node_id] = True
    for node_id in edges[now_node_id]:
        s2, e2 = unite_clause(node_id, par, visited, start_idx, end_idx)
        start_idx = min(start_idx, s2)
        end_idx = max(end_idx, e2)
        parent[node_id] = par
    start_idx = min(start_idx, misc[now_node_id][0])
    end_idx = max(end_idx, misc[now_node_id][1])
    return start_idx, end_idx


# 木を作る
def struct_tree():
    lst = []
    q = deque([0])
    while q:
        p = q.popleft()
        lst.append(p)
        for i in edges[p]:
            q.append(i)
    return lst


# 子ノードの結合
def unite(now_node_id, par, visited, start_idx, end_idx, dictionary, TYPE):
    if visited[now_node_id] == True:
        return start_idx, end_idx
    visited[now_node_id] = True
    is_conj = False
    is_nsubj = False
    for node_id in edges[now_node_id]:
        # andかorでつながれている部分を接合する
        if deprel[node_id] == 'conj':
            is_conj = True
            for node_id2 in edges[node_id]:
                if deprel[node_id2][0:5] == 'nsubj':
                    is_nsubj = True
                if xpos[node_id2] == 'TO':
                    s2, e2 = unite(node_id, node_id, visited, misc[node_id][0], misc[node_id][1], dictionary, 'Modifier')
                    add_result(node_id, 'Modifier', [s2, e2])
        # to be 構文
        if deprel[node_id]  == 'xcomp':
            for node_id2 in edges[node_id]:
                if xpos[node_id2] == 'TO':
                    dictionary.append('cop')
                    s2, e2 = unite(node_id, node_id, visited, misc[node_id][0], misc[node_id][1], dictionary, 'Complement')
                    dictionary.pop()
                    add_result(node_id, 'Complement', [s2, e2])
        # 再帰してstart_idxとend_idxを更新する
        if TYPE != 'Modifier' and is_conj == True and is_nsubj == True:
            continue
        for dic in dictionary:
            if deprel[node_id] == dic or TYPE == 'Modifier':
                s2, e2 = unite(node_id, par, visited, start_idx, end_idx, dictionary, TYPE)
                start_idx = min(start_idx, s2)
                end_idx = max(end_idx, e2)
                parent[node_id] = par
    start_idx = min(start_idx, misc[now_node_id][0])
    end_idx = max(end_idx, misc[now_node_id][1])
    return start_idx, end_idx


# SVOCの判定
def annotate_svoc():
    visited = [False for i in range(0, len(id)+1)]
    lst_tree = struct_tree()
    dictionary = ['det', 'amod', 'nmod:poss','nummod', 'compound', 'case', 'mark', 'conj']
    # SVOCの判定
    for i in lst_tree:      # 木の根に違い方から順番に探索する
        # 変数の宣言
        TYPE = None
        start_idx = misc[i][0]
        end_idx = misc[i][1]
        if visited[i] == True:
            continue

        # その単語がSVOCのどれか判定
        if deprel[i][0:5] == 'nsubj' or deprel[i] == 'csubj' or deprel[i] == 'expl':
            TYPE = 'Subject'
        if deprel[i] == 'root' or deprel[i] == 'cop' or deprel[i] == 'conj':
            TYPE = 'Verb'
        if deprel[i] == 'iobj' or deprel[i] == 'obj':
            TYPE = 'Object'
        if deprel[i] == 'xcomp':
            TYPE = 'Complement'
        if deprel[i][0:3] == 'obl' or deprel[i][0:3] == 'adv' or deprel[i] == 'nmod' or deprel[i][0:3] == 'acl':
            TYPE = 'Modifier'
        if deprel[i] == 'aux:pass':
            TYPE = 'be'
        if deprel[i] == 'aux':
            TYPE = 'auxiliary'
        if deprel[i] == 'root':
            for node_id in edges[i]:
                if deprel[node_id] == 'cop' and xpos[i] == 'NN':
                    TYPE = 'Complement'

        # 判定用変数の宣言
        par_root = (deprel[i] == 'root')
        found_cop = False
        found_nsubj = False

        # 判定用変数の値の格納
        for node_id in edges[i]:
            if deprel[node_id] == 'cop':
                found_cop = True
            if deprel[node_id][0:5] == 'nsubj':
                found_nsubj = True

        # rootに繋がっているのが動詞とは限らないのでその条件分岐
        dic_C = ['CD', 'FW', 'JJ', 'JJR', 'JJS', 'LS', 'NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WDT', 'WP', 'WRB']
        dic_M = ['EX', 'RB', 'RBR', 'RBS']
        if par_root and found_cop:
            for dic in dic_C:
                if xpos[i] == dic:
                    TYPE = 'Complement'
            for dic in dic_M:
                if xpos[i] == dic:
                    TYPE = 'Modifier'

        # どれにも当てはまらない場合continue
        if TYPE == None:
            continue

        # want to 動詞の原形V のようなもののせいで動詞が want から 動詞の原形V に変わったりするのでその対策
        ii = i

        # xcompの処理　（would like to 動詞 のようなものの処理）
        aux_start_idx = 100000      # would like to 動詞 の would のような意味を持つ単語の start_idx
        aux_id = -1
        for node_id in edges[i]:
            if deprel[node_id] == 'aux':
                aux_start_idx = misc[node_id][0]
                aux_id = node_id
            if deprel[node_id] == 'xcomp' and TYPE == 'Verb':
                for node_id2 in edges[node_id]:
                    if xpos[node_id2] == 'TO':
                        # would like to 動詞 のwould like to の部分をまとめて助動詞として登録する
                        visited[i] = True
                        visited[node_id2] = True
                        if aux_id != -1:
                            visited[aux_id] = True
                        start_idx2 = min(misc[i][0], aux_start_idx)
                        end_idx2 = max(misc[i][1], misc[node_id2][1])
                        add_result(id[i], 'auxiliary', [start_idx2, end_idx2])
                        # would like to 動詞 の動詞部分を本物の動詞として登録する
                        start_idx = misc[node_id][0]
                        end_idx = misc[node_id][1]
                        start_idx, end_idx = unite(node_id, node_id, visited, start_idx, end_idx, dictionary, TYPE)
                        ii = node_id
        
        # コピュラ動詞と主語があれば、コピュラ動詞がbe動詞判定
        if found_cop == True and found_nsubj == True and par_root == True:
            for node_id in edges[i]:
                if deprel[node_id] == 'nsubj':
                    s2, e2 = unite(node_id, node_id, visited, misc[node_id][0], misc[node_id][1], dictionary, 'Subject')
                    add_result(id[node_id], 'Subject', [s2, e2])
                if deprel[node_id] == 'cop':
                    s2, e2 = unite(node_id, node_id, visited, misc[node_id][0], misc[node_id][1], dictionary, 'Verb')
                    add_result(id[node_id], 'Verb', [s2, e2])
                if deprel[node_id] == 'aux':
                    s2, e2 = unite(node_id, node_id, visited, misc[node_id][0], misc[node_id][1], dictionary, 'auxiliary')
                    add_result(id[node_id], 'auxiliary', [s2, e2])

        # ccompの処理
        for node_id in edges[ii]:
            if deprel[node_id] == 'ccomp' and TYPE == 'Verb':
                s2, e2 = unite_clause(node_id, node_id, visited, misc[node_id][0], misc[node_id][1])
                add_result(id[node_id], 'Object', [s2, e2])
            if deprel[node_id] == 'ccomp' and TYPE != 'Verb':
                s2, e2 = unite_clause(node_id, node_id, visited, misc[node_id][0], misc[node_id][1])
                add_result(id[node_id], 'Modifier', [s2, e2])

        # 連結してSVOCの意味をなしているものをつなげる
        start_idx, end_idx = unite(ii, ii, visited, start_idx, end_idx, dictionary, TYPE)

        # SVOCのどれかに含まれていれば追加する
        add_result(id[ii], TYPE, [start_idx, end_idx])





def export_to_html(original_text, ID, DEPREL, MISC, EDGES, NAME, XPOS):
    global result_id, result_type, result_range, id, deprel, misc, edges, name, xpos, parent
    result_id = []
    result_type = []
    result_range = []
    id = ID
    deprel = DEPREL
    misc = MISC
    edges = EDGES
    name = NAME
    xpos = XPOS
    parent = [i for i in range(len(id)+1)]

    # SVOCを付けるときの情報を格納する変数
    html_text = ""

    # SVOCの判定
    annotate_svoc()

    # アノテーションの設定
    html_text += setting_of_annotation()

    # アノテーションの適用
    html_text += application_of_annotation(original_text)

    return html_text

    
