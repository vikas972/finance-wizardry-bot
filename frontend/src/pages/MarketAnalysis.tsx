import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
// Temporarily using HTML select instead of Select component
import { TrendingUp, TrendingDown } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, LineChart, Line } from "recharts";

const marketIndices = [
  {
    name: "S&P 500",
    value: "5,342.16",
    change: "+24.15",
    percentage: "+0.45%",
    positive: true
  },
  {
    name: "NASDAQ",
    value: "16,785.83",
    change: "+128.18",
    percentage: "+0.77%",
    positive: true
  },
  {
    name: "DOW JONES",
    value: "39,561.78",
    change: "-17.52",
    percentage: "-0.04%",
    positive: false
  },
  {
    name: "RUSSELL 2000",
    value: "2,070.16",
    change: "+12.38",
    percentage: "+0.60%",
    positive: true
  }
];

const marketPerformanceData = [
  { time: "9:30", value: 95 },
  { time: "10:00", value: 98 },
  { time: "10:30", value: 102 },
  { time: "11:00", value: 105 },
  { time: "11:30", value: 103 },
  { time: "12:00", value: 108 },
  { time: "12:30", value: 112 },
  { time: "1:00", value: 115 },
  { time: "1:30", value: 118 },
  { time: "2:00", value: 120 },
  { time: "2:30", value: 122 },
  { time: "3:00", value: 125 },
  { time: "3:30", value: 128 },
  { time: "4:00", value: 130 }
];

const sectors = [
  { name: "Technology", symbol: "XLK", change: "+2.1%", positive: true },
  { name: "Healthcare", symbol: "XLV", change: "+1.8%", positive: true },
  { name: "Financials", symbol: "XLF", change: "-0.5%", positive: false },
  { name: "Consumer Discretionary", symbol: "XLY", change: "+1.2%", positive: true },
  { name: "Industrials", symbol: "XLI", change: "+0.8%", positive: true },
  { name: "Energy", symbol: "XLE", change: "+3.2%", positive: true },
  { name: "Materials", symbol: "XLB", change: "+1.5%", positive: true },
  { name: "Utilities", symbol: "XLU", change: "-0.3%", positive: false }
];

const trends = [
  { name: "AI & Machine Learning", impact: "High", sentiment: "Bullish" },
  { name: "Clean Energy Transition", impact: "Medium", sentiment: "Bullish" },
  { name: "Remote Work Solutions", impact: "Medium", sentiment: "Neutral" },
  { name: "Cryptocurrency Adoption", impact: "High", sentiment: "Volatile" }
];

const analysisData = [
  { metric: "Market Volatility", value: "Low", indicator: "Positive" },
  { metric: "Volume Trends", value: "Above Average", indicator: "Positive" },
  { metric: "Institutional Flow", value: "Inflows", indicator: "Positive" },
  { metric: "Economic Indicators", value: "Mixed", indicator: "Neutral" }
];

interface MarketAnalysisProps {
  customerId?: number | null;
}

export default function MarketAnalysis({ customerId }: MarketAnalysisProps) {
  const [selectedMarket, setSelectedMarket] = useState("US Market");

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Market Analysis</h1>
        <select className="w-48 px-3 py-2 border border-gray-200 rounded-lg" defaultValue="US Market">
          <option value="US Market">US Market</option>
          <option value="European Market">European Market</option>
          <option value="Asian Market">Asian Market</option>
        </select>
      </div>

      {/* Market Analysis Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="sectors">Sectors</TabsTrigger>
          <TabsTrigger value="trends">Trends</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Market Indices */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {marketIndices.map((index) => (
              <Card key={index.name}>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <h3 className="font-semibold text-gray-900">{index.name}</h3>
                    <p className="text-2xl font-bold">{index.value}</p>
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-medium ${
                        index.positive ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {index.change}
                      </span>
                      <span className={`text-sm font-medium ${
                        index.positive ? 'text-green-600' : 'text-red-600'
                      }`}>
                        ({index.percentage})
                      </span>
                      {index.positive ? (
                        <TrendingUp className="w-4 h-4 text-green-600" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-600" />
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Market Performance Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Market Performance</CardTitle>
              <p className="text-sm text-gray-600">Performance over time</p>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={marketPerformanceData}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Sectors Tab */}
        <TabsContent value="sectors" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Sector Performance</CardTitle>
              <p className="text-sm text-gray-600">Today's sector performance breakdown</p>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {sectors.map((sector) => (
                  <div
                    key={sector.name}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                  >
                    <div>
                      <h4 className="font-semibold">{sector.name}</h4>
                      <p className="text-sm text-gray-600">{sector.symbol}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${
                        sector.positive ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {sector.change}
                      </span>
                      {sector.positive ? (
                        <TrendingUp className="w-4 h-4 text-green-600" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-600" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Trends Tab */}
        <TabsContent value="trends" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Market Trends</CardTitle>
              <p className="text-sm text-gray-600">Current market trends and their impact</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {trends.map((trend) => (
                  <div
                    key={trend.name}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                  >
                    <div>
                      <h4 className="font-semibold">{trend.name}</h4>
                      <p className="text-sm text-gray-600">Impact: {trend.impact}</p>
                    </div>
                    <Badge
                      variant={
                        trend.sentiment === "Bullish" ? "default" :
                        trend.sentiment === "Neutral" ? "secondary" : "destructive"
                      }
                    >
                      {trend.sentiment}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analysis Tab */}
        <TabsContent value="analysis" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Market Analysis</CardTitle>
              <p className="text-sm text-gray-600">Technical and fundamental analysis indicators</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analysisData.map((item) => (
                  <div
                    key={item.metric}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                  >
                    <div>
                      <h4 className="font-semibold">{item.metric}</h4>
                      <p className="text-sm text-gray-600">{item.value}</p>
                    </div>
                    <Badge
                      variant={
                        item.indicator === "Positive" ? "default" :
                        item.indicator === "Neutral" ? "secondary" : "destructive"
                      }
                    >
                      {item.indicator}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Additional Analysis Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Volume Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={marketPerformanceData.slice(0, 8)}>
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Bar dataKey="value" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Price Movement</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={marketPerformanceData.slice(0, 8)}>
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#10b981"
                        strokeWidth={2}
                        dot={{ fill: "#10b981", strokeWidth: 2, r: 3 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
