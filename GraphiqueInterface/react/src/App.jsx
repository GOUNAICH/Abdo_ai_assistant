import { useEffect, useState } from "react";
import EyeWidget from "./components/EyeCanvas";

export default function App() {
  const [response, setResponse] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    if (window.electron) {
      console.log("Electron interface detected");

      // Send ready signal to main process only once
      if (!isInitialized) {
        window.electron.sendMessage('electron-ready');
        setIsInitialized(true);
      }

      // Set up listener for Python responses
      window.electron.onMessage('python-response', (data) => {
        console.log('Received from Python:', data);

        // Handle "Listening..." signal
        if (data.includes("Listening...")) {
          setIsListening(true);
          setResponse("Listening...");
        } else if (data && data.trim()) {
          setIsListening(false);
          setResponse(data.trim());
        }
      });
    } else {
      console.log("Running in browser mode - Electron interface not detected");
    }
  }, [isInitialized]);

  return (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        //background
        //backgroundImage: "url('/background.jpg')",
        //backgroundSize: "cover",
        //backgroundPosition: "center",
        //background
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden'
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
          transition: "opacity 0.3s ease"
        }}
      >
        {isListening ? "Listening..." : response}
      </div>
    </div>
  );
}