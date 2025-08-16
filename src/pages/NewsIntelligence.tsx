import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
// Temporarily using HTML select instead of Select component
import { Clock, TrendingUp, TrendingDown, Eye, RefreshCw } from "lucide-react";
import { config } from "@/config";

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

interface NewsArticle {
  id: number;
  title: string;
  url: string;
  source: string;
  published_date: string;
  snippet: string;
  category: string;
  sentiment_score: number;
  sentiment_label: string;
  impact_score: number;
  symbols: string[];
  keywords: string[];
  market_region: string;
}

interface TrendingTopic {
  topic: string;
  mentions: number;
  sentiment: string;
  change: string;
}

interface MarketSentimentMetric {
  metric: string;
  value: string;
  score: number;
}

export default function NewsIntelligence({ customerId }: NewsIntelligenceProps) {
  const [newsArticles, setNewsArticles] = useState<NewsArticle[]>([]);
  const [trendingTopics, setTrendingTopics] = useState<TrendingTopic[]>([]);
  const [marketSentiment, setMarketSentiment] = useState<MarketSentimentMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("All Categories");
  const [selectedRegion, setSelectedRegion] = useState("US");

  // Fetch news data
  const fetchNewsData = async () => {
    try {
      setLoading(true);
      
      // Fetch news articles
      const newsResponse = await fetch(`${config.apiUrl}/news/?limit=20`);
      if (newsResponse.ok) {
        const newsData = await newsResponse.json();
        setNewsArticles(newsData);
      }

      // Fetch trending topics
      const trendingResponse = await fetch(`${config.apiUrl}/news/trending`);
      if (trendingResponse.ok) {
        const trendingData = await trendingResponse.json();
        setTrendingTopics(trendingData);
      }

      // Fetch market sentiment
      const sentimentResponse = await fetch(`${config.apiUrl}/news/sentiment`);
      if (sentimentResponse.ok) {
        const sentimentData = await sentimentResponse.json();
        setMarketSentiment(sentimentData.market_metrics || []);
      }

    } catch (error) {
      console.error('Error fetching news data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Update news feed
  const updateNewsFeed = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${config.apiUrl}/news/update`, {
        method: 'POST'
      });
      if (response.ok) {
        // Refresh the data after update
        await fetchNewsData();
      }
    } catch (error) {
      console.error('Error updating news feed:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNewsData();
  }, []);

  // Filter articles based on selected category
  const filteredArticles = selectedCategory === "All Categories" 
    ? newsArticles 
    : newsArticles.filter(article => 
        article.category.toLowerCase() === selectedCategory.toLowerCase()
      );

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">News Intelligence</h1>
        <div className="flex items-center gap-4">
          <select 
            className="w-32 px-3 py-2 border border-gray-200 rounded-lg" 
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
          >
            <option value="US">US</option>
            <option value="Global">Global</option>
            <option value="Europe">Europe</option>
            <option value="Asia">Asia</option>
          </select>
          <select 
            className="w-48 px-3 py-2 border border-gray-200 rounded-lg" 
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="All Categories">All Categories</option>
            <option value="Economy">Economy</option>
            <option value="Technology">Technology</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Energy">Energy</option>
            <option value="Financial">Financial</option>
            <option value="Markets">Markets</option>
          </select>
          <Button 
            onClick={updateNewsFeed}
            disabled={loading}
            variant="outline"
            size="sm"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Updating...' : 'Update Feed'}
          </Button>
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
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="w-6 h-6 animate-spin mr-2" />
              <span>Loading news articles...</span>
            </div>
          ) : filteredArticles.length === 0 ? (
            <Card className="p-8 text-center">
              <h3 className="text-lg font-semibold mb-2">No news articles found</h3>
              <p className="text-gray-600 mb-4">Try updating the news feed or adjusting your filters.</p>
              <Button onClick={updateNewsFeed} variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Update News Feed
              </Button>
            </Card>
          ) : (
            <div className="space-y-4">
              {filteredArticles.map((article) => (
              <Card key={article.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant={
                          article.sentiment_label === "positive" ? "default" :
                          article.sentiment_label === "negative" ? "destructive" : "secondary"
                        }>
                          {article.sentiment_label === "positive" ? (
                            <TrendingUp className="w-3 h-3 mr-1" />
                          ) : article.sentiment_label === "negative" ? (
                            <TrendingDown className="w-3 h-3 mr-1" />
                          ) : null}
                          {article.sentiment_label}
                        </Badge>
                        <Badge variant="outline" className="capitalize">
                          {article.category}
                        </Badge>
                        <Badge variant="outline">
                          Impact: {Math.round(article.impact_score * 100)}%
                        </Badge>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {article.title}
                      </h3>
                      <p className="text-gray-600 text-sm mb-3">
                        {article.snippet}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>{article.source}</span>
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          <span>{new Date(article.published_date).toLocaleString()}</span>
                        </div>
                        <span>Market: {article.market_region}</span>
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
                              level <= Math.ceil(article.impact_score * 5)
                                ? "bg-red-500"
                                : "bg-gray-300"
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {article.symbols && article.symbols.map((symbol) => (
                        <Badge key={symbol} variant="outline" className="text-xs">
                          {symbol}
                        </Badge>
                      ))}
                      {article.keywords && article.keywords.slice(0, 3).map((keyword) => (
                        <Badge key={keyword} variant="secondary" className="text-xs">
                          {keyword}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
            </div>
          )}
        </TabsContent>

        {/* Trending Tab */}
        <TabsContent value="trending" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Trending Topics</CardTitle>
              <p className="text-sm text-gray-600">Most discussed topics in financial news</p>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="flex items-center justify-center py-4">
                  <RefreshCw className="w-4 h-4 animate-spin mr-2" />
                  <span>Loading trending topics...</span>
                </div>
              ) : (
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
              )}
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
                {loading ? (
                  <div className="flex items-center justify-center py-4">
                    <RefreshCw className="w-4 h-4 animate-spin mr-2" />
                    <span>Loading market sentiment...</span>
                  </div>
                ) : (
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
                )}
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
                  {filteredArticles.filter(article => article.impact_score > 0.6).map((article) => (
                    <div
                      key={article.id}
                      className="p-4 border border-gray-200 rounded-lg"
                    >
                      <h4 className="font-semibold mb-2">{article.title}</h4>
                      <p className="text-sm text-gray-600 mb-2">{article.snippet}</p>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{article.source} • {new Date(article.published_date).toLocaleString()}</span>
                        <Badge variant="destructive">High Impact ({Math.round(article.impact_score * 100)}%)</Badge>
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
