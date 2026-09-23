import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# 1. Load data
df = pd.read_excel("sales_data.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime("%Y-%m")

# 2. Process data
total_sales = df["Amount"].sum()
sales_by_category = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
sales_by_month = df.groupby("Month")["Amount"].sum().sort_index()
top_product = df.groupby("Product")["Amount"].sum().idxmax()

# 3. Chart 1: Sales by category (bar chart)
plt.figure(figsize=(6, 4))
sales_by_category.plot(kind="bar", color="#4C72B0")
plt.title("Sales by Category")
plt.ylabel("Amount ($)")
plt.xlabel("")
plt.tight_layout()
plt.savefig("chart_category.png", dpi=150)
plt.close()

# 4. Chart 2: Sales over time (line chart)
plt.figure(figsize=(6, 4))
sales_by_month.plot(kind="line", marker="o", color="#55A868")
plt.title("Monthly Sales Trend")
plt.ylabel("Amount ($)")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_trend.png", dpi=150)
plt.close()

# 5. Build PDF report
doc = SimpleDocTemplate("sales_report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
elements = []

elements.append(Paragraph("Sales Report", styles["Title"]))
elements.append(Spacer(1, 12))
elements.append(Paragraph(f"Total Sales: ${total_sales:,.2f}", styles["Normal"]))
elements.append(Paragraph(f"Best-Selling Product: {top_product}", styles["Normal"]))
elements.append(Spacer(1, 20))

elements.append(Paragraph("Sales by Category", styles["Heading2"]))
elements.append(Image("chart_category.png", width=5*inch, height=3.3*inch))
elements.append(Spacer(1, 20))

elements.append(Paragraph("Monthly Sales Trend", styles["Heading2"]))
elements.append(Image("chart_trend.png", width=5*inch, height=3.3*inch))
elements.append(Spacer(1, 20))

table_data = [["Category", "Total Sales"]] + [[cat, f"${amt:,.2f}"] for cat, amt in sales_by_category.items()]
table = Table(table_data, colWidths=[200, 150])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C72B0")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
]))
elements.append(Paragraph("Summary Table", styles["Heading2"]))
elements.append(table)

doc.build(elements)
print("sales_report.pdf generated successfully!")