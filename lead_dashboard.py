import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import timedelta, datetime
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Mablle Lead Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #6B73FF 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .main-title {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.3rem;
        margin-top: 0.8rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .filter-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
    }
    
    .filter-title {
        color: #495057;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #6B73FF;
    }
    
    .section-header {
        background: linear-gradient(135deg, #6B73FF 0%, #9644F0 100%);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin: 2.5rem 0 1.5rem 0;
        font-size: 1.4rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(107, 115, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        top: 0;
        right: -10px;
        width: 100px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1));
        transform: skewX(-20deg);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        border-radius: 15px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        border-color: #6B73FF;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .priority-hot { 
        color: #dc3545; 
        font-weight: 700;
        background: rgba(220, 53, 69, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
    }
    .priority-medium { 
        color: #fd7e14; 
        font-weight: 700;
        background: rgba(253, 126, 20, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
    }
    .priority-cold { 
        color: #20c997; 
        font-weight: 700;
        background: rgba(32, 201, 151, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
    }
    
    .footer-section {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 10px 40px rgba(52, 152, 219, 0.3);
    }
    
    .action-button {
        background: linear-gradient(135deg, #6B73FF 0%, #9644F0 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(107, 115, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h2 class="main-title">🏡 Mablle Lead Prioritization Dashboard</h2>
    
</div>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
file_path = os.path.join(os.path.dirname(__file__), "leads.csv")

try:
    # Load data with correct column names
    df = pd.read_csv(file_path, parse_dates=["SubmittedDate", "DesiredStartDate"])
    
    # Map the actual columns to expected names
    column_mapping = {
        'Name': 'CustomerName',
        'Budget': 'Budget',
        'PropertyType': 'PropertyType', 
        'RenovationType': 'RenovationType',
        'SubmittedDate': 'SubmittedDate',
        'DesiredStartDate': 'DesiredStartDate'
    }
    
    # Rename columns if they exist in the mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Create LeadID if it doesn't exist
    if 'LeadID' not in df.columns:
        df['LeadID'] = ['LEAD' + str(i+1).zfill(4) for i in range(len(df))]
    
    # --- AUTO URGENCY SCORE BASED ON DATE DIFFERENCE ---
    def compute_urgency_score(submitted, desired):
        try:
            days_diff = (desired - submitted).days
            if days_diff <= 7:
                return 10
            elif days_diff <= 14:
                return 8
            elif days_diff <= 30:
                return 6
            elif days_diff <= 60:
                return 4
            else:
                return 2
        except:
            return 5  # Default score if calculation fails

    df["UrgencyScore"] = df.apply(lambda row: compute_urgency_score(row["SubmittedDate"], row["DesiredStartDate"]), axis=1)

    


    # --- ENHANCED LEAD SCORING ---
    def score_lead(row):
        score = 0
        # Budget scoring (40% weight)
        try:
            budget = float(row["Budget"])
            if budget >= 2000000:
                score += 4
            elif budget >= 1500000:
                score += 3
            elif budget >= 1000000:
                score += 2
            else:
                score += 1
        except:
            score += 1

        # Urgency scoring (30% weight)
        if row["UrgencyScore"] >= 9:
            score += 3
        elif row["UrgencyScore"] >= 6:
            score += 2
        else:
            score += 1

        # Renovation type scoring (20% weight)
        if "Full" in str(row["RenovationType"]):
            score += 2
        elif "Partial" in str(row["RenovationType"]):
            score += 1

        # Property type scoring (10% weight)
        if str(row["PropertyType"]) in ["Landed"]:
            score += 2
        elif str(row["PropertyType"]) in ["Condo"]:
            score += 1

        return score

    df["LeadScore"] = df.apply(score_lead, axis=1)
    df["Priority"] = df["LeadScore"].apply(
        lambda x: "🔥 Hot" if x >= 8 else ("⚠️ Medium" if x >= 6 else "❄️ Cold")
    )

    # --- RECOMMENDED FOLLOW-UP DATE ---
    df["FollowUpDate"] = df["SubmittedDate"] + timedelta(days=2)
    df["DaysToFollowUp"] = (df["FollowUpDate"] - pd.Timestamp.now()).dt.days

    # --- SIDEBAR FILTERS ---
    with st.sidebar:
        st.markdown("""
        <div class="filter-section">
            <div class="filter-title">🔍 Filter Dashboard</div>
        """, unsafe_allow_html=True)
        
        property_filter = st.multiselect(
            "🏠 Property Type", 
            options=df["PropertyType"].unique(), 
            default=list(df["PropertyType"].unique()),
            help="Filter leads by property type"
        )
        
        reno_filter = st.multiselect(
            "🔨 Renovation Type", 
            options=df["RenovationType"].unique(), 
            default=list(df["RenovationType"].unique()),
            help="Filter by renovation scope"
        )
        
        priority_filter = st.multiselect(
            "⚡ Priority Level", 
            options=df["Priority"].unique(), 
            default=list(df["Priority"].unique()),
            help="Filter by lead priority"
        )
        
        budget_min = int(df["Budget"].min())
        budget_max = int(df["Budget"].max())
        
        budget_range = st.slider(
            "💰 Budget Range (SGD)",
            min_value=budget_min,
            max_value=budget_max,
            value=(budget_min, budget_max),
            format="$%d",
            help="Filter by budget range"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df[
        (df["PropertyType"].isin(property_filter)) &
        (df["RenovationType"].isin(reno_filter)) &
        (df["Priority"].isin(priority_filter)) &
        (df["Budget"] >= budget_range[0]) &
        (df["Budget"] <= budget_range[1])
    ]

    # --- ENHANCED KPI SECTION ---
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_df)}</div>
            <div class="metric-label">Total Leads</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        hot_leads = filtered_df[filtered_df["Priority"] == "🔥 Hot"].shape[0]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{hot_leads}</div>
            <div class="metric-label">🔥 Hot Leads</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        medium_leads = filtered_df[filtered_df["Priority"] == "⚠️ Medium"].shape[0]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{medium_leads}</div>
            <div class="metric-label">⚠️ Medium Leads</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_budget = filtered_df['Budget'].mean() if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">S${avg_budget/1000:.0f}K</div>
            <div class="metric-label">Avg Budget</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        conversion_rate = (hot_leads / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{conversion_rate:.1f}%</div>
            <div class="metric-label">Hot Lead Rate</div>
        </div>
        """, unsafe_allow_html=True)

    # --- COMPREHENSIVE ANALYTICS SECTION ---
    st.markdown('<div class="section-header">📈 Comprehensive Lead Analytics</div>', unsafe_allow_html=True)
    
    # First row of charts
    # First row of charts (2 charts)
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Priority Distribution with custom colors
        priority_counts = filtered_df["Priority"].value_counts()
        fig_pie = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            title="Lead Priority Distribution",
            color_discrete_map={
                "🔥 Hot": "#FF6B6B",
                "⚠️ Medium": "#FFD93D", 
                "❄️ Cold": "#6BCF7F"
            }
        )
        fig_pie.update_layout(
            title_font_size=16,
            title_x=0.5,
            font=dict(size=12),
            height=400,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Property Type Distribution
        property_counts = filtered_df["PropertyType"].value_counts()
        fig_bar1 = px.bar(
            x=property_counts.index,
            y=property_counts.values,
            title="Leads by Property Type",
            color=property_counts.values,
            color_continuous_scale="Viridis"
        )
        fig_bar1.update_layout(
            title_font_size=16,
            title_x=0.5,
            font=dict(size=12),
            height=400,
            showlegend=False,
            xaxis_title="Property Type",
            yaxis_title="Number of Leads",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=50, l=50, r=20)
        )
        st.plotly_chart(fig_bar1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Second row (1 chart centered)
    chart_col3 = st.columns([1, 2, 1])[1]  # This centers the chart

    with chart_col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Renovation Type Distribution
        reno_counts = filtered_df["RenovationType"].value_counts()
        fig_bar2 = px.bar(
            x=reno_counts.values,
            y=reno_counts.index,
            orientation='h',
            title="Leads by Renovation Type",
            color=reno_counts.values,
            color_continuous_scale="Plasma"
        )
        fig_bar2.update_layout(
            title_font_size=16,
            title_x=0.5,
            font=dict(size=12),
            height=400,
            showlegend=False,
            xaxis_title="Number of Leads",
            yaxis_title="Renovation Type",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=50, l=150, r=20)
        )
        st.plotly_chart(fig_bar2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Second row of advanced charts
    chart_col4, chart_col5 = st.columns(2)
    
    with chart_col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Budget vs Lead Score Scatter Plot
        fig_scatter = px.scatter(
            filtered_df,
            x="Budget",
            y="LeadScore",
            color="Priority",
            size="UrgencyScore",
            hover_data=["CustomerName", "PropertyType"],
            title="<b>Budget vs Lead Score Analysis</b>",
            color_discrete_map={
                "🔥 Hot": "#FF6B6B",
                "⚠️ Medium": "#FFD93D", 
                "❄️ Cold": "#6BCF7F"
            }
        )
        fig_scatter.update_layout(
            title_font_size=14,
            title_x=0.5,
            font=dict(size=11),
            height=400,
            xaxis_title="Budget (SGD)",
            yaxis_title="Lead Score",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_scatter.update_xaxes(tickformat="$,.0f")
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with chart_col5:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Lead Score Distribution Histogram
        fig_hist = px.histogram(
            filtered_df,
            x="LeadScore",
            color="Priority",
            title="<b>Lead Score Distribution</b>",
            nbins=15,
            color_discrete_map={
                "🔥 Hot": "#FF6B6B",
                "⚠️ Medium": "#FFD93D", 
                "❄️ Cold": "#6BCF7F"
            }
        )
        fig_hist.update_layout(
            title_font_size=14,
            title_x=0.5,
            font=dict(size=11),
            height=400,
            xaxis_title="Lead Score",
            yaxis_title="Number of Leads",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Third row - Advanced Analytics
    chart_col6, chart_col7 = st.columns(2)
    
    with chart_col6:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Budget Distribution by Property Type (Box Plot)
        fig_box = px.box(
            filtered_df,
            x="PropertyType",
            y="Budget",
            color="PropertyType",
            title="<b>Budget by Property Type</b>"
        )
        fig_box.update_layout(
            title_font_size=14,
            title_x=0.5,
            font=dict(size=11),
            height=400,
            xaxis_title="Property Type",
            yaxis_title="Budget (SGD)",
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_box.update_yaxes(tickformat="$,.0f")
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_col7:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Urgency Score Distribution
        fig_urgency = px.bar(
            x=filtered_df["UrgencyScore"].value_counts().sort_index().index,
            y=filtered_df["UrgencyScore"].value_counts().sort_index().values,
            title="<b>Urgency Score Distribution</b>",
            color=filtered_df["UrgencyScore"].value_counts().sort_index().values,
            color_continuous_scale="Reds"
        )
        fig_urgency.update_layout(
            title_font_size=14,
            title_x=0.5,
            font=dict(size=11),
            height=400,
            xaxis_title="Urgency Score",
            yaxis_title="Number of Leads",
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_urgency, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PRIORITY LEADS TABLE ---
    st.markdown('<div class="section-header">🎯 High Priority Leads Requiring Immediate Action</div>', unsafe_allow_html=True)
    
    priority_leads = filtered_df[filtered_df["Priority"].isin(["🔥 Hot", "⚠️ Medium"])].sort_values(by="LeadScore", ascending=False)
    
    if len(priority_leads) > 0:
        styled_df = priority_leads[["LeadID", "CustomerName", "PropertyType", "RenovationType", "Budget", "Priority", "UrgencyScore", "FollowUpDate"]].copy()
        styled_df["Budget"] = styled_df["Budget"].apply(lambda x: f"S${x:,.0f}")
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "LeadID": "Lead ID",
                "CustomerName": "Customer Name",
                "PropertyType": "Property Type",
                "RenovationType": "Renovation Type",
                "Budget": "Budget (SGD)",
                "Priority": st.column_config.TextColumn("Priority", width="small"),
                "UrgencyScore": st.column_config.ProgressColumn("Urgency", min_value=0, max_value=10),
                "FollowUpDate": "Follow Up Date"
            }
        )
    else:
        st.success("🎉 No high-priority leads matching current filters!")

    # --- COMPLETE LEADS DATABASE ---
    st.markdown('<div class="section-header">📋 Complete Lead Database</div>', unsafe_allow_html=True)
    
    display_df = filtered_df.sort_values(by="LeadScore", ascending=False).copy()
    display_df["Budget_Display"] = display_df["Budget"].apply(lambda x: f"S${x:,.0f}")
    display_df["Follow_Up_Status"] = display_df["DaysToFollowUp"].apply(
        lambda x: "⚠️ Overdue" if x < 0 else ("🟡 Due Soon" if x <= 2 else "✅ On Track")
    )
    
    st.dataframe(
        display_df[["LeadID", "CustomerName", "PropertyType", "RenovationType", "Budget_Display", 
                   "Priority", "LeadScore", "UrgencyScore", "SubmittedDate", "DesiredStartDate", 
                   "FollowUpDate", "Follow_Up_Status"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "LeadID": "Lead ID",
            "CustomerName": "Customer Name",
            "PropertyType": "Property Type",
            "RenovationType": "Renovation Type",
            "Budget_Display": "Budget (SGD)",
            "Priority": st.column_config.TextColumn("Priority", width="small"),
            "LeadScore": st.column_config.ProgressColumn("Lead Score", min_value=0, max_value=12),
            "UrgencyScore": st.column_config.ProgressColumn("Urgency", min_value=0, max_value=10),
            "SubmittedDate": "Submitted Date",
            "DesiredStartDate": "Desired Start Date",
            "FollowUpDate": "Follow Up Date",
            "Follow_Up_Status": "Status"
        }
    )

    # --- EXPORT SECTION ---
    st.markdown('<div class="section-header">📥 Export & Action Center</div>', unsafe_allow_html=True)
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        st.download_button(
            label="📥 All Filtered Leads",
            data=filtered_df.to_csv(index=False),
            file_name=f"mablle_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with action_col2:
        hot_leads_df = filtered_df[filtered_df["Priority"] == "🔥 Hot"]
        st.download_button(
            label="🔥 Hot Leads Only",
            data=hot_leads_df.to_csv(index=False),
            file_name=f"mablle_hot_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with action_col3:
        overdue_leads = filtered_df[filtered_df["DaysToFollowUp"] < 0]
        st.download_button(
            label="⚠️ Overdue Follow-ups",
            data=overdue_leads.to_csv(index=False),
            file_name=f"mablle_overdue_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with action_col4:
        high_budget_leads = filtered_df[filtered_df["Budget"] >= 1500000]
        st.download_button(
            label="💎 Premium Leads (>1.5M)",
            data=high_budget_leads.to_csv(index=False),
            file_name=f"mablle_premium_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

    # --- FOOTER ---
    # st.markdown("""
    # <div class="footer-section">
    #     <h2>🏆 Mablle Interior Design</h2>
    #     <h4>Singapore's Premier Interior Solutions</h4>
    #     <p>Transforming spaces, creating dreams • Dashboard last updated: {}</p>
    #     <p>📞 Contact: +65 1234-5678 | 📧 info@mablle.sg | 🌐 www.mablle.sg</p>
    # </div>
    # """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ 'leads.csv' not found in the current directory.")
    st.info("📁 Please ensure the leads.csv file is in the same directory as this dashboard.")
    st.code("""
    Expected CSV format:
    Name,Budget,PropertyType,RenovationType,SubmittedDate,DesiredStartDate
    John Doe,1500000,Condo,Full Renovation,2025-08-20,2025-09-10
    """)
