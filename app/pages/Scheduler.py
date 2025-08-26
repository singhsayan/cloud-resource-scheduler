import streamlit as st
from utils import scheduler

st.title("Auto Scheduling (Dev/Test Off-hours)")

st.caption("Define rules to stop/start non-prod resources during off-hours to save cost.")

with st.form("sched_form"):
    env = st.selectbox("Environment", ["dev", "test", "staging"])
    provider = st.selectbox("Cloud", ["AWS", "Azure"])
    action = st.selectbox("Action", ["stop", "start"])
    timezone = st.text_input("Timezone", value="UTC")
    cron = st.text_input("Cron Expression", value="0 20 * * 1-5")  # 20:00 Mon-Fri
    enabled = st.checkbox("Enabled", value=True)

    submitted = st.form_submit_button("Save Rule")
    if submitted:
        rule_id = scheduler.save_rule({
            "env": env,
            "provider": provider,
            "action": action,
            "timezone": timezone,
            "cron": cron,
            "enabled": enabled
        })
        st.success(f"Saved rule with id: {rule_id}")

st.write("---")
st.subheader("Existing Rules")
rules = scheduler.list_rules()
if not rules:
    st.info("No rules defined yet.")
else:
    for r in rules:
        st.write(f"• [{r['id']}] {r['provider']} {r['env']} → {r['action']} @ {r['cron']} ({'on' if r['enabled'] else 'off'})")
        col1, col2, col3 = st.columns(3)
        if col1.button("Toggle", key=f"toggle_{r['id']}"):
            scheduler.toggle_rule(r["id"])
            st.rerun()
        if col2.button("Run Now", key=f"run_{r['id']}"):
            scheduler.run_rule_now(r["id"])
            st.success("Triggered.")
        if col3.button("Delete", key=f"del_{r['id']}"):
            scheduler.delete_rule(r["id"])
            st.warning("Deleted.")
            st.rerun()