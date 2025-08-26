import streamlit as st
import pandas as pd
from services import aws_service, azure_service
from config import settings

st.title("Cost Dashboard")

# st.caption(f"Mode: {'MOCK' if settings.USE_MOCK_DATA else 'LIVE'}")

with st.spinner("Loading cost breakdown..."):
    aws_df = aws_service.get_cost_breakdown()
    az_df  = azure_service.get_cost_breakdown()  # still mock

tab1, tab2, tab3 = st.tabs(["Summary", "AWS", "Azure"])

with tab1:
    st.subheader("Combined Monthly Cost by Service")
    combined = pd.concat([
        aws_df.assign(provider="AWS"),
        az_df.assign(provider="Azure")
    ], ignore_index=True)
    st.dataframe(combined)
    st.bar_chart(
        combined.pivot_table(
            index="service", columns="provider", values="cost", aggfunc="sum"
        ).fillna(0)
    )

with tab2:
    st.subheader("AWS Cost by Service / Region")
    st.dataframe(aws_df)

    st.bar_chart(aws_df.groupby("service")["cost"].sum())

    daily = aws_df.groupby("date")["cost"].sum()
    st.line_chart(daily)

    monthly = aws_df.groupby("month")["cost"].sum()
    st.bar_chart(monthly)

with tab3:
    st.subheader("Azure Cost by Service / Region")
    st.dataframe(az_df)
    st.bar_chart(az_df.set_index("service")["cost"])
    st.line_chart(az_df.pivot_table(index="month", values="cost", aggfunc="sum"))
