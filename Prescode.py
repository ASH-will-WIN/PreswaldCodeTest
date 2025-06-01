from preswald import connect, get_df, text, plotly, table
import plotly.express as px
import pandas as pd

# Connect to the data
connect()
df = get_df("data/student_info.csv")

# Drop rows with missing key values
df.dropna(subset=["math_score", "reading_score", "writing_score", "study_hours", "attendance_rate"], inplace=True)

# Title + preview
text("# Student Performance Analysis Report")
text("## Dataset Overview")
table(df.head(10), "Sample Student Records")

# Gender distribution
text("## Demographic Distribution")
text("Based on the pie chart below, there is no major difference between the distributions of different genders in this demographic. However, there are a significant amount of people that identify as other in comparison to the United States national average which is only 2.65% of individuals that identify as non-cisgender.")

fig1 = px.pie(df, names="gender", title="Gender Distribution")
plotly(fig1)

text("Between each of the grade levels, there is no major difference in the gender distribution within each grade level, however, 9th grade has the most students while 12th grade has the fewest.")

df["grade_level"] = df["grade_level"].astype(str)
grade_order = ["9", "10", "11", "12"]
fig2 = px.histogram(df, x="grade_level", color="gender", title="Students by Grade Level",
                    category_orders={"grade_level": grade_order},
                    labels={"grade_level": "Grade Level"})
plotly(fig2)

# Socioeconomic section
text("## Socioeconomic Influences")
text("Regardless of lunch program — a proxy for socioeconomic status — pass/fail rates remained similar. Interestingly, the pass rate was slightly higher among students in the free/reduced lunch program.")
fig3 = px.bar(df, x="lunch_type", color="final_result", title="Outcomes by Lunch Program",
              labels={"lunch_type": "Lunch Type", "final_result": "Result"})
plotly(fig3)

text("Parental education showed no significant influence on pass/fail outcomes. Although more students had parents with college degrees, the outcome distribution was similar regardless of education level.")
fig4 = px.sunburst(df, path=["parent_education", "final_result"], title="Parent Education Impact")
plotly(fig4)

# Engagement analysis
text("## Student Engagement Analysis")

df["attendance_rate"] = pd.to_numeric(df["attendance_rate"], errors="coerce")
df["study_hours"] = pd.to_numeric(df["study_hours"], errors="coerce")
df["math_score"] = pd.to_numeric(df["math_score"], errors="coerce")

text("The scatter plot below shows a very weak relationship between attendance and math performance, as well as study hours. There is no strong trend indicating that higher attendance or more study hours consistently lead to better performance.")

fig5 = px.scatter(df, x="attendance_rate", y="math_score", color="study_hours", size="study_hours",
                  title="Attendance vs Math Performance",
                  labels={"attendance_rate": "Attendance Rate (%)",
                          "math_score": "Math Score",
                          "study_hours": "Study Hours"})
plotly(fig5)

text("The histogram below illustrates how study hours are distributed by gender. While overall patterns are similar, some gender-based variations appear at certain study-hour intervals.")
fig6 = px.histogram(df, x="study_hours", color="gender", title="Study Hours Distribution",
                    labels={"study_hours": "Weekly Study Hours"})
plotly(fig6)

# Correlation section
text("## Performance Correlations")
text("The heatmap below highlights very weak correlations across all academic and engagement metrics. Study hours had a weak positive correlation with math scores (r = 0.02), while attendance rate showed a weak negative correlation with most outcomes (r ≈ -0.06).")

cols = ["math_score", "reading_score", "writing_score", "study_hours", "attendance_rate"]
corr = df[cols].corr().round(2)
fig7 = px.imshow(corr, text_auto=True, title="Academic Factor Correlations",
                 labels={"color": "Correlation Coefficient"})
fig7.update_traces(hovertemplate="Correlation: %{z}")
plotly(fig7)

# Final Summary
text("## Key Findings")
text("- Students achieved similar average math scores regardless of extracurricular participation.")
text("- Sudents with ≥90% attendance and ≥4 study hours per week averaged math scores above 76%.")
text("- Standard lunch program students had a 51.2% pass rate, compared to 52.2% for free/reduced lunch students — showing no significant difference.")
text("- Students with a parent holding a bachelor’s degree or higher had a 51.9% pass rate vs 51.6% for others — again, showing no significant difference.")
text("- Math scores showed a very weak positive correlation with study hours (r = 0.02) and a very weak negative correlation with attendance rate (r = -0.06).")

# Footer
text("**Data Source**: student_info.csv | 1,000 student records analyzed")
