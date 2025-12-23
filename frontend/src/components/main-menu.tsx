import { getSolvers } from "@/api/solver";
import { SolverType } from "@/lib/types";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";
import { Input } from "./ui/input";
import { useNavigate } from "react-router-dom";

const MainMenu = () => {
  const navigate = useNavigate();
  const [solverSearch, setSolverSearch] = useState<string>("");

  const { data: solvers } = useQuery({
    queryKey: ["solvers"],
    queryFn: getSolvers,
  });

  const filteredSolvers = solvers?.filter((s) =>
    s.name.toLowerCase().includes(solverSearch.toLowerCase())
  );

  const solversByType = filteredSolvers?.reduce<
    Partial<Record<SolverType["type"], SolverType[]>>
  >((acc, s) => {
    (acc[s.type] ??= []).push(s);
    return acc;
  }, {});

  return (
    <div className="flex flex-col gap-8">
      <Input
        placeholder="Search solvers..."
        className="w-48"
        value={solverSearch}
        onChange={(e) => setSolverSearch(e.target.value)}
      />
      {solversByType &&
        Object.entries(solversByType).map(([type, solvers]) => (
          <Card key={type}>
            <CardHeader>
              <CardTitle>
                Choose a {type.charAt(0).toUpperCase() + type.slice(1)} solver
              </CardTitle>
            </CardHeader>
            <Separator className="h-[0.5px]" />
            <CardContent className="grid gap-4 p-6 md:grid-cols-3">
              {solvers!.map((s) => (
                <Button
                  key={s.name}
                  variant="outline"
                  className="py-12"
                  onClick={() => navigate(`/play/${type}/${s.name}`)}
                >
                  {s.name}
                </Button>
              ))}
            </CardContent>
          </Card>
        ))}
    </div>
  );
};

export default MainMenu;
