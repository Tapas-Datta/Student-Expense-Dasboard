import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration for a Premium Look
st.set_page_config(
    page_title='Advanced International Student Expense Intelligence.',
    layout='wide',
    initial_sidebar_state='expanded',
)
st.title('🌏 Advanced Student Expense Comparison & Savings Intelligence')
st.markdown(
    'Welcome to the next-gen student data analysis platform. Compare expenses, simulate part-time income, and analyze budget safety.'
)

# YOUR EXPERIENCED LINE EXTRACTED INTO A NEW PROFESSIONAL NOTE HERE
st.markdown(
    "💡 **Tapas's Note:** Having personally lived and studied in both Australia and Europe, the datasets and insights presented in this dashboard are grounded in real-world observations and firsthand financial tracking."
)
st.markdown('---')

# 1. Core Dataset (Updated Food & Groceries: Australia=200, Europe=100, USA=150)
expense_data = {
    'Expense Category': [
        'Accommodation',
        'Food & Groceries',
        'Tuition Fees (Avg)',
        'Public Transport',
        'Entertainment',
        'Accommodation',
        'Food & Groceries',
        'Tuition Fees (Avg)',
        'Public Transport',
        'Entertainment',
        'Accommodation',
        'Food & Groceries',
        'Tuition Fees (Avg)',
        'Public Transport',
        'Entertainment',
    ],
    'Region': [
        'Australia',
        'Australia',
        'Australia',
        'Australia',
        'Australia',
        'Europe',
        'Europe',
        'Europe',
        'Europe',
        'Europe',
        'USA',
        'USA',
        'USA',
        'USA',
        'USA',
    ],
    'Monthly Cost (USD)': [
        700,
        200,
        1500,
        150,
        250,  # Australia Total: 2800
        400,
        100,
        800,
        90,
        200,  # Europe Total: 1590
        850,
        150,
        1000,
        100,
        140,  # USA Total: 2240
    ],
}
df = pd.DataFrame(expense_data)

# Adding Calculated Columns for Advanced View
df['Daily Cost (USD)'] = round(df['Monthly Cost (USD)'] / 30, 2)

# 2. Sidebar Advanced Controls
st.sidebar.header('⚙️ Dashboard Intelligence Controls')
selected_regions = st.sidebar.multiselect(
    'Select Regions to Compare:',
    options=df['Region'].unique(),
    default=['Australia', 'Europe', 'USA'],
)

# Dynamic Budget Check
st.sidebar.markdown('---')
st.sidebar.subheader('💰 Budget Configuration')
user_budget = st.sidebar.number_input(
    'Your Monthly Budget ($ USD):', min_value=100, value=2500, step=50
)

# Part-time Job Simulation
st.sidebar.markdown('---')
st.sidebar.subheader('💼 Part-time Job Simulation')
simulate_income = st.sidebar.checkbox('Add Part-time Monthly Income?')
part_time_earnings = 0
if simulate_income:
    part_time_earnings = st.sidebar.slider(
        'Estimated Monthly Earnings ($ USD):',
        min_value=0,
        max_value=2000,
        value=800,
        step=50,
    )

df_filtered = df[df['Region'].isin(selected_regions)]

# 3. Main Dashboard: KPI Metric Layer with Savings Intelligence
if not df_filtered.empty:
    kpi_cols = st.columns(len(selected_regions))

    for i, region in enumerate(selected_regions):
        total_cost = df_filtered[df_filtered['Region'] == region][
            'Monthly Cost (USD)'
        ].sum()
        net_financials = user_budget + part_time_earnings - total_cost

        with kpi_cols[i]:
            st.metric(
                label=f'Total Cost ({region})', value=f"${total_cost:,} USD"
            )
            if net_financials >= 0:
                st.success(
                    f"✅ Safe! Potential Savings: ${net_financials:,} USD"
                )
            else:
                st.error(f"⚠️ Deficit! Short by: ${abs(net_financials):,} USD")

    st.markdown('---')

    # 4. Data Layout Matrix
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('📋 Detailed Searchable Breakdown')
        pivot_df = df_filtered.pivot(
            index='Expense Category',
            columns='Region',
            values='Monthly Cost (USD)',
        )
        st.dataframe(pivot_df, use_container_width=True)

        # Download Report Feature
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='📥 Download Advanced Cost Report (CSV)',
            data=csv,
            file_name='advanced_student_expense_report.csv',
            mime='text/csv',
        )

        # Pie Chart Section
        st.markdown('---')
        st.subheader('🍕 Expense Share Analysis')
        pie_region = st.selectbox(
            'Select Region for Share Breakdown:', options=selected_regions
        )
        pie_df = df_filtered[df_filtered['Region'] == pie_region]
        fig_pie = px.pie(
            pie_df,
            values='Monthly Cost (USD)',
            names='Expense Category',
            title=f'Cost Share Distribution in {pie_region}',
            hole=0.4,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader('📊 Expense Group Comparison (Monthly)')
        fig_bar = px.bar(
            df_filtered,
            x='Expense Category',
            y='Monthly Cost (USD)',
            color='Region',
            barmode='group',
            text_auto=True,
            color_discrete_map={
                'Australia': '#FF4B4B',
                'Europe': '#1C83E1',
                'USA': '#2CA02C',
            },
        )
        fig_bar.update_layout(
            yaxis_title='Monthly Cost ($ USD)', xaxis_title=''
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Daily Cost Analytical View
        st.markdown('---')
        st.subheader('⏱️ Estimated Daily Cost Distribution')
        fig_scatter = px.scatter(
            df_filtered,
            x='Expense Category',
            y='Daily Cost (USD)',
            color='Region',
            size='Daily Cost (USD)',
            title='Daily Micro-Expenses Comparison',
            color_discrete_map={
                'Australia': '#FF4B4B',
                'Europe': '#1C83E1',
                'USA': '#2CA02C',
            },
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.warning('Please select at least one region from the sidebar.')
