
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

// Log file thanks to ChatGPT to log on macOS errors

const fs = require('fs');
const path = require('path');

// Définir le chemin du fichier log dans un dossier accessible en écriture
const logDir = path.join(require('os').homedir(), 'Library', 'Logs', 'HypLoad');
const logFile = path.join(logDir, 'app.log');

// S'assurer que le dossier existe
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// Stream d’écriture
const logStream = fs.createWriteStream(logFile, { flags: 'a' });

// Rediriger console.log et console.error
const log = (...args) => {
  const message = `[${new Date().toISOString()}] ${args.join(' ')}\n`;
  logStream.write(message);
};

console.log = log;
console.error = (...args) => log('[ERROR]', ...args);

// Exporter une fonction si tu veux l'utiliser ailleurs
module.exports = {
  log,
};
