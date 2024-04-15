from flask import Flask, render_template, request, redirect, url_for,session
import pandas as pd
import sys
import os
import webbrowser
from threading import Timer


#template의 directory를 불러오도록 하는 코드'''
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

# app = Flask(__name__)
# app.secret_key = 'jaewon'

# data = pd.read_excel('데이터경로', sheet_name='시트명')
data = pd.read_excel('data/(동아출판) 8차_최종납품본_20240411_9956건.xlsx', sheet_name='시트1')
# data = pd.read_excel('data/(동아출판) 신규3_1차_최종납품본_20240411_2176건_수정.xlsx', sheet_name='공백제거')

col_name = ['문항ID', '출처_학교급', '출처_학년', '출처_학기', '출처_과목', '출처_교육과정', '출처_시리즈/브랜드',
       '출처_제품명', '출처_페이지','출처-문제번호', '출처_판형', '저자', '발행처정보', '사용기한', '사용범위', '사용권리',
       '내용_교육과정', '내용_학교급', '내용_교과', '내용_학년(군)', '성취기준_영역(대)_연번', '성취기준_영역(대)',
       '성취기준_영역(중)_연번', '성취기준_영역(중)', '성취기준_성취기준명_연번', '성취기준_성취기준명',
       '성취기준_표준코드', 'KC1', 'KC2', '키워드', '행동영역', '난이도', '지문(세트문제)', '발문', '객관식선지1',
       '객관식선지2', '객관식선지3', '객관식선지4', '객관식선지5', '객관식정답', '주관식정답입력개수', '주관식정답_1',
       '주관식정답_2', '주관식정답_3', '주관식정답_4', '주관식정답_5', '주관식정답_6', '주관식정답_7',
       '주관식정답_8', '주관식정답_9', '주관식정답_10', '주관식정답_11', '주관식정답_12', '주관식정답_13',
       '주관식정답_14', '주관식정답_15', '주관식정답_16', '주관식정답_17', '주관식정답_18', '주관식정답_19',
       '주관식정답_20', '풀이', '평가기준1(서술형)', '평가기준1(퍼센트)', '평가기준2(서술형)',
       '평가기준2(퍼센트)', '평가기준3(서술형)', '평가기준3(퍼센트)', 
       '평가기준4(서술형)', '평가기준4(퍼센트)', '평가기준5(서술형)', '평가기준5(퍼센트)', '문제유형', '선택지유형',
       '선택지개수', '세트문제여부', '개별출제여부','세트문항 대표ID', '딸린문항수', '교과서1_교육과정', '교과서1_학교급',
       '교과서1_학년', '교과서1_학기', '교과서1_교과서명', '교과서1_저자', '교과서1_대단원순서', '교과서1_대단원명',
       '교과서1_중단원순서', '교과서1_중단원명', '교과서1_소단원순서', '교과서1_소단원명', '교과서2_교육과정',
       '교과서2_학교급', '교과서2_학년', '교과서2_학기', '교과서2_교과서명', '교과서2_저자', '교과서2_대단원순서',
       '교과서2_대단원명', '교과서2_중단원순서', '교과서2_중단원명', '교과서2_소단원순서', '교과서2_소단원명','memo']
data.columns = col_name


data['객관식정답'].replace({'1': '①', '2': '②', '3': '③', '4': '④', '5': '⑤',1: '①', 2: '②', 3: '③',4: '④',5: '⑤'}, regex=True, inplace=True)
ans = data[['객관식정답','주관식정답_1', '주관식정답_2', '주관식정답_3', '주관식정답_4', '주관식정답_5', '주관식정답_6', '주관식정답_7',
       '주관식정답_8', '주관식정답_9', '주관식정답_10', '주관식정답_11', '주관식정답_12', '주관식정답_13',
       '주관식정답_14', '주관식정답_15', '주관식정답_16', '주관식정답_17', '주관식정답_18', '주관식정답_19', '주관식정답_20']]
ans.fillna('')
ans_values=[]

for index, row in ans.iterrows():
    ans_values.append( '정답: '+' <span style="color:red">//</span> '.join(str(value) for value in row.dropna()) )

data['정답']=ans_values

ev = ['평가기준1(서술형)', '평가기준1(퍼센트)', '평가기준2(서술형)', '평가기준2(퍼센트)', '평가기준3(서술형)', '평가기준3(퍼센트)', '평가기준4(서술형)', '평가기준4(퍼센트)', '평가기준5(서술형)', '평가기준5(퍼센트)']
for e in ev:
    data[e] = data[e].fillna('').astype(str)



dot0 = ['교과서1_학년', '교과서1_학기','교과서1_대단원순서', '교과서1_중단원순서', '교과서1_소단원순서',   
     '교과서2_학년', '교과서2_학기', '교과서2_대단원순서', '교과서2_중단원순서', '교과서2_소단원순서']
for d in dot0:
    data[d] = data[d].apply(lambda x : str(x).replace('.0',''))



for co in ['객관식선지1', '객관식선지2', '객관식선지3', '객관식선지4', '객관식선지5']:
    data[co] = data[co].apply(lambda x:str(x))
data['문항ID']=data['문항ID'].apply(lambda x:str(x))
data.set_index('문항ID',inplace=True)



# 문항 ID 리스트 생성
question_ids = list(data.index)
question_ids.sort()


@app.route('/')
def index():
    return render_template('index.html')


#_______________________________________________________________________________________________________________________________________

#sampling
@app.route('/show_data3', methods=['POST'])
def show_data3():
    if request.method == 'POST':
        selected_id = str(request.form['selected_id'])

        # 입력된 ID가 DataFrame에 없는 경우
        if selected_id not in data.index:
            return render_template('result.html', not_found=True)
        
        dap = data.loc[selected_id,'정답']
        
        if data.loc[selected_id,'문제유형'][:3]=='객관식':
            sunji ='① ' + data.loc[selected_id,'객관식선지1'] + '<br>② ' + data.loc[selected_id,'객관식선지2'] + '<br>③ ' + data.loc[selected_id,'객관식선지3'] + '<br>④ ' + data.loc[selected_id,'객관식선지4'] + '<br>⑤ ' + data.loc[selected_id,'객관식선지5']
        else:
            sunji = ''
            
        
        contents_group = data.loc[selected_id, '내용_학년(군)']
        contents_achi_1_num = data.loc[selected_id, '성취기준_영역(대)_연번']
        contents_achi_1 = data.loc[selected_id, '성취기준_영역(대)']
        contents_achi_2_num = data.loc[selected_id, '성취기준_영역(중)_연번']
        contents_achi_2 = data.loc[selected_id, '성취기준_영역(중)']
        contents_achi_3_num = data.loc[selected_id, '성취기준_성취기준명_연번']
        contents_achi_3_code = data.loc[selected_id, '성취기준_표준코드']
        contents_achi_3 = data.loc[selected_id, '성취기준_성취기준명']
        contents_kc1 = data.loc[selected_id, 'KC1']
        contents_kc2 = data.loc[selected_id, 'KC2']
        
        #-----------------------------
        

            
        cc_years = data.loc[selected_id, '출처_판형']
        cc_school = data.loc[selected_id, '출처_학교급']
        cc_grade = data.loc[selected_id, '출처_학년']
        cc_semester = data.loc[selected_id, '출처_학기']
        cc_series = data.loc[selected_id, '출처_시리즈/브랜드']
        cc_name = data.loc[selected_id, '출처_제품명']
        cc_page = data.loc[selected_id, '출처_페이지']
        cc_num = data.loc[selected_id, '출처-문제번호']
        keyw = data.loc[selected_id, '키워드']
        action = data.loc[selected_id, '행동영역']
        level = data.loc[selected_id, '난이도']
        cate = data.loc[selected_id, '문제유형']
        select_cate = data.loc[selected_id, '선택지유형']
        setyn = data.loc[selected_id, '세트문제여부']
        set1 = data.loc[selected_id, '개별출제여부']
        set_origin = data.loc[selected_id, '세트문항 대표ID']
        
        kyo1_school = data.loc[selected_id, '교과서1_학교급']
        kyo1_grade = data.loc[selected_id, '교과서1_학년']
        kyo1_semester = data.loc[selected_id, '교과서1_학기']
        kyo1_author = data.loc[selected_id, '교과서1_저자']
        kyo1_big_rank = data.loc[selected_id, '교과서1_대단원순서']
        kyo1_big = data.loc[selected_id, '교과서1_대단원명']
        kyo1_mid_rank = data.loc[selected_id, '교과서1_중단원순서']
        kyo1_mid = data.loc[selected_id, '교과서1_중단원명']
        kyo1_small_rank = data.loc[selected_id, '교과서1_소단원순서']
        kyo1_small = data.loc[selected_id, '교과서1_소단원명']
        
        kyo2_school = data.loc[selected_id, '교과서2_학교급']
        kyo2_grade = data.loc[selected_id, '교과서2_학년']
        kyo2_semester = data.loc[selected_id, '교과서2_학기']
        kyo2_author = data.loc[selected_id, '교과서2_저자']
        kyo2_big_rank = data.loc[selected_id, '교과서2_대단원순서']
        kyo2_big = data.loc[selected_id, '교과서2_대단원명']
        kyo2_mid_rank = data.loc[selected_id, '교과서1_중단원순서']
        kyo2_mid = data.loc[selected_id, '교과서2_중단원명']
        kyo2_small_rank = data.loc[selected_id, '교과서2_소단원순서']
        kyo2_small = data.loc[selected_id, '교과서2_소단원명']
        
        if data.loc[selected_id, '세트문제여부'] == 'Y' :
            set_J = data.loc[str(set_origin),'지문(세트문제)']
        else: 
            set_J = ''

        #-----------------------------

        
        if data.loc[selected_id,'문제유형']=='주관식-서술형':
            eval = '평가기준1: ' + data.loc[selected_id, '평가기준1(서술형)'] + ' ' + data.loc[selected_id, '평가기준1(퍼센트)'] +'%'+'<br>평가기준2: ' + data.loc[selected_id, '평가기준2(서술형)'] + ' ' + data.loc[selected_id, '평가기준2(퍼센트)'] +'%'+'<br>평가기준3: ' + data.loc[selected_id, '평가기준3(서술형)'] + ' ' + data.loc[selected_id, '평가기준3(퍼센트)'] +'%'+'<br>평가기준4: ' + data.loc[selected_id, '평가기준4(서술형)'] + ' ' + data.loc[selected_id, '평가기준4(퍼센트)'] +'%'+'<br>평가기준5: ' + data.loc[selected_id, '평가기준5(서술형)'] + ' ' + data.loc[selected_id, '평가기준5(퍼센트)'] +'%'
        else:
            eval = ''
       
        
        
        fingerprint = data.loc[selected_id, '지문(세트문제)']
        content = data.loc[selected_id, '발문']
        answer = data.loc[selected_id, '정답']
        solution = data.loc[selected_id, '풀이']
        
        
        
        
        current_index = question_ids.index(selected_id)
        next_index = (current_index + 1) % len(question_ids)
        prev_index = (current_index - 1) % len(question_ids)
        
        # 다음 문제의 ID
        next_question_id = question_ids[next_index]
        prev_question_id = question_ids[prev_index]
        
        return render_template('result3.html', selected_id=selected_id, contents_group=contents_group,
                               fingerprint=fingerprint, content=content, answer=answer, solution=solution,
                               contents_achi_1_num=contents_achi_1_num,contents_achi_1=contents_achi_1,
                               contents_achi_2_num=contents_achi_2_num,contents_achi_2=contents_achi_2,
                               contents_achi_3_num=contents_achi_3_num,contents_achi_3_code=contents_achi_3_code,contents_achi_3=contents_achi_3,
                               contents_kc1=contents_kc1,contents_kc2=contents_kc2, eval=eval,
                                prev_question_id=prev_question_id,next_question_id=next_question_id,sunji=sunji, dap=dap,
                                
                                cc_years =cc_years ,cc_school =cc_school ,cc_grade =cc_grade ,cc_semester =cc_semester ,cc_series =cc_series ,cc_name =cc_name ,cc_page =cc_page ,cc_num =cc_num ,keyw =keyw ,action =action ,level =level ,cate =cate ,select_cate =select_cate ,setyn =setyn ,set1 =set1 ,set_origin =set_origin ,kyo1_school =kyo1_school ,kyo1_grade =kyo1_grade ,kyo1_semester =kyo1_semester ,kyo1_author =kyo1_author ,kyo1_big_rank =kyo1_big_rank ,kyo1_big =kyo1_big ,kyo1_mid_rank =kyo1_mid_rank ,kyo1_mid =kyo1_mid ,kyo1_small_rank =kyo1_small_rank ,kyo1_small =kyo1_small ,kyo2_school =kyo2_school ,kyo2_grade =kyo2_grade ,kyo2_semester =kyo2_semester ,kyo2_author =kyo2_author ,kyo2_big_rank =kyo2_big_rank ,kyo2_big =kyo2_big ,kyo2_mid_rank =kyo2_mid_rank ,kyo2_mid =kyo2_mid ,kyo2_small_rank =kyo2_small_rank ,kyo2_small =kyo2_small ,set_J=set_J,
                                not_found=False
                                )


    return render_template('index.html')

@app.route('/search_again', methods=['POST'])
def search_again():
    return redirect(url_for('index'))

def open_browser():
      webbrowser.open_new('http://127.0.0.1:'+str(port)+'/') 

port = 9000

if __name__ == "__main__":
    Timer(1,open_browser).start();
    app.run(port=port, debug=True)  
    
# if __name__ == '__main__':
#     app.run( port =5000, debug=True)
