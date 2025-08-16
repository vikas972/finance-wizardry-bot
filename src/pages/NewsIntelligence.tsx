import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
// Temporarily using HTML select instead of Select component
import { Clock, TrendingUp, TrendingDown, Eye } from "lucide-react";

const newsArticles = [
  {
    id: 1,
    title: "Fed Signals Potential Rate Cut in Q3 as Inflation Eases",
    source: "Financial Times",
    time: "2 hours ago",
    sentiment: "positive",
    category: "economy",
    impact: "High",
    summary: "Federal Reserve officials indicated they may be ready to cut interest rates by September if inflation continues its downward trend. Markets responded positively with major indices climbing after the announcement.",
    symbols: ["JPM", "GS", "BAC"],
    marketImpact: "US"
  },
  {
    id: 2,
    title: "Apple Unveils New AI Features for iPhone, Shares Jump 3%",
    source: "Reuters",
    time: "6 hours ago",
    sentiment: "positive",
    category: "tech",
    impact: "Medium",
    summary: "Apple announced a suite of new AI-powered features for the upcoming iPhone operating system. The news sent shares up 3% as analysts predict the new capabilities could drive a significant upgrade cycle.",
    symbols: ["AAPL", "GOOGL", "MSFT"],
    marketImpact: "US"
  },
  {
    id: 3,
    title: "Global Semiconductor Shortage Expected to Ease by Q4",
    source: "Wall Street Journal",
    time: "12 hours ago",
    sentiment: "positive",
    category: "market",
    impact: "Medium",
    summary: "Industry analysts predict the global semiconductor shortage will begin to ease by the fourth quarter as new production capacity comes online. Automotive and electronics manufacturers are expected to benefit.",
    symbols: ["NVDA", "TSM", "INTC"],
    marketImpact: "US"
  },
  {
    id: 4,
    title: "Energy Sector Rallies on Rising Oil Prices",
    source: "Bloomberg",
    time: "1 day ago",
    sentiment: "positive",
    category: "energy",
    impact: "Medium",
    summary: "Oil prices surged following OPEC's announcement of extended production cuts. Energy stocks led market gains with several companies posting double-digit increases.",
    symbols: ["XOM", "CVX", "COP"],
    marketImpact: "US"
  },
  {
    id: 5,
    title: "Healthcare Stocks Under Pressure from Regulatory Concerns",
    source: "MarketWatch",
    time: "1 day ago",
    sentiment: "negative",
    category: "healthcare",
    impact: "Low",
    summary: "Healthcare stocks declined following reports of potential new regulations on drug pricing. Pharmaceutical companies were among the day's worst performers.",
    symbols: ["JNJ", "PFE", "MRK"],
    marketImpact: "US"
  }
];

const trendingTopics = [
  { topic: "AI Integration", mentions: 156, sentiment: "Bullish", change: "+23%" },
  { topic: "Interest Rates", mentions: 89, sentiment: "Mixed", change: "+12%" },
  { topic: "Semiconductor Recovery", mentions: 67, sentiment: "Bullish", change: "+34%" },
  { topic: "Green Energy", mentions: 45, sentiment: "Bullish", change: "+18%" },
  { topic: "Inflation Data", mentions: 78, sentiment: "Neutral", change: "-5%" }
];

const marketSentiment = [
  { metric: "Overall Sentiment", value: "Positive", score: 65 },
  { metric: "News Volume", value: "High", score: 82 },
  { metric: "Market Impact", value: "Moderate", score: 58 },
  { metric: "Volatility Index", value: "Low", score: 34 }
];

const aiAnalysis = [
  {
    category: "Technology",
    sentiment: "Very Positive",
    confidence: 89,
    keyDrivers: ["AI Innovation", "Earnings Growth", "Market Leadership"],
    prediction: "Continued outperformance expected"
  },
  {
    category: "Financial Services",
    sentiment: "Positive",
    confidence: 76,
    keyDrivers: ["Rate Environment", "Credit Quality", "Economic Growth"],
    prediction: "Benefiting from rate cycle"
  },
  {
    category: "Healthcare",
    sentiment: "Neutral",
    confidence: 65,
    keyDrivers: ["Regulatory Uncertainty", "Innovation Pipeline", "Demographic Trends"],
    prediction: "Mixed outlook near-term"
  }
];

interface NewsIntelligenceProps {
  customerId?: number | null;
}

export default function NewsIntelligence({ customerId }: NewsIntelligenceProps) {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">News Intelligence</h1>
        <div className="flex items-center gap-4">
          <select className="w-32 px-3 py-2 border border-gray-200 rounded-lg" defaultValue="US">
            <option value="US">US</option>
            <option value="Global">Global</option>
            <option value="Europe">Europe</option>
            <option value="Asia">Asia</option>
          </select>
          <select className="w-48 px-3 py-2 border border-gray-200 rounded-lg" defaultValue="All Categories">
            <option value="All Categories">All Categories</option>
            <option value="Economy">Economy</option>
            <option value="Technology">Technology</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Energy">Energy</option>
          </select>
        </div>
      </div>

      {/* News Intelligence Tabs */}
      <Tabs defaultValue="all-news" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="all-news">All News</TabsTrigger>
          <TabsTrigger value="trending">Trending</TabsTrigger>
          <TabsTrigger value="high-impact">High Impact</TabsTrigger>
          <TabsTrigger value="ai-analysis">AI Analysis</TabsTrigger>
        </TabsList>

        {/* All News Tab */}
        <TabsContent value="all-news" className="space-y-6">
          <div className="space-y-4">
            {newsArticles.map((article) => (
              <Card key={article.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant={
                          article.sentiment === "positive" ? "default" :
                          article.sentiment === "negative" ? "destructive" : "secondary"
                        }>
                          {article.sentiment === "positive" ? (
                            <TrendingUp className="w-3 h-3 mr-1" />
                          ) : article.sentiment === "negative" ? (
                            <TrendingDown className="w-3 h-3 mr-1" />
                          ) : null}
                          {article.sentiment}
                        </Badge>
                        <Badge variant="outline" className="capitalize">
                          {article.category}
                        </Badge>
                        <Badge variant="outline">
                          {article.category}
                        </Badge>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {article.title}
                      </h3>
                      <p className="text-gray-600 text-sm mb-3">
                        {article.summary}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>{article.source}</span>
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          <span>{article.time}</span>
                        </div>
                        <span>Market: {article.marketImpact}</span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Impact Score */}
                  <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-600">Impact Score</span>
                      <div className="flex space-x-1">
                        {[1, 2, 3, 4, 5].map((level) => (
                          <div
                            key={level}
                            className={`w-2 h-2 rounded-full ${
                              level <= (article.impact === "High" ? 4 : article.impact === "Medium" ? 3 : 2)
                                ? "bg-red-500"
                                : "bg-gray-300"
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {article.symbols.map((symbol) => (
                        <Badge key={symbol} variant="outline" className="text-xs">
                          {symbol}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Trending Tab */}
        <TabsContent value="trending" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Trending Topics</CardTitle>
              <p className="text-sm text-gray-600">Most discussed topics in financial news</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {trendingTopics.map((topic) => (
                  <div
                    key={topic.topic}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                  >
                    <div className="flex items-center gap-4">
                      <div>
                        <h4 className="font-semibold">{topic.topic}</h4>
                        <p className="text-sm text-gray-600">{topic.mentions} mentions</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge variant={
                        topic.sentiment === "Bullish" ? "default" :
                        topic.sentiment === "Bearish" ? "destructive" : "secondary"
                      }>
                        {topic.sentiment}
                      </Badge>
                      <span className={`font-medium ${
                        topic.change.startsWith('+') ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {topic.change}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* High Impact Tab */}
        <TabsContent value="high-impact" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Market Sentiment */}
            <Card>
              <CardHeader>
                <CardTitle>Market Sentiment</CardTitle>
                <p className="text-sm text-gray-600">Real-time sentiment analysis</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {marketSentiment.map((item) => (
                    <div key={item.metric} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{item.metric}</span>
                        <span className="font-semibold">{item.value}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="h-2 bg-blue-500 rounded-full"
                          style={{ width: `${item.score}%` }}
                        />
                      </div>
                      <div className="text-right text-sm text-gray-600">
                        {item.score}%
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* High Impact News */}
            <Card>
              <CardHeader>
                <CardTitle>High Impact Events</CardTitle>
                <p className="text-sm text-gray-600">Events with significant market impact</p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {newsArticles.filter(article => article.impact === "High").map((article) => (
                    <div
                      key={article.id}
                      className="p-4 border border-gray-200 rounded-lg"
                    >
                      <h4 className="font-semibold mb-2">{article.title}</h4>
                      <p className="text-sm text-gray-600 mb-2">{article.summary}</p>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{article.source} • {article.time}</span>
                        <Badge variant="destructive">High Impact</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* AI Analysis Tab */}
        <TabsContent value="ai-analysis" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>AI Sentiment Analysis</CardTitle>
              <p className="text-sm text-gray-600">Machine learning-powered market analysis</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {aiAnalysis.map((analysis) => (
                  <div
                    key={analysis.category}
                    className="p-6 border border-gray-200 rounded-lg"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-semibold">{analysis.category}</h4>
                      <div className="flex items-center gap-2">
                        <Badge variant={
                          analysis.sentiment.includes("Positive") ? "default" :
                          analysis.sentiment.includes("Negative") ? "destructive" : "secondary"
                        }>
                          {analysis.sentiment}
                        </Badge>
                        <span className="text-sm text-gray-600">
                          {analysis.confidence}% confidence
                        </span>
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <h5 className="font-medium mb-2">Key Drivers:</h5>
                      <div className="flex flex-wrap gap-2">
                        {analysis.keyDrivers.map((driver) => (
                          <Badge key={driver} variant="outline">
                            {driver}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <h5 className="font-medium mb-1">AI Prediction:</h5>
                      <p className="text-sm text-gray-700">{analysis.prediction}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
