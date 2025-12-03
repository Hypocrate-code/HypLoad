
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

const { app } = require('electron');
const path = require('node:path');
const sharedState = require('./sharedState');
const { exec, spawn } = require('node:child_process');
const iconv = require('iconv-lite');

const PATH_TO_YT_DLP = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked' ,'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'yt-dlp.exe' : 'yt-dlp') : path.join(__dirname, '..', '..', 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'yt-dlp.exe' : 'yt-dlp');


function chunkArray(array, size = 5) {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}


async function loadPlaylist(e, link) {

    let title = "";
    let playlist_id = "";
    
    const webContents = e.sender;
    if (!link.includes("&list") && !link.includes("?list")) {
        webContents.send('update-progress-bar', "Error", "Pas un lien de playlist.");
        return;
    }
    if (link.includes("&si")) {
        link = link.substring(0, link.indexOf("&si"));
    }

    webContents.send('update-progress-bar', "Start", null);
    const cmd = exec(`${PATH_TO_YT_DLP} --skip-download --flat-playlist --print "%(title)s | %(uploader)s | %(webpage_url)s | https://i.ytimg.com/vi/%(id)s/sddefault.jpg | %(view_count)s | %(playlist)s | %(playlist_id)s | %(playlist_index)s | %(playlist_count)s | " "${link}"`,
        {
            encoding: 'buffer'
        }
    );
    sharedState.currentProcess = cmd.pid;
    
    cmd.stdout.on('data', (data) => {
        const baseString = data.toString().replaceAll(" | \n", " | ");
        const newData = baseString.split(' | ');
        newData.pop();
        const chuckOfData = chunkArray(newData, size=9)
        chuckOfData.forEach(el => {
            console.log("un el : ", el);
            const index = parseInt(el.length - 2);
            const total = parseInt(el.length - 1);
            title = el[5];
            playlist_id = el[6];
            webContents.send('update-progress-bar', ((index/total) * 100).toFixed(0));
            webContents.send('video-data-transmitter', el);
        });
    });

    
    cmd.stderr.on('data', (data) => {
        process.stderr.write(`stderr: ${data}`);
        if (data.includes("WARNING")) return;
        webContents.send('update-progress-bar', "Error", data.toString());
    });

    
    cmd.on('close', (code) => {
        console.log(`Process exited with code ${code}`);
        sharedState.currentProcess = null;
        code !== 1 && webContents.send('update-progress-bar', "toPlaylistScreen", {"link": `https://youtube.com/playlist?list=${playlist_id}`, "title": title}); 
    });

    return cmd.pid;
}

module.exports = { loadPlaylist }