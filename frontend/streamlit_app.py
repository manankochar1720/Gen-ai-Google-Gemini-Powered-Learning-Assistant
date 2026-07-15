import streamlit as st
import os
import base64

# --------------------------------------------------
# Page Setup & Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="EduGenie - AI Learning Assistant",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Full-Screen Iframe Injection & Streamlit Hiding
# --------------------------------------------------
st.markdown("""
<style>
/* Hide top header, main menu, and footer entirely */
[data-testid="stHeader"], footer, #MainMenu {
    display: none !important;
}

/* Remove Streamlit default page container padding */
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    height: 100vh !important;
}

/* Force child iframe to expand to full viewport height */
iframe {
    height: 100vh !important;
    width: 100vw !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Serve Single Page HTML Application
# --------------------------------------------------
current_dir = os.path.dirname(__file__)
html_file_path = os.path.join(current_dir, "assets", "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Read and inject brand logo as inline Base64 Data URL
    logo_path = os.path.join(current_dir, "assets", "edugenie_logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_b64 = base64.b64encode(img_file.read()).decode("utf-8")
        html_content = html_content.replace("assets/edugenie_logo.png", f"data:image/png;base64,{logo_b64}")
        
    # Read and inject bottom sidebar illustration as inline Base64 Data URL
    decor_path = os.path.join(current_dir, "assets", "sidebar_decoration.png")
    if os.path.exists(decor_path):
        with open(decor_path, "rb") as img_file:
            decor_b64 = base64.b64encode(img_file.read()).decode("utf-8")
        html_content = html_content.replace("assets/sidebar_decoration.png", f"data:image/png;base64,{decor_b64}")

    # Read and inject robot workspace illustration as inline Base64 Data URL
    workspace_path = os.path.join(current_dir, "assets", "robot_workspace.png")
    if os.path.exists(workspace_path):
        with open(workspace_path, "rb") as img_file:
            workspace_b64 = base64.b64encode(img_file.read()).decode("utf-8")
        html_content = html_content.replace("assets/robot_workspace.png", f"data:image/png;base64,{workspace_b64}")

    # Inject backend URL dynamically (checks Streamlit secrets, then environment variables, then defaults to localhost)
    if "BACKEND_URL" in st.secrets:
        backend_url = st.secrets["BACKEND_URL"]
    else:
        backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/api")
    
    html_content = html_content.replace("BACKEND_URL_PLACEHOLDER", backend_url)

    # Optional debug logic injected directly into HTML JS execution
    debug_js = ""
    if "debug" in st.query_params:
        debug_js = f"""
        const banner = document.createElement("div");
        banner.style.position = "fixed";
        banner.style.top = "0";
        banner.style.left = "0";
        banner.style.width = "100%";
        banner.style.background = "#e11d48";
        banner.style.color = "white";
        banner.style.padding = "10px";
        banner.style.textAlign = "center";
        banner.style.zIndex = "999999";
        banner.style.fontWeight = "bold";
        banner.style.fontFamily = "Outfit, sans-serif";
        banner.innerText = "🔧 DEBUG: Injected Backend URL is: {backend_url}";
        document.body.appendChild(banner);
        """
    html_content = html_content.replace("// DEBUG_PLACEHOLDER", debug_js)

    # Serve full screen (using 680 height to fit typical laptop screens)
    st.components.v1.html(html_content, height=680, scrolling=True)
else:
    st.error("⚠️ **System Error**: `assets/index.html` not found. Please verify the folder structure.")
