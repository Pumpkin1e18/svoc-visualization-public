# original_text = "Ed O'Kelley was the man who shot the man who shot Jesse James."
# result_id = ['1', '2']
# result_type = ['Subject', 'Verb']
# result_range = [['0', '11'], ['20', '23']]


# 形容詞, 黄色っぽい色
JJ = [('JJ',    '形容詞',           '#fffda8'), 
      ('JJR',   '形容詞(比較級)',   '#fffda8'), 
      ('JJS',   '形容詞(最上級)',   '#fffda8')]


# 副詞, 黄色っぽい色
RB = [('RB',    '副詞',             '#fffda8'), 
      ('RBR',   '副詞(比較級)',     '#fffda8'), 
      ('RBS',   '副詞(最上級)',     '#fffda8'),
      ('WRB',   'Wh-副詞',          '#fffda8')]
JJ.extend(RB)


# 限定詞, 灰色がかった青
DT = [('DT',    '限定詞',           '#ccadf6'),
      ('PDT',   '限定詞',           '#ccadf6'),
      ('WDT',   'wh-限定詞',        '#ccadf6')]
JJ.extend(DT)


# 数詞, 灰色がかった青
CD = [('CD', '数詞', '#ccdaf6')]
JJ.extend(CD)


# 名詞, 青
RB = [('NN',    '名詞',                 '#a4bced'),
      ('NNP',   '固有名詞(単数形)',     '#a4bced'),
      ('NNPS',  '固有名詞(複数形)',     '#a4bced'),
      ('NNS',   '名詞(複数形)',         '#a4bced')]
JJ.extend(RB)


# 代名詞, 灰色がかった青
PRP = [('PRP',  '個人代名詞',           '#ccdaf6'),
       ('PRP$', '代名詞(所有格)',       '#ccdaf6'),
       ('WP',   'wh-代名詞',            '#ccdaf6'),
       ('WP$',  'wh-代名詞(所有格)',    '#ccdaf6')]
JJ.extend(PRP)


# 前置詞, 茶色っぽい色
IN = [('IN', '前置詞', '#ffe8be'),
      ('TO', 'to', '#ffe8be')]
JJ.extend(IN)


# 動詞, 緑
MD = [('MD',    '助動詞',                   '#adf6a2'),
      ('VB',    '動詞(基本形)',             '#adf6a2'),
      ('VBD',   '動詞(過去形)',             '#adf6a2'),
      ('VBG',   '動詞(ing形)',              '#adf6a2'),
      ('VBN',   '動詞(過去分詞形)',         '#adf6a2'),
      ('VBP',   '動詞(非三人称単数形)',     '#adf6a2'),
      ('VBZ',   '動詞(三単現)',             '#adf6a2')]
JJ.extend(MD)


# その他, 紫
EX = [('EX',    'there',                    '#e4cbf6'),
      ('FW',    '外国語',                   '#e4cbf6'),
      ('LS',    'リストアイテムマーカー',   '#e4cbf6'),
      ('POS',   '所有格',                   '#e4cbf6'),
      ('RP',    'パーティクル',             '#e4cbf6'),
      ('SYM',   'シンボル',                 '#e4cbf6'),
      ('UH',    '感動詞',                   '#e4cbf6')]
JJ.extend(EX)


# その他, 色に制限なし
OTHER = [('CC',     '等位接続詞',           'yellow'),
         ('that',   '従属接続詞',           '#ffe8be'),
         ('-LRB-',  '(',                    '#e3e3e3'),
         ('-RRB-',  ')',                    '#e3e3e3')]
JJ.extend(OTHER)



# アノテーションの設定
def setting_of_annotation():
    # アノテーションの設定
    html_text = f"""
    <!-- configuration of annotation -->
    <script type="text/javascript">
        var collData4 = {{
            entity_types: [
            {{
                type: '{JJ[0][0]}',
                labels: ['{JJ[0][1]}'],
                bgColor: '{JJ[0][2]}',
                borderColor: 'darken'
            }}"""
    for i in range(1, len(JJ)):
        html_text += f""", {{
                type: '{JJ[i][0]}',
                labels: ['{JJ[i][1]}'],
                bgColor: '{JJ[i][2]}',
                borderColor: 'darken'
            }}"""      
    html_text += f"""
            ]
        }};
        
        collData4['relation_types'] = [{{
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
def application_of_annotation(original_text, ID, TYPE, RANGE, R_EDGES):
    # アノテーションの適用
    # Format: [${ID}, ${TYPE}, [[${START}, ${END}]]]

    # html_text += f"""
    # <script type = "text/javascript" >
    # var docData4 = {
    #     text: "Ed O'Kelley was the man who shot the man who shot Jesse James.",
    #     entities: [
    #         ['1', 'NNP', [[0, 11]]],
    #         ['2', 'VBD', [[12, 15]]],
    #         ['3', 'DT', [[16, 19]]],
    #         ['4', 'NN', [[20, 23]]],
    #         ['5', 'WP', [[24, 27]]],
    #         ['6', 'VBP', [[28, 32]]],
    #         ['7', 'DT', [[33, 36]]],
    #     ],
    # }

    # docData4['relations'] = [
    #     // Format: [${ID}, ${TYPE}, [[${ARGNAME}, ${TARGET}], [${ARGNAME}, ${TARGET}]]]
    #     ['R1', 'Anaphora', [['Anaphor', '3'], ['Entity', '4']]]
    # ]
    # </script >
    # """

    

    html_text = f"""
    <script type="text/javascript">
    var docData4 = {{
        text     : "{ original_text }",
        entities : ["""

    for i in range(1, len(ID)):
        if TYPE[i] != 'HYPH' and TYPE[i] != ',' and TYPE[i] != '.':
            html_text += f"""
                ['{ID[i]}', '{TYPE[i]}', [[ {RANGE[i][0]}, {RANGE[i][1]} ]]],"""

    html_text += f"""
        ],
    }};
    docData4['relations'] = ["""
    for i in range(1, len(R_EDGES)):
        if TYPE[i] == 'DT' or TYPE[i] == 'PDT' or TYPE[i] == 'PRP$' or TYPE[i] == 'JJ':
            html_text += f"""
                ['R{ i }', 'Anaphora', [['Anaphor', { str(i) }], ['Entity', { str(R_EDGES[i]) }]]],"""
    html_text += f"""
    ]
    </script>
    """
    return html_text



def export_to_html(original_text, id, xpos, misc, r_edges):
    html_text = ""

    # アノテーションの設定
    html_text += setting_of_annotation()

    # アノテーションの適用
    html_text += application_of_annotation(original_text, id, xpos, misc, r_edges)

    return html_text
