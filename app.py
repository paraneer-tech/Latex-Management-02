from utils.calculator import run_latex_management

R = [70000, 55000, 80000, 60000, 65000]
price = [50, 52, 49, 51, 53, 54, 55, 56, 57]

T = 5

result = run_latex_management(R, price, T)

for day in result["daily_log"]:
    print(day)

print("Total Profit:", result["total_profit"])
