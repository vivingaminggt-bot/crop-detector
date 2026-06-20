import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile, os
from detector import detect_disease, save_result

# ── Page config ───────────────────────────────────
st.set_page_config(
    page_title = "🌾 Crop Disease Detector",
    page_icon  = "🌿",
    layout     = "wide"
)
st.title("🌾 AI Crop Disease Detector")
st.write("Upload a crop leaf image to identify the plant and health status.")

# ── Sidebar ───────────────────────────────────────
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to:", ["🔍 Detect", "📊 EDA Dashboard"])

# ════════════════════════════════════════════════
# PAGE 1 — DETECT
# ════════════════════════════════════════════════
if page == "🔍 Detect":
    uploaded = st.file_uploader(
        "📸 Upload crop/leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:
        st.image(uploaded, caption="Uploaded Image", width=300)

        if st.button("🔍 Analyze Crop"):
            # save temp file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".jpg"
            ) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name

            with st.spinner("🌿 Analyzing... please wait"):
                result = detect_disease(tmp_path)

            os.unlink(tmp_path)   # delete temp file

            if result:
                st.success("✅ Analysis Complete!")

                col1, col2, col3 = st.columns(3)
                col1.metric("🌱 Plant",      result["plant_name"])
                col2.metric("📊 Confidence", f"{result['confidence']}%")
                col3.metric("🔬 Family",     result["family"])

                st.info(f"**Scientific Name:** {result['scientific']}")

                status = "Healthy ✅" if result["confidence"] > 70 \
                         else "Needs Attention ⚠️"
                st.warning(f"**Crop Status:** {status}")

                save_result(uploaded.name, result)
                st.success("💾 Result saved to database!")
            else:
                st.error("❌ Could not analyze. Try another image.")

# ════════════════════════════════════════════════
# PAGE 2 — EDA DASHBOARD
# ════════════════════════════════════════════════
elif page == "📊 EDA Dashboard":
    st.subheader("📊 Exploratory Data Analysis")

    try:
        df = pd.read_csv("crop_results.csv")

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Analyzed",  len(df))
        col2.metric("Unique Plants",   df['plant_name'].nunique())
        col3.metric("Avg Confidence",  f"{df['confidence'].mean():.1f}%")
        col4.metric("Healthy Crops",
                    len(df[df['status'] == 'Healthy']))

        # Data table
        st.subheader("📋 Raw Data")
        st.dataframe(df)

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🥧 Health Status")
            fig, ax = plt.subplots()
            df['status'].value_counts().plot.pie(
                autopct='%1.1f%%',
                colors=['#2ecc71', '#f39c12'],
                ax=ax
            )
            ax.set_ylabel("")
            st.pyplot(fig)

        with col2:
            st.subheader("🌿 Top Plants Detected")
            fig, ax = plt.subplots()
            df['plant_name'].value_counts().head(5).plot(
                kind='bar', color='#3498db', ax=ax
            )
            ax.set_xlabel("")
            plt.xticks(rotation=30)
            st.pyplot(fig)

        st.subheader("📈 Confidence Distribution")
        fig, ax = plt.subplots(figsize=(8, 3))
        sns.histplot(df['confidence'], bins=10,
                     color='#9b59b6', kde=True, ax=ax)
        st.pyplot(fig)

    except FileNotFoundError:
        st.warning("⚠️ No data yet! Go to 🔍 Detect and analyze some crops first.")