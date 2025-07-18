
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


const { setOptions, getOptions } = require("./utils_file");

const AVAILABLE_CUSTOM_RES = ["1080", "720", "480", "360", "240", "144"];
const AVAILABLE_GENERIC_RES = ["bv", "wv"];

async function changeResolution(e, res) {
    if (AVAILABLE_CUSTOM_RES.includes(res) || AVAILABLE_GENERIC_RES.includes(res)) {
        getOptions().then(options => {
            options.video_res = res;
            setOptions(options);
        }).catch(err=>console.log(err));
    }
}


module.exports = { changeResolution, AVAILABLE_CUSTOM_RES, AVAILABLE_GENERIC_RES }