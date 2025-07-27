
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

const { spawn } = require('child_process');
const { app } = require("electron");
const path = require('node:path');
const sharedState = require('./sharedState');
const { getOptions } = require('./utils_file');
const { AVAILABLE_CUSTOM_RES } = require('./resolution');


const PATH_TO_YT_DLP = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked' ,'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'yt-dlp.exe' : 'yt-dlp') : path.join(__dirname, '..', '..', 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'yt-dlp.exe' : 'yt-dlp');
const PATH_TO_FFMPEG = app.isPackaged ? path.join(process.resourcesPath, 'app.asar.unpacked', 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'ffmpeg.exe' : 'ffmpeg') : path.join(__dirname, '..', '..', 'bin', process.platform === "win32" ? 'win' : 'mac', process.platform === "win32" ? 'ffmpeg.exe' : 'ffmpeg');

async function download(e, listLinks) {

    // console.log(listLinks);
    
    if (!listLinks || listLinks.length == 0) {
        return;
    }
    const webContents = e.sender;

    const [link, onlyAudio] = listLinks[0];
    console.log("Téléchargement lancé pour : ", link);

    webContents.send('update-progress-bar', "Start");

    const options = await getOptions();
    const videoParameters = AVAILABLE_CUSTOM_RES.includes(options.video_res) ? ["-t", "mp4","-S", `res:${options.video_res}`] : ["-t", "mp4",'-f', `${options.video_res}*+ba/b`];

    const path_to_download = path.join(onlyAudio ? app.getPath('music') : app.getPath('videos'),'HypLoad', '%(title)s.%(ext)s');
    
    console.log(path_to_download);
    console.log(PATH_TO_FFMPEG);
    console.log(PATH_TO_YT_DLP);

    const audioParameters = ['-x', "-f", "ba" , '-t', 'mp3'];
    const generalParameters = ["--embed-thumbnail", "--embed-metadata", '--no-playlist' ,"-o", path_to_download , '--ffmpeg-location', PATH_TO_FFMPEG, link]
    const finalParameters = onlyAudio ? [...audioParameters, ...generalParameters] : [...videoParameters, ...generalParameters];
    // console.log(finalParameters);
    
    const cmd = spawn(PATH_TO_YT_DLP, finalParameters); // Remplace par ta commande
    
    sharedState.currentProcess = cmd.pid;
    // const cmd = spawn(path.join(__dirname, '../bin/win/yt-dlp.exe'), [link]); // Remplace par ta commande
    cmd.stdout.on('data', (data) => {

        const baseString = data.toString();

        if (baseString.includes("[download]") && baseString.includes("ETA") && baseString.includes("%")) {

            const segmentedData = baseString.split("%")[0].split(" ");
            const progressValue = parseFloat(segmentedData[segmentedData.length - 1])
            // console.log(progressValue);
            
            // win.setProgressBar(parseFloat(progressValue));
            webContents.send('update-progress-bar', progressValue);
        }
    });

    cmd.stderr.on('data', (data) => {
        process.stderr.write(`stderr: ${data}`);
        webContents.send('update-progress-bar', "Error", data.toString());
    });
    
    cmd.on('close', (code) => {
        console.log(`Process exited with code ${code}`);
        sharedState.currentProcess = null;
        if (code !== 1) {
            listLinks.shift();
            listLinks.length === 0 ? webContents.send('update-progress-bar', "End") : download(e, listLinks);
        }
    });
    return "go !";
}



module.exports = { download };
