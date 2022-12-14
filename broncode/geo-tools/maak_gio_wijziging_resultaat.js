window.addEventListener('load', function () {

    function MaakLink(downloadLink, key, mimeType) {
        var tekst = document.getElementById(downloadLink.dataset[key]).value
        var textFileAsBlob = new Blob([tekst], { type: mimeType });
        downloadLink.download = downloadLink.dataset['filenaam'];
        if (window.webkitURL !== null) {
            downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
        }
        else {
            downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
        }
    }

    document.querySelectorAll('[data-download_xml]').forEach(downloadLink => {
        MaakLink(downloadLink, 'download_xml', 'text/xml');
    });
    document.querySelectorAll('[data-download_json]').forEach(downloadLink => {
        MaakLink(downloadLink, 'download_json', 'application/json');
    });

    document.querySelectorAll('[data-copy]').forEach(copyLink => {
        copyLink.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();
            var area = document.getElementById(e.srcElement.dataset['copy']);
            area.select();
            document.execCommand('copy');
        });
    });

});
