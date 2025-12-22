import { Link } from "react-router-dom";
import { gameModes } from "../lib/consts";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";
import { useQuery } from "@tanstack/react-query";
import { getModels } from "@/api/model";
import { Input } from "./ui/input";
import { useState } from "react";

const MainMenu = () => {
  const [modelSearch, setModelSearch] = useState<string>("");

  const currentModel = "mistral";

  const { data } = useQuery({
    queryKey: ["models"],
    queryFn: () => getModels(currentModel),
  });

  const filteredModels = data?.data.filter((model) =>
    model.name.toLowerCase().includes(modelSearch.toLowerCase())
  );

  return (
    <div className="flex flex-col gap-8">
      <Card>
        <CardHeader>
          <CardTitle>Choose a game mode</CardTitle>
        </CardHeader>
        <Separator className="h-[0.5px]" />
        <CardContent className="grid gap-4 p-6 md:grid-cols-3">
          {gameModes.map((mode, idx) => (
            <Button
              key={idx}
              asChild
              className="flex-col h-32"
              variant={"outline"}
            >
              <Link to={mode.link}>
                <div className="flex gap-4">
                  <mode.Icon1 className="w-6 h-6" />
                  vs
                  <mode.Icon2 className="w-6 h-6" />
                </div>
                <p className="mt-4">{mode.name}</p>
              </Link>
            </Button>
          ))}
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex items-center justify-between gap-4 md:flex-row">
          <CardTitle>Choose a model</CardTitle>
          <Input
            placeholder="Search model..."
            className="w-48"
            value={modelSearch}
            onChange={(e) => setModelSearch(e.target.value)}
          />
        </CardHeader>
        <Separator className="h-[0.5px]" />
        <CardContent className="grid gap-4 p-6 md:grid-cols-3">
          {filteredModels?.map((model, idx) => (
            <Button key={idx} asChild className="h-32" variant={"outline"}>
              <Link to={`/vs-llm/${currentModel}/${model.name}`}>
                <p>{model.name}</p>
              </Link>
            </Button>
          ))}
        </CardContent>
      </Card>
    </div>
  );
};

export default MainMenu;
