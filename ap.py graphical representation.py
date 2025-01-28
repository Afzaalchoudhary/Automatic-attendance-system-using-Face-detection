import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the attendance data
file_path = "C:\\Users\\hp\\Downloads\\Cleaned_Attendance_Record.csv"
df = pd.read_csv(file_path)

# Data preprocessing
date_columns = df.columns[2:-1]  # All date columns (excluding ID, Student Name, and TOTAL)

def calculate_attendance_percentage(row):
    total_present = row[date_columns].fillna("A").str.count("P").sum()
    total_days = len(date_columns)
    return (total_present / total_days) * 100

df["Attendance (%)"] = df.apply(calculate_attendance_percentage, axis=1)

# Filter for students below 75% attendance
short_attendance = df[df["Attendance (%)"] < 75]

# Streamlit Dashboard
st.set_page_config(page_title="Student Attendance Dashboard", layout="wide")

# Adding the IAC logo at the top with a better display
# Ensure the logo path is correct, or use a web URL for better portability
st.image(r"C:\\Users\\hp\\Downloads\\images.jpeg", width=300)  # Resize logo for better look

# Title
st.title("Student Attendance Dashboard")
st.markdown("### Presented by M.Afzaal Amjad & Zain Ul Abideen")

# Sidebar Filters
st.sidebar.header("Filters")
attendance_filter = st.sidebar.slider("Minimum Attendance (%)", 0, 100, 75)
filtered_data = df[df["Attendance (%)"] >= attendance_filter]

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", len(df))
col2.metric("Average Attendance (%)", f"{df['Attendance (%)'].mean():.2f}")
col3.metric("Students Below 75%", len(short_attendance))

# Attendance Percentage Table
st.subheader("Attendance Records")
st.dataframe(filtered_data)

# Notice for Short Attendance
st.subheader("Notice: Students Below 75% Attendance")
if len(short_attendance) > 0:
    st.warning(
        "The following students have attendance below 75% and are not allowed to sit for exams:")
    st.dataframe(short_attendance[["ID", "Student Name", "Attendance (%)"]])
else:
    st.success("No students with attendance below 75%.")

# Visualizations
st.subheader("Visualizations")

# 1. Bar Chart: Attendance Percentage by Student
fig_bar = px.bar(
    df,
    x="Student Name",
    y="Attendance (%)",
    color="Attendance (%)",
    title="Attendance Percentage by Student",
    template="plotly_dark",  # Change to dark theme for the bar chart
    color_continuous_scale="Viridis"
)
fig_bar.update_layout(title_x=0.5, title_font=dict(size=20, color="white"), margin=dict(b=100))
st.plotly_chart(fig_bar, use_container_width=True)

# 2. Line Chart: Attendance Trend by Date
attendance_trend = df.melt(id_vars=["ID", "Student Name"], value_vars=date_columns, 
                           var_name="Date", value_name="Status")
attendance_trend["Present"] = attendance_trend["Status"].fillna("A").apply(lambda x: 1 if x == "P" else 0)
trend_data = attendance_trend.groupby("Date")["Present"].mean().reset_index()
trend_data["Present"] *= 100

fig_line = px.line(
    trend_data,
    x="Date",
    y="Present",
    title="Overall Attendance Trend",
    labels={"Present": "% Present"},
    template="plotly_dark"  # Change to dark theme for the line chart
)
fig_line.update_layout(title_x=0.5, title_font=dict(size=20, color="white"), margin=dict(b=100))
st.plotly_chart(fig_line, use_container_width=True)

# 3. Attendance Status Color Coding: Present in Green, Absent in Yellow, Left in Red
attendance_status = df.melt(id_vars=["ID", "Student Name"], value_vars=date_columns, 
                            var_name="Date", value_name="Status")
attendance_status['Color'] = attendance_status['Status'].apply(
    lambda x: 'green' if x == 'P' else ('yellow' if x == 'A' else 'red')
)

# Plotting Color-Coded Attendance
fig_status = px.scatter(
    attendance_status, x="Date", y="Student Name", color="Color",
    color_discrete_map={'green': 'green', 'yellow': 'yellow', 'red': 'red'},
    title="Attendance Status: Green = Present, Yellow = Absent, Red = Left",
    template="plotly_dark"
)
fig_status.update_layout(title_x=0.5, title_font=dict(size=20, color="white"), margin=dict(b=100))
st.plotly_chart(fig_status, use_container_width=True)

# 4. 3D Scatter Plot of Attendance Data
fig_3d = go.Figure(data=[go.Scatter3d(
    x=df["Attendance (%)"],
    y=df["ID"],
    z=df["Attendance (%)"],
    mode="markers",
    marker=dict(
        size=12,
        color=df["Attendance (%)"],  # Color points based on attendance percentage
        colorscale="Viridis",  # Add a color scale
        opacity=0.8
    ),
    text=df["Student Name"],
)])

fig_3d.update_layout(
    title="3D Scatter Plot of Attendance Data",
    scene=dict(
        xaxis_title="Attendance %",
        yaxis_title="Student ID",
        zaxis_title="Attendance %",
    ),
    template="plotly_dark"
)

st.plotly_chart(fig_3d, use_container_width=True)

# Custom CSS to enhance the look with dark mode
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;  /* Dark background for the whole app */
            color: white;  /* White text color */
        }
        .stTitle {
            font-size: 32px;
            font-weight: bold;
            color: #50fa7b;  /* Light green color for the title */
        }
        .stMetric {
            font-size: 22px;
            color: #f8f8f2;  /* Light color for metrics */
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            background-color: #333;  /* Dark background for tables */
        }
        .stWarning {
            background-color: #f1c40f;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
        }
        .stSuccess {
            background-color: #2ecc71;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
        }
        .stSidebar {
            background-color: #2c3e50;  /* Dark background for the sidebar */
        }
        .stSlider {
            color: white;  /* White color for sliders */
        }
    </style>
""", unsafe_allow_html=True)
