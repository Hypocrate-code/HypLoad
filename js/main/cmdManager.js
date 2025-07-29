
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


const sharedState = require("./sharedState");
const treeKill = require('tree-kill');

async function stopCmd() {
    if (sharedState.currentProcess) {
        treeKill(sharedState.currentProcess, (err) => { 
            if (err) {
                console.log("Erreur en voulant kill.");
            }
            else {
                console.log("Correctement kill.");
            }
         })
        sharedState.currentProcess = null;
    }
}

module.exports = {
    stopCmd
};