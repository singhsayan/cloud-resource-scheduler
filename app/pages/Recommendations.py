import streamlit as st
from services import aws_service, azure_service, analyzer

st.title("FinOps Recommendations")

aws_cost = aws_service.get_cost_summary()
az_cost  = azure_service.get_cost_summary()
recs = analyzer.generate_recommendations({"aws": aws_cost, "azure": az_cost})

st.metric("AWS Cost (Monthly)", f"${aws_cost:,.2f}")
st.metric("Azure Cost (Monthly)", f"${az_cost:,.2f}")

st.write("---")
st.subheader("Recommendations")
for r in recs:
    st.write("•", r)
