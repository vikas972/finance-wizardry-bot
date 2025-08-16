import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, LineChart, Line } from "recharts";

const portfolioData = {
  totalValue: "$128,430.45",
  totalReturn: "+$12,546.32",
  monthlyChange: "+2.5%",
  allTimeReturn: "+10.8%",
  riskLevel: "Moderate"
};

const allocationData = [
  { name: "Stocks", value: 45, color: "#3b82f6" },
  { name: "Bonds", value: 25, color: "#10b981" },
  { name: "Cash", value: 15, color: "#f59e0b" },
  { name: "Real Estate", value: 10, color: "#8b5cf6" },
  { name: "Commodities", value: 5, color: "#f97316" },
];

const performanceHistory = [
  { month: "Jan", value: 115000 },
  { month: "Feb", value: 118000 },
  { month: "Mar", value: 122000 },
  { month: "Apr", value: 119000 },
  { month: "May", value: 125000 },
  { month: "Jun", value: 128430 },
];

const assetPerformance = [
  { name: "Stocks", performance: 12.5 },
  { name: "Bonds", performance: 4.2 },
  { name: "Real Estate", performance: 8.7 },
  { name: "Commodities", performance: -2.1 },
];

const positions = [
  { symbol: "AAPL", name: "Apple Inc.", shares: 50, value: "$9,922.50", return: "+15.2%", positive: true },
  { symbol: "MSFT", name: "Microsoft Corp.", shares: 25, value: "$10,718.75", return: "+8.3%", positive: true },
  { symbol: "GOOGL", name: "Alphabet Inc.", shares: 30, value: "$4,089.00", return: "+12.1%", positive: true },
  { symbol: "TSLA", name: "Tesla Inc.", shares: 15, value: "$2,857.50", return: "-5.2%", positive: false },
  { symbol: "AMZN", name: "Amazon.com Inc.", shares: 20, value: "$3,646.00", return: "+7.8%", positive: true },
];

interface PortfolioProps {
  customerId?: number | null;
}

export default function Portfolio({ customerId }: PortfolioProps) {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Portfolio</h1>
      </div>

      {/* Portfolio Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="positions">Positions</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Portfolio Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">Total Value</p>
                  <p className="text-3xl font-bold">{portfolioData.totalValue}</p>
                  <p className="text-sm text-green-600 flex items-center gap-1">
                    <TrendingUp className="w-4 h-4" />
                    {portfolioData.monthlyChange} since last month
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">Total Return</p>
                  <p className="text-3xl font-bold text-green-600">{portfolioData.totalReturn}</p>
                  <p className="text-sm text-green-600 flex items-center gap-1">
                    <TrendingUp className="w-4 h-4" />
                    {portfolioData.allTimeReturn} all time
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">Risk Assessment</p>
                  <p className="text-3xl font-bold">{portfolioData.riskLevel}</p>
                  <p className="text-sm text-gray-600">Based on current holdings</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Asset Allocation and Performance */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Asset Allocation */}
            <Card>
              <CardHeader>
                <CardTitle>Asset Allocation</CardTitle>
                <p className="text-sm text-gray-600">Current portfolio distribution</p>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center">
                  <div className="w-80 h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={allocationData}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={120}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {allocationData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
                <div className="mt-4 space-y-2">
                  {allocationData.map((item) => (
                    <div key={item.name} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: item.color }}
                        />
                        <span className="text-sm">{item.name}</span>
                      </div>
                      <span className="text-sm font-medium">({item.value}%)</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Performance History */}
            <Card>
              <CardHeader>
                <CardTitle>Performance History</CardTitle>
                <p className="text-sm text-gray-600">6 month trend</p>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={performanceHistory}>
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Positions Tab */}
        <TabsContent value="positions" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Current Positions</CardTitle>
              <p className="text-sm text-gray-600">Your portfolio holdings</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {positions.map((position) => (
                  <div
                    key={position.symbol}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                  >
                    <div className="flex items-center gap-4">
                      <div>
                        <h4 className="font-semibold">{position.symbol}</h4>
                        <p className="text-sm text-gray-600">{position.name}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-8">
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Shares</p>
                        <p className="font-medium">{position.shares}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Value</p>
                        <p className="font-medium">{position.value}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Return</p>
                        <p className={`font-medium ${
                          position.positive ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {position.return}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Performance by Asset Class</CardTitle>
              <p className="text-sm text-gray-600">Returns over the past year</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {assetPerformance.map((asset) => (
                  <div key={asset.name} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">{asset.name}</span>
                      <span className={`text-sm font-bold ${
                        asset.performance >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {asset.performance >= 0 ? '+' : ''}{asset.performance}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          asset.performance >= 0 ? 'bg-green-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${Math.abs(asset.performance) * 5}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Portfolio Value History</CardTitle>
              <p className="text-sm text-gray-600">Track your portfolio growth over time</p>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={performanceHistory}>
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#3b82f6"
                      strokeWidth={3}
                      dot={{ fill: "#3b82f6", strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
