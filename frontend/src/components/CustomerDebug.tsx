import { useEffect } from "react";

interface CustomerDebugProps {
  customers: any[];
  selectedCustomerId: number | null;
}

export function CustomerDebug({ customers, selectedCustomerId }: CustomerDebugProps) {
  useEffect(() => {
    console.log("🔍 Customer Debug Info:");
    console.log("Customers:", customers);
    console.log("Selected Customer ID:", selectedCustomerId);
    console.log("Selected Customer:", customers.find(c => c.id === selectedCustomerId));
    console.log("Customers length:", customers.length);
  }, [customers, selectedCustomerId]);

  if (process.env.NODE_ENV === 'production') {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 bg-black text-white p-3 rounded-lg text-xs z-50 max-w-sm">
      <div className="font-bold mb-2">🔍 Debug Info</div>
      <div>Customers: {customers.length}</div>
      <div>Selected ID: {selectedCustomerId}</div>
      <div>Selected: {customers.find(c => c.id === selectedCustomerId)?.name || 'None'}</div>
    </div>
  );
}
