import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CreditCard, PiggyBank, Plane, Gift, AlertCircle } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import { CreditCardUpdates } from "./CreditCardUpdates";
import { config } from "@/config";

interface CreditCardOffer {
  id: number;
  bank_name: string;
  card_name: string;
  card_type: string;
  annual_fee: number;
  reward_points: any;
  cashback_details: any;
  travel_benefits: any;
  lifestyle_benefits: any;
  welcome_benefits: any;
}

interface CreditCardDashboardProps {
  customerId: number;
}

interface RecommendationResponse {
  customer_profile: {
    monthly_income: number;
    credit_score: number;
    preferences: any;
  };
  recommendations: string;
}

export function CreditCardDashboard({ customerId }: CreditCardDashboardProps) {
  const [recommendations, setRecommendations] = useState<string>("");
  const [allCards, setAllCards] = useState<CreditCardOffer[]>([]);
  const [comparisonCards, setComparisonCards] = useState<CreditCardOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("recommended");
  const [lastChatRecommendation, setLastChatRecommendation] = useState<string | null>(null);

  useEffect(() => {
    fetchRecommendations();
    fetchAllCards();
    // Check for stored chat recommendations
    const storedRecommendation = localStorage.getItem(`chatRecommendation_${customerId}`);
    if (storedRecommendation) {
      setLastChatRecommendation(storedRecommendation);
    }

    // Listen for new recommendations from chat
    const handleRecommendationUpdate = (event: CustomEvent<{ recommendation: string }>) => {
      setLastChatRecommendation(event.detail.recommendation);
      setActiveTab("recommended");
    };

    window.addEventListener('creditCardRecommendationUpdate', handleRecommendationUpdate as EventListener);

    return () => {
      window.removeEventListener('creditCardRecommendationUpdate', handleRecommendationUpdate as EventListener);
    };
  }, [customerId]);

  const fetchRecommendations = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/customers/${customerId}/recommend-credit-cards`, {
        method: 'POST'
      });
      if (response.ok) {
        const data: RecommendationResponse = await response.json();
        setRecommendations(data.recommendations);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const fetchAllCards = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/credit-cards/`);
      if (response.ok) {
        const data = await response.json();
        setAllCards(data);
      }
    } catch (error) {
      console.error('Error fetching cards:', error);
    } finally {
      setLoading(false);
    }
  };

  // Function to update recommendations from chat
  const updateRecommendationsFromChat = (chatRecommendation: string) => {
    setLastChatRecommendation(chatRecommendation);
    localStorage.setItem(`chatRecommendation_${customerId}`, chatRecommendation);
    setActiveTab("recommended");
  };

  const addToComparison = (card: CreditCardOffer) => {
    if (comparisonCards.length < 3) {
      setComparisonCards([...comparisonCards, card]);
    }
  };

  const removeFromComparison = (cardId: number) => {
    setComparisonCards(comparisonCards.filter(card => card.id !== cardId));
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const renderCardBenefits = (card: CreditCardOffer) => {
    return (
      <div className="space-y-2">
        {card.welcome_benefits && (
          <div className="flex items-start gap-2">
            <Gift className="w-4 h-4 mt-1" />
            <div>
              <p className="font-semibold">Welcome Benefits</p>
              <p className="text-sm text-muted-foreground">
                {typeof card.welcome_benefits === 'string' 
                  ? card.welcome_benefits 
                  : JSON.stringify(card.welcome_benefits, null, 2)}
              </p>
            </div>
          </div>
        )}
        {card.reward_points && (
          <div className="flex items-start gap-2">
            <PiggyBank className="w-4 h-4 mt-1" />
            <div>
              <p className="font-semibold">Reward Points</p>
              <p className="text-sm text-muted-foreground">
                {typeof card.reward_points === 'string'
                  ? card.reward_points
                  : `${card.reward_points.regular_spend} points per ₹100`}
              </p>
            </div>
          </div>
        )}
        {card.travel_benefits && (
          <div className="flex items-start gap-2">
            <Plane className="w-4 h-4 mt-1" />
            <div>
              <p className="font-semibold">Travel Benefits</p>
              <p className="text-sm text-muted-foreground">
                {typeof card.travel_benefits === 'string'
                  ? card.travel_benefits
                  : JSON.stringify(card.travel_benefits, null, 2)}
              </p>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderComparisonTable = () => {
    if (comparisonCards.length === 0) {
      return (
        <Card className="p-6 text-center">
          <AlertCircle className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
          <p>Add cards to compare their features</p>
        </Card>
      );
    }

    return (
      <div className="grid gap-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {comparisonCards.map(card => (
            <Card key={card.id} className="p-4">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-semibold">{card.bank_name}</h3>
                  <p className="text-sm text-muted-foreground">{card.card_name}</p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeFromComparison(card.id)}
                >
                  Remove
                </Button>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium">Annual Fee</p>
                  <p className="text-lg font-semibold">{formatCurrency(card.annual_fee)}</p>
                </div>
                {renderCardBenefits(card)}
              </div>
            </Card>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="grid gap-4">
        <Card className="p-6">
          <div className="h-24 bg-muted animate-pulse rounded" />
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Tabs defaultValue={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="recommended">Recommended Cards</TabsTrigger>
          <TabsTrigger value="all">All Cards</TabsTrigger>
          <TabsTrigger value="compare">Compare Cards</TabsTrigger>
          <TabsTrigger value="updates">Updates & Offers</TabsTrigger>
        </TabsList>

        <TabsContent value="recommended" className="space-y-4">
          {lastChatRecommendation ? (
            <Card className="p-6">
              <h2 className="text-2xl font-semibold mb-4">Recent Chat Recommendations</h2>
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown>{lastChatRecommendation}</ReactMarkdown>
              </div>
              {recommendations && (
                <>
                  <div className="my-6 border-t" />
                  <h2 className="text-2xl font-semibold mb-4">General Recommendations</h2>
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{recommendations}</ReactMarkdown>
                  </div>
                </>
              )}
            </Card>
          ) : recommendations ? (
            <Card className="p-6">
              <h2 className="text-2xl font-semibold mb-4">Personalized Recommendations</h2>
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown>{recommendations}</ReactMarkdown>
              </div>
            </Card>
          ) : (
            <Card className="p-6 text-center">
              <AlertCircle className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
              <p>No recommendations available. Try asking for recommendations in the chat!</p>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="all" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {allCards.map(card => (
              <Card key={card.id} className="p-4">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-semibold">{card.bank_name}</h3>
                    <p className="text-sm text-muted-foreground">{card.card_name}</p>
                  </div>
                  <Badge>{card.card_type}</Badge>
                </div>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium">Annual Fee</p>
                    <p className="text-lg font-semibold">{formatCurrency(card.annual_fee)}</p>
                  </div>
                  {renderCardBenefits(card)}
                  <Button
                    className="w-full"
                    onClick={() => addToComparison(card)}
                    disabled={comparisonCards.length >= 3 || comparisonCards.some(c => c.id === card.id)}
                  >
                    Add to Compare
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="compare" className="space-y-4">
          {renderComparisonTable()}
        </TabsContent>

        <TabsContent value="updates" className="space-y-4">
          <CreditCardUpdates />
        </TabsContent>
      </Tabs>
    </div>
  );
} 