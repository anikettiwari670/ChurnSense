import streamlit as st


def apply_theme():
    """Apply a consistent, high-contrast dark theme to ChurnSense."""

    st.markdown(
        """
<style>

/* =====================================================
   1. GLOBAL BACKGROUND AND TYPOGRAPHY
===================================================== */

.stApp {
    background:
        radial-gradient(
            ellipse at top left,
            rgba(32, 74, 111, 0.22),
            transparent 42%
        ),
        #0B1120 !important;
    color: #E2E8F0 !important;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 2.5rem;
}

h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
}

.stApp .stMarkdown,
.stApp .stMarkdown p,
.stApp .stMarkdown li {
    color: #CBD5E1;
}

.stApp [data-testid="stCaptionContainer"] {
    color: #A7B7CB !important;
}

/* =====================================================
   2. SIDEBAR AND NAVIGATION
===================================================== */

[data-testid="stSidebar"] {
    background: #0D1729 !important;
    border-right: 1px solid #24334B;
}

[data-testid="stSidebar"] * {
    color: #DCE7F5;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #CBD5E1;
}

[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin-bottom: 4px;
}

[data-testid="stSidebarNav"] a:hover {
    background: #172A40 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #18334A !important;
    border: 1px solid #2B5869;
}

/* =====================================================
   3. KPI AND METRIC CARDS
===================================================== */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #18263D,
        #111C2F
    ) !important;
    border: 1px solid #293A54;
    border-radius: 15px;
    padding: 20px 22px;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.12);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #AFC0D4 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-weight: 750;
}

[data-testid="stMetricDelta"] {
    color: #5EEAD4 !important;
}

/* =====================================================
   4. FORM LABELS
===================================================== */

.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label,
.stApp .stSelectbox label,
.stApp .stMultiSelect label,
.stApp .stTextInput label,
.stApp .stNumberInput label,
.stApp .stTextArea label,
.stApp .stDateInput label,
.stApp .stTimeInput label,
.stApp .stSlider label,
.stApp .stFileUploader label,
.stApp [data-testid="stCheckbox"] label,
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stToggle"] label {
    color: #F1F5F9 !important;
    -webkit-text-fill-color: #F1F5F9 !important;
    font-weight: 600 !important;
}

.stApp [data-testid="stWidgetLabel"] small,
.stApp [data-testid="stCaptionContainer"] {
    color: #CBD5E1 !important;
}

/* =====================================================
   5. TEXT INPUTS, NUMBER INPUTS AND TEXT AREAS
===================================================== */

.stApp div[data-baseweb="input"] > div,
.stApp div[data-baseweb="textarea"] > div {
    background-color: #F1F5F9 !important;
    border: 1px solid #A8B8CA !important;
    border-radius: 9px !important;
}

.stApp div[data-baseweb="input"] input,
.stApp div[data-baseweb="textarea"] textarea,
.stApp input[type="text"],
.stApp input[type="number"],
.stApp input[type="email"],
.stApp input[type="password"],
.stApp textarea {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    caret-color: #0F766E !important;
    opacity: 1 !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
    opacity: 1 !important;
}

.stApp div[data-testid="stNumberInput"] button {
    color: #0F172A !important;
}

/* =====================================================
   6. SELECT BOXES AND DROPDOWNS
===================================================== */

.stApp div[data-baseweb="select"] > div {
    background-color: #F1F5F9 !important;
    border: 1px solid #A8B8CA !important;
    border-radius: 9px !important;
}

.stApp div[data-baseweb="select"] div[class*="singleValue"],
.stApp div[data-baseweb="select"] div[class*="placeholder"] {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

.stApp div[data-baseweb="select"] span,
.stApp div[data-baseweb="select"] input {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

.stApp div[data-baseweb="select"] svg {
    fill: #334155 !important;
    color: #334155 !important;
}

/* Dropdown popup */

.stApp [data-baseweb="popover"],
.stApp [data-baseweb="menu"] {
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
}

.stApp [role="option"] {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

.stApp [role="option"] * {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

.stApp [role="option"]:hover {
    background-color: #DDECF4 !important;
}

/* Multiselect tags */

.stApp [data-baseweb="tag"] {
    background-color: #DCECEB !important;
}

.stApp [data-baseweb="tag"] * {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

/* Focus states */

.stApp div[data-baseweb="input"]:focus-within,
.stApp div[data-baseweb="textarea"]:focus-within,
.stApp div[data-baseweb="select"]:focus-within {
    border-color: #0F766E !important;
    box-shadow: 0 0 0 2px rgba(94, 234, 212, 0.22) !important;
}

/* =====================================================
   7. STANDARD, PRIMARY AND DOWNLOAD BUTTONS
===================================================== */

/* Standard buttons */

.stApp .stButton > button,
.stApp .stFormSubmitButton > button {
    background-color: #1D354B !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #5B7C96 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 42px;
    padding: 0.55rem 1rem !important;
    opacity: 1 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

.stApp .stButton > button *,
.stApp .stFormSubmitButton > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Primary buttons */

.stApp .stButton > button[kind="primary"],
.stApp .stFormSubmitButton > button[kind="primary"] {
    background-color: #5EEAD4 !important;
    color: #0B1120 !important;
    -webkit-text-fill-color: #0B1120 !important;
    border-color: #5EEAD4 !important;
    font-weight: 800 !important;
}

.stApp .stButton > button[kind="primary"] *,
.stApp .stFormSubmitButton > button[kind="primary"] * {
    color: #0B1120 !important;
    -webkit-text-fill-color: #0B1120 !important;
}

/* Download buttons */

.stApp .stDownloadButton > button {
    background-color: #5EEAD4 !important;
    color: #0B1120 !important;
    -webkit-text-fill-color: #0B1120 !important;
    border: 1px solid #5EEAD4 !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    min-height: 42px;
    padding: 0.55rem 1rem !important;
    opacity: 1 !important;
}

.stApp .stDownloadButton > button * {
    color: #0B1120 !important;
    -webkit-text-fill-color: #0B1120 !important;
}

/* Standard button hover */

.stApp .stButton > button:hover,
.stApp .stFormSubmitButton > button:hover {
    background-color: #2C536B !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border-color: #5EEAD4 !important;
}

.stApp .stButton > button:hover *,
.stApp .stFormSubmitButton > button:hover * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Primary and download button hover */

.stApp .stButton > button[kind="primary"]:hover,
.stApp .stFormSubmitButton > button[kind="primary"]:hover,
.stApp .stDownloadButton > button:hover {
    background-color: #99F6E4 !important;
    color: #0B1120 !important;
    -webkit-text-fill-color: #0B1120 !important;
    border-color: #99F6E4 !important;
}

.stApp .stButton > button[kind="primary"]:hover *,
.stApp .stFormSubmitButton > button[kind="primary"]:hover *,
.stApp .stDownloadButton > button:hover * {
    color: #0B1120 !important;
    -webkit-text-fill-color: #0B1120 !important;
}

/* Disabled buttons */

.stApp .stButton > button:disabled,
.stApp .stDownloadButton > button:disabled,
.stApp .stFormSubmitButton > button:disabled {
    background-color: #273449 !important;
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
    border-color: #475569 !important;
    opacity: 1 !important;
    cursor: not-allowed !important;
}

.stApp .stButton > button:disabled *,
.stApp .stDownloadButton > button:disabled *,
.stApp .stFormSubmitButton > button:disabled * {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
}

/* Keyboard focus */

.stApp .stButton > button:focus-visible,
.stApp .stDownloadButton > button:focus-visible,
.stApp .stFormSubmitButton > button:focus-visible {
    outline: 3px solid #FBBF24 !important;
    outline-offset: 3px !important;
}

/* =====================================================
   8. FILE UPLOADER — WHITE INSTRUCTIONS AND FILE LIMIT
   Includes "200MB Per File · CSV" and "Browse Files"
===================================================== */

.stApp [data-testid="stFileUploader"] {
    background-color: #111C2F !important;
    border: 1px dashed #49647F !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

/* Keep the drop zone dark */

.stApp [data-testid="stFileUploaderDropzone"] {
    background-color: #111C2F !important;
    border: 1px dashed #49647F !important;
    border-radius: 10px !important;
}

/* Make uploader instructions and size/type information white */

.stApp [data-testid="stFileUploader"] *,
.stApp [data-testid="stFileUploaderDropzone"] *,
.stApp [data-testid="stFileUploaderDropzoneInstructions"],
.stApp [data-testid="stFileUploaderDropzoneInstructions"] *,
.stApp [data-testid="stFileUploaderDropzoneInstructions"] span,
.stApp [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Browse files button */

.stApp [data-testid="stFileUploader"] button {
    background-color: #1D354B !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #5EEAD4 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

.stApp [data-testid="stFileUploader"] button *,
.stApp [data-testid="stFileUploader"] button span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Uploaded file names and details */

.stApp [data-testid="stFileUploaderFile"],
.stApp [data-testid="stFileUploaderFile"] *,
.stApp [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* =====================================================
   9. CHECKBOXES, RADIO BUTTONS AND TOGGLES
===================================================== */

.stApp [data-testid="stCheckbox"] label,
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stToggle"] label {
    color: #F1F5F9 !important;
    -webkit-text-fill-color: #F1F5F9 !important;
}

/* =====================================================
   10. DATAFRAMES AND TABLES
===================================================== */

.stApp [data-testid="stDataFrame"],
.stApp [data-testid="stTable"] {
    border: 1px solid #293A54;
    border-radius: 12px;
    overflow: hidden;
}

/* =====================================================
   11. EXPANDERS
===================================================== */

.stApp [data-testid="stExpander"] {
    background-color: #111C2F !important;
    border: 1px solid #293A54 !important;
    border-radius: 12px;
}

.stApp [data-testid="stExpander"] summary {
    color: #F1F5F9 !important;
}

/* =====================================================
   12. ALERTS AND DIVIDERS
===================================================== */

.stApp [data-testid="stAlert"] {
    border-radius: 12px;
}

.stApp hr {
    border-color: #293A54 !important;
}

/* =====================================================
   13. RESPONSIVE LAYOUT
===================================================== */

@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }
}

</style>
        """,
        unsafe_allow_html=True,
    )