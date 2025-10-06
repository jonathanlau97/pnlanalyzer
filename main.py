import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(page_title="P&L Profitability Analyzer", layout="wide", initial_sidebar_state="expanded")

# GL Code Mapping with Categories
GL_CODE_MAPPING = {
    # Revenue Categories
    '41110': {'name': 'Scheduled Flight', 'category': 'Flight Revenue', 'type': 'Revenue'},
    '41116': {'name': 'Revenue - Loyalty Point Redemption', 'category': 'Flight Revenue', 'type': 'Revenue'},
    '41150': {'name': 'Refund and Chargeback', 'category': 'Flight Revenue', 'type': 'Revenue'},
    '41151': {'name': 'Refund', 'category': 'Flight Revenue', 'type': 'Revenue'},
    '4160C': {'name': 'Travel, Lifestyle and Shopping', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41641': {'name': 'Commission', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41643': {'name': 'Gross Billing - Merchandise', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41648': {'name': 'Inflight Shopping Commission', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41654': {'name': 'Gross Billing - Discount Pass', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41658': {'name': 'Advertising and Partnerships', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41649': {'name': 'Inflight Shopping Merchant Fees', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41651': {'name': 'Refund', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41675': {'name': 'Revenue - Discount', 'category': 'Non-Airline Direct Revenue', 'type': 'Revenue'},
    '41332': {'name': 'Revenue - Inflight Duty Free Onboard', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '41321': {'name': 'Revenue - Inflight Merchandise Pre-book', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '41322': {'name': 'Revenue - Inflight Merchandise Onboard', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '41331': {'name': 'Revenue - Inflight Duty Free Pre-book', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '41264': {'name': 'Revenue - Service Fees', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '42114': {'name': 'Advertising - Publication', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '41801': {'name': 'Management Fee', 'category': 'Non-Inflight Revenues', 'type': 'Revenue'},
    '45130': {'name': 'Gain / (Loss) on Disposal', 'category': 'Other Income', 'type': 'Revenue'},
    '45132': {'name': 'Other Income - Gain/(Loss) on Asset Disposal', 'category': 'Other Income', 'type': 'Revenue'},
    '45150': {'name': 'Others', 'category': 'Other Income', 'type': 'Revenue'},
    '45199': {'name': 'Other Income - Others', 'category': 'Other Income', 'type': 'Revenue'},
    
    # Cost of Sales
    '51711': {'name': 'Credit Card Commission', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51621': {'name': 'Inflight Merchandise', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51631': {'name': 'Duty Free', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51664': {'name': 'Merchandise', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51717': {'name': 'Commission paid to Partner', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51718': {'name': 'Payment Gateway Fee', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51719': {'name': 'Commission to AA.Com', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51726': {'name': 'Collection Shortage', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51749': {'name': 'Other Distribution Cost', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51754': {'name': 'Merchant Fee', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51256': {'name': 'Travelling - Others', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51536': {'name': 'Freight Charges', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51610': {'name': 'Inflight Meal and Beverage', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51615': {'name': 'Inflight Amenities', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51640': {'name': 'Other Inflight Cost', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51648': {'name': 'Other Operating Cost - Inflight', 'category': 'Sales And Distribution', 'type': 'COGS'},
    '51912': {'name': 'COS - First Mile/Last Mile', 'category': 'Other Cost Of Sales', 'type': 'COGS'},
    '51913': {'name': 'COS - Teleportal', 'category': 'Other Cost Of Sales', 'type': 'COGS'},
    '51942': {'name': 'Online Advertising Cost', 'category': 'Other Cost Of Sales', 'type': 'COGS'},
    '51966': {'name': 'Point of Issuing Cost', 'category': 'Other Cost Of Sales', 'type': 'COGS'},
    
    # Operating Expenses - Direct Payroll
    '51211': {'name': 'Basic Salary', 'category': 'Direct Payroll', 'type': 'OPEX'},
    '51215': {'name': 'Allowance - Others', 'category': 'Direct Payroll', 'type': 'OPEX'},
    '51218': {'name': 'Provident Fund - Employer', 'category': 'Direct Payroll', 'type': 'OPEX'},
    '51219': {'name': 'Social Security Fund - Employer', 'category': 'Direct Payroll', 'type': 'OPEX'},
    '51251': {'name': 'Human Resource Development Fund (HRDF)', 'category': 'Direct Payroll', 'type': 'OPEX'},
    '51257': {'name': 'Accommodation - Hotels', 'category': 'Direct Payroll', 'type': 'OPEX'},
    
    # Operating Expenses - Indirect Payroll
    '61111': {'name': 'Basic Salary', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61113': {'name': 'Bonus', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61114': {'name': 'Allowance', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61116': {'name': 'Medical Expenses', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61117': {'name': 'Provident Fund - Employer', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61118': {'name': 'Social Security Fund - Employer', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61149': {'name': 'Other Payroll Cost', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61151': {'name': 'Human Resource Development Fund (HRDF)', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61152': {'name': 'Housing Fund Contribution', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61153': {'name': 'Training', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61154': {'name': 'Uniform & Accessories', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61155': {'name': 'Travelling - Air Ticket / Other Transport', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61156': {'name': 'Travelling - Others', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61157': {'name': 'Accommodation', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61160': {'name': 'Recruitment Expenses', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    '61189': {'name': 'Other Personnel Cost', 'category': 'Indirect Payroll', 'type': 'OPEX'},
    
    # Marketing & Advertising
    '61211': {'name': 'Advertising - Outdoor', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61213': {'name': 'Advertising - Radio', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61215': {'name': 'Advertising - Internet', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61218': {'name': 'Point Of Display', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61219': {'name': 'Design/Production', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61220': {'name': 'Events and Fairs', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61221': {'name': 'Gift - General', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61223': {'name': 'Sponsorship', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61226': {'name': 'Special Projects', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61227': {'name': 'Photography', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61228': {'name': 'License Fee', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61229': {'name': 'Web Transaction Fees', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61230': {'name': 'Communication Materials', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61232': {'name': 'Merchandise Consumption', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61233': {'name': 'Loyalty Cost', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61237': {'name': 'Regional Special Project', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61239': {'name': 'Advertising - Always On Digital (MKT)', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61240': {'name': 'Marketing Incentive', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61241': {'name': 'Partnership Funds Spending', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    '61249': {'name': 'Other Advertising Cost', 'category': 'Marketing & Advertising', 'type': 'OPEX'},
    
    # Insurance & Fees
    '61311': {'name': 'Group Hospitalisation', 'category': 'Insurance', 'type': 'OPEX'},
    '61312': {'name': 'Group Term Life', 'category': 'Insurance', 'type': 'OPEX'},
    '61313': {'name': 'Group Personal Accident', 'category': 'Insurance', 'type': 'OPEX'},
    '61349': {'name': 'Other Insurance Cost', 'category': 'Insurance', 'type': 'OPEX'},
    '61411': {'name': 'Management Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61412': {'name': 'Audit Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61413': {'name': 'Professional Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61415': {'name': 'Secretarial Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61419': {'name': 'Consultant Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61420': {'name': 'Stamping Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61421': {'name': 'Tax Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61422': {'name': 'Fines / Penalties', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61423': {'name': 'Brand License Cost', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61425': {'name': 'AASEA Service Cost', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61426': {'name': 'ICT Shared Service Cost', 'category': 'Professional Fees', 'type': 'OPEX'},
    '61449': {'name': 'Other Fees', 'category': 'Professional Fees', 'type': 'OPEX'},
    
    # General & Administrative
    '61511': {'name': 'Printing', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61512': {'name': 'Stationeries and Office Supplies', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61513': {'name': 'Telephone and Faxes', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61514': {'name': 'Utility', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61515': {'name': 'Postage & Courier', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61516': {'name': 'Entertainment - Staff', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61517': {'name': 'Entertainment - Business', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61522': {'name': 'Rental - Warehouse', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61526': {'name': 'Maintainance - Others', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61527': {'name': 'Refreshments', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61532': {'name': 'Staff Welfare', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61535': {'name': 'Maintenance - Office Equipment', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61549': {'name': 'Other Office Expenses', 'category': 'General & Administrative', 'type': 'OPEX'},
    '61552': {'name': 'Communication Service - Internet Access Fee', 'category': 'IT Expenses', 'type': 'OPEX'},
    '61554': {'name': 'Hosted System', 'category': 'IT Expenses', 'type': 'OPEX'},
    '61556': {'name': 'Maintenance - Computer Software', 'category': 'IT Expenses', 'type': 'OPEX'},
    '61557': {'name': 'License Fee - Computer Software', 'category': 'IT Expenses', 'type': 'OPEX'},
    '61558': {'name': 'Web Services', 'category': 'IT Expenses', 'type': 'OPEX'},
    '61569': {'name': 'Other IT Expenses', 'category': 'IT Expenses', 'type': 'OPEX'},
    
    # Other Operating Expenses
    '61713': {'name': 'FA Expensed Off', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '61714': {'name': 'Provision for Doubtful Debts', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '61716': {'name': 'Provision for Impairment PPE', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '61720': {'name': 'AEP Expenses', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '61724': {'name': 'Rounding Account', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '61727': {'name': 'Bad Debts Written Off', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '61725': {'name': 'Imported Service Tax Expense', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    '617A6': {'name': 'Provision for Impairment of Investment', 'category': 'Other Operating Expenses', 'type': 'OPEX'},
    
    # Depreciation & Amortization
    '61629': {'name': 'Depreciation - Computer Hardware', 'category': 'Depreciation & Amortization', 'type': 'D&A'},
    '61630': {'name': 'Depreciation - Computer Software', 'category': 'Depreciation & Amortization', 'type': 'D&A'},
    '61685': {'name': 'Amortisation - Intangibles', 'category': 'Depreciation & Amortization', 'type': 'D&A'},
    
    # Interest & Financial
    '71111': {'name': 'Interest Income - Bank Interest', 'category': 'Interest Income', 'type': 'Interest'},
    '71121': {'name': 'Term Loan Interest', 'category': 'Interest Expense', 'type': 'Interest'},
    '71130': {'name': 'Lease Interest - IFRS 16', 'category': 'Interest Expense', 'type': 'Interest'},
    '71141': {'name': 'Bank Charges', 'category': 'Financial Charges', 'type': 'Interest'},
    '71142': {'name': 'Bank Guarantee Charges', 'category': 'Financial Charges', 'type': 'Interest'},
    '71149': {'name': 'Other Financial Charges', 'category': 'Financial Charges', 'type': 'Interest'},
    
    # Non-Operating
    '81111': {'name': 'FOREX - Realised Gain /(Loss)', 'category': 'Forex', 'type': 'Non-Operating'},
    '81121': {'name': 'FOREX - Unrealised Gain/(Loss)', 'category': 'Forex', 'type': 'Non-Operating'},
}

def calculate_metrics(df):
    """Calculate key financial metrics"""
    metrics = {}
    
    # Total Revenue
    revenue_df = df[df['type'] == 'Revenue']
    metrics['total_revenue'] = revenue_df['amount'].sum()
    
    # COGS
    cogs_df = df[df['type'] == 'COGS']
    metrics['total_cogs'] = abs(cogs_df['amount'].sum())
    
    # Gross Profit
    metrics['gross_profit'] = metrics['total_revenue'] - metrics['total_cogs']
    metrics['gross_margin'] = (metrics['gross_profit'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] != 0 else 0
    
    # OPEX
    opex_df = df[df['type'] == 'OPEX']
    metrics['total_opex'] = abs(opex_df['amount'].sum())
    
    # EBITDA
    metrics['ebitda'] = metrics['gross_profit'] - metrics['total_opex']
    metrics['ebitda_margin'] = (metrics['ebitda'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] != 0 else 0
    
    # D&A
    da_df = df[df['type'] == 'D&A']
    metrics['total_da'] = abs(da_df['amount'].sum())
    
    # EBIT
    metrics['ebit'] = metrics['ebitda'] - metrics['total_da']
    metrics['ebit_margin'] = (metrics['ebit'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] != 0 else 0
    
    # Interest
    interest_df = df[df['type'] == 'Interest']
    interest_income = interest_df[interest_df['category'] == 'Interest Income']['amount'].sum()
    interest_expense = abs(interest_df[interest_df['category'] != 'Interest Income']['amount'].sum())
    metrics['net_interest'] = interest_income - interest_expense
    
    # Non-Operating
    nonop_df = df[df['type'] == 'Non-Operating']
    metrics['non_operating'] = nonop_df['amount'].sum()
    
    # PBT
    metrics['pbt'] = metrics['ebit'] + metrics['net_interest'] + metrics['non_operating']
    metrics['pbt_margin'] = (metrics['pbt'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] != 0 else 0
    
    return metrics

def generate_optimization_recommendations(df, metrics):
    """Generate AI-driven optimization recommendations based on investment banking principles"""
    recommendations = []
    
    # 1. Margin Analysis
    if metrics['gross_margin'] < 40:
        recommendations.append({
            'priority': 'High',
            'category': 'Gross Margin',
            'issue': f"Gross margin at {metrics['gross_margin']:.1f}% is below industry benchmark (40-50% for airlines)",
            'action': 'Review pricing strategy and negotiate supplier contracts for inflight products',
            'impact': 'Potential 3-5% margin improvement could add $' + f"{(metrics['total_revenue'] * 0.04):,.0f}" + ' to bottom line'
        })
    
    # 2. COGS Efficiency
    cogs_categories = df[df['type'] == 'COGS'].groupby('category')['amount'].sum().abs()
    if len(cogs_categories) > 0:
        top_cogs = cogs_categories.nlargest(3)
        for cat, amt in top_cogs.items():
            cogs_pct = (amt / metrics['total_cogs']) * 100
            if cogs_pct > 25:
                recommendations.append({
                    'priority': 'High',
                    'category': 'COGS Optimization',
                    'issue': f"{cat} represents {cogs_pct:.1f}% of total COGS (${amt:,.0f})",
                    'action': f'Benchmark {cat} against competitors and negotiate volume discounts',
                    'impact': f'10% reduction could save ${amt * 0.10:,.0f} annually'
                })
    
    # 3. Marketing ROI
    marketing_spend = abs(df[df['category'] == 'Marketing & Advertising']['amount'].sum())
    if marketing_spend > 0:
        marketing_pct = (marketing_spend / metrics['total_revenue']) * 100
        if marketing_pct > 8:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Marketing Efficiency',
                'issue': f"Marketing spend at {marketing_pct:.1f}% of revenue (${marketing_spend:,.0f}) exceeds benchmark (5-7%)",
                'action': 'Implement digital marketing attribution model and shift to performance-based channels',
                'impact': f'Optimizing to 6% could save ${(marketing_spend - metrics['total_revenue'] * 0.06):,.0f}'
            })
    
    # 4. Revenue Diversification
    revenue_by_category = df[df['type'] == 'Revenue'].groupby('category')['amount'].sum()
    if len(revenue_by_category) > 0:
        flight_rev = revenue_by_category.get('Flight Revenue', 0)
        flight_pct = (flight_rev / metrics['total_revenue']) * 100
        if flight_pct > 80:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Revenue Diversification',
                'issue': f"Flight revenue represents {flight_pct:.1f}% of total - high concentration risk",
                'action': 'Develop ancillary revenue streams: baggage fees, seat selection, inflight sales, partnerships',
                'impact': 'Ancillary revenue can add 15-20% to total revenue per industry standards'
            })
    
    # 5. Personnel Cost Analysis
    payroll_costs = abs(df[df['category'].str.contains('Payroll', na=False)]['amount'].sum())
    if payroll_costs > 0:
        payroll_pct = (payroll_costs / metrics['total_revenue']) * 100
        if payroll_pct > 30:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Labor Productivity',
                'issue': f"Personnel costs at {payroll_pct:.1f}% of revenue (${payroll_costs:,.0f}) above benchmark (25-28%)",
                'action': 'Review headcount efficiency, automate processes, and optimize crew scheduling',
                'impact': f'2% improvement could save ${payroll_costs * 0.02:,.0f}'
            })
    
    # 6. Technology & Digital Transformation
    it_spend = abs(df[df['category'] == 'IT Expenses']['amount'].sum())
    if it_spend > 0:
        it_pct = (it_spend / metrics['total_revenue']) * 100
        if it_pct < 2:
            recommendations.append({
                'priority': 'Low',
                'category': 'Digital Investment',
                'issue': f"IT spend at {it_pct:.1f}% of revenue (${it_spend:,.0f}) below benchmark (3-5%)",
                'action': 'Increase investment in digital booking platforms, mobile apps, and data analytics',
                'impact': 'Digital transformation can improve customer experience and reduce distribution costs'
            })
    
    # 7. Commission & Distribution Costs
    commission_items = df[df['name'].str.contains('Commission|Gateway|Merchant', case=False, na=False)]
    total_commission = abs(commission_items['amount'].sum())
    if total_commission > 0:
        comm_pct = (total_commission / metrics['total_revenue']) * 100
        if comm_pct > 5:
            recommendations.append({
                'priority': 'High',
                'category': 'Distribution Cost',
                'issue': f"Commission & payment fees at {comm_pct:.1f}% of revenue (${total_commission:,.0f})",
                'action': 'Shift to direct booking channels, renegotiate credit card fees, and optimize payment mix',
                'impact': f'1% reduction could save ${metrics['total_revenue'] * 0.01:,.0f}'
            })
    
    # 8. EBITDA Optimization
    if metrics['ebitda_margin'] < 15:
        recommendations.append({
            'priority': 'Critical',
            'category': 'Overall Profitability',
            'issue': f"EBITDA margin at {metrics['ebitda_margin']:.1f}% below healthy airline benchmark (15-20%)",
            'action': 'Implement comprehensive margin enhancement program across all cost categories',
            'impact': 'Target 18% EBITDA margin for sustainable operations and growth investment'
        })
    
    return sorted(recommendations, key=lambda x: {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}[x['priority']])

# App Title
st.title("✈️ Airline P&L Profitability Analyzer")
st.markdown("**Investment Banking-Grade Financial Analysis & Optimization Platform**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Data Upload")
    st.markdown("Upload your P&L data with GL codes and amounts")
    
    uploaded_file = st.file_uploader("Choose CSV or Excel file", type=['csv', 'xlsx', 'xls'])
    
    st.markdown("---")
    st.markdown("### 📋 Required Columns:")
    st.markdown("- `gl_code` or `GL Code`")
    st.markdown("- `amount` or `Amount`")
    st.markdown("- `month` or `period` (optional)")
    st.markdown("- Supports formats: 2024-01, Jan-2024, January 2024")
    
    st.markdown("---")
    st.markdown("### 💡 Analysis Features:")
    st.markdown("✓ Month-over-Month Trends")
    st.markdown("✓ P&L Waterfall Analysis")
    st.markdown("✓ Margin Breakdown")
    st.markdown("✓ Cost Category Analysis")
    st.markdown("✓ AI-Powered Recommendations")
    st.markdown("✓ Benchmarking Analysis")

# Main Content
if uploaded_file is None:
    st.info("👆 Please upload your P&L data file to begin analysis")
    
    # Sample data structure
    st.markdown("### 📝 Sample Data Format")
    sample_df = pd.DataFrame({
        'gl_code': ['41110', '51711', '61111', '71121'],
        'amount': [1000000, -50000, -200000, -10000],
        'month': ['2024-01', '2024-01', '2024-01', '2024-01']
    })
    st.dataframe(sample_df)
    
else:
    # Load data
    try:
        if uploaded_file.name.endswith('.csv'):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)
        
        # Normalize column names
        raw_df.columns = raw_df.columns.str.lower().str.strip()
        
        # Check for required columns
        if 'gl_code' not in raw_df.columns and 'gl code' not in raw_df.columns:
            st.error("❌ File must contain 'gl_code' or 'GL Code' column")
            st.stop()
        
        if 'amount' not in raw_df.columns:
            st.error("❌ File must contain 'amount' or 'Amount' column")
            st.stop()
        
        # Standardize column names
        if 'gl code' in raw_df.columns:
            raw_df.rename(columns={'gl code': 'gl_code'}, inplace=True)
        
        # Handle month/period column
        has_time_dimension = False
        if 'month' in raw_df.columns:
            raw_df['period'] = pd.to_datetime(raw_df['month'], errors='coerce')
            has_time_dimension = True
        elif 'period' in raw_df.columns:
            raw_df['period'] = pd.to_datetime(raw_df['period'], errors='coerce')
            has_time_dimension = True
        
        if has_time_dimension:
            raw_df = raw_df.dropna(subset=['period'])
            raw_df['month_name'] = raw_df['period'].dt.strftime('%b %Y')
            raw_df['year_month'] = raw_df['period'].dt.strftime('%Y-%m')
        
        # Convert GL codes to string
        raw_df['gl_code'] = raw_df['gl_code'].astype(str).str.strip()
        
        # Map GL codes to categories
        raw_df['name'] = raw_df['gl_code'].map(lambda x: GL_CODE_MAPPING.get(x, {}).get('name', 'Unknown'))
        raw_df['category'] = raw_df['gl_code'].map(lambda x: GL_CODE_MAPPING.get(x, {}).get('category', 'Unknown'))
        raw_df['type'] = raw_df['gl_code'].map(lambda x: GL_CODE_MAPPING.get(x, {}).get('type', 'Unknown'))
        
        # Filter out unknown codes
        df = raw_df[raw_df['type'] != 'Unknown'].copy()
        unknown_codes = raw_df[raw_df['type'] == 'Unknown']['gl_code'].unique()
        
        if len(unknown_codes) > 0:
            st.warning(f"⚠️ {len(unknown_codes)} GL codes not recognized: {', '.join(unknown_codes[:5])}{'...' if len(unknown_codes) > 5 else ''}")
        
        # Period/Month selector if time dimension exists
        selected_periods = None
        if has_time_dimension:
            st.sidebar.markdown("---")
            st.sidebar.header("📅 Time Period Selection")
            
            all_periods = sorted(df['month_name'].unique())
            period_selection = st.sidebar.radio(
                "Analysis Mode:",
                ["All Periods Combined", "Single Period", "Compare Periods", "Trend Analysis"]
            )
            
            if period_selection == "Single Period":
                selected_period = st.sidebar.selectbox("Select Month:", all_periods)
                selected_periods = [selected_period]
                df = df[df['month_name'] == selected_period]
                st.info(f"📅 Analyzing data for: **{selected_period}**")
                
            elif period_selection == "Compare Periods":
                selected_periods = st.sidebar.multiselect(
                    "Select Periods to Compare:",
                    all_periods,
                    default=all_periods[-2:] if len(all_periods) >= 2 else all_periods
                )
                if selected_periods:
                    df = df[df['month_name'].isin(selected_periods)]
                    st.info(f"📅 Comparing: **{', '.join(selected_periods)}**")
            
            elif period_selection == "Trend Analysis":
                st.info(f"📅 Trend analysis across **{len(all_periods)} periods**")
        
        # Calculate metrics based on selection
        if has_time_dimension and period_selection in ["Compare Periods", "Trend Analysis"]:
            metrics_by_period = {}
            for period in df['month_name'].unique():
                period_df = df[df['month_name'] == period]
                metrics_by_period[period] = calculate_metrics(period_df)
            
            # Use most recent period for main metrics display
            latest_period = sorted(df['month_name'].unique())[-1]
            metrics = metrics_by_period[latest_period]
        else:
            metrics = calculate_metrics(df)
        
        # Calculate metrics
        # metrics = calculate_metrics(df)
        
        # Generate recommendations
        recommendations = generate_optimization_recommendations(df, metrics)
        
        # Display Key Metrics
        st.header("📈 Financial Performance Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Revenue", f"${metrics['total_revenue']:,.0f}")
            st.metric("Gross Profit", f"${metrics['gross_profit']:,.0f}")
        
        with col2:
            st.metric("Gross Margin", f"{metrics['gross_margin']:.1f}%")
            st.metric("EBITDA", f"${metrics['ebitda']:,.0f}")
        
        with col3:
            st.metric("EBITDA Margin", f"{metrics['ebitda_margin']:.1f}%")
            st.metric("EBIT", f"${metrics['ebit']:,.0f}")
        
        with col4:
            st.metric("EBIT Margin", f"{metrics['ebit_margin']:.1f}%")
            st.metric("PBT", f"${metrics['pbt']:,.0f}")
        
        st.markdown("---")
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Optimization", "📊 P&L Waterfall", "💰 Revenue Analysis", "💸 Cost Analysis", "📋 Detailed Data"])
        
        with tab1:
            st.header("🎯 Strategic Optimization Recommendations")
            st.markdown("*Based on investment banking best practices and industry benchmarks*")
            
            if len(recommendations) == 0:
                st.success("✅ Your P&L structure is optimized! No major issues detected.")
            else:
                for i, rec in enumerate(recommendations):
                    priority_color = {
                        'Critical': '🔴',
                        'High': '🟠',
                        'Medium': '🟡',
                        'Low': '🟢'
                    }
                    
                    with st.expander(f"{priority_color[rec['priority']]} **{rec['category']}** - {rec['priority']} Priority"):
                        st.markdown(f"**Issue:** {rec['issue']}")
                        st.markdown(f"**Recommended Action:** {rec['action']}")
                        st.markdown(f"**Potential Impact:** {rec['impact']}")
            
            # Quick Win Summary
            st.markdown("---")
            st.subheader("💡 Quick Wins Summary")
            high_priority = [r for r in recommendations if r['priority'] in ['Critical', 'High']]
            if len(high_priority) > 0:
                st.markdown(f"**{len(high_priority)} high-priority items** identified for immediate action")
                total_potential_impact = sum([float(r['impact'].split(')[1].replace(',', '').split()[0]) 
                                             for r in high_priority if ' in r['impact'] and 'save' in r['impact']])
                if total_potential_impact > 0:
                    st.markdown(f"**Estimated annual savings potential: ${total_potential_impact:,.0f}**")
        
        with tab2:
            st.header("📊 P&L Waterfall Analysis")
            
            # Create waterfall data
            waterfall_data = {
                'Metric': ['Revenue', 'COGS', 'Gross Profit', 'OPEX', 'EBITDA', 'D&A', 'EBIT', 'Interest', 'Non-Op', 'PBT'],
                'Amount': [
                    metrics['total_revenue'],
                    -metrics['total_cogs'],
                    metrics['gross_profit'],
                    -metrics['total_opex'],
                    metrics['ebitda'],
                    -metrics['total_da'],
                    metrics['ebit'],
                    metrics['net_interest'],
                    metrics['non_operating'],
                    metrics['pbt']
                ]
            }
            
            # Create waterfall chart
            fig = go.Figure(go.Waterfall(
                name="P&L Waterfall",
                orientation="v",
                measure=["absolute", "relative", "total", "relative", "total", "relative", "total", "relative", "relative", "total"],
                x=waterfall_data['Metric'],
                y=waterfall_data['Amount'],
                text=[f"${v:,.0f}" for v in waterfall_data['Amount']],
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "#EF5350"}},
                increasing={"marker": {"color": "#66BB6A"}},
                totals={"marker": {"color": "#42A5F5"}}
            ))
            
            fig.update_layout(
                title="P&L Waterfall: Revenue to Pre-Tax Profit",
                height=600,
                showlegend=False,
                yaxis_title="Amount ($)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Margin progression
            st.subheader("📉 Margin Progression")
            margin_df = pd.DataFrame({
                'Stage': ['Gross Margin', 'EBITDA Margin', 'EBIT Margin', 'PBT Margin'],
                'Margin %': [metrics['gross_margin'], metrics['ebitda_margin'], 
                           metrics['ebit_margin'], metrics['pbt_margin']]
            })
            
            fig2 = px.bar(margin_df, x='Stage', y='Margin %', 
                         color='Margin %',
                         color_continuous_scale='RdYlGn',
                         text='Margin %')
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig2.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            st.header("💰 Revenue Analysis")
            
            # Revenue by category
            revenue_df = df[df['type'] == 'Revenue'].copy()
            revenue_by_cat = revenue_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Revenue by Category")
                fig3 = px.pie(values=revenue_by_cat.values, 
                            names=revenue_by_cat.index,
                            title="Revenue Distribution")
                fig3.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                st.subheader("Top 10 Revenue Line Items")
                top_revenue = revenue_df.nlargest(10, 'amount')[['name', 'amount', 'category']]
                top_revenue['amount'] = top_revenue['amount'].apply(lambda x: f"${x:,.0f}")
                st.dataframe(top_revenue, hide_index=True, use_container_width=True)
            
            # Revenue concentration analysis
            st.subheader("📊 Revenue Concentration Risk")
            top_3_revenue = revenue_by_cat.head(3).sum()
            concentration = (top_3_revenue / metrics['total_revenue']) * 100
            
            st.metric("Top 3 Categories Concentration", f"{concentration:.1f}%")
            if concentration > 70:
                st.warning("⚠️ High revenue concentration risk. Consider diversifying revenue streams.")
            else:
                st.success("✅ Healthy revenue diversification")
        
        with tab4:
            st.header("💸 Cost Analysis")
            
            # Combined cost analysis
            cost_df = df[df['type'].isin(['COGS', 'OPEX'])].copy()
            cost_by_category = cost_df.groupby(['type', 'category'])['amount'].sum().abs()
            
            # Cost structure treemap
            st.subheader("Cost Structure Breakdown")
            
            cost_tree_df = cost_df.groupby(['type', 'category'])['amount'].sum().abs().reset_index()
            cost_tree_df.columns = ['Type', 'Category', 'Amount']
            
            fig4 = px.treemap(cost_tree_df, 
                            path=['Type', 'Category'], 
                            values='Amount',
                            title='Cost Structure Hierarchy',
                            color='Amount',
                            color_continuous_scale='Reds')
            fig4.update_layout(height=600)
            st.plotly_chart(fig4, use_container_width=True)
            
            # Cost efficiency metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Cost as % of Revenue")
                cost_metrics = pd.DataFrame({
                    'Cost Type': ['COGS', 'OPEX', 'D&A', 'Total Costs'],
                    'Amount': [metrics['total_cogs'], metrics['total_opex'], 
                              metrics['total_da'], 
                              metrics['total_cogs'] + metrics['total_opex'] + metrics['total_da']],
                    '% of Revenue': [
                        (metrics['total_cogs'] / metrics['total_revenue'] * 100),
                        (metrics['total_opex'] / metrics['total_revenue'] * 100),
                        (metrics['total_da'] / metrics['total_revenue'] * 100),
                        ((metrics['total_cogs'] + metrics['total_opex'] + metrics['total_da']) / metrics['total_revenue'] * 100)
                    ]
                })
                cost_metrics['Amount'] = cost_metrics['Amount'].apply(lambda x: f"${x:,.0f}")
                cost_metrics['% of Revenue'] = cost_metrics['% of Revenue'].apply(lambda x: f"{x:.1f}%")
                st.dataframe(cost_metrics, hide_index=True, use_container_width=True)
            
            with col2:
                st.subheader("Top 10 Cost Items")
                top_costs = cost_df.nlargest(10, 'amount', keep='first')[['name', 'amount', 'category']]
                top_costs['amount'] = top_costs['amount'].abs().apply(lambda x: f"${x:,.0f}")
                st.dataframe(top_costs, hide_index=True, use_container_width=True)
            
            # Cost optimization opportunities
            st.subheader("🎯 Cost Optimization Matrix")
            
            cost_summary = cost_df.groupby('category').agg({
                'amount': lambda x: abs(x.sum())
            }).reset_index()
            cost_summary['% of Total Cost'] = (cost_summary['amount'] / cost_summary['amount'].sum() * 100)
            cost_summary = cost_summary.sort_values('amount', ascending=False).head(10)
            
            fig5 = px.bar(cost_summary, 
                         x='category', 
                         y='amount',
                         text='amount',
                         title='Top 10 Cost Categories',
                         labels={'amount': 'Cost ($)', 'category': 'Category'})
            fig5.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
            fig5.update_layout(height=500, xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)
        
        with tab5:
            st.header("📋 Detailed Transaction Data")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                type_filter = st.multiselect("Filter by Type", 
                                            options=df['type'].unique(),
                                            default=df['type'].unique())
            
            with col2:
                category_filter = st.multiselect("Filter by Category",
                                                options=df['category'].unique())
            
            with col3:
                search_term = st.text_input("Search GL Code or Name")
            
            # Apply filters
            filtered_df = df[df['type'].isin(type_filter)].copy()
            
            if category_filter:
                filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
            
            if search_term:
                filtered_df = filtered_df[
                    filtered_df['gl_code'].str.contains(search_term, case=False, na=False) |
                    filtered_df['name'].str.contains(search_term, case=False, na=False)
                ]
            
            # Display data
            st.dataframe(
                filtered_df[['gl_code', 'name', 'category', 'type', 'amount']].sort_values('amount', ascending=False),
                use_container_width=True,
                height=600
            )
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"pl_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Footer with key insights
        st.markdown("---")
        st.header("🔍 Executive Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Strengths")
            strengths = []
            if metrics['gross_margin'] >= 40:
                strengths.append(f"✅ Strong gross margin at {metrics['gross_margin']:.1f}%")
            if metrics['ebitda_margin'] >= 15:
                strengths.append(f"✅ Healthy EBITDA margin at {metrics['ebitda_margin']:.1f}%")
            if len(strengths) == 0:
                strengths.append("Focus on implementing recommendations to build strengths")
            for s in strengths:
                st.markdown(s)
        
        with col2:
            st.subheader("Areas for Improvement")
            improvements = []
            if metrics['gross_margin'] < 40:
                improvements.append(f"⚠️ Gross margin below benchmark ({metrics['gross_margin']:.1f}%)")
            if metrics['ebitda_margin'] < 15:
                improvements.append(f"⚠️ EBITDA margin needs improvement ({metrics['ebitda_margin']:.1f}%)")
            if len([r for r in recommendations if r['priority'] == 'Critical']) > 0:
                improvements.append(f"🔴 {len([r for r in recommendations if r['priority'] == 'Critical'])} critical issues require immediate attention")
            
            if len(improvements) == 0:
                improvements.append("✅ No major concerns identified")
            for imp in improvements:
                st.markdown(imp)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)
