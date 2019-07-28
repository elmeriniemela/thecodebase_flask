# The Codebase


[www.thecodebase.site](http://www.thecodebase.site "www.thecodebase.site")

This website is built using Python's 
<a href="http://flask.pocoo.org/">Flask library</a> 
 and styled
<a href="https://getbootstrap.com/docs/4.1/getting-started/introduction/">Bootstrap v4.1.3.</a> 
It's  running on the laptop 
<a href="https://www.lenovo.com/fi/fi/laptops/thinkpad/t-series/ThinkPad-T480/p/22TP2TT4800">(Lenovo ThinkPad T480)</a>
    shown in the pictures. Deplyoying the server cost me only the domain name ($1.46).
    I deployed it using the following instructions:
<ul class="text-left">
    <li>
        <a href="https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps">
            How To Deploy a Flask Application on an Ubuntu VPS
        </a>
    </li>
    <li>
        <a href="https://blog.mindorks.com/how-to-convert-your-laptop-desktop-into-a-server-and-host-internet-accessible-website-on-it-part-1-545940164ab9">
            How to convert your laptop/desktop into a server and host internet accessible website on it
        </a>
    </li>
    <li>
        <a href="https://letsencrypt.org/getting-started/">
            Enabling HTTPS with Let's Encrypt
        </a>
    </li>
    <li>
        <a href="https://pythonprogramming.net/practical-flask-introduction/">
            Introduction to Practical Flask
        </a>
    </li>
    <li>
        <a href="https://github.com/thecodebasesite/apache2-conf">
            Configuring Apache2 to force WWW on HTTP host
        </a>
    </li>
    <li>
        <a href="https://www.hostinger.com/">
            Cheap domain from Hostinger
        </a>
    </li>
</ul>



![alt text](https://raw.githubusercontent.com/thecodebasesite/thecodebase/master/thecodebase.png)

Install instructions:

* `sudo apt-get install mysql-client mysql-server libmysqlclient-dev -y`
* `git clone <this repo>`
* `cd thecodebase`
* `pip install -e .`
* `python init_db.py`
* `flask run`
