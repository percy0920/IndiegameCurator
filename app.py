import streamlit as st
import requests
import random
import re

# 1. 페이지 설정을 넓은 화면(wide)으로 변경하여 잉여 여백 제거
st.set_page_config(page_title="Retro Game Curator", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

# 2. 강력한 레트로 아케이드 네온 CSS 주입 (여백 제거, 네온 컬러, 글로우 효과)
retro_css = """
<style>
/* 둥근모꼴(레트로 한글) 폰트 불러오기 */
@import url('https://cdn.jsdelivr.net/gh/neodgm/neodgm-web-font@1.530/neodgm/style.css');

/* 기본 배경색 블랙으로 고정 */
html, body, [class*="css"], .stApp {
    background-color: #000000 !important;
}

/* 🎯 갤러그 도트 배경을 화면 전체에 꽉 채우기 (여백 없음) */
.stApp::before {
    content: "";
    position: fixed;
    top: -50%; left: -50%; width: 200%; height: 200%;
    /* 네온 핑크색 갤러그 우주선 패턴 */
    background-image: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 11 11' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23FF0055' fill-opacity='1'%3E%3Crect x='2' y='0' width='1' height='1'/%3E%3Crect x='8' y='0' width='1' height='1'/%3E%3Crect x='3' y='1' width='1' height='1'/%3E%3Crect x='7' y='1' width='1' height='1'/%3E%3Crect x='2' y='2' width='7' height='1'/%3E%3Crect x='1' y='3' width='2' height='1'/%3E%3Crect x='4' y='3' width='3' height='1'/%3E%3Crect x='8' y='3' width='2' height='1'/%3E%3Crect x='0' y='4' width='11' height='1'/%3E%3Crect x='0' y='5' width='1' height='1'/%3E%3Crect x='2' y='5' width='7' height='1'/%3E%3Crect x='10' y='5' width='1' height='1'/%3E%3Crect x='0' y='6' width='1' height='1'/%3E%3Crect x='2' y='6' width='1' height='1'/%3E%3Crect x='8' y='6' width='1' height='1'/%3E%3Crect x='10' y='6' width='1' height='1'/%3E%3Crect x='3' y='7' width='2' height='1'/%3E%3Crect x='6' y='7' width='2' height='1'/%3E%3C/g%3E%3C/svg%3E");
    background-repeat: repeat;
    transform: rotate(-15deg);
    opacity: 0.15; /* 배경 패턴 밝기 조절 */
    z-index: 0;
    pointer-events: none;
}

/* 🎯 불필요한 상단 여백 및 헤더 완전 제거 */
header[data-testid="stHeader"] {
    display: none !important;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
    max-width: 100% !important;
    z-index: 1;
    /* 본문 영역을 반투명 검은 박스로 덮어 글씨가 잘 보이게 함 */
    background-color: rgba(0, 0, 0, 0.8) !important;
    border: 3px solid #00FFFF !important; /* 네온 사이안 테두리 */
    box-shadow: 0 0 20px #00FFFF, inset 0 0 20px #00FFFF !important;
    border-radius: 10px !important;
    margin-top: 1rem !important;
}

/* 🎯 모든 텍스트에 폰트 적용 및 기본 컬러(네온 사이안) + 글로우 효과 */
* {
    font-family: 'NeoDunggeunmo', monospace !important;
}
p, span, div, label, li {
    color: #00FFFF !important;
    text-shadow: 0 0 5px rgba(0, 255, 255, 0.6) !important;
}

/* 제목(h1, h2, h3)은 네온 그린으로 강조 */
h1, h2, h3 {
    color: #39FF14 !important;
    text-shadow: 0 0 10px #39FF14 !important;
    text-align: center;
}

/* 텍스트 입력창 스타일 */
.stTextInput > div > div > input {
    background-color: #000000 !important;
    color: #39FF14 !important; /* 입력 글씨는 네온 그린 */
    border: 3px solid #39FF14 !important;
    border-radius: 0px !important;
    font-size: 22px !important;
    text-align: center;
    box-shadow: 0 0 15px rgba(57, 255, 20, 0.5) !important;
}

/* 버튼 스타일 (네온 핑크) */
.stButton > button {
    background-color: #000000 !important;
    color: #FF0055 !important; 
    border: 4px solid #FF0055 !important;
    border-radius: 0px !important;
    font-size: 26px !important;
    box-shadow: 0 0 20px #FF0055 !important;
    transition: 0.3s;
    margin-top: 1rem !important;
}
.stButton > button:hover {
    background-color: #FF0055 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 40px #FF0055 !important;
    text-shadow: 0 0 10px #FFFFFF !important;
}

/* 사이드바 디자인 */
section[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.95) !important;
    border-right: 3px solid #FF0055 !important;
    box-shadow: 5px 0 15px rgba(255, 0, 85, 0.5) !important;
}
section[data-testid="stSidebar"] * {
    color: #FF0055 !important;
    text-shadow: 0 0 5px rgba(255, 0, 85, 0.5) !important;
}

/* 결과 박스 스타일 */
.stAlert {
    background-color: #000000 !important;
    border: 2px solid #00FFFF !important;
    box-shadow: 0 0 10px #00FFFF !important;
}
.stSuccess {
    background-color: #000000 !important;
    border: 2px solid #39FF14 !important;
    box-shadow: 0 0 10px #39FF14 !important;
}
</style>
"""
st.markdown(retro_css, unsafe_allow_html=True)

# 3. 중복 방지 세션 초기화
if "shown_games" not in st.session_state:
    st.session_state.shown_games = []

# 4. 다국어 지원 딕셔너리 확장
translations = {
    "한국어": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... 당신의 취향을 입력하면 완벽한 게임 단 1개를 엄선해 드립니다.",
        "search_label": "⬇️ 키워드를 입력하세요 (예: 좀비, 생존, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "korean",
        "loading": "데이터베이스 탐색 중... (최대 10초 소요)",
        "no_result": "GAME OVER. 일치하는 새로운 게임이 없습니다. 다른 키워드나 기준을 설정하세요.",
        "found": "STAGE CLEAR! 완벽한 게임을 찾았습니다.",
        "critic_title": "🖋️ 비평가의 큐레이팅 노트",
        "guide_title": "🎮 추천 플레이 가이드",
        "steam_link": "[스팀 상점 접속하기]",
        "rating_label": "평가 필터 기준",
        "ratings": {"모든 평가 (0%+)": 0.0, "복합적 이상 (40%+)": 0.4, "대체로 긍정적 이상 (70%+)": 0.7, "매우 긍정적 이상 (80%+)": 0.8, "압도적으로 긍정적 (95%+)": 0.95}
    },
    "English": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... Enter your taste to get exactly ONE perfect game.",
        "search_label": "⬇️ Enter keyword (e.g. Zombie, Survival, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "english",
        "loading": "Scanning Database... (Takes up to 10s)",
        "no_result": "GAME OVER. No new matching games found. Try a different keyword.",
        "found": "STAGE CLEAR! Perfect game selected.",
        "critic_title": "🖋️ Critic's Note",
        "guide_title": "🎮 Play Guide",
        "steam_link": "[Go to Steam Store]",
        "rating_label": "Minimum Rating",
        "ratings": {"All Ratings (0%+)": 0.0, "Mixed+ (40%+)": 0.4, "Mostly Positive+ (70%+)": 0.7, "Very Positive+ (80%+)": 0.8, "Overwhelmingly Positive (95%+)": 0.95}
    },
    "日本語": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... あなたの好みを入力すると、完璧なゲームを1つ厳選します。",
        "search_label": "⬇️ キーワードを入力 (例: ゾンビ, サバイバル, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "japanese",
        "loading": "データベースを検索中... (最大10秒)",
        "no_result": "GAME OVER. 一致するゲームがありません。別のキーワードをお試しください。",
        "found": "STAGE CLEAR! 完璧なゲームを見つけました。",
        "critic_title": "🖋️ 批評家のキュレーションノート",
        "guide_title": "🎮 おすすめプレイガイド",
        "steam_link": "[Steamストアへ]",
        "rating_label": "最低評価基準",
        "ratings": {"すべての評価 (0%+)": 0.0, "賛否両論以上 (40%+)": 0.4, "やや好評以上 (70%+)": 0.7, "非常に好評以上 (80%+)": 0.8, "圧倒的に好評 (95%+)": 0.95}
    },
    "中文": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... 输入您的喜好，为您精选一款完美的游戏。",
        "search_label": "⬇️ 输入关键字 (例: 丧尸, 生存, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "schinese",
        "loading": "正在搜索数据库... (最多10秒)",
        "no_result": "GAME OVER. 没有找到匹配的新游戏。请尝试其他关键字。",
        "found": "STAGE CLEAR! 找到了完美的游戏。",
        "critic_title": "🖋️ 评论家的策展笔记",
        "guide_title": "🎮 推荐游玩指南",
        "steam_link": "[前往Steam商店]",
        "rating_label": "最低评价标准",
        "ratings": {"所有评价 (0%+)": 0.0, "褒贬不一及以上 (40%+)": 0.4, "多半好评及以上 (70%+)": 0.7, "特别好评及以上 (80%+)": 0.8, "好评如潮 (95%+)": 0.95}
    },
    "Español": {
        "title": "🕹️ THE ONE GAME CURATOR",
        "desc": "INSERT COIN... Ingresa tus gustos para obtener UN juego perfecto.",
        "search_label": "⬇️ Ingresa palabra clave (ej. Zombie, RPG)",
        "btn": "▶ START Curation",
        "lang_code": "spanish",
        "loading": "Buscando en la base de datos... (Hasta 10s)",
        "no_result": "GAME OVER. No se encontraron juegos nuevos. Intenta otra vez.",
        "found": "STAGE CLEAR! Juego perfecto seleccionado.",
        "critic_title": "🖋️ Nota del Crítico",
        "guide_title": "🎮 Guía de Juego",
        "steam_link": "[Ir a la tienda de Steam]",
        "rating_label": "Calificación Mínima",
        "ratings": {"Todas (0%+)": 0.0, "Variadas+ (40%+)": 0.4, "Mayormente Positivas+ (70%+)": 0.7, "Muy Positivas+ (80%+)": 0.8, "Extremadamente Positivas (95%+)": 0.95}
    }
}

# 사이드바 언어 선택
st.sidebar.markdown("### 🌐 SELECT LANGUAGE")
selected_lang = st.sidebar.radio("", ["한국어", "English", "日本語", "中文", "Español"])
t = translations[selected_lang]

# 사이드바 스팀 평가 필터 선택 추가
st.sidebar.markdown("---")
st.sidebar.markdown(f"### ⭐ {t['rating_label']}")
rating_options = list(t['ratings'].keys())
# 기본값으로 '복합적 이상'(인덱스 1) 설정
selected_rating_label = st.sidebar.selectbox("", rating_options, index=1)
min_rating_threshold = t['ratings'][selected_rating_label]

# 5. UI 본문
st.title(t["title"])
st.markdown(f"<p style='text-align: center;'><b>{t['desc']}</b></p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_keyword = st.text_input(t["search_label"])
    search_button = st.button(t["btn"], use_container_width=True)

def get_steam_rating_text(ratio, lang):
    if ratio >= 0.95:
        return {"한국어": "압도적으로 긍정적", "English": "Overwhelmingly Positive", "日本語": "圧倒的に好評", "中文": "好评如潮", "Español": "Extremadamente Positivas"}[lang]
    elif ratio >= 0.80:
        return {"한국어": "매우 긍정적", "English": "Very Positive", "日本語": "非常に好評", "中文": "特别好评", "Español": "Muy Positivas"}[lang]
    elif ratio >= 0.70:
        return {"한국어": "대체로 긍정적", "English": "Mostly Positive", "日本語": "やや好評", "中文": "多半好评", "Español": "Mayormente Positivas"}[lang]
    elif ratio >= 0.40:
        return {"한국어": "복합적", "English": "Mixed", "日本語": "賛否両論", "中文": "褒贬不一", "Español": "Variadas"}[lang]
    else:
        return {"한국어": "부정적", "English": "Negative", "日本語": "不評", "中文": "差评", "Español": "Negativas"}[lang]

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).replace('&quot;', "'")

# 6. 검색 및 검증 로직
if search_button:
    if not user_keyword.strip():
        st.warning("PLEASE ENTER KEYWORD!")
    else:
        with st.spinner(t["loading"]):
            keyword_lower = user_keyword.strip().lower()
            steam_lang = t["lang_code"]
            
            store_search_url = f"https://store.steampowered.com/api/storesearch/?term={keyword_lower}&l={steam_lang}&cc=KR"
            search_res = requests.get(store_search_url)
            
            if search_res.status_code == 200:
                search_data = search_res.json()
                items = search_data.get('items', [])
                
                candidates = items[:15]
                random.shuffle(candidates)
                
                selected_game = None
                game_ratio = 0
                game_description = ""
                game_tags = []
                
                for item in candidates:
                    appid = item.get('id')
                    name = item.get('name', '')
                    
                    if appid in st.session_state.shown_games:
                        continue
                        
                    spy_res = requests.get(f"https://steamspy.com/api.php?request=appdetails&appid={appid}")
                    if spy_res.status_code != 200: continue
                    spy_data = spy_res.json()
                    
                    pos = spy_data.get('positive', 0)
                    neg = spy_data.get('negative', 0)
                    total_reviews = pos + neg
                    
                    if total_reviews == 0: continue
                    ratio = pos / total_reviews
                    
                    # 🎯 유저가 사이드바에서 선택한 평가 기준(min_rating_threshold) 반영
                    if ratio < min_rating_threshold: continue 
                    
                    details_res = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l={steam_lang}")
                    if details_res.status_code != 200: continue
                    details_data = details_res.json()
                    
                    if not details_data or str(appid) not in details_data or not details_data[str(appid)].get('success'):
                        continue
                        
                    app_info = details_data[str(appid)]['data']
                    short_desc = clean_html(app_info.get('short_description', ''))
                    tags_dict = spy_data.get('tags', {})
                    
                    match_in_desc = keyword_lower in short_desc.lower()
                    match_in_name = keyword_lower in name.lower()
                    match_in_tags = any(keyword_lower in tag.lower() for tag in tags_dict.keys())
                    
                    if match_in_desc or match_in_name or match_in_tags:
                        selected_game = app_info
                        game_ratio = ratio
                        game_description = short_desc
                        game_tags = list(tags_dict.keys())[:3]
                        
                        st.session_state.shown_games.append(appid)
                        break 
                
                if not selected_game:
                    st.error(t["no_result"])
                else:
                    appid = selected_game.get('steam_appid')
                    name = selected_game.get('name')
                    rating_text = get_steam_rating_text(game_ratio, selected_lang)
                    
                    st.markdown("---")
                    st.markdown(f"### {t['found']}")
                    
                    res_col1, res_col2 = st.columns([1, 1])
                    
                    with res_col1:
                        img_url = selected_game.get('header_image', f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg")
                        st.image(img_url, use_column_width=True)
                        st.markdown(f"## [{name}]")
                        st.write(f"▶ RATING: {rating_text} ({int(game_ratio*100)}%)")
                        st.markdown(f"▶ {t['steam_link']}(https://store.steampowered.com/app/{appid})")
                        
                    with res_col2:
                        st.markdown(f"#### {t['critic_title']}")
                        tag_str = ", ".join(game_tags) if game_tags else "독창적인(Original)"
                        
                        # 다국어 큐레이팅 노트 생성
                        if selected_lang == "한국어":
                            critic_review = f"**'{user_keyword}'**의 매력을 완벽하게 담아낸 수작입니다. 스팀 평가 **{rating_text}**는 결코 거짓말을 하지 않습니다.\n\n*{game_description[:100]}...*\n\n이 텍스트가 증명하듯, {tag_str} 요소를 엮어낸 이 게임은 당신이 찾던 바로 그 몰입감을 선사할 것입니다."
                        elif selected_lang == "English":
                            critic_review = f"A masterpiece that perfectly captures the essence of **'{user_keyword}'**. The **{rating_text}** rating on Steam is well-deserved.\n\n*{game_description[:100]}...*\n\nWith its {tag_str} elements, this game will provide exactly the immersive experience you are looking for."
                        elif selected_lang == "日本語":
                            critic_review = f"**'{user_keyword}'**の魅力を完璧に表現した傑作です。Steam評価**{rating_text}**は決して嘘をつきません。\n\n*{game_description[:100]}...*\n\n{tag_str}の要素を組み合わせたこのゲームは、あなたが求めていた没入感を提供してくれるでしょう。"
                        elif selected_lang == "中文":
                            critic_review = f"这是一部完美捕捉了**'{user_keyword}'**魅力的杰作。Steam上的**{rating_text}**评价绝非虚言。\n\n*{game_description[:100]}...*\n\n凭借其{tag_str}元素，这款游戏将提供您一直在寻找的沉浸式体验。"
                        else: # Español
                            critic_review = f"Una obra maestra que captura perfectamente la esencia de **'{user_keyword}'**. La calificación de **{rating_text}** en Steam es bien merecida.\n\n*{game_description[:100]}...*\n\nCon sus elementos de {tag_str}, este juego proporcionará exactamente la experiencia inmersiva que buscas."
                        
                        st.info(critic_review)
                        
                        st.markdown(f"#### {t['guide_title']}")
                        
                        # 다국어 플레이 가이드 생성
                        if selected_lang == "한국어":
                            play_guide = f"1. **'{user_keyword}'** 키워드가 게임 속에서 어떻게 표현되었는지 관찰하세요.\n2. 실패를 두려워하지 말고 이 게임만의 템포에 몸을 맡겨보세요.\n3. 사운드를 꼭 켜고 세계관에 동화되는 것을 추천합니다."
                        elif selected_lang == "English":
                            play_guide = f"1. Observe how the keyword **'{user_keyword}'** is represented in the game.\n2. Don't fear failure; adapt to the unique tempo of this game.\n3. Highly recommended to play with the sound ON to fully immerse yourself."
                        elif selected_lang == "日本語":
                            play_guide = f"1. **'{user_keyword}'**というキーワードがゲーム内でどのように表現されているか観察してください。\n2. 失敗を恐れず、このゲーム独自のテンポに身を任せてみましょう。\n3. サウンドをオンにして世界観に没入することを強くお勧めします。"
                        elif selected_lang == "中文":
                            play_guide = f"1. 观察**'{user_keyword}'**关键字在游戏中的表现方式。\n2. 不要害怕失败；适应这款游戏独特的节奏。\n3. 强烈建议开启声音以完全沉浸在世界观中。"
                        else: # Español
                            play_guide = f"1. Observa cómo se representa la palabra clave **'{user_keyword}'** en el juego.\n2. No temas al fracaso; adáptate al ritmo único de este juego.\n3. Se recomienda encarecidamente jugar con el sonido activado para sumergirte por completo."
                            
                        st.success(play_guide)
            else:
                st.error("NETWORK ERROR. Please try again.")