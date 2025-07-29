
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


const { contextBridge, ipcRenderer } = require('electron/renderer')

contextBridge.exposeInMainWorld('hyploadAPI', {

  minimize: () => ipcRenderer.send('minimize'),
  maximize: () => ipcRenderer.send('maximize'),
  close: () => ipcRenderer.send('close'),

  onErrorXattr: (goToErrorXattr) => ipcRenderer.on('errorXattr', () => goToErrorXattr()),

  open : (link) => ipcRenderer.send("open", link),

  getOptions: () => ipcRenderer.invoke('get-options'),
  getText: (key, lang) => ipcRenderer.invoke('get-text', key, lang),

  isAlreadyDownloaded: (title, only_audio) => ipcRenderer.invoke('is-already-downloaded', title, only_audio),

  switchColorMode: () => ipcRenderer.invoke("switch-color-mode"),
  switchMode: () => ipcRenderer.invoke("switch-mode"),

  setNewLink: (link, title) => ipcRenderer.invoke("set-new-link", link, title),
  getPlaylistLinks: () => ipcRenderer.invoke("get-playlist-links"),
  
  changeLanguage: (lang) => ipcRenderer.invoke("change-language", lang),
  changeResolution: (res) => ipcRenderer.send("change-resolution", res),

  download: (listLinks) => ipcRenderer.invoke('download', listLinks),
  loadPlaylist: (link) => ipcRenderer.invoke('load-playlist', link),

  stopCmd: () => ipcRenderer.send("stop-current-cmd"),

  onProgressUpdate: (callback) => ipcRenderer.on('update-progress-bar', (e, value, message) => callback(value, message)),
  onNewVideoData: (callback) => ipcRenderer.on('video-data-transmitter', (e, videoData) => callback(videoData))
})