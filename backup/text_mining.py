#python解析器janome,ベクトル変換ツールword2vecをインポート
from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import re

def mining(msg):

    #テキストファイルの読み込み -2
    bindata = msg#open("text_1.txt").read()
    text = bindata

    #形態素解析 -3
    t = Tokenizer()
    results = []

    #テキストを1行ごとに処理 -4
    lines = text.split("\r\n")
    for line in lines:
        s = line
        s = s.replace("|","")
        s = re.sub(r"《#.+?》","",s)
        s = re.sub(r"[#.+?]","",s)
        tokens = t.tokenize(s)

        #必要な語句だけを対象とする -5
        r = []
        for tok in tokens:
            if tok.base_form == "*":
                w = tok.surface

            else:
                w = tok.base_form

            ps = tok.part_of_speech
            hinsi = ps.split(",")[0]

            if hinsi in ["名詞","形容詞","動詞","記号"]:
                r.append(w)
    
        rl = (" ".join(r)).strip()
        results.append(rl)
        return rl
        #print(rl)


# #書き込み先テキストを開く -6
# text_file = "text_2.txt"
# with open(text_file,"w",encoding="utf-8") as fp:
#     fp.write("/n".join(results))

# #word2vecでモデルを作成 -7
# data = word2vec.LineSentence(text_file)
# model = word2vec.Word2Vec(data,window=1,hs=1,min_count=1,sg=1)#(data,size=100,window=1,hs=1,min_count=1,sg=1)
# model.save("text_2.model")
# print("ok")