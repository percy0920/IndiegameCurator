import streamlit as st
import requests
import random

st.set_page_config(page_title="One Game Curator", page_icon="🎯", layout="centered")

st.title("🎯 The One Game Curator")
st.markdown("입력하신 키워드에 완벽하게 부합하는, 스팀 평가 **'복합적' 이상**의 게임 **단 하나**를 전문 비평가의 시선으로 큐레이팅해 드립니다.")
st.markdown("---")

# 검색어 입력
st.subheader("🔍 당신의 취향을 알려주세요")
user_tag = st.text_input("스팀 태그(키워드) 영문 입력 (예: Story Rich, Survival, Zombies, Pixel Graphics, Open World)")

search_button = st.button("✨ 나만을 위한 단 하나의 게임 찾기", type="primary", use_container_width=True)

# 스팀 평가 등급 계산 함수 (긍정적 리뷰 비율에 따라)
def get_steam_rating_text(ratio):
    if ratio >= 0.95: return "압도적으로 긍정적"
    elif ratio >= 0.80: return "매우 긍정적"
    elif ratio >= 0.70: return "대체로 긍정적"
    elif ratio >= 0.40: return "복합적"
    else: return "부정적"

if search_button:
    if not user_tag.strip():
        st.warning("키워드를 입력해주세요! (예: Cyberpunk, Cute, Horror)")
    else:
        st.markdown("---")
        
        with st.spinner("방대한 스팀 라이브러리에서 당신을 위한 단 하나의 게임을 발굴하고 비평을 작성 중입니다..."):
            
            # 1. SteamSpy API 호출
            url = f"https://steamspy.com/api.php?request=tag&tag={user_tag.strip()}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                games = list(data.values())
                
                if not games:
                    st.error(f"💡 '{user_tag}' 키워드에 해당하는 게임을 찾지 못했습니다. 스펠링을 확인하거나 다른 키워드를 시도해보세요.")
                else:
                    # 2. '복합적' 이상 필터링 로직 (긍정적 리뷰 40% 이상)
                    filtered_games = []
                    for game in games:
                        pos = game.get('positive', 0)
                        neg = game.get('negative', 0)
                        total_reviews = pos + neg
                        
                        if total_reviews > 0:
                            ratio = pos / total_reviews
                            # ratio가 0.4 이상이면 '복합적' 이상의 평가를 받은 게임
                            if ratio >= 0.40:
                                game['ratio'] = ratio
                                filtered_games.append(game)
                    
                    if not filtered_games:
                        st.warning("조건(복합적 평가 이상)을 만족하는 게임이 없습니다.")
                    else:
                        # 3. 필터링된 게임 중 최상위권(인기도순 상위 20개) 중에서 무작위로 딱 1개 선택
                        # (항상 똑같은 게임만 나오면 재미없으므로 약간의 무작위성 부여)
                        top_candidates = filtered_games[:20]
                        selected_game = random.choice(top_candidates)
                        
                        app_id = selected_game.get('appid')
                        name = selected_game.get('name')
                        ratio = selected_game.get('ratio')
                        rating_text = get_steam_rating_text(ratio)
                        
                        st.subheader("🎯 큐레이터의 선택")
                        
                        # 게임 헤더 이미지
                        img_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
                        st.image(img_url, use_column_width=True)
                        
                        st.markdown(f"## **{name}**")
                        
                        # 기본 정보
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**스팀 평가:** {rating_text} ({int(ratio*100)}%)")
                        with col2:
                            price = selected_game.get('price', '0')
                            st.write(f"**가격:** {'무료' if str(price) == '0' else f'${int(price)/100:.2f}'}")
                        with col3:
                            st.markdown(f"[➡️ 스팀 상점 페이지로 이동](https://store.steampowered.com/app/{app_id})")
                        
                        st.markdown("---")
                        
                        # 4. 전문 비평가의 큐레이팅 및 플레이 가이드 (LLM 프롬프트 시뮬레이션)
                        # 실제 기획서의 'AI Prompt' 항목에 들어갈 내용의 결과물입니다.
                        st.markdown("### 🖋️ 전문 비평가의 큐레이팅 노트")
                        
                        critic_review = f"""
                        **"{user_tag.capitalize()}"** 장르의 문법을 새롭게 정의하는 작품입니다. 
                        
                        **『{name}』**은(는) 단순히 스팀에서 **{rating_text}** 평가를 받은 것을 넘어, 이 키워드를 검색한 플레이어에게 가장 깊이 있는 경험을 선사할 수 있는 숨겨진 원석입니다. 이 게임이 가진 고유한 메커니즘과 아트워크의 조화는 타겟 장르의 한계를 뛰어넘는 몰입감을 제공합니다. 대중적인 찬사와 함께, 개발자가 의도한 섬세한 디테일들이 플레이어의 발걸음을 이끌 것입니다.
                        """
                        st.info(critic_review)
                        
                        st.markdown("### 🎮 큐레이터의 추천 플레이 가이드")
                        
                        play_guide = f"""
                        이 게임의 진정한 재미를 끌어내기 위해 다음의 플레이 방식을 적극 권장합니다:
                        
                        1. **속도를 늦추고 세계에 동화되세요:** 이 게임은 목표를 향해 무작정 달려가는 것보다, 세계관 내에 배치된 오브젝트나 텍스트를 천천히 음미할 때 그 진가가 드러납니다.
                        2. **실패를 내러티브의 일부로 받아들이기:** 진행 과정에서 마주하는 시행착오나 게임오버를 스트레스로 여기지 마세요. 이 게임에서 실패는 다음 챕터를 위한 훌륭한 튜토리얼입니다.
                        3. **사운드 온(Sound-On) 필수:** 가능하다면 헤드폰을 착용하세요. 배경음악과 효과음이 게임의 분위기를 완성하는 핵심 요소입니다.
                        """
                        st.success(play_guide)
                        
                        st.markdown("<p style='text-align: right; color: gray; font-size: small;'>* 본 비평과 가이드는 게임 데이터를 기반으로 생성된 AI 큐레이팅 시뮬레이션입니다.</p>", unsafe_allow_html=True)
            else:
                st.error("API 서버와 연결할 수 없습니다. 잠시 후 다시 시도해주세요.")