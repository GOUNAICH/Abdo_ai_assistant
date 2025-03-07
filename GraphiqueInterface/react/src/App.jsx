import { useEffect, useState } from "react";
import EyeWidget from "./components/EyeCanvas";

export default function App() {
  const [response, setResponse] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [lastUserMessage, setLastUserMessage] = useState(""); // Stocke le dernier message de l'utilisateur

  useEffect(() => {
    if (window.electron) {
      console.log("Electron interface detected");

      if (!isInitialized) {
        window.electron.sendMessage("electron-ready");
        setIsInitialized(true);
      }

      window.electron.onMessage("python-response", (data) => {
        console.log("Received from Python:", data);

        if (data.includes("Listening...")) {
          setIsListening(true);
          setResponse("Listening...");
        } else if (data && data.trim()) {
          setIsListening(false);
          setResponse(`${data.trim()}`);
        }
      });

      // Capture user's messages (assume there's an event)
      window.electron.onMessage("user-message", (message) => {
        setLastUserMessage(`User: ${message}`);
      });
    } else {
      console.log("Running in browser mode - Electron interface not detected");
    }
  }, [isInitialized]);

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      <EyeWidget />

      {/* AI Assistant Response Box */}
      <div
        style={{
          position: "fixed",
          bottom: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          background: "rgba(0, 0, 0, 0.7)",
          color: "#fff",
          padding: "10px 20px",
          borderRadius: "10px",
          fontSize: "18px",
          fontFamily: "inherit",
          maxWidth: "80%",
          wordWrap: "break-word",
          opacity: response ? 1 : 0,
          transition: "opacity 0.3s ease",
          whiteSpace: "pre-line", // Permet d'afficher les sauts de ligne
        }}
      >
        {lastUserMessage ? `${lastUserMessage}\n` : ""}
        {response}
      </div>
    </div>
  );
}
