
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

export function setGateState(value, actualSection) {
    try {
        if (!actualSection) {
            actualSection = document.querySelector("section.active");
        }
        if (!actualSection.classList.contains("DownloadSingle") && !actualSection.classList.contains("DownloadPlaylist")) {
            return null;
        }

        if (!actualSection) {
            throw new Error("Pas de section active, étrange.");
        }
        
        const linkContainer = actualSection.querySelector('.link-container');
        const btn = actualSection.querySelector('.switchMode');
        const pb = actualSection.querySelector('.progressDlBar');
        
        if (!linkContainer || !btn || !pb) {
            throw new Error("L'un des éléments nécessaire au changement d'état n'existe pas, étrange.");
        }

        if (value === "loading") {
            linkContainer.classList.add('inactive');
            linkContainer.classList.remove('active');
            btn.classList.add('inactive');
            btn.classList.remove('active');
            pb.classList.add('active');
            pb.classList.remove('inactive');
        }
        else {
            linkContainer.classList.add('active');
            linkContainer.classList.remove('inactive');
            btn.classList.add('active');
            btn.classList.remove('inactive');
            pb.classList.add('inactive');
            pb.classList.remove('active');
        }
        return actualSection;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export function setP(text, actualSection) {
    try {
        if (!actualSection) {
            actualSection = document.querySelector("section.active");
        }
        if (!actualSection) {
            throw new Error("Pas de section active, étrange.");
        }
        const p = actualSection.querySelector('p');
        if (!p) {
            throw new Error("Pas de p, étrange.");
        }
        p.innerHTML = text;
    } catch (error) {
        console.log(error);
    }
}

export function resetInputValue(actualSection) {
    try {
        if (!actualSection) {
            actualSection = document.querySelector("section.active");
        }
        if (!actualSection) {
            throw new Error("Pas de section active, étrange.");
        }
        const input = actualSection.querySelector('input[type="text"]');
        input.value = "";
    } catch (error) {
        console.log(error);
    }
}

export function resetGate(direction) {

}