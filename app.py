import streamlit as st
import pandas as pd
import numpy as np
from persiantools.jdatetime import JalaliDate
import base64

st.set_page_config(page_title="تحلیل رقبا", layout="centered")

# استایل ظاهری
st.markdown("""
<style>
* {
    font-family: Tahoma, sans-serif !important;
}
html, body, [class*='css'] {
    background-color: #3a3a3a;
    color: #ffffff;
}
.stButton > button {
    color: white !important;
    background-color: #2563eb !important;
}
</style>
""", unsafe_allow_html=True)

st.image("logo.png", width=100)
st.markdown(f"تاریخ امروز: {JalaliDate.today().strftime('%Y/%m/%d')}")

# خوش‌آمدگویی
if "شروع" not in st.session_state:
    st.session_state["شروع"] = False

if not st.session_state["شروع"]:
    st.markdown("""
    ## خوش آمدید به نرم‌افزار تحلیل رقبا

    این نرم‌افزار به شما کمک می‌کند تا بر اساس شاخص‌های کلیدی رقابتی، جایگاه خود را در بازار نسبت به رقبا تحلیل کنید.

    ### شاخص‌ها شامل:
    - سهم بازار
    - قیمت‌گذاری
    - کیفیت محصول
    - رضایت مشتری
    - حضور دیجیتال
    - نوآوری و مزیت رقابتی
    - قدرت برند
    - پشتیبانی و پاسخ‌گویی

    تحلیل بر اساس وزن‌دهی استاندارد AHP و مقایسه امتیاز رقبا با برند شما انجام می‌شود.

    برای دریافت فایل نمونه:
    """)
    with open("نمونه_تحلیل_رقبا.xlsx", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="نمونه_تحلیل_رقبا.xlsx" style="color:#93c5fd;">دانلود فایل نمونه اکسل</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.markdown("توسعه‌یافته توسط شرکت <a href='https://inohub.ir' target='_blank'>اینوهاب</a>", unsafe_allow_html=True)
    if st.button("شروع تحلیل"):
        st.session_state["شروع"] = True
    st.stop()

st.title("تحلیل رقبا بر اساس شاخص‌های کلیدی")

uploaded_file = st.file_uploader("فایل اکسل رقبا را بارگذاری کنید", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("فایل با موفقیت بارگذاری شد.")
    st.dataframe(df)

    st.subheader("وزن‌دهی به شاخص‌ها بر اساس اهمیت (مقیاس ۱ تا ۱۰)")
    weights = {}
    columns = df.columns[1:]
    tabs = st.tabs(["وزن‌دهی شاخص‌ها"])
    with tabs[0]:
        for col in columns:
            weights[col] = st.slider(f"اهمیت {col}", 1, 10, 5)

    weight_array = np.array([weights[col] for col in columns])
    weight_array = weight_array / weight_array.sum()

    score_matrix = df[columns].values
    weighted_scores = np.dot(score_matrix, weight_array)
    df["امتیاز نهایی"] = weighted_scores.round(2)

    

    result = df.sort_values(by="امتیاز نهایی", ascending=False).reset_index(drop=True)
    result.index += 1
    st.dataframe(result)

    st.subheader("تحلیل جایگاه رقبا نسبت به برند شما:")
    base_score = df[df["نام رقیب/خودتان"] == "شرکت ما"]["امتیاز نهایی"].values[0]
    for _, row in df.iterrows():
        if row["نام رقیب/خودتان"] == "شرکت ما":
            continue
        delta = row["امتیاز نهایی"] - base_score
        if delta >= 1.5:
            level = "برتری مطلق"
        elif 0.5 <= delta < 1.5:
            level = "رقیب نزدیک"
        elif -0.5 <= delta < 0.5:
            level = "در حال رشد"
        elif -1.5 <= delta < -0.5:
            level = "ضعیف / خطر کم"
        else:
            level = "تهدید بالقوه"
        st.markdown(f"**{row['نام رقیب/خودتان']}**: {level} (امتیاز: {row['امتیاز نهایی']})")

    st.markdown("---")
    st.markdown("تمام حقوق این نرم‌افزار متعلق به شرکت <a href='https://inohub.ir' target='_blank'>اینوهاب</a> است.", unsafe_allow_html=True)
    st.image("logo.png", width=100)
