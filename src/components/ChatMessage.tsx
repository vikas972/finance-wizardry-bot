import { cn } from "@/lib/utils";
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  message: string;
  isAi: boolean;
  timestamp: string;
}

export function ChatMessage({ message, isAi, timestamp }: ChatMessageProps) {
  return (
    <div
      className={cn(
        "flex w-full gap-2 p-4 border-b",
        isAi ? "bg-muted/50" : "bg-background"
      )}
    >
      <div className="flex-1">
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{message}</ReactMarkdown>
        </div>
        <div className="text-xs text-muted-foreground mt-2">
          {timestamp}
        </div>
      </div>
    </div>
  );
}