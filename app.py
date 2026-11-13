import streamlit as st
import requests
import random

# 페이지 설정
st.set_page_config(
    page_title="Indie Game Vibe Matcher",
    page_icon="🎮",
    layout="centered"
)

# 타이틀 및 소개
st.title("🎮 Indie Game Finder")
st.markdown("원하는 장르, 플레이 방식, 그래픽 스타일을 선택하면 나에게 딱 맞는 인디 게임을 추천해 드립니다.")
st.markdown("---")

# 1. 필터 섹션 (사이드바 또는 메인 폼)
st.subheader("🔍 게임 검색 조건 설정")

col1, col2, col3 = st.columns(3)

with col1:
    genre_choice = st.selectbox(
        "장르 (Genre)",
        ["전체", "RPG", "Action", "Strategy", "Adventure", "Indie"]
    )

with col2:
    play_choice = st.selectbox(
        "플레이 방식",
        ["전체", "멀티플레이 (Multiplayer)", "싱글플레이 (Singleplayer)"]
    )

with col3:
    style_choice = st.selectbox(
        "그래픽 스타일",
        ["전체", "도트 / 픽셀 (Pixel Art)", "3D", "2D", "로파이 (Lo-Fi)"]
    )

# 검색 버튼
search_button = st.button("🚀 내 취향 게임 찾기", type="primary", use_container_width=True)

# 샘플 데이터 (API 키가 없거나 호출 실패 시 보여줄 백업 데이터)
SAMPLE_GAMES = [
    {
        "name": "Barony",
        "genres": ["RPG", "Action", "Indie"],
        "tags": ["Pixel Art", "RPG", "Multiplayer", "Dungeon Crawler"],
        "rating": 4.5,
        "description": "고전 도트 그래픽 기반의 1인칭 로그라이크 RPG로, 최대 4인 온라인 멀티플레이를 지원합니다. 친구들과 함께 던전을 탐험하며 함정을 피하고 협동 플레이를 즐기기에 최적화되어 있습니다.",
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Stardew Valley",
        "genres": ["Indie", "Simulation", "RPG"],
        "tags": ["Pixel Art", "Multiplayer", "Simulation", "Relaxing"],
        "rating": 4.9,
        "description": "할아버지의 오래된 농장 부지를 물려받아 진행하는 오픈에어 농장 경영 RPG입니다. 도트 그래픽의 따뜻한 감성과 최대 4인 멀티플레이를 지원하여 친구들과 함께 농장을 가꿀 수 있습니다.",
        "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Dead Cells",
        "genres": ["Action", "Indie"],
        "tags": ["Pixel Art", "Action", "Singleplayer", "Roguelike"],
        "rating": 4.8,
        "description": "로그배니아 스타일의 빠른 액션 플랫포머 게임입니다. 정교한 픽셀 아트와 긴장감 넘치는 전투 시스템이 특징이며, 몰입도 높은 싱글플레이 경험을 제공합니다.",
        "image": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=600&q=80"
    },
    {
        "name": "Terraria",
        "genres": ["Adventure", "Action", "Indie"],
        "tags": ["Pixel Art", "Multiplayer", "Sandbox", "Adventure"],
        "rating": 4.7,
        "description": "파고, 싸우고, 탐험하고, 건설하세요! 무엇이든 가능성인 세상에서 도트 그래픽으로 구현된 방대한 세계를 친구들과 함께 멀티플레이로 탐험하는 샌드박스 게임입니다.",
        "image": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=600&q=80"
    }
]

# 2. 결과 출력 로직
if search_button:
    st.markdown("---")
    st.subheader("🎯 추천 결과")
    
    # 필터 조건 매칭 시뮬레이션 (데모용 필터링)
    filtered_games = []
    for game in SAMPLE_GAMES:
        match = True
        if genre_choice != "전체" and genre_choice not in game["genres"]:
            match = False
        if "멀티" in play_choice and "Multiplayer" not in game["tags"]:
            match = False
        if "싱글" in play_choice and "Singleplayer" not in game["tags"]:
            match = False
        if "도트" in style_choice and "Pixel Art" not in game["tags"]:
            match = False
            
        if match:
            filtered_games.append(game)
            
    # 조건에 정확히 일치하는 결과가 없으면 전체 샘플 중 무작위 혹은 근접 결과 출력 (Edge Case Handling)
    if not filtered_games:
        st.info("💡 선택하신 조건과 정확히 일치하는 게임이 없어, 가장 인기 있는 인디 게임들을 대신 추천해 드립니다!")
        filtered_games = SAMPLE_GAMES[:2]
    else:
        st.success(f"✨ 총 {len(filtered_games)}개의 어울리는 게임을 찾았습니다!")

    # 카드 그리드 형태로 결과 출력
    for game in filtered_games:
        with st.container():
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                st.image(game["image"], use_column_width=True)
                
            with col_info:
                st.markdown(f"### **{game['name']}** (평점: ⭐ {game['rating']})")
                
                # 태그 뱃지 표시
                tag_markdown = " ".join([f"`{tag}`" for tag in game["tags"]])
                st.markdown(f"**태그**: {tag_markdown}")
                
                # AI 요약 박스 시뮬레이션
                st.info(f"🤖 **AI 큐레이터 요약**\n\n{game['description']}")
                
            st.markdown("---")

# 하단 푸터
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by RAWG API & Streamlit | Indie Game Vibe Matcher Demo</p>", 
    unsafe_allow_html=True
)