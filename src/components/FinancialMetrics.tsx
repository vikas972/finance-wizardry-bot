import { Card } from "@/components/ui/card";
import { ArrowUpRight, TrendingUp, CreditCard, Wallet, PiggyBank, AlertTriangle } from "lucide-react";
import { useEffect, useState } from "react";
import { config } from "@/config";

interface LoanEligibilityMetrics {
  eligibility_score: number;
  score_range: string;
  debt_to_income_ratio: number;
  dti_status: string;
  current_emi_load: number;
  emi_status: string;
}

interface FinancialMetricsProps {
  customerId: number;
}

export const FinancialMetrics = ({ customerId }: FinancialMetricsProps) => {
  const [metrics, setMetrics] = useState<LoanEligibilityMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${config.apiUrl}/customers/${customerId}/loan-eligibility`);
        if (response.ok) {
          const data = await response.json();
          setMetrics(data);
        }
      } catch (error) {
        console.error('Error fetching loan eligibility metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    if (customerId) {
      fetchMetrics();
    }
  }, [customerId]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="p-4 hover:shadow-lg transition-shadow animate-pulse">
            <div className="h-24 bg-gray-200 rounded"></div>
          </Card>
        ))}
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Loan Eligibility Score</p>
            <h3 className="text-2xl font-bold mt-1">{metrics.eligibility_score}</h3>
            <p className="text-xs text-primary mt-1 flex items-center">
              <ArrowUpRight size={12} className="mr-1" />
              {metrics.score_range} Range
            </p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <TrendingUp size={20} className="text-primary" />
          </div>
        </div>
      </Card>

      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Debt-to-Income Ratio</p>
            <h3 className="text-2xl font-bold mt-1">{metrics.debt_to_income_ratio.toFixed(1)}%</h3>
            <p className="text-xs text-primary mt-1">{metrics.dti_status}</p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <PiggyBank size={20} className="text-primary" />
          </div>
        </div>
      </Card>

      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Current EMI Load</p>
            <h3 className="text-2xl font-bold mt-1">{formatCurrency(metrics.current_emi_load)}</h3>
            <p className={`text-xs ${metrics.emi_status === 'Above Threshold' ? 'text-destructive' : metrics.emi_status === 'Near Threshold' ? 'text-warning' : 'text-primary'} mt-1 flex items-center`}>
              {metrics.emi_status === 'Above Threshold' && <AlertTriangle size={12} className="mr-1" />}
              {metrics.emi_status}
            </p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <CreditCard size={20} className="text-primary" />
          </div>
        </div>
      </Card>

      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Available Credit Limit</p>
            <h3 className="text-2xl font-bold mt-1">
              {formatCurrency(metrics.eligibility_score * 10000)} {/* Example calculation */}
            </h3>
            <p className="text-xs text-primary mt-1">Based on Score & Income</p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <Wallet size={20} className="text-primary" />
          </div>
        </div>
      </Card>
    </div>
  );
};