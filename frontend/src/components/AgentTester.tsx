import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { 
  Bot, 
  PlayCircle, 
  CheckCircle,
  XCircle,
  Loader2
} from "lucide-react";
import { agentService } from "@/services/agentService";

interface TestResult {
  test: string;
  status: 'pending' | 'success' | 'error';
  result?: any;
  error?: string;
}

export function AgentTester({ customerId }: { customerId: number }) {
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [customQuery, setCustomQuery] = useState("");

  const testCases = [
    {
      name: "Get Available Agents",
      test: () => agentService.getAvailableAgents(),
    },
    {
      name: "News Intelligence - Market Sentiment",
      test: () => agentService.chatWithAgent("news_intelligence", {
        query: "What's the current market sentiment?",
        customer_id: customerId
      }),
    },
    {
      name: "Financial Advisor - Investment Advice",
      test: () => agentService.chatWithAgent("financial_advisor", {
        query: "Should I invest $5000 in stocks?",
        customer_id: customerId
      }),
    },
    {
      name: "Credit Specialist - Credit Analysis",
      test: () => agentService.chatWithAgent("credit_card_specialist", {
        query: "How can I improve my credit score?",
        customer_id: customerId
      }),
    },
    {
      name: "Intelligent Chat Routing",
      test: () => agentService.intelligentChat(customerId, "What are the latest financial news?"),
    },
    {
      name: "Comprehensive Analysis Workflow",
      test: () => agentService.getComprehensiveAnalysis(customerId),
    },
    {
      name: "Market Analysis Workflow",
      test: () => agentService.getMarketAnalysis(),
    }
  ];

  const runAllTests = async () => {
    setIsRunning(true);
    const results: TestResult[] = testCases.map(tc => ({
      test: tc.name,
      status: 'pending'
    }));
    setTestResults(results);

    for (let i = 0; i < testCases.length; i++) {
      try {
        const result = await testCases[i].test();
        results[i] = {
          test: testCases[i].name,
          status: 'success',
          result: result
        };
      } catch (error: any) {
        results[i] = {
          test: testCases[i].name,
          status: 'error',
          error: error.message
        };
      }
      setTestResults([...results]);
    }
    setIsRunning(false);
  };

  const testCustomQuery = async () => {
    if (!customQuery.trim()) return;
    
    setIsRunning(true);
    try {
      const result = await agentService.intelligentChat(customerId, customQuery);
      setTestResults(prev => [...prev, {
        test: `Custom Query: "${customQuery}"`,
        status: 'success',
        result: result
      }]);
    } catch (error: any) {
      setTestResults(prev => [...prev, {
        test: `Custom Query: "${customQuery}"`,
        status: 'error',
        error: error.message
      }]);
    }
    setIsRunning(false);
    setCustomQuery("");
  };

  const getStatusIcon = (status: TestResult['status']) => {
    switch (status) {
      case 'pending':
        return <Loader2 className="w-4 h-4 animate-spin text-yellow-500" />;
      case 'success':
        return <CheckCircle className="w-4 h-4 text-yellow-600" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />;
    }
  };

  const getStatusBadge = (status: TestResult['status']) => {
    switch (status) {
      case 'pending':
        return <Badge variant="secondary">Running...</Badge>;
      case 'success':
        return <Badge variant="default" className="bg-yellow-500">Success</Badge>;
      case 'error':
        return <Badge variant="destructive">Failed</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="w-5 h-5" />
            Multi-Agent System Tester
          </CardTitle>
          <p className="text-sm text-gray-600">
            Test the multi-agent architecture and verify all endpoints are working correctly.
          </p>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Button 
              onClick={runAllTests} 
              disabled={isRunning}
              className="flex items-center gap-2"
            >
              <PlayCircle className="w-4 h-4" />
              {isRunning ? "Running Tests..." : "Run All Tests"}
            </Button>
            <Button variant="outline" onClick={() => setTestResults([])}>
              Clear Results
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Custom Query Test */}
      <Card>
        <CardHeader>
          <CardTitle>Custom Query Test</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder="Enter a custom query to test the intelligent routing..."
            value={customQuery}
            onChange={(e) => setCustomQuery(e.target.value)}
            rows={3}
          />
          <Button 
            onClick={testCustomQuery}
            disabled={isRunning || !customQuery.trim()}
            size="sm"
          >
            Test Custom Query
          </Button>
        </CardContent>
      </Card>

      {/* Test Results */}
      {testResults.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Test Results</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {testResults.map((result, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(result.status)}
                      <span className="font-medium">{result.test}</span>
                    </div>
                    {getStatusBadge(result.status)}
                  </div>
                  
                  {result.status === 'success' && result.result && (
                    <div className="mt-2">
                      <details className="text-sm">
                        <summary className="cursor-pointer text-blue-600 hover:text-blue-800">
                          View Response
                        </summary>
                        <pre className="mt-2 p-2 bg-gray-100 rounded text-xs overflow-x-auto">
                          {JSON.stringify(result.result, null, 2)}
                        </pre>
                      </details>
                    </div>
                  )}
                  
                  {result.status === 'error' && result.error && (
                    <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
                      <p className="text-sm text-red-600">{result.error}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
