
# PHONEPE_DATA_VISUALIZATION_AND_EXPLORATION
The aim of this project is to develop a solution that extracts, transforms, and visualizes data from the Phonepe Pulse GitHub repository. The process involves:

*Developed a user-friendly tool for visualizing and exploring PhonePe Pulse data using Streamlit and Plotly.*

**Data Retrieval:**
- Fetched PhonePe Pulse data from PhonePe's Repo via Git Clone.
- Transformed JSON data to Pandas DataFrames.
- Converted data to CSV format and downloaded to the local environment.

**SQL Integration:**
- Created six tables in SQL to store CSV data.
- Transferred CSV data to SQL tables using Python with PostgreSQL connection.

**Streamlit Interface:**
- Utilized Streamlit for the front-end interface.
- Implemented dynamic visualizations using Plotly, including Choropleth maps.
- Enabled user interaction to select options, triggering back-end queries to fetch and process data from SQL.
- Presented visual representations in the Streamlit interface based on user selections.

**Workflow:**
1. **Data Retrieval and Transformation:**
   - Cloned PhonePe Pulse data from the repository.
   - Converted JSON to CSV, facilitating local accessibility.

2. **SQL Integration:**
   - Established PostgreSQL connection.
   - Created tables and transferred data for efficient storage.

3. **Streamlit Application:**
   - Developed an interactive Streamlit app for user-friendly data exploration.
   - Implemented Plotly for dynamic visualizations, including Choropleth maps.

4. **User Interaction and Query Processing:**
   - Enabled user selection options in the Streamlit interface.
   - Executed back-end queries based on user selections to fetch and process data from SQL.

5. **Visualization:**
   - Presented visual insights in real-time within the Streamlit interface.
   - Utilized Choropleth maps and other Plotly visualizations for effective data representation.

**Results**
   - The result of this project will be a comprehensive and user-friendly solution
for extracting, transforming, and visualizing data from the Phonepe pulse Github
repository.
   - This project seamlessly integrates data retrieval, transformation, storage in SQL, and dynamic visualization in Streamlit to offer a comprehensive tool for exploring PhonePe Pulse data.
