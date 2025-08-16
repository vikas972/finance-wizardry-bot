import { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";

interface LayoutProps {
  children: ReactNode;
  customers?: any[];
  selectedCustomerId?: number | null;
  onCustomerChange?: (customerId: number) => void;
}

export function Layout({ children, customers, selectedCustomerId, onCustomerChange }: LayoutProps) {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          customers={customers}
          selectedCustomerId={selectedCustomerId}
          onCustomerChange={onCustomerChange}
        />
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
