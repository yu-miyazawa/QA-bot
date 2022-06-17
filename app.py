from flask import Flask, render_template, jsonify, request
from wordnet import get_synonyms # 自作関数
from wakati import separate_word # 自作関数
#from gensim.models import word2vec
import numpy as np
import json
import openpyxl


# 問い合わせ台帳の読み込み
excel_path = "./data/QA.xlsx"
wb = openpyxl.load_workbook(excel_path)
sheet = wb.worksheets[0]
q_col = "B"# 質問の列（ABC...）
a_col = "C"# 回答の列（ABC...）

# 日本語Wikipedia学習済みモデルを読み込み
#wiki_model = word2vec.Word2Vec.load('./model/word2vec.gensim.model')

# ヒット率が高いものを回答
def answer(question):
    # question = "支払い方法を変更する方法を教えてください" #request.form['question']

    # 質問を形態素解析して単語リストに変換
    word_list = separate_word(question)

    # 類義語を追加
    synonym_word_list = []
    for word in word_list:
        synonym_word_list += get_synonyms(word)
    word_list = word_list + synonym_word_list
    #print('■debug:質問の名詞+類義語')

    # 問い合わせ台帳を検索
    row_points = search_question(word_list)

    # ヒットしない場合は、類義語でもう一度検索
    # 毎回類義語で検索したい場合は加算0.5点とか
#    if len(row_points) == 0 :
#        synonym_word_list = []
#    for word in word_list:
#        synonym_word_list += get_synonyms(word)
#    row_points = search_question(synonym_word_list)

    # 関連度の高い質問と回答のセットを返却
    top_points = []
    top_row = [0,0]# [行番号,類似度]

    if len(row_points) > 0 :
        # ヒット数でソート（降順）  
        row_points.sort(key=lambda x: x[1],reverse=True)
        print('■debug:採点結果（点数の降順）')
        #pprint.pprint(row_points)
        # 最高点のみに絞り込む
        top_points = [i for i in row_points if i[1] == row_points[0][1]]
        print('■debug:採点結果（最高点のみ）')
        #pprint.pprint(top_points)
        # 最高点が複数存在する場合は、入力された質問とベクトル類似度が高いQAを返す
#        if len(top_points) > 1:
#            m_vec = get_vector(question)
#            for row in top_points:
#                print('■debug:q_vec ' + sheet[q_col + str(row[0])].value)
#                q_vec = get_vector(sheet[q_col + str(row[0])].value)
#                print('コサイン類似度：' + str(cos_sim(m_vec, q_vec)))
#                if top_row[1] < cos_sim(m_vec, q_vec):
#                    top_row[0] = row[0]
#                    top_row[1] = cos_sim(m_vec, q_vec)
#        # 最高点が1件の場合はそれを返す
#        else: top_row[0] = row_points[0][0]
#        return_json = {
#            "information":"最も関連度の高い回答はこちらです。",
#            "hit_question": sheet[q_col + str(top_row[0])].value,
#            "hit_answer": sheet[a_col + str(top_row[0])].value
#        }
#    else:# １件もヒットしない場合はsorry回答
#        return_json = {
#            "information":"すみません。「" + question + "」に関連する回答はありません。",
#            "hit_question": "",
#            "hit_answer": ""
#        }

    if len(row_points) > 0 :
        row_points.sort(key=lambda x: x[1],reverse=True)# ヒット数でソート（降順）
        return_json = {
            "information":"最も関連度の高い回答はこちらです。",
            "hit_question": sheet[q_col + str(row_points[0][0])].value,
            "hit_answer": sheet[a_col + str(row_points[0][0])].value
        }
    else:# １件もヒットしない場合はsorry回答
        return_json = {
            "information":"すみません。「" + question + "」に関連する回答はありません。",
            "hit_question": "",
            "hit_answer": ""
        }

    return return_json


# エクセルを単語リストで検索し、行番号とヒット数を返す
def search_question(word_list):
    row_points = []
    for i in range(300):#検索対象の行数（いったん300）
        point = 0
        q_cell = sheet[q_col + str(i+1)]
        a_cell = sheet[a_col + str(i+1)]
        if q_cell.value is not None and a_cell.value is not None:
            for keyword in word_list:
                if keyword.casefold() in q_cell.value.casefold():# 大文字小文字区別しない
                    point += 1
            if point > 0: row_points.append([i+1,point])
    return row_points

# cos類似度を計算
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# 文章のベクトル平均を計算
def get_vector(text):
    sum_vec = np.zeros(50) # 読み込んだモデルの次元数に合わせる
    word_count = 0
    for token in a.analyze(text):
        try:
            sum_vec += wiki_model[str(token).split()[0]]
            word_count += 1
        except KyeError: # モデルに単語が存在しない
            print('■debug:KeyError発生 ' + str(token).split()[0])
    return sum_vec / word_count



#質問を入力して回答
#question = input("質問を入力したください>")
#data = answer(question)
#print('最も関連度の高い回答はこちらです。\n'
#      '質問：' + data['hit_question']+'\n'
#      '回答：' + data['hit_answer'])

