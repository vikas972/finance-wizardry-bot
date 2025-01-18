import { Card } from "@/components/ui/card";
import { ArrowUpRight, TrendingUp, CreditCard, Wallet, PiggyBank, AlertTriangle } from "lucide-react";

export const FinancialMetrics = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Loan Eligibility Score</p>
            <h3 className="text-2xl font-bold mt-1">785</h3>
            <p className="text-xs text-primary mt-1 flex items-center">
              <ArrowUpRight size={12} className="mr-1" />
              Excellent Range
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
            <h3 className="text-2xl font-bold mt-1">32%</h3>
            <p className="text-xs text-primary mt-1">Good Standing</p>
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
            <h3 className="text-2xl font-bold mt-1">₹45,000</h3>
            <p className="text-xs text-warning mt-1 flex items-center">
              <AlertTriangle size={12} className="mr-1" />
              Near Threshold
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
            <h3 className="text-2xl font-bold mt-1">₹12.5L</h3>
            <p className="text-xs text-primary mt-1">Based on Income</p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <Wallet size={20} className="text-primary" />
          </div>
        </div>
      </Card>
    </div>
  );
};