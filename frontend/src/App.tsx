import { useState, useEffect } from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "@/components/layout/Layout";
import Dashboard from "./pages/Dashboard";
import Portfolio from "./pages/Portfolio";
import MarketAnalysis from "./pages/MarketAnalysis";
import AssetAllocation from "./pages/AssetAllocation";
import NewsIntelligence from "./pages/NewsIntelligence";
import Recommendations from "./pages/Recommendations";
import ChatAssistant from "./pages/ChatAssistant";
import CreditCards from "./pages/CreditCards";
import Settings from "./pages/Settings";
import Index from "./pages/Index";
import AgentChatAssistant from "./components/AgentChatAssistant";
import { CustomerDebug } from "./components/CustomerDebug";
import { config } from "@/config";

const queryClient = new QueryClient();

interface Customer {
  id: number;
  name: string;
  email: string;
}

const App = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch customers when component mounts
  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        console.log("🔄 Fetching customers from:", `${config.apiUrl}/customers/`);
        const response = await fetch(`${config.apiUrl}/customers/`);
        if (response.ok) {
          const data = await response.json();
          console.log("✅ Customers fetched:", data);
          setCustomers(data);
          // Set first customer as default if available
          if (data.length > 0) {
            console.log("🎯 Setting default customer:", data[0].id);
            setSelectedCustomerId(data[0].id);
          }
        } else {
          console.error("❌ Failed to fetch customers:", response.status, response.statusText);
        }
      } catch (error) {
        console.error('❌ Error fetching customers:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const handleCustomerChange = (customerId: number) => {
    console.log("🔄 Customer changed to:", customerId);
    setSelectedCustomerId(customerId);
  };

  // Show loading state while fetching customers
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>Loading customers...</p>
        </div>
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Layout 
            customers={customers}
            selectedCustomerId={selectedCustomerId}
            onCustomerChange={handleCustomerChange}
          >
            <Routes>
              <Route path="/" element={<Dashboard customerId={selectedCustomerId} />} />
              <Route path="/portfolio" element={<Portfolio customerId={selectedCustomerId} />} />
              <Route path="/market" element={<MarketAnalysis customerId={selectedCustomerId} />} />
              <Route path="/allocation" element={<AssetAllocation customerId={selectedCustomerId} />} />
              <Route path="/news" element={<NewsIntelligence customerId={selectedCustomerId} />} />
              <Route path="/recommendations" element={<Recommendations customerId={selectedCustomerId} />} />
              <Route path="/chat" element={<ChatAssistant customerId={selectedCustomerId} />} />
              <Route path="/agent-chat" element={<AgentChatAssistant customerId={selectedCustomerId} />} />
              <Route path="/credit-cards" element={<CreditCards customerId={selectedCustomerId} />} />
              <Route path="/settings" element={<Settings customerId={selectedCustomerId} />} />
              <Route path="/legacy" element={<Index />} />
            </Routes>
          </Layout>
          <CustomerDebug customers={customers} selectedCustomerId={selectedCustomerId} />
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
