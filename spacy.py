#中文
import spacy
nlp = spacy.blank("zh") #創建一個空白的中文nlp對象
doc = nlp("這是一個句子。")
print(doc.text)

'''result>>>這是一個句子。'''

#-----------------------------------------我是分隔線

#英文
import spacy
nlp = spacy.blank("en") #創建一個空白的英文nlp對象
doc = nlp("This is a sentence.")
print(doc.text)

'''result>>>This is a sentence.'''

#-----------------------------------------我是分隔線

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

'''result>>>
0 我
1 喜
2 歡
3 老
4 虎
5 和
6 獅
7 子
8 。
老虎
老虎和獅子
'''

#-----------------------------------------我是分隔線

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

'''result>>>
Price found: 2
Price found: 5
'''

#-----------------------------------------我是分隔線

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

'''result>>>
Rita is a happy people.
Rita        PROPN     nsubj     
is          AUX       ROOT      
a           DET       det       
happy       ADJ       amod      
people      NOUN      attr      
.           PUNCT     punct 
'''

#-----------------------------------------我是分隔線

import spacy
nlp = spacy.load('zh_core_web_sm')
text = "寫入歷史了：蘋果是美國第一家市值超過一萬億美元的上市公司。"

#處理文本
doc = nlp(text)

#對識別出的實體進行遍歷
for ent in doc.ents:
    print(ent.text, ent.label_) #Print出實體文本及標注

'''result>>> 第一 ORDINAL'''

#-----------------------------------------我是分隔線

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

'''result>>>
0 蘋果
1 公布
2 了
3 預購
4 細節
5 ，
6 洩漏
7 了
8 即將
9 到
10 來
11 的
12 iPhone
13 14
14 的
15 發布
16 日期
17 。
14 CARDINAL
Missing entity: iPhone
'''

#-----------------------------------------我是分隔線

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

'''result>>>Matcher: ['iPhone 14']'''

#-----------------------------------------我是分隔線

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

'''result>>>
Total matches found: 3
Match found: IOS 7
Match found: IOS 11
Match found: IOS 10
'''

#-----------------------------------------我是分隔線

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

'''result>>>
Total matches found: 2
Match found: 下載艾爾
Match found: 下載TEJ
'''
