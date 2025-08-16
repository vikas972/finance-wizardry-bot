import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Briefcase,
  BarChart3,
  PieChart,
  Newspaper,
  Star,
  Settings,
  MessageSquare,
  CreditCard,
  Bot
} from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Portfolio",
    href: "/portfolio",
    icon: Briefcase,
  },
  {
    name: "Market Analysis",
    href: "/market",
    icon: BarChart3,
  },
  {
    name: "Asset Allocation",
    href: "/allocation",
    icon: PieChart,
  },
  {
    name: "News Intelligence",
    href: "/news",
    icon: Newspaper,
  },
  {
    name: "Recommendations",
    href: "/recommendations",
    icon: Star,
  },
  {
    name: "Credit Cards",
    href: "/credit-cards",
    icon: CreditCard,
  },
  {
    name: "Chat Assistant",
    href: "/chat",
    icon: MessageSquare,
  },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <div className="flex h-screen w-64 flex-col bg-slate-900 text-white">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-6 border-b border-slate-700">
        <div className="flex items-center justify-center w-8 h-8 bg-cyan-500 rounded-lg">
          <Bot className="w-5 h-5 text-white" />
        </div>
        <div>
          <span className="text-xl font-bold text-cyan-400">InsightAI</span>
          <span className="text-xl font-bold text-white ml-1">Invest</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-cyan-500 text-white"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              )}
            >
              <item.icon className="w-5 h-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Settings */}
      <div className="px-4 py-4 border-t border-slate-700">
        <Link
          to="/settings"
          className={cn(
            "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
            location.pathname === "/settings"
              ? "bg-cyan-500 text-white"
              : "text-slate-300 hover:bg-slate-800 hover:text-white"
          )}
        >
          <Settings className="w-5 h-5" />
          Settings
        </Link>
      </div>
    </div>
  );
}
