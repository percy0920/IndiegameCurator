import streamlit as st
import requests

st.set_page_config(page_title="Free Game Finder", page_icon="🎮", layout="centered")

# --- 다국어 지원 딕셔너리 ---
translations = {
    "한국어": {
        "title": "🎮 Free Game Finder",
        "desc": "키워드와 장르를 선택해 지금 바로 무료로 즐길 수 있는 글로벌 PC/웹 게임을 찾아보세요. (API Key 불필요)",
        "search_header": "🔍 게임 검색 조건 설정",
        "keyword_label": "직접 키워드 입력 (예: 영문으로 space, hero, zombie 등)",
        "genre_label": "장르",
        "style_label": "테마 / 스타일",
        "genres": ["전체", "MMORPG", "슈팅 (Shooter)", "전략 (Strategy)", "액션 RPG"],
        "styles": ["전체", "도트/픽셀 (Pixel)", "판타지 (Fantasy)", "SF (Sci-Fi)", "애니메이션 (Anime)"],
        "btn": "🚀 실시간 무료 게임 찾기",
        "result_header": "🎯 실시간 검색 결과",
        "no_result": "💡 조건과 일치하는 게임을 찾지 못했습니다. 다른 키워드나 장르로 시도해보세요!",
        "found": "✨ 총 {}개의 게임을 찾았습니다!",
        "ai_summary": "🤖 AI 큐레이터 요약 (게임 설명)",
    },
    "English": {
        "title": "🎮 Free Game Finder",
        "desc": "Find free-to-play PC/Web games instantly. No API key required.",
        "search_header": "🔍 Search Conditions",
        "keyword_label": "Custom Keyword (e.g., space, hero, zombie)",
        "genre_label": "Genre",
        "style_label": "Theme / Style",
        "genres": ["All", "MMORPG", "Shooter", "Strategy", "Action RPG"],
        "styles": ["All", "Pixel", "Fantasy", "Sci-Fi", "Anime"],
        "btn": "🚀 Search Live Data",
        "result_header": "🎯 Live Search Results",
        "no_result": "💡 No exact match found. Try a different keyword!",
        "found": "✨ Found {} games!",
        "ai_summary": "🤖 AI Curator Summary",
    }
}

# FreeToGame API 태그 매핑
API_GENRES = ["", "mmorpg", "shooter", "strategy", "action-rpg"]
API_STYLES = ["", "pixel", "fantasy", "sci-fi", "anime"]

st.sidebar.header("🌐 Language")
selected_lang = st.sidebar.selectbox("Choose Language", ["한국어", "English"])
t = translations[selected_lang]

st.title(t["title"])
st.markdown(t["desc"])
st.markdown("---")
st.subheader(t["search_header"])

# 키워드 검색 (영문 API이므로 영문 검색을 유도)
user_keyword = st.text_input(t["keyword_label"])

col1, col2 = st.columns(2)
with col1:
    genre_choice = st.selectbox(t["genre_label"], t["genres"])
with col2:
    style_choice = st.selectbox(t["style_label"], t["styles"])

search_button = st.button(t["btn"], type="primary", use_container_width=True)

# --- FreeToGame API 통신 로직 (API Key 불필요) ---
if search_button:
    st.markdown("---")
    st.subheader(t["result_header"])
    
    with st.spinner("전 세계 무료 게임 데이터베이스를 뒤지고 있습니다..."):
        
        # 태그 결합을 위한 리스트 생성
        tags = []
        
        genre_idx = t["genres"].index(genre_choice)
        if API_GENRES[genre_idx]:
            tags.append(API_GENRES[genre_idx])
            
        style_idx = t["styles"].index(style_choice)
        if API_STYLES[style_idx]:
            tags.append(API_STYLES[style_idx])
        
        # API URL 분기 처리
        if len(tags) > 1:
            # 태그가 2개 이상일 때 (filter 엔드포인트)
            url = f"https://www.freetogame.com/api/filter?tag={'.'.join(tags)}"
        elif len(tags) == 1:
            # 태그가 1개일 때
            url = f"https://www.freetogame.com/api/games?category={tags[0]}"
        else:
            # 전체 검색
            url = "https://www.freetogame.com/api/games"

        response = requests.get(url)
        
        if response.status_code == 200:
            games_data = response.json()
            
            # API에서 에러 메시지(status 0)를 보낸 경우 처리
            if isinstance(games_data, dict) and games_data.get("status") == 0:
                games_data = []
                
            # 유저 입력 키워드로 파이썬 내부에서 한번 더 필터링
            if user_keyword.strip() and games_data:
                keyword_lower = user_keyword.lower()
                filtered_data = []
                for game in games_data:
                    if keyword_lower in game.get("title", "").lower() or keyword_lower in game.get("short_description", "").lower():
                        filtered_data.append(game)
                games_data = filtered_data
            
            # 결과가 너무 많으면 최대 10개까지만 표시
            display_games = games_data[:10]
            
            if not display_games:
                st.info(t["no_result"])
            else:
                st.success(t["found"].format(len(games_data)))
                
                for game in display_games:
                    with st.container():
                        col_img, col_info = st.columns([1, 2])
                        
                        with col_img:
                            st.image(game.get("thumbnail"), use_column_width=True)
                                
                        with col_info:
                            st.markdown(f"### **{game.get('title')}**")
                            st.markdown(f"**플랫폼**: 💻 {game.get('platform')} | **장르**: 🏷️ {game.get('genre')}")
                            
                            # 바로가기 링크 제공
                            st.markdown(f"[게임 웹사이트 바로가기]({game.get('game_url')})")
                            
                            st.info(f"**{t['ai_summary']}**\n\n{game.get('short_description')}")
                            
                        st.markdown("---")
        else:
            st.error(f"API 통신 오류가 발생했습니다. (상태 코드: {response.status_code})")