import { Card } from "@/components/ui/card";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { Area, AreaChart, CartesianGrid, Line, LineChart, PieChart, Pie, ResponsiveContainer, XAxis, YAxis, Cell, Legend } from "recharts";

const emiTrendData = [
  { month: "Jan", amount: 42000 },
  { month: "Feb", amount: 43000 },
  { month: "Mar", amount: 45000 },
  { month: "Apr", amount: 44000 },
  { month: "May", amount: 45000 },
  { month: "Jun", amount: 45000 },
];

const expenseData = [
  { name: "Home Loan EMI", value: 45000, color: "#8BA888" },
  { name: "Car Loan EMI", value: 15000, color: "#2F4858" },
  { name: "Credit Card", value: 10000, color: "#F0F7F4" },
  { name: "Personal Loan", value: 8000, color: "#E5E5E5" },
];

const savingsData = [
  { month: "Jan", amount: 25000 },
  { month: "Feb", amount: 28000 },
  { month: "Mar", amount: 27000 },
  { month: "Apr", amount: 30000 },
  { month: "May", amount: 32000 },
  { month: "Jun", amount: 35000 },
];

export const FinancialCharts = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 p-4">
      <Card className="p-4">
        <h3 className="text-lg font-semibold mb-4">EMI Trend Analysis</h3>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={emiTrendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <ChartTooltip content={(props) => <ChartTooltipContent {...props} />} />
              <Line type="monotone" dataKey="amount" stroke="#8BA888" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-4">
        <h3 className="text-lg font-semibold mb-4">Monthly Expense Breakdown</h3>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={expenseData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {expenseData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Legend />
              <ChartTooltip content={(props) => <ChartTooltipContent {...props} />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card className="p-4">
        <h3 className="text-lg font-semibold mb-4">Savings Potential</h3>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={savingsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <ChartTooltip content={(props) => <ChartTooltipContent {...props} />} />
              <Area type="monotone" dataKey="amount" stroke="#2F4858" fill="#F0F7F4" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};