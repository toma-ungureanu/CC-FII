function get_service_info(number)
{
    document.getElementById("usrform1").addEventListener("click", function(event)
    {event.preventDefault()});
    document.getElementById("usrform2").addEventListener("click", function(event)
    {event.preventDefault()});

    let xmlhttp;
    if (window.XMLHttpRequest)
    {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    let dataToSend = null;
    if(number === 1)
    {
        dataToSend = document.getElementById('usrform1Text').value;
    }
    else
    {
        dataToSend = document.getElementById('usrform2Text').value;
    }
    xmlhttp.open("POST", "../python/get_service_info.py", true);
    xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xmlhttp.onreadystatechange = function ()
    {
        if (this.readyState === 4 && this.status === 200)
        {
            let respDiv = document.createElement("div");
            let respDivParent = null;
            if(number === 1)
            {
                respDivParent = document.getElementById('service_1');
                if(document.getElementById('firstServiceResp') != null)
                {
                    document.getElementById('firstServiceResp').remove();
                }
                respDiv.setAttribute('class', 'firstServiceResp');
                respDiv.setAttribute('id', 'firstServiceResp');
            }
            else
            {
                respDivParent = document.getElementById('service_2');
                if(document.getElementById('secondServiceResp') != null)
                {
                    document.getElementById('secondServiceResp').remove();
                }
                respDiv.setAttribute('class', 'secondServiceResp');
                respDiv.setAttribute('id', 'secondServiceResp');
            }

            let respInfo = document.createElement("div");
            console.log(this.responseText);
            respInfo.innerHTML = this.responseText;
            respDiv.appendChild(respInfo);
            respDivParent.appendChild(respDiv);
        }
    };

    xmlhttp.send("&serviceID=" + JSON.stringify(number) + "&info=" + JSON.stringify(dataToSend));
}