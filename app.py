import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Bullwhip Effect Simulator | The Value Stack", layout="wide")

# Title & Context
st.title("🌊 The Bullwhip Effect Simulator")
st.markdown("""
### From a Whisper to a Scream: Visualizing Information Distortion.
*Insights by Igor Cancarevic*

The Bullwhip Effect occurs when small fluctuations in demand at the retail level create progressively larger waves of inventory up the supply chain. This simulator calculates how much **Capital** is trapped because of these information gaps.
""")

st.sidebar.header("📊 Simulation Inputs")

with st.sidebar:
    st.subheader("1. Financial Context")
    unit_price = st.number_input("Value per Unit (€)", value=100.0, step=10.0, 
                                 help="The cost or market value of a single unit of your product.")
    
    st.subheader("2. Demand Trigger")
    base_demand = st.slider("Base Customer Demand (Units)", 50, 1000, 200)
    demand_spike = st.slider("Customer Demand Increase (%)", 0, 50, 10)
    
    st.subheader("3. The Panic Factor")
    safety_buffer = st.slider("Safety Stock Buffer (%)", 0, 50, 15, 
                             help="The 'just-in-case' margin each stage adds to their orders.")

# --- THE LOGIC ---
stages = ["Customer", "Pharmacy", "Wholesaler", "Distributor", "Factory"]
current_demand = base_demand * (1 + (demand_spike / 100))

# Baseline (Normal State)
baseline_values = [base_demand] * len(stages)

# Amplified State (The Wave)
amplified_values = [current_demand]
temp_val = current_demand
for i in range(len(stages) - 1):
    temp_val = temp_val * (1 + (safety_buffer / 100))
    amplified_values.append(temp_val)

# Financial Calculations
total_excess_inventory = sum(amplified_values) - sum(baseline_values)
trapped_capital = total_excess_inventory * unit_price

# --- VISUALIZATION ---

fig = go.Figure()

# Normal Baseline
fig.add_trace(go.Scatter(x=stages, y=baseline_values, name='Steady State',
                         line=dict(color='#bdc3c7', width=2, dash='dash')))

# The Bullwhip Wave
fig.add_trace(go.Scatter(x=stages, y=amplified_values, name='Amplified Orders',
                         line=dict(color='#e74c3c', width=5),
                         mode='lines+markers'))

fig.update_layout(
    title="Demand Amplification Up the Chain",
    xaxis_title="Supply Chain Stages",
    yaxis_title="Units Ordered",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# --- FINANCIAL SUMMARY ---

c1, c2 = st.columns(2)

with c1:
    st.error(f"### 📈 Total Over-Ordering: {int(total_excess_inventory)} units")
    st.write(f"""
    A small **{demand_spike}%** change at the customer level has caused the factory 
    to produce **{((amplified_values[-1]/base_demand)-1)*100:.1f}%** more than needed.
    """)

with c2:
    st.warning(f"### 💸 Trapped Capital: €{trapped_capital:,.2f}")
    st.write(f"""
    This is the total value of inventory that is 'frozen' in the chain. 
    By the time the signal reaches the factory, bad data has turned into **dead capital**.
    """)

st.divider()

# --- THE MATH SECTION ---
with st.expander("📝 The Economic Logic (Formulas)"):
    st.write("The Bullwhip Effect is a consequence of serial decision-making without real-time data transparency.")
    
    st.latex(r"Order_{n} = Order_{n-1} \times (1 + \text{Buffer}\%)")
    
    st.markdown("---")
    st.subheader("Calculating Trapped Capital")
    st.write("We calculate the delta between the steady-state demand and the amplified orders at every node, multiplied by your Unit Price.")
    st.latex(r"\text{Trapped Capital} = \sum_{stage=1}^{n} (Units_{amplified} - Units_{baseline}) \times \text{Unit Price}")
    
    st.info("💡 **Strategy:** To fix this, you don't need a bigger warehouse. You need an API. If the Factory can see the Customer data directly, the buffer reduces to near zero.")
