
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
const { getOptions, isAlreadyDownloaded } = require('./js/main/utils_file'); 
const { download } = require('./js/main/download');
const { loadPlaylist } = require('./js/main/loadPlaylist');
const { stopCmd } = require('./js/main/cmdManager');
const { switchColorMode } = require("./js/main/colorMode");
const { switchMode } = require("./js/main/audioOrVideo");
const { changeLanguage, getText } = require('./js/main/traductions');
const { changeResolution } = require('./js/main/resolution');
const { setNewLink, getPlaylistLinks } = require('./js/main/savedPlaylists');

if(require('electron-squirrel-startup')) return;

const createWindow = () => {
  const win = new BrowserWindow({
    width: 404,
    minWidth: 390,
    height: 574,
    minHeight: 550,
    titleBarOverlay: false,
    icon: "assets/icon.png",
    titleBarStyle: "hidden",
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
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
  
  const win = createWindow();
  
  ipcMain.on('minimize', () => win.minimize())
  ipcMain.on('maximize', () => win.isMaximized() ? win.unmaximize() : win.maximize())
  ipcMain.on('close', () => win.close())
  ipcMain.handle('change-language', (e, link) => {
    changeLanguage(link).then(is => is && getOptions().then(options => {
      win.loadFile(`html/index_${options.lang}.html`);
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
