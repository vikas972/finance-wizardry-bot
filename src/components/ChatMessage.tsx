import { cn } from "@/lib/utils";
import { MessageCircle, Bot } from "lucide-react";

interface ChatMessageProps {
  message: string;
  isAi: boolean;
  timestamp: string;
}

export const ChatMessage = ({ message, isAi, timestamp }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex w-full gap-4 p-6 animate-fade-up",
        isAi ? "bg-accent/50 backdrop-blur-sm" : "bg-background"
      )}
    >
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md",
          isAi ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"
        )}
      >
        {isAi ? <Bot size={18} /> : <MessageCircle size={18} />}
      </div>
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2">
          <span className="font-semibold">
            {isAi ? "Financial Advisor" : "You"}
          </span>
          <span className="text-sm text-muted-foreground">{timestamp}</span>
        </div>
        <div className="prose prose-sm max-w-none">
          <p className="leading-relaxed text-secondary">{message}</p>
        </div>
      </div>
    </div>
  );
};