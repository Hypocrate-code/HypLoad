
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


export async function setPlaylists() {
    const btnContainer = document.querySelector('.Playlists .scrollContainer .btn-container');
    await window.hyploadAPI.getPlaylistLinks().then(data => {        
        console.log(data.length);
        console.log(data);
        if (data && Object.entries(data).length > 0) {
            console.log(data);
            btnContainer.innerHTML = "";
            for (const [link, title] of Object.entries(data)) {
                const btn = document.createElement('button');
                btn.textContent = title;
                btn.addEventListener('click', () => {
                    goTo("DownloadPlaylist", 1, null);
                    document.querySelector(".DownloadPlaylist .link-container input").value = link;
                })
                btnContainer.appendChild(btn);
            }
        }
    })
}