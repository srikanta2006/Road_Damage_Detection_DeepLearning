import streamlit as st

def apply_custom_style():
    """
    Applies an Enterprise-Grade Subtle Light Theme (Slate/Blue).
    High-readability, minimalist design with professional typography.
    """
    st.markdown("""
    <!-- FontAwesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    
    <!-- Custom CSS -->
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;600;800&display=swap');

    :root {
        --bg-slate-50: #F8FAFC;
        --bg-white: #FFFFFF;
        --text-slate-900: #0F172A;
        --text-slate-600: #475569;
        --text-slate-400: #94A3B8;
        --primary-blue: #3B82F6;
        --border-slate-200: #E2E8F0;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }

    /* Global Body */
    html, body, [data-testid="stSidebar"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-slate-50) !important;
        color: var(--text-slate-900);
    }

    /* Hide Default Streamlit Elements */
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stHeader"] { visibility: hidden !important; height: 0 !important; }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    footer { visibility: hidden !important; }

    /* Layout Spacing */
    .block-container { padding-top: 1rem !important; }

    /* Modern Card Layout */
    .modern-card {
        background: var(--bg-white);
        border-radius: 12px;
        border: 1px solid var(--border-slate-200);
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .modern-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--primary-blue);
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        color: var(--text-slate-900) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--text-slate-600);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-slate-900);
    }

    /* Navbar Redesign */
    .nav-label {
        font-size: 0.65rem;
        color: var(--text-slate-400);
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 6px;
        text-align: center;
    }

    /* Button Overrides - Professional Link Style */
    .stButton>button {
        background: transparent;
        color: var(--text-slate-600);
        border: none;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        font-weight: 600;
        padding: 8px 12px;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        white-space: nowrap !important;
        width: auto !important;
    }

    .stButton>button:hover {
        color: var(--primary-blue);
        background: rgba(59, 130, 246, 0.05);
        border-bottom: 2px solid var(--primary-blue);
    }

    /* Use this wrapper to mark a button as active */
    .nav-active button {
        color: var(--primary-blue) !important;
        border-bottom: 2px solid var(--primary-blue) !important;
    }

    /* Action Buttons (Standard styled buttons) */
    .action-btn button {
        background: var(--primary-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1) !important;
    }

    .action-btn button:hover {
        background: #2563EB !important;
        box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.2) !important;
    }

    /* Sidebar Integrity */
    [data-testid="stSidebar"] {
        border-right: 1px solid var(--border-slate-200);
        padding-top: 2.5rem;
    }

    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 60px 0 40px 0;
        background: radial-gradient(circle at top, #EFF6FF 0%, transparent 70%);
        border-radius: 20px;
        margin-bottom: 40px;
    }

    .hero-tagline {
        color: var(--text-slate-600);
        font-size: 1.125rem;
        max-width: 600px;
        margin: 16px auto;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

def render_modern_card(title, value, icon_class):
    """
    Renders a high-precision card for metrics.
    """
    st.markdown(f"""
    <div class="modern-card">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <div style="width: 32px; height: 32px; background: #EFF6FF; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--primary-blue);">
                <i class="fa-solid {icon_class}"></i>
            </div>
            <div class="metric-label">{title}</div>
        </div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_top_nav(current_page):
    """
    Renders the Elite Modern Single-Row Navbar with logical hierarchy.
    """
    # Define pages for better mapping
    pages = {
        "Home": "Home.py",
        "Image": "pages/Image_Detection.py",
        "Video": "pages/Video_Detection.py",
        "Live": "pages/Webcam_Detection.py",
        "Management": "pages/6_Management.py",
        "Verification": "pages/8_Verification.py",
        "Maps": "pages/Map.py",
        "Analytics": "pages/7_Analytics.py",
        "Report": "pages/Report.py"
    }

    # Custom styling for active button injection
    def get_style(page_name):
        return "nav-active" if current_page == page_name else ""

    # Group Header Labels (Above Buttons)
    h1, h2, h3, h4 = st.columns([1, 2, 2, 1.5])
    h1.markdown("<div class='nav-label'>MISSION HUB</div>", unsafe_allow_html=True)
    h2.markdown("<div class='nav-label'>DEPLOYMENT CORE</div>", unsafe_allow_html=True)
    h3.markdown("<div class='nav-label'>TACTICAL OPS</div>", unsafe_allow_html=True)
    h4.markdown("<div class='nav-label'>INTELLIGENCE</div>", unsafe_allow_html=True)

    # Navbar Row
    c1, c2, c3, c4 = st.columns([1, 2.5, 2.5, 1.5])

    with c1:
        st.markdown(f"<div class='{get_style('Home')}'>", unsafe_allow_html=True)
        if st.button("🏠 Home", key="btn_h"):
            st.switch_page(pages["Home"])
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        sub1, sub2, sub3 = st.columns(3)
        with sub1:
            st.markdown(f"<div class='{get_style('Image')}'>", unsafe_allow_html=True)
            if st.button("📸 IMAGE"): st.switch_page(pages["Image"])
            st.markdown("</div>", unsafe_allow_html=True)
        with sub2:
            st.markdown(f"<div class='{get_style('Video')}'>", unsafe_allow_html=True)
            if st.button("🎥 VIDEO"): st.switch_page(pages["Video"])
            st.markdown("</div>", unsafe_allow_html=True)
        with sub3:
            st.markdown(f"<div class='{get_style('Live')}'>", unsafe_allow_html=True)
            if st.button("📡 LIVE"): st.switch_page(pages["Live"])
            st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        sub1, sub2, sub3 = st.columns(3)
        with sub1:
            st.markdown(f"<div class='{get_style('Management')}'>", unsafe_allow_html=True)
            if st.button("📋 MGMT"): st.switch_page(pages["Management"])
            st.markdown("</div>", unsafe_allow_html=True)
        with sub2:
            st.markdown(f"<div class='{get_style('Verification')}'>", unsafe_allow_html=True)
            if st.button("✅ VFY"): st.switch_page(pages["Verification"])
            st.markdown("</div>", unsafe_allow_html=True)
        with sub3:
            st.markdown(f"<div class='{get_style('Maps')}'>", unsafe_allow_html=True)
            if st.button("🗺️ MAPS"): st.switch_page(pages["Maps"])
            st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        sub1, sub2 = st.columns(2)
        with sub1:
            st.markdown(f"<div class='{get_style('Analytics')}'>", unsafe_allow_html=True)
            if st.button("📊 ANA"): st.switch_page(pages["Analytics"])
            st.markdown("</div>", unsafe_allow_html=True)
        with sub2:
            st.markdown(f"<div class='{get_style('Report')}'>", unsafe_allow_html=True)
            if st.button("🧾 REP"): st.switch_page(pages["Report"])
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 4px; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
