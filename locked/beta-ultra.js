javascript: (async (e) => {
  console.log(document.location, document.referrer);
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));
  
  var date = new Date();
  var tomorrow = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 30, 0, 0);

  if (
    document.referrer.includes("doughcookie.glitch.me") ||
    location.hostname == "doughcookie.glitch.me" ||
    location.hostname == ""
  ) {
    for (
      var o = 30 * (parseInt(99) || 1),
        t = new Date(2e14).toUTCString(),
        n = location.hostname.split(".").slice(-2).join("."),
        r = 0;
      r < 200;
      r++
    )
      document.cookie = `cd${r}=${encodeURIComponent(
        btoa(
          String.fromCharCode.apply(
            0,
            crypto.getRandomValues(new Uint8Array(o))
          )
        )
      ).substring(0, o)};expires=${t};domain=${n};path=/`;

    await delay(200);

    if (document.location == "about:srcdoc")
      window.open("https://doughcookie.glitch.me/doughsuccess");
    parent.location = "https://doughcookie.glitch.me/doughsuccess";
  }
})();
