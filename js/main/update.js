const { spawn } = require('child_process');

function updateYTDLP(PATH_TO_YT_DLP, currentWin) {
    // Chmod yt-dlp and ffmpeg
    const update_yt_dlp = spawn(PATH_TO_YT_DLP, ["-U"]);

    // Logging data updating yt-dlp
    // update_yt_dlp.stdout.on('data', (data) => {
    //   console.log(`stdout ytlp: ${data}`);
    // });

    // Error handling and logging for updating yt-dlp
    // update_yt_dlp.stderr.on('data', (data) => {
    //   console.log(`stderr ytlp: ${data}`);
    // });

    update_yt_dlp.on('close', (code) => {
      if (code === 100) {
        console.log("No internet connexion");
        currentWin.webContents.send("errorConn");
      }
      else if (code === 0) {
        console.log("YtDlp upgraded correctly.");
      }
      else {
        console.log("Untreated code : ", code);
      }
    });
}

module.exports = { updateYTDLP }