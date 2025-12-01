
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


const { FusesPlugin } = require('@electron-forge/plugin-fuses');
const { FuseV1Options, FuseVersion } = require('@electron/fuses');

module.exports = {
  packagerConfig: {
    icon: "./assets/icon.ico",
    name: "HypLoad",
    asar: {
      unpack: "**/bin/**"
    }
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      platforms: ['win32'],
      config: {
        loadingGif: "./assets/loading.gif",
        appDirectory: "./",
        exe: "HypLoad.exe",
        iconUrl: 'https://github.com/Hypocrate-code/HypLoad/blob/main/assets/icon.ico?raw=true',
        setupIcon: './assets/icon.ico',
        noMsi: false
      },
    },
    // {
    //   name: '@electron-forge/maker-zip',
    //   platforms: ['darwin'],
    // },
    // {
    //   name: '@electron-forge/maker-deb',
    //   config: {
    //     options: {
    //         icon: '/assets/icon.png'
    //     }
    //   },
    // },
    // {
    //   name: '@electron-forge/maker-dmg',
    //   platforms: ['darwin'],
    //   config: {
    //     // background: './assets/icon.png',
    //     icon: "./assets/icon.icns",
    //     format: 'ULFO'
    //   }
    // },
    // {
    //   name: '@electron-forge/maker-rpm',
    //   config: {},
    // },
    // {
    //   name: '@electron-forge/maker-wix',
    //   platforms: ['win32'],
    //   config: {
    //     name: 'HypLoad',
    //     manufacturer: 'Hypocrate (Thibaut Alvoet)',
    //     version: '1.0.0',
    //     description: "A Youtube video downloader, ad free. (GUI of yt-dlp)",
    //     icon: "./assets/icon.ico",
    //     language: 1033,
    //     ui: false
    //   }
    // }
  ],
  plugins: [
    {
      name: '@electron-forge/plugin-auto-unpack-natives',
      config: {},
    },
    // Fuses are used to enable/disable various Electron functionality
    // at package time, before code signing the application
    new FusesPlugin({
      version: FuseVersion.V1,
      [FuseV1Options.RunAsNode]: false,
      [FuseV1Options.EnableCookieEncryption]: true,
      [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
      [FuseV1Options.EnableNodeCliInspectArguments]: false,
      [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
      [FuseV1Options.OnlyLoadAppFromAsar]: true,
    }),
  ],
};
