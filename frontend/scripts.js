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