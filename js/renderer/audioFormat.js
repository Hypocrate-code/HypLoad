
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


export function setAudioFormat(options) {
    document.querySelectorAll(".ChangeFormat .btn-container button").forEach(btn=> {
        btn.classList.remove('activeFormat');
        if (btn.getAttribute('format') === options.audio_format) {
            btn.classList.add("activeFormat");
        }
    })
}

export async function changeAudioFormat(format) {
    window.hyploadAPI.changeAudioFormat(format)
    window.hyploadAPI.getOptions().then(options => {
        // console.log(options);
        setAudioFormat(options);
    });
}