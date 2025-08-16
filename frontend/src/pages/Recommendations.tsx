import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
// Temporarily using HTML select instead of Select component
import { TrendingUp, TrendingDown, Star, Target, AlertCircle } from "lucide-react";

const stockRecommendations = [
  {
    symbol: "AAPL",
    company: "Apple Inc.",
    sector: "Technology",
    recommendation: "Buy",
    currentPrice: 198.45,
    targetPrice: 225,
    potential: 13.4,
    confidence: 92,
    analyst: "AI Analysis",
    reasoning: "Strong AI integration, robust ecosystem, and solid fundamentals"
  },
  {
    symbol: "MSFT",
    company: "Microsoft Corp.",
    sector: "Technology", 
    recommendation: "Buy",
    currentPrice: 428.75,
    targetPrice: 470,
    potential: 9.6,
    confidence: 88,
    analyst: "AI Analysis",
    reasoning: "Cloud dominance, AI leadership, and enterprise strength"
  },
  {
    symbol: "AMZN",
    company: "Amazon.com Inc.",
    sector: "Consumer Discretionary",
    recommendation: "Hold",
    currentPrice: 182.3,
    targetPrice: 195,
    potential: 7.0,
    confidence: 76,
    analyst: "AI Analysis",
    reasoning: "AWS growth, e-commerce resilience, but margin pressures"
  },
  {
    symbol: "NVDA",
    company: "NVIDIA Corp.",
    sector: "Technology",
    recommendation: "Buy",
    currentPrice: 118.25,
    targetPrice: 135,
    potential: 14.2,
    confidence: 85,
    analyst: "AI Analysis",
    reasoning: "AI chip demand, data center growth, and market leadership"
  },
  {
    symbol: "TSLA",
    company: "Tesla Inc.",
    sector: "Automotive",
    recommendation: "Sell",
    currentPrice: 190.5,
    targetPrice: 170,
    potential: -10.8,
    confidence: 72,
    analyst: "AI Analysis",
    reasoning: "Valuation concerns, increased competition, delivery challenges"
  },
  {
    symbol: "GOOGL",
    company: "Alphabet Inc.",
    sector: "Technology",
    recommendation: "Buy",
    currentPrice: 168.75,
    targetPrice: 185,
    potential: 9.6,
    confidence: 81,
    analyst: "AI Analysis",
    reasoning: "Search dominance, cloud growth, and AI investments"
  }
];

const portfolioRecommendations = [
  {
    type: "Rebalancing",
    priority: "High",
    action: "Reduce cash allocation by 5%",
    reason: "Current cash holding (15%) exceeds optimal allocation (10%)",
    impact: "Potential additional $6,375 in market exposure"
  },
  {
    type: "Diversification",
    priority: "Medium",
    action: "Add international exposure",
    reason: "Portfolio is heavily weighted toward US markets (85%)",
    impact: "Improved risk-adjusted returns through geographic diversification"
  },
  {
    type: "Tax Optimization",
    priority: "Medium",
    action: "Consider tax-loss harvesting",
    reason: "Opportunity to offset gains with underperforming positions",
    impact: "Potential tax savings of $2,100 - $3,500"
  },
  {
    type: "Risk Management",
    priority: "Low",
    action: "Review stop-loss orders",
    reason: "Some positions lack downside protection",
    impact: "Enhanced portfolio protection during market volatility"
  }
];

const sectorRecommendations = [
  { sector: "Technology", recommendation: "Overweight", confidence: 89, reasoning: "AI boom, digital transformation" },
  { sector: "Healthcare", recommendation: "Neutral", confidence: 65, reasoning: "Mixed regulatory environment" },
  { sector: "Energy", recommendation: "Underweight", confidence: 78, reasoning: "Transition to renewables" },
  { sector: "Financials", recommendation: "Overweight", confidence: 72, reasoning: "Rising interest rate environment" }
];

interface RecommendationsProps {
  customerId?: number | null;
}

export default function Recommendations({ customerId }: RecommendationsProps) {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">AI Recommendations</h1>
        <select className="w-48 px-3 py-2 border border-gray-200 rounded-lg" defaultValue="United States">
          <option value="United States">United States</option>
          <option value="Global">Global</option>
          <option value="Europe">Europe</option>
          <option value="Asia Pacific">Asia Pacific</option>
        </select>
      </div>

      {/* Top AI Stock Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Top AI Stock Recommendations
          </CardTitle>
          <p className="text-sm text-gray-600">
            Intelligent trading recommendations for United States market based on AI analysis
          </p>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold">Symbol</th>
                  <th className="text-left py-3 px-4 font-semibold">Company</th>
                  <th className="text-left py-3 px-4 font-semibold">Sector</th>
                  <th className="text-left py-3 px-4 font-semibold">Recommendation</th>
                  <th className="text-left py-3 px-4 font-semibold">Current Price</th>
                  <th className="text-left py-3 px-4 font-semibold">Target Price</th>
                  <th className="text-left py-3 px-4 font-semibold">Potential</th>
                </tr>
              </thead>
              <tbody>
                {stockRecommendations.map((stock) => (
                  <tr key={stock.symbol} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div className="font-semibold">{stock.symbol}</div>
                    </td>
                    <td className="py-4 px-4">
                      <div className="font-medium">{stock.company}</div>
                    </td>
                    <td className="py-4 px-4">
                      <div className="text-sm text-gray-600">{stock.sector}</div>
                    </td>
                    <td className="py-4 px-4">
                      <Badge 
                        variant={
                          stock.recommendation === "Buy" ? "default" :
                          stock.recommendation === "Hold" ? "secondary" : "destructive"
                        }
                        className={
                          stock.recommendation === "Buy" ? "bg-green-100 text-green-800" :
                          stock.recommendation === "Hold" ? "bg-yellow-100 text-yellow-800" : 
                          "bg-red-100 text-red-800"
                        }
                      >
                        {stock.recommendation}
                      </Badge>
                    </td>
                    <td className="py-4 px-4">
                      <div className="font-medium">{stock.currentPrice}</div>
                    </td>
                    <td className="py-4 px-4">
                      <div className="font-medium">{stock.targetPrice}</div>
                    </td>
                    <td className="py-4 px-4">
                      <div className={`flex items-center gap-1 font-medium ${
                        stock.potential >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stock.potential >= 0 ? (
                          <TrendingUp className="w-4 h-4" />
                        ) : (
                          <TrendingDown className="w-4 h-4" />
                        )}
                        {stock.potential >= 0 ? '+' : ''}{stock.potential}%
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Portfolio Recommendations and Sector Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-500" />
              Portfolio Recommendations
            </CardTitle>
            <p className="text-sm text-gray-600">
              Personalized suggestions to optimize your portfolio
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {portfolioRecommendations.map((rec, index) => (
                <div
                  key={index}
                  className="p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">{rec.type}</Badge>
                      <Badge 
                        variant={
                          rec.priority === "High" ? "destructive" :
                          rec.priority === "Medium" ? "default" : "secondary"
                        }
                      >
                        {rec.priority} Priority
                      </Badge>
                    </div>
                  </div>
                  <h4 className="font-semibold mb-2">{rec.action}</h4>
                  <p className="text-sm text-gray-600 mb-2">{rec.reason}</p>
                  <p className="text-sm font-medium text-blue-600">{rec.impact}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Sector Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-orange-500" />
              Sector Analysis
            </CardTitle>
            <p className="text-sm text-gray-600">
              AI-driven sector allocation recommendations
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {sectorRecommendations.map((sector) => (
                <div
                  key={sector.sector}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex-1">
                    <h4 className="font-semibold">{sector.sector}</h4>
                    <p className="text-sm text-gray-600">{sector.reasoning}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <Badge 
                        variant={
                          sector.recommendation === "Overweight" ? "default" :
                          sector.recommendation === "Neutral" ? "secondary" : "destructive"
                        }
                      >
                        {sector.recommendation}
                      </Badge>
                      <p className="text-xs text-gray-500 mt-1">
                        {sector.confidence}% confidence
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-lg mb-2">Ready to Act on These Recommendations?</h3>
              <p className="text-sm text-gray-600">
                Implement AI-driven recommendations to optimize your portfolio performance.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline">
                Download Report
              </Button>
              <Button>
                Implement Recommendations
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
