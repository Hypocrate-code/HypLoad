
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


const { getJSONFile, saveJSONFile } = require("./utils_file");
const { app } = require("electron");
const path = require('node:path');
const fs = require("fs");

const PLAYLISTS_FILE_PATH = path.join(app.getPath('userData'), "playlists.json");
const PLAYLISTS_DEFAULT_FILE_PATH = path.join(__dirname, "..", "..", "playlists-default.json");

async function setNewLink(e, link, title) {
    const data = await getJSONFile(PLAYLISTS_FILE_PATH);
    data[link] = title;
    saveJSONFile(PLAYLISTS_FILE_PATH, data);
}


async function getPlaylistLinks() {
    try {
        let playlistFile;
        if (!fs.existsSync(PLAYLISTS_FILE_PATH)) {
            fs.copyFileSync(PLAYLISTS_DEFAULT_FILE_PATH, PLAYLISTS_FILE_PATH);
            playlistFile = await getJSONFile(PLAYLISTS_FILE_PATH);
        }
        else {
            playlistFile = await getJSONFile(PLAYLISTS_FILE_PATH);
        }
        if (playlistFile) {
            return playlistFile;
        }
        else {
            throw new Error("playlistFile n'existe pas.");
        }
    }
    catch(e) {
        console.log("Erreur : ", e);
    }
}

module.exports = { setNewLink, getPlaylistLinks }