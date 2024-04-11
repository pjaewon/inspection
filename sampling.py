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
                                
                                cc_years =cc_years ,cc_school =cc_school ,cc_grade =cc_grade ,cc_semester =cc_semester ,cc_series =cc_series ,cc_name =cc_name ,cc_page =cc_page ,cc_num =cc_num ,keyw =keyw ,action =action ,level =level ,cate =cate ,select_cate =select_cate ,setyn =setyn ,set1 =set1 ,set_origin =set_origin ,kyo1_school =kyo1_school ,kyo1_grade =kyo1_grade ,kyo1_semester =kyo1_semester ,kyo1_author =kyo1_author ,kyo1_big_rank =kyo1_big_rank ,kyo1_big =kyo1_big ,kyo1_mid_rank =kyo1_mid_rank ,kyo1_mid =kyo1_mid ,kyo1_small_rank =kyo1_small_rank ,kyo1_small =kyo1_small ,kyo2_school =kyo2_school ,kyo2_grade =kyo2_grade ,kyo2_semester =kyo2_semester ,kyo2_author =kyo2_author ,kyo2_big_rank =kyo2_big_rank ,kyo2_big =kyo2_big ,kyo2_mid_rank =kyo2_mid_rank ,kyo2_mid =kyo2_mid ,kyo2_small_rank =kyo2_small_rank ,kyo2_small =kyo2_small ,
                                not_found=False
                                )


    return render_template('index.html')