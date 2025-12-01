const { exec } = require('child_process');
const iconv = require('iconv-lite');

const path = require('node:path');

const PATH_TO_YT_DLP = path.join(__dirname, '..', '..', 'bin', 'win' , 'yt-dlp.exe');

exec('echo riviére', (err, stdout) => {
  console.log("riviére");
  console.log(stdout);
});
exec('echo rivière', { encoding: 'buffer' }, (err, stdout) => {
  const decoded = iconv.decode(stdout, 'cp850');
  console.log('Décodé correctement :', decoded);
});
exec(
  `${PATH_TO_YT_DLP} --skip-download --flat-playlist --print "%(title)s | %(uploader)s | %(webpage_url)s" https://www.youtube.com/playlist?list=PLlBnH7YULqQog6OkqaJSPqCotkleDDLBq`,
  { encoding: 'buffer' },
  (err, stdout) => {
    const decoded = iconv.decode(stdout, 'windows1252');
    console.log(decoded);
  }
);