# =========================
# 🎨 LIGHT THEME CONFIGURATION
# =========================

# Light Color Palette - Fresh and Modern
PRIMARY = "#8DBCC7"        # Soft Teal Blue - Primary brand color
SECONDARY = "#A4CCD9"      # Light Sky Blue - Secondary elements
ACCENT = "#C4E1E6"         # Very Light Blue - Accent backgrounds
BACKGROUND = "#EBFFD8"     # Very Light Green - Main background
LIGHT = "#FFFFFF"          # Pure White - Cards and containers
TEXT_DARK = "#2C3E50"      # Dark Navy Blue - Primary text
TEXT_MEDIUM = "#34495E"    # Medium Gray Blue - Secondary text
TEXT_LIGHT = "#7F8C8D"     # Light Gray - Muted text
BORDER_LIGHT = "#E8F4F8"   # Very Light Blue Border
SUCCESS = "#27AE60"        # Green for success states
WARNING = "#F39C12"        # Orange for warnings
ERROR = "#E74C3C"          # Red for errors

def get_light_theme_css():
    """Returns the complete CSS for light theme styling"""
    return f"""
    <style>
        /* Import Modern Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* Main App Background - Light and Fresh */
        .stApp {{
            background: linear-gradient(135deg, {BACKGROUND} 0%, {LIGHT} 50%, {ACCENT} 100%);
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            direction: rtl;
            text-align: right;
        }}
        
        /* Arabic Font Support */
        * {{
            font-family: 'Inter', 'Segoe UI', 'Tahoma', 'Arial', sans-serif !important;
        }}
        
        /* RTL Support for all text elements */
        .stMarkdown, .stText, p, div, span {{
            direction: rtl;
            text-align: right;
        }}
        
        /* Fix button alignment for RTL */
        .stButton {{
            direction: rtl;
            text-align: center;
        }}
        
        /* File uploader RTL support */
        .stFileUploader {{
            direction: rtl;
            text-align: center;
        }}
        
        /* Sidebar RTL support */
        .css-1d391kg {{
            direction: rtl;
        }}
        
        /* Column layout RTL support */
        .stColumns {{
            direction: rtl;
        }}
        
        /* Metric containers RTL support */
        .metric-container {{
            direction: rtl;
            text-align: center;
        }}
        
        /* Subtle Pattern Overlay */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 80%, {PRIMARY}08 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, {SECONDARY}06 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, {ACCENT}04 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }}
        
        /* Main Content Container */
        .main .block-container {{
            padding: 2rem 1rem;
            max-width: 1200px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(141, 188, 199, 0.1);
            margin: 1rem auto;
        }}
        
        /* Headers and Titles */
        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT_DARK} !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em;
        }}
        
        h1 {{
            font-size: 2.5rem !important;
            color: {TEXT_DARK} !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }}
        
        /* Sidebar Styling */
        .css-1d391kg {{
            background: linear-gradient(180deg, {LIGHT} 0%, {ACCENT} 100%) !important;
            border-right: 1px solid {BORDER_LIGHT};
        }}
        
        /* Sidebar Navigation */
        .css-17lntkn {{
            background: {LIGHT} !important;
            border: 1px solid {BORDER_LIGHT} !important;
            border-radius: 12px !important;
            color: {TEXT_DARK} !important;
        }}
        
        /* Active Sidebar Item */
        .css-17lntkn[aria-selected="true"] {{
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}) !important;
            color: white !important;
            font-weight: 600 !important;
        }}
        
        /* Buttons - Modern and Clean */
        .stButton > button {{
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(141, 188, 199, 0.2) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(141, 188, 199, 0.3) !important;
            background: linear-gradient(135deg, {SECONDARY}, {PRIMARY}) !important;
        }}
        
        .stButton > button:active {{
            transform: translateY(0px) !important;
        }}
        
        /* File Uploader */
        .stFileUploader {{
            background: {LIGHT} !important;
            border: 2px dashed {PRIMARY} !important;
            border-radius: 16px !important;
            padding: 2rem !important;
            text-align: center !important;
        }}
        
        .stFileUploader label {{
            color: {TEXT_DARK} !important;
            font-weight: 500 !important;
        }}
        
        .stFileUploader:hover {{
            border-color: {SECONDARY} !important;
            background: {ACCENT} !important;
        }}
        
        .stFileUploader:hover label {{
            color: {TEXT_DARK} !important;
        }}
        
        /* Uploaded File Details */
        .stFileUploader div[data-testid="stFileUploaderFile"] {{
            background: {ACCENT} !important;
            border: 1px solid {BORDER_LIGHT} !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            margin: 0.5rem 0 !important;
        }}
        
        .stFileUploader div[data-testid="stFileUploaderFile"] * {{
            color: {TEXT_DARK} !important;
        }}
        
        /* File name and size text */
        .stFileUploader .uploadedFileName {{
            color: {TEXT_DARK} !important;
            font-weight: 500 !important;
        }}
        
        .stFileUploader .uploadedFileSize {{
            color: {TEXT_MEDIUM} !important;
        }}
        
        /* Remove file button (X) */
        .stFileUploader button[title="Remove file"] {{
            color: {TEXT_DARK} !important;
            background: transparent !important;
            border: 1px solid {TEXT_LIGHT} !important;
            border-radius: 4px !important;
        }}
        
        .stFileUploader button[title="Remove file"]:hover {{
            background: {ERROR} !important;
            color: white !important;
            border-color: {ERROR} !important;
        }}
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {{
            background: {LIGHT} !important;
            border: 2px solid {BORDER_LIGHT} !important;
            border-radius: 12px !important;
            color: {TEXT_DARK} !important;
            font-size: 1rem !important;
            padding: 0.75rem !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 3px rgba(141, 188, 199, 0.1) !important;
        }}
        
        /* Cards and Containers */
        .stContainer {{
            background: {LIGHT} !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            box-shadow: 0 4px 20px rgba(141, 188, 199, 0.1) !important;
            border: 1px solid {BORDER_LIGHT} !important;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: {ACCENT} !important;
            border-radius: 12px !important;
            color: {TEXT_DARK} !important;
            font-weight: 500 !important;
        }}
        
        .streamlit-expanderContent {{
            background: {LIGHT} !important;
            border: 1px solid {BORDER_LIGHT} !important;
            border-radius: 0 0 12px 12px !important;
        }}
        
        /* Metrics */
        .metric-container {{
            background: {LIGHT} !important;
            padding: 1.5rem !important;
            border-radius: 16px !important;
            border: 1px solid {BORDER_LIGHT} !important;
            text-align: center !important;
        }}
        
        /* Success/Warning/Error Messages */
        .stAlert {{
            border-radius: 12px !important;
            border: none !important;
            font-weight: 500 !important;
        }}
        
        .stSuccess {{
            background: rgba(39, 174, 96, 0.1) !important;
            color: {SUCCESS} !important;
        }}
        
        .stWarning {{
            background: rgba(243, 156, 18, 0.1) !important;
            color: {WARNING} !important;
        }}
        
        .stError {{
            background: rgba(231, 76, 60, 0.1) !important;
            color: {ERROR} !important;
        }}
        
        /* Tables */
        .stDataFrame {{
            background: {LIGHT} !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 20px rgba(141, 188, 199, 0.1) !important;
        }}
        
        /* Progress Bar */
        .stProgress > div > div {{
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}) !important;
        }}
        
        /* Columns */
        .css-12oz5g7 {{
            padding: 1rem !important;
        }}
        
        /* Text Elements */
        .stMarkdown {{
            color: {TEXT_DARK} !important;
        }}
        
        .caption {{
            color: {TEXT_LIGHT} !important;
            font-style: italic !important;
        }}
        
        /* Code Blocks */
        .stCodeBlock {{
            background: {LIGHT} !important;
            border: 1px solid {BORDER_LIGHT} !important;
            border-radius: 12px !important;
        }}
        
        /* Custom Classes for Special Elements */
        .invoice-header {{
            background: linear-gradient(135deg, {PRIMARY}, {SECONDARY}) !important;
            color: white !important;
            padding: 2rem !important;
            border-radius: 16px !important;
            text-align: center !important;
            margin-bottom: 2rem !important;
        }}
        
        .invoice-header h1 {{
            color: white !important;
            background: none !important;
            -webkit-text-fill-color: white !important;
        }}
        
        .feature-card {{
            background: {LIGHT} !important;
            border: 1px solid {BORDER_LIGHT} !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            transition: all 0.3s ease !important;
        }}
        
        .feature-card:hover {{
            transform: translateY(-4px) !important;
            box-shadow: 0 8px 30px rgba(141, 188, 199, 0.15) !important;
        }}
        
        /* Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {BACKGROUND};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {PRIMARY};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {SECONDARY};
        }}
    </style>
    """

def get_page_config():
    """Returns page configuration for Streamlit"""
    return {
        "page_title": "📑 محلل الفواتير الذكي",
        "page_icon": "📊",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "menu_items": {
            'Get Help': 'https://github.com/your-repo/help',
            'Report a bug': "https://github.com/your-repo/issues",
            'About': "# محلل الفواتير الذكي\nنظام معالجة الفواتير بالذكاء الاصطناعي"
        }
    }