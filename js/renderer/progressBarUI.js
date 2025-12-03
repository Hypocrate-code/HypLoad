
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


// renderer process module

export function setProgressBarValue(value, section) {
    const progressBar = findActualPb(section);
    try {
        if (!progressBar) {
            throw new Error("Progress bar n'existe pas.");
        }
        const child = progressBar.children[0];
        if (!child) {
            throw new Error("Enfant de la progress bar n'existe pas.");
        }
        child.style.setProperty('width', value+"%");
        
    } catch (error) {
        console.log(error);
    }
}

function findActualPb(section) {
    if (!section) {
        section = document.querySelector("section.active");
    }
    const progressBar = section.querySelector('.progressDlBar');
    return progressBar;
}
