import os
import sys
import sqlite3

# Add the project root directory to the python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration first
st.set_page_config(
    page_title="AI Burning & Micro-Dumping Detection",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from app.config import (
    MODEL_PATH,
    DATABASE_PATH,
    UPLOAD_IMAGE_DIR,
    UPLOAD_VIDEO_DIR,
    OUTPUT_IMAGE_DIR,
    OUTPUT_VIDEO_DIR,
    CLASSES
)
from app.database import (
    get_all_violations,
    update_violation_status,
    delete_violation,
    create_database
)
from app.detector import WasteDetector

# Ensure folders exist
os.makedirs(UPLOAD_IMAGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_VIDEO_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_VIDEO_DIR, exist_ok=True)

# Initialize database
create_database()

# Premium Glassmorphism styling and fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .kpi-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .kpi-val {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 5px 0;
    }
    
    .kpi-title {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
    }
    
    /* Custom Alerts */
    .alert-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Detector
@st.cache_resource
def get_detector():
    return WasteDetector(model_path=MODEL_PATH)

detector = get_detector()

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/external-flatart-icons-lineal-color-flatart-icons/128/external-ecology-ecology-flatart-icons-lineal-color-flatart-icons-3.png", width=80)
    st.markdown("<h2 style='margin-top: 0;'>EcoGuard AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem;'>Burning & Micro-Dumping Detection</p>", unsafe_allow_html=True)
    st.write("---")
    
    nav = st.radio(
        "Navigation",
        ["🏠 Home Dashboard", "🔍 Run Detection", "📋 Historical Logs", "📊 Analytics Hub"]
    )
    
    st.write("---")
    st.markdown("### System Configuration")
    conf_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.5, 0.05)
    detector.confidence_threshold = conf_threshold
    
    st.info("Tailored for Local Municipalities & Health Inspectors.")

# --- 1. HOME DASHBOARD ---
if nav == "🏠 Home Dashboard":
    st.markdown("<h1>Municipal Health Inspection Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Real-time ecological violation overview</p>", unsafe_allow_html=True)
    
    # Fetch Data
    rows = get_all_violations()
    df = pd.DataFrame(rows, columns=["ID", "Filename", "Type", "Confidence", "Timestamp", "Screenshot", "Status"])
    
    # KPIs
    total_cases = len(df)
    pending_cases = len(df[df["Status"] == "Pending"])
    resolved_cases = len(df[df["Status"] == "Resolved"])
    burning_cases = len(df[df["Type"].isin(["Smoke", "Fire"])])
    dumping_cases = len(df[df["Type"] == "Garbage_Pile"])
    
    # Render KPI Cards
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">🚨 Total Violations</div>
                <div class="kpi-val" style="color: #f8fafc;">{total_cases}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">⏳ Pending Review</div>
                <div class="kpi-val" style="color: #f59e0b;">{pending_cases}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">✅ Resolved</div>
                <div class="kpi-val" style="color: #10b981;">{resolved_cases}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">🔥 Burning Cases</div>
                <div class="kpi-val" style="color: #ef4444;">{burning_cases}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">🗑️ Dumping Cases</div>
                <div class="kpi-val" style="color: #3b82f6;">{dumping_cases}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Latest Alerts Banner
    if pending_cases > 0:
        latest_pending = df[df["Status"] == "Pending"].iloc[0]
        st.markdown(f"""
            <div class="alert-banner">
                <strong>⚠️ Action Required:</strong> Latest unresolved violation <b>{latest_pending['Type']}</b> detected in 
                <code>{latest_pending['Filename']}</code> at {latest_pending['Timestamp']} (Conf: {latest_pending['Confidence']:.2f}).
            </div>
        """, unsafe_allow_html=True)

    # Splitting Screen
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'><h3>Recent Unresolved Violations</h3>", unsafe_allow_html=True)
        unresolved_df = df[df["Status"] == "Pending"].head(5)
        if not unresolved_df.empty:
            st.dataframe(
                unresolved_df[["Filename", "Type", "Confidence", "Timestamp"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No pending violations! All clear. 🎉")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'><h3>System Information</h3>", unsafe_allow_html=True)
        st.write(f"**YOLO weights:** `{os.path.basename(MODEL_PATH)}`")
        st.write(f"**Database Location:** `{os.path.basename(DATABASE_PATH)}`")
        st.write(f"**Configured Classes:** {', '.join(CLASSES)}")
        st.write(f"**Current Confidence Cutoff:** `{conf_threshold}`")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. RUN DETECTION ---
elif nav == "🔍 Run Detection":
    st.markdown("<h1>AI Detection Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Upload media files to analyze and log violations</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📸 Image Detection", "🎥 Video Detection"])
    
    # Image Tab
    with tab1:
        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="image_uploader")
        if uploaded_image is not None:
            # Save original
            orig_path = os.path.join(UPLOAD_IMAGE_DIR, uploaded_image.name)
            with open(orig_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
                
            st.success(f"Image uploaded: {uploaded_image.name}")
            
            # Output path
            out_path = os.path.join(OUTPUT_IMAGE_DIR, f"annotated_{uploaded_image.name}")
            
            with st.spinner("Analyzing image..."):
                detections = detector.detect_image(orig_path, out_path)
                
            col_orig, col_annot = st.columns(2)
            with col_orig:
                st.subheader("Original Image")
                st.image(orig_path, use_container_width=True)
            with col_annot:
                st.subheader("AI Detection Result")
                st.image(out_path, use_container_width=True)
                
            if detections:
                st.markdown("### Detections Logged to Database")
                det_df = pd.DataFrame(detections)
                st.table(det_df[["class", "confidence"]])
            else:
                st.info("No violations detected in this image.")
                
    # Video Tab
    with tab2:
        uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov"], key="video_uploader")
        cooldown = st.number_input("Cooldown period (seconds)", min_value=5, max_value=300, value=30, step=5)
        
        if uploaded_video is not None:
            # Save original
            orig_path = os.path.join(UPLOAD_VIDEO_DIR, uploaded_video.name)
            with open(orig_path, "wb") as f:
                f.write(uploaded_video.getbuffer())
                
            st.success(f"Video uploaded: {uploaded_video.name}")
            
            # Output path
            out_path = os.path.join(OUTPUT_VIDEO_DIR, f"annotated_{uploaded_video.name}")
            
            if st.button("Start AI Analysis"):
                progress_bar = st.progress(0.0)
                status_text = st.empty()
                
                def update_progress(progress_val):
                    progress_bar.progress(progress_val)
                    status_text.text(f"Processing frame-by-frame: {progress_val*100:.1f}%")
                    
                with st.spinner("Running YOLOv11 model on video frames..."):
                    violations_count = detector.detect_video(
                        video_path=orig_path,
                        output_path=out_path,
                        cooldown_seconds=cooldown,
                        progress_callback=update_progress
                    )
                    
                st.success(f"Processing complete! Logged {violations_count} new violations.")
                
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    st.subheader("Input Video")
                    st.video(orig_path)
                with col_v2:
                    st.subheader("Processed Video")
                    st.video(out_path)
                    
                # Download Button
                with open(out_path, "rb") as file:
                    st.download_button(
                        label="Download Annotated Video",
                        data=file,
                        file_name=f"annotated_{uploaded_video.name}",
                        mime="video/mp4"
                    )

# --- 3. HISTORICAL LOGS ---
elif nav == "📋 Historical Logs":
    st.markdown("<h1>Historical Violation Records</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Review, update, and manage violation records</p>", unsafe_allow_html=True)
    
    # Fetch Data
    rows = get_all_violations()
    if not rows:
        st.info("No violations logged in the database yet.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Filename", "Type", "Confidence", "Timestamp", "Screenshot", "Status"])
        
        # Filters Section
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🔍 Filter Log Records")
        f_col1, f_col2, f_col3 = st.columns(3)
        
        with f_col1:
            filter_type = st.multiselect("Violation Type", options=df["Type"].unique(), default=df["Type"].unique())
        with f_col2:
            filter_status = st.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())
        with f_col3:
            filter_conf = st.slider("Confidence Range", 0.0, 1.0, (0.0, 1.0), 0.05)
            
        search_query = st.text_input("Search by File Name")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Apply Filters
        filtered_df = df[
            (df["Type"].isin(filter_type)) &
            (df["Status"].isin(filter_status)) &
            (df["Confidence"] >= filter_conf[0]) &
            (df["Confidence"] <= filter_conf[1])
        ]
        if search_query:
            filtered_df = filtered_df[filtered_df["Filename"].str.contains(search_query, case=False)]
            
        if filtered_df.empty:
            st.warning("No records match the filter criteria.")
        else:
            # Main Layout
            col_list, col_details = st.columns([3, 2])
            
            with col_list:
                st.subheader("Violations List")
                # Add index or select row
                selected_id = st.selectbox(
                    "Select a violation to view details and update status:",
                    options=filtered_df["ID"].tolist(),
                    format_func=lambda x: f"ID: {x} | {filtered_df[filtered_df['ID'] == x]['Type'].values[0]} | {filtered_df[filtered_df['ID'] == x]['Timestamp'].values[0]}"
                )
                
                st.dataframe(
                    filtered_df[["ID", "Filename", "Type", "Confidence", "Timestamp", "Status"]],
                    use_container_width=True,
                    hide_index=True
                )
                
            with col_details:
                st.subheader("Violation Details")
                if selected_id:
                    v_row = filtered_df[filtered_df["ID"] == selected_id].iloc[0]
                    
                    st.markdown(f"""
                        <div class='glass-card'>
                            <h4>Record #{v_row['ID']}</h4>
                            <p><b>File:</b> {v_row['Filename']}</p>
                            <p><b>Type:</b> {v_row['Type']}</p>
                            <p><b>Confidence:</b> {v_row['Confidence']:.2f}</p>
                            <p><b>Logged At:</b> {v_row['Timestamp']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display Screenshot
                    if os.path.exists(v_row["Screenshot"]):
                        st.image(v_row["Screenshot"], caption="Violation Screenshot Evidence", use_container_width=True)
                    else:
                        st.warning("Screenshot file not found on disk.")
                        
                    # Action Section
                    st.markdown("### Action Center")
                    new_status = st.selectbox(
                        "Change Status:",
                        options=["Pending", "Resolved", "Spurious"],
                        index=["Pending", "Resolved", "Spurious"].index(v_row["Status"])
                    )
                    
                    act_col1, act_col2 = st.columns(2)
                    with act_col1:
                        if st.button("Update Status", use_container_width=True):
                            update_violation_status(selected_id, new_status)
                            st.success(f"Status updated to {new_status}!")
                            st.rerun()
                    with act_col2:
                        if st.button("🚨 Delete Record", use_container_width=True):
                            # Remove screenshot if exists
                            if os.path.exists(v_row["Screenshot"]):
                                try:
                                    os.remove(v_row["Screenshot"])
                                except Exception:
                                    pass
                            delete_violation(selected_id)
                            st.success("Record deleted successfully!")
                            st.rerun()

# --- 4. ANALYTICS HUB ---
elif nav == "📊 Analytics Hub":
    st.markdown("<h1>Analytical Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Statistical visualization of violation records</p>", unsafe_allow_html=True)
    
    rows = get_all_violations()
    if not rows:
        st.info("No violations logged to generate charts.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Filename", "Type", "Confidence", "Timestamp", "Screenshot", "Status"])
        
        # Convert timestamp to datetime object
        df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
        df["Month"] = pd.to_datetime(df["Timestamp"]).dt.strftime('%Y-%m')
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Violation Type Distribution")
            fig_pie = px.pie(
                df, 
                names="Type", 
                hole=0.4,
                color="Type",
                color_discrete_map={"Garbage_Pile": "#3b82f6", "Smoke": "#f59e0b", "Fire": "#ef4444"}
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_c2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Resolution Status Breakdown")
            fig_status = px.bar(
                df.groupby("Status").size().reset_index(name="Count"),
                x="Status",
                y="Count",
                color="Status",
                color_discrete_map={"Pending": "#f59e0b", "Resolved": "#10b981", "Spurious": "#64748b"}
            )
            fig_status.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f8fafc",
                showlegend=False
            )
            st.plotly_chart(fig_status, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Daily Trend Chart
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Daily Violation Trends")
        daily_df = df.groupby(["Date", "Type"]).size().reset_index(name="Count")
        fig_trend = px.bar(
            daily_df,
            x="Date",
            y="Count",
            color="Type",
            barmode="group",
            color_discrete_map={"Garbage_Pile": "#3b82f6", "Smoke": "#f59e0b", "Fire": "#ef4444"}
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Monthly Trend Chart
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Monthly Violation Trends")
        monthly_df = df.groupby(["Month", "Type"]).size().reset_index(name="Count")
        fig_month = px.line(
            monthly_df,
            x="Month",
            y="Count",
            color="Type",
            markers=True,
            color_discrete_map={"Garbage_Pile": "#3b82f6", "Smoke": "#f59e0b", "Fire": "#ef4444"}
        )
        fig_month.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc"
        )
        st.plotly_chart(fig_month, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)