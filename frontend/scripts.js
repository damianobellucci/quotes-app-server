function GetQuote(){

    const request = new Request('http://127.0.0.1:5000/random_quote?number=1');
    fetch(request)
        .then(response => response.json())
        .then(data => {

            data = data.quotes[0]

            /*remove present quote*/
            document.getElementById('quotes').innerHTML = '';


            var element = document.createElement("div");

            content = '<p>'
                      +
                      data.quote
                      +
                      '</p>'
                      +
                      '<div class=info-author>'
                      + data.author 
                      + ',   '
                      +data.info
                      +
                      '</div>'

            element.innerHTML = content
            document.getElementById('quotes').appendChild(element);
        })
}