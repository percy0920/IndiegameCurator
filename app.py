import streamlit as st
import requests
import random
import re

# 1. 페이지 설정 (넓게 보기, 제목 설정)
st.set_page_config(page_title="Retro Game Curator", page_icon="🕹️", layout="centered")

# 2. 레트로 비디오 게임 CSS 스타일 주입
retro_css = """
<style>
/* 레트로 한글 폰트 (둥근모꼴) 및 영문 픽셀 폰트 불러오기 */
@import url('https://cdn.jsdelivr.net/gh/neodgm/neodgm-web-font@1.530/neodgm/style.css');
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

/* 전체 폰트 및 배경색 적용 */
html, body, [class*="css"] {
    font-family: 'NeoDunggeunmo', 'Press Start 2P', monospace !important;
    background-color: #111111 !important;
    color: #33FF33 !important; /* 네온 그린 텍스트 */
}

/* 텍스트 인풋 박스 스타일 */
.stTextInput > div > div > input {
    background-color: #000000 !important;
    color: #33FF33 !important;
    border: 4px solid #33FF33 !important;
    border-radius: 0px !important;
    font-size: 18px !important;
}

/* 버튼 스타일 */
.stButton > button {
    background-color: #000000 !important;
    color: #FF0055 !important; /* 네온 핑크 */
    border: 4px solid #FF0055 !important;
    border-radius: 0px !important;
    font-size: 20px !important;
    transition: 0.2s;
}
.stButton > button:hover {
    background-color: #FF0055 !important;
    color: #FFFFFF !important;
    border: 4px solid #FFFFFF !important;
}

/* 정보 박스(비평가 노트 등) 스타일 */
.stAlert {
    background-color: #000000 !important;
    color: #00FFFF !important; /* 사이안 */
    border: 4px solid #00FFFF !important;
    border-radius: 0px !important;
}
.stSuccess {
    background-color: #000000 !important;
    color: #FFFF00 !important; /* 옐로우 */
    border: 4px solid #FFFF00 !important;
    border-radius: 0px !important;
}
</style>
"""
st.markdown(retro_css, unsafe_allow_html=True)

# 3. 중복 추천 방지를 위한 세션 상태(Session State) 초기화
if "shown_games" not in st.session_state:
    st.session_state.shown_games = []

# 4. 다국어 지원 딕셔너리
translations = {
    "한국어": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... 당신의 취향을 입력하면 완벽한 게임 단 1개를 엄선해 드립니다.",
        "search_label": "> 키워드를 입력하세요 (예: 좀비, 생존, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "korean",
        "loading": "데이터베이스 탐색 중... (최대 10초 소요)",
        "no_result": "GAME OVER. 일치하는 새로운 게임이 없습니다. 다른 키워드를 입력하세요.",
        "found": "STAGE CLEAR! 완벽한 게임을 찾았습니다.",
        "critic_title": "🖋️ 비평가의 큐레이팅 노트",
        "guide_title": "🎮 큐레이터의 추천 플레이 가이드",
        "steam_link": "[스팀 상점 접속하기]"
    },
    "English": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... Enter your taste to get exactly ONE perfect game.",
        "search_label": "> Enter keyword (e.g. Zombie, Survival, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "english",
        "loading": "Scanning Database... (Takes up to 10s)",
        "no_result": "GAME OVER. No new matching games found. Try a different keyword.",
        "found": "STAGE CLEAR! Perfect game selected.",
        "critic_title": "🖋️ Critic's Curation Note",
        "guide_title": "🎮 Recommended Play Guide",
        "steam_link": "[Go to Steam Store]"
    }
}

# 사이드바 언어 선택
st.sidebar.markdown("### 🌐 SELECT LANGUAGE")
selected_lang = st.sidebar.radio("", ["한국어", "English"])
t = translations[selected_lang]

# 5. 메인 화면 UI 구성
st.title(t["title"])
st.markdown(f"**{t['desc']}**")
st.markdown("---")

user_keyword = st.text_input(t["search_label"])
search_button = st.button(t["btn"], use_container_width=True)

# 평점 텍스트 변환기
def get_steam_rating_text(ratio, lang):
    if lang == "한국어":
        if ratio >= 0.95: return "압도적으로 긍정적"
        elif ratio >= 0.80: return "매우 긍정적"
        elif ratio >= 0.70: return "대체로 긍정적"
        elif ratio >= 0.40: return "복합적"
        else: return "부정적"
    else:
        if ratio >= 0.95: return "Overwhelmingly Positive"
        elif ratio >= 0.80: return "Very Positive"
        elif ratio >= 0.70: return "Mostly Positive"
        elif ratio >= 0.40: return "Mixed"
        else: return "Negative"

# HTML 태그 제거 함수
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).replace('&quot;', "'")

# 6. 검색 로직 (중복 방지 및 교차 검증)
if search_button:
    if not user_keyword.strip():
        st.warning("PLEASE ENTER KEYWORD!")
    else:
        with st.spinner(t["loading"]):
            keyword_lower = user_keyword.strip().lower()
            steam_lang = t["lang_code"]
            
            # 스팀 검색 API 호출
            store_search_url = f"https://store.steampowered.com/api/storesearch/?term={keyword_lower}&l={steam_lang}&cc=KR"
            search_res = requests.get(store_search_url)
            
            if search_res.status_code == 200:
                search_data = search_res.json()
                items = search_data.get('items', [])
                
                # 순서 무작위 셔플
                candidates = items[:15]
                random.shuffle(candidates)
                
                selected_game = None
                game_ratio = 0
                game_description = ""
                game_tags = []
                
                for item in candidates:
                    appid = item.get('id')
                    name = item.get('name', '')
                    
                    # [중복 방지 로직] 이미 추천했던 게임이면 패스!
                    if appid in st.session_state.shown_games:
                        continue
                        
                    # SteamSpy 평가 및 태그 확인
                    spy_res = requests.get(f"https://steamspy.com/api.php?request=appdetails&appid={appid}")
                    if spy_res.status_code != 200: continue
                    spy_data = spy_res.json()
                    
                    pos = spy_data.get('positive', 0)
                    neg = spy_data.get('negative', 0)
                    total_reviews = pos + neg
                    
                    if total_reviews == 0: continue
                    ratio = pos / total_reviews
                    
                    if ratio < 0.40: continue # '복합적' 미만 탈락
                    
                    # 공식 소개글 확인
                    details_res = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l={steam_lang}")
                    if details_res.status_code != 200: continue
                    details_data = details_res.json()
                    
                    if not details_data or str(appid) not in details_data or not details_data[str(appid)].get('success'):
                        continue
                        
                    app_info = details_data[str(appid)]['data']
                    short_desc = clean_html(app_info.get('short_description', ''))
                    tags_dict = spy_data.get('tags', {})
                    
                    # 키워드 교차 검증 (소개글, 제목, 태그 중 하나라도 일치하면 OK)
                    match_in_desc = keyword_lower in short_desc.lower()
                    match_in_name = keyword_lower in name.lower()
                    match_in_tags = any(keyword_lower in tag.lower() for tag in tags_dict.keys())
                    
                    if match_in_desc or match_in_name or match_in_tags:
                        selected_game = app_info
                        game_ratio = ratio
                        game_description = short_desc
                        game_tags = list(tags_dict.keys())[:3]
                        
                        # 당첨된 게임의 ID를 세션에 저장하여 다음 번엔 안 나오게 함
                        st.session_state.shown_games.append(appid)
                        break 
                
                # 결과 출력 UI
                if not selected_game:
                    st.error(t["no_result"])
                else:
                    appid = selected_game.get('steam_appid')
                    name = selected_game.get('name')
                    rating_text = get_steam_rating_text(game_ratio, selected_lang)
                    
                    st.markdown("---")
                    st.markdown(f"### {t['found']}")
                    
                    # 게임 이미지
                    img_url = selected_game.get('header_image', f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg")
                    st.image(img_url, use_column_width=True)
                    
                    st.markdown(f"## [{name}]")
                    
                    st.write(f"▶ RATING: {rating_text} ({int(game_ratio*100)}%)")
                    st.markdown(f"▶ {t['steam_link']}(https://store.steampowered.com/app/{appid})")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 큐레이팅 노트 (Alert 스타일)
                    st.markdown(f"#### {t['critic_title']}")
                    tag_str = ", ".join(game_tags) if game_tags else "독창적인"
                    
                    if selected_lang == "한국어":
                        critic_review = f"**'{user_keyword}'**의 매력을 완벽하게 담아낸 수작입니다. 스팀 평가 **{rating_text}**는 결코 거짓말을 하지 않습니다.\n\n*{game_description[:100]}...*\n\n이 텍스트가 증명하듯, {tag_str} 요소를 엮어낸 이 게임은 당신이 찾던 바로 그 몰입감을 선사할 것입니다."
                    else:
                        critic_review = f"A masterpiece that perfectly captures the essence of **'{user_keyword}'**. The **{rating_text}** rating on Steam is well-deserved.\n\n*{game_description[:100]}...*\n\nWith its {tag_str} elements, this game will provide exactly the immersive experience you are looking for."
                    
                    st.info(critic_review)
                    
                    # 플레이 가이드 (Success 스타일)
                    st.markdown(f"#### {t['guide_title']}")
                    if selected_lang == "한국어":
                        play_guide = f"1. **'{user_keyword}'** 키워드가 게임 속에서 어떻게 표현되었는지 관찰하세요.\n2. 실패를 두려워하지 말고 이 게임만의 템포에 몸을 맡겨보세요.\n3. 사운드를 꼭 켜고 세계관에 동화되는 것을 추천합니다."
                    else:
                        play_guide = f"1. Observe how the keyword **'{user_keyword}'** is represented in the game.\n2. Don't fear failure; adapt to the unique tempo of this game.\n3. Highly recommended to play with the sound ON to fully immerse yourself."
                        
                    st.success(play_guide)
            else:
                st.error("NETWORK ERROR. Please try again.")