import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis } from "recharts";

const currentAllocation = [
  { name: "Stocks", value: 45, color: "#3b82f6", amount: "$57,375" },
  { name: "Bonds", value: 25, color: "#10b981", amount: "$31,875" },
  { name: "Cash", value: 15, color: "#f59e0b", amount: "$19,125" },
  { name: "Real Estate", value: 10, color: "#8b5cf6", amount: "$12,750" },
  { name: "Commodities", value: 5, color: "#f97316", amount: "$6,375" },
];

const recommendedAllocation = [
  { name: "Stocks", current: 45, recommended: 50, difference: 5 },
  { name: "Bonds", current: 25, recommended: 25, difference: 0 },
  { name: "Cash", current: 15, recommended: 10, difference: -5 },
  { name: "Real Estate", current: 10, recommended: 10, difference: 0 },
  { name: "Commodities", current: 5, recommended: 5, difference: 0 },
];

const performanceByAsset = [
  { name: "Stocks", performance: 12.5, color: "#3b82f6" },
  { name: "Bonds", performance: 4.2, color: "#10b981" },
  { name: "Real Estate", performance: 8.7, color: "#8b5cf6" },
  { name: "Commodities", performance: -2.1, color: "#f97316" },
  { name: "Cash", performance: 2.1, color: "#f59e0b" },
];

const riskMetrics = [
  { metric: "Portfolio Beta", value: "1.12", description: "Slightly more volatile than market" },
  { metric: "Sharpe Ratio", value: "1.45", description: "Good risk-adjusted returns" },
  { metric: "Max Drawdown", value: "-8.3%", description: "Maximum historical loss" },
  { metric: "Volatility", value: "12.4%", description: "Annual price fluctuation" },
];

interface AssetAllocationProps {
  customerId?: number | null;
}

export default function AssetAllocation({ customerId }: AssetAllocationProps) {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Asset Allocation</h1>
      </div>

      {/* Asset Allocation Tabs */}
      <Tabs defaultValue="current" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="current">Current Allocation</TabsTrigger>
          <TabsTrigger value="recommended">Recommended</TabsTrigger>
          <TabsTrigger value="custom">Custom Allocation</TabsTrigger>
        </TabsList>

        {/* Current Allocation Tab */}
        <TabsContent value="current" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Current Asset Allocation Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Current Asset Allocation</CardTitle>
                <p className="text-sm text-gray-600">Your portfolio distribution</p>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center mb-6">
                  <div className="w-80 h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={currentAllocation}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={120}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {currentAllocation.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
                <div className="space-y-3">
                  {currentAllocation.map((item) => (
                    <div key={item.name} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-4 h-4 rounded-full"
                          style={{ backgroundColor: item.color }}
                        />
                        <span className="font-medium">{item.name}</span>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">{item.value}%</p>
                        <p className="text-sm text-gray-600">{item.amount}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Allocation Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle>Allocation Breakdown</CardTitle>
                <p className="text-sm text-gray-600">By asset class</p>
              </CardHeader>
              <CardContent className="space-y-6">
                {currentAllocation.map((asset) => (
                  <div key={asset.name} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{asset.name}</span>
                      <span className="font-semibold">{asset.value}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className="h-3 rounded-full"
                        style={{ 
                          backgroundColor: asset.color,
                          width: `${asset.value}%`
                        }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-600">
                      <span>{asset.amount}</span>
                      <span>Target: {asset.value}%</span>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Performance by Asset Class */}
          <Card>
            <CardHeader>
              <CardTitle>Performance by Asset Class</CardTitle>
              <p className="text-sm text-gray-600">Returns over the past year</p>
            </CardHeader>
            <CardContent>
              <div className="h-64 mb-6">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={performanceByAsset}>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Bar dataKey="performance" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                {performanceByAsset.map((asset) => (
                  <div key={asset.name} className="text-center">
                    <h4 className="font-semibold text-sm">{asset.name}</h4>
                    <p className={`text-lg font-bold ${
                      asset.performance >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {asset.performance >= 0 ? '+' : ''}{asset.performance}%
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Recommended Allocation Tab */}
        <TabsContent value="recommended" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Recommended Allocation</CardTitle>
              <p className="text-sm text-gray-600">AI-optimized portfolio allocation based on your risk profile</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {recommendedAllocation.map((asset) => (
                  <div key={asset.name} className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h4 className="font-semibold">{asset.name}</h4>
                      <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-600">
                          Current: {asset.current}%
                        </span>
                        <span className="text-sm font-medium">
                          Recommended: {asset.recommended}%
                        </span>
                        {asset.difference !== 0 && (
                          <Badge variant={asset.difference > 0 ? "default" : "secondary"}>
                            {asset.difference > 0 ? '+' : ''}{asset.difference}%
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="relative">
                      <div className="w-full bg-gray-200 rounded-full h-4">
                        <div
                          className="h-4 bg-blue-500 rounded-full"
                          style={{ width: `${asset.current}%` }}
                        />
                      </div>
                      <div className="w-full absolute top-0">
                        <div
                          className="h-4 border-2 border-green-500 rounded-full bg-transparent"
                          style={{ width: `${asset.recommended}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">Allocation Recommendations</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Consider increasing stock allocation by 5% for higher growth potential</li>
                  <li>• Reduce cash holdings to optimize returns</li>
                  <li>• Current allocation aligns well with moderate risk profile</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Custom Allocation Tab */}
        <TabsContent value="custom" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Risk Metrics */}
            <Card>
              <CardHeader>
                <CardTitle>Risk Metrics</CardTitle>
                <p className="text-sm text-gray-600">Portfolio risk analysis</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {riskMetrics.map((metric) => (
                    <div key={metric.metric} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{metric.metric}</span>
                        <span className="font-bold text-lg">{metric.value}</span>
                      </div>
                      <p className="text-sm text-gray-600">{metric.description}</p>
                      <hr className="border-gray-200" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Allocation Tools */}
            <Card>
              <CardHeader>
                <CardTitle>Allocation Tools</CardTitle>
                <p className="text-sm text-gray-600">Customize your portfolio allocation</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-semibold mb-2">Rebalancing Needed</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Your portfolio has drifted from target allocation
                    </p>
                    <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700">
                      Auto-Rebalance Portfolio
                    </button>
                  </div>

                  <div className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-semibold mb-2">Risk Assessment</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Update your risk tolerance and investment goals
                    </p>
                    <button className="w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-50">
                      Retake Risk Assessment
                    </button>
                  </div>

                  <div className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-semibold mb-2">Custom Allocation</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Set your own target allocation percentages
                    </p>
                    <button className="w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-50">
                      Customize Allocation
                    </button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
