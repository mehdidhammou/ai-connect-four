import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AutoGame from "./components/game/auto-game";
import DefaultGame from "./components/game/default-game";
import Header from "./components/header";
import MainMenu from "./components/main-menu";
import { ThemeProvider } from "./providers/theme-provider";
import LLMGame from "./components/game/llm-game";
const App = () => {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="flex flex-col max-w-4xl min-h-screen gap-16 p-4 pt-12 mx-auto">
        <Header />
        <Router>
          <Routes>
            <Route path="/" element={<MainMenu />} />
            <Route path="/vs-heuristic/:heuristic" element={<DefaultGame />} />
            <Route path="/vs-llm/:provider/:model" element={<LLMGame />} />
            <Route path="/heuristic-vs-heuristic" element={<AutoGame />} />
          </Routes>
        </Router>
      </div>
    </ThemeProvider>
  );
};

export default App;
