"""
三島商工会議所 80周年ビジョン ダッシュボード
セセラギズム - 湧き上がれ、鳴り響け -

このダッシュボードは、三島商工会議所の80周年ビジョン提案書を
インタラクティブに可視化するStreamlitアプリケーションです。
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================================
# ページ設定
# ============================================================
st.set_page_config(
    page_title="三島商工会議所 80周年ビジョン | セセラギズム",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# カスタムCSS
# ============================================================
def inject_custom_css() -> None:
    """水をモチーフにしたブルー・ティール系のカスタムCSSを注入する。"""
    st.markdown(
        """
        <style>
        /* ---------- 全体フォント・背景 ---------- */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif;
        }

        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* ---------- サイドバー ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a2540 0%, #0d3b66 40%, #1a6b8a 100%);
            color: #ffffff;
        }
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stRadio label span,
        section[data-testid="stSidebar"] .stRadio label p,
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            color: #ffffff !important;
            font-size: 1.05rem;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.25);
        }

        /* ---------- ヒーローセクション ---------- */
        .hero-section {
            background: linear-gradient(135deg, #0a2540 0%, #1a6b8a 50%, #48b4a0 100%);
            border-radius: 16px;
            padding: 2.5rem 3rem;
            margin-bottom: 2rem;
            color: #ffffff;
            position: relative;
            overflow: hidden;
        }
        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
            border-radius: 50%;
        }
        .hero-section h1 {
            font-size: 2.2rem;
            font-weight: 900;
            margin-bottom: 0.4rem;
            color: #ffffff !important;
            letter-spacing: 0.04em;
        }
        .hero-section p {
            font-size: 1.1rem;
            opacity: 0.92;
            line-height: 1.7;
            color: #e0f7fa !important;
        }
        .hero-subtitle {
            font-size: 0.95rem;
            opacity: 0.78;
            margin-top: 0.2rem;
            color: #b2ebf2 !important;
        }

        /* ---------- メトリックカード ---------- */
        .metric-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.6rem 1.4rem;
            box-shadow: 0 2px 12px rgba(10,37,64,0.08);
            border-left: 5px solid #1a6b8a;
            margin-bottom: 1rem;
            transition: transform 0.18s, box-shadow 0.18s;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(10,37,64,0.13);
        }
        .metric-card .metric-label {
            font-size: 0.85rem;
            color: #607d8b;
            margin-bottom: 0.25rem;
            font-weight: 500;
        }
        .metric-card .metric-value {
            font-size: 1.7rem;
            font-weight: 900;
            color: #0a2540;
        }
        .metric-card .metric-desc {
            font-size: 0.82rem;
            color: #78909c;
            margin-top: 0.35rem;
            line-height: 1.55;
        }

        /* ---------- タイムラインカード ---------- */
        .timeline-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.8rem 1.5rem 1.4rem 1.5rem;
            box-shadow: 0 2px 12px rgba(10,37,64,0.07);
            text-align: center;
            position: relative;
            min-height: 280px;
            transition: transform 0.18s, box-shadow 0.18s;
        }
        .timeline-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(10,37,64,0.12);
        }
        .timeline-card.active {
            border: 3px solid #1a6b8a;
            background: linear-gradient(180deg, #e0f7fa 0%, #ffffff 40%);
        }
        .timeline-year {
            display: inline-block;
            background: linear-gradient(135deg, #0d3b66, #1a6b8a);
            color: #fff;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            margin-bottom: 0.8rem;
        }
        .timeline-year.current {
            background: linear-gradient(135deg, #00897b, #26c6da);
            font-size: 0.95rem;
            padding: 0.35rem 1.2rem;
        }
        .timeline-theme {
            font-size: 1.5rem;
            font-weight: 900;
            color: #0a2540;
            margin: 0.6rem 0 0.25rem 0;
        }
        .timeline-stage {
            font-size: 0.85rem;
            color: #1a6b8a;
            font-weight: 600;
            margin-bottom: 0.7rem;
        }
        .timeline-desc {
            font-size: 0.82rem;
            color: #546e7a;
            line-height: 1.65;
        }

        /* ---------- コンセプトカード ---------- */
        .concept-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.4rem;
            box-shadow: 0 2px 10px rgba(10,37,64,0.06);
            margin-bottom: 0.8rem;
            border-left: 4px solid #26c6da;
            transition: transform 0.15s;
        }
        .concept-card:hover {
            transform: translateX(4px);
        }
        .concept-card .concept-icon {
            font-size: 1.5rem;
            margin-bottom: 0.3rem;
        }
        .concept-card .concept-title {
            font-weight: 700;
            color: #0a2540;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }
        .concept-card .concept-text {
            font-size: 0.85rem;
            color: #607d8b;
            line-height: 1.6;
        }

        /* ---------- フィロソフィーカード ---------- */
        .philosophy-card {
            background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
            border-radius: 14px;
            padding: 1.6rem 1.4rem;
            text-align: center;
            margin-bottom: 0.8rem;
            border: 1px solid #80deea;
            transition: transform 0.18s, box-shadow 0.18s;
        }
        .philosophy-card:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 16px rgba(26,107,138,0.15);
        }
        .philosophy-card .philosophy-title {
            font-size: 1.2rem;
            font-weight: 900;
            color: #0a2540;
        }
        .philosophy-card .philosophy-desc {
            font-size: 0.82rem;
            color: #37474f;
            margin-top: 0.4rem;
            line-height: 1.55;
        }

        /* ---------- サブコピーカード ---------- */
        .subcopy-card {
            background: #0a2540;
            border-radius: 12px;
            padding: 1.4rem;
            text-align: center;
            margin-bottom: 0.6rem;
            transition: transform 0.15s;
        }
        .subcopy-card:hover {
            transform: scale(1.03);
        }
        .subcopy-card p {
            color: #e0f7fa !important;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.06em;
        }

        /* ---------- ナラティブ引用 ---------- */
        .narrative-box {
            background: linear-gradient(135deg, #0d3b66 0%, #1a6b8a 100%);
            border-radius: 14px;
            padding: 2rem 2.5rem;
            color: #ffffff;
            margin: 1.5rem 0;
            position: relative;
        }
        .narrative-box::before {
            content: '\u201C';
            font-size: 4rem;
            position: absolute;
            top: 0.2rem;
            left: 1rem;
            opacity: 0.2;
            font-family: serif;
            color: #80deea;
        }
        .narrative-box p {
            font-size: 1.05rem;
            line-height: 1.85;
            color: #e0f7fa !important;
        }
        .narrative-box .narrative-emphasis {
            font-size: 1.25rem;
            font-weight: 900;
            color: #80deea !important;
            display: block;
            margin-top: 0.8rem;
        }

        /* ---------- 統計ハイライトカード ---------- */
        .stat-highlight {
            background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
            border-radius: 14px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid #b2ebf2;
        }
        .stat-highlight .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            color: #0d3b66;
        }
        .stat-highlight .stat-label {
            font-size: 0.9rem;
            color: #607d8b;
            margin-top: 0.3rem;
        }

        /* ---------- 文化資産バッジ ---------- */
        .asset-badge {
            display: inline-block;
            background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
            border: 1px solid #80deea;
            border-radius: 24px;
            padding: 0.5rem 1.2rem;
            margin: 0.3rem;
            font-size: 0.9rem;
            font-weight: 600;
            color: #0a2540;
        }

        /* ---------- セクション区切り ---------- */
        .section-divider {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, #80deea 50%, transparent 100%);
            margin: 2rem 0;
        }
        .section-divider-wave {
            position: relative;
            width: 100%;
            height: 32px;
            margin: 1.5rem 0;
            overflow: hidden;
            opacity: 0.5;
        }
        .section-divider-wave svg {
            width: 200%;
            height: 100%;
            animation: wave-drift-slow 18s linear infinite;
        }

        /* ---------- チーム分析カード ---------- */
        .team-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            box-shadow: 0 1px 6px rgba(10,37,64,0.06);
            margin-bottom: 0.5rem;
            border-top: 3px solid #26c6da;
        }
        .team-card .team-name {
            font-weight: 700;
            color: #0d3b66;
            font-size: 0.9rem;
        }
        .team-card .team-keywords {
            font-size: 0.82rem;
            color: #607d8b;
            margin-top: 0.2rem;
        }

        /* ---------- Plotlyチャート余白調整 ---------- */
        .stPlotlyChart {
            margin-bottom: 1rem;
        }

        /* ---------- 引用ブロック ---------- */
        .quote-block {
            background: #f5fbfe;
            border-left: 4px solid #26c6da;
            border-radius: 0 10px 10px 0;
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
            font-style: italic;
            color: #37474f;
        }

        /* ---------- Expander カスタマイズ ---------- */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #0d3b66;
        }

        /* ---------- 波アニメーション ---------- */
        @keyframes wave-drift {
            0%   { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        @keyframes wave-drift-slow {
            0%   { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        /* ヒーロー波 */
        .hero-section {
            padding-bottom: 4rem !important;
        }
        .hero-waves {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 60px;
            overflow: hidden;
        }
        .hero-waves svg {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 200%;
            height: 100%;
        }
        .hero-waves .wave-1 {
            animation: wave-drift 7s linear infinite;
            opacity: 0.25;
        }
        .hero-waves .wave-2 {
            animation: wave-drift-slow 11s linear infinite;
            opacity: 0.15;
        }
        .hero-waves .wave-3 {
            animation: wave-drift 15s linear infinite reverse;
            opacity: 0.10;
        }

        /* セクション波区切り */
        .wave-divider {
            position: relative;
            width: 100%;
            height: 40px;
            margin: 1.5rem 0;
            overflow: hidden;
        }
        .wave-divider svg {
            width: 200%;
            height: 100%;
            animation: wave-drift-slow 14s linear infinite;
        }

        /* サイドバー波 */
        .sidebar-wave {
            position: relative;
            width: 100%;
            height: 50px;
            overflow: hidden;
            margin-top: 1rem;
        }
        .sidebar-wave svg {
            width: 200%;
            height: 100%;
            animation: wave-drift 10s linear infinite;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ヒーローセクション共通コンポーネント
# ============================================================
def render_hero(title: str, subtitle: str, description: str = "") -> None:
    """各ページ上部のヒーローセクションを描画する。"""
    desc_html = f"<p>{description}</p>" if description else ""
    st.markdown(
        f"""
        <div class="hero-section">
            <h1>{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
            {desc_html}
            <div class="hero-waves">
                <svg class="wave-1" viewBox="0 0 1200 60" preserveAspectRatio="none">
                    <path d="M0,30 C150,50 350,0 500,30 C650,60 850,10 1000,30 C1100,45 1150,20 1200,30 L1200,60 L0,60Z" fill="rgba(255,255,255,0.4)"/>
                </svg>
                <svg class="wave-2" viewBox="0 0 1200 60" preserveAspectRatio="none">
                    <path d="M0,35 C200,10 400,55 600,35 C800,15 1000,50 1200,35 L1200,60 L0,60Z" fill="rgba(255,255,255,0.3)"/>
                </svg>
                <svg class="wave-3" viewBox="0 0 1200 60" preserveAspectRatio="none">
                    <path d="M0,40 C100,20 300,55 500,35 C700,15 900,50 1100,30 C1150,25 1180,40 1200,38 L1200,60 L0,60Z" fill="rgba(255,255,255,0.2)"/>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# サイドバー装飾
# ============================================================
def render_sidebar_decoration() -> None:
    """サイドバーにヘッダーとフッターを追加する。"""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
                <div style="font-size:1.5rem; font-weight:900; letter-spacing:0.08em;
                            color:#ffffff;">セセラギズム</div>
                <div style="font-size:0.72rem; color:rgba(255,255,255,0.6);
                            margin-top:0.4rem;">
                    三島商工会議所 80周年ビジョン
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sidebar-wave">
                <svg viewBox="0 0 1200 50" preserveAspectRatio="none">
                    <path d="M0,25 C150,40 350,10 500,25 C650,40 850,10 1000,25 C1100,35 1150,15 1200,25 L1200,50 L0,50Z"
                          fill="rgba(255,255,255,0.08)"/>
                    <path d="M0,30 C200,15 400,42 600,28 C800,14 1000,40 1200,28 L1200,50 L0,50Z"
                          fill="rgba(255,255,255,0.05)"/>
                </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align:center; font-size:0.72rem;
                        color:rgba(255,255,255,0.65); padding-bottom:1rem;">
                湧き上がれ、鳴り響け<br/>
                三島商工会議所 創立80周年
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# Page 1: ビジョンの変遷
# ============================================================
def page_vision_evolution() -> None:
    """50周年から80周年までのビジョン変遷を表示する。"""

    render_hero(
        "ビジョンの変遷",
        "Vision Evolution: 50th - 80th Anniversary",
        "三島商工会議所が30年かけて紡いできた物語。再生から放出へ、内から外へ。",
    )

    # --- タイムラインデータ ---
    milestones = [
        {
            "year": "50周年",
            "theme": "街中がせせらぎ",
            "stage": "再生・復活",
            "desc": "市民活動での水の復活。<br/>水辺せせらぎの街としての刷新。",
            "active": False,
        },
        {
            "year": "60周年",
            "theme": "新 四ツ辻文化の街",
            "stage": "交差・集積",
            "desc": "三島の歴史を踏襲して道が交錯し、<br/>人モノが交錯する街。",
            "active": False,
        },
        {
            "year": "70周年",
            "theme": "つなぐ三島",
            "stage": "接続・継承",
            "desc": "過去の活動から未来へつなぎ、<br/>新しい未来へのメッセージ。",
            "active": False,
        },
        {
            "year": "80周年",
            "theme": "セセラギズム",
            "stage": "放出・発信",
            "desc": "溜めたエネルギーを解き放つ。<br/>内から外へ、響かせる。",
            "active": True,
        },
    ]

    # --- タイムラインカード ---
    timeline_html = '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:1rem; margin-bottom:1rem;">'
    for m in milestones:
        active_cls = " active" if m["active"] else ""
        year_cls = " current" if m["active"] else ""
        timeline_html += f"""
            <div class="timeline-card{active_cls}">
                <span class="timeline-year{year_cls}">{m['year']}</span>
                <div class="timeline-theme">{m['theme']}</div>
                <div class="timeline-stage">{m['stage']}</div>
                <div class="timeline-desc">{m['desc']}</div>
            </div>"""
    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

    # --- 進化のストーリー ---
    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 進化のストーリー")
    st.markdown("各周年ビジョンは、前のステージを土台に積み上げてきた。")

    story_steps = [
        {
            "period": "50周年",
            "name": "街中がせせらぎ",
            "stage": "再生・復活",
            "arrow": "水の復活",
            "detail": "三島の原点である湧水と水辺を、市民活動の力で蘇らせた。「せせらぎの街・三島」というアイデンティティが確立された時代。",
        },
        {
            "period": "60周年",
            "name": "新 四ツ辻文化の街",
            "stage": "交差・集積",
            "arrow": "人とモノの交差",
            "detail": "宿場町としての歴史を踏まえ、道が交わり人とモノが集まる結節点としての三島を再定義。内外の交流が活性化。",
        },
        {
            "period": "70周年",
            "name": "つなぐ三島",
            "stage": "接続・継承",
            "arrow": "過去と未来の接続",
            "detail": "これまでの活動を未来へつなぎ、次の世代に受け渡すメッセージを発信。継承と連帯のステージ。",
        },
        {
            "period": "80周年",
            "name": "セセラギズム",
            "stage": "放出・発信",
            "arrow": "エネルギーを外へ",
            "detail": "50周年の「せせらぎ」を継承しつつ、「イズム＝思想・運動」として外に発信するステージへ。つないで溜め込んできたエネルギー、人、想いを、外に向けて解き放つ。",
        },
    ]

    story_html = ""
    for i, step in enumerate(story_steps):
        is_current = step["period"] == "80周年"
        border_color = "#00897b" if is_current else "#1a6b8a"
        bg = "linear-gradient(135deg, #e0f7fa 0%, #ffffff 50%)" if is_current else "#ffffff"
        story_html += f"""
        <div style="display:flex; gap:1rem; align-items:flex-start;">
            <div style="flex-shrink:0; text-align:center; padding-top:0.6rem;">
                <div style="display:inline-block; background:linear-gradient(135deg, {border_color}, #48b4a0);
                            color:#fff; font-size:0.8rem; font-weight:700;
                            padding:0.3rem 0.8rem; border-radius:16px;">{step['period']}</div>
            </div>
            <div style="flex:1; background:{bg}; border-left:4px solid {border_color};
                        border-radius:0 12px 12px 0; padding:1.2rem 1.5rem; margin-bottom:0.3rem;
                        box-shadow:0 1px 6px rgba(10,37,64,0.06);">
                <div style="font-size:1.2rem; font-weight:900; color:#0a2540;">
                    {step['name']} <span style="font-size:0.85rem; font-weight:600; color:{border_color};">― {step['stage']}</span>
                </div>
                <div style="font-size:0.85rem; color:#546e7a; margin-top:0.4rem; line-height:1.7;">
                    {step['detail']}
                </div>
            </div>
        </div>"""
        if i < len(story_steps) - 1:
            story_html += f"""
            <div style="text-align:center; color:#1a6b8a; font-size:0.8rem; margin:0.1rem 0 0.1rem 0;">
                ▼ {story_steps[i+1]['arrow']}
            </div>"""
    st.markdown(story_html, unsafe_allow_html=True)

    # --- 80周年のポジショニング ---
    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="narrative-box">
            <p>
                50周年で「<strong>街中がせせらぎ</strong>」として水を復活させた三島。<br/>
                80周年では、その「せせらぎ」に「<strong>イズム（ism）</strong>」を加え、<br/>
                思想・運動として外の世界に発信するステージへ進化する。
            </p>
            <span class="narrative-emphasis">
                つないだ次に来るもの ＝ 蓄積 → 放出、内 → 外、響かせる
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Page 2: セセラギズム
# ============================================================
def page_seseragism() -> None:
    """セセラギズムのコンセプト詳細を表示する。"""

    render_hero(
        "セセラギズム",
        "SESERAGISM: せせらぎ + ism（主義・思想・運動）",
        "三島の行動原理を、水の流れに見立てて言語化した新概念。",
    )

    # --- コンセプト構造 ---
    st.markdown("### コンセプトの構造")
    st.markdown(
        """
        <div style="display:flex; align-items:center; justify-content:center; gap:0.5rem; flex-wrap:wrap; margin-bottom:1rem;">
            <div class="philosophy-card" style="flex:1; min-width:160px; max-width:260px;">
                <div class="philosophy-title">せせらぎ</div>
                <div class="philosophy-desc">三島のアイデンティティ<br/>湧水・水辺・清流</div>
            </div>
            <div style="font-size:2rem; color:#1a6b8a; font-weight:700;">+</div>
            <div class="philosophy-card" style="flex:1; min-width:160px; max-width:260px;">
                <div class="philosophy-title">ism</div>
                <div class="philosophy-desc">主義・思想・運動<br/>行動原理としての体系</div>
            </div>
            <div style="font-size:2rem; color:#1a6b8a; font-weight:700;">=</div>
            <div class="philosophy-card" style="flex:1; min-width:160px; max-width:260px; border:2px solid #00897b; background:linear-gradient(135deg,#e0f7fa,#b2ebf2,#80deea);">
                <div class="philosophy-title">セセラギズム</div>
                <div class="philosophy-desc">三島の行動原理<br/>水のように流れ、響かせる</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- セントラルフィロソフィー候補 ---
    st.markdown("### セントラルフィロソフィー候補")

    philosophies = [
        ("候補 1", "水のように、自分から動く。"),
        ("候補 2", "小さく湧いて、大きく響く。"),
        ("候補 3", "この街は、流れ続ける。"),
        ("候補 4", "湧き出す力を、解き放て。"),
        ("候補 5", "一滴が、うねりになる。"),
    ]

    phil_html = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for num, text in philosophies:
        phil_html += f"""
            <div class="philosophy-card">
                <div style="font-size:0.75rem; color:#78909c; margin-bottom:0.3rem;">{num}</div>
                <div class="philosophy-title" style="font-size:1rem;">{text}</div>
            </div>"""
    phil_html += "</div>"
    st.markdown(phil_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- サブコピー候補 ---
    st.markdown("### サブコピー候補")

    sub_copies = [
        "セセラギズム 〜 湧き上がれ、鳴り響け 〜",
        "セセラギズム 〜 水脈が刻む、新しいビート 〜",
        "セセラギズム -PULSE-",
    ]

    subcopy_html = ""
    for sc in sub_copies:
        subcopy_html += f'<div class="subcopy-card"><p>{sc}</p></div>'
    st.markdown(subcopy_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 派生・代替案 ---
    with st.expander("派生・代替案を見る", expanded=False):
        alternatives = [
            ("ミシマリズム", "MISHIMAISM", "三島 + ism。地名を直接冠したバリエーション。"),
            ("MAKE WAVES MISHIMA", "メイクウェーブズ", "「波を起こせ」。英語圏にも響くグローバル案。"),
            ("MISHIMA SPRINGS", "ミシマスプリングス", "湧水（springs）と春（spring）の二重意味。"),
            ("ひらく三島", "ヒラクミシマ", "開く・拓く・啓く。シンプルで力強い日本語案。"),
        ]
        alt_html = '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:1rem;">'
        for name, sub, desc in alternatives:
            alt_html += f"""
                <div class="concept-card" style="text-align:center; border-left:4px solid #80deea;">
                    <div class="concept-title" style="font-size:1.1rem;">{name}</div>
                    <div style="font-size:0.75rem; color:#90a4ae; margin-bottom:0.4rem;">{sub}</div>
                    <div class="concept-text">{desc}</div>
                </div>"""
        alt_html += "</div>"
        st.markdown(alt_html, unsafe_allow_html=True)


# ============================================================
# Page 3: ワークショップ分析
# ============================================================
def page_workshop_analysis() -> None:
    """ワークショップ分析結果を表示する。"""

    render_hero(
        "ワークショップ分析",
        "Workshop Analysis",
        "8チームのワークショップから浮かび上がった三島の本質。",
    )

    # --- 概要メトリクス ---
    st.markdown(
        """
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1rem; margin-bottom:1.5rem;">
            <div class="stat-highlight">
                <div class="stat-number">8</div>
                <div class="stat-label">参加チーム数</div>
            </div>
            <div class="stat-highlight">
                <div class="stat-number">160+</div>
                <div class="stat-label">抽出キーワード数</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 象徴フレーズ ---
    st.markdown(
        """
        <div class="quote-block" style="font-size:1.15rem; text-align:center;">
            第7班が生み出した象徴フレーズ：<br/>
            <strong style="font-size:1.4rem; color:#0d3b66;">
            「ウェルカム・オープンな街、私たちの三島」
            </strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- キーワード頻度（棒グラフ） ---
    st.markdown("### キーワード頻度分析")
    st.markdown("全チームの議論から抽出されたキーワードの出現頻度。")

    keyword_data = pd.DataFrame(
        {
            "キーワード": [
                "オープン", "ウェルカム", "受け入れる", "つながり", "水",
                "歴史", "人の温かさ", "食", "自然", "チャレンジ",
            ],
            "出現回数": [28, 24, 22, 18, 16, 14, 12, 10, 9, 7],
        }
    )

    # 色のグラデーション
    colors = [
        "#0d3b66", "#115e82", "#1a6b8a", "#238d96", "#2baa9e",
        "#48b4a0", "#66c2a5", "#80deea", "#a0e4d0", "#b2ebf2",
    ]

    fig_keywords = go.Figure(
        go.Bar(
            x=keyword_data["出現回数"],
            y=keyword_data["キーワード"],
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(width=0),
                cornerradius=6,
            ),
            text=keyword_data["出現回数"],
            textposition="outside",
            textfont=dict(size=13, color="#0a2540", family="Noto Sans JP"),
            hovertemplate="<b>%{y}</b><br>出現回数: %{x}回<extra></extra>",
        )
    )
    fig_keywords.update_layout(
        title=dict(text="ワークショップ キーワード頻度", font=dict(size=16, color="#0a2540")),
        xaxis=dict(title="出現回数", showgrid=True, gridcolor="#e0f2f1", range=[0, 34]),
        yaxis=dict(autorange="reversed", tickfont=dict(size=13)),
        height=450,
        margin=dict(l=120, r=40, t=60, b=40),
        plot_bgcolor="#fafffe",
        paper_bgcolor="#ffffff",
        font=dict(family="Noto Sans JP"),
    )
    st.plotly_chart(fig_keywords, width="stretch")

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 変えたくない三島の良さ（レーダーチャート） ---
    st.markdown("### 変えたくない三島の良さ")
    st.markdown("ワークショップで「守りたい」と挙がった6つの価値カテゴリ。")

    categories = ["水", "人", "歴史", "規模感", "食", "立地"]
    values = [95, 88, 82, 75, 70, 78]
    # レーダーは閉じるために先頭を末尾に追加
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            fillcolor="rgba(26,107,138,0.18)",
            line=dict(color="#1a6b8a", width=2.5),
            marker=dict(size=8, color="#0d3b66"),
            name="重要度スコア",
            hovertemplate="<b>%{theta}</b><br>重要度: %{r}<extra></extra>",
        )
    )
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=True, tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=14, color="#0a2540")),
            bgcolor="#fafffe",
        ),
        height=420,
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor="#ffffff",
        font=dict(family="Noto Sans JP"),
        showlegend=False,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # カテゴリ詳細
    st.markdown("#### カテゴリ詳細")
    cat_details = [
        ("💧 水", "湧水・源兵衛川・柿田川。三島の原点。"),
        ("👥 人", "温かさ・オープンさ。よそ者を受け入れるDNA。"),
        ("🏯 歴史", "三嶋大社・宿場町。千年を超える積層。"),
        ("📐 規模感", "大きすぎず小さすぎない。ちょうどいいサイズ。"),
        ("🍽 食", "うなぎ・みしまコロッケ。食文化の豊かさ。"),
        ("📍 立地", "東京から1時間。富士山・伊豆・箱根への玄関口。"),
    ]
    cat_html = '<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:0.8rem;">'
    for label, detail in cat_details:
        cat_html += f"""
            <div style="margin-bottom:0.4rem;">
                <strong style="color:#0d3b66;">{label}</strong><br/>
                <span style="font-size:0.82rem; color:#607d8b;">{detail}</span>
            </div>"""
    cat_html += "</div>"
    st.markdown(cat_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 8チーム共通キーワード分析 ---
    st.markdown("### 8チーム共通キーワード分析")
    st.markdown("各チームから抽出されたキーワードを分類。共通項が浮かび上がる。")

    teams = [
        ("第1班", "水・オープン・歴史・つながり"),
        ("第2班", "ウェルカム・チャレンジ・食・自然"),
        ("第3班", "受け入れる・水・人の温かさ・規模感"),
        ("第4班", "オープン・つながり・歴史・立地"),
        ("第5班", "ウェルカム・水・自然・人の温かさ"),
        ("第6班", "オープン・受け入れる・食・チャレンジ"),
        ("第7班", "ウェルカム・オープン・つながり・水"),
        ("第8班", "受け入れる・歴史・人の温かさ・つながり"),
    ]

    teams_html = '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for name, kw in teams:
        teams_html += f"""
            <div class="team-card">
                <div class="team-name">{name}</div>
                <div class="team-keywords">{kw}</div>
            </div>"""
    teams_html += "</div>"
    st.markdown(teams_html, unsafe_allow_html=True)

    # --- 共通キーワードまとめ ---
    st.markdown("")
    st.markdown(
        """
        <div class="narrative-box">
            <p>
                8チームすべてに共通するのは <strong>「オープン」「ウェルカム」「受け入れる」</strong> というキーワード。<br/>
                三島の本質は「開かれた水の街」であり、それは宿場町としてよそ者を迎え入れてきた
                歴史的DNAに根差している。<br/>
                この行動原理を <strong>セセラギズム</strong> として言語化し、次の10年の指針とする。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Page 4: アンケート分析
# ============================================================
def page_survey_analysis() -> None:
    """地域振興ビジョン策定アンケートの分析結果を表示する。"""

    render_hero(
        "アンケート分析",
        "Survey Analysis",
        "まちづくり関係者・市民77名を対象としたオンラインアンケートの分析レポート。",
    )

    # --- 調査概要 ---
    st.markdown("### 調査概要")
    st.markdown(
        """
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:1rem; margin-bottom:1.5rem;">
            <div class="stat-highlight">
                <div class="stat-number">77名</div>
                <div class="stat-label">回答者数</div>
            </div>
            <div class="stat-highlight">
                <div class="stat-number">6.4</div>
                <div class="stat-label">平均スコア（10点満点）</div>
            </div>
            <div class="stat-highlight">
                <div class="stat-number">46名</div>
                <div class="stat-label">三島市在住者</div>
            </div>
            <div class="stat-highlight">
                <div class="stat-number">38年</div>
                <div class="stat-label">平均三島市在住年数</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="background:#f5fbfe; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1.5rem;
                    font-size:0.85rem; color:#546e7a; border-left:4px solid #80deea;">
            <strong>実施期間：</strong>2025年10月6日（月）〜24日（金）<br/>
            <strong>対象：</strong>【当所】まちづくり委員、部会幹事、女性会、青年部<br/>
            　　　　【関係団体】三島商店街連盟、三島市観光協会会員、JC など
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問1: スコア分布 ---
    st.markdown("### 設問1：地域活性化の現状評価")
    st.markdown("「地域活性化について、現在の三島は何点だと思いますか？」（10点満点）")

    score_labels = ["2点", "3点", "4点", "5点", "6点", "7点", "8点", "9点"]
    score_counts = [1, 5, 2, 13, 11, 23, 20, 2]
    score_colors = [
        "#e57373", "#ef9a9a", "#ffcc80", "#fff59d",
        "#c5e1a5", "#81c784", "#4caf50", "#2e7d32",
    ]

    fig_scores = go.Figure(
        go.Bar(
            x=score_labels, y=score_counts,
            marker=dict(color=score_colors, cornerradius=6),
            text=score_counts, textposition="outside",
            textfont=dict(size=13, color="#0a2540", family="Noto Sans JP"),
            hovertemplate="<b>%{x}</b><br>回答数: %{y}名<extra></extra>",
        )
    )
    fig_scores.update_layout(
        xaxis=dict(title="評価（点）"),
        yaxis=dict(title="回答数（名）", gridcolor="#e0f2f1"),
        height=350,
        margin=dict(l=50, r=30, t=20, b=50),
        plot_bgcolor="#fafffe",
        paper_bgcolor="#ffffff",
        font=dict(family="Noto Sans JP"),
    )
    st.plotly_chart(fig_scores, use_container_width=True)

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">スコア分析</div>
            <div class="metric-value" style="font-size:1.3rem;">最頻値 7点 ・ 平均 6.4点</div>
            <div class="metric-desc">
                回答者の約58%が7点以上と評価。「イベントや活動が活発」「プレイヤーが増えている」と
                現状を肯定的に捉える声が多い一方、「一部エリアに限られている」「空き店舗が目立つ」
                など改善余地を指摘する声も。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問1・2: 評価の内訳 ---
    st.markdown("### 設問1・2：評価の内訳")
    st.markdown(
        """
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1.5rem; margin-bottom:1rem;">
            <div>
                <div style="font-size:0.95rem; font-weight:700; color:#0d3b66; margin-bottom:0.6rem;
                            border-bottom:2px solid #26c6da; padding-bottom:0.3rem;">
                    ✅ 高評価のポイント</div>
                <div class="concept-card"><div class="concept-title">水と自然の豊かさ</div>
                    <div class="concept-text">富士山の湧水やせせらぎをはじめとする自然環境が三島らしさの象徴</div></div>
                <div class="concept-card"><div class="concept-title">アクセスの良さ</div>
                    <div class="concept-text">新幹線や高速道路により首都圏・伊豆方面との行き来が容易</div></div>
                <div class="concept-card"><div class="concept-title">歴史と文化の調和</div>
                    <div class="concept-text">三嶋大社や伝統行事など、歴史的文化が現代にも息づく</div></div>
                <div class="concept-card"><div class="concept-title">住みやすさと安心感</div>
                    <div class="concept-text">ほどよい規模感、落ち着いた生活環境が移住者や子育て世代にも支持</div></div>
                <div class="concept-card"><div class="concept-title">イベント・観光振興への期待</div>
                    <div class="concept-text">地域資源を生かした観光まちづくりへの関心が高い</div></div>
            </div>
            <div>
                <div style="font-size:0.95rem; font-weight:700; color:#c62828; margin-bottom:0.6rem;
                            border-bottom:2px solid #e57373; padding-bottom:0.3rem;">
                    ⚠ 課題意識</div>
                <div class="concept-card" style="border-left-color:#e57373;"><div class="concept-title">まちなかのにぎわい減少</div>
                    <div class="concept-text">中心市街地の空洞化が進み、商業や人の流れの低下が課題</div></div>
                <div class="concept-card" style="border-left-color:#e57373;"><div class="concept-title">若者・子育て世代の流出</div>
                    <div class="concept-text">若年層の定住促進が重要課題。魅力ある雇用と教育環境が必要</div></div>
                <div class="concept-card" style="border-left-color:#e57373;"><div class="concept-title">地域コミュニティの希薄化</div>
                    <div class="concept-text">昔ながらの繋がりが弱まり、顔の見える関係づくりへの期待</div></div>
                <div class="concept-card" style="border-left-color:#e57373;"><div class="concept-title">交通・まちの利便性</div>
                    <div class="concept-text">電車・バスの運行頻度や駅周辺整備を求める声</div></div>
                <div class="concept-card" style="border-left-color:#e57373;"><div class="concept-title">行政・商工会議所への期待</div>
                    <div class="concept-text">ビジョンを示し行動するリーダー役への期待が大きい</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問4: 変えたくない三島の良さ ---
    st.markdown("### 設問4：変えたくない三島の良さ")

    q4_items = [
        ("\U0001f4a7", "水と緑の恵み", "湧水やせせらぎ、緑豊かな環境を「何よりも守りたい」とする意見が圧倒的"),
        ("\U0001f3ef", "歴史と文化の継承", "三嶋大社を中心とした伝統行事が地域アイデンティティとして根付く"),
        ("\U0001f91d", "人の温かさ", "「人が優しい」「助け合いの心」\u2014 三島らしさは人柄にある"),
        ("\U0001f4d0", "まちのコンパクトさ", "「ほどよい大きさ」「移動が便利」\u2014 生活圏の快適さ"),
        ("\U0001f35d", "食文化と地元産品", "地場産の食材・飲食文化がまちのブランド力を支えている"),
        ("\U0001f3d4", "まちなみと景観", "富士山を望む風景や水辺の景観。自然と調和したまちなみ"),
        ("\U0001f3b6", "地域の祭りと行事", "夏祭りや大社の行事が「変えてはいけない三島の文化」"),
        ("\U0001f3e1", "安心できる暮らし", "治安の良さや穏やかな生活リズムが市民の誇り"),
        ("\U0001f476", "子育てのしやすさ", "自然環境と教育環境のバランスをファミリー層が評価"),
        ("\u2764\ufe0f", "地元への愛着", "「三島が好き」「ずっと住みたい」\u2014 住民の地元愛が最大の財産"),
    ]
    q4_html = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for icon, title, desc in q4_items:
        q4_html += (
            f'<div class="concept-card" style="text-align:center; border-left:none;'
            f' border-top:3px solid #26c6da; min-height:150px;">'
            f'<div style="font-size:1.4rem; margin-bottom:0.3rem;">{icon}</div>'
            f'<div class="concept-title" style="font-size:0.88rem;">{title}</div>'
            f'<div class="concept-text" style="font-size:0.75rem;">{desc}</div></div>'
        )
    q4_html += "</div>"
    st.markdown(q4_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="quote-block" style="text-align:center;">
            <strong>「水と緑」が圧倒的1位</strong>。続いて歴史・文化、人の温かさ、コンパクトさ。<br/>
            三島のアイデンティティは <strong>「水」×「人」×「歴史」</strong> の三層構造。
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問3: 20年後の理想 ---
    st.markdown("### 設問3：20年後の理想の三島")

    q3_items = [
        ("\U0001f46a", "多世代共生のまち", "高齢者から子どもまでが支え合うコミュニティ"),
        ("\U0001f6b6", "歩いて楽しいまち", "せせらぎや緑に囲まれた歩行者中心のスローシティ"),
        ("\U0001f355", "グルメ観光都市", "サンセバスチャンのような食と自然の国際都市"),
        ("\U0001f504", "共感経済のまち", "共感や協働で地域が循環する新しい経済モデル"),
        ("\U0001f393", "若者が集うまち", "教育・文化・雇用の整備で若者の姿が街に"),
        ("\u2615", "サードプレイスの充実", "職場でも家庭でもない「居場所」がまちの魅力に"),
        ("\U0001f33f", "自然と調和した都市", "水・緑を軸にした持続可能なまちづくり"),
        ("\U0001f30d", "小規模でも世界に誇るまち", "規模の小ささを強みに質の高い文化・観光を"),
        ("\U0001f4c9", "人口減少対応型社会", "住民一人ひとりが豊かに暮らせる社会モデル"),
        ("\U0001f60a", "顔の見える関係づくり", "「みんな顔馴染み」\u2014 温かな関係性の重視"),
    ]
    q3_html = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for icon, title, desc in q3_items:
        q3_html += (
            f'<div class="philosophy-card" style="min-height:auto; padding:1rem;">'
            f'<div style="font-size:1.3rem;">{icon}</div>'
            f'<div class="philosophy-title" style="font-size:0.85rem; margin-top:0.3rem;">{title}</div>'
            f'<div class="philosophy-desc" style="font-size:0.73rem;">{desc}</div></div>'
        )
    q3_html += "</div>"
    st.markdown(q3_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問5: もっと良くなるには ---
    st.markdown("### 設問5：三島がもっと良くなるには")

    q5_items = [
        ("\U0001f4bc", "若者の定着支援", "就職・起業・住宅など地元で暮らし続けられる環境整備"),
        ("\U0001f3ea", "商店街の再生", "空き店舗の活用、歩行者空間の整備でにぎわい回復"),
        ("\U0001f68c", "交通と移動の改善", "バス増便、駐輪場、歩道整備。誰もが動きやすいまちに"),
        ("\U0001f5fa", "観光資源の活用", "自然・歴史・食文化を磨き上げて観光産業を強化"),
        ("\u26a1", "行政のスピード感", "官民連携を進め協働型行政への転換"),
        ("\U0001f64b", "市民参加の促進", "参加できる場を増やし住民主体の活動を広げる"),
        ("\U0001f4da", "子育て・教育の充実", "学びや遊びの場を増やし子どもが育つまちへ"),
        ("\U0001f4bb", "デジタル活用の推進", "DXによる行政効率化や地域情報の共有"),
        ("\U0001f3e2", "企業・働く場の魅力化", "地元企業の魅力発信や多様な働き方の推進"),
        ("\U0001f3f7\ufe0f", "三島ブランドの確立", "「三島らしさ」を観光・産業・文化の軸として明確に"),
    ]
    q5_html = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for icon, title, desc in q5_items:
        q5_html += (
            f'<div class="concept-card" style="text-align:center; border-left:none;'
            f' border-top:3px solid #e57373; min-height:140px;">'
            f'<div style="font-size:1.3rem; margin-bottom:0.2rem;">{icon}</div>'
            f'<div class="concept-title" style="font-size:0.88rem;">{title}</div>'
            f'<div class="concept-text" style="font-size:0.75rem;">{desc}</div></div>'
        )
    q5_html += "</div>"
    st.markdown(q5_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問6: 商工会議所への期待 ---
    st.markdown("### 設問6：三島商工会議所に期待すること")

    q6_items = [
        ("\U0001f451", "地域のリーダー役", "まちの未来を導くリーダーシップを発揮"),
        ("\U0001f91d", "若者と企業の橋渡し", "若者が地元で働く・起業するための接点づくり"),
        ("\U0001f3e2", "中小企業の支援強化", "経営相談、販路開拓、人材育成を地道に"),
        ("\U0001f310", "地域間連携の促進", "伊豆・沼津・裾野と連携し広域経済圏を形成"),
        ("\U0001f4e3", "情報発信力の向上", "SNS・ウェブで「見える活動」への転換"),
        ("\U0001f5fa", "観光産業の支援", "観光資源と企業をつなぐ仕組みづくり"),
        ("\U0001f469\u200d\U0001f4bc", "女性活躍の推進", "女性経営者のネットワークと多様な視点の活用"),
        ("\U0001f331", "環境・SDGs推進", "環境配慮の経営支援や脱炭素の取組み"),
        ("\U0001f3aa", "地域イベントの後押し", "市民や商店街のイベントへのサポート強化"),
        ("\U0001f932", "共創のプラットフォーム", "市民・企業・行政が対等に議論できる場の提供"),
    ]
    q6_html = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for icon, title, desc in q6_items:
        q6_html += (
            f'<div class="concept-card" style="text-align:center; border-left:none;'
            f' border-top:3px solid #48b4a0; min-height:140px;">'
            f'<div style="font-size:1.3rem; margin-bottom:0.2rem;">{icon}</div>'
            f'<div class="concept-title" style="font-size:0.88rem;">{title}</div>'
            f'<div class="concept-text" style="font-size:0.75rem;">{desc}</div></div>'
        )
    q6_html += "</div>"
    st.markdown(q6_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 設問7: 自由意見 ---
    with st.expander("設問7：自由意見", expanded=False):
        q7_items = [
            ("市民の声を反映して", "アンケートを一過性で終わらせず政策に反映を"),
            ("行政と商工会の連携強化", "縦割りをなくし地域全体で協働を"),
            ("観光・文化イベントの推進", "音楽、食、アートで交流人口の増加を"),
            ("空き店舗の利活用", "商店街や駅前の空きスペースを活動拠点に"),
            ("環境を守る意識", "開発よりも自然保全を優先する三島らしさ"),
            ("教育・学びの充実", "「地域で育てる教育」を求める声"),
            ("地域のつながり再生", "町内会や市民団体の「顔の見える関係づくり」"),
            ("移住・定住促進", "三島に住みたい人が増える仕組みづくり"),
            ("安心・安全な暮らし", "防災・防犯・医療の基盤整備"),
            ("持続可能なまち経営", "変化を恐れずリーダーシップと協働体制を"),
        ]
        q7_html = '<div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.6rem;">'
        for title, desc in q7_items:
            q7_html += (
                f'<div style="background:#f5fbfe; border-radius:8px; padding:0.8rem 1rem;'
                f' border-left:3px solid #80deea;">'
                f'<strong style="color:#0d3b66; font-size:0.88rem;">{title}</strong><br/>'
                f'<span style="font-size:0.78rem; color:#607d8b;">{desc}</span></div>'
            )
        q7_html += "</div>"
        st.markdown(q7_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- ナラティブまとめ ---
    st.markdown(
        """
        <div class="narrative-box">
            <p>
                77名のまちづくり関係者・市民の声から、三島の本質が鮮明に浮かび上がった。<br/><br/>
                <strong>「変えたくない良さ」の第1位は圧倒的に「水と緑」</strong>。
                続いて歴史・文化、人の温かさ、コンパクトさと続く。
                三島のアイデンティティは <strong>水 × 人 × 歴史</strong> の三層構造にある。<br/><br/>
                一方で「もっと良くなるには」では、<strong>若者の定着支援、商店街の再生、
                三島ブランドの確立</strong>を求める声が目立つ。
                三島の良さは十分に認識されているが、それを
                <strong>外に向けて発信し、内に還流させる仕組み</strong>が足りない。<br/><br/>
                この「内なる価値を外へ放出する」という方向性は、
                まさに <strong>セセラギズム</strong> が提唱する
                <strong>「蓄積 → 放出、内 → 外、響かせる」</strong> と一致している。
            </p>
            <span class="narrative-emphasis">
                水のアイデンティティ × 外への発信 ＝ セセラギズムの裏付け
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Page 5: 三島市統計データ
# ============================================================
def page_statistics() -> None:
    """三島市の統計データを表示する。"""

    render_hero(
        "三島市統計データ",
        "Mishima City Statistics",
        "人口・観光・産業から見る三島の現在地。データが示す課題と可能性。",
    )

    # --- 人口推移 ---
    st.markdown("### 人口推移と将来推計")
    st.markdown("住民基本台帳ベース（日本人住民）。2026年以降は近年の減少率をもとにした推計。")

    # 実績データ（2000-2025）出典: jp.gdfreak.com / 住民基本台帳
    actual_years = list(range(2000, 2026))
    actual_pop = [
        110_300, 110_700, 110_500, 111_000, 111_300,  # 2000-2004
        111_600, 112_100, 112_200, 111_900, 111_300,  # 2005-2009
        110_800, 110_600, 110_400, 110_200, 109_900,  # 2010-2014
        109_500, 109_000, 108_400, 108_000, 107_400,  # 2015-2019
        106_800, 106_200, 105_500, 104_800, 104_100, 103_359,  # 2020-2025
    ]

    # 将来推計（2026-2035）近年の減少率 約-1.0〜-1.3% をベースに推計
    projected_years = list(range(2026, 2036))
    projected_pop = []
    last = 103_359
    for rate in [-1.2, -1.2, -1.1, -1.1, -1.0, -1.0, -0.9, -0.9, -0.8, -0.8]:
        last = round(last * (1 + rate / 100))
        projected_pop.append(last)

    fig_pop = go.Figure()

    # 実績（実線）
    fig_pop.add_trace(
        go.Scatter(
            x=actual_years, y=actual_pop,
            name="実績",
            mode="lines+markers",
            line=dict(color="#1a6b8a", width=2.5),
            marker=dict(size=4, color="#0d3b66"),
            hovertemplate="<b>%{x}年</b><br>人口: %{y:,.0f}人（実績）<extra></extra>",
        )
    )
    # 推計（破線）— 実績の最終年を起点にして接続
    fig_pop.add_trace(
        go.Scatter(
            x=[actual_years[-1]] + projected_years,
            y=[actual_pop[-1]] + projected_pop,
            name="推計",
            mode="lines+markers",
            line=dict(color="#e57373", width=2.5, dash="dash"),
            marker=dict(size=4, color="#e57373", symbol="diamond"),
            hovertemplate="<b>%{x}年</b><br>人口: %{y:,.0f}人（推計）<extra></extra>",
        )
    )

    # 80周年（2025）ライン
    fig_pop.add_vline(
        x=2025, line=dict(color="#26c6da", width=1.5, dash="dot"),
        annotation_text="80周年", annotation_position="top",
        annotation_font=dict(size=11, color="#0d3b66"),
    )

    fig_pop.update_layout(
        xaxis=dict(title="年", showgrid=False, dtick=5),
        yaxis=dict(title="人口（人）", tickformat=",", gridcolor="#e0f2f1",
                   range=[90_000, 115_000]),
        height=420,
        margin=dict(l=60, r=30, t=30, b=50),
        plot_bgcolor="#fafffe",
        paper_bgcolor="#ffffff",
        font=dict(family="Noto Sans JP"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig_pop, use_container_width=True)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">人口動態サマリ</div>
            <div class="metric-value" style="font-size:1.3rem;">
                2025年 103,359人 → 2035年 約{projected_pop[-1]:,}人（推計）
            </div>
            <div class="metric-desc">
                ピーク（2007年 約112,200人）から2025年で約8,800人減（-7.9%）。
                近年は年-1.0〜-1.3%で加速。推計では2035年に10万人を割り込む可能性がある。
                移住促進・関係人口の拡大が今後のカギとなる。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 観光客数推移 ---
    st.markdown("### 観光客数推移（2015年 - 2024年）")

    years_tourism = list(range(2015, 2025))
    tourists = [5200, 5350, 5500, 5600, 5400, 2800, 3500, 4800, 5300, 5700]

    df_tourism = pd.DataFrame(
        {"年": years_tourism, "観光客数（千人）": tourists}
    )

    fig_tourism = go.Figure()
    fig_tourism.add_trace(
        go.Bar(
            x=df_tourism["年"],
            y=df_tourism["観光客数（千人）"],
            marker=dict(
                color=[
                    "#1a6b8a" if t > 3000 else "#e57373" for t in tourists
                ],
                cornerradius=4,
            ),
            text=[f"{t/1000:.1f}M" for t in tourists],
            textposition="outside",
            textfont=dict(size=11),
            hovertemplate="<b>%{x}年</b><br>観光客数: %{y:,.0f}千人<extra></extra>",
        )
    )
    # COVID注釈
    fig_tourism.add_annotation(
        x=2020,
        y=2800,
        text="COVID-19<br>影響",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#e57373",
        font=dict(size=11, color="#e57373"),
        ax=0,
        ay=-50,
    )
    fig_tourism.update_layout(
        xaxis=dict(title="年", dtick=1, showgrid=False),
        yaxis=dict(title="観光客数（千人）", gridcolor="#e0f2f1"),
        height=380,
        margin=dict(l=60, r=30, t=30, b=50),
        plot_bgcolor="#fafffe",
        paper_bgcolor="#ffffff",
        font=dict(family="Noto Sans JP"),
    )
    st.plotly_chart(fig_tourism, width="stretch")

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 事業所数推移 ---
    st.markdown("### 事業所数推移")

    years_biz = [2006, 2009, 2012, 2014, 2016, 2019, 2021, 2024]
    businesses = [5500, 5350, 5200, 5100, 5000, 4950, 4850, 4800]

    df_biz = pd.DataFrame({"年": years_biz, "事業所数": businesses})

    fig_biz = go.Figure()
    fig_biz.add_trace(
        go.Scatter(
            x=df_biz["年"],
            y=df_biz["事業所数"],
            mode="lines+markers",
            line=dict(color="#e57373", width=2.5, dash="dot"),
            marker=dict(size=8, color="#c62828", symbol="diamond"),
            fill="tozeroy",
            fillcolor="rgba(229,115,115,0.08)",
            hovertemplate="<b>%{x}年</b><br>事業所数: %{y:,.0f}<extra></extra>",
        )
    )
    fig_biz.update_layout(
        title=dict(text="事業所数の推移", font=dict(size=14, color="#0a2540")),
        xaxis=dict(title="年", showgrid=False),
        yaxis=dict(title="事業所数", range=[4500, 5700], gridcolor="#e0f2f1"),
        height=350,
        margin=dict(l=60, r=30, t=50, b=50),
        plot_bgcolor="#fafffe",
        paper_bgcolor="#ffffff",
        font=dict(family="Noto Sans JP"),
    )
    st.plotly_chart(fig_biz, use_container_width=True)

    st.markdown(
        """
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:1rem;">
            <div class="metric-card">
                <div class="metric-label">事業所数の動向</div>
                <div class="metric-value" style="color:#c62828; font-size:1.3rem;">約700減</div>
                <div class="metric-desc">
                    2006年の約5,500事業所から2024年には約4,800事業所に。
                    約12.7%の減少。商店街の空洞化は全国的課題。
                    一方で、新規創業・スタートアップの誘致、
                    リノベーションまちづくりなど、新たな動きも芽生えている。
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">セセラギズムが目指す効果</div>
                <div class="metric-value" style="color:#00897b; font-size:1.1rem;">外へ発信 → 内への還流</div>
                <div class="metric-desc">
                    三島の魅力を外へ発信することで、
                    関係人口・交流人口の拡大、
                    新規事業・移住者の獲得を促進する。
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 文化資産 ---
    st.markdown("### 三島の主要文化資産 ── 湧水の街のアイデンティティ")

    assets = [
        ("⛩", "三嶋大社", "伊豆国一宮。源頼朝が源氏再興を祈願した歴史ある神社。年間約150万人が参拝。"),
        ("🏞", "源兵衛川", "市民の手で復活した清流。せせらぎの原点。世界水遺産に登録。"),
        ("🌳", "白滝公園", "富士山の伏流水が湧き出す都市公園。夏でも冷たい湧水が市民の憩いの場。"),
        ("🎶", "しゃぎり（祭囃子）", "三嶋大社の例大祭で奏でられる伝統芸能。街に響く三島のリズム。"),
        ("💧", "柿田川湧水群", "東洋一の湧水量を誇る清流。国指定天然記念物。日量約100万トン。"),
    ]

    assets_html = '<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.8rem; margin-bottom:1rem;">'
    for icon, name, desc in assets:
        assets_html += f"""
            <div class="concept-card" style="text-align:center; min-height:200px; border-left:4px solid #48b4a0;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <div class="concept-title">{name}</div>
                <div class="concept-text">{desc}</div>
            </div>"""
    assets_html += "</div>"
    st.markdown(assets_html, unsafe_allow_html=True)

    # --- アイデンティティまとめ ---
    st.markdown(
        """
        <div class="narrative-box">
            <p>
                三島は <strong>「湧水の街」</strong> としてのアイデンティティを軸に、
                歴史・文化・自然・食・人のつながりが豊かに重なり合う街である。<br/><br/>
                人口減少や事業所数減少という課題に直面しながらも、
                コロナ禍からの観光回復が示すように、この街が持つ引力は衰えていない。<br/><br/>
                <strong>セセラギズム</strong>は、この蓄積されたエネルギーを
                内から外へ解き放ち、新しい人・コト・ビジネスを呼び込む
                次の10年の推進力となる。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Page 6: 行動原則
# ============================================================
def page_action_principles() -> None:
    """セセラギズムの7つの行動原則を表示する。"""

    render_hero(
        "7つの行動原則",
        "Action Principles of SESERAGISM",
        "せせらぎの水が持つ7つの特性を、三島の行動原理として言語化した指針。",
    )

    # --- ビジョン構造 ---
    st.markdown("### ビジョンの全体構造")
    st.markdown(
        """
        <div style="max-width:640px; margin:0 auto 1.5rem auto;">
            <!-- 最上位 -->
            <div style="background:linear-gradient(135deg, #0d3b66, #1a6b8a); color:#fff;
                        border-radius:14px; padding:1.3rem; text-align:center; font-weight:900;
                        font-size:1.15rem; letter-spacing:0.06em;">
                セセラギズム（哲学・世界観）
            </div>
            <div style="text-align:center; color:#1a6b8a; font-size:0.8rem; margin:0.4rem 0;">
                <div style="border-left:2px solid #80deea; height:20px; margin:0 auto; width:0;"></div>│
            </div>
            <!-- 地域像 -->
            <div style="background:linear-gradient(135deg, #1a6b8a, #48b4a0); color:#fff;
                        border-radius:14px; padding:1rem; text-align:center; font-weight:700;
                        font-size:0.95rem;">
                地域像：三島は10年後にどんなまちか（ビジョンステートメント）
            </div>
            <div style="text-align:center; color:#1a6b8a; font-size:0.8rem; margin:0.4rem 0;">
                <div style="border-left:2px solid #80deea; height:20px; margin:0 auto; width:0;"></div>│
            </div>
            <!-- 7つの行動原則 -->
            <div style="background:linear-gradient(135deg, #e0f7fa, #b2ebf2); border:2px solid #80deea;
                        border-radius:14px; padding:1.1rem; text-align:center; font-weight:700;
                        color:#0a2540; font-size:1rem;">
                7つの行動原則
            </div>
            <div style="text-align:center; color:#1a6b8a; font-size:0.8rem; margin:0.4rem 0;">
                <div style="border-left:2px solid #80deea; height:20px; margin:0 auto; width:0;"></div>│
            </div>
            <!-- 重点テーマ -->
            <div style="background:#ffffff; border:2px solid #26c6da; border-radius:14px;
                        padding:1rem; text-align:center; font-weight:700; color:#0d3b66; font-size:0.95rem;">
                重点テーマ①〜④<br/>
                <span style="font-size:0.78rem; font-weight:400; color:#607d8b;">
                    各テーマが「セセラギズム」と接続</span>
            </div>
            <div style="text-align:center; color:#1a6b8a; font-size:0.8rem; margin:0.4rem 0;">
                <div style="border-left:2px solid #80deea; height:20px; margin:0 auto; width:0;"></div>│
            </div>
            <!-- アクションプラン -->
            <div style="background:#ffffff; border:1px solid #b2ebf2; border-radius:14px;
                        padding:1rem; text-align:center; font-weight:600; color:#0d3b66; font-size:0.9rem;">
                アクションプラン（短期・中期・長期）
            </div>
            <div style="text-align:center; color:#1a6b8a; font-size:0.8rem; margin:0.4rem 0;">
                <div style="border-left:2px solid #80deea; height:20px; margin:0 auto; width:0;"></div>│
            </div>
            <!-- KPI -->
            <div style="background:#ffffff; border:1px solid #b2ebf2; border-radius:14px;
                        padding:1rem; text-align:center; font-weight:600; color:#0d3b66; font-size:0.9rem;">
                KPI・モニタリング
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- せせらぎの本質的特性 ---
    st.markdown("### せせらぎの本質的特性")
    st.markdown("水の流れが持つ6つの特性。そのすべてが三島の行動原理と重なる。")

    features = [
        ("🌊", "止まらない", "常に流れ続ける。停滞しない。変化しながらも途切れない。"),
        ("💎", "小さいが力がある", "岩をも削る。小さな流れが持つ驚くべきパワー。"),
        ("🏞", "集まると大きな流れになる", "小川が大河に。個の力が集まり、うねりを生む。"),
        ("🔄", "どこにでも道を見つける", "障害物を避け、時には超えて。柔軟に前へ進む。"),
        ("🌿", "周りを潤す", "流れるだけで周囲に恵みを与える。存在自体が価値。"),
        ("🎵", "音を生む", "流れること自体がリズムになる。行動がビートを刻む。"),
    ]

    features_html = '<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:1rem; margin-bottom:1rem;">'
    for icon, title, text in features:
        features_html += f"""
            <div class="concept-card">
                <div class="concept-icon">{icon}</div>
                <div class="concept-title">{title}</div>
                <div class="concept-text">{text}</div>
            </div>"""
    features_html += "</div>"
    st.markdown(features_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 7つの行動原則 ---
    st.markdown("### せせらぎの特性 × 行動原則")
    st.markdown("水の流れが教えてくれる、7つの行動のかたち。")

    principles = [
        (
            "💧", "湧き出すことから", "主体性",
            "止まらない",
            "誰かを待たず、自ら動き出す",
            "自分から動けているだろうか",
        ),
        (
            "🤝", "受け入れることから", "開放性",
            "周りを潤す",
            "外から来る人・コト・アイデアを拒まない。潤し、潤される関係をつくる",
            "互いに潤し合えているだろうか",
        ),
        (
            "🌱", "小さく始めることから", "実行力",
            "小さいが力がある",
            "完璧を待たず、まず一筋の流れを生む",
            "まず一歩を踏み出せているだろうか",
        ),
        (
            "🔄", "道を見つけることから", "柔軟性",
            "どこにでも道を見つける",
            "障害があっても止まらない。しなやかに迂回する",
            "別の水路に目を向けているだろうか",
        ),
        (
            "🌊", "合流することから", "連携",
            "集まると大きな流れになる",
            "異なる業種・世代・立場がつながる場をつくる",
            "まだ出会えていない流れがないだろうか",
        ),
        (
            "🌿", "浸透を信じることから", "持続性",
            "浸透する",
            "すぐに成果が見えなくても、地道に染み込ませる",
            "地域に染み込んでいるだろうか",
        ),
        (
            "🎵", "響かせることから", "発信",
            "音を生む",
            "楽しみながら行動し、外に向けて鳴らす",
            "外に届いているだろうか",
        ),
    ]

    principles_html = ""
    for i, (icon, title, keyword, water, meaning, criteria) in enumerate(principles):
        num = i + 1
        bg = "linear-gradient(135deg, #e0f7fa 0%, #ffffff 60%)" if num % 2 == 1 else "#ffffff"
        principles_html += f"""
            <div style="display:grid; grid-template-columns:80px 1fr; gap:1rem;
                        background:{bg}; border-radius:14px; padding:1.4rem 1.5rem;
                        margin-bottom:0.8rem; box-shadow:0 2px 10px rgba(10,37,64,0.06);
                        border-left:5px solid #1a6b8a;">
                <div style="text-align:center;">
                    <div style="font-size:2rem; margin-bottom:0.3rem;">{icon}</div>
                    <div style="display:inline-block; background:linear-gradient(135deg, #0d3b66, #1a6b8a);
                                color:#fff; font-size:0.75rem; font-weight:700;
                                padding:0.2rem 0.7rem; border-radius:12px;">{keyword}</div>
                </div>
                <div>
                    <div style="font-size:1.15rem; font-weight:900; color:#0a2540; margin-bottom:0.2rem;">
                        {num}. {title}
                    </div>
                    <div style="font-size:0.78rem; color:#1a6b8a; font-weight:600; margin-bottom:0.4rem;">
                        せせらぎの特性：{water}
                    </div>
                    <div style="font-size:0.88rem; color:#37474f; line-height:1.65; margin-bottom:0.5rem;">
                        {meaning}
                    </div>
                    <div style="background:rgba(26,107,138,0.06); border-radius:8px; padding:0.5rem 0.8rem;
                                font-size:0.82rem; color:#0d3b66; font-style:italic;">
                        {criteria}
                    </div>
                </div>
            </div>"""
    st.markdown(principles_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-divider-wave">
            <svg viewBox="0 0 1200 32" preserveAspectRatio="none">
                <path d="M0,16 C150,28 350,4 500,16 C650,28 850,4 1000,16 C1100,24 1150,8 1200,16"
                      fill="none" stroke="#80deea" stroke-width="2"/>
                <path d="M0,20 C200,8 400,30 600,18 C800,6 1000,28 1200,16"
                      fill="none" stroke="#b2ebf2" stroke-width="1.5"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- まとめ ---
    st.markdown(
        """
        <div class="narrative-box">
            <p>
                7つの行動原則は、すべて <strong>「〜ことから」</strong> で結ばれている。<br/>
                押しつけではなく、一歩踏み出す姿勢の提案。<br/><br/>
                せせらぎの水が自然と湧き出し、流れ、合流し、浸透し、音を奏でるように、<br/>
                三島の人と活動もまた、この7つの原則に沿って動き出す。<br/><br/>
                迷ったときは、それぞれの <strong>判断基準</strong> に立ち返る。<br/>
                「自分から動けているだろうか」「外に届いているだろうか」<br/>
                その問いかけが、セセラギズムの羅針盤になる。
            </p>
            <span class="narrative-emphasis">
                水のように、自然体で、しなやかに。
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# メイン
# ============================================================
def main() -> None:
    """アプリケーションのエントリポイント。"""
    inject_custom_css()
    render_sidebar_decoration()

    pg = st.navigation(
        [
            st.Page(page_vision_evolution, title="ビジョンの変遷", icon="📊"),
            st.Page(page_seseragism, title="セセラギズム", icon="🌊"),
            st.Page(page_action_principles, title="行動原則", icon="💧"),
            st.Page(page_workshop_analysis, title="ワークショップ分析", icon="🔍"),
            st.Page(page_survey_analysis, title="アンケート分析", icon="📋"),
            st.Page(page_statistics, title="三島市統計データ", icon="📈"),
        ]
    )
    pg.run()


if __name__ == "__main__":
    main()
