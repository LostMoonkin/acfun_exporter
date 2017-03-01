var labels = new Array();
labels['综合'] = 'Comprehensive'
labels['工作·情感'] = 'Work'
labels['动漫文化']  = 'Anime'
labels['漫画·小说'] = 'Comic'
labels['游戏'] = 'Game'

api_url = 'http://localhost:8080/api/v0.1/top_articles/latest'

function get_top_articles(url, callback) {
    $.ajax({
        url: api_url,
        type: 'GET',
        async: true,
        timeout: 5000,
        dataType: 'json',
        success: function(data,textStatus,jqXHR){
            show_articls(data)
    },
        error: function(xhr,textStatus){
            console.log('Error')
            console.log(xhr)
            console.log(textStatus)
    },
    })
}

function show_articls(articles) {
        for (var i in articles) {
            var article = articles[i]
            add_row(labels[article.type], article)
            console.log(article.type)
        }
    }

function add_row(id, article) {
    table_id = '#' + id
    var new_row = '<tbody><tr><td class="title">' + article.title + 
    '</td><td class="views">' + article.info.views +
    '</td><td class="comments">' + article.info.comments +
    '</td><td class="time">' + article.info.time +
    '</td><td class="url"> <a target="_blank" href=' + article.url + '>' + get_url(article.url) + '</a></td></tr></tbody>'
    $(table_id).append(new_row)
}

function get_url(url) {
    re = new RegExp("/(ac.*)")
    return url.match(re)[0].replace('/','')
}

document.addEventListener('DOMContentLoaded', function () {
    // var article = {
    //     title: '123',
    //     views: 1000,
    //     comments: 120,
    //     url: 'http://www.acfun.cn'
    // }
    // add_row('Comprehensive', article)
    get_top_articles(api_url, show_articls)
});
