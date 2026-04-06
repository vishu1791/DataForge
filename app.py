import streamlit as st
from ui.sidebar import render_sidebar
from ui.main_panel import render_main_panel
from config.settings import APP_CONFIG

def main():
    st.set_page_config(
        page_title=APP_CONFIG["app_title"],
        page_icon=APP_CONFIG["app_icon"],
        layout=APP_CONFIG["layout"]
    )
    
    st.title(APP_CONFIG["app_title"])
    
    # Render sidebar and main panel
    render_sidebar()
    render_main_panel()

if __name__ == "__main__":
    main()
