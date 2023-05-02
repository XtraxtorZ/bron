import requests
import json
import random
import base64
import os

from flask import *
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_cors import CORS, cross_origin

maintenance_mode = False
disab_glob = False
fmaintenance_mode = False

app = Flask(__name__)
app.secret_key = os.environ["secret_key"]

login_manager = LoginManager()
login_manager.init_app(app)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

def increment_count():
    filename = "datastore/count"
    with open(filename, "r") as f:
        count = int(f.read())
    count += 1
    with open(filename, "w") as f:
        f.write(str(count))
    return count

code_snippets = [
    'chrome.tabs.query({url:"*://*.google.com/*"},(e)=>{for (var o = 0; o < e.length; o++){chrome.tabs.remove(e.id)}});\n // Note that if you ran such of this on on a extension, you\'ll be hardly trolled',
    "alert(navigator.userAgent)",
    "let myArray = [1, 2, 3, 4, 5];\nfor (let i = 0; i < myArray.length; i++) { console.log(myArray[i]); }",
    "chrome.management",
    "let myObject = { name: 'John', age: 30, city: 'New York' };",
    "let myMap = new Map([['name', 'John'], ['age', 30]]);",
    'const Trolled = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; location = Trolled\n// btw, I actually like the song',
    "from flask import *",
    ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+.",
    """const concatenator = (originalStr) => { return (strTwo) => { return `${originalStr} ${strTwo}`; }; }
  console.log(concatenator('hello')('world'));
  """,
    "console.log(1 && 0 === 1 || 0); // 🤯",
    "console.log(1 ?? 0 == 1 ? 0 : null); // 🤯",
]

announcement = """
<script src="//cdn.jsdelivr.net/npm/sweetalert2@10"></script>
<script src="//cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.js"></script>

    <div class="announcement-top-bar pcenter" role="alert">
      <p class="d-none d-md-block">Support us via an Ad Link  <button onclick="AdLink()" class="btn btn-primary">Support Us</button></p>
    </div>
    
    <script>
    function AdLink() {
      Swal.fire({
        icon: "warning",
        title: "Warning",
        html: "<p style='font-family: 'Montserrat', sans-serif; color:black!important;'>Please be aware that we do not endorse or take responsibility for any content displayed on the ad website. Additionally, we recommend that you do not install any extensions or software prompted by the ads. It is also advised to close any popups that may appear on the AdLink. Thanks for supporting us!</p>",
      }).then((result) => {
        if (result.isConfirmed) {
          location = "/generate-ad-link";
        }
      });
    }
</script>
"""


# function to make error HTML and handle errors


def make_error_page(error_code, error_message, error_name, actual_error=""):
    random_code_snippet = random.choice(code_snippets)
    error_html = (
        f'<div style="position: absolute; top: 0; left: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%; background-color: #ffffff;"><div style="background-color: #ffff; color: #721c24; padding: 10px; text-align: center; font-family: Segoe UI;"><h1 style="font-size: 40px; font-weight: 800;">{error_name}</h1><p style="font-size: 20px;">{error_message}</p><br /><h2 style="font-size: 14px; font-weight: 400; font-family: Segoe UI;">Try to guess what this code snippet does:</h2><div class="code-block"><pre><code>{random_code_snippet}</code></pre></div><div id="navigator" style="margin-top: 20px;"><button onclick="window.history.back();" style="background-color: transparent; border: none; cursor: pointer;" class="backbtn"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width: 24px; height: 24px;"><path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/></svg></button></div></div></div><style>'
        + ".backbtn { position: absolute; top: 10px; left: 10px; transform: scale(1.3); transition: 0.3s; width: 20px; } .backbtn:hover { width: 20px; position: absolute; top: 10px; left: 10px; transform: scale(1.7); } button {cursor: pointer; text-align:center;padding:15px; border:none; background-color: lightgrey; border-radius:10px; width:125px;}h2 {font-family: \"Roboto Condensed\", sans-serif;}.code-block { background-color: #f7f7f7; border: 1px solid #ddd; border-radius: 4px; padding: 10px; overflow-x: auto; } pre { margin: 0; } code { font-family: 'Courier New', Courier, monospace; font-size: 14px; }</style></div></div>"
    )
    response = make_response(
        f'<html><head><meta charset="UTF-8"><title>{error_name}</title></head><body>{error_html}</body></html>'
    )
    response.status_code = error_code
    response.headers["Content-Type"] = "text/html"
    return response
  
ALLOWED_IPS_FILE = 'datastore/history-ips.json'
def load_allowed_ips():
    try:
        with open(ALLOWED_IPS_FILE, 'r') as f:
            allowed_ips = json.load(f)
    except FileNotFoundError:
        allowed_ips = []
    return allowed_ips
  
def save_allowed_ips(allowed_ips):
    with open(ALLOWED_IPS_FILE, 'w') as f:
        json.dump(allowed_ips, f)

@app.before_first_request
def init_allowed_ips():
    app.allowed_ips = load_allowed_ips()

@app.before_request
def check_for_maintenance():
  print(request.path)
  if fmaintenance_mode and (not "/admin/" in request.path) and (not "/doughultra.js" in request.path):
    return ""
  
  if maintenance_mode and (not "/admin/" in request.path): 
    return make_error_page(503, "Maintenance Mode is enabled on the server. Check back soon.", "Maintenance")
  
  if disab_glob and ("doughultra" in request.path):
    response = make_response(send_from_directory("static", "disabled.js"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response
  
  if "doughultra" in request.path:
    message_bytes = request.headers["X-Forwarded-For"].split(",")[0].encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    ip = base64_bytes.decode("ascii")
    
    if ip in app.allowed_ips:
      response = make_response(send_from_directory("locked", "dough-history.js"))
      response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
      return response 

@app.errorhandler(404)
def page_not_found(error):
    return make_error_page(404, "Not found. What are you looking for?", "404 Not Found")


@app.errorhandler(500)
def internal_server_error(error):
    return make_error_page(
        500,
        "Something happened on the backstage, this error will be solved. This also applies for 404 pages using custom routing.",
        "500 Internal Server Error",
    )


@app.errorhandler(400)
def bad_request(error):
    return make_error_page(
        400,
        "The server can't understand what your browser told the server, or even you used Cookie Dough on our website.",
        "400 Bad Request",
    )


@app.errorhandler(414)
def uri_long(error):
    return make_error_page(
        414, '"GoGuardian Discord Unblock"', "Lol, make smaller the URI"
    )


@app.route("/")
def home():
    response = make_response(
        render_template("html/index.php", ann=Markup(announcement))
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@app.route("/index.html")
def indx():
    return redirect("https://doughcookie.glitch.me/")


@app.route("/<path:path>")
def whatever(path):
    try:
        response = make_response(
            render_template("html/" + path + ".html", ann=Markup(announcement))
        )
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, max-age=0"
        return response
    except:
        abort(404)


@app.route("/ty")
def ty():
    referrer = request.referrer
    if referrer is None or not referrer.startswith("https://cutty.app/"):
        return make_error_page(
            403,
            "To access '/ty' you have to go first to '<a href=\"https://cuty.io/CDqJQfdbWc\">https://cuty.io/CDqJQfdbWc</a>', finish the ad-link, and you will be redirected here.",
            "403 Forbidden.",
        )
    return render_template("html/thanks.html", ann=Markup(announcement))


@app.route("/static/<path:path>")
@cross_origin()
def stat(path):
    response = make_response(send_from_directory("static", path))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@app.route("/doughultra.js")
@cross_origin()
def doughscript():
    response = make_response(send_from_directory("static", "doughultra.js"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response
  
@app.route("/beta-join")
@cross_origin()
def joinbeta():
    response = make_response(render_template("html/index.html", ann=Markup(announcement)))
    response.set_cookie("is-beta", True)
    return response


@app.route("/super-error")
def super_secret_error():
    return make_error_page(200, "you just found a cool page", "Cool Super Secret Error")


@app.route("/generate-ad-link")
def generate_ad_link():
    count = increment_count()
    response = requests.get(
        f"https://api.cuty.io/quick?token=ffdf36c00b1bef14443003dc8&url=https://doughcookie.glitch.me/ty&alias={count}dcookie"
    )
    data = response.json()
    url = data["short_url"]
    return redirect(url)


def check_credentials(user, passw):
    if (user == os.environ["username"]) and (passw == os.environ["passw"]):
        return True
    else:
        return False


@app.route(
    "/admin/login/",
)
@login_manager.user_loader
def admin_login():
    auth = request.authorization
    if auth and check_credentials(auth.username, auth.password):
        response = make_response(
            render_template(
                "admin/index.html",
                saved_data=request.headers["X-Forwarded-For"].split(",")[0],
            )
        )
        return response
    else:
        return Response(
            "Invalid credentials",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )


# dict to save session fingerprints (IPs)
allowed_fingerprints = {}

@app.route("/admin/api/proveauth/<fingerprint>")
def prove_fingerprint(fingerprint):
    message_bytes = request.headers["X-Forwarded-For"].split(",")[0].encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    
    allowed_fingerprints[base64_message] = fingerprint
    return jsonify(
        {
            "success": True,
            "message": "fingerprint saved",
            "fingerprint_decoder": base64_message,
            "current_data": {
                "s1": maintenance_mode,
                "s2": fmaintenance_mode,
                "c2": disab_glob,
                "c1": base64_message in app.allowed_ips
            },
        }
    )


def maintenance(value):
  global maintenance_mode
  maintenance_mode = value == "true" and True or False
  return jsonify({ "success": True, "message": "success",})
  pass

def globally(value):
  global disab_glob
  disab_glob = value == "true" and True or False
  return jsonify({ "success": True, "message": "success",})
  pass

def history(value):
  global app
  global save_allowed_ips
  message = None
  
  message_bytes = request.headers["X-Forwarded-For"].split(",")[0].encode("ascii")
  base64_bytes = base64.b64encode(message_bytes)
  ip = base64_bytes.decode("ascii")
  
  if value == "true" and True or False:
    app.allowed_ips.append(ip)
    save_allowed_ips(app.allowed_ips)
    message = { "success": True, "message": "should be added",}
  else:
    app.allowed_ips.remove(ip)
    save_allowed_ips(app.allowed_ips)
    message = { "success": True, "message": "should be removed",}
    
  return jsonify(message)
  pass

def fmaintenance(value):
  global fmaintenance_mode
  fmaintenance_mode = value == "true" and True or False
  return jsonify({ "success": True, "message": "success",})
  pass

cases = {
    "c1": history,
    "c2": globally,
    "s1": maintenance,
    "s2": fmaintenance,
}

@app.route("/admin/api/<setting>/<value>/", methods=["POST"])
def admin_api(setting, value):
    message_bytes = request.headers["X-Forwarded-For"].split(",")[0].encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")

    if base64_message in allowed_fingerprints.keys():
      try:
        return cases[str(setting)](value)
      except Exception as e:
        print(e)
        return jsonify(
            {"success": False, "message": "something happened when saving data, " + e}
        )
    else:
        return jsonify(
            {
                "success": False,
                "message": "\nplease login again, or reload\nprob a server restart if you were alr logged in, or your IP changed",
            }
        )


if __name__ == "__main__":
    app.run()
    # dksb | 14:12 3/04
  