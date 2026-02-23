import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Bullwhip Effect Simulator | The Value Stack", layout="wide")

st.title("🌊 The Bullwhip Effect Simulator")
st.markdown("""
### Watch a small ripple turn into a tsunami.
*Insights by Igor Čančarević*

This tool simulates how a small change in consumer demand amplifies as it moves from the Pharmacy to the Factory. 
""")

st.sidebar.header("📊 Simulation Settings")

with st.sidebar:
    st.subheader("The Demand Trigger")
    base_demand = st.slider("Base Customer Demand (Units)", 50, 500, 100)
    demand_spike = st.slider("Demand Increase (%)", 0, 50, 10)
    
    st.subheader("The 'Panic' Factor")
    safety_buffer = st.slider("Safety Stock Buffer (%)", 0, 50, 20, 
                             help="How much extra each stage orders 'just in case'.")

# 1. The Logic: Amplification through 4 stages
stages = ["Customer", "Pharmacy", "Wholesaler", "Distributor", "Factory"]
demand_values = []

current_demand = base_demand * (1 + (demand_spike / 100))
demand_values.append(base_demand) # Start with base for the "Before" view

# Simulate amplification
val = current_demand
results = [base_demand] # The "Normal" state
amplified_results = [current_demand]

for i in range(len(stages) - 1):
    val = val * (1 + (safety_buffer / 100))
    amplified_results.append(val)
    results.append(base_demand) # Keep baseline flat for comparison

# 2. Financial Impact
total_excess_inventory = sum(amplified_results) - sum(results)
holding_cost_per_unit = 5.0 # Estimated cost
trapped_capital = total_excess_inventory * holding_cost_per_unit

# 3. Visualization
fig = go.Figure()

# Baseline
fig.add_trace(go.Scatter(x=stages, y=results, name='Normal Demand',
                         line=dict(color='gray', width=2, dash='dash')))

# Amplified Wave
fig.add_trace(go.Scatter(x=stages, y=amplified_results, name='Amplified Orders',
                         line=dict(color='#1f77b4', width=4),
                         mode='lines+markers'))

fig.update_layout(title="Order Amplification Up the Supply Chain",
                  xaxis_title="Supply Chain Stage",
                  yaxis_title="Units Ordered",
                  hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

# 4. Economic Summary
c1, c2 = st.columns(2)

with c1:
    st.error(f"### 📈 Total Over-Ordering: {int(total_excess_inventory)} units")
    st.write(f"""
    Because of a **{demand_spike}%** increase in customer demand, the Factory is now 
    producing **{((amplified_results[-1]/base_demand)-1)*100:.0f}%** more than normal.
    """)

with c2:
    st.warning(f"### 💸 Trapped Capital: €{trapped_capital:,.2f}")
    st.write(f"""
    This is the estimated cost of holding excess inventory across the chain. 
    This money is 'frozen' because the data at the factory is disconnected from the customer.
    """)

st.divider()

# 5. The Formula Section
with st.expander("📝 The Math of the 'Whip'"):
    st.write("The amplification is often modeled as a compounding variance. In this simple version:")
    st.latex(r"Order_{stage} = Order_{previous} \times (1 + \text{Buffer}\%)")
    st.write("In reality, the Bullwhip Effect is driven by the **Variance Amplification (VAM)**:")
    st.latex(r"VAM = \frac{\sigma^2_{orders}}{\sigma^2_{demand}}")
    st.info("When VAM > 1, you have a bullwhip effect. The goal of Data Engineering (EDI, Real-time APIs) is to bring VAM as close to 1 as possible.")
