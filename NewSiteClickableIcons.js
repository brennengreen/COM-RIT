// A small script created to make an icon both clickable but also
// robust so that it will change dynamically with the site
// avoiding all hard coding

var elements = document.getElementsByClassName("home-icon");

var onClick = function() {
    window.location.href = this.getElementsByTagName('a')[0].href;
}

for (i=0; i < elements.length; i++) {
    elements[i].addEventListener("click", onClick, false);
}

