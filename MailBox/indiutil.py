def get_patches(cur,subject,html,attachs,l):

    ##################### top###############
    top = rb''' {% load static %}

<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<title>MailBOX</title>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

<!-- Bootstrap CSS -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
</head>
<body>
<nav class="navbar navbar-expand-lg text-light bg-dark">
<a class="navbar-brand" href="#" disable>IMAP</a>
<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>

<div class="collapse navbar-collapse" id="navbarSupportedContent">
<ul class="navbar-nav mr-auto">
<li class="nav-item active">
<a class="nav-link" href="{% url 'pagenated' ''' + f"'{cur}'".encode() + rb''' 1 %}">''' +f'{cur}'.encode()+rb'''<span class="sr-only">(current)</span></a>
</li>

<li class="nav-item dropdown">
<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    Info
</a>
<div class="dropdown-menu" aria-labelledby="navbarDropdown">
    {% for k,v in D %}
    <a class=" nav-link disabled dropdown-item" href="#">{{k}} : {{v}}</a>
    <div class=" nav-link disabled dropdown-divider"></div>
    {% endfor %}

</div>
</li>
           <li class="text-dark">
          {% include "MailBox/delete.html" %}

          </li>
         <li class="text-dark">
          {% include "MailBox/move.html" %}
          </li>
    <li class="text-dark">
          {% include "MailBox/copy.html" %}
          </li>
</ul>
</div>
</nav>
'''
    ######################bottom part###############
    bottom = rb'''
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
</body>
</html>
'''
    Attachs = '{% '+ f'if  {l} >  0' + '%}  <hr> <h5> '+ f'{l} Attachments </h5>' + '{% endif %}'
    if l:
        for fn in attachs:
            Attachs += '<li><a href="{% static '+ f" 'MailBoX/{fn}' " + '%}" download> '+ f'{fn} </a> </li>'

    ######################################
    card = rf'''<div class="border-dark border-3 mt-4 mb-4 card" style="width: 70%; margin-left: 15%;box-shadow: 10px 10px 5px #aaaaaa; border: 1px solid #BFBFBF;z-index:10;">
<div class="card-header bg-info">
<h4>{subject}</h4>
</div>
<div class="card-body">
<blockquote class="blockquote mb-0">
{html}
</blockquote>
{Attachs}
</div>

</div>'''.encode()


    return top,bottom,card
