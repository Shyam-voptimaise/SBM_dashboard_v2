import streamlit as st
from PIL import Image
from datetime import datetime
import os
from config.config import TUNNELS
from utils.image_utils import get_latest_image, get_latest_images, get_all_annotations
from utils.metadata_utils import load_metadata, save_metadata
from utils.stats_utils import calculate_shift_stats
from reports.report_utils import collect_validation_data, generate_excel, generate_pdf

st.set_page_config(layout="wide")

st.sidebar.title("Operator")
op = st.sidebar.text_input("Name")
shift = st.sidebar.selectbox("Shift",["A","B","C"])

st.title("Special Bar Mill Defect Detection Dashboard")

cols = st.columns(2)

for col,(name,cfg) in zip(cols, TUNNELS.items()):
    with col:
        st.subheader(name)
        images = get_latest_images(cfg["image_dir"], count=2)
        if images:
            st.caption("Latest 2 coil images")
            img_cols = st.columns(len(images))
            for c,img in zip(img_cols, images):
                with c:
                    st.image(Image.open(img), width=600)
                    st.caption(f"Part image: {os.path.basename(img)}")

            st.divider()
            st.caption("Annotated defect images (by part)")
            for img in images:
                ann = get_all_annotations(cfg["annot_dir"], img)
                if ann:
                    st.markdown(f"**Annotations for {os.path.basename(img)}**")
                    ann_cols = st.columns(min(3,len(ann)))
                    for c,a in zip(ann_cols, ann):
                        with c:
                            st.image(Image.open(a),width=600)
                else:
                    st.markdown(f"*No annotated defects for {os.path.basename(img)}*)")

            # Use metadata based on latest image for decision save
            meta = load_metadata(images[0])
            decision = st.radio("Decision",["OK","Defect"], key=name)
            if st.button(f"Save {name}"):
                meta.update({"shift":shift,"decision":decision,"time":str(datetime.now())})
                save_metadata(images[0],meta)
        else:
            st.info("No images found in this tunnel image directory.")
            no_img_cols = st.columns(4)
            for c in no_img_cols:
                with c:
                    c.empty().info("No image")

st.divider()
st.subheader("Stats")
st.write(calculate_shift_stats(TUNNELS))

df = collect_validation_data(TUNNELS)
if st.button("Export Excel"):
    p = generate_excel(df)
    st.download_button("Download Excel", open(p,"rb"))
if st.button("Export PDF"):
    p = generate_pdf(df)
    st.download_button("Download PDF", open(p,"rb"))
