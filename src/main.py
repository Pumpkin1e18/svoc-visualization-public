from module import setting_of_html as setting   # output.htmlの最初のコード
from module import annotation_of_svoc as svoc1  # SVOCMのアノテーションをする
from module import annotation_of_xpos as Xpos   # 品詞のアノテーションをする
from module import output_of_html as output2    # output.htmlの最後のコード
import stanza                                   # 解析するツール


def analyze():
    # 変数の宣言
    # f = open('input.txt', 'r')
    # datalist = f.readlines()
    # f.close()
    # original_text = datalist[25].rstrip('\n')     # input.txtの1行目を解析対象にする
    original_text = input('解析したい英文を入力してください\n')
    output_file_name = 'output/output.html'
    # output_file_name = 'output.html'
    # 単語ごとに区切り、1番からidなどを格納する
    id = [0]                    # その単語のid
    deprel = ['ROOT']           # その単語の特性
    misc = [[-1, -1]]           # その単語の始まりと終わり
    edges = [[]]                # グラフの辺
    r_edges = []                # edgesの逆向きの有向辺
    name = ['ROOT']                   # その単語の文字列
    xpos = ['ROOT']


    # stanzaによる解析
    # stanza.download('en')  # download English model
    nlp = stanza.Pipeline('en')  # initialize English neural pipeline
    doc = nlp(original_text)
    # print(doc)
    # print(doc.entities)


    # 解析結果の保存
    dicts = doc.to_dict()[0]    # 1文目を取り出す
    edges = [[] for i in range(0, len(dicts)+1)]
    r_edges = [0 for i in range(0, len(dicts)+1)]
    for i in range(0, len(dicts)):
        # その単語の始めと終わりのindexを取り出す
        start_char, end_char = dicts[i]['misc'].split('|')
        start_idx = int(start_char.split('=')[1])
        end_idx = int(end_char.split('=')[1])
        # 得られた情報を表示する
        print(str(dicts[i]['id']) + ': ' + dicts[i]['text'], end='')
        print('-' + dicts[i]['xpos'] + '  ←  ' + dicts[i]['deprel'], end='')
        print('  ←  ' + str(dicts[i]['head']) +
            '-' + dicts[dicts[i]['head']-1]['text'])
        # 得られた情報を変数に格納する
        id.append(str(dicts[i]['id']))
        deprel.append(dicts[i]['deprel'])
        misc.append([start_idx, end_idx])
        edges[dicts[i]['head']].append(dicts[i]['id'])
        r_edges[dicts[i]['id']] = dicts[i]['head']
        name.append(dicts[i]['text'])
        if dicts[i]['xpos'] == 'IN' and dicts[i]['text'] == 'that' or dicts[i]['text'] == 'if':
            xpos.append('that')
        else:
            xpos.append(dicts[i]['xpos'])


    # htmlのソースコードをhtml_textに格納する
    html_text = ""
    # 初期化
    html_text += setting.export_to_html()
    # SVOCのアノテート
    html_text += svoc1.export_to_html(original_text,
                                    id, deprel, misc, edges, name, xpos)
    # 品詞のアノテート
    html_text += Xpos.export_to_html(original_text, id, xpos, misc, r_edges)
    # 出力
    html_text += output2.export_to_html()


    # htmlに作成した文字列を書きだす
    with open(output_file_name, 'wb') as file:
        file.write(html_text.encode('utf-8'))

    print('\n入力した英文: ' + original_text)
    print('outputフォルダにあるoutput.htmlが更新されているのでそれをダブルクリックで開いてください。\n')




if __name__ == "__main__":
    loop = True
    stanza.download('en')  # download English model
    while loop:
        analyze()
        while True:
            ans = input('もう一度解析しますか？(Yes or No): ')
            if ans[0:1] == 'n' or ans[0:1] == 'N':
                loop = False
                break
            if ans[0:1] == 'y' or ans[0:1] == 'Y':
                loop = True
                break
