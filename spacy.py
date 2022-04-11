'''Rita Lin 2022/04/08 SpaCy Practice'''

#中文
import spacy
nlp = spacy.blank("zh") #創建一個空白的中文nlp對象
doc = nlp("這是一個句子。")
print(doc.text)

'''result>>>這是一個句子。'''

#-----------------------------------------我是分隔線-----------------------------------------

#英文
import spacy
nlp = spacy.blank("en") #創建一個空白的英文nlp對象
doc = nlp("This is a sentence.")
print(doc.text)

'''result>>>This is a sentence.'''

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

import spacy
nlp = spacy.load('zh_core_web_sm')
text = "寫入歷史了：蘋果是美國第一家市值超過一萬億美元的上市公司。"

#處理文本
doc = nlp(text)

#對識別出的實體進行遍歷
for ent in doc.ents:
    print(ent.text, ent.label_) #Print出實體文本及標注

'''result>>> 第一 ORDINAL'''

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

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

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>Total matches found: 0''' #我也想知道為毛什麼都沒match到???算了,可能是因為中文吧

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
5439657043933447811
cat
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
2840559385213016379
貓
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
16486493800568926464
人物
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
380
PERSON
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>Rita is cute!''' #Rita很滿意!

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
ILoveSallyWang
Sally PERSON
[('Sally', 'PERSON')] 
''' #希望這招撩妹能成功

#-----------------------------------------我是分隔線-----------------------------------------

import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('Sally is a beautiful girl.')

for token in doc:
    if token.pos_ == "PROPN":
        if doc[token.i + 1].pos_ == "AUX":
            print("I find a beautiful girl in Taiwan:", token.text)
    
'''result>>>I find a beautiful girl in Taiwan: Sally'''

#-----------------------------------------我是分隔線-----------------------------------------
import spacy

nlp = spacy.load('zh_core_web_sm')
doc = nlp("台北是一個討厭的城市")

for token in doc:
    if token.pos_ == "PROPN":
        if doc[token.i + 1].pos_ == "VERB":
            print("全台灣最愛下雨的城市:", token.text)
            
'''result>>>全台灣最愛下雨的城市: 台北'''


#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
兩隻
貓咪
跑
得
快
[-2.8459    0.32048  -0.30816  -0.93138  -0.28018   1.8831   -1.8911
  5.5937   -1.423     1.6578   -0.58878   4.7068   -1.0706    3.2047
 -3.5505    0.57562  -4.0097    3.1418    2.3283    2.079     1.6681
 -3.1713   -2.7232    2.4075   -1.5068    3.4791    0.2104    1.5859
 -4.3877    3.5712   -6.8421    1.6928   -0.84454  -0.37157  -1.5298
 -1.5461    2.5694   -0.86163   2.508    -4.0392   -1.9058    0.98413
 -0.34074   0.93309  -2.3112    1.9918    4.6978    1.4879    0.98123
  2.0115   -1.8009    3.0979   -2.4079    3.5671    0.50252  -1.0893
 -1.9335    2.6888    0.073567 -0.13746  -0.23608   3.7539    4.1994
 -0.76696  -6.4953   -1.268    -2.1181    6.2575   -6.2589    2.023
 -0.43734   4.703    -2.5326    3.623    -5.5291    2.3048   -3.3765
 -7.5948   -7.5931   -1.4838   -0.83584  -3.7131    3.0294   -4.0067
 -2.0883   -1.6006   -0.64951  -0.41297  -1.3434    0.56647  -4.082
 -0.49194   1.0295   -1.3925    1.5148   -0.82669  -0.28327  -3.5983
 -2.4945    2.1808    3.3454   -0.97422  -1.651    -3.0983    2.5726
  4.8229   -0.58639   1.3523   -4.6994   -1.4542   -0.67998  -0.23783
  4.058     0.79777   3.1005    1.469     0.76425   4.4673    3.3695
 -2.049    -4.7043    3.4321    0.14609   0.47851   2.6236    7.3958
 -1.1071   -3.6781    0.045345 -3.8379   -2.001    -0.87283   5.2053
 -1.8151   -0.73952   5.0747   -1.4508   -2.8353    3.2562   -1.9893
  0.53765   3.6111   -0.69568  -4.0102    1.4874    2.4547   -1.2718
 -1.3292    4.8522    2.1334    2.693     2.8358    1.8752   -2.1354
 -5.0739    4.5413   -0.2431    4.3455    5.9955   -5.4541   -2.1903
 -4.3887   -4.7135    0.92903   4.6048    0.34937  -3.519     2.0599
  0.0776    0.71868   3.4485    1.7418   -6.4764    7.0633   -2.4193
 -0.71579   2.2805    5.0837   -6.1097   -2.5283    1.7687    0.93335
  0.71355  -0.07924   3.7854   -2.8356    0.80234   1.87      2.2274
 -2.7812    1.5416   -0.099173  0.9011    0.80188   0.26838   2.831
  5.0987   -1.3956    3.6094    3.8579   -6.039     2.079    -2.5081
  2.2117    0.085181  1.8744   -2.7273    0.1034    1.0134   -0.22146
  4.0682   -0.68277  -0.59248   3.463    -4.5475    5.9292   -0.22155
  4.1383   -1.9925    1.3171    4.4531    8.3175   -0.59322   3.78
  0.2039    4.2507   -0.50988   0.56524   2.6006   -0.24982   0.25998
  0.044752 -1.1434    0.80015   4.1431   -0.98096   4.3174    1.2404
 -2.488     4.5906    4.9128    1.0712    0.2736    0.23919   2.1338
  3.3499   -4.8238    1.3999   -1.7971   -0.62635  -2.6744    4.486
  3.3492   -0.39178   0.925     3.1327    2.5609   -0.946     0.51222
 -6.0145    6.727     5.05     -2.9908    0.98053   1.5935   -2.2211
 -0.17363   3.1939   -4.3147   -5.1022   -4.6016   -5.8662    2.9769
  1.5749   -1.8924    2.8187   -1.6992    0.29212   3.18      2.2629
 -1.9054   -1.2447   -0.52973  -2.573     0.77359  -3.8377   -0.62775
  1.9443    0.24332  -0.88069   0.7388   -0.030259  0.82479   4.0046
  2.1749    7.082    -0.58326   1.6944    2.7205    3.5291  ]
  '''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>> 0.6826446632529931 ''' #還滿高的耶,酷!

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
0 美女
1 和
2 辣妹
0.5233612656593323
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
0 這
1 是
2 一
3 部
4 不
5 錯
6 的
7 電影
8 ,
9 看
10 完
11 我
12 們去
13 吃
14 了
15 一
16 間
17 很
18 好吃
19 的
20 餐廳
0.6407151222229004
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
['tok2vec', 'tagger', 'parser', 'attribute_ruler', 'ner']
[('tok2vec', <spacy.pipeline.tok2vec.Tok2Vec object at 0x000001A486A96708>), ('tagger', <spacy.pipeline.tagger.Tagger object at 0x000001A486A96348>), ('parser', <spacy.pipeline.dep_parser.DependencyParser object at 0x000001A492EE99E8>), ('attribute_ruler', <spacy.pipeline.attributeruler.AttributeRuler object at 0x000001A4DEDCEDC8>), ('ner', <spacy.pipeline.ner.EntityRecognizer object at 0x000001A492EE9C18>)]
'''

#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
['length_component', 'tok2vec', 'tagger', 'parser', 'attribute_ruler', 'ner']
This document is 6 tokens long.
'''
#-----------------------------------------我是分隔線-----------------------------------------

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

'''result>>>
animal_patterns: [柴柴, 貓貓, 碰企, 勞贖, 腔棘魚]
['tok2vec', 'tagger', 'parser', 'attribute_ruler', 'ner', 'animal_component']
[('貓貓', 'ANIMAL'), ('腔棘魚', 'ANIMAL')]
'''

#-----------------------------------------我是分隔線-----------------------------------------

