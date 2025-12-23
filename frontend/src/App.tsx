import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Game from "./components/game/game";
import Header from "./components/header";
import MainMenu from "./components/main-menu";
import { ThemeProvider } from "./providers/theme-provider";

const App = () => {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="flex flex-col max-w-4xl min-h-screen gap-16 p-4 pt-12 mx-auto">
        <Header />
        <Router>
          <Routes>
            <Route path="/" element={<MainMenu />} />
            <Route path="/play/:solver/:name" element={<Game />} />
          </Routes>
        </Router>
      </div>
    </ThemeProvider>
  );
};

export default App;
