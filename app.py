import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.simple_extractor import extract_contract_simple
from src.database import ContractDatabase

st.set_page_config(
    page_title="Contract Intelligence System",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Contract Intelligence System</h1>', unsafe_allow_html=True)

st.markdown("""
This application extracts key information from procurement contract PDFs.

Extracted fields:
- Vendor Name
- Contract Number
- Effective & Expiration Dates
- Total Amount
- Payment Terms
- Contract Type
- Key Deliverables
""")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to:",
    ["Upload Contract", "Contract History","Dashboard"]
)

st.sidebar.markdown("---")
db = ContractDatabase("data/contracts.db")
total_contracts = db.get_contract_count()
st.sidebar.metric("Total Contracts", total_contracts)

st.markdown("---")
st.markdown("Powered by OpenAI GPT-4o-mini")

if page == "Upload Contract":
    st.markdown("---")
    st.subheader("Upload Contract")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a contract in PDF format"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / uploaded_file.name
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Extract Contract Data"):
            with st.spinner("Extracting data..."):
                try:
                    extracted_data = extract_contract_simple(str(temp_path))
                    st.session_state.extracted_data = extracted_data
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.success("Extraction successful!")
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
        
        if 'extracted_data' in st.session_state:
            extracted_data = st.session_state.extracted_data
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Vendor Information**")
                st.info(f"**Vendor:** {extracted_data.get('vendor_name', 'N/A')}")
                st.info(f"**Contract Number:** {extracted_data.get('contract_number', 'N/A')}")
                st.info(f"**Contract Type:** {extracted_data.get('contract_type', 'N/A')}")
            
            with col2:
                st.markdown("**Financial & Dates**")
                st.info(f"**Total Amount:** {extracted_data.get('total_amount', 'N/A')}")
                st.info(f"**Payment Terms:** {extracted_data.get('payment_terms', 'N/A')}")
                st.info(f"**Effective Date:** {extracted_data.get('effective_date', 'N/A')}")
                st.info(f"**Expiration Date:** {extracted_data.get('expiration_date', 'N/A')}")
            
            st.markdown("**Key Deliverables**")
            st.text_area(
                "Deliverables",
                value=extracted_data.get('key_deliverables', 'N/A'),
                height=100,
                disabled=True
            )
            
            st.markdown("---")
            
            if st.button("Save to Database"):
                try:
                    contract_id = db.insert_contract(
                        filename=st.session_state.uploaded_filename,
                        contract_data=extracted_data
                    )
                    st.balloons()
                    st.success(f"Contract saved successfully! (ID: {contract_id})")
                    del st.session_state.extracted_data
                    del st.session_state.uploaded_filename
                except Exception as e:
                    st.error(f"Error saving: {str(e)}")

elif page == "Contract History":
    st.markdown("---")
    st.subheader("Contract History")
    
    contracts = db.get_all_contracts()
    
    if not contracts:
        st.warning("No contracts in database yet. Upload your first contract!")
    else:
        import pandas as pd
        df = pd.DataFrame(contracts)
        
        st.markdown("### Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            vendors = ['All'] + sorted(df['vendor_name'].dropna().unique().tolist())
            selected_vendor = st.selectbox("Filter by Vendor", vendors)
        
        with col2:
            types = ['All'] + sorted(df['contract_type'].dropna().unique().tolist())
            selected_type = st.selectbox("Filter by Type", types)
        
        with col3:
            sort_by = st.selectbox("Sort By", 
                ['Upload Date (Newest)', 'Upload Date (Oldest)', 'Vendor Name', 'Amount'])
        
        filtered_df = df.copy()
        
        if selected_vendor != 'All':
            filtered_df = filtered_df[filtered_df['vendor_name'] == selected_vendor]
        
        if selected_type != 'All':
            filtered_df = filtered_df[filtered_df['contract_type'] == selected_type]
        
        if sort_by == 'Upload Date (Newest)':
            filtered_df = filtered_df.sort_values('upload_date', ascending=False)
        elif sort_by == 'Upload Date (Oldest)':
            filtered_df = filtered_df.sort_values('upload_date', ascending=True)
        elif sort_by == 'Vendor Name':
            filtered_df = filtered_df.sort_values('vendor_name')
        elif sort_by == 'Amount':
            filtered_df = filtered_df.sort_values('total_amount')
        
        st.success(f"Showing {len(filtered_df)} of {len(df)} contracts")
        
        display_df = filtered_df[['id', 'filename', 'vendor_name', 'contract_number', 
                         'contract_type', 'total_amount', 'effective_date', 
                         'expiration_date', 'upload_date']]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": "ID",
                "filename": "File",
                "vendor_name": "Vendor",
                "contract_number": "Contract #",
                "contract_type": "Type",
                "total_amount": "Amount",
                "effective_date": "Start",
                "expiration_date": "End",
                "upload_date": "Uploaded"
            }
        )
        
        st.markdown("---")
        st.markdown("### Export Data")
        
        export_format = st.selectbox("Format", ["CSV", "Excel", "JSON"])
        
        if st.button("Export Contracts", type="primary"):
            from datetime import datetime
            
            if export_format == "CSV":
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"contracts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            elif export_format == "Excel":
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='Contracts')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"contracts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif export_format == "JSON":
                json_str = filtered_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"contracts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
elif page == "Dashboard":
    st.markdown("---")
    st.subheader("Analytics Dashboard")
    
    contracts = db.get_all_contracts()
    
    if not contracts:
        st.warning("No contracts to analyze yet. Upload contracts first!")
    else:
        import pandas as pd
        import plotly.express as px
        
        df = pd.DataFrame(contracts)
        
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Contracts", len(df))
        
        with col2:
            with_amounts = df[df['total_amount'].notna()].shape[0]
            st.metric("With Amount", with_amounts)
        
        with col3:
            unique_vendors = df['vendor_name'].nunique()
            st.metric("Unique Vendors", unique_vendors)
        
        with col4:
            from datetime import datetime, timedelta
            df['upload_date'] = pd.to_datetime(df['upload_date'])
            recent = df[df['upload_date'] > datetime.now() - timedelta(days=7)].shape[0]
            st.metric("Last 7 Days", recent)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Contracts by Type")
            type_counts = df['contract_type'].value_counts().reset_index()
            type_counts.columns = ['Contract Type', 'Count']
            
            fig = px.pie(
                type_counts,
                values='Count',
                names='Contract Type',
                title='Distribution by Type'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Top Vendors")
            vendor_counts = df['vendor_name'].value_counts().head(10).reset_index()
            vendor_counts.columns = ['Vendor', 'Count']
            
            fig = px.bar(
                vendor_counts,
                x='Count',
                y='Vendor',
                orientation='h',
                title='Top 10 Vendors by Contract Count'
            )
            st.plotly_chart(fig, use_container_width=True)