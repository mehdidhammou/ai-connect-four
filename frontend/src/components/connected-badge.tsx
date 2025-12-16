import getApiHealth from "@/api/health";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";

export default function ConnectedBadge() {
  const { isSuccess } = useQuery({
    queryKey: ["api-health"],
    queryFn: getApiHealth,
    refetchInterval: 5000,
  });

  return (
    <>
      {isSuccess ? (
        <Badge variant="secondary" className="text-green-200 bg-green-700">
          Connected
        </Badge>
      ) : (
        <Badge variant="destructive">Disconnected</Badge>
      )}
    </>
  );
}
