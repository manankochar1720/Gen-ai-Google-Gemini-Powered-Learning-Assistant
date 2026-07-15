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
html_file_path = os.path.join(current_dir, "assets", "index_v2.html")

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

    # Automatically detect environment: Local Laptop vs Streamlit Cloud
    is_local_machine = False
    try:
        # Check if the folder path belongs to your local D: drive structure
        if "edugenie" in html_file_path.lower() and ("d:\\" in html_file_path.lower() or "d:/" in html_file_path.lower()):
            is_local_machine = True
    except Exception:
        pass

    if is_local_machine:
        backend_url = "http://127.0.0.1:8000/api"
    else:
        # Streamlit Cloud deployment: Use your Render backend URL directly
        backend_url = "https://edugenie-backend-dxox.onrender.com/api"

    html_content = html_content.replace("BACKEND_URL_PLACEHOLDER", backend_url)

    # Serve full screen (using 680 height to fit typical laptop screens)
    st.components.v1.html(html_content, height=680, scrolling=True)
else:
    st.error("⚠️ **System Error**: `assets/index.html` not found. Please verify the folder structure.")
