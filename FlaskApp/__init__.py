from flask import Flask
from datetime import datetime
app = Flask(__name__)

def days_hours_minutes_seconds(td):
	import re
	time = re.findall(r'\d\d:\d\d:\d\d', str(td))[0]
	hours, minutes, seconds = time.split(":")
	days = td.days
	return "{} päivää, {} tuntia, {} minuuttia, {} sekunttia".format(days, hours, minutes, seconds)



@app.route("/")
def hello():
    today = datetime.now()
    future = datetime(2018, 12, 14, hour=10, minute=20)

    html = """
<!DOCTYPE HTML> 
<HTML> 
<HEAD> 
<TITLE>Päivä laskuri</TITLE> 
<STYLE>
p {
    font-size: 40px;
}
</STYLE>

</HEAD> 
<BODY> 
<p>Aikaa jäljellä meidän Thaimaa reissuun: %s</p>

</BODY>
</HTML>
    """
    return html % (days_hours_minutes_seconds(future - today))



if __name__ == "__main__":
    app.run()
