
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


import { setGateState, setP, resetInputValue } from "./js/renderer/gateElementManager.js";
import { setProgressBarValue } from "./js/renderer/progressBarUI.js";
import { setColorMode, switchColorMode } from "./js/renderer/colorMode.js";
import { setMusicOrVideoBtns, switchMode } from "./js/renderer/audioOrVideo.js";
import { setResolution, changeResolution} from "./js/renderer/resolution.js";
import { changeAudioFormat, setAudioFormat } from "./js/renderer/audioFormat.js";
import { setPlaylists } from "./js/renderer/savedPlaylists.js";

const playlistScreen = document.querySelector(".LoadedPlaylist");
const titleOfPlaylist = playlistScreen.querySelector('p');

window.addEventListener('DOMContentLoaded', async () => {
    // Initial setup of options
    console.log("Lancement");
    window.hyploadAPI.getOptions().then(options => {
        setColorMode(options);
        setMusicOrVideoBtns(options);
        setResolution(options);
        setAudioFormat(options);
        setPlaylists();
    }).catch(err => console.log(err));
    const body = document.querySelector('body');
    if (navigator.platform === "MacIntel") {
        body.classList.add("macOS");
    }
    setTimeout(()=>body.classList.remove('isLoading'), 777)
})

window.switchColorMode = switchColorMode;
window.switchMode = switchMode;
window.changeResolution = changeResolution;
window.changeAudioFormat = changeAudioFormat;

async function goTo(sectionName, direction, callback) {
    const newSection = document.querySelector("."+sectionName);
    if (newSection === null) return;
    const actualSection = document.querySelector("section.active");
    if (direction === -1) {
        window.hyploadAPI.stopCmd();
        actualSection.classList.add("leavingScreenRight")
        actualSection.addEventListener("animationend", async ()=> {
            callback && await callback(actualSection);
            actualSection.classList.remove("active");
            actualSection.classList.remove("leavingScreenRight")
            newSection.classList.add("enteringScreenLeft")
            newSection.classList.add("active");
            newSection.addEventListener("animationend", ()=>{
                newSection.classList.remove("enteringScreenLeft")
            }, {once: true})
        }, {once: true})
    }
    else {
        actualSection.classList.add("leavingScreenLeft");
        actualSection.addEventListener("animationend", ()=> {
            callback && callback(actualSection);
            actualSection.classList.remove("active");
            actualSection.classList.remove("leavingScreenLeft");
            newSection.classList.add("enteringScreenRight");
            newSection.classList.add("active");
            newSection.addEventListener("animationend", ()=>{
                newSection.classList.remove("enteringScreenRight");
            }, {once: true})
        }, {once: true})
    }
}
window.goTo = goTo;



async function launchDownloadSingle() {
    try {
        const actualSection = document.querySelector("section.active");
        if (!actualSection) {
            throw new Error("Section active n'existe pas, étrange.");
        }
        const input = actualSection.querySelector('input[type="text"]');
        if (!input) {
            throw new Error("Input dans section active n'existe pas, étrange sachant que cette fonction ne s'éxécute qu'ici.");
        }
        const link = input.value;
        if (link.includes("playlist?list=")) {
            setP(await hyploadAPI.getText("error_playlist_link_for_video"), actualSection)
            resetInputValue(actualSection);
        }
        else {
            window.hyploadAPI.getOptions().then(options=> window.hyploadAPI.download([[link, options.only_audio]], ''))
        }
    } catch (error) {
        console.log(error);
    }
}
window.launchDownloadSingle = launchDownloadSingle;


async function launchLoadPlaylist() {
    try {
        const actualSection = document.querySelector("section.active");
        if (!actualSection) {
            throw new Error("Section active n'existe pas, étrange.");
        }
        const input = actualSection.querySelector('input[type="text"]');
        if (!input) {
            throw new Error("Input dans section active n'existe pas, étrange sachant que cette fonction ne s'éxécute qu'ici.");
        }
        const link = input.value;

        if (!link.includes("&list") && !link.includes("?list")) {
            setP(await hyploadAPI.getText("error_video_link_for_playlist"), actualSection)
            resetInputValue(actualSection);
        }
        else {
            window.hyploadAPI.loadPlaylist(link);
        }

    } catch (error) {
        console.log(error);
    }
}
window.launchLoadPlaylist = launchLoadPlaylist;




window.hyploadAPI.onProgressUpdate(async (value, content) => {
    const section = document.querySelector("section.active");
    switch (value) {
        case "Start":
            setProgressBarValue(0);
            let textLoading = await hyploadAPI.getText("loading");
            if (content !== undefined && content !== null) {
                textLoading = `${textLoading.replace('...', ' :')} ${content} ${await hyploadAPI.getText("remaining")}`;
            } 
            setP(textLoading, section);
            setGateState("loading", section);
            break;
        case "Error":
            setP(await hyploadAPI.getText("error"), section);
            setGateState("error", section);
            resetInputValue(section);
            break;
        case "toPlaylistScreen":
            const callback = async (section) => {
                if (section && section.classList.contains("DownloadPlaylist")) {
                    setProgressBarValue(100, section);
                    resetInputValue(section);
                    setP(await hyploadAPI.getText("playlist_label"), section);
                    setGateState("end", section);
                }
            }
            goTo('LoadedPlaylist', 1, callback);
            window.hyploadAPI.setNewLink(content.link, content.title);
            setPlaylists();
            break;
        case "End":            
            setProgressBarValue(100, section);
            resetInputValue(section);
            setTimeout(async () => {
                if (section.classList.contains("DownloadPlaylist")) {
                    setP(await hyploadAPI.getText("playlist_downloaded"), section);
                }
                else {
                    setP(await hyploadAPI.getText("video_downloaded"), section);
                }
                setGateState("end");
            }, 200);
            break;
        default:
            setP(value+"%", section);
            setProgressBarValue(value, section);
            break;
    }
})




const audioSvg = `
    <svg width="99" height="84" viewBox="0 0 99 84" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 33.0368C0 28.2053 3.95752 24.2886 8.83937 24.2886H53.0362V59.2814H8.83937C3.95752 59.2814 0 55.3647 0 50.5332V33.0368Z" fill="var(--color)"/>
        <path d="M53.036 7.2778V25.2569H22.3611C40.2683 9.70832 53.036 -11.1878 53.036 7.2778Z" fill="var(--color)"/>
        <path d="M53.036 76.3433V58.3642H22.3611C40.2683 73.9128 53.036 94.8089 53.036 76.3433Z" fill="var(--color)"/>
        <path d="M65.578 21.7293C67.224 20.0494 69.901 19.957 71.6598 21.4815L71.8277 21.6344L72.1346 21.9353C75.3244 25.1178 78.9197 30.5986 80.0043 37.4107C81.1599 44.6695 79.3951 53.0692 72.0493 61.2206C70.4246 63.0234 67.6308 63.1815 65.8091 61.5737C63.9875 59.9658 63.8277 57.2008 65.4523 55.3979C71.0707 49.1635 72.0073 43.3879 71.2724 38.772C70.5495 34.2316 68.1414 30.4663 66.0806 28.3218L65.6739 27.9145L65.5147 27.7541C63.9205 26.0611 63.9318 23.4094 65.578 21.7293Z" fill="var(--color)"/>
        <path d="M80.5605 7.88614C82.3914 6.28854 85.1834 6.46234 86.7977 8.27438C96.0335 18.6418 108.781 46.2963 86.9972 74.5704C85.5171 76.4913 82.7441 76.861 80.8031 75.3962C78.8622 73.9314 78.4886 71.187 79.9687 69.266C98.3434 45.4171 87.6653 22.4747 80.1682 14.0591C78.5539 12.247 78.7295 9.48374 80.5605 7.88614Z" fill="var(--color)"/>
    </svg>
`
const videoSvg = `
    <svg width="169" height="120" viewBox="0 0 169 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="169" height="120" rx="13" fill="var(--primary-color)"/>
        <rect x="14" y="12" width="13" height="20" rx="3" fill="var(--background-of-the-app)"/>
        <rect x="14" y="88" width="13" height="20" rx="3" fill="var(--background-of-the-app)"/>
        <rect x="14" y="48" width="13" height="20" rx="3" fill="var(--background-of-the-app)"/>
        <rect x="142" y="12" width="13" height="20" rx="3" fill="var(--background-of-the-app)"/>
        <rect x="142" y="88" width="13" height="20" rx="3" fill="var(--background-of-the-app)"/>
        <rect x="142" y="48" width="13" height="20" rx="3" fill="var(--background-of-the-app)"/>
        <path d="M110.5 57.4019C112.5 58.5566 112.5 61.4434 110.5 62.5981L70 85.9808C68 87.1355 65.5 85.6921 65.5 83.3827V36.6173C65.5 34.3079 68 32.8645 70 34.0192L110.5 57.4019Z" fill="var(--background-of-the-app)"/>
    </svg>
`

window.hyploadAPI.onNewVideoData((videoData) => {
    try {
        window.hyploadAPI.getOptions().then(async (options) => {
            const videoContainer = playlistScreen.querySelector('.videoContainer');
            if (!videoContainer) {
                throw new Error("Pas de video container, bizarre.");
            }
            
            const newVideo = document.createElement('div');
            if(titleOfPlaylist) {
                titleOfPlaylist.innerHTML = `<b>HypLoad</b><br/>${videoData[5]}`;
            };

            newVideo.classList.add("video");
            newVideo.setAttribute("link", videoData[2]);

            const formatBtn = document.createElement("button");
            formatBtn.classList.add("format");
            options.only_audio && newVideo.classList.add("onlyAudio");
            formatBtn.innerHTML = options.only_audio ? audioSvg : videoSvg;
            formatBtn.addEventListener("click", ()=> {
                newVideo.classList.toggle("onlyAudio");
                formatBtn.innerHTML = newVideo.classList.contains("onlyAudio") ? audioSvg : videoSvg;
            });
            
            const toDownloadBtn = document.createElement("button");
            toDownloadBtn.classList.add("toDownload");
            toDownloadBtn.innerHTML = `
                <svg width="78" height="69" viewBox="0 0 78 69" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7.82886 35.1963C13.9473 40.6011 18.7778 45.81 24.3289 55.5C39.2331 35.7735 50.3586 22.3728 70.3289 7.69629" stroke="#E5211E" stroke-width="14" stroke-linecap="round"/>
                </svg>
            `
            const isAlready = await window.hyploadAPI.isAlreadyDownloaded(videoData[0], options.only_audio, options.only_audio ? options.audio_format : "mp4", videoData[5]);
            // console.log("isAlready");
            // console.log(isAlready);
            isAlready && newVideo.classList.add("notDownloadable");
            toDownloadBtn.addEventListener("click", ()=> {newVideo.classList.toggle("notDownloadable")});

            newVideo.innerHTML = `
            <div class="thumbnail" style="background-image: url('${videoData[3]}');" ></div>
            <div class="video-info">
                <p  class="title">${videoData[0]}</p>
                <p class="views">${Number(videoData[4]).toLocaleString()} views</p>
                <p class="uploader">${videoData[1]}</p>
            </div>
            <div class="option-container">
            </div>
            `
            const optionContainer = newVideo.querySelector('.option-container');
            optionContainer.appendChild(formatBtn);
            optionContainer.appendChild(toDownloadBtn);
            videoContainer.appendChild(newVideo);
        })
    } catch (error) {
        console.log(error);
        
    }
})



async function resetSection(section) {
    setGateState("end");
    if (section.classList.contains('DownloadSingle')) {
        resetInputValue();
        // console.log("Single download screen.");
        setP(await hyploadAPI.getText("video_label"));
    }
    else if (section.classList.contains('DownloadPlaylist')) {
        resetInputValue();
        // console.log("Playlist download screen.");
        setP(await hyploadAPI.getText("playlist_label"));
    }
    else if (section.classList.contains("LoadedPlaylist")) {
        const container = section.querySelector(".videoContainer");
        if (container) {
            container.innerHTML = '';   
        }
        else {
            console.log("Pas de videoContainer pour enlever les videos, bizarre.");
        }
    }
}
window.resetSection = resetSection;


function launchDownloadPlaylist() {
    const videos = document.querySelectorAll('.video');
    const linksToDownload = [];
    videos.forEach(video => {
        !video.classList.contains("notDownloadable") && linksToDownload.push([video.getAttribute('link'), video.classList.contains("onlyAudio")]);
    });
    // console.log(linksToDownload);
    const callback = (section) => {
        resetSection(section);
        window.hyploadAPI.download(linksToDownload, titleOfPlaylist.textContent.replace("HypLoad", ""));
    }
    goTo('DownloadPlaylist', -1, callback);
}

window.hyploadAPI.onErrorXattr(() => {goTo("ErrorXattr", 1, null)});
window.hyploadAPI.onErrorConn(() => {goTo("ErrorConn", 1, null)});

window.launchDownloadPlaylist = launchDownloadPlaylist;