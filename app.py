import streamlit as st
import pandas as pd
from data.frameworks_data import get_all_frameworks, get_framework_categories
from utils.visualization import create_overview_dashboard
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Business Framework Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app
def main():
    st.title("🎯 Business Framework Analysis Platform")
    st.markdown("### Comprehensive analysis of 100+ business frameworks with interactive visualizations")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        [
            "Home",
            "Framework Explorer", 
            "Comparative Analysis",
            "Industry Recommendations",
            "Framework Relationships"
        ]
    )
    
    # Load data
    frameworks_df = get_all_frameworks()
    categories = get_framework_categories()
    
    # Page routing with error handling
    try:
        if page == "Home":
            show_home_page(frameworks_df, categories)
        elif page == "Framework Explorer":
            st.write("Loading Framework Explorer...")
            import pages.framework_explorer as fe
            fe.show_page()
        elif page == "Comparative Analysis":
            st.write("Loading Comparative Analysis...")
            import pages.comparative_analysis as ca
            ca.show_page()
        elif page == "Industry Recommendations":
            st.write("Loading Industry Recommendations...")
            import pages.industry_recommendations as ir
            ir.show_page()
        elif page == "Framework Relationships":
            st.write("Loading Framework Relationships...")
            import pages.framework_relationships as fr
            fr.show_page()
    except Exception as e:
        st.error(f"Error loading page '{page}': {str(e)}")
        st.write("Please try refreshing the page or contact support if the issue persists.")

def show_home_page(frameworks_df, categories):
    """Display the home page with overview statistics and quick access"""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Frameworks", len(frameworks_df))
    
    with col2:
        st.metric("Categories", len(categories))
    
    with col3:
        st.metric("Strategic Frameworks", len(frameworks_df[frameworks_df['category'] == 'Strategic Planning Frameworks']))
    
    with col4:
        st.metric("Industries Covered", "10+")
    
    st.markdown("---")
    
    # Category overview
    st.subheader("📊 Framework Categories Overview")
    
    category_counts = frameworks_df['category'].value_counts()
    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        title="Number of Frameworks by Category",
        labels={'x': 'Category', 'y': 'Number of Frameworks'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick framework search
    st.subheader("🔍 Quick Framework Search")
    search_term = st.text_input("Search for a framework:")
    
    if search_term:
        filtered_frameworks = frameworks_df[
            frameworks_df['name'].str.contains(search_term, case=False) |
            frameworks_df['core_function'].str.contains(search_term, case=False) |
            frameworks_df['typical_uses'].str.contains(search_term, case=False)
        ]
        
        if not filtered_frameworks.empty:
            st.dataframe(
                filtered_frameworks[['name', 'category', 'core_function', 'typical_uses']],
                use_container_width=True
            )
        else:
            st.warning("No frameworks found matching your search.")
    
    # Recent additions or featured frameworks
    st.subheader("⭐ Featured Frameworks")
    
    featured_frameworks = [
        "SWOT Analysis",
        "Business Model Canvas", 
        "Porter's Five Forces",
        "Design Thinking",
        "Lean Management"
    ]
    
    featured_df = frameworks_df[frameworks_df['name'].isin(featured_frameworks)]
    
    for _, framework in featured_df.iterrows():
        with st.expander(f"📋 {framework['name']}"):
            st.write(f"**Category:** {framework['category']}")
            st.write(f"**Core Function:** {framework['core_function']}")
            st.write(f"**Typical Uses:** {framework['typical_uses']}")
    
    # Getting started guide
    st.subheader("🚀 Getting Started")
    st.markdown("""
    **How to use this platform:**
    
    1. **Framework Explorer** - Dive deep into individual frameworks with interactive parameters
    2. **Comparative Analysis** - Compare multiple frameworks side by side
    3. **Industry Recommendations** - Get framework suggestions based on your industry
    4. **Framework Relationships** - Explore how frameworks connect and complement each other
    
    **Tips:**
    - Use the sidebar to navigate between different sections
    - Adjust sliders and parameters to see real-time visualizations
    - Export your analysis results for presentations
    """)

if __name__ == "__main__":
    main()
