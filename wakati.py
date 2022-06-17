from janome.analyzer import Analyzer # 形態素解析ライブラリ 「pip install janome」
from janome.charfilter import *
from janome.tokenfilter import *

# 形態素解析の設定
token_filters = [CompoundNounFilter(),# 連続する名詞の複合名詞化
                 POSKeepFilter(['名詞','形容詞']), # 抽出する品詞の指定
                 UpperCaseFilter()] # アルファベットを大文字に変換
a = Analyzer(token_filters=token_filters)

# 分かち書き
def separate_word(question):
    #print('■debug:「%s」を形態素解析します。' % question)
    word_list = []
    for token in a.analyze(question):
        print(str(token))
        word_list.append(str(token).split()[0])
    return word_list
