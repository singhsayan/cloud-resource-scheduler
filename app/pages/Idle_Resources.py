import streamlit as st
from services import aws_service, azure_service

st.title("Idle / Underutilized Resources")

aws_idle = aws_service.list_idle_resources()
az_idle  = azure_service.list_idle_resources()

c1, c2 = st.columns(2)
with c1:
    st.subheader("AWS")
    if aws_idle:
        for item in aws_idle:
            st.write("•", item)
    else:
        st.success("No idle resources detected on AWS!")

with c2:
    st.subheader("Azure")
    if az_idle:
        for item in az_idle:
            st.write("•", item)
    else:
        st.success("No idle resources detected on Azure!")

st.info("Tip: In LIVE mode, this page can check stopped/idle VMs, unattached disks/volumes, stale load balancers, etc.")