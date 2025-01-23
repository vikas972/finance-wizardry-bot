import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bell, Gift, AlertCircle } from "lucide-react";

interface CardInfo {
  bank_name: string;
  card_name: string;
}

interface Update {
  id: number;
  type: string;
  title: string;
  description: string;
  valid_until: string;
}

interface GroupedUpdates {
  [key: string]: {
    card: CardInfo;
    updates: Update[];
  };
}

export function CreditCardUpdates() {
  const [groupedUpdates, setGroupedUpdates] = useState<GroupedUpdates>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUpdates();
  }, []);

  const fetchUpdates = async () => {
    try {
      const response = await fetch('http://localhost:3000/credit-cards/updates');
      if (response.ok) {
        const data = await response.json();
        setGroupedUpdates(data);
      }
    } catch (error) {
      console.error('Error fetching updates:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Card className="p-6">
        <div className="h-24 bg-muted animate-pulse rounded" />
      </Card>
    );
  }

  if (Object.keys(groupedUpdates).length === 0) {
    return (
      <Card className="p-6 text-center">
        <AlertCircle className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
        <p>No updates available at the moment</p>
      </Card>
    );
  }

  return (
    <div className="space-y-8">
      {Object.entries(groupedUpdates).map(([cardId, { card, updates }]) => (
        <div key={cardId} className="space-y-4">
          <h3 className="text-lg font-semibold">{card.bank_name} {card.card_name}</h3>
          <div className="space-y-4">
            {updates.map((update) => (
              <Card key={update.id} className="p-4">
                <div className="flex items-start gap-4">
                  {update.type === "offer" ? (
                    <Gift className="w-5 h-5 mt-1" />
                  ) : (
                    <Bell className="w-5 h-5 mt-1" />
                  )}
                  <div className="flex-1">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-semibold">{update.title}</h3>
                      </div>
                      <Badge variant={update.type === "offer" ? "default" : "secondary"}>
                        {update.type === "offer" ? "Offer" : 
                         update.type === "feature_update" ? "Feature Update" : 
                         "Promotion"}
                      </Badge>
                    </div>
                    <p className="text-sm mb-2">{update.description}</p>
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Valid until: {new Date(update.valid_until).toLocaleDateString('en-IN', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric'
                      })}</span>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
} 