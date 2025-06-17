from music_links import music_links
import streamlit as st
import random
from datetime import datetime
# main.py

import streamlit as st
import random
from datetime import datetime

# 👉 MBTI 스타일 매핑 (추가 필요 시 수정 가능)
style_mapping = {
    "INTJ": "클래식",
    "INTP": "Lofi",
    "ENTJ": "정돈된 테마 음악",
    "ENTP": "다양성 있는 셔플 믹스",
    "INFJ": "몽환적 사운드",
    "INFP": "감성 발라드",
    "ENFJ": "OST",
    "ENFP": "신나는 팝",
    "ISTJ": "재즈",
    "ISFJ": "클래식",
    "ESTJ": "EDM",
    "ESFJ": "가사 중심 감성곡",
    "ISTP": "드림팝",
    "ISFP": "레트로팝",
    "ESTP": "EDM",
    "ESFP": "신나는 팝"
}

# 기분/날씨/계절/시간대에 따른 스타일
mood_boost = {
    "맑음": "신나는 팝",
    "흐림": "Lofi",
    "비": "감성 발라드",
    "눈": "몽환적 사운드",
    "행복": "EDM",
    "우울": "감성 발라드",
    "설렘": "OST",
    "집중": "Lofi",
    "봄": "드림팝",
    "여름": "신나는 팝",
    "가을": "재즈",
    "겨울": "클래식",
    "아침": "Lofi",
    "점심": "신나는 팝",
    "저녁": "OST",
    "밤": "몽환적 사운드"
}

# 국가에 따른 음악 취향
country_style_preference = {
    "대한민국": "감성 발라드",
    "일본": "OST",
    "미국": "EDM",
    "영국": "재즈",
    "기타": "신나는 팝"
}

# 국가별 기본 추천 수
country_song_count = {
    "대한민국": 3,
    "일본": 3,
    "미국": 4,
    "영국": 3,
    "기타": 3
}
# ------------------ 추천 함수 ------------------
def recommend_music(mbti, weather, mood, season, time_of_day, country):
    print(f"DEBUG: country={country}, mbti={mbti}, weather={weather}, mood={mood}, season={season}, time_of_day={time_of_day}")
    
    base_style = style_mapping.get(mbti.upper(), "다양성 있는 셔플 믹스")
    style_candidates = [base_style]

    for factor in [weather, mood, season, time_of_day]:
        if factor in mood_boost:
            style_candidates.append(mood_boost[factor])

    if country in country_style_preference:
        style_candidates.append(country_style_preference[country])

    final_style = max(set(style_candidates), key=style_candidates.count)
    songs = music_links[final_style]
    random.shuffle(songs)
    count = country_song_count.get(country, 3) + 2
    return final_style, songs[:count]

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="MBTI 음악 추천기 🎧", page_icon="🎵")
st.title("🌤️ MBTI + 날씨 + 기분 + 계절 + 시간 + 국가 기반 음악 추천기 🎶")

mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(style_mapping.keys()))
weather = st.selectbox("오늘의 날씨는 어떤가요?", ["맑음", "흐림", "비", "눈"])
mood = st.selectbox("지금 기분은 어떤가요?", ["행복", "우울", "설렘", "집중"])
season = st.selectbox("현재 계절은?", ["봄", "여름", "가을", "겨울"])
country = st.selectbox("당신이 위치한 국가는 어디인가요?", ["대한민국", "일본", "미국", "영국", "기타"])
country = st.selectbox("당신이 위치한 국가는 어디인가요?", ["대한민국", "일본", "미국", "영국", "기타"])
st.write(f"선택된 국가: {country}")  # 디버깅용 출력


# 시간대 자동 감지
time_now = datetime.now().hour
time_of_day = "아침" if 5 <= time_now < 11 else \
               "점심" if 11 <= time_now < 16 else \
               "저녁" if 16 <= time_now < 21 else "밤"
st.write(f"🕒 현재 시간대: **{time_of_day}**")

if st.button("🎵 음악 추천받기"):
    style, recommendations = recommend_music(mbti, weather, mood, season, time_of_day, country)
    st.success(f"💡 추천 스타일: **{style}**")
    for i, url in enumerate(recommendations, 1):
        st.markdown(f"{i}. [YouTube 링크]({url})")
        st.video(url)
