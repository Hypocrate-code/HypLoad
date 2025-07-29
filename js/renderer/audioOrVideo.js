
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


export function setMusicOrVideoBtns(options) {
    const switchModeBtns = document.querySelectorAll('.switchMode');
    if (options && options.lang) {
        switchModeBtns.forEach(btn => {
            if (options.only_audio) {
                btn.innerHTML = `
                <svg width="99" height="84" viewBox="0 0 99 84" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0 33.0368C0 28.2053 3.95752 24.2886 8.83937 24.2886H53.0362V59.2814H8.83937C3.95752 59.2814 0 55.3647 0 50.5332V33.0368Z" fill="var(--color)"/>
                    <path d="M53.036 7.2778V25.2569H22.3611C40.2683 9.70832 53.036 -11.1878 53.036 7.2778Z" fill="var(--color)"/>
                    <path d="M53.036 76.3433V58.3642H22.3611C40.2683 73.9128 53.036 94.8089 53.036 76.3433Z" fill="var(--color)"/>
                    <path d="M65.578 21.7293C67.224 20.0494 69.901 19.957 71.6598 21.4815L71.8277 21.6344L72.1346 21.9353C75.3244 25.1178 78.9197 30.5986 80.0043 37.4107C81.1599 44.6695 79.3951 53.0692 72.0493 61.2206C70.4246 63.0234 67.6308 63.1815 65.8091 61.5737C63.9875 59.9658 63.8277 57.2008 65.4523 55.3979C71.0707 49.1635 72.0073 43.3879 71.2724 38.772C70.5495 34.2316 68.1414 30.4663 66.0806 28.3218L65.6739 27.9145L65.5147 27.7541C63.9205 26.0611 63.9318 23.4094 65.578 21.7293Z" fill="var(--color)"/>
                    <path d="M80.5605 7.88614C82.3914 6.28854 85.1834 6.46234 86.7977 8.27438C96.0335 18.6418 108.781 46.2963 86.9972 74.5704C85.5171 76.4913 82.7441 76.861 80.8031 75.3962C78.8622 73.9314 78.4886 71.187 79.9687 69.266C98.3434 45.4171 87.6653 22.4747 80.1682 14.0591C78.5539 12.247 78.7295 9.48374 80.5605 7.88614Z" fill="var(--color)"/>
                </svg>
                <p>${options.lang === "en" ? "Audio only" : "Audio uniquement"}</p>
                `
            }
            else {
                btn.innerHTML = `
                <svg width="169" height="120" viewBox="0 0 169 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="169" height="120" rx="13" fill="var(--color)"/>
                    <rect x="14" y="12" width="13" height="20" rx="3" fill="var(--bg-color)"/>
                    <rect x="14" y="88" width="13" height="20" rx="3" fill="var(--bg-color)"/>
                    <rect x="14" y="48" width="13" height="20" rx="3" fill="var(--bg-color)"/>
                    <rect x="142" y="12" width="13" height="20" rx="3" fill="var(--bg-color)"/>
                    <rect x="142" y="88" width="13" height="20" rx="3" fill="var(--bg-color)"/>
                    <rect x="142" y="48" width="13" height="20" rx="3" fill="var(--bg-color)"/>
                    <path d="M110.5 57.4019C112.5 58.5566 112.5 61.4434 110.5 62.5981L70 85.9808C68 87.1355 65.5 85.6921 65.5 83.3827V36.6173C65.5 34.3079 68 32.8645 70 34.0192L110.5 57.4019Z" fill="var(--bg-color)"/>
                </svg>
                <p>${options.lang === "en" ? "Audio and Video" : "Audio et Vidéo"}</p>
                `
            }
        })
    }
}

export async function switchMode() {
    window.hyploadAPI.switchMode().then(options => setMusicOrVideoBtns(options));
}