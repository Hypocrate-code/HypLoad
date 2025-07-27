
// HypLoad is a smart software made to download YouTube videos & playlists. Acts as a clean GUI yt-dlp.
    // Copyright (C) 2025  Hypocrate (Thibaut Alvoet)

    // This program is free software: you can redistribute it and/or modify
    // it under the terms of the GNU General Public License as published by
    // the Free Software Foundation, either version 3 of the License, or
    // (at your option) any later version.

    // This program is distributed in the hope that it will be useful,
    // but WITHOUT ANY WARRANTY; without even the implied warranty of
    // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    // GNU General Public License for more details.

    // You should have received a copy of the GNU General Public License
    // along with this program.  If not, see <https://www.gnu.org/licenses/>.

const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('node:path');
const { getOptions, isAlreadyDownloaded, saveJSONFile } = require('./js/main/utils_file'); 
const { download } = require('./js/main/download');
const { loadPlaylist } = require('./js/main/loadPlaylist');
const { stopCmd } = require('./js/main/cmdManager');
const { switchColorMode } = require("./js/main/colorMode");
const { switchMode } = require("./js/main/audioOrVideo");
const { changeLanguage, getText } = require('./js/main/traductions');
const { changeResolution } = require('./js/main/resolution');
const { setNewLink, getPlaylistLinks } = require('./js/main/savedPlaylists');
const { spawn } = require('child_process');
// require('./log');

if(require('electron-squirrel-startup')) return;

let currentWin = null;

const createWindow = () => {
  const win = new BrowserWindow({
    width: 404,
    minWidth: 390,
    height: 574,
    minHeight: 550,
    icon: "assets/icon.png",
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  if (process.platform === "win32") {
    win.titleBarOverlay = false;
    win.titleBarStyle = "hidden";
  }
  // win.webContents.openDevTools();
  win.setMenuBarVisibility(false);
  
  getOptions().then(options => {
    win.loadFile(`html/index_${options.lang}.html`);
  })

  return win;
}

app.whenReady().then(() => {
  
  // Gestion des fonctions IPC 
  ipcMain.handle('get-options', getOptions);
  ipcMain.handle('get-text', getText);
  ipcMain.handle('is-already-downloaded', isAlreadyDownloaded);
  ipcMain.handle('download', download);
  ipcMain.handle('load-playlist', loadPlaylist);
  ipcMain.handle('switch-color-mode', switchColorMode);
  ipcMain.handle('switch-mode', switchMode);
  ipcMain.handle('set-new-link', setNewLink);
  ipcMain.handle('get-playlist-links', getPlaylistLinks);
  ipcMain.on('change-resolution', changeResolution);
  ipcMain.on('stop-current-cmd', stopCmd);
  ipcMain.on('open', (e, link) => shell.openExternal(link));
  
  currentWin = createWindow();

  if (process.platform === "darwin") {
    
    const PATH_TO_YT_DLP = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked' ,'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'yt-dlp.exe' : 'yt-dlp') : path.join(__dirname, 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'yt-dlp.exe' : 'yt-dlp');
    const PATH_TO_FFMPEG = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked', 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'ffmpeg.exe' : 'ffmpeg') : path.join(__dirname, 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'ffmpeg.exe' : 'ffmpeg');
    
    saveJSONFile(path.join(app.getPath('userData'), "c.json"), { yt: PATH_TO_YT_DLP, ff: PATH_TO_FFMPEG })

    // Chmod yt-dlp and ffmpeg
    const chmod_yt_dlp = spawn("chmod", ["+x", PATH_TO_YT_DLP]);
    const chmod_ffmpeg = spawn("chmod", ["+x", PATH_TO_FFMPEG]);

    // Remove quarantine attributes
    const xattr_yt_dlp = spawn("xattr", ["-d", "com.apple.quarantine", PATH_TO_YT_DLP]);
    const xattr_ffmpeg = spawn("xattr", ["-d", "com.apple.quarantine", PATH_TO_FFMPEG]);

    // Error handling and logging for yt-dlp
    chmod_yt_dlp.stderr.on('data', (data) => {
      console.log(`stderr ytlp: ${data}`);
      app.quit();
    });

    chmod_yt_dlp.on('close', (code) => {
      console.log(`Process exited ytdlp with code ${code}`);
    });

    // Error handling and logging for ffmpeg
    chmod_ffmpeg.stderr.on('data', (data) => {
      process.stderr.write(`stderr ffmpeg: ${data}`);
      app.quit();
    });

    chmod_ffmpeg.on('close', (code) => {
      console.log(`Process ffmpeg exited with code ${code}`);
    });

    // Error handling and logging for xattr yt-dlp
    xattr_yt_dlp.stderr.on('data', (data) => {
      console.log(`stderr xattr ytlp: ${data.toString()}`);
      if (!data.toString().includes('No such xattr: com.apple.quarantine')) {
        app.quit();
      }
    });

    xattr_yt_dlp.on('close', (code) => {
      console.log(`Process xattr ytdlp exited with code ${code}`);
    });

    // Error handling and logging for xattr ffmpeg
    xattr_ffmpeg.stderr.on('data', (data) => {
      console.log(`stderr xattr ffmpeg: ${data.toString()}`);
      if (!data.toString().includes('No such xattr: com.apple.quarantine')) {
        app.quit();
      }
    });

    xattr_ffmpeg.on('close', (code) => {
      console.log(`Process xattr ffmpeg exited with code ${code}`);
    });
  }
  
  ipcMain.on('minimize', () => currentWin.minimize())
  ipcMain.on('maximize', () => currentWin.isMaximized() ? currentWin.unmaximize() : currentWin.maximize())
  ipcMain.on('close', () => currentWin.close())
  ipcMain.handle('change-language', (e, link) => {
    changeLanguage(link).then(is => is && getOptions().then(options => {
      currentWin.loadFile(`html/index_${options.lang}.html`);
    }))
  });
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    console.log("Exit HypLoad");
    app.quit()
  };
})

app.on("close", ()=>{
  currentWin = null;
  app.quit();
})