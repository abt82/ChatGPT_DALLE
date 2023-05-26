import streamlit as st
import openai

openai.api_key = st.secrets['api_key']  # OpenAI API 키 설정

st.title('ChatGPT + DALL-E')  # 웹 앱 타이틀 설정

# 사용자로부터 입력을 받는 폼 생성
with st.form('form'):
    user_input = st.text_input('프롬프트 입력')
    size = st.selectbox('크기', ['1024x1024', '512x512', '256x256'])
    submit = st.form_submit_button('보내기')

# 제출 버튼이 클릭되었고 사용자 입력이 있으면
if submit and user_input:
    # 시스템 메시지와 사용자 메시지 생성
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appeareance of the input. Response it shortly around 20 words"
    }]
    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })

    # GPT-3.5-turbo 모델로부터 응답 받기
    with st.spinner('ChatGPT 응답 생성중...'):    
        gpt_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            # model='gpt-4', 
            messages=gpt_prompt,
            temperature = 0.8
            )

    # 응답 내용을 화면에 출력
    prompt = gpt_response['choices'][0]['message']['content']
    st.write(prompt)

    # Dall-e로 그림그리기
    with st.spinner('DALL-E가 그림을 그리는 중...'):
        dalle_response = openai.Image.create(
            prompt = prompt,
            size = size
        )
        st.image(dalle_response['data'][0]['url'])

    # 사용한 토큰 수 계산하여 사이드바에 출력
    total_tokens = gpt_response['usage']['total_tokens']
    if 'token_history' not in st.session_state:
        st.session_state['token_history'] = ''
    st.session_state['token_history'] += f"{total_tokens} tokens are used.\n\n"
    st.sidebar.markdown(st.session_state['token_history'])
