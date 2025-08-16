import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Eye, Globe } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

const marketData = [
  { name: "S&P 500", value: "5,123.45", change: "+0.75%", positive: true },
  { name: "NASDAQ", value: "17,289.3", change: "+1.2%", positive: true },
  { name: "DOW JONES", value: "38,624.78", change: "+0.25%", positive: true },
  { name: "RUSSELL 2000", value: "2,067.89", change: "+0.32%", positive: true },
];

const sectorData = [
  { name: "Technology", performance: 2.3, positive: true },
  { name: "Healthcare", performance: 1.5, positive: true },
  { name: "Financials", performance: -0.8, positive: false },
  { name: "Consumer Discretionary", performance: 0.5, positive: true },
  { name: "Industrials", performance: -0.3, positive: false },
  { name: "Energy", performance: 1.8, positive: true },
];

const allocationData = [
  { name: "Stocks", value: 60, color: "#3b82f6" },
  { name: "Bonds", value: 25, color: "#10b981" },
  { name: "Cash", value: 10, color: "#f59e0b" },
  { name: "Alternative", value: 5, color: "#8b5cf6" },
];

const sentimentData = [
  { name: "Positive", value: 45, color: "#10b981" },
  { name: "Neutral", value: 30, color: "#6b7280" },
  { name: "Negative", value: 25, color: "#ef4444" },
];

const portfolioHistory = [
  { month: "Jan", value: 120000 },
  { month: "Feb", value: 122000 },
  { month: "Mar", value: 118000 },
  { month: "Apr", value: 125000 },
  { month: "May", value: 127000 },
  { month: "Jun", value: 125750 },
];

interface DashboardProps {
  customerId?: number | null;
}

export default function Dashboard({ customerId }: DashboardProps) {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="flex items-center gap-2">
          <Globe className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">United States</span>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Portfolio Summary</CardTitle>
            <p className="text-sm text-gray-600">Current portfolio status and allocation</p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Portfolio Values */}
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600">Total Value</p>
                <p className="text-2xl font-bold">$125,750.63</p>
                <p className="text-sm text-green-600 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  $952.8 (0.76%)
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Gain</p>
                <p className="text-2xl font-bold text-green-600">$25,750.63</p>
                <p className="text-sm text-gray-600">25.75%</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Risk Level</p>
                <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                  Moderate
                </Badge>
                <p className="text-sm text-gray-600">Balanced</p>
              </div>
            </div>

            {/* Asset Allocation */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold">Asset Allocation</h4>
                <Eye className="w-4 h-4 text-gray-400" />
              </div>
              <div className="space-y-2">
                {allocationData.map((item) => (
                  <div key={item.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: item.color }}
                      />
                      <span className="text-sm">{item.name}</span>
                    </div>
                    <span className="text-sm font-medium">{item.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Market Overview */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Market Overview</CardTitle>
            <p className="text-sm text-gray-600">Real-time market indices and sector performance</p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Market Indices */}
            <div className="grid grid-cols-2 gap-4">
              {marketData.map((market) => (
                <div key={market.name} className="space-y-1">
                  <p className="text-sm text-gray-600">{market.name}</p>
                  <p className="text-lg font-bold">{market.value}</p>
                  <p className={`text-sm flex items-center gap-1 ${
                    market.positive ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {market.positive ? (
                      <TrendingUp className="w-3 h-3" />
                    ) : (
                      <TrendingDown className="w-3 h-3" />
                    )}
                    {market.change}
                  </p>
                </div>
              ))}
            </div>

            {/* Sector Performance */}
            <div>
              <h4 className="font-semibold mb-3">Sector Performance</h4>
              <div className="space-y-2">
                {sectorData.map((sector) => (
                  <div key={sector.name} className="flex items-center justify-between">
                    <span className="text-sm">{sector.name}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${
                            sector.positive ? 'bg-green-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${Math.abs(sector.performance) * 20}%` }}
                        />
                      </div>
                      <span className={`text-sm font-medium ${
                        sector.positive ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {sector.positive ? '+' : ''}{sector.performance}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Market Sentiment */}
            <div>
              <h4 className="font-semibold mb-3">Market Sentiment</h4>
              <div className="flex items-center gap-4">
                {sentimentData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm">{item.value}% {item.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Asset Performance */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Asset Performance</CardTitle>
            <p className="text-sm text-gray-600">Track your investments and market performance</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Portfolio Value History</h4>
                <p className="text-sm text-gray-600 mb-4">$130.75K</p>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={portfolioHistory}>
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Bar dataKey="value" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* News Intelligence */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">News Intelligence</CardTitle>
            <p className="text-sm text-gray-600">AI-analyzed market news with sentiment scoring</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h5 className="font-medium">Fed Signals Potential Rate Cut in September Meeting</h5>
                  <Badge className="bg-green-100 text-green-800">Positive</Badge>
                </div>
                <p className="text-sm text-gray-600 mb-2">Financial Times • 2 hours ago</p>
                <p className="text-sm">The Federal Reserve has signaled a potential interest rate cut in the September...</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
