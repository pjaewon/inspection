from flask import Flask, render_template, request, redirect, url_for
import pandas as pd


app = Flask(__name__)
app.secret_key = 'jaewon'

data = pd.read_excel('data/[동아출판] 6차_최종납품본_20240314_13331건.xlsx', sheet_name='Sheet1')
# data = pd.read_excel('data/1-6차 최종납품본_72132건.xlsx', sheet_name='통합')





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

# mapping = {'0.0':'0','1.0': '1', '2.0': '2', '3.0': '3', '4.0': '4', '5.0': '5','6.0':'6','7.0':'7','8.0':'8','9.0':'9'}
# mapping_col = [ '출처-문제번호','성취기준_영역(대)_연번', '성취기준_영역(중)_연번', '성취기준_성취기준명_연번', '난이도', '딸린문항수',
#        '교과서1_학년', '교과서1_학기', '교과서1_대단원순서', '교과서1_중단원순서', '교과서1_소단원순서',  '교과서2_학년',
#        '교과서2_학기',  '교과서2_대단원순서', '교과서2_중단원순서', '교과서2_소단원순서']
# for i in mapping_col:
#     data[i] = data[i].apply(lambda x: str(x))
#     data[i].replace(mapping,regex=True,inplace=True)


data['객관식정답'].replace({'1': '①', '2': '②', '3': '③', '4': '④', '5': '⑤',1: '①', 2: '②', 3: '③',4: '④',5: '⑤'}, regex=True, inplace=True)
ans = data[['객관식정답','주관식정답_1', '주관식정답_2', '주관식정답_3', '주관식정답_4', '주관식정답_5', '주관식정답_6', '주관식정답_7',
       '주관식정답_8', '주관식정답_9', '주관식정답_10', '주관식정답_11', '주관식정답_12', '주관식정답_13',
       '주관식정답_14', '주관식정답_15', '주관식정답_16', '주관식정답_17', '주관식정답_18', '주관식정답_19', '주관식정답_20']]
ans.fillna('')
ans_values=[]

for index, row in ans.iterrows():
    ans_values.append( '정답: '+' // '.join(str(value) for value in row.dropna()) )

# LaTeX data_strframe 생성 df_J, df_Q, df_A
data['지문(세트문제)'] = data['지문(세트문제)'].fillna('지문없음')
data['풀이'] = data['풀이'].fillna('풀이없음')

#객관식 선지 추가
data_str = data[:].astype('str')
ques = []
for i in range(len(data_str)):
    if data_str.iloc[i, list(data_str.columns).index('문제유형')] == '객관식-단답형' or data_str.iloc[i, list(data_str.columns).index('문제유형')] == '객관식-다답형':
        ques.append( data_str.iloc[i,list(data_str.columns).index('발문')] + '<br>① ' + data_str.iloc[i,list(data_str.columns).index('객관식선지1')] + '<br>② ' + data_str.iloc[i,list(data_str.columns).index('객관식선지2')] + '<br>③ ' + data_str.iloc[i,list(data_str.columns).index('객관식선지3')] + '<br>④ ' + data_str.iloc[i,list(data_str.columns).index('객관식선지4')] + '<br>⑤ ' + data_str.iloc[i,list(data_str.columns).index('객관식선지5')] )
    else:
        ques.append( data_str.iloc[i,list(data_str.columns).index('발문')])
        
#평가기준 
est_cri_col = ['평가기준1(서술형)', '평가기준1(퍼센트)', '평가기준2(서술형)',
       '평가기준2(퍼센트)', '평가기준3(서술형)', '평가기준3(퍼센트)', 
        '평가기준4(서술형)','평가기준4(퍼센트)', '평가기준5(서술형)', '평가기준5(퍼센트)'] 
for col in est_cri_col:
    data[col] = data[col].fillna('')
    
est_cri = []
for i in range(len(data_str)):
    if data_str.iloc[i, list(data_str.columns).index('문제유형')] == '주관식-서술형':
        est_cri.append( data_str.iloc[i,list(data_str.columns).index('풀이')] +'<br>' +
                    '서술형 평가기준1: ' + data_str.iloc[i,list(data_str.columns).index('평가기준1(서술형)')] +' '+ data_str.iloc[i,list(data_str.columns).index('평가기준1(퍼센트)')] + '<br>' +
                    '서술형 평가기준2: ' + data_str.iloc[i,list(data_str.columns).index('평가기준2(서술형)')] +' '+ data_str.iloc[i,list(data_str.columns).index('평가기준2(퍼센트)')] + '<br>' +
                    '서술형 평가기준3: ' + data_str.iloc[i,list(data_str.columns).index('평가기준3(서술형)')] +' '+ data_str.iloc[i,list(data_str.columns).index('평가기준3(퍼센트)')] + '<br>' +
                    '서술형 평가기준4: ' + data_str.iloc[i,list(data_str.columns).index('평가기준4(서술형)')] +' '+ data_str.iloc[i,list(data_str.columns).index('평가기준4(퍼센트)')] + '<br>' +
                    '서술형 평가기준5: ' + data_str.iloc[i,list(data_str.columns).index('평가기준5(서술형)')] +' '+ data_str.iloc[i,list(data_str.columns).index('평가기준5(퍼센트)')] )
    else:
        est_cri.append( data_str.iloc[i,list(data_str.columns).index('풀이')] )


df_J = data_str[['문항ID', '지문(세트문제)']]
df_Q = pd.DataFrame(zip(list(data_str['문항ID']), ques), columns=['문항ID','발문'])
df_A = pd.DataFrame(zip(list(data_str['문항ID']),ans_values, est_cri), columns = ['문항ID','정답','풀이'])
df_A['정답_풀이'] = df_A['정답'].astype(str) + '<br>' + df_A['풀이'].astype(str)

latex_df = pd.DataFrame(zip(df_J['문항ID'],  df_J['지문(세트문제)'],   df_Q['발문'] ,df_A['정답_풀이']    ), 
                        columns=['문항ID', '지문(세트문제)', '발문', '정답_풀이'] )


# 수학메타데이터
df = pd.DataFrame()
df['문항ID']=data['문항ID'].apply(lambda x:str(x))
df['출처_학교급'] = data['출처_학교급']
df['출처_학년_학기'] = data[['출처_학년', '출처_학기']].apply(lambda x: '-'.join(x.values.astype(str)), axis=1)
df['출처_교육과정']= data['출처_교육과정']
df['출처_판형_시리즈_제품명'] = data[[ '출처_판형', '출처_시리즈/브랜드', '출처_제품명', '출처_페이지']].apply(lambda x: ' // '.join(x.values.astype(str)), axis=1)
df['저자'] = data['저자']
df['내용_교육과정'] = data['내용_교육과정']
df['내용_학교급'] = data['내용_학교급']
df['키워드'] = data['키워드']
df['행동영역'] = data['행동영역']
df['난이도'] = data['난이도']
df['문제유형'] = data[['문제유형','선택지유형']].apply(lambda x: ' / 선택지유형: '.join(x.values.astype(str)), axis=1)
#-------------------------------------------------------------------------------------
df['KC'] = data[['KC1', 'KC2']].apply(lambda x: ' > '.join(x.values.astype(str)), axis=1)

col_list = list(data.columns)
achi, set_table, textbook1, textbook2 = [], [], [], []
for i in range(len(data_str)):
    achi.append( data_str.iloc[i,col_list.index('내용_학년(군)')] + ' > ' +data_str.iloc[i,col_list.index('성취기준_영역(대)_연번')] + '. ' +data_str.iloc[i,col_list.index('성취기준_영역(대)')] + ' > ' +
                data_str.iloc[i,col_list.index('성취기준_영역(중)_연번')] + '. ' +data_str.iloc[i,col_list.index('성취기준_영역(중)')] + ' > ' +
                 data_str.iloc[i,col_list.index('성취기준_표준코드')] +' - '+ data_str.iloc[i,col_list.index('성취기준_성취기준명_연번')] + '. ' +data_str.iloc[i,col_list.index('성취기준_성취기준명')] )
    set_table.append( '세트문제여부: '+ data_str.iloc[i,col_list.index('세트문제여부')] +' / ' + '개별출제: ' +data_str.iloc[i,col_list.index('개별출제여부')]+' / ' + '지문문항: '+ str(data_str.iloc[i,col_list.index('세트문항 대표ID')])  )
    textbook1.append( '교육과정: '+ data_str.iloc[i,col_list.index('교과서1_교육과정')] +' / '+'학교-학년-학기: ' + data_str.iloc[i,col_list.index('교과서1_학교급')]+' '+data_str.iloc[i,col_list.index('교과서1_학년')]+'-'+data_str.iloc[i,col_list.index('교과서1_학기')] + '<br>'+
                     '저자: '+data_str.iloc[i,col_list.index('교과서1_저자')] + ' / 단원: ' + data_str.iloc[i,col_list.index('교과서1_대단원순서')] +'.'+data_str.iloc[i,col_list.index('교과서1_대단원명')]+' > '+
                     data_str.iloc[i,col_list.index('교과서1_중단원순서')] +'. '+data_str.iloc[i,col_list.index('교과서1_중단원명')]+' > '+
                     data_str.iloc[i,col_list.index('교과서1_소단원순서')] +'. '+data_str.iloc[i,col_list.index('교과서1_소단원명')])
    textbook2.append( '교육과정: '+ data_str.iloc[i,col_list.index('교과서2_교육과정')] +' / '+'학교-학년-학기: ' + data_str.iloc[i,col_list.index('교과서2_학교급')]+' '+data_str.iloc[i,col_list.index('교과서2_학년')]+'-'+data_str.iloc[i,col_list.index('교과서2_학기')] + '<br>'+
                     '저자: '+data_str.iloc[i,col_list.index('교과서2_저자')] + ' / 단원: ' + data_str.iloc[i,col_list.index('교과서2_대단원순서')] +'.'+data_str.iloc[i,col_list.index('교과서2_대단원명')]+' > '+
                     data_str.iloc[i,col_list.index('교과서2_중단원순서')] +'. '+data_str.iloc[i,col_list.index('교과서2_중단원명')]+' > '+
                     data_str.iloc[i,col_list.index('교과서2_소단원순서')] +'. '+data_str.iloc[i,col_list.index('교과서2_소단원명')])
df['성취기준'] = achi
df['세트문제'] = set_table
df['교과서1'] = textbook1
df['교과서2'] = textbook2
    
df['정답'] = ans_values
    
latex_df = latex_df.drop('문항ID',axis=1)
df = pd.concat([df,latex_df],axis=1)


data['문항ID']=data['문항ID'].apply(lambda x:str(x))





data.set_index('문항ID',inplace=True)
df.set_index('문항ID', inplace=True)



# 문항 ID 리스트 생성
question_ids = list(df.index)
question_ids.sort()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_data', methods=['POST'])
def show_data():
    if request.method == 'POST':
        selected_id = str(request.form['selected_id'])
        #origin추가
        origin_selected_id = selected_id.split('-')[0]
        # 입력된 ID가 DataFrame에 없는 경우
        if selected_id not in df.index:
            return render_template('result.html', not_found=True)
        
        dap = df.loc[selected_id,'정답']
        if data.loc[selected_id,'문제유형'][:3]=='객관식':
            sunji ='① ' + data.loc[selected_id,'객관식선지1'] + '\n② ' + data.loc[selected_id,'객관식선지2'] + '\n③ ' + data.loc[selected_id,'객관식선지3'] + '\n④ ' + data.loc[selected_id,'객관식선지4'] + '\n⑤ ' + data.loc[selected_id,'객관식선지5']
        else:
            sunji = ''


        origin_J = data.loc[selected_id, '지문(세트문제)']
        origin_Q = data.loc[selected_id, '발문']
        origin_A = data.loc[selected_id, '풀이']
        Q_num = data.loc[selected_id,'출처-문제번호']
        
        source_school = df.loc[selected_id, '출처_학교급']
        source_grade = df.loc[selected_id, '출처_학년_학기']
        source_cirri = df.loc[selected_id, '출처_교육과정']
        source_book_name = df.loc[selected_id, '출처_판형_시리즈_제품명']
        source_author = df.loc[selected_id, '저자']
        contents_cirri = df.loc[selected_id, '내용_교육과정']
        contents_school = df.loc[selected_id, '내용_학교급']
        contents_achi = df.loc[selected_id, '성취기준']
        contents_kc = df.loc[selected_id, 'KC']
        contents_keyword = df.loc[selected_id, '키워드']
        contents_behavior = df.loc[selected_id, '행동영역']
        contents_level = df.loc[selected_id, '난이도']
        contents_type = df.loc[selected_id, '문제유형']
        contents_set = df.loc[selected_id, '세트문제']
        textbook1 = df.loc[selected_id, '교과서1']
        textbook2 = df.loc[selected_id, '교과서2']
        
        if 'aws' in df.loc[selected_id, '정답_풀이']:
            selected_id_A = df.loc[selected_id,'정답_풀이']
        else:
            selected_id_A = df.loc[selected_id,'정답_풀이'].replace('<img src ="', '<img src="').replace('<img src="', '<img src="./static/images/deepnatural_img/'+str(origin_selected_id)[:2]+'/')
        
        if 'aws' in  df.loc[selected_id, '발문']:
            selected_id_Q = df.loc[selected_id,'발문']
        else:
            selected_id_Q = df.loc[selected_id,'발문'].replace('<img src ="', '<img src="').replace('<img src="', '<img src="./static/images/deepnatural_img/'+str(origin_selected_id)[:2]+'/')
        
        if 'aws' in df.loc[selected_id, '지문(세트문제)']:
            selected_id_J = df.loc[selected_id,'지문(세트문제)']
        else:
            selected_id_J = df.loc[selected_id,'지문(세트문제)'].replace('<img src ="', '<img src="').replace('<img src="', '<img src="./static/images/deepnatural_img/'+str(origin_selected_id)[:2]+'/')

        
        origin_id_J = './static/images/' + str(origin_selected_id)[:2]+'/'+ str(origin_selected_id)+'/image/'+str(origin_selected_id)+'_J.gif'
        origin_id_Q = './static/images/' + str(origin_selected_id)[:2]+'/'+ str(origin_selected_id)+'/image/'+str(origin_selected_id)+'_Q.gif'
        origin_id_A = './static/images/' + str(origin_selected_id)[:2]+'/'+ str(origin_selected_id)+'/image/'+str(origin_selected_id)+'_A.gif'
        
        # J_img = df.loc[selected_id, 'J_img']
        # Q_img = df.loc[selected_id, 'Q_img']
        # A_img = df.loc[selected_id, 'A_img']
        
        
        current_index = question_ids.index(selected_id)
        next_index = (current_index + 1) % len(question_ids)
        prev_index = (current_index - 1) % len(question_ids)
        
        # 다음 문제의 ID
        next_question_id = question_ids[next_index]
        prev_question_id = question_ids[prev_index]
        
        return render_template('result2.html', selected_id=selected_id, origin_selected_id=origin_selected_id,
                               source_school=source_school, source_grade=source_grade,source_cirri=source_cirri,source_book_name=source_book_name,source_author=source_author,
                               contents_cirri=contents_cirri,contents_school=contents_school,contents_kc=contents_kc,contents_keyword=contents_keyword,contents_behavior=contents_behavior,contents_level=contents_level,contents_type=contents_type,contents_set=contents_set,
                               textbook1=textbook1,textbook2=textbook2,contents_achi=contents_achi,
                               selected_id_A=selected_id_A,selected_id_Q=selected_id_Q,selected_id_J=selected_id_J,
                               origin_id_Q=origin_id_Q,origin_id_A=origin_id_A,next_question_id=next_question_id, origin_id_J=origin_id_J,
                                prev_question_id=prev_question_id,not_found=False
                                ,origin_Q=origin_Q,origin_A=origin_A,Q_num=Q_num,origin_J=origin_J,sunji=sunji, dap=dap)


    return render_template('index.html')

@app.route('/search_again', methods=['POST'])
def search_again():
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)