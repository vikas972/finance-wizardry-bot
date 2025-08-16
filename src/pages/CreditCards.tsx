import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FinancialMetrics } from "@/components/FinancialMetrics";
import { CreditCardDashboard } from "@/components/CreditCardDashboard";
import { CreditCard, TrendingUp, TrendingDown, Star } from "lucide-react";

interface CreditCardsProps {
  customerId?: number | null;
}

export default function CreditCards({ customerId }: CreditCardsProps) {
  if (!customerId) {
    return (
      <div className="p-6">
        <Card className="p-8 text-center">
          <div className="flex items-center justify-center mb-4">
            <CreditCard className="w-12 h-12 text-blue-500" />
          </div>
          <h2 className="text-xl font-semibold mb-4">Credit Card Dashboard</h2>
          <p className="text-gray-600">Please select a customer to view credit card information.</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center gap-3">
        <CreditCard className="w-8 h-8 text-blue-500" />
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Credit Cards</h1>
          <p className="text-gray-600">Manage your credit cards and discover new offers</p>
        </div>
      </div>

      {/* Credit Card Tabs */}
      <Tabs defaultValue="dashboard" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
          <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          <TabsTrigger value="metrics">Financial Metrics</TabsTrigger>
        </TabsList>

        {/* Dashboard Tab */}
        <TabsContent value="dashboard" className="space-y-6">
          <CreditCardDashboard customerId={customerId} />
        </TabsContent>

        {/* Recommendations Tab */}
        <TabsContent value="recommendations" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Star className="w-5 h-5 text-yellow-500" />
                Personalized Credit Card Recommendations
              </CardTitle>
              <p className="text-sm text-gray-600">
                AI-powered recommendations based on your spending patterns and financial profile
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 border border-blue-200 bg-blue-50 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Premium Travel Card</h4>
                  <p className="text-sm text-blue-800 mb-3">
                    Based on your travel spending patterns, this card offers 3x points on travel purchases 
                    and complimentary airport lounge access.
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-green-600">95% Match Score</span>
                    </div>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
                      Learn More
                    </button>
                  </div>
                </div>

                <div className="p-4 border border-green-200 bg-green-50 rounded-lg">
                  <h4 className="font-semibold text-green-900 mb-2">Cashback Rewards Card</h4>
                  <p className="text-sm text-green-800 mb-3">
                    Perfect for your grocery and dining spending. Earn 5% cashback on rotating categories 
                    and 1.5% on all other purchases.
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-green-600">88% Match Score</span>
                    </div>
                    <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
                      Learn More
                    </button>
                  </div>
                </div>

                <div className="p-4 border border-purple-200 bg-purple-50 rounded-lg">
                  <h4 className="font-semibold text-purple-900 mb-2">Business Credit Card</h4>
                  <p className="text-sm text-purple-800 mb-3">
                    Ideal for business expenses with 2x points on office supplies and business services. 
                    Includes expense tracking tools.
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-green-600">82% Match Score</span>
                    </div>
                    <button className="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
                      Learn More
                    </button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Financial Metrics Tab */}
        <TabsContent value="metrics" className="space-y-6">
          <FinancialMetrics customerId={customerId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
