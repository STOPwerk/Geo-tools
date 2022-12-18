window.addEventListener('load', function () {

    document.querySelectorAll('[data-download]').forEach(downloadLink => {
        var tekst = document.getElementById(downloadLink.dataset['download']).value
        var textFileAsBlob = new Blob([tekst], { type: 'text/xml' });
        downloadLink.download = downloadLink.dataset['filenaam'];
        if (window.webkitURL !== null) {
            downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
        }
        else {
            downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
        }
    });

    document.querySelectorAll('[data-copy]').forEach(copyLink => {
        copyLink.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();
            var area = document.getElementById(e.srcElement.dataset['copy']);
            area.select();
            document.execCommand('copy');
            area.selectionStart = 0;
            area.selectionEnd = 0;
        });
    });

});
