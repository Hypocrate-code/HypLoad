
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

const { getOptions, setOptions, getJSONFile } = require("./utils_file");

const path = require('node:path');

const AVAILABLE_LANGS = ["en", "fr"];

const TEXT_FILE_PATH = path.join(__dirname, "..","..", "data", "data.json" );

async function changeLanguage(lang) {
    if (AVAILABLE_LANGS.includes(lang)) {
        const options = await getOptions();
        if (options.lang !== lang) {
            options.lang = lang;
            setOptions(options);
            return true;
        }
        return false;
    }
    return false;
}

async function getText(e, key) {
    const options = await getOptions();
    const data = getJSONFile(TEXT_FILE_PATH)        
    // log.inf(data[options.lang][key]);
    return data[options.lang][key];
}

module.exports = { AVAILABLE_LANGS, changeLanguage, getText };