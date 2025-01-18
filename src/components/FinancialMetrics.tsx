import { Card } from "@/components/ui/card";
import { ArrowUpRight, TrendingUp, CreditCard, Wallet } from "lucide-react";

export const FinancialMetrics = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4">
      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Credit Score</p>
            <h3 className="text-2xl font-bold mt-1">750</h3>
            <p className="text-xs text-primary mt-1 flex items-center">
              <ArrowUpRight size={12} className="mr-1" />
              +15 pts this month
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
            <p className="text-sm text-muted-foreground">Monthly Income</p>
            <h3 className="text-2xl font-bold mt-1">₹85,000</h3>
            <p className="text-xs text-primary mt-1">Last updated: Today</p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <Wallet size={20} className="text-primary" />
          </div>
        </div>
      </Card>

      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Total EMIs</p>
            <h3 className="text-2xl font-bold mt-1">₹25,000</h3>
            <p className="text-xs text-primary mt-1">3 active loans</p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <CreditCard size={20} className="text-primary" />
          </div>
        </div>
      </Card>

      <Card className="p-4 hover:shadow-lg transition-shadow">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-muted-foreground">Savings Rate</p>
            <h3 className="text-2xl font-bold mt-1">28%</h3>
            <p className="text-xs text-primary mt-1">Above average</p>
          </div>
          <div className="bg-primary/10 p-2 rounded-full">
            <TrendingUp size={20} className="text-primary" />
          </div>
        </div>
      </Card>
    </div>
  );
};