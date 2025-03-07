const { app, BrowserWindow, ipcMain } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let mainWindow;
let pythonProcess;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            nodeIntegration: true,
            contextIsolation: true,
        },
    });

    mainWindow.loadURL("http://localhost:5173");

    // Start Python process with 'electron' argument
    pythonProcess = spawn("python", ["C:\\Users\\dell\\Desktop\\Abdo_ai_assistant\\main.py", "electron"], {
        stdio: ["pipe", "pipe", "pipe"]
    });

    // Set up IPC communication
    ipcMain.on('electron-ready', () => {
        
        pythonProcess.stdin.write('window_ready\n');
    });

    pythonProcess.stdout.on("data", (data) => {
        const response = data.toString().trim();
        console.log(` ${response}`); // Log to terminal for debugging
        if (mainWindow) {
            mainWindow.webContents.send("python-response", response);
        }
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Python error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        console.log(`Python process exited with code ${code}`);
    });

    mainWindow.on("closed", () => {
        if (pythonProcess) {
            pythonProcess.kill();
        }
        mainWindow = null;
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});