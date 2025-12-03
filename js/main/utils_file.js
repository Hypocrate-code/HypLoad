
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


// main process module
const path = require('node:path');
const fs = require("fs");
const { app } = require("electron");
const { platform } = require('node:os');

const OPTIONS_FILE_PATH = path.join(app.getPath('userData'), "config.json");
const OPTIONS_DEFAULT_FILE_PATH = path.join(__dirname, "..", "..", "config-default.json");

function getJSONFile(file) {
  try {
    let data = JSON.parse(fs.readFileSync(file, 'utf-8'));
    return data;
  }
  catch (e) {
    console.log("Erreur durant la lecture du fichier ", file, ": ", e); 
  }
}

function saveJSONFile(file, data) {
  try {
    fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf-8');
  }
  catch (e) {
    console.log("Erreur durant l'écriture du fichier ", file, ": ", e); 
  }
}


async function getOptions (e) {
  try {
    let optionsFile;
    if (!fs.existsSync(OPTIONS_FILE_PATH)) {
      fs.copyFileSync(OPTIONS_DEFAULT_FILE_PATH, OPTIONS_FILE_PATH);
      optionsFile = await getJSONFile(OPTIONS_FILE_PATH);
    }
    else {
      console.log("Get config.json, file exists");
      optionsFile = await getJSONFile(OPTIONS_FILE_PATH);
    }
    if (optionsFile) {
      return optionsFile;
    }
    else {
      throw new Error("optionsFile n'existe pas.");
    }
  }
  catch(e) {
    console.log("Erreur : ", e);
  }
}

function setOptions (options) {
  saveJSONFile(OPTIONS_FILE_PATH, options);
}

async function isAlreadyDownloaded(e, title, onlyAudio, format, playlistName) {
  if (platform() === "darwin") {title = sanitizeFilename(title)}
  const isPath = path.join(onlyAudio ? app.getPath('music') : app.getPath('videos'),'HypLoad', sanitizeFolderName(playlistName),`${title}.${format}`);;  
  return new Promise((resolve) => {
    fs.access(isPath, fs.constants.F_OK, (err) => {
      if (err) {
          console.log('File doesnt exist', title);
          resolve(false);
        } else {
          console.log('File exists', title);
          resolve(true);
        }
      });
  })
}


function sanitizeFolderName(name) {
  if (platform() === "darwin") {return sanitizeFilename(name)}
  else {
    const forbidden = /[<>:"/\\|?*\x00-\x1F]/g;
    const reserved = /^(con|prn|aux|nul|com[1-9]|lpt[1-9])$/i;
    let cleaned = name.replace(forbidden, "_").trim();
    cleaned = cleaned.replace(/[ .]+$/g, "");
    if (reserved.test(cleaned)) {
      cleaned += "_playlist";
    }
    if (!cleaned.length) {
      cleaned = "";
    }
    return cleaned;
  }
}

function sanitizeFilename(str) {
  const map = {
    '/': '／',
    '\\': '＼',
    ':': '：',
    '*': '＊',
    '?': '？',
    '"': '＂',
    '<': '＜',
    '>': '＞',
    '|': '｜'
  };

  return str.replace(/[\/\\:\*\?"<>|]/g, m => map[m]);
}




module.exports = { getOptions, setOptions, isAlreadyDownloaded, getJSONFile, saveJSONFile, sanitizeFolderName };