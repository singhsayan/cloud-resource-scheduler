import streamlit as st
from services import aws_service, azure_service
from config import settings

st.set_page_config(page_title="Cloud Cost Optimizer", layout="wide")

st.title(" Cloud Cost Management Dashboard")

aws_cost = aws_service.get_cost_summary()
azure_cost = azure_service.get_cost_summary()
total_cost = aws_cost + azure_cost

st.metric("Total Cloud Cost (Monthly)", f"${total_cost:,.2f}")

c1, c2 = st.columns(2)
c1.metric("AWS Cost", f"${aws_cost:,.2f}")
c2.metric("Azure Cost", f"${azure_cost:,.2f}")

st.write("---")
st.subheader("Project Info")
st.write("Use the left sidebar pages for details →")