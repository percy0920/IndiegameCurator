import streamlit as st
import requests
import random
import re

st.set_page_config(page_title="One Game Curator", page_icon="🎯", layout="centered")

st.title("🎯 The One Game Curator")
st.markdown("입력하신 키워드가 **실제 게임 소개글이나 태그에 정확히 포함된**, 평가 **'복합적' 이상**의 게임 **단 하나**를 엄선하여 큐레이팅해 드립니다.")
st.markdown("---")

st.subheader("🔍 당신의 취향을 알려주세요")
user_keyword = st.text_input("검색 키워드 (예: 좀비, 농사, Cyberpunk, 오픈월드, 생존)")

search_button = st.button("✨ 나만을 위한 단 하나의 게임 찾기", type="primary", use_container_width=True)

def get_steam_rating_text(ratio):
    if ratio >= 0.95: return "압도적으로 긍정적"
    elif ratio >= 0.80: return "매우 긍정적"
    elif ratio >= 0.70: return "대체로 긍정적"
    elif ratio >= 0.40: return "복합적"
    else: return "부정적"

# HTML 태그 제거용 함수
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).replace('&quot;', "'")

if search_button:
    if not user_keyword.strip():
        st.warning("키워드를 입력해주세요!")
    else:
        st.markdown("---")
        
        with st.spinner("수만 개의 스팀 게임 소개글과 평가를 분석하며 당신을 위한 단 하나의 게임을 찾는 중입니다... (최대 10~15초 소요)"):
            
            keyword_lower = user_keyword.strip().lower()
            
            # 1. 스팀 상점 API로 1차 검색 (관련도 순)
            store_search_url = f"https://store.steampowered.com/api/storesearch/?term={keyword_lower}&l=korean&cc=KR"
            search_res = requests.get(store_search_url)
            
            if search_res.status_code == 200:
                search_data = search_res.json()
                items = search_data.get('items', [])
                
                # 매번 똑같은 게임만 나오지 않도록 상위 10개 결과의 순서를 섞음
                candidates = items[:10]
                random.shuffle(candidates)
                
                selected_game = None
                game_ratio = 0
                game_description = ""
                game_tags = []
                
                # 2. 1차 검색된 게임들을 하나씩 까보며 '엄격한 교차 검증' 진행
                for item in candidates:
                    appid = item.get('id')
                    name = item.get('name', '')
                    
                    # 2-1. SteamSpy API로 평가 점수 및 유저 태그 확인
                    spy_res = requests.get(f"https://steamspy.com/api.php?request=appdetails&appid={appid}")
                    if spy_res.status_code != 200: continue
                    spy_data = spy_res.json()
                    
                    pos = spy_data.get('positive', 0)
                    neg = spy_data.get('negative', 0)
                    total_reviews = pos + neg
                    
                    if total_reviews == 0: continue
                    
                    ratio = pos / total_reviews
                    
                    # [조건 A] 스팀 평가가 '복합적'(40%) 미만이면 가차 없이 탈락
                    if ratio < 0.40: continue
                    
                    # 2-2. Steam 상점 세부 API로 공식 소개글 확인
                    details_res = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=korean")
                    if details_res.status_code != 200: continue
                    details_data = details_res.json()
                    
                    if not details_data or str(appid) not in details_data or not details_data[str(appid)].get('success'):
                        continue
                        
                    app_info = details_data[str(appid)]['data']
                    short_desc = clean_html(app_info.get('short_description', ''))
                    tags_dict = spy_data.get('tags', {})
                    
                    # [조건 B] 키워드가 '공식 소개글', '게임 이름', '유저 태그' 중 하나라도 정확히 포함되어 있는지 검증
                    match_in_desc = keyword_lower in short_desc.lower()
                    match_in_name = keyword_lower in name.lower()
                    match_in_tags = any(keyword_lower in tag.lower() for tag in tags_dict.keys())
                    
                    if match_in_desc or match_in_name or match_in_tags:
                        # 모든 까다로운 조건을 통과한 게임 당첨!
                        selected_game = app_info
                        game_ratio = ratio
                        game_description = short_desc
                        game_tags = list(tags_dict.keys())[:3]
                        break # 단 하나만 찾으면 되므로 루프 종료
                
                # 3. 결과 출력
                if not selected_game:
                    st.error(f"💡 '{user_keyword}' 키워드가 소개글이나 태그에 정확히 포함되면서, 평가가 '복합적' 이상인 게임을 찾지 못했습니다. 키워드를 조금 더 단순하게(예: 생존, RPG) 바꿔보세요.")
                else:
                    appid = selected_game.get('steam_appid')
                    name = selected_game.get('name')
                    rating_text = get_steam_rating_text(game_ratio)
                    
                    st.success("✨ 엄격한 검증을 통과한 완벽한 게임을 찾았습니다!")
                    st.subheader("🎯 큐레이터의 선택")
                    
                    # 게임 헤더 이미지
                    img_url = selected_game.get('header_image', f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg")
                    st.image(img_url, use_column_width=True)
                    
                    st.markdown(f"## **{name}**")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**스팀 평가:** {rating_text} ({int(game_ratio*100)}%)")
                    with col2:
                        price_data = selected_game.get('price_overview', {})
                        price_text = price_data.get('final_formatted', '무료 (Free)') if price_data else "무료 (Free)"
                        st.write(f"**가격:** {price_text}")
                    with col3:
                        st.markdown(f"[➡️ 스팀 상점 페이지로 이동](https://store.steampowered.com/app/{appid})")
                    
                    st.markdown("---")
                    
                    # 4. 전문 비평가 큐레이팅 및 추천 플레이 가이드 (동적 생성)
                    st.markdown("### 🖋️ 전문 비평가의 큐레이팅 노트")
                    
                    # AI가 작성한 것처럼 실제 데이터를 녹여내어 비평 작성
                    tag_str = ", ".join(game_tags) if game_tags else "독창적인"
                    critic_review = f"""
                    **"{user_keyword}"**의 감성을 이토록 훌륭하게 엮어낸 작품이 또 있을까요? 
                    
                    **『{name}』**은(는) {tag_str} 장르의 문법을 따르면서도, 플레이어에게 강렬한 인상을 남깁니다. 스팀에서 **{rating_text}** 평가를 받은 것은 우연이 아닙니다. 
                    
                    *{game_description[:150]}...* 
                    
                    이 게임이 제시하는 세계관과 독보적인 분위기는 당신이 찾던 바로 그 경험을 충족시키기에 충분한 숨겨진 명작입니다.
                    """
                    st.info(critic_review)
                    
                    st.markdown("### 🎮 큐레이터의 추천 플레이 가이드")
                    
                    play_guide = f"""
                    이 게임의 진면목을 100% 즐기기 위해 비평가가 제안하는 3가지 방법론입니다.
                    
                    1. **키워드의 본질에 집중하세요:** 당신이 검색한 **'{user_keyword}'** 요소가 게임 내에서 어떻게 변주되는지 관찰하며 플레이해보세요. 개발자의 깊은 의도를 엿볼 수 있습니다.
                    2. **메커니즘에 몸을 맡기기:** 처음에는 낯설 수 있지만, {game_tags[0] if game_tags else '이 게임 특유의'} 시스템이 요구하는 템포에 익숙해지면 엄청난 몰입감을 선사합니다.
                    3. **공식 소개글의 행간 읽기:** 텍스트와 내러티브를 가볍게 넘기지 마세요. 사소해 보이는 디테일들이 모여 압도적인 후반부 경험을 만들어냅니다.
                    """
                    st.success(play_guide)
                    
                    st.markdown("<p style='text-align: right; color: gray; font-size: small;'>* 본 비평과 가이드는 실제 게임 API 데이터를 기반으로 생성된 큐레이팅 시뮬레이션입니다.</p>", unsafe_allow_html=True)
            else:
                st.error("스팀 서버와 연결할 수 없습니다. 잠시 후 다시 시도해주세요.")