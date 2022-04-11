#中文
import spacy
nlp = spacy.blank("zh") #創建一個空白的中文nlp對象
doc = nlp("這是一個句子。")
print(doc.text)
#---------------------------------------Cut Line---------------------------------------
#英文
import spacy
nlp = spacy.blank("en") #創建一個空白的英文nlp對象
doc = nlp("This is a sentence.")
print(doc.text)
#---------------------------------------Cut Line---------------------------------------
import spacy
nlp = spacy.blank("zh")
#處理文本
doc = nlp("我喜歡老虎和獅子。")
#遍歷印出doc中的內容
for i, token in enumerate(doc):
    print(i, token.text)

#擷取doc中"老虎"的部分
laohu = doc[3:5]
print(laohu.text)

#擷取doc中"老虎和獅子"的部分(不包含。)
laohuheshizhi = doc[3:8]
print(laohuheshizhi.text)
#---------------------------------------Cut Line---------------------------------------
import spacy
nlp = spacy.blank("zh")

#處理文本
doc = nlp(
    "在1994年,一碗滷肉飯只要$20元"
    "現在一碗滷肉飯要$55元"
)

#遍歷doc中的詞符
for token in doc:
    #檢測詞符是否是"$"
    if token.text == "$":
        #獲取文檔的下一個詞符
        next_token = doc[token.i + 1]
        #檢測下一個詞符是否組成一個數字
        if next_token.like_num:
            print("Price found:",next_token.text)
#---------------------------------------Cut Line---------------------------------------
import spacy

#讀取"en_core_web_sm"流程
nlp = spacy.load('en_core_web_sm')
text = "Rita is a happy people."

#處理文本
doc = text.lower()
doc = nlp(text)

#Print
print(doc.text)

for token in doc:
    #獲取詞符文本,詞性標注,及依存關係標籤
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    #正規化印出的格式
    print(f"{token_text:<12}{token_pos:<10}{token_dep:10}")

for ent in doc.ents:
    print(ent.text, ent.label_)
#---------------------------------------Cut Line---------------------------------------
import spacy
nlp = spacy.load('zh_core_web_sm')
text = "寫入歷史了：蘋果是美國第一家市值超過一萬億美元的上市公司。"

#處理文本
doc = nlp(text)

#對識別出的實體進行遍歷
for ent in doc.ents:
    print(ent.text, ent.label_) #Print出實體文本及標注
#---------------------------------------Cut Line---------------------------------------
import spacy
nlp = spacy.load("zh_core_web_sm")
text = "蘋果公布了預購細節，洩漏了即將到來的iPhone 14的發布日期。"

#處理文本
doc = nlp(text)

#印出token及序號
for i,token in enumerate(doc):
    print(i,token.text)

#遍歷實體
for ent in doc.ents:
    print(ent.text, ent.label_)
    
#獲取"iPhone 14"的跨度(Span)
iPhone_14 = doc[12:13]

#印出Span的文本
print("Missing entity:", iPhone_14.text)
#---------------------------------------Cut Line---------------------------------------
#試試使用SpaCy基於規則的Matcher, 寫一個可以匹配到文本中"iPhone 14" 這個短語的模板
import spacy

#導入Matcher
from spacy.matcher import Matcher

nlp = spacy.load("zh_core_web_sm")
doc = nlp("蘋果公布了預購細節，洩漏了即將到來的iPhone 14的發布日期。")

#用模型分享詞彙表初始化Matcher
matcher = Matcher(nlp.vocab)

#創建一個模板來匹配這兩個詞符: "iPhone"和 "14"
pattern = [{"text":"iPhone"},{"text":"14"}]

#把模板加入matcher中
matcher.add("iPhone_14_pattern",[pattern])

#在doc中使用matcher
matches = matcher(doc)
print("Matcher:",[doc[start:end].text for match_id, start, end in matches])
#---------------------------------------Cut Line---------------------------------------
#試著用不同的詞符屬性和運算符號寫一些更複雜的匹配模板
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("zh_core_web_sm")
matcher = Matcher(nlp.vocab)

doc = nlp(
    "升級IOS以後，我們並沒有發現系統有多大的不同，沒有當年IOS 7 發布時帶來的"
    "煥然一新的感覺。大部分IOS 11的設計與IOS 10保持一致。但我仔細試用後也發現了一些"
    "小小的改進"
)

#寫一個模板來匹配完整的IOS版本 ("IOS 7", "IOS 10", "IOS 11")
pattern = [{"text":"IOS"},{"IS_DIGIT":True}]

#把模板加入到matcher中,將matcher應用到doc上
matcher.add("IOS_VERSION_PATTERN",[pattern])
matches = matcher(doc)
print("Total matches found:",len(matches))

#遍歷所有的匹配,再印出span的文本
for match_id, start, end in matches:
    print("Match found:", doc[start:end].text)
#---------------------------------------Cut Line---------------------------------------
#寫一個模板,只匹配到不同格式的"Download"詞(詞符的英文原詞是"Download"),後面跟著一個註記POS詞性"PROPN"(專有名詞)的詞符
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("zh_core_web_sm")
matcher = Matcher(nlp.vocab)

doc = nlp(
    "我之前有下載艾爾登法環到MAC電腦上，但是根本打不開遊戲，到底怎麼辦？"
    "我下載TEJ的資料庫，居然是.ZIP檔，這樣MAC根本沒辦法解壓縮！"
    "MAC想要解壓縮.ZIP檔案，真的很麻煩，還是請Windows的朋友幫忙吧～"
)

#寫一個模板來匹配"下載"加一個代詞
pattern = [{"text":"下載"},{"POS":"PROPN"}]

#把模板加入matcher中,將matcher應用到doc上
matcher.add("Download_Things_Pattern",[pattern])
matches = matcher(doc)
print("Total matches found:",len(matches))

#遍歷所有的匹配,印出Span的文本
for match_id, start, end in matches:
    print("Match found:",doc[start:end].text)
#---------------------------------------Cut Line---------------------------------------
#寫一個模板,匹配到形容詞("adj")後面跟著一兩個名詞("noun")
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("zh_core_web_sm")
matcher = Matcher(nlp.vocab)

doc = nlp(
    "宮三餐廳的特色包含了好吃餐點、優秀服務、及漂亮店員。"
)

#寫一個模板:形容詞+一或兩個名詞
pattern = [{"POS":"ADJ"},{"POS":"NOUN"},{"POS":"NOUN"},{"OP":"?"}]

#把模板加入到matcher中,並將matcher應用到doc上面
matcher.add("ADJ_NOUN_PATTERN",[pattern])
matches = matcher(doc)
print("Total matches found:",len(matches))

#遍歷所有的匹配,印出span的文本
for match_id, start, end in matches:
    print("Match found:",doc[start:end].text)
#---------------------------------------Cut Line---------------------------------------
#在nlp.vocab.strings中查找字符串"cat"來獲得hash值(哈希值)
import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp("I have a cat.")

#查詢cat的hash值
cat_hash = nlp.vocab.strings["cat"]
print(cat_hash)

#查找cat_hash來得到字符串
cat_string = nlp.vocab.strings[cat_hash]
print(cat_string)
#---------------------------------------Cut Line---------------------------------------
#上面的中文版,可以發現貓和cat的hash值不一樣(繁體中文和英文的差別)
#在nlp.vocab.strings中查找字符串"cat"來獲得hash值(哈希值)
import spacy

nlp = spacy.load('zh_core_web_sm')
doc = nlp("我養了一隻貓.")

#查詢cat的hash值
cat_hash = nlp.vocab.strings["貓"]
print(cat_hash)

#查找cat_hash來得到字符串
cat_string = nlp.vocab.strings[cat_hash]
print(cat_string)
#---------------------------------------Cut Line---------------------------------------
#在nlp.vocab.strings中查找人物來得到hash值,查找這個hash值來返還原本的字符串
import spacy

nlp = spacy.load("zh_core_web_sm")
doc = nlp("蔡依林是一個明星。") #不要找小咖

#查找標籤是"人物"的字符串的hash值
person_hash = nlp.vocab.strings["人物"]
print(person_hash)

#查找person_hash來拿到字符串
person_string = nlp.vocab.strings[person_hash]
print(person_string)
#---------------------------------------Cut Line---------------------------------------
#樓上的英文版
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Will Smith is a super star") #不要找小咖

#查找標籤是"PERSON"的字符串的hash值
person_hash = nlp.vocab.strings["PERSON"]
print(person_hash)

#查找person_hash來拿到字符串
person_string = nlp.vocab.strings[person_hash]
print(person_string)
#---------------------------------------Cut Line---------------------------------------
#試試看創建一個DOC
#從spacy.token中導入Doc
#用words和spaces創建一個Doc,記得把vocab傳進去

import spacy
nlp = spacy.blank("en")

#導入Doc
from spacy.tokens import Doc

#目標文本: "Rita is cute!"
words = ["Rita","is","cute","!"]
spaces = [True,True,False,False]

#用words和spaces創建一個Doc
doc = Doc(nlp.vocab, words = words, spaces = spaces)
print(doc.text)
#---------------------------------------Cut Line---------------------------------------
#從頭開始練習Doc(文件) spans(跨度) entities(實體)
#動手創建Doc和Span實例,然後重新更新命名實體

import spacy
nlp = spacy.blank("en")

#導入Doc和Span類
from spacy.tokens import Doc, Span

words = ["I","Love","Sally","Wang"]
spaces = [False, False, False, False]

#用words和spaces創建一個doc
doc = Doc(nlp.vocab, words = words, spaces = spaces)
print(doc.text)

#為doc中的"Sally Wang"創建一個span, 並賦予其"person"的標籤
span = Span(doc, 2, 3, label = "PERSON" )
print(span.text, span.label_)

#把此Span加到Doc的實體中
doc.ents = [span]

#print出所有實體的文本和標籤
print([(ent.text,ent.label_) for ent in doc.ents])
#---------------------------------------Cut Line---------------------------------------
import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('Sally is a beautiful girl.')

for token in doc:
    if token.pos_ == "PROPN":
        if doc[token.i + 1].pos_ == "AUX":
            print("I find a beautiful girl in Taiwan:", token.text)
#---------------------------------------Cut Line---------------------------------------
import spacy

nlp = spacy.load('zh_core_web_sm')
doc = nlp("台北是一個討厭的城市")

for token in doc:
    if token.pos_ == "PROPN":
        if doc[token.i + 1].pos_ == "VERB":
            print("全台灣最愛下雨的城市:", token.text)
#---------------------------------------Cut Line---------------------------------------
#使用更大的中文/英文流程,該模型大約有2萬個詞彚Vector,模型要提前安裝好
#在cmd輸入 python -m spacy download zh_core_web_md
#在cmd輸入 python -m spacy download en_core_web_md

import spacy

#讀取zh_core_web_md流程
nlp = spacy.load("zh_core_web_md")

#處理文本
doc = nlp("兩隻貓咪跑得快")

for token in doc:
    print(token.text)

#獲取詞符"貓咪"的vector
cat_vector = doc[2].vector
print(cat_vector)
#---------------------------------------Cut Line---------------------------------------
#練習使用SpaCy中的similarity方法來比較Doc,Token,Span得到相似分數
#使用doc.similarity方法來比較doc1和doc2的相似度,並print出結果

import spacy

nlp = spacy.load("zh_core_web_md")

#使用當代電影大師 - 你說台北的天氣好冷,來做個sample
doc1 = nlp("你說台北的天氣好冷")
doc2 = nlp("冷冷的剛好降低你的體溫")

#獲取doc1/doc2的相似度
similarity = doc1.similarity(doc2)
print(similarity)
#---------------------------------------Cut Line---------------------------------------
#使用token.similarity方法來比較doc1/doc2的相似度並打印結果
import spacy

nlp = spacy.load("zh_core_web_md")

doc = nlp("美女和辣妹")

for i, token in enumerate(doc):
    print(i,token.text)

token1, token2 = doc[0], doc[2]

#獲取詞符"美女"和"辣妹"的相似度
similarity = token1.similarity(token2)
print(similarity)
#---------------------------------------Cut Line---------------------------------------
#使用token.similarity方法來比較doc1/doc2的相似度並打印結果
import spacy

nlp = spacy.load("zh_core_web_md")

doc = nlp("爸爸和媽媽")

for i, token in enumerate(doc):
    print(i,token.text)

token1, token2 = doc[0], doc[2]

#獲取詞符"爸爸"和"媽媽"的相似度
similarity = token1.similarity(token2)
print(similarity)
#---------------------------------------Cut Line---------------------------------------
import spacy

nlp = spacy.load("zh_core_web_md")

doc = nlp("這是一部不錯的電影,看完我們去吃了一間很好吃的餐廳")

for i, token in enumerate(doc):
    print(i,token.text)
    
span1 = doc[4:8] #print(span1) 發現要多取一根電線桿,不能只取4:7,要取到4:8,可以印出來看看做實驗
span2 = doc[17:21] #print(span2) 發現要多取一根電線桿,不能只取17:20,要取到17:21,可以印出來看看做實驗

#獲取兩個span的相似度 (不錯的電影vs很好吃的餐廳)
similarity = span1.similarity(span2)
print(similarity)
#---------------------------------------Cut Line---------------------------------------
#讀取zh_core_web_sm流程來創建nlp sample
#用nlp.pipe_names來印出流程組件的名字
#用nlp.pipeline來印出(name,component)元件的完整流程

import spacy

#讀取
nlp = spacy.load("zh_core_web_sm")

#印出流程組件的名字
print(nlp.pipe_names)

#應該不用說惹,印出來看看
print(nlp.pipeline)

#當不確定當前的流程時,可以隨時用nlp.pipe_names或nlp.pipeline來檢查當下的流程!
#---------------------------------------Cut Line---------------------------------------
#訂製化流程組件
import spacy
from spacy.language import Language

#定義訂製化組件
@Language.component("length_component")
def length_component_function(doc):
    doc_length = len(doc) #獲取doc的長度
    print(f"This document is {doc_length} tokens long.")
    return doc #返回doc

nlp = spacy.load("zh_core_web_sm") #讀取小規模的中文流程

nlp.add_pipe("length_component", first = True) #將組件加入到流程的最前面,印出流程組件名稱
print(nlp.pipe_names)

doc = nlp("這是一隻貓咪。") #處理一段文本
#---------------------------------------Cut Line---------------------------------------
import spacy
from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

nlp = spacy.load("zh_core_web_sm")
animals = ["柴柴","貓貓","碰企","勞贖","腔棘魚"] 
animal_patterns = list(nlp.pipe(animals))
print("animal_patterns:", animal_patterns)
matcher = PhraseMatcher(nlp.vocab)
matcher.add("ANIMAL",animal_patterns)

#定義訂製化組件
@Language.component("animal_component")
def language_component_function(doc):
    matches = matcher(doc) #把matcher應用到doc上
    spans = [Span(doc, start, end, label = "ANIMAL") for match_id, start, end in matches] #為每一個匹配結果生成一個Span並賦予"animal"的標籤
    doc.ents = spans #用匹配到的span覆蓋doc.ents
    return doc

#把組件加入到流程中,緊跟在"ner"組件後面
nlp.add_pipe("animal_component", after = "ner")
print(nlp.pipe_names)

#處理文本,印出doc.ents的文本和標籤
doc = nlp("我養了一隻貓貓叫腔棘魚")
print([(ent.text, ent.label_) for ent in doc.ents])
#---------------------------------------Cut Line---------------------------------------
