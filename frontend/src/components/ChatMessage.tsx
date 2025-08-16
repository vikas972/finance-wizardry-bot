import { cn } from "@/lib/utils";
import ReactMarkdown from 'react-markdown';
import { Loader2 } from "lucide-react";

interface ChatMessageProps {
  message: string;
  isAi: boolean;
  timestamp: string;
  isLoading?: boolean;
}

export function ChatMessage({ message, isAi, timestamp, isLoading }: ChatMessageProps) {
  return (
    <div
      className={cn(
        "flex w-full gap-2 p-4 border-b",
        isAi ? "bg-muted/50" : "bg-background"
      )}
    >
      <div className="flex-1">
        {isLoading ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span>AI is thinking...</span>
          </div>
        ) : (
          <>
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown>{message}</ReactMarkdown>
            </div>
            <div className="text-xs text-muted-foreground mt-2">
              {timestamp}
            </div>
          </>
        )}
      </div>
    </div>
  );
}