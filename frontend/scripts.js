function GetQuote(){

    const request = new Request('http://127.0.0.1:5000/random_quote?number=1');
    fetch(request)
        .then(response => response.json())
        .then(data => {

            data = data.quotes[0]

            document.getElementById('text-quote').innerHTML = data.quote;
            document.getElementById('author-info').innerHTML = "- " + data.author;

        })
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    console.log("ciao")
    return "";
    }