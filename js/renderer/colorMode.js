
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


export function setColorMode(options) {
    const colorModeBtn = document.querySelector("button#colorMode");
    if (!colorModeBtn || !options || !options.lang) {return;}
    switch (options.lang) {
        case "fr":
            colorModeBtn.innerText = `Mode ${options.color_mode === "light" ? "clair" : "sombre"}`;
            break;
        default:
            colorModeBtn.innerText = `${options.color_mode} mode`;
            break;
    }
    document.querySelector("html").setAttribute("style", `--primary-color: var(--${options.color_mode}-primary-color); --background-of-the-app: var(--${options.color_mode}-background-of-the-app);`);
}

export async function switchColorMode() {
    window.hyploadAPI.switchColorMode().then(options => {
        setColorMode(options);
    });
}